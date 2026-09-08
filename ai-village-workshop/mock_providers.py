"""
mock_providers.py — Playwright page.route() mocks for LIVE-mode flows.

Exercises every provider path (Anthropic direct, CLAUDE CODE
relay, Ollama) without spending real API budget. The
mocks intercept the demo's outbound fetch() at the network layer and return
shape-accurate canned responses — same JSON keys, same SSE frame layout the
demo's parser actually consumes. If the demo's call shape regresses (e.g.
forgets `x-api-key` on Anthropic, omits the
SSE `Accept:` header on CLAUDE CODE), the test that uses the corresponding
asserter will fail.

Usage pattern:

    from mock_providers import (
        mock_anthropic, mock_ollama,
        mock_cc_relay_sse, spawn_relay_with_stub_claude,
    )

    def test_forge_anthropic_live(safe_page, demo_url):
        mock_anthropic(safe_page, content="canned forge phase output")
        safe_page.goto(demo_url('swarm-factory-live.html'), wait_until='domcontentloaded')
        safe_page.locator('#prv-ant').click()
        safe_page.locator('#ak').fill('sk-ant-test')
        safe_page.locator('#ibtn').click()
        ...

The Playwright `safe_page` fixture filters `net::ERR_*` console noise so
abort()ed routes don't cause false failures. Real JS exceptions from the
demo's catch blocks still surface via pageerror — which is what we want.
"""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import textwrap
import time
from contextlib import contextmanager
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────
# Anthropic direct (operator's default workflow)
# ─────────────────────────────────────────────────────────────────────────

def mock_anthropic(page, *, content: str = 'OK', status: int = 200,
                   capture: list | None = None,
                   error_message: str | None = None,
                   malformed: bool = False):
    """Stub api.anthropic.com/v1/messages.

    The demo's `callAnthropic` reads `(await r.json()).content[0].text`.
    Our canned response matches that shape. If `capture` is supplied
    (a list), every intercepted request appends a dict with `url`,
    `headers` (lower-cased keys), and `body` (parsed JSON or raw bytes).

    `malformed=True` forces a response with no `content[0].text` field
    so the demo's catch block fires (covered by the "malformed response
    surfaces recovery banner" test).
    """
    def handler(route):
        req = route.request
        if capture is not None:
            try:
                body = json.loads(req.post_data or '{}')
            except Exception:
                body = req.post_data
            capture.append({
                'url': req.url,
                'headers': {k.lower(): v for k, v in (req.headers or {}).items()},
                'body': body,
            })
        if status >= 400:
            payload = {'error': {'message': error_message or f'HTTP {status}'}}
            route.fulfill(
                status=status,
                content_type='application/json',
                body=json.dumps(payload),
            )
            return
        if malformed:
            # No content[] at all — the demo's `(json).content[0].text`
            # access throws a TypeError caught by the per-phase recovery.
            route.fulfill(
                status=200,
                content_type='application/json',
                body=json.dumps({'role': 'assistant'}),
            )
            return
        route.fulfill(
            status=200,
            content_type='application/json',
            body=json.dumps({
                'id': 'msg_mock',
                'type': 'message',
                'role': 'assistant',
                'content': [{'type': 'text', 'text': content}],
                'model': 'claude-sonnet-4-6',
                'stop_reason': 'end_turn',
            }),
        )

    page.route('**/api.anthropic.com/v1/messages**', handler)


# ─────────────────────────────────────────────────────────────────────────
# Ollama (local fallback)
# ─────────────────────────────────────────────────────────────────────────

def mock_ollama(page, *, content: str = 'OK', status: int = 200,
                capture: list | None = None,
                error_message: str | None = None,
                connection_refused: bool = False):
    """Stub localhost:11434/v1/chat/completions (the OpenAI-compat path
    every demo actually uses; the bare /api/generate path is no longer
    referenced in the code).

    `connection_refused=True` aborts the request with a network error,
    simulating Ollama not running.
    """
    def handler(route):
        req = route.request
        if capture is not None:
            try:
                body = json.loads(req.post_data or '{}')
            except Exception:
                body = req.post_data
            capture.append({
                'url': req.url,
                'headers': {k.lower(): v for k, v in (req.headers or {}).items()},
                'body': body,
            })
        if connection_refused:
            route.abort('connectionrefused')
            return
        if status >= 400:
            payload = {'error': error_message or f'HTTP {status}'}
            route.fulfill(
                status=status,
                content_type='application/json',
                body=json.dumps(payload),
            )
            return
        route.fulfill(
            status=200,
            content_type='application/json',
            body=json.dumps({
                'id': 'chatcmpl-mock',
                'object': 'chat.completion',
                'model': 'llama3.2',
                'choices': [{
                    'index': 0,
                    'message': {'role': 'assistant', 'content': content},
                    'finish_reason': 'stop',
                }],
            }),
        )

    page.route('**/localhost:11434/**', handler)
    page.route('**/127.0.0.1:11434/**', handler)


# ─────────────────────────────────────────────────────────────────────────
# CLAUDE CODE relay — application-level mock (page.route on /v1/chat)
# ─────────────────────────────────────────────────────────────────────────
#
# Two modes:
#   1. mock_cc_relay_sse() — page.route() stub the demo talks to directly
#      WITHOUT spawning the real relay. Faster; no subprocess. Use for
#      every test that just wants to assert the demo posts the correct
#      headers/body and consumes deltas. The frame layout matches what
#      relay.py emits (data: {"delta":...} / data: {"done":..., "content":...}
#      / data: {"warning":...}).
#   2. spawn_relay_with_stub_claude() — boots the real relay.py against a
#      stubbed `claude` shell script on PATH. Use when a test must exercise
#      the actual subprocess path (binary-missing recovery banner, full
#      relay → demo round-trip with the real SSE wiring).

def _sse_frames(deltas: list[str], *, done: bool = True,
                done_content: str | None = None,
                error: str | None = None,
                warning: str | None = None,
                recovered: bool = False,
                cli_error: str | None = None) -> bytes:
    """Build a single response body containing all the SSE frames at once.
    Playwright's page.route() doesn't natively support drip-fed responses
    — fulfill() takes a single body. The demo's parser handles all frames
    arriving in one chunk identically to drip-fed (it splits on \\n\\n)."""
    parts = []
    if warning is not None:
        parts.append(f'data: {json.dumps({"warning": warning})}\n\n')
    for d in deltas:
        parts.append(f'data: {json.dumps({"delta": d})}\n\n')
    if error is not None:
        parts.append(f'data: {json.dumps({"error": error})}\n\n')
    elif done:
        full = done_content if done_content is not None else ''.join(deltas)
        payload = {'done': True, 'content': full, 'deltas': len(deltas)}
        if recovered:
            payload['recovered'] = True
            if cli_error:
                payload['cli_error'] = cli_error
        parts.append(f'data: {json.dumps(payload)}\n\n')
    return ''.join(parts).encode('utf-8')


def mock_cc_relay_sse(page, *, deltas: list[str] | None = None,
                      done_content: str | None = None,
                      error: str | None = None,
                      warning: str | None = None,
                      recovered: bool = False,
                      cli_error: str | None = None,
                      capture: list | None = None,
                      status: int = 200,
                      json_body: dict | None = None):
    """Stub localhost:3001/v1/chat with an SSE response (when the demo
    sends `Accept: text/event-stream`) or a JSON response (when it
    doesn't — used by the relay's own /health check shape).

    `deltas` defaults to a single chunk so callers can write
    `mock_cc_relay_sse(page)` and get a working pipeline. Pass an empty
    list with `error=...` to simulate a stream that ends in error.

    `recovered=True` mirrors the relay's "is_error after deltas
    streamed → graceful recovery" path: the demo should NOT throw a
    recovery banner because the streamed content is what the user saw.

    `json_body` provides the non-SSE response body (used when the test
    wants to mock the JSON path explicitly — e.g. a fall-through where
    the demo somehow doesn't request SSE)."""
    if deltas is None:
        deltas = ['mock token output\n']

    def handler(route):
        req = route.request
        if capture is not None:
            try:
                body = json.loads(req.post_data or '{}')
            except Exception:
                body = req.post_data
            capture.append({
                'url': req.url,
                'headers': {k.lower(): v for k, v in (req.headers or {}).items()},
                'body': body,
            })
        accept = (req.headers or {}).get('accept', '') \
            or (req.headers or {}).get('Accept', '')
        if 'text/event-stream' in accept:
            body = _sse_frames(
                deltas,
                done=(error is None),
                done_content=done_content,
                error=error,
                warning=warning,
                recovered=recovered,
                cli_error=cli_error,
            )
            route.fulfill(
                status=status,
                headers={
                    'Content-Type': 'text/event-stream',
                    'Cache-Control': 'no-cache',
                    'Access-Control-Allow-Origin': '*',
                },
                body=body,
            )
            return
        # JSON path
        if json_body is None:
            json_body_local = {'content': done_content or ''.join(deltas)}
        else:
            json_body_local = json_body
        if error is not None and status < 400:
            status_local = 502
            payload = {'error': error}
        else:
            status_local = status
            payload = json_body_local
        route.fulfill(
            status=status_local,
            content_type='application/json',
            body=json.dumps(payload),
        )

    page.route('**/localhost:3001/v1/chat**', handler)
    page.route('**/127.0.0.1:3001/v1/chat**', handler)


# ─────────────────────────────────────────────────────────────────────────
# Real relay.py + stubbed `claude` binary on PATH
# ─────────────────────────────────────────────────────────────────────────
#
# Used by tests that must exercise the actual relay subprocess:
#   - "claude binary missing" recovery banner test
#   - the relay's /health endpoint surface
#   - end-to-end SSE round-trip through real network sockets

WORKSHOP_DIR = Path(__file__).resolve().parent

# Stubbed `claude` binary script. Emits stream-json frames for the SSE
# branch and a single-line JSON object for the json branch. Keeps tests
# fast: no model latency, deterministic content. Honors --output-format
# to decide which path to take.
STUB_CLAUDE_SCRIPT = textwrap.dedent('''\
    #!/usr/bin/env python3
    """Stub `claude` binary for offline runs. Emits canned stream-json
    or single-line json output. Drains stdin (the user prompt moved
    to stdin to avoid ARG_MAX) before responding so the relay's stdin-close
    sequence matches production.

    Behavior driven by env vars set by the test fixture:
      STUB_TEXT      — the text to "stream" / return (default: "OK")
      STUB_DELAY_MS  — milliseconds to wait between frames (default: 0)
      STUB_IS_ERROR  — if "1", emit result.is_error=true after deltas
                           (exercises the relay's graceful-recovery
                           path: streamed content + late error → recovered)
      STUB_VERSION   — `claude --version` output (default: "stub 0.0.0")
    """
    import json
    import os
    import sys
    import time

    args = sys.argv[1:]

    # `claude --version` health-check support
    if args and args[0] in ('--version', '-V'):
        print(os.environ.get('STUB_VERSION', 'stub 0.0.0'))
        sys.exit(0)
    if args and args[0] in ('--help', '-h'):
        print('stub claude — supports --output-format, --include-partial-messages')
        sys.exit(0)

    # Drain stdin (the relay closes stdin after writing the user prompt,
    # so this returns immediately once the EOF arrives).
    try:
        sys.stdin.read()
    except Exception:
        pass

    text = os.environ.get('STUB_TEXT', 'OK')
    delay_ms = int(os.environ.get('STUB_DELAY_MS', '0') or '0')
    is_error_after = os.environ.get('STUB_IS_ERROR') == '1'

    streaming = '--include-partial-messages' in args
    if streaming:
        # Split text into a few chunks so the demo can observe multiple
        # deltas (matters for the tok-count ticker assertions).
        chunks = [text[i:i+max(1, len(text)//3 or 1)] for i in range(0, len(text), max(1, len(text)//3 or 1))]
        if not chunks:
            chunks = ['']
        for c in chunks:
            frame = {'type': 'stream_event',
                     'event': {'type': 'content_block_delta',
                               'delta': {'type': 'text_delta', 'text': c}}}
            sys.stdout.write(json.dumps(frame) + '\\n')
            sys.stdout.flush()
            if delay_ms:
                time.sleep(delay_ms / 1000.0)
        # Final result
        if is_error_after:
            result = {'type': 'result', 'subtype': 'error',
                      'is_error': True, 'result': 'late upstream error'}
        else:
            result = {'type': 'result', 'subtype': 'success',
                      'is_error': False, 'result': text}
        sys.stdout.write(json.dumps(result) + '\\n')
        sys.stdout.flush()
        sys.exit(0)

    # Non-streaming JSON path.
    sys.stdout.write(json.dumps({'result': text}) + '\\n')
    sys.stdout.flush()
    sys.exit(0)
''')


def _relay_health_ok(timeout: float = 5.0) -> bool:
    """Poll relay /health until it responds or the timeout elapses."""
    import urllib.error
    import urllib.request
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen('http://127.0.0.1:3001/health',
                                        timeout=0.5) as r:
                return r.status == 200
        except urllib.error.URLError:
            pass
        except Exception:
            pass
        time.sleep(0.1)
    return False


def _free_port_3001_or_wait(timeout: float = 8.0):
    """If a previous relay is still listening on 3001 (the port is hard-
    coded), wait for it to release. Each test cleans up its own subprocess
    on context exit, but Linux's TIME_WAIT keeps the socket bound for a
    few seconds after the process dies. We probe with SO_REUSEADDR set so
    we can detect "real" port conflicts (operator's manually-started
    relay) and distinguish them from TIME_WAIT — which the relay's own
    binding loop will tolerate via aiohttp's default reuse semantics.

    Returns True if the port is free, False if still bound at timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        s = socket.socket()
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('127.0.0.1', 3001))
            s.close()
            return True
        except OSError:
            try:
                s.close()
            except Exception:
                pass
            time.sleep(0.2)
    return False


@contextmanager
def spawn_relay_with_stub_claude(*, claude_text: str = 'OK',
                                 is_error_after: bool = False,
                                 strip_path: bool = False,
                                 timeout_sec: int = 60,
                                 startup_timeout: float = 8.0):
    """Spawn relay.py with a stubbed `claude` binary on PATH. Yields the
    relay's base URL (always http://127.0.0.1:3001 since the port is
    hard-coded). The relay subprocess is killed on context exit.

    `strip_path=True` runs the relay with PATH containing only directories
    that DO NOT include `claude` — used to test the binary-missing path.

    The relay's /health endpoint is polled until it responds; if it doesn't
    come up in `startup_timeout` seconds, the context manager raises so
    the test fails fast rather than hanging on later requests.
    """
    if not _free_port_3001_or_wait():
        raise RuntimeError(
            'Port 3001 is in use — kill any existing relay.py before '
            'running the relay stubs.'
        )

    # Build the stub claude binary in a temp dir so we can control PATH.
    import tempfile
    tmpdir = tempfile.mkdtemp(prefix='s50-relay-stub-')
    stub = Path(tmpdir) / 'claude'
    stub.write_text(STUB_CLAUDE_SCRIPT)
    stub.chmod(0o755)

    env = os.environ.copy()
    env['STUB_TEXT'] = claude_text
    env['STUB_IS_ERROR'] = '1' if is_error_after else '0'
    env['RELAY_TIMEOUT_SEC'] = str(timeout_sec)

    if strip_path:
        # Keep only Python's own directory and a barren PATH so `which
        # claude` returns None. The relay still needs to find python3 and
        # the aiohttp egg, but the relay is invoked directly by absolute
        # path so we don't actually need PATH lookups for it.
        safe_dirs = [
            os.path.dirname(shutil.which('python3') or '/usr/bin/python3'),
            '/usr/bin', '/bin',
        ]
        env['PATH'] = ':'.join(d for d in safe_dirs if d)
    else:
        env['PATH'] = f'{tmpdir}:{env.get("PATH", "")}'

    relay_py = WORKSHOP_DIR / 'relay.py'
    proc = subprocess.Popen(
        ['python3', str(relay_py)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=str(WORKSHOP_DIR),
    )
    try:
        if not _relay_health_ok(timeout=startup_timeout):
            # Relay didn't come up — drain output for the error message.
            try:
                proc.terminate()
                out, _ = proc.communicate(timeout=2)
            except Exception:
                out = b''
            raise RuntimeError(
                'Relay did not become healthy within '
                f'{startup_timeout}s. Output: {out.decode("utf-8", "replace")[-500:]}'
            )
        yield 'http://127.0.0.1:3001'
    finally:
        try:
            proc.terminate()
            proc.wait(timeout=3)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass
        try:
            shutil.rmtree(tmpdir, ignore_errors=True)
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────────────────
# Convenience: stub the demo's `dc()` so DEMO MODE branches don't get
# pulled into a LIVE-mode test by accident.
# ─────────────────────────────────────────────────────────────────────────

def disable_demo_short_circuit(page, kind: str = 'forge'):
    """Some forge tests depend on the LIVE-mode call() path actually
    reaching fetch(); the dc() helper otherwise short-circuits to canned
    DEMO content. This mirrors `_accelerate_demo(..., dc_override=False)`
    for callers who don't otherwise want the full acceleration
    suite."""
    if kind == 'forge':
        # forge's dc() reads SWARMS[selSwarm]... — leave it alone here;
        # the LIVE call() path doesn't go through dc().
        return
    # combat and evolve LIVE paths bypass callDemo() naturally (see
    # callAPI / streamPhase / call). Nothing to override.
