---
id: "c-circuit-breakers"
title: "Circuit breakers"
type: "concept"
status: "stub"
theme:
  - "S05"
theme-name:
  - "S05 — Distributed systems"
half-life: "systems concept (~40 years)"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
ladder: "Systems ladder"
tags:
  - "concept"
  - "reliability"
  - "patterns"
---

# Circuit breakers

*Concept · Systems ladder · S05 — Distributed systems · The Fundamentals Reset (Field Manual, Edition 2026)*

> [!question] Predict the failure
> *What breaks when this is absent, wrong, or misunderstood? One sentence, written by you. Until this line exists, the concept is not yours.*

## What it is


## Why it matters now

A stability pattern: stop calling the thing that's failing before you take yourself down with it.

## How it breaks


## Questions I should be able to answer

- [ ] When should the breaker open, and what does the system do while it's open?

## In my own words

<!-- Closed book. One paragraph. If you can't, status stays 'drafted'. -->


## Where I'd look

- [[Release It!]]

## Related

- [[S05 — Distributed systems]]

- [[Timeouts]]
- [[Bulkheads]]
- [[Retries and retry storms]]
- [[Model fallback]]
