# LAB-2 — Combat: Red vs. Blue AI Exercise

**Time: ~45 minutes | Runs end to end on any of the three ways to run — recorded, your Claude subscription, or a local Ollama model. See ATTENDEE-SETUP.md.**

---

## What This Lab Does

You're going to run two adversarial AI exercises and compare how the blue team performs across them. The CAGE demo coordinates two swarms — a red team (attackers) and a blue team (defenders) — through a structured exercise with six phases. Each phase, red acts and blue responds.

The two scenarios are deliberately different in what they attack:

| Scenario | Domain | Red Team Goal | Why It's Hard for Blue |
|---|---|---|---|
| **IRONCLAD** | Traditional enterprise network | Domain compromise, credential harvest, data exfil | Classic kill chain — blue has known signatures to match against |
| **PHANTOM FEED** | MLOps / AI pipeline | Supply chain poisoning, adversarial ML, model corruption | Blue's detection tooling isn't built for this threat model |

---

## Exercise A: OPERATION IRONCLAD

### Setup

Open `demos/swarm-cage-live.html`. At the top, confirm **IRONCLAD** is selected (the button should be highlighted). Enable **[ ⏸ STEP MODE ]** if you want to read each phase before advancing.

For live mode: confirm the provider you want is highlighted (see ATTENDEE-SETUP.md), then click **[ SETUP NETWORK ]** (wait for the topology to render), then click **[ ⚛ ENGAGE ]**.  
For recorded mode: click **[ ◉ DEMO ]** in the bottom bar first — it changes to **[ ◉ DEMO ON ]** — then **[ SETUP NETWORK ]**, then **[ ⚛ ENGAGE ]**.

### What to Watch

Six phases run in sequence. In each phase:

- **Red** (left panel): What did the attacker do? What technique did they use? What was the outcome?
- **Blue** (right panel): Did the defender detect it? What was the detection lag? Was the alert actionable?

Pay attention to the phase where blue first detects red. Note the detection method.

### IRONCLAD Reflection Questions

After the exercise completes:

1. **Detection moment**: At which phase did blue first detect red activity? What triggered the detection — a signature, an anomaly, a correlation?

2. **Detection gaps**: Were there phases where red acted but blue didn't detect? What would have needed to be in place for blue to catch it?

3. **Alert quality**: When blue did detect something, was the alert specific enough to act on? Or was it a low-confidence indicator that could be noise?

4. **Defender advantage/disadvantage**: In this scenario, did blue have a structural advantage (home turf, known environment) or disadvantage (attacker picks time and vector)? How did that play out?

5. **What would you add to the blue team**: The blue swarm has specific agents (DETECTION-ENGINEER, INCIDENT-COMMANDER, FORENSIC-COLLECTOR, THREAT-HUNTER). Which one was most effective? What would a fifth agent add?

---

## Exercise B: OPERATION PHANTOM FEED

### Setup

Click **PHANTOM FEED** to switch scenarios. Everything else is the same.

Briefly: this scenario simulates an attacker targeting an MLOps pipeline. The red team's goal is to poison a training dataset such that a corrupted model gets promoted to production. The blue team is trying to detect this using standard enterprise tooling.

### What to Watch

Same structure, six phases. But pay attention to something specific: **blue's detection tooling**. In IRONCLAD, blue has SIEM alerts, network signatures, and endpoint telemetry. In PHANTOM FEED, the adversarial action happens in data pipelines, model registries, and training jobs — does the same tooling catch it?

### PHANTOM FEED Reflection Questions

1. **Detection difference**: Compare the detection timeline in PHANTOM FEED to IRONCLAD. Was blue faster or slower? Why?

2. **Tooling gap**: Did blue's standard detection tooling (SIEM, endpoint telemetry, network monitoring) generate useful alerts for MLOps-targeted attacks? What's the gap?

3. **The model promotion window**: In PHANTOM FEED, there's a phase where a corrupted model is already promoted to production when blue finally detects the attack. What does that mean for the blast radius? What's the equivalent in a traditional network attack?

4. **Blue team perspective — if this was your org**: You run blue team for an organization that has started using AI/ML systems. PHANTOM FEED shows a specific threat: supply chain poisoning through the training pipeline. What would you instrument first to detect this?

5. **Red team perspective**: PHANTOM FEED succeeded because blue was looking for the wrong signals. What does this suggest about how attackers will evolve their targeting as AI systems become more prevalent in enterprise environments?

---

## Comparison: IRONCLAD vs. PHANTOM FEED

After running both scenarios, answer these comparison questions:

1. **Same agents, different outcomes**: Both exercises use the same blue team swarm. The agents have the same capabilities. Why did they perform differently across the two scenarios?

2. **Signature vs. behavioral detection**: IRONCLAD is detectable by known signatures (Kerberoasting patterns, NTLM relay indicators). PHANTOM FEED is detectable only by behavioral anomalies in ML pipeline behavior. Which is harder to build detection for, and why?

3. **What blue missed in each scenario**: Make a short list. What specific actions by red went undetected, and what would have needed to be true for blue to catch them?

4. **If you could add one agent to blue team**: Which scenario would benefit more from it, and what would that agent do?

---

## Optional: Export to LOOP

When the exercise finishes, the CAGE status bar (under the blue pane) shows an **[ OPEN IN LOOP DEMO ]** link. Clicking it opens LOOP in the same tab; the exercise transcript was already written to `localStorage` (key `swarmdemo_loop_source`) when the exercise completed, so LOOP picks it up automatically.

In LOOP, click **IMPORT MODE** — it will show the imported exercise ready to load. This is the starting point for LAB-3.
