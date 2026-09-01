---
id: "t-a2"
title: "A2 — Inference mechanics"
type: "theme"
theme:
  - "A2"
ladder: "AI ladder"
tags:
  - "theme"
  - "ai"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# A2 — Inference mechanics

*Theme · AI ladder · The Fundamentals Reset (Field Manual, Edition 2026)*

**Inference mechanics — the engineering reality**

## Why now

This is the layer people skip and then get surprised by their bill.

## Concepts on this rung

- [[The context window]]
- [[KV cache]]
- [[Prompt caching]]
- [[Temperature and sampling]]
- [[Time to first token vs tokens per second]]
- [[Model non-determinism]]

## Answer these

Straight from the manual. Unchecked means you can't yet answer it out loud, without notes.

- [ ] What is the context window, physically? Why does cost scale the way it does with it?
- [ ] What is a KV cache, and why does it make prompt caching possible?
- [ ] Temperature and sampling: what are you actually adjusting?
- [ ] Where does latency come from — time to first token vs tokens per second — and which does your use case care about?
- [ ] Why is the same prompt not guaranteed to give the same output, and when does that matter?

## Build to learn

- [[Cost model for one workload]] — Build a cost model for one real workload: tokens in, tokens out, cache hit rate, dollars per request.

> Build a cost model for one real workload: tokens in, tokens out, cache hit rate, dollars per request.

## Canonical sources

- [[Provider API documentation]]

## Blocks

- [[Block 03-04 — The toolchain & shell]] *(paired as the AI theme: Inference mechanics)*
