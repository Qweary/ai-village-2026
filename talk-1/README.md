# Talk 1: Swarms That Fight and Fix Each Other in a Cage

AI Village, September 2026. One hour, village room, practitioner audience.

Two swarms of AI agents go into a cage. One attacks, one defends, live models calling
live models, and you watch the whole thing happen. Both swarms were built to order:
describe what you want hacked, and a factory builds you one. Then you watch the system
take the result apart.

That teardown is the actual talk. Agents that were never in the fight read what happened,
score it, and rewrite one agent's prompt. One agent, one prompt, one cycle. The scorer is
not the rewriter, because a scorer with a stake in the fix is not a scorer. The exercise
never changes between rounds and the other side is never swapped out, which is deliberate:
if the score moves, the rewrite is the only thing that could have moved it. Sometimes the
verdict is that the rewrite made things worse. That verdict is allowed to stand.

---

## What is in here

| File | What it is |
|---|---|
| `slides/index.html` | The deck. Twenty slides plus four back-pocket slides. |
| `slides/css/deck.css` | Deck styling, with both typefaces embedded inside it. |
| `slides/lib/reveal.js/` | reveal.js 5.1.0, local copy. Three files. |
| `SPEAKER-NOTES.md` | The run sheet, the minute budget, the passages that get said as written, the cut order, and the questions this talk invites. |

The three demos the talk drives live in [`../ai-village-workshop/demos/`](../ai-village-workshop/demos/).
They are separate single-file HTML pages and they are not part of this directory.

---

## Opening the deck

Double-click `slides/index.html`. That is the whole install.

There is no build step, no server, no package manager and no network call. reveal.js sits
in `slides/lib/` beside the HTML, the styling sits in `slides/css/`, and both typefaces
are base64 data URIs inside the CSS. It renders the same on a plane as it does on
conference wifi, which is the point.

Any current browser works. The deck is laid out at 1920 by 1080 and scales to whatever the
room projector turns out to be.

---

## Driving it

Arrow keys or a clicker. Slides do not auto-advance and there are no partial reveals, so
one press is always one whole slide.

| Key | What it does |
|---|---|
| `→` `←` | next and previous slide |
| `b` or `.` | black the screen. **Use this every time you tab over to a demo.** |
| `f` | fullscreen |
| `n` | scanline overlay on and off |
| `c` | darker background, matching the cage and loop pages |
| `h` | show the key list |
| `g` | jump to a slide by name, then Enter |

**Four back-pocket slides** sit after the close and cannot be reached by pressing forward
from it. Reach them with `g`, or with the URL hash:

| Name | Use it when |
|---|---|
| `factory-recap` | the factory demo wedges and you have to speak it instead |
| `cage-recap` | the cage demo wedges |
| `loop-recap` | the improvement loop wedges |
| `withdrawn` | somebody asks why there is no measurement figure anywhere in the talk |

---

## Running the talk

Read `SPEAKER-NOTES.md` before you present. Three things in it are not optional.

**The disclosure at 0:25.** Two of the three demos call a model while the room watches.
One is a recording, and the speaker says so out loud, on stage, with that demo on screen
and nothing moving behind it. The published description opens on "live models calling live
models", which is exactly what makes the disclosure load-bearing rather than a footnote.
The wording is in the notes and it is said close to as written.

**The failure mode at 0:42.** The published description promises "the failure mode that
worries me most" in writing and never says what it is. It gets delivered in speech or it
is simply gone. It is the longest fixed passage in the hour and it is never cut.

**The staged failures at 0:50.** The description commits the talk to showing the briefs
the factory handles and the ones that break it. The failure half does not reliably happen
on its own, so it is staged in advance rather than hoped for. Four of them, listed in the
notes, and one of them is a recording on disk as insurance.

---

## Timing

The run sheet is a one hour budget. Rehearsed, it lands nearer fifty minutes, and that
gap is the question budget. A village room asks questions during the demos, so plan to
spend them from the factory beat and from the success half at 0:50, which are the two
segments with real slack. The notes say which segments to protect.

If you are behind, the cut order is in the notes, and so is the honest warning that three
of the four obvious cuts return much less clock than they look like they would.

---

## What this talk needs from the room

A projector, a laptop, and network access if you are running the two live demos. The
recorded path needs no network at all, and if that is the day you get, the notes carry a
variant of the disclosure that moves to minute three and gets bigger.

The talk also asks the room for briefs: a domain in one sentence, "what do you want a
swarm built for". One of them gets run live during the first demo and walked through at
0:50. It helps to have collected three or four out loud rather than one.

---

## A note on numbers

There is no score figure, no improvement delta and no dispersion constant anywhere in this
deck. That is deliberate, and the reason is a beat in the talk.

Every number this talk used to carry was withdrawn for the same reason: the speaker went
looking for the run transcripts the number came out of, and they were not there. One of
the three withdrawn figures turned out to be the arithmetic difference of the other two.
What replaced them is the shape rather than the size, plus a procedure the room can run on
their own system.

If you are editing this deck later, the last section of `SPEAKER-NOTES.md` lists what must
never go back onto a slide, and why.
