# Ollama Setup — Fully Local, Offline AI

This is one of the three supported ways to run these demos. Ollama runs
open-weight models entirely on your machine. No API key, no account, and no
internet needed once the model is downloaded.

**Use this if:** you want fully local operation, you are offline at the venue,
or you want to compare local model quality against a hosted one.

**Note on quality:** Local models (llama3.2, mistral, phi3) produce shorter,
less structured output than a hosted frontier model. The workflow is identical
— every phase runs — but agent outputs will be simpler.

**Note on speed, honestly.** How long a phase takes is decided almost entirely
by your hardware, and the spread is enormous. With a supported GPU, a phase is
usually tens of seconds. On a CPU-only laptop the same phase can take *many
minutes*, because generation speed can fall to a couple of tokens per second and
these prompts ask for structured output of some length. **No timing figure in
this package was measured on your machine, and none should be read as a
prediction about it.** If you want to know what your laptop does, time one call
before the session:

```bash
time ollama run llama3.2 "Write a 300-word incident summary."
```

If that is slow, use recorded mode for the labs and keep Ollama for one phase
you want to watch run locally. Both are supported.

---

## Install Ollama

**macOS:**
```bash
brew install ollama
```

**Linux (apt-based):**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
```
winget install Ollama.Ollama
```

Or download the installer from https://ollama.com/download.

---

## Start the Ollama Server

```bash
ollama serve
```

You should see output like:
```
Ollama is running on http://localhost:11434
```

Leave this terminal open. The demos call `http://localhost:11434/v1/chat/completions` directly.

---

## Pull a Model

```bash
ollama pull llama3.2
```

This downloads ~2GB. Do this before the workshop if you are on a slow connection.

---

## Verify It Works

```bash
curl http://localhost:11434/api/tags
```

You should see a JSON response listing your pulled models.

---

## Recommended Models for This Workshop

| Model | Pull command | Size | Notes |
|---|---|---|---|
| **llama3.2** | `ollama pull llama3.2` | ~2GB | Best balance of speed and quality for the workshop |
| **mistral** | `ollama pull mistral` | ~4GB | Stronger instruction-following; slower on CPU |
| **phi3** | `ollama pull phi3` | ~2.2GB | Microsoft's compact model; fast, reasonable quality |

Start with `llama3.2` if you are unsure.

---

## Important: open the demos over http://localhost, not by double-clicking

**Measured, not assumed.** A page opened by double-clicking the HTML file has
the origin `null`, and Ollama refuses `null` with **HTTP 403** on a default
install. The demo cannot tell a refused origin from a server that is not
running, so it reports `Failed to fetch` and you are led to check `ollama serve`
when `ollama serve` was never the problem.

Ollama's default allowlist does contain the literal string `file://`, but no
browser ever sends that. Firefox and Chrome both send `Origin: null` for a
local file, which is the value Ollama rejects.

**Do this instead.** Serve the folder over HTTP, which Ollama allows by default:

```bash
cd ai-village-workshop
python3 -m http.server 8080
```

Then open `http://localhost:8080/demos/swarm-factory-live.html` (or the cage or
loop demo). Nothing leaves your machine; this is a local server.

**Or, if you must use `file://`,** start Ollama with the origin allowed:

```bash
OLLAMA_ORIGINS='*' ollama serve
```

This affects only the CLAUDE CODE path not at all, and only matters for Ollama.
Measured on a default install: `Origin: null` returns 403 without it and 200
with it.

---

## Select Ollama in the Demo

1. Open any demo in your browser
2. Click **[ OLLAMA ]** in the provider selector
3. A model-name field appears beside it. Type the model you actually pulled.
   Leave it blank and the demos ask for `llama3.2`, so if you pulled something
   else the call fails with `model not found` until you type the right name.
4. No key field appears — Ollama has no authentication
5. Start the run: `[ ◆ BUILD SWARM ]` in the factory demo, `[ SETUP NETWORK ]`
   then `[ ⚛ ENGAGE ]` in the cage demo, `[ ⚛ RUN CYCLE ]` in the loop demo.
   Calls go to `http://localhost:11434/v1/chat/completions`.

The model name you type is remembered under `swarmdemo_ollama_model` and is
shared by all three demos, so you only type it once.

---

## Troubleshooting

**`Connection refused` in the demo**
→ Ollama is not running. Start it with `ollama serve`.

**`model not found`**
→ You haven't pulled the model yet. Run `ollama pull llama3.2` (or your chosen model name).

**Slow responses**
→ Expected on CPU-only machines, and the range is wide — see the note on speed
at the top of this file. This is not a fault. If you need predictable pacing for
a presentation, use recorded mode, which is a supported path and makes no
network calls at all.

**CORS error in browser console, or a silent `Failed to fetch` while `ollama serve` is clearly running**
→ This is expected if you opened the demo as a `file://` page. Ollama answers
`Origin: null` with HTTP 403 on a default install. Serve the folder over HTTP
instead (`python3 -m http.server 8080` inside `ai-village-workshop/`, then open
`http://localhost:8080/demos/swarm-factory-live.html`), or start Ollama with
`OLLAMA_ORIGINS='*' ollama serve`. See the section above.

**The demo says `UNCLASSIFIED FAILURE` and the raw message is `Failed to fetch`**
→ Your browser could not complete the request. On this path there are two
causes and the browser cannot tell them apart: `ollama serve` is not running, or
it is running and refused your page's origin. Check the server first
(`curl http://localhost:11434/api/tags`). If that answers, the origin is the
cause and the section above is the fix. The demo says UNCLASSIFIED rather than
naming a cause because it deliberately never asserts a class it did not
observe.
