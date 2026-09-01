---
id: "t-a6"
title: "A6 — Evaluation"
type: "theme"
theme:
  - "A6"
ladder: "AI ladder"
tags:
  - "theme"
  - "ai"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# A6 — Evaluation

*Theme · AI ladder · The Fundamentals Reset (Field Manual, Edition 2026)*

**Evaluation — the real skill**

## Why now

If Part 1 §8 said verification is the bottleneck, this is the AI version, and it's the thing that separates people shipping AI systems from people demoing them.

## Concepts on this rung

- [[Golden datasets]]
- [[What to measure in an eval]]
- [[LLM as judge]]
- [[Prompt regression testing]]
- [[Evaluating a system, not a model]]

## Answer these

Straight from the manual. Unchecked means you can't yet answer it out loud, without notes.

- [ ] What's your golden dataset, and how did you build it?
- [ ] What are you measuring — correctness, format compliance, latency, cost, refusal rate?
- [ ] When is LLM-as-judge valid, and what are its biases?
- [ ] How do you catch a regression when you change a prompt? (You have a test suite for code. Where's the one for prompts?)
- [ ] How do you evaluate a system, not a model, given that the model is one component?

## Build to learn

- [[A 30-case eval set]] — Take any prompt you use regularly. Build a 30-case eval set. Change the prompt. Measure.

> Take any prompt you use regularly. Build a 30-case eval set. Change the prompt. Measure. You'll be shocked how often 'obviously better' is worse.

## Canonical sources

- [[Chip Huyen on AI engineering]]
- [[Hamel Husain on evals]]

## Blocks

- [[Block 17-18 — Design & architecture]] *(paired as the AI theme: Evaluation)*
- [[Block 19-20 — Debugging & reading code]] *(paired as the AI theme: Eval regression suite)*
