---
id: "t-s03"
title: "S03 — Networking"
type: "theme"
theme:
  - "S03"
ladder: "Systems ladder"
tags:
  - "theme"
  - "systems"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# S03 — Networking

*Theme · Systems ladder · The Fundamentals Reset (Field Manual, Edition 2026)*

**Networking**

## Why now

Everything you build is distributed now, even the 'simple' apps. Latency is the tax you can't refactor away, and most people don't know what they're being charged.

## Concepts on this rung

- [[URL to first byte]]
- [[TCP handshake]]
- [[TLS handshake]]
- [[Latency vs bandwidth]]
- [[HTTP versions]]
- [[Connection pooling]]
- [[DNS]]

## Answer these

Straight from the manual. Unchecked means you can't yet answer it out loud, without notes.

- [ ] What actually happens between typing a URL and the first byte arriving? Every step.
- [ ] TCP handshake, TLS handshake — how many round trips before any data moves?
- [ ] Latency vs bandwidth: which one do you fix by upgrading the connection? (Trick question.)
- [ ] HTTP/1.1 vs 2 vs 3 — what problem did each one solve?
- [ ] What is connection pooling actually pooling, and what breaks without it?
- [ ] Why is DNS the answer to so many outages?

## Build to learn

- [[Raw-socket HTTP server]] — Implement a minimal HTTP server on raw sockets. No framework. It's a weekend and it removes all the magic.

> Implement a minimal HTTP server on raw sockets. No framework. It's a weekend and it removes all the magic.

## Canonical sources

- [[High Performance Browser Networking]]
- [[Beej's Guide to Network Programming]]

## Blocks

- [[Block 07-08 — Networking]]
