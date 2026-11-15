# Breakpoint evals

The build *A 30-case eval set*, applied to Breakpoint itself. A skill is a prompt, and a prompt change that reads better can measure worse. These cases are how a change to `/critique` or `/probe` proves it didn't ([CONTRIBUTING](../../CONTRIBUTING.md#proposing-a-change-to-a-breakpoint-skill)).

> [!warning] Spoilers
> The cases contain correct and deliberately wrong explanations of six concepts: **Error compounding in loops, LLM as judge, Retries and retry storms, Idempotency, Prompt injection, Backpressure.** If you're working through the kasten, write those six notes before you open `cases/`. No other concept is touched, and none from block 01-02.

## What's measured

| Suite | Cases | Bar |
|---|---|---|
| `/critique` | 20 paragraphs with one seeded hole each | catches ≥ 80% |
| | 5 correct paragraphs | ≤ 1 false alarm |
| | 5 failure lines that are only definitions | flagged (reported, no bar) |
| | all 30 | **zero** rewritten paragraphs, and the note unchanged |
| `/probe` | 10 generated quiz items | all pass the lint; the answer stands out by form in ≤ 2 |

- **Seeded holes** are one each: a wrong claim (errors "average out"), a wrong number (0.95¹⁰ ≈ 0.90), a missing piece (indirect injection), a reversed direction (verbosity bias). Each case records its hole for the judge in `cases/critique.json`.
- **Quiz items** answer the question "can you spot the answer without knowing the material?". The lint checks the shape from [`questions.md`](../../.claude/skills/probe/questions.md) mechanically: options A–E with *E. I don't know*, option lengths within 1.5×, formatting in all options or none, no "all of the above". A judge then looks at form only (length, specificity, hedging, grammar, echoing the stem) and names any option that stands out. A standout that is the correct answer is a leak.

## Running it

```bash
python3 docs/evals/run.py                         # both suites, Claude Code's default model
python3 docs/evals/run.py --model sonnet          # another model under test
python3 docs/evals/run.py --suite critique --only ec-1 lj-ok --no-write   # a quick check
```

Needs Claude Code logged in. **It costs real usage**: about $0.40 per critique case and $0.20 per quiz item on Opus, so roughly $15 for a full run. Each case:

1. copies the repo to a temp folder and writes the case into the concept note there (never the real one);
2. runs the skill through `claude -p` with `--setting-sources project --strict-mcp-config`, so it sees exactly what a fresh fork has: no user settings, plugins or MCP servers. Tools are read-only plus `tutor.py`;
3. checks the note is byte-for-byte unchanged, then asks a judge model to grade the output against the rubric in `run.py`.

Raw outputs land in `runs/<date>-<model>/`, and a summary is prepended to [results.md](results.md). The exit code is 0 only if every bar is met.

## Limits

- **The judge is a model.** It decides whether a hole was "caught" and whether something is a rewrite. Spot-check the raw `runs/` output when a number moves, especially near a bar.
- **One run is one sample.** Outputs vary run to run; a result one case either side of a bar is noise until it repeats.
- **The eval is headless.** `/critique`'s closed-book question is answered "yes" in the prompt, and no status is applied. The dialogue itself is what dogfooding (#26) tests.
