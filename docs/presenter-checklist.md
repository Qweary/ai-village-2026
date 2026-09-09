# Presenter checklist

For the person standing at the front of the room. Two lists: one for the night
before, one for the five minutes before you are on.

---

## The night before

Run the doctor on the machine you will actually present from, not the one you
built the talk on.

```bash
bin/doctor.sh
```

You want:

```
  RECORDED PATH: READY
  LIVE RELAY:    READY
```

If the second line says `NOT READY`, decide now whether you care. Recorded
playback runs every demo and every lab. It is the mode the presenter is expected
to use, and it is immune to the venue wifi. `LIVE RELAY: NOT READY` costs you
nothing unless you planned to take a live prompt from the room.

Then, by hand:

- [ ] Open both slide decks and page all the way to the end of each. They are
      single HTML files with everything embedded, so if the first slide renders
      the rest will, but page through anyway and confirm the fonts loaded.
- [ ] Open each of the three demos and play a recorded run start to finish.
      Time one. That number is your real segment length, not the one in the
      outline.
- [ ] Run the talk 2 side demo once: `python3 talk-2/unbounded-split/split_demo.py`.
      It is stdlib only and takes about a second.
- [ ] Put the browser in the presentation mode you will use, at the resolution
      the room projector will use. The demos are dense; check that the smallest
      text is readable from the back.
- [ ] Turn off notifications, screen dimming, and sleep.
- [ ] If you will use live mode: run `bin/start.sh`, drive one real phase end to
      end, and stop it. A working relay yesterday is not a working relay today,
      because the access token is minted per run and the sign in can expire.

---

## Five minutes before

- [ ] `bin/doctor.sh --quiet`. Three lines, five seconds. Read the two verdicts.
- [ ] Open `index.html`. Leave it open. It is your index into everything.
- [ ] Open the deck for the talk you are giving, in its own window.
- [ ] Open the demo you will show first, in its own window, with recorded
      playback already switched on. Do not switch it on in front of the room.
- [ ] If using live mode: `bin/start.sh` and leave the terminal running in a
      window you can see. The relay prints one line per call, so a stall is
      visible to you and not to the audience.

---

## If it fails in the room

The failure order that costs the least time:

1. **A live call hangs.** Switch that demo to recorded playback and keep going.
   The button is in the bottom bar. The recorded run covers the same ground.
2. **A demo will not load.** Open it directly from the file system rather than
   through the landing page. Each demo is one self contained HTML file and has
   no dependency on the landing page or the relay.
3. **The whole machine is unhappy.** Both decks are single files. Copy the deck
   onto any machine with a browser and present from that. Nothing else in this
   package is required to give either talk.

Say what happened. The talks are partly about systems that report success while
having checked nothing, so a visible honest failure is on topic.

---

## What the audience needs afterward

Everything in this package works after the conference, offline, on any machine
with a browser, with no dependency on you or on anything hosted. Point them at
the repository root and at `docs/first-run.md`.

The last two slides of the talk 2 deck are the handout card, front and back.
That is the part worth keeping.
