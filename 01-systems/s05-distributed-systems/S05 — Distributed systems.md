---
id: "t-s05"
title: "S05 — Distributed systems"
type: "theme"
theme:
  - "S05"
ladder: "Systems ladder"
tags:
  - "theme"
  - "systems"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# S05 — Distributed systems

*Theme · Systems ladder · The Fundamentals Reset (Field Manual, Edition 2026)*

**Distributed systems**

## Why now

The moment you have two processes, you have a distributed system — and the failure modes are non-obvious in a way that no amount of local reasoning prepares you for.

## Concepts on this rung

- [[The eight fallacies of distributed computing]]
- [[CAP theorem]]
- [[Strong vs eventual consistency]]
- [[Exactly-once delivery]]
- [[Idempotency]]
- [[Partial failure]]
- [[Consensus and Raft]]
- [[Circuit breakers]]
- [[Bulkheads]]
- [[Timeouts]]

## Answer these

Straight from the manual. Unchecked means you can't yet answer it out loud, without notes.

- [ ] The eight fallacies of distributed computing — can you name the failures each one causes?
- [ ] CAP: what it actually says, and why the popular summary is misleading.
- [ ] Strong vs eventual consistency: what does each cost the user, and the developer?
- [ ] Why is exactly-once delivery impossible, and what do people mean when they claim it?
- [ ] What is idempotency, and why is it the single most important property in any retry-capable system?
- [ ] What is a partial failure, and why is it harder than total failure?

## Build to learn

- [[Idempotent job queue]] — Build a job queue with at-least-once delivery. Make the consumer idempotent. Then kill the consumer mid-job and prove it recovers.

> Build a job queue with at-least-once delivery. Make the consumer idempotent. Then kill the consumer mid-job and prove it recovers.

## Canonical sources

- [[Designing Data-Intensive Applications]]
- [[The Raft paper]]
- [[Fallacies of Distributed Computing Explained]]
- [[Release It!]]

## Blocks

- [[Block 13-14 — Distributed systems]]
- [[Block 15-16 — Distributed systems, part 2]]
