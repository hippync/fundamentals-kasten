---
id: "t-a8"
title: "A8 — Knowing where not to use it"
type: "theme"
theme:
  - "A8"
ladder: "AI ladder"
tags:
  - "theme"
  - "ai"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# A8 — Knowing where not to use it

*Theme · AI ladder · The Fundamentals Reset (Field Manual, Edition 2026)*

**Knowing where not to use it**

## Why now

The most senior judgment in this whole document. Deterministic problems deserve deterministic solutions. If a regex, a SQL query, or a state machine solves it, use those — they're faster, cheaper, testable, and debuggable. Reach for a model when the problem is genuinely fuzzy: natural language, ambiguous input, open-ended synthesis.

## Concepts on this rung

- [[The determinism boundary]]

## Answer these

Straight from the manual. Unchecked means you can't yet answer it out loud, without notes.

- [ ] Is this problem genuinely fuzzy, or am I reaching for a model because it's available?
- [ ] What would the deterministic version cost to build, and what would it cost to run?
- [ ] Can I test and debug the solution I'm proposing?

## Build to learn

- [[Replace a model call with determinism]] — Take one model call in something you've built and replace it with a deterministic solution. Compare cost, latency, and testability.

> Take one model call in something you've built and replace it with a deterministic solution. Compare cost, latency, and testability.

## Canonical sources

_the manual lists none for this rung_

## Blocks

- [[Block 27-28 — Consolidation]] *(paired as the AI theme: Consolidation)*
