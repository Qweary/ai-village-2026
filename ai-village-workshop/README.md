# AI Village Workshop — Multi-Agent AI Systems for Offensive and Defensive Security

**CybrHakCon 2026 | AI Village Track**

This package contains three AI demos and three hands-on labs. Everything runs in your browser, and no account is required.

---

## What This Is

These demos show what happens when you compose multiple AI agents into a coordinated system — agents that plan together, disagree with each other, and iteratively improve their own behavior.

Three demos, one progression:

| Demo | File | What It Shows |
|---|---|---|
| **FACTORY** | `demos/swarm-factory-live.html` | A factory that designs a multi-agent swarm from a plain-language description |
| **CAGE** | `demos/swarm-cage-live.html` | A red team swarm vs. a blue team swarm — live adversarial AI exercise |
| **LOOP** | `demos/improvement-loop-live.html` | An autonomous improvement loop: score the agents, rewrite the weakest one, rerun the test |

They are connected. FACTORY builds swarms. CAGE runs them. LOOP improves them. Import a CAGE result into LOOP, refine the agent that failed, and send the improved version back.

---

## Three Ways to Engage

### Track A — 15-Minute Observer

You need nothing at all. Every demo has a recorded-playback mode that replays a
real captured run with no network calls. It is a supported way to do the
workshop, not a consolation prize.

1. Open `demos/swarm-cage-live.html` in your browser
2. Click **[ ◉ DEMO ]** in the bottom bar — it changes to **[ ◉ DEMO ON ]**
3. Confirm **IRONCLAD** is highlighted, click **[ SETUP NETWORK ]**, then **[ ⚛ ENGAGE ]**
4. Watch the red and blue agents interact across six phases

Do the same for FACTORY (**[ ◉ DEMO MODE ]** at the bottom of the left sidebar,
then **[ ▶ RUN DEMO ]**) and LOOP (**[ ◉ DEMO ]**, pick a mode, then
**[ ⚛ RUN CYCLE ]**). Total time: ~15 minutes. No account and nothing to install.

### Track B — 45-Minute Practitioner

You want to run live model calls — either through the Claude subscription you
already have, or against a local model on your own machine.

1. Read `ATTENDEE-SETUP.md` — it takes 5 minutes
2. Work through **LAB-1** (forge a swarm for something you actually do)
3. Work through **LAB-2** (run both cage scenarios, compare blue detection)
4. Optional stretch: **LAB-3** (close the loop — improve the agent that failed)

### Track C — Researcher / Builder

You want to understand how this works and extend it.

- All three demos are single-file HTML — open in a text editor and read the JavaScript
- Agent system prompts are embedded as JavaScript constants (`SYS_ARBITER`, `SYS_SCULPTOR`, `SYS_PHANTOM_RED_RECON`, etc.)
- The coordination model is a sequential state-passing pattern: each agent receives the prior agent's output as context
- The framework that generates these swarms is not published; these three demos are self-contained and are the whole of what is handed out.

---

## Files in This Package

```
ai-village-workshop/
├── README.md             (this file)
├── ATTENDEE-SETUP.md     (the three ways to run — recorded, your subscription, local model)
├── CLAUDE-CODE-SETUP.md  (use your Claude Code subscription via local helper — no separate API key)
├── OLLAMA-SETUP.md       (fully local, offline Ollama setup)
├── WORKSHOP-GUIDE.md     (paste into claude.ai for contextual help)
├── relay.py              (Claude Code relay — python3 relay.py; spawns `claude -p` per call;
│                          prints a per-run access token + a demo link carrying it)
├── mock_providers.py     (offline provider stubs — run the demos with no model access at all)
├── demos/
│   ├── swarm-factory-live.html
│   ├── swarm-cage-live.html
│   └── improvement-loop-live.html
└── labs/
    ├── LAB-1-FACTORY.md    (30 min — forge a swarm for your domain)
    ├── LAB-2-CAGE.md   (45 min — run both scenarios, compare blue detection)
    └── LAB-3-LOOP.md   (stretch — close the improvement loop)
```

---

## What Each Path Uses

There are three supported ways to run this package, and none of them asks you
to open an account or paste a key:

- **Recorded mode** makes no network calls at all
- **The local helper** reuses a Claude Code sign-in you already have
- **Ollama** runs open-weight models on hardware you already own

See `ATTENDEE-SETUP.md`.

---

## Getting Help

**During the session:** Talk to the presenter.

**Using an AI assistant:** Open `WORKSHOP-GUIDE.md` and paste its contents into claude.ai (or any chat LLM) before asking your question. The guide gives the AI full context about all three demos, provider options, error messages, and lab flow — so you'll get accurate, specific answers instead of generic troubleshooting advice.

**After the conference:** These three HTML files are self-contained — they keep
working offline, on any machine, with no dependency on this package or on us.
