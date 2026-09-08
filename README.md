# AI Village 2026

Materials from two talks at CybrHakCon 2026, AI Village track.

Everything here is self-contained. The demos and the slide deck are single HTML
files that open in any browser. There is no build step, no server, and no
account to create.

---

## Talk 1: Swarms That Fight and Fix Each Other in a Cage

A workshop plus three live demos. One swarm of AI agents plays attacker, another
plays defender, and a third loop scores both and rewrites whichever agent did
worst.

Everything for this talk is in [`ai-village-workshop/`](ai-village-workshop/).
Start with [`ai-village-workshop/README.md`](ai-village-workshop/README.md),
which lays out three ways to engage depending on how much time you have and
whether you want to run live model calls.

| Demo | Open this | What it shows |
|---|---|---|
| FACTORY | `ai-village-workshop/demos/swarm-factory-live.html` | Designing a multi-agent swarm from a plain-language description |
| CAGE | `ai-village-workshop/demos/swarm-cage-live.html` | A red swarm against a blue swarm, live |
| LOOP | `ai-village-workshop/demos/improvement-loop-live.html` | Scoring the agents, rewriting the weakest, rerunning |

The three connect. FACTORY builds swarms, CAGE runs them, LOOP improves them.

**The fastest possible start:** open `swarm-cage-live.html`, click the DEMO
button in the bottom bar, and press ENGAGE. That replays a real recorded run.
It needs no key, no account, and no setup.

The three labs in `ai-village-workshop/labs/` are the hands-on part. They assume
you have read `ATTENDEE-SETUP.md` first, which is a five minute read and covers
all three ways to run: recorded playback, a Claude Code sign-in you already
have, or a local Ollama model.

---

## Talk 2: A Language That Compiles Differently Every Time

The slide deck is [`talk-2/compiles-differently-slides.html`](talk-2/compiles-differently-slides.html).
Open it in a browser. It is one file, 21 surfaces, and it needs nothing else.

The last two slides are the handout card, front and back. If you were in the
room, that is the card you were looking at. If you were not, the card is the
part worth keeping.

---

## Running the demos with live models

Three supported paths, and none of them asks you for an API key or an account:

- **Recorded playback.** Replays a real captured run. Nothing to install.
- **Your existing Claude Code sign-in**, through the local relay in
  `ai-village-workshop/relay.py`. See `CLAUDE-CODE-SETUP.md`.
- **A local open-weight model** via Ollama. See `OLLAMA-SETUP.md`.

`ai-village-workshop/mock_providers.py` holds offline provider stubs if you want
to exercise the wiring with no model access at all.

---

## Getting help

`ai-village-workshop/WORKSHOP-GUIDE.md` is written to be pasted into a chat LLM
before you ask it a question about this package. It gives the assistant enough
context about the demos, the provider options and the error messages to answer
specifically rather than generically.

---

## License and reuse

These are conference materials, published so attendees can keep them and so
anyone who missed the room can read them. The demos are single-file HTML with
the agent prompts embedded as plain JavaScript constants. Open them in a text
editor and take whatever is useful.

The framework that generated these swarms is not published. The three demos and
the deck are self-contained and are the whole of what is handed out.
