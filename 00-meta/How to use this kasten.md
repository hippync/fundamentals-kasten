---
id: "how-to-use"
title: "How to use this vault"
type: "meta"
tags:
  - "meta"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# How to use this vault

## What this is

A retrieval map, not a textbook. The manual's second principle:

> You don't need to hold B-tree internals in your head. You need to (a) know that index behavior is *a thing that exists and explains problems*, and (b) know the one canonical source you'd open to get precise.

Every concept note is a pin on that map. The scaffolding — what the thing is, which theme it belongs to, which questions it answers, which source to open — is already filled in. **The scaffolding is not knowledge.**

## The one rule

Every concept note has an empty section called **In my own words**. That section is the only part of this vault that has any value, and only you can write it.

> If you can't explain it in a paragraph without the source open, you don't have it yet. Notes you write are worth ten times notes you copy.

A note cannot advance past `status: drafted` until that section is written with the book closed.

## The status ladder

| Status | Means |
|---|---|
| `stub` | Generated scaffolding. You haven't touched it. |
| `drafted` | You've read a source and filled in the body. |
| `explained` | You wrote *In my own words* from a closed book. |
| `tested` | You predicted a failure mode and then caused it, or built something that depends on it. |

`tested` is the real bar. `explained` is the minimum for calling it known.

## The weekly loop

1. **Pick the block.** Open the current note in `06 Blocks`. Two systems concepts, one AI concept.
2. **Read one source.** Tier 1 or tier 2 only — see [[The source hierarchy]].
3. **Build the thing.** The block's deliverable, from `05 Builds`. Reading produces recognition; building produces knowledge.
4. **Break it on purpose.** Fill in *Predict the failure* and then verify the prediction.
5. **Write it in your own words.** Close the book first.
6. **Write the ADR.** One page: context, options, decision, consequences. Goes in `07 Decisions`.

## Using AI against this vault

Use it as a tutor, not an oracle. Paste a note's *In my own words* section and ask *"where is this wrong?"* — do not ask it to write that section. See [[Use AI as a tutor, not an oracle]].

The vault is also structured to be pointed at directly as a RAG corpus for your own study tooling — see [[Note contract]] for the chunking guarantees.

## Templates

Copy these by hand, or point Obsidian's core Templates plugin at `00 Meta/Templates`.

- [[Template — Concept]] · [[Template — Source]] · [[Template — Build]] · [[Template — ADR]] · [[Template — Weekly review]]

## Optional plugins

The vault is plain markdown and works with zero plugins. If you want more:

- **Dataview** — the queries in [[Status board]] are already written, commented out. Uncomment them.
- **Spaced Repetition** — [[Questions — index]] is formatted so questions can be turned into cards.
- **Graph view** (core) — filter by tag to see one theme's cluster at a time.

Do not install anything until the vault has annoyed you in a specific way. Tools are the top row of the half-life table.
