---
id: "c-the-os-scheduler-and-blocking-i-o"
title: "The OS scheduler and blocking I/O"
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
  - "concurrency"
---

# The OS scheduler and blocking I/O

*Concept · Systems ladder · S01 — The machine · The Fundamentals Reset (Field Manual, Edition 2026)*

> [!question] Predict the failure
> *What breaks when this is absent, wrong, or misunderstood? One sentence, written by you. Until this line exists, the concept is not yours.*

## What it is


## Why it matters now

Explains why 'blocking inside an event loop' is catastrophic rather than merely slow.

## How it breaks


## Questions I should be able to answer

- [ ] What does the OS scheduler do when your thread blocks on I/O?

## In my own words

<!-- Closed book. One paragraph. If you can't, status stays 'drafted'. -->


## Where I'd look

1. **[[Operating Systems — Three Easy Pieces]]** — free and primary, per [[The source hierarchy]]:
   - **ch. 4, *The Abstraction: The Process*** — the three states and the transition diagram. Ten pages, and it is the core of this note.
   - **ch. 6, *Mechanism: Limited Direct Execution*** — what a context switch physically saves and restores. Already the source for [[System calls]].
   - **ch. 8, *Multi-Level Feedback Queue*** — why I/O-bound threads get boosted.
   - **ch. 36, *I/O Devices*** — interrupts vs. polling, and when polling is actually the better choice (fast devices, short waits).
   - **ch. 33, *Event-based Concurrency*** — read this one alongside [[Event loops and blocking]].
2. **[[Computer Systems — A Programmer's Perspective]]** — ch. 8, *Exceptional Control Flow*: the same event seen from the hardware.
3. **Primary:** `man 7 epoll`, and `man 2 select` for the historical version of the same idea.

**Build to learn:** run something that blocks on a socket, then `cat /proc/<pid>/status | grep ctxt_switches` before and after. Voluntary switches climb with I/O; involuntary switches climb with CPU contention. Two numbers, and they tell you which problem you have. `pidstat -w 1` watches the same thing live.

## Related

- [[S01 — The machine]]

- [[Event loops and blocking]]
- [[Concurrency vs parallelism]]
- [[System calls]]
- [[Latency numbers]]
- [[Memory hierarchy and cache locality]]
