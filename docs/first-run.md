# First run

Fifteen minutes, start to finish. You do not need an account, an API key, or an
internet connection.

---

## The shortest version

Open `index.html` in a browser. Double click it in a file manager, or drag it
onto a browser window. Everything in this package is reachable from that page.

That is the whole setup for the recorded path, which is enough to watch both
talks and run all three labs.

---

## Step 1: check the machine

```bash
bin/doctor.sh          # macOS and Linux
bin\doctor.ps1         # Windows PowerShell
```

It prints a `PASS` / `WARN` / `FAIL` line per check and finishes with two
verdicts:

```
  RECORDED PATH: READY   open index.html and present
  LIVE RELAY:    READY   run bin/start.sh
  warnings: 0
```

Read them separately. `RECORDED PATH: READY` means you can present, whatever the
second line says. `LIVE RELAY` only matters if you want real model calls.

The script exits 0 when both are ready and 1 otherwise, so it can gate a script
of your own.

---

## Step 2: pick how you want to run

There are three supported ways, and none of them asks for a key or an account.
`ai-village-workshop/ATTENDEE-SETUP.md` is the full page on all three. The short
version:

| | What it is | Setup time | Needs internet |
|---|---|---|---|
| Recorded playback | Replays a real captured run, no network calls at all | none | no |
| Your Claude subscription | A local helper reuses the sign in you already have | about 3 min | yes |
| A local model | Ollama on your own machine | about 10 min, mostly download | only to download |

They are alternatives, not tiers. The recorded runs are captured from real runs
and every phase, pane, and export works. It is also what the presenter uses on
stage, because it is the only one that does not care about conference wifi.

---

## Step 3a: recorded playback

1. Open `index.html`.
2. Click one of the three demo cards.
3. Find the recorded playback button in the demo and turn it on.
   - `swarm-factory-live.html`: `[ ◉ DEMO MODE ]`, at the bottom of the left sidebar, scroll down
   - `swarm-cage-live.html`: `[ ◉ DEMO ]`, in the bottom bar
   - `improvement-loop-live.html`: `[ ◉ DEMO ]`, in the bottom bar
4. The label changes to `ON` and a notice appears saying no key is needed.
5. Start the run.

One limitation, stated plainly: in the factory demo the `CUSTOM` swarm type is
disabled in recorded mode, because there is no recording of a brief you have not
written yet. The preset swarm types all play in full, and labs 2 and 3 run end
to end.

---

## Step 3b: live calls through your Claude subscription

```bash
bin/start.sh           # macOS and Linux
bin\start.ps1          # Windows PowerShell
```

That single command runs the doctor, sets up a Python virtualenv if one is
needed, mints an access token for the relay, starts the relay, and opens the
landing page with the token already attached. The demo cards on that page carry
the token through, so live mode works without you copying anything.

Stop it with Ctrl+C.

What it needs: the `claude` command working in your terminal, and Python 3.9 or
later. The doctor checks both. `ai-village-workshop/CLAUDE-CODE-SETUP.md` has
the detail, including what the relay does and why it requires a token.

If you would rather start the relay yourself:

```bash
cd ai-village-workshop
python3 relay.py
```

The relay prints its own access token and a ready made link for each demo. Click
one of those links instead of using the landing page. The relay listens on
`127.0.0.1:3001` only, and that port is fixed.

---

## Step 3c: a local model

See `ai-village-workshop/OLLAMA-SETUP.md`. Short form: install Ollama, pull a
model, pick `OLLAMA` as the provider inside a demo. The relay is not involved,
so `bin/start.sh` is not needed for this path.

Time one call before the session so you know what your hardware does:

```bash
time ollama run llama3.2 "Write a 300-word incident summary."
```

If that is slow, use recorded mode for the labs and keep the local model for one
phase you want to watch run on your own machine.

---

## When something is wrong

1. Run `bin/doctor.sh` and read the `FAIL` lines. Each one carries a fix.
2. For an error message from inside a demo, `ai-village-workshop/WORKSHOP-GUIDE.md`
   has a section on the common ones.
3. That same guide is written to be pasted into a chat assistant before you ask
   it a question about this package. It gives the assistant enough context to
   answer about these files specifically rather than in general.

Two failures worth knowing in advance:

- **The demo says the relay token is missing.** The relay mints a new token
  every restart. Reopen the demo from the link the relay printed, or restart
  through `bin/start.sh` so the landing page carries the fresh token.
- **Port 3001 is busy.** The relay hardcodes that port. Stop whatever is holding
  it. The doctor tells you whether the thing on that port is already a healthy
  relay, in which case you do not need a second one.
