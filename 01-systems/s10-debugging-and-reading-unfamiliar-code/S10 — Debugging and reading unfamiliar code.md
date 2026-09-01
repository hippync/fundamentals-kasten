---
id: "t-s10"
title: "S10 — Debugging and reading unfamiliar code"
type: "theme"
theme:
  - "S10"
ladder: "Systems ladder"
tags:
  - "theme"
  - "systems"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# S10 — Debugging and reading unfamiliar code

*Theme · Systems ladder · The Fundamentals Reset (Field Manual, Edition 2026)*

**Debugging and reading unfamiliar code**

## Why now

The highest-leverage addition to the entire list. AI makes everyone a permanent maintainer of code they didn't write. That used to be an occasional condition — inheriting a legacy system. Now it's the default condition of the job. Debugging also resists automation hardest, because it requires context the model doesn't have: your data, your load, your history, your users, what changed last Tuesday.

## Concepts on this rung

- [[Debugging as the scientific method]]
- [[Bisecting in space and time]]
- [[Reading a stack trace]]
- [[Entering an unfamiliar codebase]]
- [[Debugger vs logging vs profiler vs packet capture]]
- [[Heisenbugs]]

## Answer these

Straight from the manual. Unchecked means you can't yet answer it out loud, without notes.

- [ ] Debugging is the scientific method: observe → hypothesize → design the minimal experiment → test → repeat. Can you name the hypothesis you're currently testing? If not, you're guessing.
- [ ] How do you bisect a problem in space (which component) as well as in time (which change)?
- [ ] Can you read a stack trace all the way down and say what each frame was doing?
- [ ] What's your strategy for entering a 200k-line codebase you've never seen?
- [ ] When do you reach for a debugger vs logging vs a profiler vs a packet capture?
- [ ] What's a heisenbug, and what does its existence tell you about the system?

## Build to learn

- [[Fix a real OSS bug]] — Pick an open-source project you use and fix a real bug in it. The bug is irrelevant; the navigation skill is the point.

> Pick an open-source project you use and fix a real bug in it. The bug is irrelevant; the navigation skill is the point.

## Canonical sources

- [[Debugging (Agans)]]
- [[Working Effectively with Legacy Code]]
- [[The Pragmatic Programmer]]

## Blocks

- [[Block 19-20 — Debugging & reading code]]
