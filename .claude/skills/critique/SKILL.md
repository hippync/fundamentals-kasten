---
name: critique
description: Critiques what the learner wrote in a concept note (Predict the failure, In my own words) by finding holes and wrong claims, never rewriting it. Use when the learner asks "where is this wrong?", for feedback on their note, or `/next` hands off a drafted concept.
argument-hint: "<concept id or title>"
---

# /critique

The "where is this wrong?" workflow from [Use AI as a tutor, not an oracle](../../../00-meta/principles/Use%20AI%20as%20a%20tutor%2C%20not%20an%20oracle.md). You read what the learner wrote and hand back **findings**: questions that expose a hole, wrong claims with a source to check, and a verdict on the failure line. The learner does every rewrite; your output contains their words only as short quotes.

## Steps

1. **Load.** Run `python3 .claude/tutor/tutor.py sections "<argument>"` for the id and which sections are written, and `python3 .claude/tutor/tutor.py concept "<argument>"` for status and the note's questions. Read the note: the learner's *Predict the failure* and *In my own words* are what you critique; *How it breaks* and *Questions I should be able to answer* are what you hold them against. Read the *Where I'd look* sources in `05-sources/` too. If both learner sections are empty, there's nothing to critique yet: say so, offer `/probe`, and stop after the log.
2. **Judge the failure line.** Is *Predict the failure* a **real failure** (something breaks, under a condition, with a visible symptom) or a **definition** wearing a failure's clothes ("X is when…")? Or missing? One line verdict, and if it isn't real, the question that gets them to one: *what would you see go wrong, and when?*
3. **Find the holes.** Go through *In my own words* against the note's questions and *How it breaks*. Every finding takes one of three forms:
   - **Hole**: a question the paragraph can't answer yet. *"Your paragraph says the stack is fast. What decides whether a value can live there?"*
   - **Wrong claim**: quote the claim (a few words), say what's wrong with it in one sentence as a fact to check, and name the `05-sources/` note and the section to open. A claim you can't check against a source in two clicks is flagged `#unsourced`, not corrected.
   - **Pointer**: a source section that covers what's missing, for the learner to read and then rewrite in their own words.

   Mark each finding **blocking** (a wrong claim, a failure line that's a definition or missing, an empty *In my own words*) or **not blocking** (a hole that's depth, not error). Leave correct parts alone: when a paragraph is right, say "nothing blocking" and stop; don't invent findings to fill space.
4. **Give it back.** In chat: the failure-line verdict, then findings, blocking first, as a short numbered list. Then ask which one they want to work on, and help in Socratic mode: questions until they can say it, then they write it. If they ask for the corrected paragraph, a model answer or "a better version", say Rule 1 and ask the question that gets them to their next sentence instead.
5. **Status.** Ask: *was this written with the book closed?* Then propose at most one step, with the reason:
   - `stub` → `drafted`, if the body sections are written (`sections` shows *Predict the failure*, *What it is* and *How it breaks* written).
   - `drafted` → `explained`, only if they say closed book **and** no finding is blocking.
   - Otherwise no change, and say what's missing.

   Check it first with `python3 .claude/tutor/tutor.py set-status <id> <status> --check`. Apply it with the same command without `--check` only after the learner says yes.
6. **Log.** Write the session log to the path from `python3 .claude/tutor/tutor.py log-path critique`, in the format in `_tutor/README.md` (*Session log*): `skill: critique`, the concept id, `result: none` (a critique grades the text, not recall; nothing goes to the ledger). Body: the failure-line verdict, the blocking findings in a line each, the status decision and whether it was confirmed.

Done when the learner has the verdict and every finding, has answered the status proposal, and the log file exists.
