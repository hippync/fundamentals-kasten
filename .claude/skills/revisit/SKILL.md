---
name: revisit
description: Spaced re-probe of the concepts whose ledger entries are due, cold and capped at 15 minutes or 10 items. Use when the learner asks to do their revisits or reviews, or `/next` hands off due items.
---

# /revisit

Re-probe what's due, **cold**: the learner answers from memory before seeing anything they wrote. A pass moves the concept up a box; a fail sends it back to box 1 and proposes one status step down. Named `/revisit` so it isn't confused with Claude Code's `/review`.

Write every question by the rules in [../probe/questions.md](../probe/questions.md).

## Steps

1. **Pick.** Run `python3 .claude/tutor/tutor.py due --limit 10`. These items, in this order, are the session; nothing else gets probed. If none are due, say so, offer `/next`, and stop after the log. Run `python3 .claude/tutor/tutor.py letters revisit --count 20` for the correct letter of each question, numbered across the whole session. Run `date +%H:%M` and note the start: the session ends at 15 minutes even if items remain.
2. **Probe each item cold.** For each concept, show only its title. Don't quote the note or the learner's *In my own words* before they answer. Read the note yourself to write the questions:
   - one `consequence` question, then one `failure` question.
   - Both correct: `pass`. One correct: `partial`. Neither: `fail`. E on the first and nothing after: `dont-know`.
   - After the two answers, give the correct answer for any they missed in a sentence or two with its `05-sources/` note. Keep it short: a revisit measures, `/probe` teaches.
   - Then run `python3 .claude/tutor/tutor.py record <id> <result>` and tell them the new box and due date.
3. **On fail or dont-know**, if the concept's status is above `stub`, propose one step down with `#reread`: check it with `python3 .claude/tutor/tutor.py set-status <id> <one step down> --reread --check`, ask, and apply it without `--check` only if the learner says yes. Point at the section to reread. A `stub` has nothing to step down from; just record it.
4. **Stop** after the last item, or when `date +%H:%M` shows 15 minutes gone (check before each item). Items left over stay due for next time; say how many.
5. **Log.** Write the session log to the path from `python3 .claude/tutor/tutor.py log-path revisit`, in the format in `_tutor/README.md` (*Session log*): `skill: revisit`, every id probed under `concepts`, `result` the worst of them, `minutes` from the clock. Body: one line per concept, with result, new box and what to reread, plus any status change and whether it was confirmed.

Done when every probed item has a ledger entry dated today, every fail has had its status proposal answered, and the log file exists.
