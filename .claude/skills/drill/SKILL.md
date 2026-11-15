---
name: drill
description: Runs a theme's Answer these questions one at a time, the learner answering in their own words, graded with the gap named. Use when the learner asks to drill or be quizzed on a theme (S01, A5…), or on all questions.
argument-hint: "<theme code, id or title | all>"
---

# /drill

The recall drill from [Questions — index](../../../00-meta/indexes/Questions%20—%20index.md): open questions, answered out loud in the learner's own words, with the book closed. You grade each answer and name the **gap**. The answer itself stays the learner's to find.

## Steps

1. **Load.** Run `python3 .claude/tutor/tutor.py questions <argument>`: a theme code, id or title, or `all`. Each question has a key (`S01.3`) and a tick if the learner already said they can answer it. Drill the unticked ones in order; if all are ticked, ask whether to drill them anyway. For `all`, ask how many to do this session (default 10) and start from the first unticked.
2. **Read the ground truth.** For each question, find the concept notes the theme lists under *Concepts on this rung* and their `05-sources/`. Grade against those, not against memory.
3. **Ask one at a time.** Show the question exactly as written, then wait. No options, no hints up front.
4. **Grade** each answer in two or three lines:
   - **Grade:** `pass` (correct and complete enough to say out loud), `partial` (right direction, a named piece missing) or `fail` (wrong or empty).
   - **Gap:** what's missing or wrong, as a fact to check or a question to answer, with the `05-sources/` note to open. A wrong claim gets its correction stated as a fact plus its source; a missing piece gets a question.

   Give the full answer only when the learner asks for it. Then give it in chat, sourced, and grade the question `fail` for today.
5. **Tick on confirmation.** After a `pass`, ask: *can you answer this one out loud, without notes, any day? Tick it?* Only on yes, run `python3 .claude/tutor/tutor.py tick <key>`. It ticks the theme note and *Questions — index* together. After `partial` or `fail`, leave it unticked and name the concept note to reread.
6. **Log.** Write the session log to the path from `python3 .claude/tutor/tutor.py log-path drill`, in the format in `_tutor/README.md` (*Session log*): `skill: drill`, under `concepts` the ids of the concept notes behind the questions that weren't a pass, `result` the worst grade. Body: the theme, one line per question key with grade and gap, and which ones were ticked.

Done when every question in the session is graded, every pass has had its tick question answered, and the log file exists.
