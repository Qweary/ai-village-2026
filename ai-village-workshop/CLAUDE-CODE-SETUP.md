# Claude Code Setup — Run on the Subscription You Already Have

This is one of the three supported ways to run these demos. The **CLAUDE CODE** provider lets you run LIVE MODE using your existing Claude Code subscription. The demos talk to a small local Python server (`relay.py`) that shells out to the `claude` CLI for each call — your Claude Code authentication is reused, no separate Anthropic API key required.

**Use this if:** you have Claude Code installed and authenticated (you can already run `claude` from your terminal).

**Skip this if:** you are using recorded mode or a local Ollama model — the other two supported paths. Neither needs anything on this page.

---

## Step 1: Verify Claude Code is Installed

The relay calls the `claude` CLI as a subprocess. Confirm it is on your PATH:

```bash
which claude
claude --version
```

You should see a path (e.g. `/usr/local/bin/claude`) and a version string (e.g. `2.1.123 (Claude Code)`). If the binary is missing, install Claude Code first — see [docs.claude.com/claude-code](https://docs.claude.com/claude-code) — and confirm `claude --version` works before continuing.

The relay uses `claude -p` (non-interactive print mode) with `--no-session-persistence`, so each demo call is a one-shot completion that does not affect any of your saved Claude Code sessions.

---

## Step 2: Install aiohttp

```bash
pip install aiohttp
```

aiohttp is the only Python dependency the relay needs (not in stdlib). If you already have it, skip this step.

---

## Step 3: Run the Relay

From the `ai-village-workshop/` directory:

```bash
python3 relay.py
```

You should see:

```
[RELAY] claude CLI: /usr/local/bin/claude
[RELAY] Model: claude-haiku-4-5 (override with RELAY_MODEL=...)
[RELAY] Per-call timeout: 600s (override with RELAY_TIMEOUT_SEC=...)
[RELAY] Listening on http://localhost:3001
[RELAY] ------------------------------------------------------------------
[RELAY] Access token: 8Kx2v...          <- yours differs; new on every restart
[RELAY]   Freshly minted for THIS run. It changes every restart.
[RELAY]   Every browser request needs this token. Local non-browser
[RELAY]   callers (curl, scripts) do not, unless you set RELAY_STRICT_AUTH=1.
[RELAY]
[RELAY] Open a demo with the token already attached (click or copy):
[RELAY]   file:///.../demos/swarm-factory-live.html#relay_token=8Kx2v...
[RELAY]   file:///.../demos/swarm-cage-live.html#relay_token=8Kx2v...
[RELAY]   file:///.../demos/improvement-loop-live.html#relay_token=8Kx2v...
[RELAY]
[RELAY] Test: curl -H "Authorization: Bearer 8Kx2v..." http://localhost:3001/health
[RELAY] ------------------------------------------------------------------
[RELAY] Ctrl+C to stop
```

The relay only binds to `127.0.0.1` — it is not reachable from other machines.

### The access token, and why loopback was not enough

The relay spawns your already-authenticated `claude` CLI. It binds `127.0.0.1`,
which keeps it off the conference network — but **your browser is on
`127.0.0.1` too.** Before the token existed, any page open in any tab could POST
to `localhost:3001`, drive your CLI, spend your subscription, and read the
reply. A loopback bind is not an authentication mechanism.

So the relay mints a random token at startup and refuses any browser request
that does not carry it, as `Authorization: Bearer <token>`. Details:

- **Fresh per run.** Restarting the relay invalidates the old token. Reopen the
  demo from the newly printed link, or paste the new token when asked.
- **Delivery to the demos** is the `#relay_token=...` fragment on the printed
  `file://` links. A URL *fragment* is never transmitted to any server, so
  unlike a query string it cannot end up in a log or a `Referer` header.
- **Pin your own token** with `RELAY_TOKEN=...` (16 characters minimum — the
  relay refuses to start with anything shorter). Useful for scripts, and it
  survives restarts.
- **Non-browser callers** (curl, the test harness) are not required to present
  the token by default: a local process that can run scripts can already run
  `claude` itself, so requiring it there protects nothing the token can reach.
  Set `RELAY_STRICT_AUTH=1` to require it from every caller regardless.
- **Origins are also allowlisted** — `null` (a `file://` page) and loopback
  `http://` origins only. That is defence in depth, *not* the control: `null` is
  presented by a sandboxed iframe on any site, so the token is what actually
  decides.

---

## Step 4: Test the Relay

```bash
curl http://localhost:3001/health
```

Expected response:

```json
{"status": "ok", "claude_binary_present": true, "classifier_version": 1}
```

The response reports *whether* the CLI was found, not *where*. This endpoint
answers without a token for a non-browser caller (see the note below), so it
deliberately carries no filesystem path — the path would have contained your
home directory and account name. If you need to know which binary the relay
picked up, ask your own shell: `which claude`.

`curl` sends none of the headers a browser is forced to send, so it is treated
as a local non-browser caller and no token is needed for this check. If you run
the relay with `RELAY_STRICT_AUTH=1`, add the token:

```bash
curl -H "Authorization: Bearer $RELAY_TOKEN" http://localhost:3001/health
```

If `claude_binary_present` is `false`, the relay started in a shell where `claude` is not on PATH. Stop the relay, fix the PATH (or install Claude Code), and restart.

---

## Step 5: Select [ CLAUDE CODE ] in the Demo

1. Open any demo in your browser (file:// or localhost:8080)
2. Click the **[ CLAUDE CODE ]** button in the provider selector
3. No key field appears — authentication flows through your Claude Code installation
4. Start the run — `[ ◆ BUILD SWARM ]` in the factory demo, `[ SETUP NETWORK ]` then `[ ⚛ ENGAGE ]` in the cage demo, `[ ⚛ RUN CYCLE ]` in the loop demo. The demo posts to `http://localhost:3001/v1/chat`.

Each call spawns a one-shot `claude -p` subprocess. Expect the first call to take a few seconds longer than subsequent calls.

---

## What Attendees See

LIVE MODE through the CLAUDE CODE provider streams tokens from the model as they are produced. Each long phase (ARCHITECT, OFFENSE A+B, BRIEFER, BUILDER, AUDITOR, INSPECTOR in FACTORY; red/blue stages in CAGE; ARBITER/SCULPTOR/RERUN in LOOP) writes its output into the demo pane in real time, character by character — no more 60-300 second silent freeze while a phase generates.

A small **`tokens: N ▌`** counter in the header increments while the model is producing output. If you see the counter advancing, the model is responding correctly even if a particular pane is still filling. The counter resets at the start of each phase.

The relay opens a Server-Sent Events connection (`Accept: text/event-stream`) and forwards `claude -p --output-format stream-json --include-partial-messages` deltas as they arrive. The non-streaming JSON path remains unchanged — `/health` and any non-streaming client continue to work exactly as before.

---

## CAGE, live, on CLAUDE CODE

The cage demo (`swarm-cage-live.html`) walks through a tabletop training scenario where one swarm plays attacker (`red-team-ops-v2`) and another plays defender (`blue-team-ops-v1`) over a deliberately-vulnerable lab network or a fictional MLOps cluster. FACTORY and LOOP don't have this red/blue dynamic, so they don't run into the same provider-side behavior — but CAGE does.

**What used to happen.** Through the CLAUDE CODE provider, cage phases sometimes refused to produce content even though the operator-laptop lab network at 192.168.100.0/24 is fully synthetic and the OPERATION PHANTOM FEED MLOps pipeline is fictional. The cause is not the scenario — the same content is produced without difficulty against a model carrying its normal safety layer — it is the consumer-grade safety layer's caution in the absence of explicit engagement context. The model has no way to tell that "WinServer2019 (192.168.100.12)" is a Metasploitable3-class training image rather than a real production server, so it errs on the side of declining.

**What changed.** The cage demo now prepends a short **synthetic-lab grounding note** to every system prompt sent through CLAUDE CODE (and the Ollama consumer-grade path). It is about seven lines. It states plainly that the conversation generates content for a security training workshop demo rendered into static HTML, that every host, address, service and credential in the scenario is synthetic, and that the output is structured operational documentation written for a security-professional audience. It does not argue for permission. With that context in front, the model has something concrete to anchor against when the scenario names a lab address, and refusal rates drop.

**Where the note lands and where it doesn't.** The note is prepended on the two live paths this workshop supports — **CLAUDE CODE** and **Ollama** — because both run against a consumer-grade safety layer. It is not prepended on the direct-vendor path, which does not exhibit the same cumulative-pressure refusal cascade; there it would be token bloat with no benefit.

**What you'll see.** CAGE live on CLAUDE CODE behaves as designed: the red side produces operational logs, the blue side detects and responds, and the post-exercise hardening report compares the two. If you want to read the grounding note itself, it is the `SYS_AUTHORIZATION_PREAMBLE` constant in `demos/swarm-cage-live.html`. The FACTORY and LOOP demos do not use it (their content does not trigger the consumer-grade safety layer the same way).

**What it is NOT.** The note is a system-prompt header that grounds the synthetic-lab framing in the workshop demo context. It is **not** a substitute for legal authorization on real engagements — operators running these swarms outside this workshop produce their own written authorization document, which governs human-side authorization scope and is independent of any safety-layer header.

---

## Troubleshooting

**`claude_binary_present: false` from /health**
→ The relay started in a shell where `claude` is not on PATH.
→ Stop the relay, run `which claude` to confirm the binary location, then restart relay.py from a shell with the same PATH.

**`Claude Code CLI not found on PATH` error from the demo**
→ Same as above — the relay process can't see the `claude` binary. Install Claude Code if needed, then restart the relay.

**`Connection refused` in the demo**
→ relay.py is not running. Start it and confirm you see the `Listening` message.

**`Address already in use` on port 3001**
→ Another process owns port 3001. Check with:
```bash
lsof -i :3001
```
Kill the process or change `PORT = 3001` in relay.py to a free port, then update the demo's `callClaudeCode` fetch URL to match.

**HTTP 401 / "Relay token missing or incorrect"**
→ The page has no token, or has one from a previous relay run. Reopen the demo
from the `file://...#relay_token=...` link the relay printed, or paste the token
when the demo asks and press `[ ↻ Retry phase ]`. Remember the token changes on
every relay restart.

**CORS error in browser console**
→ The relay no longer sends `Access-Control-Allow-Origin: *`; it echoes back
only an allowlisted origin — `null` (a `file://` page) or a loopback `http://`
origin. A CORS error therefore means the page was served from an origin that is
not on that list. Open the demo as a `file://` page, or serve it from
`http://localhost` / `http://127.0.0.1`. Also confirm you are calling
http://localhost:3001 (not https) and that the relay is running.

**`claude CLI timeout (600s)`**
→ A phase took longer than 600 seconds. The default already gives 10 minutes of headroom — the heavy phases (BRIEFER research, BUILDER fabrication, OFFENSE Library Specification) run ~250-300s on typical workshop hardware. If you genuinely need more time, bump the timeout before starting the relay:
```bash
RELAY_TIMEOUT_SEC=900 python3 relay.py
```
If a single phase needs more time without restarting the relay, the recovery banner's **[ ⏳ Continue waiting (+60s) ]** button bumps the budget for that one call — the demo posts to `?timeout=N` (clamped 60-1800) which overrides the per-call timeout for that single request only.
If timeouts persist, run `time claude -p "ping" --output-format json` in a separate shell to measure your CLI's baseline latency — anything over ~30s for that minimal call indicates a Claude Code installation issue rather than a relay problem.

**Recovery banner appeared during a phase**
→ A phase failed (timeout, transient API error, or other fault). The banner offers five options:
- **[ ⏳ Continue waiting (+60s) ]** — re-issue the same call with a 60s timeout boost. Use when the model is just slow.
- **[ ↻ Retry phase ]** — re-issue the call with the default budget. Use for transient API errors.
- **[ ⏭ Skip phase ]** — substitute a `[phase skipped by operator]` placeholder and continue. Downstream phases get the placeholder as context. Use when one phase is broken but the rest of the run is salvageable.
- **[ ◉ Switch to DEMO ]** — flip to DEMO MODE and retry. Use as a safety net if LIVE is genuinely unavailable.
- **[ ✕ Abort run ]** — surface to the whole-run recovery banner. Use to stop the run.

**Token ticker is stuck at 0 / a phase pane is empty**
→ The relay's SSE branch isn't producing deltas. Confirm streaming end-to-end with:
```bash
curl -N -H 'Accept: text/event-stream' -H 'Content-Type: application/json' \
  -X POST http://localhost:3001/v1/chat \
  -d '{"system":"Be brief","user":"count to 5"}'
```
You should see a sequence of `data: {"delta": "..."}` events ending in `data: {"done": true, ...}`. If you only see a single `data: {"error": ...}` line, your `claude` CLI does not support `--output-format stream-json` — upgrade Claude Code and restart the relay.

**`claude returned non-JSON output`**
→ Your Claude Code CLI is older than the version that supports `--output-format json`. Upgrade Claude Code (`claude --version` should be ≥ 2.0.x) and restart the relay.

**`claude exited with code N` from the demo**
→ The CLI failed before producing output. The error message in the demo banner will include the stderr text — usually authentication-related. Run `claude -p "hello"` in your terminal to confirm the CLI itself works; if it prompts you to log in, do so, then retry the demo.
