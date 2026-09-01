---
id: "t-s07"
title: "S07 — Security"
type: "theme"
theme:
  - "S07"
ladder: "Systems ladder"
tags:
  - "theme"
  - "systems"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# S07 — Security

*Theme · Systems ladder · The Fundamentals Reset (Field Manual, Edition 2026)*

**Security**

## Why now

Generated code is plausible-looking by construction. Plausible-looking is exactly what an insecure pattern is. The volume of code shipping has gone up; the volume of review has not.

## Concepts on this rung

- [[Threat modeling]]
- [[Authentication vs authorization]]
- [[OWASP Top 10]]
- [[Parameterized queries]]
- [[Secrets management]]
- [[Supply chain security]]

## Answer these

Straight from the manual. Unchecked means you can't yet answer it out loud, without notes.

- [ ] Threat modeling: what are you protecting, from whom, and what's the attack surface?
- [ ] AuthN vs AuthZ — and why is authorization the one that actually gets breached?
- [ ] The OWASP Top 10 — for each, the mechanism and the mitigation.
- [ ] Why do parameterized queries work? (Not 'they escape input' — the real reason.)
- [ ] How do secrets get into and out of a system safely?
- [ ] Supply chain: what is your actual dependency tree, and who can push to it?

## Build to learn

- [[Attack a vulnerable app]] — Set up OWASP Juice Shop and exploit it yourself. Attacking teaches defense faster than reading does.

> Set up a deliberately vulnerable app (OWASP Juice Shop) and exploit it yourself. Attacking teaches defense faster than reading does.

## Canonical sources

- [[OWASP Top 10 and Cheat Sheet Series]]
- [[Threat Modeling]]

## Blocks

- [[Block 21-22 — Security]]
