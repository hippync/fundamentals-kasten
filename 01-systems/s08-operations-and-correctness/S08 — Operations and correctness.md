---
id: "t-s08"
title: "S08 — Operations and correctness"
type: "theme"
theme:
  - "S08"
ladder: "Systems ladder"
tags:
  - "theme"
  - "systems"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# S08 — Operations and correctness

*Theme · Systems ladder · The Fundamentals Reset (Field Manual, Edition 2026)*

**Operations and correctness**

## Why now

'It works on my machine' was never acceptable, but now that generation is fast, the bottleneck has moved entirely to verification. Your ability to tell good output from bad output is the whole job.

## Concepts on this rung

- [[Logs, metrics, and traces]]
- [[SLOs]]
- [[Rollback procedures]]
- [[The test pyramid]]
- [[Property-based testing]]
- [[Invariants]]

## Answer these

Straight from the manual. Unchecked means you can't yet answer it out loud, without notes.

- [ ] Logs, metrics, traces — what question does each one answer that the others can't?
- [ ] What's an SLO, and how does it turn into an engineering decision?
- [ ] What does your rollback procedure look like, and have you actually run it?
- [ ] The test pyramid: what's the right shape, and why do most codebases get it upside down?
- [ ] What's a property-based test, and when is it stronger than example-based testing?
- [ ] What invariants does your system have, and are any of them enforced by the type system?

## Build to learn

- [[Instrument and break]] — Instrument something you own with traces. Then cause an incident on purpose and see if your telemetry actually tells you what happened.

> Instrument something you own with traces. Then cause an incident on purpose and see if your telemetry actually tells you what happened.

## Canonical sources

- [[Site Reliability Engineering]]
- [[Release It!]]
- [[Working Effectively with Legacy Code]]

## Blocks

- [[Block 23-24 — Operations]]
- [[Block 25-26 — Correctness & testing]]
