---
id: "noise-filter"
title: "The noise filter"
type: "meta"
tags:
  - "meta"
  - "strategy"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# The noise filter

*Meta · a decision procedure for what deserves your evening.*

The constraint is not motivation. It is that there are perhaps six good hours in a week and an
effectively infinite supply of things that look worth learning. Most of the anxiety in this
industry is the gap between those two facts.

## The filter

Before spending time on something, place it in the table:

| Knowledge type | Half-life | Example |
|---|---|---|
| Framework / library API | ~3 years | The current React data-fetching pattern |
| Language | ~10 years | Go, C#, Python |
| Systems concept | ~40 years | Cache locality, ACID, TCP, coupling |
| Reasoning skill | Career-length | Decomposition, failure analysis, tradeoff judgment |

**Row one: cap it.** Learn it when a task requires it, at the depth the task requires, and let
it go. This is also the row a model handles well, which is not a coincidence — it is documented,
patterned, and requires no judgment.

**Row two: one, deep.** See [[One language deep, the rest as literacy]].

**Rows three and four: this is the investment.** Time here compounds, transfers between jobs and
stacks, and is what you are actually being paid for at any level above junior.

## Three signals that something is row one wearing a disguise

1. **It has a version number in its name.** Concepts do not have release notes.
2. **The tutorial is a walkthrough of an interface.** If the material is mostly "click here,
   then set this option," you are learning a product, not an idea.
3. **It would be obsolete if one company changed its mind.** That is a dependency, not knowledge.

## The inverse test, which matters more

Some row-one things are worth real time because of what sits underneath them. The question is
not "how long will this tool last" but **"what does learning it force me to understand?"**

Writing a Dockerfile is row one. Understanding namespaces, cgroups and layered filesystems
because Docker made you curious is row three. Same evening, different outcome, and the
difference is entirely in whether you followed the abstraction down.

So the filter is not a ban on new tools. It is a rule about where you stop: use the tool, and
when it surprises you, go down one layer rather than sideways to another tool.

## When you are already behind

The honest answer to "there is too much and I am behind" is that you are behind on row one and
will always be, permanently, along with everyone else including the people who look like they
aren't. Nobody is behind on row three, because row three barely moves. Cache locality has not
had a breaking change since you were born.

That is the whole reason to invest where the half-life is long: it is the only place where the
effort accumulates instead of evaporating.

## Related

- [[Invest by half-life]] — the principle
- [[Judgment is the scarce good]]
- [[The source hierarchy]] — where to read once you have decided what to read
- [[The two-click rule]]
- [[Build a retrieval map, not a memory]]
