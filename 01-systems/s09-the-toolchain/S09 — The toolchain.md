---
id: "t-s09"
title: "S09 — The toolchain"
type: "theme"
theme:
  - "S09"
ladder: "Systems ladder"
tags:
  - "theme"
  - "systems"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# S09 — The toolchain

*Theme · Systems ladder · The Fundamentals Reset (Field Manual, Edition 2026)*

**The toolchain — how code becomes a running artifact**

## Why now

There's a gap between 'the code is written' and 'the thing is running,' and most developers treat it as magic. It isn't, and the abstractions leak constantly. This is also the layer where AI assistance is weakest, because it depends entirely on your environment.

## Concepts on this rung

- [[The Unix philosophy]]
- [[Shell composition]]
- [[Git objects and the commit DAG]]
- [[Rebase vs merge]]
- [[git bisect]]
- [[Containers]]
- [[The path from push to production]]

## Answer these

Straight from the manual. Unchecked means you can't yet answer it out loud, without notes.

- [ ] The Unix philosophy: small composable tools, text streams, pipes. Why has this design survived fifty years?
- [ ] Enough shell to be dangerous: pipes, redirection, `grep` / `sed` / `awk` / `find` / `xargs`. Not memorized — composable.
- [ ] Git: what is a commit? (A content-addressed snapshot in a directed acyclic graph. Once you see that, rebase vs merge stops being scary.)
- [ ] `git bisect` — do you know it exists? It finds the breaking commit in log(n) steps and most people have never run it.
- [ ] What is a container, actually? (Namespaces + cgroups + a filesystem layer. Not a VM.)
- [ ] What happens between `git push` and running code in production? Every step.

## Build to learn

- [[Bisect and build from scratch]] — Break a repo deliberately five commits back, then find it with `git bisect`. Build a container from a scratch base image and understand every layer you added.

> Break a repo deliberately five commits back, then find it with `git bisect`. Build a container from a scratch base image and understand every layer you added.

## Canonical sources

- [[The Pragmatic Programmer]]
- [[Pro Git]]
- [[Missing Semester of Your CS Education]]

## Blocks

- [[Block 03-04 — The toolchain & shell]]
