#!/usr/bin/env python3
"""
Workshop Local Relay — bridges demo API requests to the Claude Code CLI subprocess.

Usage:
  pip install aiohttp
  python3 relay.py

Spawns `claude -p` for each request. Uses the operator's existing Claude Code
authentication (OAuth / keychain) — no separate Anthropic API key required.
The demo posts {system, user, model, max_tokens} to localhost:3001/v1/chat.

Two response modes:
  - Default JSON: returns {"content": "..."} when the subprocess finishes.
    Used by `/health` curl checks and any client that doesn't opt into SSE.
  - Streaming SSE: when the request includes `Accept: text/event-stream`,
    relay forwards `claude -p --output-format stream-json --include-partial-messages`
    NDJSON frames as Server-Sent Events. Each text_delta becomes
    `data: {"delta": "<chunk>"}\n\n`; the final aggregate becomes
    `data: {"done": true, "content": "<full result>"}\n\n`. Errors and
    timeouts arrive as `data: {"error": "<msg>"}\n\n`.

Prompt routing:
  - The demo's `system` field is passed as `--system-prompt` to override
    Claude Code's default agent system prompt. Without this override, every
    call carries the full Claude-Code-as-agent context (tool harness,
    permission prompts, etc.) which slows responses 3-5x and isn't relevant
    to demo completions.
  - The demo's `user` field is passed as the `-p` positional prompt.
  - Model defaults to claude-haiku-4-5 (fast enough for live demo pacing).
    Override globally via RELAY_MODEL env var.

Failure classification:
  Every error response — JSON body and SSE `error` event alike — carries a
  machine-readable class beside the existing human `error` string:
    failure_class      infrastructure | content | unknown
    failure_reason     quota_exhausted, timeout, prompt_too_long, ...
    failure_confidence high | medium | none
    failure_detail     <=200 chars of the diagnostics the verdict rests on
    classifier_version integer
  `error` is unchanged, so callers reading only that field keep working.
  Successful responses (and SSE `done` events) carry `completed: true` — the
  caller's evidence that a model turn happened, which is what separates "the
  answer was unusable" from "there was no answer". An unrecognized signature
  degrades to `unknown`; it is never folded into a neighbouring class.

Test: curl http://localhost:3001/health
"""
import asyncio
import json
import os
import re
import secrets
import shutil
from aiohttp import web

PORT = 3001
# Each call spawns a fresh `claude -p` subprocess. BRIEFER and BUILDER phases on
# typical workshop hardware land at ~250-300s for the unabridged forge demo
# prompts; 600s gives enough headroom for slower laptops without making real
# stalls take forever to surface. Override via RELAY_TIMEOUT_SEC.
TIMEOUT_SEC = int(os.environ.get('RELAY_TIMEOUT_SEC', '600'))
# Per-line buffer limit on the subprocess StreamReader. asyncio's default is
# 64 KB, but `claude --output-format stream-json` emits assistant-message
# snapshot lines that contain the FULL accumulated content for each chunk
# — those routinely exceed 64 KB once the model produces ~3K+ tokens of
# structured output, which throws LimitOverrunError mid-stream. 4 MB gives
# enough headroom for any realistic single-call output.
SUBPROC_LIMIT = int(os.environ.get('RELAY_SUBPROC_LIMIT', str(4 * 1024 * 1024)))
# Default model overrides the demo's request. Haiku 4.5 is ~3-4x faster
# than Sonnet 4.6 and adequate for the workflow-focused demo. Operators
# who want max-quality output can set RELAY_MODEL=claude-sonnet-4-6.
# Set to empty string to honor whatever model the demo requests.
DEFAULT_MODEL = os.environ.get('RELAY_MODEL', 'claude-haiku-4-5')


# ─── Access control ──────────────────────────────────────────────────────────
# THE THREAT THIS BLOCK EXISTS FOR
# --------------------------------
# This relay drives the operator's ALREADY-AUTHENTICATED `claude` CLI. Until
# this block existed it answered every caller with
# `Access-Control-Allow-Origin: *` and required no credential of any kind.
# `--tools ""` was the only thing standing between a caller and tool
# execution, it sat one argument away from `--permission-mode
# bypassPermissions`, and NO TEST ASSERTED EITHER. Meanwhile ATTENDEE-SETUP.md
# tells attendees to start the relay and leave it running.
#
# THE 127.0.0.1 BIND IS NOT AUTHENTICATION. It keeps the relay off the
# conference network, and that is worth having, but the browser IS on
# 127.0.0.1. Every page the attendee had open could POST to localhost:3001,
# spend their subscription, and read the answer. Loopback stops the room; it
# does not stop the tab.
#
# THE CONTROL IS THE BEARER TOKEN. The origin allowlist below it is defence in
# depth and must never be mistaken for the control — see origin_allowed().

MIN_TOKEN_LEN = 16


def _init_token():
    """Per-run token. Minted from `secrets` unless the operator supplies one.

    A supplied token shorter than MIN_TOKEN_LEN is a hard startup failure, not
    a warning: a control that quietly accepts `RELAY_TOKEN=test` is not a
    control. Refusing to start is the only outcome an operator cannot miss.
    """
    supplied = os.environ.get('RELAY_TOKEN', '').strip()
    if not supplied:
        return secrets.token_urlsafe(32), True
    if len(supplied) < MIN_TOKEN_LEN:
        raise SystemExit(
            f'[RELAY] FATAL: RELAY_TOKEN is {len(supplied)} characters; at '
            f'least {MIN_TOKEN_LEN} are required. Unset RELAY_TOKEN and the '
            'relay will mint a strong one for you.')
    return supplied, False


RELAY_TOKEN, TOKEN_WAS_MINTED = _init_token()

# Extends the token requirement to NON-browser clients too (curl, scripts,
# the test harness). Off by default because the threat this control answers is
# a web page in the attendee's browser, and a local non-browser process
# already owns the shell — it can run `claude` itself and never touch the
# relay. On for an operator who wants the stricter posture anyway.
STRICT_AUTH = os.environ.get('RELAY_STRICT_AUTH', '').strip().lower() \
    not in ('', '0', 'false', 'no', 'off')

# Headers a browser attaches and page JavaScript CANNOT suppress: `Origin`,
# `Referer` and the `Sec-Fetch-*` set are all Forbidden Header Names, so
# `fetch()` may neither set nor delete them. Their presence is therefore
# reliable evidence that a request came from a browser — which is the whole
# population this control defends against. Their ABSENCE is not evidence of
# anything trustworthy, which is why it only ever relaxes the requirement for
# local non-browser callers, and why STRICT_AUTH exists to remove even that.
# The predicate fails CLOSED: any one of these present ⇒ token required.
_BROWSER_ONLY_HEADERS = ('Origin', 'Referer', 'Sec-Fetch-Site',
                         'Sec-Fetch-Mode', 'Sec-Fetch-Dest')

# file:// pages present `Origin: null`, and the demos are opened from the
# filesystem, so `null` has to be allowed. It is WEAK: a sandboxed iframe on
# ANY site also presents `null`, as do some redirect chains. The e2e suite
# serves the same pages over http on 127.0.0.1, so loopback http is allowed
# too. Neither of these is the control. The token is the control.
_LOCAL_ORIGIN_RE = re.compile(
    r'^http://(?:localhost|127\.0\.0\.1|\[::1\])(?::\d{1,5})?$', re.I)

AUTH_ERROR_TEXT = (
    'Relay token missing or incorrect. When the relay started it printed '
    '"[RELAY] Access token: ..." and a ready-made demo link containing it. '
    'Open the demo with that link, or paste the token when the demo asks. '
    'Programmatic callers send: Authorization: Bearer <token>'
)


def origin_allowed(origin):
    """True when `origin` may be echoed back in Access-Control-Allow-Origin.

    Defence in depth ONLY. `null` is allowed and `null` is forgeable by any
    site willing to host a sandboxed iframe, so this function can never be the
    thing that keeps a hostile page out. It narrows the casual case; token_ok()
    is what actually decides.
    """
    if not origin:
        return False
    if origin == 'null':
        return True
    return bool(_LOCAL_ORIGIN_RE.match(origin))


def allowed_origin_for(request):
    origin = request.headers.get('Origin')
    return origin if origin_allowed(origin) else None


def browser_originated(request):
    return any(h in request.headers for h in _BROWSER_ONLY_HEADERS)


def token_ok(request):
    """Constant-time comparison. `==` on a secret leaks its prefix length
    through timing; compare_digest does not. Both sides are encoded so a
    non-ASCII operator-supplied token cannot raise instead of returning False.
    """
    scheme, _, presented = request.headers.get('Authorization', '').partition(' ')
    if scheme.lower() != 'bearer':
        return False
    return secrets.compare_digest(presented.strip().encode('utf-8'),
                                  RELAY_TOKEN.encode('utf-8'))


def auth_required(request):
    return STRICT_AUTH or browser_originated(request)


# ─── DNS REBINDING: assessed, and deliberately NOT given a Host check ────────
# There is no Host-header validation in this file, on purpose. The reasoning is
# recorded here with the measurement behind it so the next reader can RE-DERIVE
# the verdict rather than inherit it — and can overturn it by re-measuring.
#
# THE ATTACK. Attendee opens a lure at http://evil.example:3001. That name has
# a ~0 TTL and the attacker re-points it at 127.0.0.1. The page then fetches
# http://evil.example:3001/v1/chat, which the browser now sends to THIS relay.
# Because the lure was served from the same scheme/host/port, the request is
# SAME-ORIGIN: no preflight, no CORS check, and the response body is readable
# by the attacker's script. The loopback bind does not help — the browser is on
# the host. `Host: evil.example:3001` arrives and nothing here looks at it.
#
# WHY IT STILL FAILS. security_mw does not consult the Origin allowlist to
# decide whether to demand a token; it consults browser_originated(), which
# fires on the mere PRESENCE of Origin / Referer / Sec-Fetch-{Site,Mode,Dest}.
# A rebound request is still sent BY A BROWSER, so it carries them, so a token
# is demanded, and the attacker does not have one: it is freshly minted per
# run, printed only to the operator's terminal, and compared with
# compare_digest. The rebinding gets the attacker a connection and a 401.
#
# MEASURED, not recalled, because the whole verdict rests on it. Headless
# Chromium 151.0.7922.34, page served over http from 127.0.0.1, page carrying
# <meta name="referrer" content="no-referrer"> — i.e. the attacker suppressing
# the one header they control. Same-origin requests, what actually arrived:
#
#   POST, application/json  Origin: yes   Referer: SUPPRESSED  Sec-Fetch-*: yes
#   GET                     Origin: no    Referer: SUPPRESSED  Sec-Fetch-*: yes
#   POST, text/plain        Origin: yes   Referer: SUPPRESSED  Sec-Fetch-*: yes
#   <img> subresource       Origin: no    Referer: SUPPRESSED  Sec-Fetch-*: yes
#
# browser_originated() is TRUE in all four. Referrer-Policy killed Referer in
# every one — the attacker really does control that — and Sec-Fetch-* survived
# it, because Fetch Metadata has no policy knob and is a Forbidden Header Name.
# Note also that Origin rides EVERY same-origin POST, which is the shape
# /v1/chat takes; that is a second, independent carrier on the only endpoint
# that spawns a subprocess.
#
# THE RESIDUAL, stated honestly. A browser old enough to send no Sec-Fetch-*
# at all (pre-Chrome-76 / pre-Firefox-90 / pre-Safari-16.4) with the attacker
# suppressing Referer would present a bare GET with nothing to key on, and
# GET /health would answer untokened. That is why _health_payload() carries no
# path and no username: the residual read is
# {status, claude_binary_present, classifier_version}, and there is nothing in
# it worth rebinding DNS to obtain. /v1/chat is not reachable that way at all,
# because its POST carries Origin on every browser generation that has fetch.
#
# SO NO HOST CHECK. It would be a second gate on a door the token already
# holds, and its only unique catch is a body that is now deliberately empty of
# secrets. An operator who wants the tail closed anyway has RELAY_STRICT_AUTH=1,
# which demands the token from EVERY caller including curl, and is one env var.
#
# WHAT WOULD OVERTURN THIS: widening _health_payload() to carry anything worth
# stealing, adding a route that answers something sensitive on GET, or removing
# a member of _BROWSER_ONLY_HEADERS. Any of those and the Host check earns its
# place. The bigger exposure on this endpoint is NOT rebinding — see the note
# on _build_args: a local non-browser process needs no token at all by design,
# so the containment argv, not this predicate, is what keeps /v1/chat from
# being command execution.


def cors(response):
    """Request-independent CORS headers.

    Access-Control-Allow-Origin is deliberately NOT set here. A value chosen
    without looking at the request's Origin header can only ever be a
    wildcard, and the wildcard is exactly the defect being removed. The
    origin-specific value is applied by apply_cors(), which can see the
    request.
    """
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = (
        'Content-Type, Accept, Authorization')
    response.headers['Vary'] = 'Origin'
    return response


def apply_cors(response, request):
    """Echo the request's Origin only when it is allowlisted. An origin that
    is not allowlisted gets NO Access-Control-Allow-Origin header at all, so
    the browser refuses to hand the response body to the page. Fail closed.

    Credentials are never allowed (no Access-Control-Allow-Credentials): this
    relay authenticates with a bearer token, never a cookie, so ambient
    browser credentials must not be in play.
    """
    if getattr(response, 'prepared', False):
        # An SSE StreamResponse already sent its headers; it sets its own
        # allowlisted origin at construction time in _handle_chat_sse.
        return response
    cors(response)
    allowed = allowed_origin_for(request)
    if allowed:
        response.headers['Access-Control-Allow-Origin'] = allowed
    return response


@web.middleware
async def security_mw(request, handler):
    """Single choke point. Every route is behind it, so a route added later
    is authenticated by default rather than by remembering to add a check.
    """
    if request.method != 'OPTIONS' and auth_required(request) \
            and not token_ok(request):
        # Preflight is exempt because a preflight cannot carry Authorization;
        # it reveals nothing and the real request behind it is still checked.
        info = _classification(CLASS_INFRA, 'relay_token_missing',
                               CONFIDENCE_HIGH,
                               'no valid bearer token on a request that '
                               'requires one')
        return apply_cors(fail_json(AUTH_ERROR_TEXT, info), request)
    response = await handler(request)
    return apply_cors(response, request)


def claude_path():
    return shutil.which('claude')


# ─── Failure classification ──────────────────────────────────────────────────
# WHY THIS EXISTS
# ---------------
# Every non-zero exit from the CLI subprocess used to become one 502 carrying
# one prose string. An exhausted quota, a dropped uplink, a crashed binary and
# a genuine model refusal were indistinguishable to the caller. A session once
# recorded — and had to withdraw — a CONTENT conclusion ("the degenerate brief
# hard-fails") that was in fact a session quota wall: the same call succeeded
# in 14s on clean quota. One error path had collapsed two different worlds into
# one string.
#
# The consequence this is really written for is the live stage. If the quota
# dies mid-run the room sees the pipeline stop on THEIR brief, and "it was the
# network" is both exactly what a speaker always says and unfalsifiable from
# the podium. The machine has to say which one it was.
#
# THE CLASSIFIER MUST BE ABLE TO SAY "I DO NOT KNOW".
# ---------------------------------------------------
# These signatures come from a third-party CLI whose messages we do not control
# and which WILL change. Every path below is written so that an unrecognized
# signature falls through to UNKNOWN:
#   * no signature match                      -> UNKNOWN (never "probably infra")
#   * signatures matching MORE THAN ONE class -> UNKNOWN, not first-wins
#   * empty diagnostics                       -> UNKNOWN
# UNKNOWN is a real answer with its own banner copy and its own status code. It
# is never silently folded into either neighbour. A classifier that cannot
# report "I do not know" is the same defect class as a verifier that was told
# what to conclude.
#
# WHERE EACH CLASS CAN ACTUALLY ORIGINATE (checked against the code paths; not
# inferred from what the classes sound like):
#   INFRASTRUCTURE — reachable on every error path here: spawn failure, missing
#       binary, timeout, signal kill, and any exit whose diagnostics carry a
#       quota / auth / network / upstream signature.
#   CONTENT       — barely reachable here, and that is correct. A genuine model
#       refusal is a SUCCESSFUL call: exit 0, refusal prose in `result`, served
#       as a 200. The relay does not read prose and does not judge refusals.
#       The only content failures visible at this layer are the ones rejected
#       BEFORE generation: an over-long prompt, a filtered input. Every other
#       content judgement belongs to the caller — which is why successful
#       responses now carry `completed: true`. That flag is the caller's
#       evidence that the model ran, and therefore that any failure it sees
#       downstream is a content failure and not a broken uplink.
#   UNKNOWN       — everything else, including protocol drift (the CLI stopped
#       emitting the JSON shape we parse) and a bare non-zero exit with silent
#       stderr, which is exactly what the withdrawn finding looked like.

CLASS_INFRA = 'infrastructure'
CLASS_CONTENT = 'content'
CLASS_UNKNOWN = 'unknown'

CONFIDENCE_HIGH = 'high'
CONFIDENCE_MEDIUM = 'medium'
CONFIDENCE_NONE = 'none'

# Bump when the signature table or the reason vocabulary changes, so a caller
# (or a recorded transcript) can tell which classifier produced a verdict.
CLASSIFIER_VERSION = 1

# (compiled pattern, class, reason). Matched against stderr + stdout + detail.
# Patterns are deliberately narrow. A pattern broad enough to catch more cases
# is also broad enough to produce a CONFIDENT WRONG ANSWER, which is strictly
# worse than UNKNOWN here.
_SIGNATURES = [
    # ── CONTENT: the request was rejected for WHAT IT ASKED, before the model
    # produced an answer. These are the only content failures this layer can
    # legitimately see.
    (re.compile(r'prompt is too long', re.I), CLASS_CONTENT, 'prompt_too_long'),
    (re.compile(r'input length and .{0,30}max_tokens', re.I),
     CLASS_CONTENT, 'prompt_too_long'),
    (re.compile(r'(context (window|length)|maximum context)\D{0,40}'
                r'(exceed|too long|too large)'
                r'|exceed\w*\D{0,40}(context (window|length)|maximum context)', re.I),
     CLASS_CONTENT, 'prompt_too_long'),
    (re.compile(r'blocked by content filtering|content[_ ]filter(ing|ed)\b', re.I),
     CLASS_CONTENT, 'content_filtered'),

    # ── INFRASTRUCTURE: the plumbing, not the brief.
    (re.compile(r'usage limit reached|rate[_ ]?limit|\b429\b|\bquota\b'
                r'|too many requests|limits? will reset'
                r'|credit balance is too low|out of credits|insufficient credit', re.I),
     CLASS_INFRA, 'quota_exhausted'),
    (re.compile(r'\b401\b|\b403\b|unauthorized|forbidden'
                r'|authentication[_ ]error|invalid api[ _]key|invalid x-api-key'
                r'|not logged in|please run .{0,3}claude (login|setup-token)'
                r'|oauth\D{0,30}(expired|invalid|revoked)'
                r'|credentials? (are )?(expired|missing|invalid)', re.I),
     CLASS_INFRA, 'auth_unavailable'),
    (re.compile(r'ENOTFOUND|ECONNREFUSED|ECONNRESET|EAI_AGAIN|ETIMEDOUT'
                r'|EHOSTUNREACH|ENETUNREACH|getaddrinfo|socket hang up'
                r'|fetch failed|network (error|is unreachable)'
                r'|unable to (connect|resolve)|\bTLS\b|\bSSL\b'
                r'|certificate (has expired|verify failed)'
                r'|self.signed certificate', re.I),
     CLASS_INFRA, 'network_unreachable'),
    (re.compile(r'overloaded|service unavailable|bad gateway'
                r'|internal server error'
                r'|(status|code|error)\D{0,10}\b(500|502|503|529)\b', re.I),
     CLASS_INFRA, 'upstream_unavailable'),
    (re.compile(r'command not found|Exec format error|Permission denied'
                r'|cannot find module|MODULE_NOT_FOUND|bad option'
                r'|Segmentation fault|core dumped', re.I),
     CLASS_INFRA, 'cli_unusable'),
    (re.compile(r'out of memory|heap out of memory|ENOMEM|ENOSPC|EMFILE'
                r'|no space left on device', re.I),
     CLASS_INFRA, 'local_resource_exhausted'),
]


def _classification(cls, reason, confidence, detail):
    return {
        'failure_class': cls,
        'failure_reason': reason,
        'failure_confidence': confidence,
        'failure_detail': detail,
        'classifier_version': CLASSIFIER_VERSION,
    }


# ─── Identity redaction for outbound diagnostic text ─────────────────────────
# MEASURED, not inferred. Driving the real handlers with a fake CLI whose
# stderr named the operator's home directory, this arrived on the wire — on
# BOTH the JSON and the SSE path, in BOTH the `error` and the `failure_detail`
# field, and on the operator's terminal via _log_failure:
#
#   "error": "Claude AI usage limit reached|1756400000\n
#             at loadConfig (<HOME>/.claude/settings.json:12)\n
#             cwd=<HOME>/working/<a-project-name>"
#
# <HOME> stands for the real home directory, which is written out in full on
# the wire. It is a placeholder HERE because this file ships to attendees: a
# comment that documents a disclosure by pasting the disclosed value is the
# same defect wearing an explanation. (Caught by a username scan of this file
# after the fix was written -- the /health shape-detector does not read source
# comments, and nothing else was looking.)
#
# Three populations can read that. The token holder is entitled to it. A local
# non-browser process needs no token here BY DESIGN, but it can already read
# the filesystem, so the relay tells it nothing new. The third is the one that
# matters: THE PROJECTOR. These demos are driven live at a conference, the
# failure banner is rendered on stage, and the operator's terminal is on screen
# during setup. A working-directory name is a client or project name.
#
# The demos already carry a client-side redactPaths(). It is NOT sufficient and
# this is not a duplicate of it:
#   * it is CLIENT-SIDE, so curl, capture_live_campaign.py, any recording of
#     the raw response, and _log_failure's terminal line all bypass it;
#   * measured, it leaves `cwd=/home/<user>/working/<repo>` COMPLETELY
#     UNTOUCHED, because its regex requires the path to follow whitespace or a
#     bracket and `=` is neither — and `cwd=`/`path=`/`file=` is a very common
#     shape in tool output;
#   * measured, it collapses a bare `/home/<user>` to `.../<user>`, which
#     KEEPS the username as the surviving last segment.
# Redacting at the source fixes all three for every consumer at once.
#
# WHY THIS COSTS NO CLASSIFIER SIGNAL, which is the property that matters most:
# classify_failure() matches its signature table against `evidence`, and only
# then slices `snippet` for display. Redaction is applied to the SNIPPET and to
# the outbound message, never to the text the matcher sees. The class, reason
# and confidence are computed from unredacted evidence and are bit-for-bit what
# they were. A quota wall still reads as quota_exhausted, live, on stage.
#
# DELIBERATELY NARROW: this removes the operator's IDENTITY (the home prefix),
# not paths in general. `/etc/foo` and `./config.json` are diagnostic and stay.
# A bare username token is NOT redacted either — a login name like "claude" or
# "test" would mangle unrelated prose, and mangled diagnostics on stage are the
# defect this whole classifier exists to prevent.
_HOME_PREFIXES = tuple(sorted(
    {p for p in (os.path.expanduser('~'), os.path.realpath(os.path.expanduser('~')))
     if p and len(p) > 1 and p != os.sep},
    key=len, reverse=True))

# Windows: C:\Users\<name> and \Users\<name>, any drive, any case.
_WIN_HOME_RE = re.compile(r'(?:[A-Za-z]:)?\\Users\\[^\\/:*?"<>|\r\n]+', re.I)


def _redact_identity(text):
    """Replace the operator's home directory with `~` in outbound text.

    Applied to what LEAVES the relay, never to what the classifier reads.
    """
    if not text:
        return text
    out = str(text)
    for prefix in _HOME_PREFIXES:
        out = out.replace(prefix, '~')
    return _WIN_HOME_RE.sub('~', out)


def _match_signatures(text):
    """Every signature that fires, in table order. Returns [(class, reason)]."""
    if not text:
        return []
    return [(cls, reason) for rx, cls, reason in _SIGNATURES if rx.search(text)]


def classify_failure(origin, returncode=None, stderr='', stdout='', detail=''):
    """Classify one relay failure as INFRASTRUCTURE / CONTENT / UNKNOWN.

    `origin` names WHERE the failure was observed, which is evidence the
    diagnostic text cannot supply:
        'cli_missing' — no `claude` on PATH
        'spawn'       — the subprocess could not be started at all
        'timeout'     — the relay killed the call on its own clock
        'exit'        — the subprocess exited non-zero
        'cli_result'  — the CLI itself reported an error in its result frame
        'protocol'    — the CLI ran but did not emit the shape we parse
        'exception'   — an unexpected relay-side exception

    Pure function: no I/O, no globals, no subprocess. Unit-testable directly.
    """
    evidence = '\n'.join(t for t in (stderr, stdout, detail) if t).strip()
    # `evidence` stays RAW: every _match_signatures() call below reads it, and
    # redacting it would change classification. `snippet` is display-only, so
    # it is the correct and only place to redact. See _redact_identity().
    snippet = _redact_identity(evidence[-200:])

    # Structural certainties. These do not depend on any third-party message
    # text, so they survive the CLI changing its wording.
    if origin == 'timeout':
        return _classification(CLASS_INFRA, 'timeout', CONFIDENCE_HIGH, snippet)
    if origin == 'cli_missing':
        return _classification(CLASS_INFRA, 'cli_missing', CONFIDENCE_HIGH, snippet)

    hits = _match_signatures(evidence)
    classes = {cls for cls, _ in hits}
    if len(classes) > 1:
        # Two signatures disagreeing is LESS information than one, not more.
        # First-wins here would be a coin flip wearing a confidence label.
        return _classification(CLASS_UNKNOWN, 'ambiguous_signature',
                               CONFIDENCE_NONE, snippet)
    if len(classes) == 1:
        return _classification(hits[0][0], hits[0][1], CONFIDENCE_HIGH, snippet)

    # ── Nothing matched. Only structural facts may speak from here on. ──
    if origin == 'spawn':
        # Spawning is entirely local; the model was never reached. Infrastructure
        # by construction, not by pattern guess.
        return _classification(CLASS_INFRA, 'spawn_failed', CONFIDENCE_HIGH, snippet)
    if returncode is not None and (returncode < 0 or returncode in (137, 143)):
        # Killed by a signal (SIGKILL/SIGTERM, OOM killer, operator Ctrl-C).
        # Outside the model either way, but we did not observe the cause.
        return _classification(CLASS_INFRA, 'process_killed',
                               CONFIDENCE_MEDIUM, snippet)
    if origin == 'protocol':
        return _classification(CLASS_UNKNOWN, 'protocol_mismatch',
                               CONFIDENCE_NONE, snippet)
    if not snippet:
        return _classification(CLASS_UNKNOWN, 'no_diagnostic_output',
                               CONFIDENCE_NONE, '')
    return _classification(CLASS_UNKNOWN, 'unrecognized_signature',
                           CONFIDENCE_NONE, snippet)


# Reasons whose HTTP status predates the classifier. Preserved so existing
# callers that learned these codes keep seeing them.
_STATUS_BY_REASON = {'timeout': 504, 'cli_missing': 500, 'bad_request': 400,
                     'relay_token_missing': 401}
_STATUS_BY_CLASS = {CLASS_INFRA: 503, CLASS_CONTENT: 422, CLASS_UNKNOWN: 502}


def status_for(info):
    """HTTP status for a classification. UNKNOWN keeps the historical 502."""
    if info['failure_reason'] in _STATUS_BY_REASON:
        return _STATUS_BY_REASON[info['failure_reason']]
    return _STATUS_BY_CLASS.get(info['failure_class'], 502)


def _log_failure(msg, info):
    print(f"[RELAY] FAILURE class={info['failure_class']} "
          f"reason={info['failure_reason']} "
          f"confidence={info['failure_confidence']} :: {str(msg)[:160]}",
          flush=True)


def fail_json(msg, info):
    """Error response. `error` keeps the wording it always had; the only
    change is that the operator's home directory is collapsed to `~` before it
    leaves the process. Callers reading only that field are unaffected.

    Redacting HERE rather than at each call site means a future error path
    cannot forget to do it, and _log_failure() below is inside the redaction
    so the operator's terminal -- which is on screen during setup -- is
    covered by the same edit."""
    msg = _redact_identity(msg)
    _log_failure(msg, info)
    body = {'error': msg}
    body.update(info)
    return cors(web.json_response(body, status=status_for(info)))


def fail_event(msg, info):
    """Same contract on the SSE wire, where there is no status code to carry
    it. `error` keeps its existing string; the class rides beside it. Same
    identity redaction as fail_json -- the SSE path was measured leaking the
    identical bytes, so a fix on only one path would have been half a fix."""
    msg = _redact_identity(msg)
    _log_failure(msg, info)
    payload = {'error': msg}
    payload.update(info)
    return payload


async def handle_options(request):
    return cors(web.Response(status=204))


def _health_payload():
    """The /health body, built WITHOUT touching aiohttp so a test can assert
    on the actual dict rather than on a mock of it.

    DELIBERATELY PATH-FREE, and that is a security property, not tidiness.

    /health is UNAUTHENTICATED for a non-browser caller: auth_required() is
    `STRICT_AUTH or browser_originated(request)`, and curl sends no Origin,
    no Referer and no Sec-Fetch-* header, so in the default posture a bare
    `curl http://localhost:3001/health` is answered with no token at all.
    ATTENDEE-SETUP.md documents exactly that call.

    This response used to carry `claude_binary_path`, the full return of
    shutil.which('claude'). On a stock install that is
    /home/<username>/.local/bin/claude -- so the endpoint handed out the
    operator's ACCOUNT NAME and HOME DIRECTORY to any unauthenticated local
    caller. That is CWE-200 (exposure of sensitive information to an
    unauthorized actor), and the population that matters is not hypothetical:
    this relay ships to attendees at a security conference, who are told to
    start it and leave it running on machines nobody controls. Any other
    process on the box -- and, on the loopback-reachable paths a browser can
    be steered down, any page that gets a response body -- could read a
    username off it.

    The path was never what the documented purpose needed. ATTENDEE-SETUP.md
    tells the reader that `"claude_binary_present": true` means they are
    ready, and the troubleshooting entry for the false case already sends
    them to `which claude` in their OWN shell -- which answers the question
    locally, for the person entitled to the answer, without publishing it.

    So: presence is a BOOLEAN, and no value in this dict is a filesystem
    path. test_workshop.py enforces that over EVERY value, by shape rather
    than by key name, so a path cannot re-enter under a new key.
    """
    return {
        'status': 'ok',
        # bool(), not the path. See the docstring above before widening this.
        'claude_binary_present': bool(claude_path()),
        # Lets a caller feature-detect the failure-classification contract
        # instead of assuming it. An older relay omits this key entirely.
        'classifier_version': CLASSIFIER_VERSION,
    }


async def handle_health(request):
    return cors(web.json_response(_health_payload()))


def _build_args(binary, system, model, streaming):
    # --tools ""               : strip the entire built-in tool set so the
    #                            model isn't reasoning about Read/Write/Bash/
    #                            WebSearch/etc. on every call. Cuts input
    #                            from ~30k cached tokens to ~3k.
    # --disable-slash-commands : skip skill/slash-command resolution.
    # --setting-sources ""     : skip CLAUDE.md auto-discovery and hooks.
    # Together these turn `claude -p` into a thin LLM-completion endpoint
    # rather than a full Claude-Code-as-agent invocation.
    #
    # The USER prompt is piped via stdin (not -p arg) — by Phase 3 the
    # accumulated context (architecture doc + advisor outputs + collection
    # design + research instructions) routinely exceeds the kernel's ARG_MAX
    # when passed as an exec argument. The SYSTEM prompt stays as
    # --system-prompt since it's bounded by the advisor template.
    args = [
        binary,
        '-p',
        '--model', model,
        '--no-session-persistence',
        '--permission-mode', 'bypassPermissions',
        '--tools', '',
        '--disable-slash-commands',
        '--setting-sources', '',
    ]
    if streaming:
        # stream-json + include-partial-messages emits NDJSON content_block_delta
        # frames as the model produces them. --verbose is required by the CLI
        # when combining stream-json with --print.
        args += ['--output-format', 'stream-json',
                 '--include-partial-messages', '--verbose']
    else:
        args += ['--output-format', 'json']
    if system:
        args += ['--system-prompt', system]
    return args


def _per_call_timeout(request) -> int:
    """Honor `?timeout=N` query param so a recovery banner's 'Continue
    waiting' button can extend the budget for one specific call without
    restarting the relay. Clamped to [60, 1800] to avoid silly values."""
    raw = request.rel_url.query.get('timeout')
    if not raw:
        return TIMEOUT_SEC
    try:
        n = int(raw)
    except ValueError:
        return TIMEOUT_SEC
    return max(60, min(1800, n))


async def handle_chat(request):
    try:
        body = await request.json()
    except Exception:
        # A malformed body is the local harness misbehaving, never the brief.
        return fail_json('Invalid JSON body', _classification(
            CLASS_INFRA, 'bad_request', CONFIDENCE_HIGH,
            'request body was not valid JSON'))

    binary = claude_path()
    if not binary:
        return fail_json(
            'Claude Code CLI not found on PATH. Install Claude Code to use this provider.',
            classify_failure('cli_missing', detail='claude not found on PATH'))

    system = body.get('system', '')
    user = body.get('user', '')
    model = DEFAULT_MODEL or body.get('model', 'claude-haiku-4-5')
    timeout = _per_call_timeout(request)

    accept = request.headers.get('Accept', '')
    if 'text/event-stream' in accept:
        return await _handle_chat_sse(request, binary, system, user, model, timeout)

    args = _build_args(binary, system, model, streaming=False)

    try:
        proc = await asyncio.create_subprocess_exec(
            *args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            limit=SUBPROC_LIMIT,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(input=user.encode('utf-8')), timeout=timeout
            )
        except asyncio.TimeoutError:
            try:
                proc.kill()
            except ProcessLookupError:
                pass
            return fail_json(
                f'claude CLI timeout ({timeout}s)',
                classify_failure('timeout',
                                 detail=f'no completion within {timeout}s'))

        stderr_text = stderr.decode('utf-8', errors='replace').strip()
        stdout_text = stdout.decode('utf-8', errors='replace')

        if proc.returncode != 0:
            # This is the branch the withdrawn finding died on: a quota wall,
            # a dropped uplink, a crashed CLI and a rejected prompt all exited
            # non-zero and all became the same 502 string. The message is
            # unchanged; the class beside it is the whole fix.
            err = stderr_text or f'claude exited with code {proc.returncode}'
            return fail_json(err, classify_failure(
                'exit', returncode=proc.returncode,
                stderr=stderr_text, stdout=stdout_text[:2000]))

        try:
            data = json.loads(stdout_text)
        except json.JSONDecodeError:
            # The CLI ran but did not emit the shape we parse. It may have
            # printed a plain-text diagnostic instead, so the signatures still
            # get a look at stdout; absent a match this is protocol drift,
            # which is UNKNOWN and must not be guessed into either neighbour.
            return fail_json(
                'claude returned non-JSON output (run `claude --version` to confirm CLI version supports --output-format json)',
                classify_failure('protocol', returncode=proc.returncode,
                                 stderr=stderr_text, stdout=stdout_text[:2000]))

        content = data.get('result')
        if content is None:
            return fail_json(
                f'claude JSON missing "result" field: {list(data.keys())}',
                classify_failure('protocol', returncode=proc.returncode,
                                 stderr=stderr_text,
                                 stdout=json.dumps(sorted(data.keys()))))

        # Success. `completed: true` is the caller's positive evidence that a
        # model turn actually happened — the flag that lets a browser say "the
        # system answered and the answer was unusable" instead of guessing.
        out = {'content': content, 'completed': True}
        if data.get('is_error'):
            # Exit 0 but the CLI flagged the turn. We still hand back the text
            # (that is what the caller saw produced), mirroring the SSE
            # recovered path, but we say so rather than passing it off clean.
            out['recovered'] = True
            out['cli_error'] = str(data.get('subtype') or 'claude reported an error')
        return cors(web.json_response(out))
    except FileNotFoundError:
        return fail_json(
            'Claude Code CLI not found on PATH. Install Claude Code to use this provider.',
            classify_failure('cli_missing', detail='claude vanished from PATH between check and exec'))
    except Exception as e:
        return fail_json(str(e), classify_failure('exception', detail=str(e)))


async def _handle_chat_sse(request, binary, system, user, model, timeout=None):
    if timeout is None:
        timeout = TIMEOUT_SEC
    args = _build_args(binary, system, model, streaming=True)

    # These headers go out with response.prepare() below, before any middleware
    # could touch them, so the allowlisted origin is resolved HERE. An origin
    # that is not allowlisted simply gets no ACAO header and the browser drops
    # the stream — the same fail-closed behaviour as the JSON path.
    sse_headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Accel-Buffering': 'no',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Accept, Authorization',
        'Vary': 'Origin',
    }
    _allowed = allowed_origin_for(request)
    if _allowed:
        sse_headers['Access-Control-Allow-Origin'] = _allowed

    response = web.StreamResponse(status=200, headers=sse_headers)
    await response.prepare(request)

    async def send_event(payload):
        try:
            await response.write(f'data: {json.dumps(payload)}\n\n'.encode('utf-8'))
        except (ConnectionResetError, asyncio.CancelledError):
            raise

    try:
        proc = await asyncio.create_subprocess_exec(
            *args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            limit=SUBPROC_LIMIT,
        )
    except FileNotFoundError:
        await send_event(fail_event(
            'Claude Code CLI not found on PATH. Install Claude Code to use this provider.',
            classify_failure('cli_missing', detail='claude not found on PATH')))
        await response.write_eof()
        return response
    except Exception as e:
        await send_event(fail_event(
            f'failed to spawn claude: {e}',
            classify_failure('spawn', detail=str(e))))
        await response.write_eof()
        return response

    # Send the user prompt over stdin (avoids ARG_MAX when context is large)
    # then close stdin so the CLI starts processing immediately.
    try:
        proc.stdin.write(user.encode('utf-8'))
        await proc.stdin.drain()
        proc.stdin.close()
    except (ConnectionResetError, BrokenPipeError):
        pass

    stderr_tail = bytearray()

    async def drain_stderr():
        nonlocal stderr_tail
        assert proc.stderr is not None
        while True:
            chunk = await proc.stderr.read(4096)
            if not chunk:
                return
            stderr_tail.extend(chunk)
            # Keep only the last 2KB so a chatty stderr can't blow memory.
            if len(stderr_tail) > 2048:
                del stderr_tail[:-2048]

    stderr_task = asyncio.create_task(drain_stderr())

    full_content = ''
    delta_count = 0
    timed_out = False
    completed = False
    # Stall watchdog state: surface a non-fatal warning to the demo when no
    # text_delta arrives for STALL_WARN_SEC. Keeps the operator's UI from
    # going silent during long thinking pauses without bailing the call.
    last_delta_at = asyncio.get_event_loop().time()
    stall_warned = False
    STALL_WARN_SEC = 30

    async def stall_watcher():
        nonlocal stall_warned
        while not completed and not timed_out:
            await asyncio.sleep(5)
            if completed or timed_out:
                return
            gap = asyncio.get_event_loop().time() - last_delta_at
            if gap > STALL_WARN_SEC and not stall_warned:
                stall_warned = True
                try:
                    await send_event({'warning': f'stalled — no token in {int(gap)}s'})
                except Exception:
                    return

    stall_task = asyncio.create_task(stall_watcher())
    try:
        async def pump():
            nonlocal full_content, delta_count, completed, last_delta_at, stall_warned
            assert proc.stdout is not None
            while True:
                line = await proc.stdout.readline()
                if not line:
                    return
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                t = obj.get('type')
                if t == 'stream_event':
                    ev = obj.get('event') or {}
                    if ev.get('type') == 'content_block_delta':
                        d = ev.get('delta') or {}
                        if d.get('type') == 'text_delta':
                            chunk = d.get('text') or ''
                            if chunk:
                                full_content += chunk
                                delta_count += 1
                                last_delta_at = asyncio.get_event_loop().time()
                                stall_warned = False
                                await send_event({'delta': chunk})
                elif t == 'result':
                    canonical = obj.get('result')
                    if obj.get('is_error'):
                        # The CLI reported a post-completion error (e.g.
                        # transient API hiccup at the very end of the stream).
                        # If we already streamed visible text, treat the run
                        # as successful and surface the streamed content —
                        # the user saw it produced cleanly. Only surface the
                        # error when we have no content to fall back on.
                        if full_content:
                            completed = True
                            await send_event({
                                'done': True,
                                'completed': True,
                                'content': full_content,
                                'deltas': delta_count,
                                'recovered': True,
                                'cli_error': str(canonical) if canonical else 'claude reported an error',
                            })
                            return
                        cli_msg = (str(canonical) if canonical
                                   else 'claude reported an error')
                        await send_event(fail_event(cli_msg, classify_failure(
                            'cli_result', stdout=cli_msg,
                            stderr=bytes(stderr_tail).decode('utf-8', errors='replace'))))
                        return
                    if isinstance(canonical, str) and canonical:
                        # Prefer the canonical aggregate when available — it
                        # captures any text we missed via partial frames.
                        out_content = canonical
                    else:
                        out_content = full_content
                    completed = True
                    await send_event({'done': True, 'completed': True,
                                      'content': out_content,
                                      'deltas': delta_count})
                    return

        try:
            await asyncio.wait_for(pump(), timeout=timeout)
        except asyncio.TimeoutError:
            timed_out = True
            try:
                proc.kill()
            except ProcessLookupError:
                pass
            tail = bytes(stderr_tail).decode('utf-8', errors='replace').strip()
            tail = tail[-200:] if tail else ''
            msg = f'claude CLI timeout ({timeout}s)'
            if tail:
                msg += f' — stderr tail: {tail}'
            await send_event(fail_event(msg, classify_failure(
                'timeout', stderr=tail,
                detail=f'no completion within {timeout}s')))
    except (ConnectionResetError, asyncio.CancelledError):
        try:
            proc.kill()
        except ProcessLookupError:
            pass
        raise
    finally:
        try:
            await asyncio.wait_for(proc.wait(), timeout=2)
        except (asyncio.TimeoutError, ProcessLookupError):
            try:
                proc.kill()
            except ProcessLookupError:
                pass
        stderr_task.cancel()
        try:
            await stderr_task
        except (asyncio.CancelledError, Exception):
            pass
        stall_task.cancel()
        try:
            await stall_task
        except (asyncio.CancelledError, Exception):
            pass

    # Skip the post-stream exit-code check when pump() already emitted a done
    # event — the CLI's exit code is informational at that point and surfacing
    # it as an error would mask a successful streamed completion.
    if not completed and not timed_out and proc.returncode not in (0, None):
        tail = bytes(stderr_tail).decode('utf-8', errors='replace').strip()
        tail = tail[-200:] if tail else ''
        err = f'claude exited with code {proc.returncode}'
        if tail:
            err += f' — stderr tail: {tail}'
        await send_event(fail_event(err, classify_failure(
            'exit', returncode=proc.returncode, stderr=tail)))

    await response.write_eof()
    return response


async def main():
    # Every route is behind security_mw, so a route added later is
    # authenticated by default instead of by remembering to add a check.
    app = web.Application(middlewares=[security_mw])
    app.router.add_route('OPTIONS', '/{path_info:.*}', handle_options)
    app.router.add_get('/health', handle_health)
    app.router.add_post('/v1/chat', handle_chat)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', PORT)
    await site.start()

    binary = claude_path()
    if binary:
        print(f'[RELAY] claude CLI: {binary}')
    else:
        print('[RELAY] WARNING: claude CLI not found on PATH — install Claude Code before running demos.')
    print(f'[RELAY] Model: {DEFAULT_MODEL or "(demo-supplied)"} (override with RELAY_MODEL=...)')
    print(f'[RELAY] Per-call timeout: {TIMEOUT_SEC}s (override with RELAY_TIMEOUT_SEC=...)')
    print(f'[RELAY] Listening on http://localhost:{PORT}')
    print('[RELAY] ' + '-' * 66)
    if TOKEN_WAS_MINTED:
        print(f'[RELAY] Access token: {RELAY_TOKEN}')
        print('[RELAY]   Freshly minted for THIS run. It changes every restart.')
    else:
        print(f'[RELAY] Access token: {RELAY_TOKEN}   (from RELAY_TOKEN)')
    if STRICT_AUTH:
        print('[RELAY]   RELAY_STRICT_AUTH is on: EVERY request needs the token.')
    else:
        print('[RELAY]   Every browser request needs this token. Local '
              'non-browser')
        print('[RELAY]   callers (curl, scripts) do not, unless you set '
              'RELAY_STRICT_AUTH=1.')
    print('[RELAY]')
    print('[RELAY] Open a demo with the token already attached '
          '(click or copy):')
    _demos = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'demos')
    _any = False
    for _name in ('swarm-factory-live.html', 'swarm-cage-live.html',
                  'improvement-loop-live.html'):
        _path = os.path.join(_demos, _name)
        if os.path.exists(_path):
            _any = True
            # The token rides in the URL FRAGMENT, never the query string: a
            # fragment is not sent to any server and so cannot land in a
            # server log, an access log, or a Referer header.
            print(f'[RELAY]   file://{_path}#relay_token={RELAY_TOKEN}')
    if not _any:
        print(f'[RELAY]   (no demos/ directory beside relay.py — append '
              f'#relay_token={RELAY_TOKEN} to the demo URL yourself)')
    print('[RELAY]')
    print(f'[RELAY] Test: curl -H "Authorization: Bearer {RELAY_TOKEN}" '
          f'http://localhost:{PORT}/health')
    print('[RELAY] ' + '-' * 66)
    print('[RELAY] Ctrl+C to stop')

    await asyncio.Event().wait()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n[RELAY] Stopped.')
