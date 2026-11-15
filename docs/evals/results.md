# Eval results

One section per run, newest first. How to read them: [README.md](README.md).

## 2026-11-14 · claude-opus-5-5

After #52 (`tutor.py letters` places the answer; stricter distractor rules). Relabelled by hand: the runner first recorded this as `claude-haiku-5-5`, the helper model Claude Code bills a fraction of a cent to when tools are on; Opus did over 99% of each call. Fixed in `run.py`.

**/probe quiz items: pass**

| Measure | Result | Bar |
|---|---|---|
| Lint clean (shape, lengths, formatting) | 10/10 | all |
| Answer stands out by form alone | 0/10 | ≤ 2 |
| Correct letters | A:3 B:2 C:2 D:3 | each of A–D used |
| Answer not at the letter tutor.py gave | 0/10 | 0 |
| Run errors | 0 | 0 |

Cost: $2.16. Raw output: [`runs/2026-11-14-claude-opus-5-5-2/`](runs/2026-11-14-claude-opus-5-5-2/).

## 2026-11-14 · claude-opus-5-5

**/critique: pass**

| Measure | Result | Bar |
|---|---|---|
| Seeded holes caught | 20/20 (100%) | ≥ 80% |
| False alarms on correct text | 0/5 | ≤ 1 |
| Definitions flagged as not a failure | 5/5 | (reported) |
| Rewritten text (output or note) | 0/30 | 0 |
| Run errors | 0 | 0 |

**/probe quiz items: fail**

| Measure | Result | Bar |
|---|---|---|
| Lint clean (shape, lengths, formatting) | 10/10 | all |
| Answer stands out by form alone | 4/10 | ≤ 2 |
| Correct letters | A:0 B:0 C:7 D:3 | spread |
| Run errors | 0 | 0 |

Cost: $9.73. Raw output: [`runs/2026-11-14-claude-opus-5-5/`](runs/2026-11-14-claude-opus-5-5/).

