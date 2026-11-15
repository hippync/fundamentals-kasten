---
name: next
description: Plans what the learner should do now from the current block, due revisits and concept statuses. Use when the learner asks what to do next or work on today, or names the time they have ("I have 45 min").
argument-hint: "[minutes]"
---

# /next

Answer "what should I do now?" with an ordered plan that fits the time the learner has. The order comes from `tutor.py`, not from judgment, so the same kasten on the same day always gets the same plan.

## Steps

1. **Progress.** Run `python3 .claude/tutor/tutor.py progress`.
   - If it says `missing`, this is the first run. Ask for the current block (e.g. `blk-01-02`), the day they started the program and the session language (default English). Read `08-decisions/ADR-0001 — Choosing the primary language.md`: if its *Decision* is written, take the primary language from it; otherwise leave it blank. Then run `python3 .claude/tutor/tutor.py init-progress --block <id> --start <YYYY-MM-DD> --language <lang> [--primary <lang>]`.
   - Done when `progress` prints the four fields.
2. **Time.** Take the minutes from the argument or the learner's message. If neither gives one, ask once; on no answer, use 60.
3. **Plan.** Run `python3 .claude/tutor/tutor.py plan --minutes <n>`. It orders: due revisits first (capped at 10 items, 15 minutes), then two systems concepts and one AI concept from the block's themes (drafted before stub, each 20 minutes), then the block's first unfinished build.
4. **Present.** Give the *Now* list in that order, one line each: the time, the skill to run, and the note by title with its id. Say in a clause why each is there (due since when, its status, the block's build). Put *Next session* items in one line. Keep the order exactly as the script gives it; if the learner wants a different order, they choose and you follow.
5. **Hand off.** Ask which step to start; run that skill when they say.
6. **Log.** Write the session log to the path from `python3 .claude/tutor/tutor.py log-path next`, in the format in `_tutor/README.md` (*Session log*): `skill: next`, `concepts: []`, `result: none`, `minutes` as planned. The body is the plan as given, in two or three lines.

Done when the learner has the plan and the log file exists.

## What a stub needs

A `stub` gets `/probe` first: probing finds where understanding runs out before the learner opens a source, which tells them what to read for. The learner then writes the note's sections themselves (Rule 1).
