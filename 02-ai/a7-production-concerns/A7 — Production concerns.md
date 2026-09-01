---
id: "t-a7"
title: "A7 — Production concerns"
type: "theme"
theme:
  - "A7"
ladder: "AI ladder"
tags:
  - "theme"
  - "ai"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# A7 — Production concerns

*Theme · AI ladder · The Fundamentals Reset (Field Manual, Edition 2026)*

**Production concerns**

## Why now

The gap between a demo and a system is entirely in this section.

## Concepts on this rung

- [[Cost per request]]
- [[Model fallback]]
- [[Prompt injection]]
- [[Human in the loop]]
- [[Guardrails in code]]

## Answer these

Straight from the manual. Unchecked means you can't yet answer it out loud, without notes.

- [ ] What's your cost per request, and what's the biggest term in that equation?
- [ ] What's your fallback when the model API is down or slow?
- [ ] Prompt injection — why is it structurally the SQL injection of this decade, and why is it harder to fix?
- [ ] Where do you need a human in the loop, and what does the interface for that look like?
- [ ] What are your guardrails, and are they enforced in code or hoped for in the prompt? (Only one of those is real.)

## Build to learn

- [[Attack your own agent]] — Attack your own agent with prompt injection. Then enforce one guardrail in code rather than in the prompt.

> Attack your own agent. Then enforce one guardrail in code rather than in the prompt.

## Canonical sources

- [[Release It!]]
- [[OWASP Top 10 and Cheat Sheet Series]]

## Blocks

- [[Block 21-22 — Security]] *(paired as the AI theme: Prompt injection)*
- [[Block 23-24 — Operations]] *(paired as the AI theme: Production AI)*
- [[Block 25-26 — Correctness & testing]] *(paired as the AI theme: Guardrails & human-in-loop)*
