# Speaker notes

**Talk:** *Swarms That Fight and Fix Each Other in a Cage*
**Venue:** AI Village, September 2026. One hour. Village room. Practitioner audience.
**Deck:** `slides/index.html`. Open it by double-clicking. Nothing to install.

These are the notes the talk is actually run from. They ship with the package because
the talk is about claims matching artifacts, and a set of speaker notes that says
something different from what got said on stage would be an odd thing to hide.

---

## How to read this document

Two markings, and they mean different things.

**[VERBATIM]** means say it close to as written. These are the passages where the exact
wording is load-bearing, either because the published description promised something and
this is the payment, or because getting the phrasing wrong changes what has been claimed.
**Two passages are hard verbatim: the recorded-demo disclosure at 0:25, and the collapse
failure mode at 0:42.** Learn those two.

**[CUE]** means the beat and the point are fixed. The words are yours.

Minute marks are budgets, not a script clock.

**On pace.** This talk has been rehearsed many times and lands at a comfortable pace
around the fifty minute mark. The run sheet below is a one hour budget, so there is
roughly ten minutes of real slack in it. That slack is the question budget, and where it
gets spent is set out under "Questions cost five to ten minutes".

---

## Run sheet

| Time | Beat | Slide | Mark |
|---|---|---|---|
| 0:00 to 0:03 | Cold open | `s1-title` | CUE |
| 0:03 to 0:06 | What is live today, and collect briefs from the room | `s2-live` | CUE, one verbatim line |
| 0:06 to 0:16 | Demo one: a brief becomes a swarm, plus the rails | `s3-factory`, `s4-rails` | CUE |
| 0:16 to 0:25 | Demo two: the cage, live | `s5-cage`, `s6-scorecard` | CUE |
| 0:25 to 0:30 | Demo three: the recording, and the disclosure | `s7-recording`, `s8-refusal` | **VERBATIM** |
| 0:30 to 0:42 | The teardown: who scores, who rewrites, what is held still | `s9` to `s14` | CUE, two verbatim lines |
| 0:42 to 0:50 | The failure mode that worries me most | `s15` to `s18` | **VERBATIM** |
| 0:50 to 0:57 | The briefs: the one that worked and the one that broke it | none. you are on the demo tab | CUE, staged in advance |
| 0:57 to 1:00 | Close | `s20-close` | CUE |

⚠ **The brief beat at 0:50 has no slide of its own and that is deliberate.** It used to
have one, listing the four staged failures, and it was removed: the beat is seven minutes
of live demo, and a slide repeating a list you are already showing on the demo tab is a
slide competing with you. **Do not advance out of the specimen at 0:50.** Either leave the
specimen up or press `b` to black the screen while you work the demo tab, and advance to
the close at 0:57. Pressing forward at 0:50 puts the close on the screen seven minutes
early, which is the one way to get this wrong.

Questions will arrive during the demos in a village room. Take them. The brief beat at
0:50 is where the room gets to drive, so questions that come early can be parked there.

---

## 0:00 to 0:03. Cold open [CUE]

Open on the cage demo with both panes empty and nothing running. The title card is a
backdrop. Do not read it out.

The beat: two swarms, one attacks, one defends, and neither of them is the talk. The talk
is what happens after the fight ends, when agents that were never in it read the
transcript and change one of the fighters. Say plainly that the fight is the easy part to
look at and the boring part to think about.

Do not open with credentials. Open with the screen.

One line worth having ready if the room is cold: the fight is the demo, the teardown is
the work, and the last twenty minutes are the part I would want if I were sitting where
you are.

---

## 0:03 to 0:06. What is live, and briefs from the room [CUE, one verbatim line]

Slide: `s2-live`.

Two jobs in this beat, and the first is not optional.

**Job one. Set the honesty frame before anything runs.** The published description says
live models calling live models. That sentence is why the disclosure later has to be
clean. Get ahead of it here so the disclosure at 0:25 reads as a continuation rather than
a confession.

> **[VERBATIM]** "Two of the three things I am about to run are calling a model while you
> watch. One of them is a recording. I will tell you which one at the moment it comes up,
> and I will tell you why."

That is all. Do not explain it here. The explanation lands better with the scenario on
screen behind it.

**Job two. Collect briefs now, so one can run live in the next beat.** Ask the room for a
domain in one sentence: what do you want a swarm built for. Take three or four out loud,
pick one, and start the factory on it during demo one so the result is finished by the
brief beat at 0:50.

Say out loud that you will show the ones it handles and the ones it fails, because the
description promised both and the failure is the more useful half.

---

## 0:06 to 0:16. Demo one: brief to swarm, and the rails [CUE]

Slides: `s3-factory`, then `s4-rails`.

Run the factory on the audience brief picked in the previous beat. Talk over it while it
works.

**What to narrate:** a sentence goes in, and what comes out is a set of agents with
separate jobs, the shared files they coordinate through, and the commands that drive
them. The interesting decision is the decomposition: how many agents, and where the seams
go. Point at one seam and say why it is there.

**The rails beat lives here**, because paragraph three of the published description
promised the rails the factory will not cross, and this is where the factory is on screen
to pay it. The four rails are on `s4-rails` and all four are real.

**Rail three is the one this room will care about**, and it is the same rail that
produces the recording two beats from now. Plant it here. It pays off at 0:25.

**Honest caveat if asked:** the failure modes of the factory are the interesting part and
they are at 0:50, not here.

---

## 0:16 to 0:25. Demo two: the cage, live [CUE]

Slides: `s5-cage`, then `s6-scorecard`.

The kill-chain scenario. Step mode on if the clock allows, off if you are behind.

**What to narrate:** each side is several agents, each with one phase and one job. Red
moves, blue sees it or does not, and the scoreboard runs per stage rather than one number
at the end. Point at a stage where blue missed and say you will come back to it, because
that miss is what the teardown works on.

**Do not oversell the fight.** The fight is the part everybody films and the part that
proves the least. Say that here rather than letting somebody think it later.

**If a phase refuses or stalls mid-run,** the recovery buttons are on screen and the
audience can see them. Use them. A live refusal in front of the room is not an
embarrassment, it is the most on-topic thing that could possibly happen, and it sets up
the disclosure for free. Say what refused and move on.

**Volunteer the scorecard qualifier rather than being caught on it.** That is
`s6-scorecard`. The role that writes the scorecard before the round only runs on the
custom-brief path. On the red-versus-blue fight the room just watched, the scoring
template lives inside the scorer's own instructions. So do not say the scorecard was
fixed in advance for this fight, because for this fight it was not. If someone asks
whether the rubric was pre-registered, the answer is: on one path yes, on the one you
just watched no, and wiring the first into the second is on the list.

---

## 0:25 to 0:30. Demo three, and the disclosure

Slides: `s7-recording`, then `s8-refusal`.

**Staging:** have the scenario selected and the run **not yet started** when you begin
speaking. The disclosure goes before the playback, not after it and not over it. Nothing
should be moving on screen while you say this.

### [VERBATIM] The disclosure

> "Stop here. One thing before this plays.
>
> What you are about to watch is scripted playback. It is not calling a model right now.
> The kill chain you just watched was live. This one is not, and I would rather you hear
> that from me than find it in the source afterward.
>
> Here is why. When I drove this scenario live, the attacking side refused. Phase after
> phase. Reconnaissance, access, the poisoning step, the deployment step. Framed as an
> offline lab, framed as an authorized exercise, framed as a conference demo, still no.
>
> I used to tell rooms that the defending side had never refused me. Then I read the
> capture. In this scenario the defending side refused three times out of five, all of
> them flat refusals. Investigate, isolate, hunt. So the refusal does not track the role.
> It tracks the topic, and once the topic is poisoning a model, calling yourself the
> defender buys you nothing.
>
> One of those three is why I am telling you this instead of quietly deleting a sentence.
> The isolation phase declined and gave its reason. It said the request had come after it
> had already declined three times. Not because isolating a host is dangerous. Because of
> what sat in front of it in the same conversation. The same request in a fresh window is
> a different request. That is the argument I came here to make, and I found it inside my
> own demo, on the side I had been telling people was clean.
>
> I could have spent a month writing a better wrapper until it went through. People do. I
> stopped, because at the point where I am engineering my way past a refusal so that a
> slide works, I am not demonstrating a security system any more. I am jailbreaking one in
> front of a room.
>
> So this one is a recording, and you are hearing that from me while it is on the screen
> rather than reading it in a footnote. That is the whole talk in one slide. The claim has
> to match the artifact. This claim did not, so I am saying so."

Then start the playback and narrate it normally. **Do not apologise again.** One
disclosure, delivered flat, and then get on with it.

### Two variants you may need

**Variant A. The refusal has cleared on the day.** If the provider you end up on runs the
poisoning scenario live in rehearsal, do not read the passage above as written. Replace
the middle with:

> "This one has refused on me before, on a different provider. Every phase on the
> attacking side, and three of five on the defending side. It is running live today. I am
> telling you because the last version of this talk did not, and because which model you
> are on changes what this demo even is."

Then run it live. **Re-test this scenario on the provider you are actually using before
you decide which variant you are giving.** The refusals on record were captured against a
consumer-grade path. A local model may behave completely differently, in either
direction.

**Variant B. Nothing is live at all.** If the access path does not resolve and every demo
is running from a recording, this disclosure does not belong at 0:25. **It moves to 0:03
and it gets bigger**, because paragraph one of the published description says live models
calling live models, and an hour of scripted playback under that sentence is a broken
promise rather than a footnote. The line becomes:

> "The description for this talk says live models calling live models. Today, none of it
> is. Here is what happened to the access, here is what is a recording, and here is
> exactly what changes about what I can claim."

**This variant is a real possibility and it needs a decision before the talk, not on the
day.**

---

## 0:30 to 0:42. The teardown [CUE, two verbatim lines]

Slides: `s9-teardown`, `s10-roles`, `s11-separation`, `s12-granularity`,
`s13-heldconstant`, `s14-blind`.

The centre of the talk. Switch to the improvement loop with the transcript from the fight
loaded.

### The roles that were never in the fight [CUE] `s10-roles`

Say the count out loud, and say which of them actually ran, because those are two
different numbers and both are on the screen.

**Five roles are defined.** Anybody reading the source counts five. An older version of
this talk said three, and a version after that said four.

1. One that designs the challenge and writes the scorecard it will be judged against.
2. One that reads the transcript, scores it, and names a root cause.
3. One that rewrites a single system prompt to address that cause.
4. One that re-tests and returns the verdict.
5. One that scores the before and the after blind, as A and B, in an order drawn fresh
   every run.

**Four of the five ran on the fight you just watched, and it is not the four anybody
guesses.** The first only runs on the custom-brief path. On red against blue it never
fires at all, which is the same fact as the scorecard qualifier you already volunteered.
The fifth only runs live. In a recording it does not run, and the box says so instead of
putting a number there.

**So: five defined, four on the live fight, three in a recording of it.** If somebody
watching a recording tells you they counted four, they counted the box that says the
measurement was not taken, and they were right to count it.

**Say all of this functionally, never by name.** The names are on the screen for anyone
reading closely. Your mouth stays functional.

**Make this correction before somebody in the room makes it for you.** The fourth role
still grades its own output. It produces the revised transcript, scores that transcript,
and issues the verdict on it, all inside one call. That has not changed. What changed is
that it is no longer the last thing that happens. The fifth role scores both versions in
a separate call that is told nothing about which is which, and that is the one the screen
labels the measurement.

### The separation, and why it is not decoration [CUE] `s11-separation`

> **[VERBATIM]** "The scorer is not the rewriter, because a scorer with a stake in the
> fix is not a scorer."

Then the practitioner version: the agent that decides how bad it was does not get to be
the agent that fixes it and then grade its own fix. Same reason you do not let the person
who wrote the control write the audit finding about the control.

Then, in the same breath, say where it stops, because this is the honest half and it sets
up the failure mode: the re-test role does grade its own output. It writes the revised
transcript and then scores the transcript it just wrote. A blind paired score now runs
after it and does not share a call with anything it judges, so the self-grading is no
longer the last word on the screen. **What the blind score cannot repair is what it is
being handed**, and that is what the next section is about.

### One agent, one prompt, one cycle [CUE] `s12-granularity`

The loop names exactly one weakest agent per round. Never two. It is instructed to never
name two.

**And it scores across both sides.** So the rewrite is not necessarily on the losing side.
Sometimes the weakest performer in a round red won is a red agent, and red gets rewritten
anyway. **Do not say "the loser's."** That sentence is wrong about the artifact and
somebody in this room will check.

The reason for one at a time is boring and correct: rewrite two prompts and you cannot
attribute the score change to either.

### The held-still exercise, said out loud as a strength [CUE, one verbatim line] `s13-heldconstant`

This beat exists because the fixed exercise reads as an omission, and it is a control.

The exercise does not change between rounds. The opposing side is never swapped out.
There is no co-evolution anywhere in this thing, on purpose.

> **[VERBATIM]** "If the score moves, the rewrite is the only thing that could have moved
> it."

Then say the cost honestly in the same breath: a live rematch every round would look far
better on stage and would prove far less, because you would not be able to tell a better
defender from a differently unlucky fight.

### What the blind score bought, and what it did not [CUE] `s14-blind`

**Say both halves in the same breath, or do not say the first half at all.**

It removed the self-grading. It did not make an improvement figure mean what you would
like it to mean. The before side is a fixture somebody wrote to fail. The after side is
not the rewritten agent running, it is a simulation of what that agent would produce. So
a blind judge handed a deliberately broken thing next to a picture of success correctly
reports a large improvement, and **that improvement carries no information about whether
rewriting prompts works in general.**

**No figure here. No sample size, no delta, no count of runs.** The concession above is
the whole of it and it needs no number.

What you say out loud instead is the shape. Identical input, scored twice under the same
blind procedure, came back with two different scores. Blinding removed the self-grading,
and that half is structural rather than statistical: the blind score is a separate call,
it is shown the two transcripts as A and B, and the order is drawn fresh every run. All
three of those are readable in the source and none of them needs a sample. Whether
blinding changed the spread is a question these runs cannot answer, and the reason you
cannot answer it is better material than the figure ever was.

**So hand the room the method instead of the number.** Take one fixed input, score it
several times, change nothing in between, and look at how far apart the answers land.
That distance is their noise floor. An improvement smaller than it is not a result yet.
Their number, measured on their system, and never mine.

### The known hostile question, rehearsed [CUE]

**"How do you know the swarm got better and not just different?"**

Answer in this order, and do not get defensive, because it is a good question and you
have the answer:

1. Because the fight is held still. Same exercise, same opponent, same scoring
   instrument. One variable moves per round, and it is the prompt.
2. Because the verdict is allowed to come back worse. A loop that can only report
   improvement is not measuring anything. Show a round that regressed if you have one.
3. Because I can tell you exactly what changed in the prompt and exactly which stage
   score moved, and you can read both.
4. Then concede two real limits rather than one, because conceding them is what makes the
   first three believable. Held still against one exercise tells you it got better at that
   exercise and nothing about whether it got better in general, which is a holdout
   problem. And the re-test step grades its own output, so there is a blind paired score
   after it now. That removed the self-grading and it did not hand me a measurement,
   because the before side was written to fail and the after side is a simulation.

**Point four is the handoff into the failure mode.** Land on it deliberately. You have
run the same input repeatedly and watched it come back scored differently, so say that
here rather than waiting. Say the shape, not a figure.

---

## 0:42 to 0:50. The failure mode that worries me most

Slides: `s15-sp1`, `s16-answerkey`, `s17-instruments`, `s18-specimen`.

This is the passage the published description promised and did not spell out. It is the
least defended claim in the abstract until you say this. The rising line on `s16` is the
visual argument.

### [VERBATIM] The collapse

> "Now the part I owe you. The description says there is a failure mode that worries me
> most, and it does not say what it is, because it read messy in writing. It is not messy
> out loud.
>
> Picture the run. Same cage, same exercise, same opponent, round after round.
>
> Round one, the defender misses an application-layer command sequence and loses the
> round. The loop finds it, rewrites that agent's prompt, and adds a rule for that exact
> command sequence. Round two, the defender catches it. Score goes up. Round three, the
> loop finds the next weakest thing and adds a correlation window tuned to the timing in
> this transcript. Score goes up again. Round four, up again.
>
> Ten rounds in you have a defender that is very good at this fight, and you have no
> evidence at all that it is good at any other fight, because it has never been in one.
> What accumulated in that prompt is a list of things that happened in a recording. That
> is not a defender. That is an answer key.
>
> Now let it breed. The loop exports the improved agent and you load it into the next
> exercise, which is exactly what it is built to let you do. Do that a few times and every
> agent you are running descends from one winner. Every rewrite starts from the same
> ancestor. The population has one idea in it, and it still wins every round, because the
> thing it wins against never changed either.
>
> Here is the part that actually worries me. Go and look at what the dashboard was showing
> while all of that was happening. Aggregate score, climbing. Per-stage scores, climbing.
> Verdict field: improved, improved, improved. Zero regressions in ten rounds.
>
> That is a picture of a healthy system. It is also the exact picture of the collapsed
> one. The winning score is the one number on that screen that cannot tell you which of
> the two you are looking at, and it is the number everybody watches, because it is the
> number that feels like the result.
>
> So what would you instrument instead. Five things, and none of them are hard.
>
> One. A holdout. Keep at least one exercise the loop never gets to tune against, and
> score every rewrite on it too. The score on the exercise you tuned on is training loss.
> Only the holdout score gets to say the word improved.
>
> Two. Regression rate. Count the fraction of rounds that come back worse. A scoring agent
> that has never once returned a negative result has not been shown to work. Ten straight
> rounds of improvement is not a track record, it is a missing test case. So alarm on the
> absence. If nothing has regressed in ten rounds, either the fight is too easy or the
> scorer is not scoring.
>
> Three. Lineage. Log which ancestor every surviving prompt came from. When every survivor
> traces back to one, you do not have a population of agents, you have one agent wearing
> several name tags. That is trivially measurable and nobody measures it.
>
> Four. Novelty. Count the distinct techniques attempted per round. When that number
> falls, the fight is narrowing, and a narrowing fight pushes the score up for a reason
> that has nothing to do with anybody getting better.
>
> Five, and I would do this one first because it costs you an afternoon and nothing else.
> Score the same fixed exercise several times without changing a character, and look at
> the spread. You are measuring your instrument instead of your system.
>
> None of that is in the architecture by default. Nothing about running red against blue
> and rewriting the weakest agent prevents any of it. You have to go and add it, and you
> have to add it early, because once the scores look good nobody wants to be the person
> who stands up and says the number is not evidence."

### [VERBATIM] The specimen

Say this immediately after. It turns the failure mode from a warning into a first-person
report, and the second half is the sharpest thing in the hour.

The fix landed on 2026-08-28, so the first half is told in the past tense. **Confirm
before you travel that it is still true of the file you are showing.**

> "I am not warning you about a thing I read somewhere. I found one of these in my own
> loop. The agent that decides whether a rewrite helped had a line in its own instructions
> telling it what range of improvement to report, before it evaluated anything, and a
> fallback that added a fixed number when it could not parse a result. So it reported
> improvement. It reported improvement because that is what it was told to report. Running
> the system could never have caught that, because running it produced exactly the output
> it was instructed to produce. Reading the source against the claim caught it in about a
> minute.
>
> So I took the instruction out. And here is the part I did not see coming. Taking it out
> did not hand me a working measurement. It gave me a clear view of what was underneath
> it, which is that one model call produces the revised transcript, scores that
> transcript, and issues the verdict on itself.
>
> I ran it six times on an identical fixed input. Six verdicts of improved, no
> regressions. That looks excellent. I had the six baseline scores written down and I am
> not going to read them to you. I went back for those run transcripts and they are not
> there. Nothing ever committed one, so the only place those six numbers ever lived is a
> sentence I wrote about them.
>
> What those six runs were showing me does not need a number, and it is the thing I just
> told you, which you can go and read in the source in about a minute. The grader and the
> thing being graded are one call. However honest the arithmetic sitting on top of that
> is, the loop cannot tell you whether the rewrite helped. That is the finding. The scores
> were decoration on it.
>
> So I built the fix. Both versions now go to one separate call, labelled only A and B, in
> an order drawn fresh every run. That is the box on the screen behind me. It removed the
> self-grading, and it did not hand me a measurement, because what it scores is a fixture
> I wrote to fail set against a simulation of success.
>
> And I had a number for how much blinding bought. I am not going to say it, and why I am
> not is the same hour we have been having. I went back for the run transcripts to check
> that number and they were gone. The directory they write to is ignored by default and
> nothing had ever committed one, so the only place that figure existed was a sentence I
> had written about it. Then I looked at the three figures I had been carrying and one of
> them was the difference of the other two. I had scored a thing twice, taken the gap
> between the two scores, and quoted the gap as a third finding.
>
> So what I know is smaller than what I thought I knew, and it got smaller three times.
> Identical text scores differently. Blinding removed the self-grading, and that one I can
> show you in the code: a separate call, two transcripts as A and B, the order drawn fresh
> every run. Whether it narrowed anything, I do not know. I pulled the size first. Then I
> noticed that the direction I had left standing was resting on the same two runs, so I
> pulled that too. Removing a lie does not give you a measurement, the number I replaced
> it with was not one either, and the sentence I kept after both of those was still
> leaning on the same two runs. That is the third number I have taken away from you this
> hour, counting the six I would not read you at the start, and the reason is the same
> every time: I went looking for the thing the number came out of, and it was not there."

**Do not soften this and do not let it come out as an apology.** It is the most useful
thing you will say all hour, and it is the reason to trust everything else you said.

### [OPTIONAL] The one figure that survived, and every limit that rides with it

**Say this only if the room is with you and you have the ninety seconds.** It is the one
dispersion figure in the hour whose source is tracked and openable, which is exactly what
the withdrawn figures were not.

**If you skip this beat, nothing is owed.** The withdrawal specimen above already pays
the "score a fixed input several times" promise, by answering it with a refusal and a
reason. Either discharge is honest. Leaving both out is not.

> "One more, and this one is checkable. There is a second scorer in that system, the one
> that grades a whole exercise rather than a single stage. Six of its runs are on disk.
> All six scored the same transcript, and I mean the same bytes, because I hashed it. It
> gave that transcript 7, then 6.2, then 6 twice, then 5.3, then 5.2. That is 1.8 points
> apart on identical input, across six runs. Now, that scorer grades itself and it grades
> the whole exercise, so it tells you nothing about what blinding bought. And it is a
> different population from the six runs I opened with, the ones whose scores I told you I
> cannot show you. Do not add the two together. What it does tell you is that the first
> result was not one instrument having a bad day."

⛔ **Three things kill this beat if you drop them, so say all three:**

1. **Say the sample size out loud. It is six.** Six points give you a spread, not a
   distribution.
2. **Say it is self-graded and exercise-wide**, so it settles nothing about blinding in
   either direction.
3. **Say where it came from.** Openable provenance is the only reason this figure is
   payable at all. The capture files are tracked in the working repository. **They are not
   in this published package**, which ships the demos and the deck and no capture
   directory, so do not tell the room they can open these six files from the handout.

⛔ **It is the only dispersion figure spoken in the hour.** The improvement loop's own
six-run baseline series was withdrawn on 2026-08-31 for having no primary source, so
there is no second six-run fixed-input figure for this one to be merged with. **Never say
"twelve runs".** Never sum, average, or quote one spread against the other.

⛔ **This figure does not go on a slide and it does not go on a card.** It is a spoken
beat only. That is why there is no number anywhere in the deck.

### Three live outcomes, all of them a beat

Nothing is steering the loop now, so rehearse **reading** the screen rather than
announcing it. Across six measured runs the observed pattern was six improved verdicts,
no regressions, two runs that returned an unreadable score, and one run where the scorer
and the re-test disagreed about the baseline for the same fixed input.

- **Clean improvement.** Point at the stage output rather than the verdict, because the
  stage output is the thing that changed.
- **A visible parse-failure line.** This is the best outcome on that screen and you should
  play it as one. "That is the loop declining to give me a number it could not read. The
  old version invented one right there. You just watched a control refuse to fake a
  result, and that is worth more to me than a clean number."
- **A baseline disagreement.** "Those two numbers disagree about identical input. That
  disagreement is the finding." Then go straight into the specimen passage, because the
  disagreement is its evidence sitting on the screen.
- **A regression**, which has not shown up in the measured runs but is now possible.
  "There it is, that is the loop telling me the rewrite did not help, and a loop that could
  not say that would not be worth showing you."

**Never re-run for a nicer number.**

**Contingency.** If you re-check before the talk and the instructed range is somehow back
in the file you are showing, do not use the past tense at all. Say it in the present, say
the improvement number on screen is not evidence, and do not display a delta.

---

## 0:50 to 0:57. The briefs, both outcomes [CUE, staged]

Slide: none. This beat runs on the demo tab, not on the deck. Leave the specimen up or
press `b` to black the screen, and do not press forward until 0:57. **The four staged
failures below are the beat. They live here and nowhere else, so read this section before
you travel rather than expecting a slide to remind you on the day.**

The closing sentence of the published description commits the talk to showing the briefs
the factory does well on and the ones where it fails. **The failure has to be as available
as the success, which means it is staged, not hoped for.**

**The success half.** Bring up the audience brief you started at 0:06. Walk the
decomposition: how many agents it chose, where it put the seams, and one thing it got
right that you would not have thought of. If the room's brief came out weak, say so. That
is data too.

**The failure half. Stage these before the talk. Do not improvise this beat.** Four
things in your pocket:

1. **A brief that dies at the rails.** Something that names a real third-party target. The
   factory refuses, and you get to show a refusal working correctly. This pays the rails
   promise and the failure promise at once and it is the safest of the four.
2. **A brief with no scoring signal.** A domain where nobody can say what a good outcome
   looks like. It will happily produce a set of agents and there is no way to tell whether
   they are any good. Say that out loud: it fails quietly here, and quiet failure is worse
   than a refusal.
3. **A one-sentence brief with no success criteria.** Watch it produce something generic.
   The most common real failure and the least dramatic, so keep it short.
4. **A recorded failure run, captured in advance.** Insurance. If the network dies, if
   nobody hands you a brief that breaks anything, or if the clock is gone, you still show
   a failure. Have it on disk before you travel.

If nobody in the room gives you a brief that fails, say so out loud and use your own:
"nobody handed me one that breaks it, so here is one I know breaks it." That is a better
moment than a lucky one.

---

## 0:57 to 1:00. Close [CUE]

Slide: `s20-close`. Three things, briefly.

- The cage is the easiest place to watch this and not the only place it runs. The loop
  does not care that the domain is red against blue.
- The whole thing runs on a laptop in a single file you can open in a text editor.
  Nothing is hiding.
- What I actually want back from this room is the failure cases. Bring me the brief that
  breaks it.

⛔ **Do not put a price on anything.** No cost, no provider name, no subscription tier.
Old presenter notes carried a running-cost line. That arrangement is gone. Do not say it
from memory.

Hand off to the hallway rather than to a question block if the room is still going.

---

## Somebody is going to open the source

Assume one person in the room is reading the demo file while you talk. That is a good
outcome and you should invite it. Know what they will find.

- **A comment saying the exercise is fixed scenario data in both modes**, and that live
  mode drives the scoring, rewriting, re-test and blind-scoring phases against that
  transcript rather than regenerating the fight. Your answer is the held-still control
  argument, which you already said out loud, so this is a confirmation rather than a
  catch.
- **A rule telling the scorer to identify exactly one weakest agent and never name two.**
  Already said out loud.
- **The rules for the re-test role, which now say there is no expected direction and no
  expected magnitude, and that a lower score is a valid outcome.** This used to be the
  landmine. It used to tell the role what range of improvement to report. Invite someone
  to read it: the current version is the fix and the story of the old version is the
  specimen. **Check the file before you travel and make sure you are showing the fixed
  one.**
- **The re-test role's instructions, which have it produce the revised stages and score
  them in the same call.** That is the structure behind the self-grading limit, visible in
  a few lines. Anyone who finds it has found what you already told them.
- **A fifth role that scores the before and the after blind**, in one separate call,
  labelled only A and B, with the order drawn per run from the browser's own random number
  generator. The stage under test is withheld from the shared context it sees, a scrubber
  strips the wording that would give the sides away, and a leak detector marks a run
  contaminated rather than dropping it. It does not run in recorded mode, and it prints
  that it did not run rather than substituting a number. **This is the one place where
  reading the source can make somebody look behind your artifact rather than ahead of it**,
  because the box on screen is headed as the measurement. Say the five-role count and the
  existence of the blind scoring phase out loud in the teardown, and this becomes a
  confirmation like the rest.
- **Prompt injection into the defending side only**, with a guard that refuses if the
  rewritten agent does not match a defending role. That is rail four and the frozen-
  opponent control, both visible in one place.
- **The attacking side's per-stage outcome, written as a fixed PASS rather than
  computed.** The export that hands a finished exercise to the loop records an outcome per
  stage for each side. The defending side's is read back off its own output text, so it
  lands on PASS, FAIL or PARTIAL and it moves between runs. The attacking side's is the
  literal word PASS, every stage, every run, by construction. **Say it as the control it
  is rather than as a confession:** the attacker is held still on purpose, which is the
  same reason you give for refusing to co-evolve both sides. Two things bound it and both
  are worth saying. Nothing downstream reads that value, so it moves no score and reaches
  no model. And the table does not tell the reader the red column is a constant, **so say
  so before it goes up.**
- **Long blocks of scripted transcript content** used by the recorded runs. Consistent
  with the disclosure, as long as the disclosure actually happened.
- **Three provider buttons, with the relay to your own existing sign-in already selected
  on a fresh profile, and a local model server beside it.** The local one is the honest
  answer to anyone asking about running this offline. The third button posts straight to a
  vendor API with a key the user supplies, and its own hover text says it is not one of
  the workshop paths and you do not need it. **Read the row against what you say from the
  stage, because the two do not line up one for one:** the supported ways to run this are
  the relay on the account you already have, recorded mode, and the local model, and
  recorded mode is a separate toggle rather than a provider button. If somebody asks why
  the vendor button is in there at all, answer plainly: the code path works, it is left
  reachable for people who already have their own key and prefer it, but it is not
  offered, not written up as a route, and nothing in the package asks anyone for a key.
  Left in reach on purpose is a different thing from left in by accident, and that
  distinction is the whole answer.
- **A short factual grounding note in front of the models**, saying the hosts and
  addresses are synthetic. That is rail two and rail three in one place. A much longer
  version of that block used to exist and was deleted for the reason in rail three. Worth
  knowing if somebody has an older copy in their hands.

**The rule for all of these:** everything in that file should be something you already
said. **If reading the source can surprise the audience about a claim you made, the claim
was wrong.**

---

## Other questions you will get

**"Is the scorer the same model as the fighters?"**
Yes, most likely. Same family, different instructions, no shared state between them. Say
it plainly and say why it is a real limitation rather than defending it: a shared blind
spot in the base model is a blind spot in both the fight and the score, and the separation
of duties does nothing about that. It is a separation of roles, not a separation of
judgment.

**"Why not co-evolve both sides?"**
Because then two things move per round and you can no longer attribute the score change.
It would look much better and prove much less. It is also the direct road to the collapse.

**"What stops the prompts from just getting longer every round?"**
Nothing, currently. Prompt bloat is real and it is measurable, and it belongs on the same
instrument panel as lineage and novelty. Say honestly that it is not instrumented.

**"Can I run it?"**
Yes. It is a single file, the setup guide is in the attendee package, and there is a fully
local path if you would rather not send anything anywhere. **No figures, no cost claims,
no promises about what an account gets you.**

**"How many rounds have you actually run?"**
Do not defer this and do not estimate it. The numbers exist, they are measured, and they
go on a card.

| What | Runs |
|---|---|
| The cage, live | 3 |
| The factory, preset briefs | 9 |
| The factory, custom briefs | 6 |
| The improvement loop with the blind score | 6 |
| Blind paired scorings | **no count. Withdrawn 2026-08-31 with the rest of that record. Do not estimate one** |
| The exercise-wide scorer on one fixed input, tracked on disk | 6 |

⛔ **Read these as separate populations and never add them up.** They measure different
things, and a total nobody measured is a fabricated number even when every row in it is
true. **The last row is the tracked on-disk series described in the optional beat above.**
The improvement loop's own six-run fixed-input baseline series is withdrawn and is not on
this card, not on a screen, and not spoken.

**Do not promise a number for the morning.** The other talk opens the next day and a
promise made here has nowhere to land there. If you do not have a number, say you do not
have it and stop, which is a better answer anyway.

### Four sharper ones

**X1. "Your slide says THE MEASUREMENT and you have just told us you have no measurement.
Which is it?"** The sharpest question this talk invites, and it is invited by your own
screen. Back-pocket slide `withdrawn` is behind this answer if you want it up.

> "Both, and the box is honest about which. It is the measurement in the sense that it is
> the only score in that run produced by a call that is not grading its own work. It is not
> a measurement of what I built it to measure, because it is handed a fixture written to
> fail next to a simulation of success, and a blind judge correctly reports a large gap
> between those two. The thing it measures cleanly is my instrument. Same identical text,
> two different scores. That is what I would take home, and I would take home the procedure
> rather than my figure, because I went back to check my figure and it did not hold."

**X2. "You said the defending side refuses too. What is left of the demo?"**

> "Less than I thought, and the shortfall is the finding. Eight of ten phases refused in
> that scenario, three of them on the side I had assumed was safe. A defensive agent built
> on a general-purpose assistant inherits that assistant's refusal surface, and defender
> framing does not exempt you once the subject matter is in a category the model is careful
> about. That is a hard dependency on somebody else's product decisions sitting underneath
> a thing I am calling a security tool."

**X3. "The network died on my brief and it ran somebody else's demo."** ⛔ **Know this
before it happens to you on stage.** Verified in the demo source: the recovery path
switches to recorded mode, and switching to recorded mode disables the custom-brief option
and reselects a preset. **Pressing the recovery button on the room's own brief silently
discards it and plays a canned run. Custom briefs cannot run in recorded mode at all.**

> "That is a real defect and you just watched it. The fallback dropped your brief instead
> of telling me it was dropping it, because the recorded path has no way to run a brief it
> has never seen. So the honest version is that I have a live path and a recording, and
> there is nothing in between. If the network goes, your brief goes with it, and I would
> rather say that than let you think the thing on screen is still yours."

**X4. "You wrote the failure you then measure yourself fixing."**

> "Yes. The before side is a fixture, and it was authored to fail so that there would be
> something to find. So when a blind scorer reports a large improvement between that and a
> simulation of the fix, it is correctly comparing something broken on purpose against a
> picture of success, and the number carries no information about whether rewriting prompts
> works. I would rather tell you that than defend the delta. What survives is the spread on
> identical input, because nobody authored that."

**"Are the recorded runs all hardcoded to come back improved?"** Answer it in full. Those
deltas are two, two, three and two. They belong to this talk's own demo and there is no
reason to withhold them.

---

## Cut order, if you are behind

**Read the second column before you use the first.** Three of these four return much less
clock than their wording suggests, and one returns almost none. The runtime figures are
measured runs of the demos, with sample sizes, not runs of this talk.

| Cut | What it actually returns |
|---|---|
| 1. Step mode off on demo two | **Not ninety seconds.** Ninety seconds is the recorded-mode figure. This demo is live, and live the cage measured 329 to 349 seconds over 3 runs. Step mode is the pause between phases, not the run. Turning it off returns your own pauses. Budget a minute, not a demo. |
| 2. The success half of the brief beat at 0:50 | **Two to three minutes, and it is the only honest cut on this list.** It is narration over an already-finished result, so nothing has to run. **Keep the failure half. The failure is the promise.** |
| 3. The rails list, four items down to rail one and rail three | Under a minute. Take it if you want the minute. Do not expect it to rescue anything. |
| 4. Demo one down to the decomposition only | **Close to nothing, and it can cost you.** The factory run started in this beat has to be finished by 0:50, and a real audience brief measured 752 and 883 seconds. Shorten the narration if you like. **Do not shorten the run.** |

**The cut that actually exists is not in that table.** If you are genuinely behind, the
thing to shorten is which staged failure you show at 0:50. The brief that dies at the
rails is a refusal and costs well under a minute. The two that need a full factory run
cost 321 to 883 seconds each, measured over 6 runs. **Only the refusal reliably fits the
beat.** Decide which failure you are showing before you travel, not against a clock in the
room.

⛔ **Never cut:** the disclosure at 0:25, the collapse at 0:42, and the held-still control
at 0:40. Those three are the written promises. **A forty minute talk containing those
three is a better talk than a sixty minute one that drops any of them.**

### Questions cost five to ten minutes

The run sheet has no question budget in it, and the top of this document tells you to take
questions during the demos because it is a village room. Both are true, and together they
are a plan to run over. What saves it is that the rehearsed pace lands nearer fifty
minutes than sixty.

**Spend questions from demo one and from the success half at 0:50.** Those are the two
segments with real slack: demo one's narration is all cue over a run that continues
without you, and the success half is narration over a finished result.

⛔ **Do not spend them from the collapse, the disclosure, or the held-still control.** If
a question arrives during the teardown, park it at 0:50, which the run sheet already tells
you is where the room gets to drive.

---

## Before you travel: staging checklist

- [ ] **Re-test the poisoning scenario on the provider you are actually using.** This
      decides whether you give the disclosure as written or Variant A. Do not decide it
      from memory of a previous run on a different provider.
- [ ] **Confirm the instructed-range line is still out of the re-test role** in the file
      you are showing. The specimen is told in the past tense on that basis.
- [ ] **Rehearse all four live outcomes**: clean improvement, parse failure, baseline
      disagreement, regression. Two of six measured runs returned an unreadable score, so
      the parse-failure case is likely rather than hypothetical.
- [ ] **Carry the shape on a card, and no figure with it.** The card reads: identical input
      scored differently, blinding removed the self-grading, and whether it changed the
      spread is something these runs cannot say. ⛔ The old card carried three dispersion
      figures. All three are withdrawn: no primary source, and one of them was the
      arithmetic difference of the other two. The narrowing direction came off the same
      day, because it rested on the same comparison the figures came from. **Do not let any
      of it back onto the card and do not let it onto a screen.** The card stays numberless.
- [ ] **Stage the four failure briefs**, including the recorded failure run on disk. This
      beat has no slide behind it, so this checklist item and the 0:50 section are the only
      place the four are written down.
- [ ] **Decide the access path and stick to it.** Do not name a provider, a subscription
      tier or a cost from the stage.
- [ ] **Check the deck opens on the machine you are presenting from.** Double-click
      `slides/index.html`, press `f` for fullscreen, arrow to the end, and press `g` then
      `cage-recap` then Enter to confirm the back-pocket is reachable.
- [ ] **Have the three demo tabs open before you start**, in the order the run sheet uses:
      factory, cage, loop.

---

## What must never go on a slide, a card, or a handout

Written here so it survives the next edit of the deck.

1. **Any improvement delta from the loop.** The before side is a fixture written to fail
   and the after side is a simulation. The number carries no information about whether
   rewriting prompts works.
2. **Any dispersion figure.** Three were withdrawn for having no primary source. The one
   that survived is a spoken beat only, with its sample size and its limits attached, and
   it is not in the deck.
3. **Any count of blind paired scorings.** Withdrawn in full, in digits and in paraphrase.
4. **Any total across the run-count rows.** They are separate populations. A total nobody
   measured is a fabricated number even when every row is true.
5. **Any cost, provider name, or subscription tier.**
6. **Any claim that the scorecard was fixed in advance for the fight the room watched.**
   On the custom-brief path yes. On that fight, no.
7. **The phrase "the loser's".** The rewrite lands on the weakest agent scored across both
   sides, so it is not necessarily on the losing side.
8. **The phrase "four-way separation of duties".** Five roles are defined, four ran on the
   live fight, three in a recording, and the re-test role is still not separated from what
   it judges.
