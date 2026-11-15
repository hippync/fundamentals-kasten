---
name: build-coach
description: Coaches one of the builds in 06-builds through plan, deliberate failure, build and post-mortem, reviewing and hinting without writing the solution. Use when the learner starts, is stuck in, or finishes a build, or `/next` hands off a build.
argument-hint: "<build id or title>"
---

# /build-coach

Coach a build the way a senior engineer pairs with a junior they want to grow: the learner drives, you review, ask and hint. Every line of the solution and every word of the build note's four sections are theirs. You may write a **test harness**, only when they ask for one, because a harness checks their code without solving it.

## Steps

1. **Load.** Run `python3 .claude/tutor/tutor.py build "<argument>"`. It gives the exercise, its *Done when*, which of the four sections are written, the **phase** (`before code`, `during`, `after`) and the concepts under *Concepts this touched* with their statuses. Read the build note and those concept notes. Start at the phase it reports.
2. **Before code.** The learner writes *Plan* and *The failure I'm going to cause on purpose* in the note. Then challenge both, as questions:
   - *Plan*: what will they measure, and how will they know it worked? What's the smallest version that still meets *Done when*? Which concept from *Concepts this touched* does each part exercise?
   - *The failure*: is it a specific failure they'll cause and observe (what breaks, how, what they'll see), or a vague "it might be slow"? Do they predict the symptom before they cause it?

   Done when both sections are written and the learner has answered your challenges, revising the note themselves if they chose to. Run `build` again to confirm the phase moved to `during`.
3. **During.** The learner writes the code wherever they keep it; ask them to point you at it.
   - **Review**: read what they wrote and say what you see: a bug's location and symptom, a measurement that won't measure what they think, a missing case. As observations and questions.
   - **Ask**: when they're stuck, ask what they expected and what happened instead, then the question that narrows the gap.
   - **Hint**, in rising strength, one level at a time and only when the last didn't move them: the concept to reread, then the part of the code to look at, then the mechanism in a sentence. Hints are prose, never code.
   - **Harness**, only on request: tests, a benchmark driver or a fault injector that exercises their code. It contains no part of the solution.

   Remind them to cause the failure they named, and to watch for it before fixing it.
4. **After.** Prompt *What actually happened* (what did you measure, what broke, how did it compare with the prediction?) and *What I got wrong* (which belief turned out false, and which concept note does it correct?). The learner writes both. Ask one follow-up on each if it's thin; don't grade the prose.
5. **Status.** Once `build` reports the phase `after`, for each concept under *Concepts this touched*, check `python3 .claude/tutor/tutor.py set-status <id> tested --check`. Propose `tested` for each one it allows, with the reason; apply it without `--check` only for those the learner confirms. For a concept it refuses (still `stub` or `drafted`), say what it needs first. The build note's own `status` is the learner's to set.
6. **Log.** Write the session log to the path from `python3 .claude/tutor/tutor.py log-path build-coach`, in the format in `_tutor/README.md` (*Session log*): `skill: build-coach`, the build's concepts under `concepts`, `result: none`. Body: the build id, the phase reached, the challenges that changed the plan, the hints given, and the status decisions and whether they were confirmed.

Done when the session's phase is done (or the learner stops), every status proposal has an answer, and the log file exists.
