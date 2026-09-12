# Attendee Setup — Three Ways to Run

**Time required: 0–5 minutes, depending on which one you pick.**

There are exactly three supported ways to run these demos. All three are real
and all three are supported. Pick the one that fits the machine in front of you.

| | What it is | Setup | Internet |
|---|---|---|---|
| **1. RECORDED MODE** | Plays back a real, previously-captured run. No network calls at all. | None | Not needed |
| **2. YOUR CLAUDE SUBSCRIPTION** | A small local helper reuses the Claude Code sign-in you already have. | ~3 min | Yes |
| **3. LOCAL MODEL (Ollama)** | An open-weight model on your own machine. | ~10 min, mostly download | Only to download the model |

None of the three asks you to open an account, and none of them asks you to
paste a key. They are alternatives, not tiers: one replays a captured run, one
uses sign-in you already have, one uses hardware you already own.

---

## Path 1 — RECORDED MODE

**This is a first-class way to run the workshop, not a fallback.** Every phase,
every pane and every export works. The content is captured from real runs. It
is also the most reliable option on conference wifi, and it is what the
presenter uses on stage.

1. Open a demo file in your browser (see *Opening a Demo* below)
2. Click the recorded-playback button in the control panel:
   - `swarm-factory-live.html` → `[ ◉ DEMO MODE ]` (bottom of the left sidebar — scroll down)
   - `swarm-cage-live.html` → `[ ◉ DEMO ]` (bottom bar)
   - `improvement-loop-live.html` → `[ ◉ DEMO ]` (bottom bar)
3. The button label changes to `[ ◉ DEMO MODE ON ]` / `[ ◉ DEMO ON ]` and a
   notice appears saying no key is needed
4. Start the run — see *First Run* below

No key field appears, no provider selection matters, and nothing leaves your
machine.

**One limitation, stated plainly:** in the factory demo the `CUSTOM` swarm type
is disabled in recorded mode, because there is no recording of a brief you have
not written yet. The RED / BLUE / INFRA presets all play in full. Labs 2 and 3
run end to end in recorded mode.

---

## Path 2 — Your Claude subscription (local helper)

If `claude` already works in your terminal, you can drive the demos with the
subscription you already have. A small local Python helper (`relay.py`) runs on
your machine and calls the `claude` CLI once per demo phase. No separate API key is involved.

**Prerequisites**

1. `claude --version` prints a version in your terminal. If it does not, install
   Claude Code first — [docs.claude.com/claude-code](https://docs.claude.com/claude-code) —
   and sign in, then confirm `claude --version` works before continuing.
2. `python3 --version` prints 3.9 or later.
3. `pip install aiohttp` — the one dependency the helper needs that is not in
   the Python standard library.

**Start the helper** (once; leave it running):

```bash
cd ai-village-workshop
python3 relay.py
```

You should see a block of `[RELAY]` lines that includes an access token and a
ready-made link for each demo:

```
[RELAY] Listening on http://localhost:3001
[RELAY] ------------------------------------------------------------------
[RELAY] Access token: 8Kx2...   <- yours will differ, and changes every restart
[RELAY]   Freshly minted for THIS run. It changes every restart.
[RELAY]   Every browser request needs this token. Local non-browser
[RELAY]   callers (curl, scripts) do not, unless you set RELAY_STRICT_AUTH=1.
[RELAY]
[RELAY] Open a demo with the token already attached (click or copy):
[RELAY]   file:///.../demos/swarm-factory-live.html#relay_token=8Kx2...
[RELAY]   ...
```

Confirm it with:

```bash
curl http://localhost:3001/health
```

`"claude_binary_present": true` means you are ready.

**Then, in the demo:** open the demo using one of the `file://...#relay_token=`
links the relay printed. That is the whole token step — the page reads the token
out of the link, remembers it, and removes it from the address bar. If you
already had the demo open, reload it from the printed link, or just start a run:
the page will ask you to paste the token once and then `[ ↻ Retry phase ]` will
work.

Now click `[ CLAUDE CODE ]` in the provider selector. It is already selected by
default. No key field appears — authentication flows through your own `claude`
CLI.

**Why there is a token at all.** The relay drives your already-signed-in
`claude` CLI, and it listens on your own machine. Binding to loopback keeps it
off the conference network, but *your browser is also on your machine* — so
without a token, any other tab you had open could quietly post to
`localhost:3001`, spend your subscription, and read the answers. The token is
what stops that. It is minted fresh for each run and never leaves your laptop.

Full instructions and troubleshooting: **CLAUDE-CODE-SETUP.md**.

---

## Path 3 — Local model with Ollama

Fully local, fully offline once the model is downloaded, no account of any kind.

1. Install Ollama and pull a model — see **OLLAMA-SETUP.md**
2. Run `ollama serve` in a terminal and leave it running
3. In any demo, click `[ OLLAMA ]` in the provider selector
4. A model-name field appears next to it — type the model you pulled, e.g.
   `llama3.2`. It defaults to `llama3.2` if you leave it alone.
5. Start the run — calls go to `http://localhost:11434/v1/chat/completions`

**What to expect:** open-weight models produce shorter, less structured agent
output than a hosted frontier model. The workflow is identical and every phase
runs. Speed depends entirely on your hardware — see OLLAMA-SETUP.md, which is
honest about the range.

---

## Opening a Demo

Open the file directly in your browser — double-click it, or drag it into a
browser window. `file://` works; no server is required.

The three files are:

```
demos/swarm-factory-live.html
demos/swarm-cage-live.html
demos/improvement-loop-live.html
```

If you would rather serve them:

```bash
cd ai-village-workshop
python3 -m http.server 8080
# then open http://localhost:8080/demos/swarm-factory-live.html
```

---

## First Run

**Factory** (`demos/swarm-factory-live.html`)

1. Select the **RED** preset
2. Click `[ ◆ BUILD SWARM ]` — in recorded mode the button reads `[ ▶ RUN DEMO ]`
3. Watch the phases run. The pipeline pauses once at the operator gate; click
   `[ APPROVE — PROCEED TO FABRICATION ]` to continue.

**Cage** (`demos/swarm-cage-live.html`)

1. Confirm **IRONCLAD** is highlighted
2. Click `[ SETUP NETWORK ]`, wait for the topology to render
3. Click `[ ⚛ ENGAGE ]`

**Loop** (`demos/improvement-loop-live.html`)

1. Pick an operating mode — **PRESET MODE** needs nothing else
2. Click `[ BEGIN EVALUATION ]`
3. Click `[ ⚛ RUN CYCLE ]`

---

## When Something Goes Wrong

**The page asks for a "relay access token", or the run stops with a message
about a missing token.** The demo was opened without the token. Look at the
terminal running `relay.py` for the line `[RELAY] Access token: ...`, paste that
value when the demo asks, then press `[ ↻ Retry phase ]`. Reopening the demo
from the printed `file://...#relay_token=` link avoids the prompt entirely. The
token changes every time you restart the relay.

**The page shows `UNCLASSIFIED FAILURE` and the raw message is `Failed to
fetch` (Chrome) or `NetworkError when attempting to fetch resource` (Firefox).**
Your browser could not complete the request. On the CLAUDE CODE path that
almost always means `relay.py` is not running — start it and try again. On the
OLLAMA path there are two causes that look the same from the browser: Ollama is
not running, or Ollama is running and refused your page's origin. A demo opened
by double-clicking the file has the origin `null`, and a default Ollama install
answers `null` with HTTP 403. Run `curl http://localhost:11434/api/tags`; if it
answers, the origin is the cause, and `OLLAMA-SETUP.md` has the two fixes. The
demo deliberately does *not* guess a cause it did not observe, which is why it
says UNCLASSIFIED rather than naming one.

**`INFRASTRUCTURE FAILURE`** — the request got out but never reached a model.
The demo will name the reason it was told (access limit, sign-in, timeout,
upstream). Nothing is wrong with your brief.

**`CONTENT FAILURE`** — a model was reached and declined. Retry, or switch to
recorded mode and keep moving.

**`claude_binary_present: false` from `/health`** — the helper started in a
shell where `claude` is not on PATH. Stop it, check `which claude`, restart it
from a shell where that resolves.

**`model not found` on the OLLAMA path** — you have not pulled that model.
`ollama pull llama3.2`, or type a model name you actually have.

**A phase pane stays empty for a long time** — on the local-model path this is
usually just slowness, not a fault. On the subscription path, the recovery
banner offers `[ ⏳ Continue waiting (+60s) ]`.

**Anything at all** — click the recorded-playback button and keep going. The
recorded path never depends on the network, and it is a supported way to do
every lab except the factory demo's `CUSTOM` brief.

---

## What the Demos Store on Your Machine

Everything these demos remember lives in your browser's localStorage, under one
prefix:

- `swarmdemo_provider` — which path you last selected (shared by all three demos)
- `swarmdemo_ollama_model` — the local model name you typed
- `swarmdemo_factory_export` — the hand-off from the factory demo to the cage
  demo (the swarm name and agent codenames you just built, nothing else)
- `swarmdemo_loop_source`, `swarmdemo_loop_export` — the hand-off between the
  cage and loop demos

None of the three supported paths asks you for a key, and there is no longer any
key field to type one into. If you used an earlier build of this package and it
saved a vendor API key, the demos now delete that key from your browser storage
the next time you open any of them; you do not have to find it yourself.

**To remove everything:** browser DevTools → Application → Local Storage →
delete every key beginning with `swarmdemo_`. That is the complete list.
Nothing is written anywhere else and nothing is sent off your machine except
the model calls on the path you chose.
