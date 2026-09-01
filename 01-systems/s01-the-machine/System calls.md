---
id: "c-system-calls"
title: "System calls"
type: "concept"
status: "stub"
theme:
  - "S01"
theme-name:
  - "S01 — The machine"
half-life: "systems concept (~40 years)"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
ladder: "Systems ladder"
tags:
  - "concept"
  - "os"
  - "runtime"
---

# System calls

*Concept · Systems ladder · S01 — The machine · The Fundamentals Reset (Field Manual, Edition 2026)*

> [!question] Predict the failure
> *What breaks when this is absent, wrong, or misunderstood? One sentence, written by you. Until this line exists, the concept is not yours.*

## What it is


## Why it matters now

The boundary between your process and the kernel — and a boundary is always a cost.

## How it breaks


## Questions I should be able to answer

- [ ] What is a system call, and why is it expensive?

## In my own words

<!-- Closed book. One paragraph. If you can't, status stays 'drafted'. -->


## Where I'd look

1. **[[Operating Systems — Three Easy Pieces]]** — ch. 6, *"Limited Direct Execution."* Free, and exactly this topic. The chapter title is the answer to "why does the boundary exist."
2. **[[Computer Systems — A Programmer's Perspective]]** — ch. 8, *Exceptional Control Flow*: the hardware view of the same event.
3. **Primary:** `man 2 syscalls` lists every one; `man 2 read` gives the contract for a single call.

**Build to learn:** `strace -c java -version` under WSL. `-c` counts calls per type. A program you thought was simple will make hundreds.

## Related

- [[S01 — The machine]]

- [[The OS scheduler and blocking IO]]
- [[Containers]]
