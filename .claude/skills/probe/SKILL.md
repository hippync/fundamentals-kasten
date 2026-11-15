---
name: probe
description: Probes a concept with closed-book graded questions until the learner's understanding breaks, then records it in the ledger. Use when the learner asks to be probed, quizzed or tested on a concept, or `/next` hands off a concept.
argument-hint: "<concept id or title>"
---

# /probe

Find where the learner's understanding of one concept runs out, before explaining anything. The output is a **break point**: the deepest level they answer correctly and the first they don't. You explain in chat; the note stays untouched, and the result goes to the ledger.

Write every question by the rules in [questions.md](questions.md).

## Steps

1. **Load.** Run `python3 .claude/tutor/tutor.py concept "<argument>"`. It gives the id, status, ledger entry, prerequisites (the concepts in the note's *Related*, in order) and the note's questions. Read the note and its *Where I'd look* sources yourself, so your questions and corrections are grounded in them. If the learner hasn't named a concept, ask which one.
2. **Close the book.** Ask the learner to close the note and any sources. Tell them: one question at a time, answer with a letter, E is always "I don't know".
3. **Prerequisites.** For each prerequisite, up to three: one `mechanism` question. Correct: move on. Wrong or E: one easier follow-up to locate the gap, then move on. A gap here is a finding in itself: name it at the end, and keep going with the main concept.
4. **Climb.** Probe the concept itself, starting at `recall`.
   - After a correct answer, jump: skip a level when you can, and make the next question harder than feels polite. You're looking for the edge, not confirming the middle.
   - After a wrong answer or E, **dig**: ask one or two questions at the same level or one below, from a different angle, until you can say what's missing (the misconception the picked distractor encodes, or the piece that isn't there). Conclude only once the digging agrees.
   - End on a `failure` question: the note's *Predict the failure* asked as a scenario. Then ask for the failure in one sentence of their own; this is the closest to *Predict the failure* a probe gets.
   - Done when you have a break point for the concept, or the learner answered the `failure` question correctly and their own sentence names a real failure (what breaks, under what condition), not a definition.
5. **Explain.** Teach only the gap the break point shows. Socratic by default: ask the question that gets them one step past the break, and explain only what their answer shows is still missing. Expository when they ask for it or say they're low on energy: explain directly, then ask one question that checks it landed. Back every factual claim with a note in `05-sources/` (title and the section to open); a claim you can't trace there is said to be `#unsourced`. All of it in chat: what they take away, they write in the note themselves.
6. **Record.** For the concept and each prerequisite you probed, run `python3 .claude/tutor/tutor.py record <id> <result>`:

   | Result | When |
   |---|---|
   | `pass` | correct through the `failure` question, and the one-sentence failure is real |
   | `partial` | correct at `recall`/`mechanism`, broke at `consequence` or `failure` |
   | `fail` | broke at `recall` or `mechanism` |
   | `dont-know` | chose E at the first question and nothing after got further |

   A prerequisite answered correctly at `mechanism` is a `pass`; otherwise `fail`, or `dont-know` if they chose E.
7. **Log.** Write the session log to the path from `python3 .claude/tutor/tutor.py log-path probe`, in the format in `_tutor/README.md` (*Session log*): `skill: probe`, the block from `progress`, every id you recorded under `concepts`, `result` the worst of them. Body: what was asked, where it broke (the misconception, in a sentence), what to reread and which source.

Done when every probed concept has a ledger entry dated today, the log file exists, and the learner has heard the break point and what to reread.

## Status

`/probe` changes no status. If the concept is a `stub`, end by pointing the learner at the section the break point says to write first.
