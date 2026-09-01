---
id: "t-a5"
title: "A5 — Tools and agents"
type: "theme"
theme:
  - "A5"
ladder: "AI ladder"
tags:
  - "theme"
  - "ai"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# A5 — Tools and agents

*Theme · AI ladder · The Fundamentals Reset (Field Manual, Edition 2026)*

**Tools and agents**

## Why now

An agent is not a mystical thing. It's a model + a loop + tools + state + a stopping condition. Once you see it that way, the engineering problems become recognizable — they're the distributed systems problems from Part 1.

## Concepts on this rung

- [[What an agent actually is]]
- [[Tool calling at the protocol level]]
- [[Error compounding in loops]]
- [[Agent state]]
- [[Stopping conditions]]

## Answer these

Straight from the manual. Unchecked means you can't yet answer it out loud, without notes.

- [ ] What is function/tool calling actually doing at the protocol level?
- [ ] In a multi-step loop, how do errors compound? (If each step is 95% reliable, what's a 10-step chain?)
- [ ] Where does state live between steps, and what happens when a step fails halfway?
- [ ] What's your stopping condition, and what happens without one?
- [ ] Which tasks genuinely need a loop, and which are one call with better prompting?

## Build to learn

- [[Three-step agent with real error handling]] — Build a 3-step agent with real error handling. Measure compounding failure across the loop.

> Build a 3-step agent with real error handling, then measure compounding failure across your loop.

## Canonical sources

- [[Designing Data-Intensive Applications]]
- [[Release It!]]

## Blocks

- [[Block 11-12 — Data, part 2 (transactions)]] *(paired as the AI theme: Tools & agents)*
- [[Block 13-14 — Distributed systems]] *(paired as the AI theme: Agent reliability)*
