---
id: "note-contract"
title: "Note contract"
type: "meta"
tags:
  - "meta"
  - "rag"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# Note contract

The rules every note in this vault follows. They exist so the vault is navigable by a human **and** chunkable by a retrieval pipeline without a custom parser.

## Frontmatter schema

```yaml
id:          stable slug, never changes, safe as a vector-store primary key
title:       human title (matches filename)
type:        concept | theme | principle | source | build | block | decision | index | meta
status:      stub | drafted | explained | tested        (concept notes only)
theme:       list of theme ids, e.g. ["S05", "A5"]
theme-name:  list of readable theme names
ladder:      Systems ladder | AI ladder | Running practices
half-life:   which row of the half-life table this sits in
tags:        lowercase, hyphenated, no spaces
source-doc:  always "The Fundamentals Reset (Field Manual, Edition 2026)"
updated:     ISO date
```

## Heading contract

Every concept note uses the same H2 set, in the same order:

1. `## Predict the failure` — the test from Part 0. Not "can I use it" but "can I predict its failure mode."
2. `## What it is`
3. `## Why it matters now`
4. `## How it breaks`
5. `## Questions I should be able to answer`
6. `## In my own words` — **the only section that counts**
7. `## Where I'd look`
8. `## Related`

Do not rename, reorder, or drop headings. Add content under them.

## Why this matters for retrieval

Chunk on H2 boundaries and every chunk is self-contained: it carries its own heading, and the line directly under the H1 repeats the note's type and theme so a chunk stripped of frontmatter still knows what it is.

Rules that keep it that way:

- **One idea per note.** If a note needs two *Predict the failure* lines, it's two notes.
- **No orphan pronouns across headings.** A section that starts with "This is why…" breaks when chunked.
- **Links carry meaning.** `[[Idempotency]]` in a sentence, not a bare list of links at the bottom of a paragraph.
- **Never edit the generated scaffolding to remove a heading you haven't filled in.** An empty section is honest signal; a missing one is a parser break.

## Tag taxonomy

Themes are frontmatter, not tags. Tags describe cross-cutting properties only:

`#concept` `#principle` `#source` `#build` `#decision` — note type
`#unsourced` — a claim you couldn't trace within two clicks ([[The two-click rule]])
`#contradicts-manual` — you found evidence the manual is wrong. Keep it. That's the most valuable note in the vault.
`#reread` — you thought you understood it and later found you didn't

## Filenames

Windows-safe: no `: / \ | ? * < > "`. Colons in the manual's titles become em dashes. Filenames are the link targets — renaming a note breaks links unless Obsidian's "automatically update internal links" is on. Turn it on.
