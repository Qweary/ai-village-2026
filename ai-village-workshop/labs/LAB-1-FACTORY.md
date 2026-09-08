# LAB-1 — Forge Your Own Swarm

**Time: ~30 minutes | Pick one of the three ways to run (recorded, your Claude subscription, or a local Ollama model) — see ATTENDEE-SETUP.md**

---

## What This Lab Does

You're going to describe something you actually do — a real workflow, a real security function, a real operational domain — and watch the framework design a multi-agent AI system for it from scratch.

The FACTORY demo runs a 9-phase pipeline:

| Phase | Agent | What Happens |
|---|---|---|
| P1 | ARCHITECT (Director) | Analyzes your domain, identifies the workflow stages |
| P1b | LIBRARIAN | Decides whether this domain benefits from a searchable knowledge store, and what belongs in it |
| P2 | Domain Advisor | Designs the micro-specialization map — which agents, what each one does |
| P2b | Domain Advisor → LIBRARIAN | Translates the advisor's library spec into a vector collection design |
| **P2c** | **Operator Gate** | **⬥ Interactive pause — read the Domain Advisor + LIBRARIAN output and click [ APPROVE — PROCEED TO FABRICATION ] to continue** |
| P3 | BRIEFER (Research) | Identifies current tooling and techniques for your domain |
| P3b | BUILDER (Fabrication) | Builds each agent: name, role, system prompt, tool requirements |
| P4 | AUDITOR + INSPECTOR (QA) | Validates agents for domain accuracy, structural completeness, and design principles |
| P5 | Packaging | Produces the final swarm package with README and deployment instructions |

---

## Exercise

### Step 1: Open the Demo

Open `demos/swarm-factory-live.html`. Pick your way to run (see ATTENDEE-SETUP.md) — `[ CLAUDE CODE ]` is already selected, `[ OLLAMA ]` is one click, and `[ ◉ DEMO MODE ]` at the bottom of the sidebar needs nothing at all. Enable **[ ⏸ STEP MODE ]** if you want to pause between phases and read each one before continuing.

### Step 2: Write Your Brief

Click **CUSTOM** in the preset selector. A text area appears. Write 2–4 sentences describing:

- What domain or function you work in
- What the main workflow looks like (the steps you repeat)
- What the hardest or most time-consuming part is

**Examples to adapt:**

> I run vulnerability assessments for mid-size enterprise clients. The workflow goes from scoping to recon to scanning to exploitation to reporting. The hardest part is triage — deciding which findings are actually exploitable vs. theoretical.

> I'm a SOC analyst. My day is: ingest alerts, triage, investigate, escalate or close. The bottleneck is context — I spend most of my time trying to understand if an alert is real before I can act on it.

> I do bug bounty on web apps. I start with recon, move to manual testing of auth and business logic, then do a final API-focused sweep before writing the report. The part that takes longest is the auth testing — it's too manual.

You don't have to use security examples. This works for any domain.

### Step 3: Launch and Observe

Click **[ ◆ BUILD SWARM ]** (the button is labeled **[ ▶ RUN DEMO ]** if you have DEMO MODE turned on). Watch each phase run.

> **Phase 2c — Operator Gate:** The pipeline pauses here and shows you the Domain Advisor's micro-specialization map and LIBRARIAN's vector collection design. Read them, then click **[ APPROVE — PROCEED TO FABRICATION ]** (or modify the spec first, or skip the vector layer). This is the only interactive pause in the pipeline.

Key things to notice:

- How does ARCHITECT decompose your description into workflow stages?
- What names does BUILDER give the agents? Do they feel right for your domain?
- Read one or two of the fabricated system prompts — are the tool requirements and domain constraints accurate?
- What does AUDITOR flag? Does it catch anything BUILDER missed?

### Step 4: Reflect

After the run completes, answer these questions (write them down or just think through them):

1. **Decomposition accuracy**: Did the Phase 1 analysis correctly identify the stages of your workflow? What did it miss or get wrong?

2. **Agent design**: Look at the fabricated agents. If you were actually going to use this swarm, which agent would you want to refine first? Why?

3. **System prompt quality**: Pick one fabricated agent and read its full system prompt. Is it specific enough to be useful, or is it too generic? What would you add?

4. **What's missing**: What coordination mechanism would this swarm need that isn't in the fabricated output? (Think about: how do agents hand off state? what shared context do they need? what do they do when they disagree?)

5. **Deploy question**: If you extracted this swarm package and actually ran it, what would be the first real-world test you'd run it against?

---

## If You Have Time: Run It Again

Try a second preset — pick **RED**, **BLUE**, or **INFRA** and run it in recorded mode, which makes no network calls. Compare how the agent decomposition differs between your custom domain and the pre-built preset. Notice that the agent count, specialization depth, and tool requirements shift significantly based on the domain's coordination complexity.

---

## What Comes Next

The swarm FACTORY produces is a starting point, not a finished product. LAB-3-LOOP.md shows you the improvement loop: run an exercise, score the agents, rewrite the one that failed, rerun. After several cycles, the agents are tuned to your actual operational conditions rather than the framework's initial best guess.

The forge output from this lab can be pasted into LOOP's CUSTOM mode if you want to try the improvement loop on your own swarm.
