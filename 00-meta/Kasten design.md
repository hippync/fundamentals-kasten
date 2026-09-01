---
id: "vault-design"
title: "Vault design"
type: "meta"
tags:
  - "meta"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# Vault design

Why this vault is shaped the way it is. Read once; you shouldn't need it again.

## The design constraint

The manual is a 24-page linear document. A linear document is the wrong shape for the thing it describes, because its own second principle says fundamentals are **a map of where the important problems live** — and a map has to be traversable from any point, not just from page one.

So the vault is not a copy of the document. It's the document decomposed into the smallest units that can be linked, and then re-linked along the connections the document only gestures at.

## The four decompositions

**Principles became rules, not notes.** The fifteen items in `01 Principles` are the only notes that arrive finished. They aren't things to learn; they're the constitution the rest of the vault runs under. When you're unsure whether to spend an evening on something, that folder answers it.

**Themes became maps of contents, not content.** A theme note holds no explanation. It holds: why this rung matters now, which concepts hang off it, the manual's verbatim questions as a checklist, the build, and the sources. It's a hub — deliberately thin, so the graph view shows structure rather than mush.

**Questions became the assessment layer.** The manual's "answer these" lists are the only objective measure it provides. They live in two places on purpose: on the theme note (as a per-rung checklist you tick when you can answer out loud) and inside the concept note they belong to (so the question is next to the material). Duplication is intentional — one is a drill, the other is context.

**Concepts became the atom.** 130 of them, one idea each, every one with the same eight headings. That uniformity is what makes the vault machine-readable later.

## What was deliberately left out

**No summaries of the manual's arguments in the concept bodies.** The scaffolding is filled in; the substance is not. This is the whole design. A vault pre-filled with correct-sounding explanations you didn't write is exactly the failure mode the manual warns about — recognition masquerading as knowledge. The empty `## In my own words` section is the product.

**No plugins.** Everything is plain markdown, wikilinks, YAML frontmatter, and checkboxes. Dataview queries exist in [[Status board]] but are commented out. Plugins are the top row of the half-life table; the vault has to work without them or it isn't durable.

**No daily notes, no PARA, no Zettelkasten IDs.** Those are organizing systems for capturing an unpredictable stream of input. This vault has a fixed, known corpus and a 28-week schedule. Adding a second organizing system on top would be pure ceremony — the [[Scrum]] failure mode applied to note-taking.

**No spaced-repetition cards.** [[Questions — index]] is formatted so you *can* generate them, but the manual's position is that recall isn't the bottleneck — prediction is. A flashcard asks "what is idempotency." The vault asks "what breaks without it." Only the second one is the test.

## Why it's shaped for retrieval too

You said this should work as a corpus you can query. Three properties make that work, and all three are enforced by [[Note contract]]:

1. **Stable ids.** Every note has an `id` in frontmatter that never changes even if you rename the file. That's your primary key in any vector store.
2. **Semantic chunk boundaries.** Chunking on `##` headings yields self-contained chunks, because no section depends on the one before it for its subject. See [[Chunking strategy]] — the vault is itself an example of the thing that theme is about.
3. **Context repetition under the H1.** Every note repeats its type, ladder, and theme in a plain-text line directly under the title, so a chunk that loses its frontmatter still carries its own metadata.

The useful consequence: once you've written the `In my own words` sections, a retrieval system over this vault answers in *your* explanations rather than a book's. That's a materially different tool than asking a model the same question cold — and it's a working demonstration of [[Grounding]].

## The failure mode of this vault

Filling it in feels like progress. It isn't, on its own. 130 notes at `explained` and zero builds at `tested` means you've written a very tidy book report.

The counterweight is [[Status board]]: the metric is not notes written, it's how many concepts you can predict the failure mode for, out loud, right now.
