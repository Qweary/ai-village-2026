# AI Village 2026

**CybrHakCon 2026, AI Village track.** Two talks and a hands on workshop, packaged
so an attendee can keep them and anyone who missed the room can still run them.

Everything here opens off the file system. The slide decks and the three demos
are single HTML files. There is no build step, no CDN, no account, and no key.

---

## Three parts, start here

| Part | What it is | Open this |
|---|---|---|
| **`index.html`** | The landing page. Every deck, demo, lab, and setup page is one click from it. | [`index.html`](index.html) |
| **`talk-1/`** | Talk 1, **Swarms That Fight and Fix Each Other in a Cage**. A slide deck plus speaker notes. Its hands on half is the workshop below. | [`talk-1/README.md`](talk-1/README.md) |
| **`talk-2/`** | Talk 2, **A Language That Compiles Differently Every Time**. A slide deck plus a small runnable demo of a parser that returns a wrong answer and exits zero. | [`talk-2/compiles-differently-slides.html`](talk-2/compiles-differently-slides.html) |
| **`ai-village-workshop/`** | The workshop. Three live demos and three labs, with three supported ways to run them. | [`ai-village-workshop/README.md`](ai-village-workshop/README.md) |

If you are new here and want the quickest path:

- **Watching a talk?** Open `index.html` and click a deck. Each deck is one file
  and needs nothing else.
- **Presenting a talk?** Run `bin/doctor.sh` on the machine you will present
  from, then work through [`docs/presenter-checklist.md`](docs/presenter-checklist.md).
  The doctor tells you what is missing before you are on stage rather than
  after.
- **Attending the workshop?** Read [`docs/first-run.md`](docs/first-run.md). It
  is five minutes. Then open a demo and turn on recorded playback. That path
  needs no key, no account, and no network.
- **Running the workshop?** One command from the repo root: `bin/start.sh` on
  macOS and Linux, `bin\start.ps1` on Windows. It checks the machine, sets up
  Python if it has to, starts the relay, and opens the landing page with live
  mode already armed. Stop it with Ctrl+C.
- **In a hurry?** Open `ai-village-workshop/demos/swarm-cage-live.html`, click
  the recorded playback button in the bottom bar, and press engage. That replays
  a real captured run.

---

## One command

```bash
bin/doctor.sh        # is this machine ready?     macOS and Linux
bin/start.sh         # start everything            macOS and Linux

bin\doctor.ps1       # Windows PowerShell
bin\start.ps1        # Windows PowerShell
```

`doctor` reports two verdicts, because the package has two independent paths:

```
  RECORDED PATH: READY   open index.html and present
  LIVE RELAY:    READY   run bin/start.sh
  warnings: 0
```

Read them separately. `RECORDED PATH: READY` means you can present, whatever the
second line says. The recorded runs are captured from real runs, every phase and
pane and export works, and they are what the presenter uses on stage because
they do not care about conference wifi. `LIVE RELAY` only matters if you want
real model calls in front of the room.

`doctor` exits 0 when both paths are ready and 1 otherwise. `start.sh` runs it
first and stops if it fails, which you can override with `--skip-checks`.

---

## The workshop, in one paragraph

Three demos, one progression. **FACTORY** designs a multi agent swarm from a
plain language description. **CAGE** runs a red swarm against a blue swarm.
**LOOP** scores both sides, rewrites the agent that did worst, and reruns. Take
a CAGE result into LOOP, improve the agent that failed, and send it back.

| Demo | Open this | What it shows |
|---|---|---|
| FACTORY | `ai-village-workshop/demos/swarm-factory-live.html` | Designing a swarm from a plain language brief |
| CAGE | `ai-village-workshop/demos/swarm-cage-live.html` | A red swarm against a blue swarm, live |
| LOOP | `ai-village-workshop/demos/improvement-loop-live.html` | Scoring the agents, rewriting the weakest, rerunning |

The three labs in `ai-village-workshop/labs/` are the hands on part.

---

## Three ways to run, none of them asking for a key

| | What it is | Setup | Internet |
|---|---|---|---|
| Recorded playback | Replays a real captured run. No network calls at all. | none | no |
| Your Claude subscription | A small local helper reuses the sign in you already have. | about 3 min | yes |
| A local model | Ollama, on your own machine. | about 10 min, mostly download | only to download |

These are alternatives, not tiers. `ai-village-workshop/ATTENDEE-SETUP.md` puts
all three side by side. `CLAUDE-CODE-SETUP.md` and `OLLAMA-SETUP.md` in the same
directory carry the detail for the second and third.

`ai-village-workshop/mock_providers.py` holds offline provider stubs if you want
to exercise the wiring with no model access at all.

---

## What is in here

```
.
├── README.md                     this file
├── index.html                    the landing page, open this first
├── bin/
│   ├── doctor.sh   doctor.ps1    is this machine ready, two verdicts
│   └── start.sh    start.ps1     one command: check, start the relay, open the page
├── docs/
│   ├── first-run.md              fifteen minutes, start to finish
│   └── presenter-checklist.md    the night before, five minutes before, and if it fails
├── talk-1/                       Swarms That Fight and Fix Each Other in a Cage
├── talk-2/
│   ├── compiles-differently-slides.html   A Language That Compiles Differently Every Time
│   └── unbounded-split/          a runnable parser defect, stdlib only, about a minute
└── ai-village-workshop/
    ├── README.md                 the workshop's own hub
    ├── ATTENDEE-SETUP.md         the three ways to run
    ├── CLAUDE-CODE-SETUP.md      use the subscription you already have
    ├── OLLAMA-SETUP.md           a local model, fully offline
    ├── WORKSHOP-GUIDE.md         common errors, and paste-into-an-assistant context
    ├── relay.py                  the local helper, 127.0.0.1:3001
    ├── mock_providers.py         offline provider stubs
    ├── demos/                    the three single-file demos
    └── labs/                     the three labs
```

---

## Getting help

Run `bin/doctor.sh` first. Every `FAIL` line carries a fix on the line below it.

For an error message from inside a demo, `ai-village-workshop/WORKSHOP-GUIDE.md`
has a section on the common ones. That guide is also written to be pasted into a
chat assistant before you ask it a question about this package, so the assistant
answers about these files rather than in general.

---

## License and reuse

These are conference materials, published so attendees can keep them and so
anyone who missed the room can read them. The demos are single file HTML with
the agent prompts embedded as plain JavaScript constants. Open them in a text
editor and take whatever is useful.

Everything here keeps working offline, on any machine with a browser, after the
conference, with no dependency on anything hosted.
