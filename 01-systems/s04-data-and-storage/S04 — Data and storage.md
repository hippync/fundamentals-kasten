---
id: "t-s04"
title: "S04 — Data and storage"
type: "theme"
theme:
  - "S04"
ladder: "Systems ladder"
tags:
  - "theme"
  - "systems"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# S04 — Data and storage

*Theme · Systems ladder · The Fundamentals Reset (Field Manual, Edition 2026)*

**Data and storage**

## Why now

This is the highest-leverage theme on the list. Schema and query decisions outlive every framework you'll wrap around them, and they're the hardest thing to change later. AI will happily generate a query that does a full table scan on 40 million rows.

## Concepts on this rung

- [[Normalization and denormalization]]
- [[B-tree indexes]]
- [[Composite indexes and the leftmost prefix]]
- [[Query plans]]
- [[ACID]]
- [[Isolation levels and anomalies]]
- [[Transaction scope]]
- [[Storage engine choices]]

## Answer these

Straight from the manual. Unchecked means you can't yet answer it out loud, without notes.

- [ ] Normalization: what problems does it solve, and when do you deliberately denormalize?
- [ ] How does a B-tree index work well enough to predict which queries it helps and which it doesn't?
- [ ] Why does a composite index on (a, b) help `WHERE a = ? AND b = ?` but not `WHERE b = ?`
- [ ] Read a query plan. Explain why the planner made that choice.
- [ ] ACID: define each letter precisely. Then define the isolation levels and what anomaly each one permits.
- [ ] What does a transaction actually hold, and for how long, and what does that do to concurrency?
- [ ] When is a document store, key-value store, or column store genuinely the right call — and when is it fashion?

## Build to learn

- [[Index tuning on real volume]] — Load a few million rows. Write a slow query. Read the plan. Add the index. Read the plan again.

> Load a few million rows. Write a slow query. Read the plan. Add the index. Read the plan again. Do this until query plans stop being intimidating.

## Canonical sources

- [[Designing Data-Intensive Applications]]
- [[Use The Index, Luke!]]

## Blocks

- [[Block 09-10 — Data & storage]]
- [[Block 11-12 — Data, part 2 (transactions)]]
