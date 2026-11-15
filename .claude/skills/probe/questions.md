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
- Exactly one correct option. Move it around: across a session, the correct letter is spread over A–D, not parked on B or C.
- Label the level in the header (`recall`, `mechanism`, `consequence`, `failure`), so the learner sees the climb.

## Writing the options

1. Write the correct claim first, as one plain sentence.
2. Make each distractor by **mutating** that sentence: swap the cause and the effect, change a quantity by an order of magnitude, swap in the neighbouring concept, flip a condition (always/never, before/after). Each distractor is a misconception someone actually holds, so a wrong pick tells you *which* one.
3. Even them out: same length within a few words, same register, same grammar. None carries its reasoning ("…because the cache is cold"); the options are claims, the reasoning is what you dig for after.
4. Formatting is uniform: bold, code and italics appear in all options or none.
5. Each option stands alone. No "all of the above", "both A and C" or "none of these".

Done when you could swap the correct option's letter with any distractor's and nothing about the layout would give it away.

## Levels

| Level | Asks | Example stem |
|---|---|---|
| `recall` | what it is | Which of these describes a system call? |
| `mechanism` | how it works | What happens to the calling thread during a blocking `read()`? |
| `consequence` | what follows from it | Why does a loop of 1-byte `read()`s run slowly? |
| `failure` | what breaks and how it shows | A service makes 10k small writes per request. What do you see first under load? |

A `failure` question is the concept's *Predict the failure* asked as a scenario. It's the top of the climb.
