# Writing a probe question

Shared by `/probe` and `/revisit`. A probe question measures what the learner can produce, not what they can recognise, so every option has to look equally plausible to someone who doesn't know.

## Shape

```
Q3 · mechanism
<the question, one or two sentences>

A. <option>
B. <option>
C. <option>
D. <option>
E. I don't know
```

- Four options plus **E. I don't know**, always present and always last. Picking it is a clean result, never a failure of nerve: say so the first time it's chosen.
- Exactly one correct option, at the letter `python3 .claude/tutor/tutor.py letters <key>` gives for this question's number (`Q3:B` means Q3's answer is B). Don't pick the letter yourself: left to choose, you park it on C or D. Count every question you ask, follow-ups and prerequisites included.
- Label the level in the header (`recall`, `mechanism`, `consequence`, `failure`), so the learner sees the climb.

## Writing the options

1. Start from the right answer, stated as one plain sentence.
2. Make each distractor by **mutating** that sentence: swap the cause and the effect, change a quantity by an order of magnitude, swap in the neighbouring concept, flip a condition (always/never, before/after). Each distractor is a misconception someone who half-knows the topic would hold, so a wrong pick tells you *which* one.
3. Every distractor has to survive a reader who knows nothing but the stem. Never one that contradicts the stem, and never an absurd one ("overwrites the stored system prompt"): if common sense alone rules it out, replace it.
4. Even them out: same length within a few words, same register, same grammar. None carries its reasoning ("…because the cache is cold"); the options are claims, the reasoning is what you dig for after.
5. Don't let the stem point at the answer. A word or idea from the stem ("unbounded queue", "swapped") appears in every option or in none, never only in the answer.
6. Mix the valence. If the stem asks what goes wrong, the distractors go wrong too, just in the wrong way; don't make the answer the only bad outcome among three benign ones, or the only good one.
7. A number or phrase from the answer appears in at most one distractor. Two options sharing "40%" tells the reader the answer is one of them.
8. Formatting is uniform: bold, code and italics appear in all options or none.
9. Each option stands alone. No "all of the above", "both A and C" or "none of these".

Done when you could swap the correct option's letter with any distractor's and nothing about the layout would give it away, and someone who has read only the stem couldn't narrow it below four.

## Levels

| Level | Asks | Example stem |
|---|---|---|
| `recall` | what it is | Which of these describes a system call? |
| `mechanism` | how it works | What happens to the calling thread during a blocking `read()`? |
| `consequence` | what follows from it | Why does a loop of 1-byte `read()`s run slowly? |
| `failure` | what breaks and how it shows | A service makes 10k small writes per request. What do you see first under load? |

A `failure` question is the concept's *Predict the failure* asked as a scenario. It's the top of the climb.
