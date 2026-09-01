---
id: "t-s01"
title: "S01 — The machine"
type: "theme"
theme:
  - "S01"
ladder: "Systems ladder"
tags:
  - "theme"
  - "systems"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# S01 — The machine

*Theme · Systems ladder · The Fundamentals Reset (Field Manual, Edition 2026)*

**The machine — how code actually executes**

## Why now

AI generates code that is correct far more often than it is appropriate. Nearly every 'it works but it's slow' problem traces to this layer, and it's the layer the model can't see because it doesn't know your hardware, your data size, or your access pattern.

## Concepts on this rung

- [[Latency numbers]]
- [[Memory hierarchy and cache locality]]
- [[Stack vs heap]]
- [[System calls]]
- [[The OS scheduler and blocking IO]]

## Answer these

Straight from the manual. Unchecked means you can't yet answer it out loud, without notes.

- [ ] What's the actual cost difference between a CPU cycle, an L1 cache hit, a RAM access, an SSD read, and a network round trip? (Orders of magnitude, not numbers.)
- [ ] Stack vs heap: what determines which one your data lands in, and why do you care?
- [ ] What is a system call, and why is it expensive?
- [ ] What does the OS scheduler do when your thread blocks on I/O?
- [ ] Why is iterating an array faster than iterating a linked list of the same size?

## Build to learn

- [[Measure cache locality]] — Write the same tight loop two ways — one cache-friendly, one not — and measure.

> Write the same tight loop two ways — one cache-friendly, one not — and measure. Feel the 10x.

## Canonical sources

- [[Computer Systems — A Programmer's Perspective]]
- [[Operating Systems — Three Easy Pieces]]
- [[Latency Numbers Every Programmer Should Know]]

## Blocks

- [[Block 01-02 — The machine]]
