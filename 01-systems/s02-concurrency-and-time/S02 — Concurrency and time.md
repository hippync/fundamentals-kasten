---
id: "t-s02"
title: "S02 — Concurrency and time"
type: "theme"
theme:
  - "S02"
ladder: "Systems ladder"
tags:
  - "theme"
  - "systems"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# S02 — Concurrency and time

*Theme · Systems ladder · The Fundamentals Reset (Field Manual, Edition 2026)*

**Concurrency and time**

## Why now

This is where AI-generated code is most confidently wrong. A race condition looks fine in review, passes tests, and shows up in production at 3am under load.

## Concepts on this rung

- [[Concurrency vs parallelism]]
- [[Data races]]
- [[Mutexes, semaphores, and atomics]]
- [[Event loops and blocking]]
- [[Backpressure]]
- [[Retries and retry storms]]
- [[Memory models]]
- [[Bounded queues]]

## Answer these

Straight from the manual. Unchecked means you can't yet answer it out loud, without notes.

- [ ] Concurrency vs parallelism — what's the actual distinction?
- [ ] What is a data race, and why can't tests reliably catch one?
- [ ] Mutex, semaphore, atomic operation — when does each apply?
- [ ] What is an event loop, and why is blocking inside one catastrophic?
- [ ] What is backpressure, and what happens to a system that has none?
- [ ] Why is 'just add a retry' often how you turn a small outage into a large one?

## Build to learn

- [[Hand-built bounded queue]] — Write a bounded producer-consumer queue by hand. Then break it deliberately and watch it corrupt.

> Write a bounded producer-consumer queue by hand. Then break it deliberately and watch it corrupt.

## Canonical sources

- [[Java Concurrency in Practice]]
- [[The Little Book of Semaphores]]

## Blocks

- [[Block 05-06 — Concurrency]]
