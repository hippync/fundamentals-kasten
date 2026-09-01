---
id: "methodology"
title: "Methodology"
type: "meta"
tags:
  - "meta"
  - "zettelkasten"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# Methodology

*Meta · why this is shaped like a Zettelkasten, and where it deliberately isn't one.*

## The problem with reading

You read a chapter on B-trees. You follow every paragraph. You close the book feeling like you
understand B-trees. Three weeks later a query is slow and it does not occur to you that the
index might be the reason.

Nothing went wrong in your reading. The problem is that following an argument and being able
to *use* it are different capabilities, and reading only trains the first one. Sönke Ahrens'
*How to Take Smart Notes* is the best account of why: understanding is produced by the effort
of restating something in your own words against the resistance of everything else you know,
and highlighting a passage skips exactly that effort.

## The three kinds of note

Ahrens' distinction, applied here:

**Fleeting notes** are whatever you scribble mid-reading. They are allowed to be messy, wrong
and abbreviated, and they are meant to be discarded within a day or two. They are not in this
repository — they belong in a scratch file or a paper notebook.

**Literature notes** record what a specific source claimed, in your own words, with a pointer
you could return to. One per source, in `05-sources/`, in the *Claims I want to keep* section.
The rule that makes them useful is that you write them with the book closed enough that you
cannot transcribe.

**Permanent notes** are the point. One idea per note, written as if for a stranger, connected
by explicit links to the notes it bears on. The 130 concept notes are permanent-note slots
waiting to be filled — the title, the rung, the question and the sources are given; the
reformulation is not.

A permanent note is finished when someone else could read it cold and get the idea. If it needs
you standing next to it explaining, it is still a fleeting note wearing better formatting.

## Where this deviates from Ahrens, and why

**1. The corpus is fixed in advance.** A classical Zettelkasten grows from whatever you happen
to read; you cannot know its shape ahead of time, which is why Luhmann needed branching IDs and
an index. This kasten has a known 130-concept inventory drawn from a specific curriculum. That
makes the ID scheme pure ceremony, so there isn't one — notes are titled in plain language and
linked by name.

**2. Notes are linked before they are written.** Ahrens links notes after writing them, because
the connection is a discovery. Here the link graph ships pre-built, which is a real cost: you
lose the discovery. You gain a map you can navigate before you know anything, which for a
curriculum matters more. Add your own links as you go — those are the ones that mean something,
and they are the reason `## Related` is a section rather than a fixed field.

**3. The test is prediction, not restatement.** Ahrens asks whether the note makes sense on its
own. This adds a harder gate: *what breaks when this is absent, wrong or misunderstood?* A
definition can be memorised without understanding; a failure mode largely cannot. This is why
every note opens with **Predict the failure** rather than with a definition.

**4. There is a fourth status above "written".** `tested` — you predicted a failure and then
caused it. No note-taking method has an equivalent, because no note-taking method is about
systems. For software this is the only status that reliably distinguishes understanding from
articulate confidence.

## Why the notes ship empty

This is the design decision everything else follows from.

A scaffold you fill in yourself and a completed reference look almost identical from the
outside and function as opposites. The completed reference is faster, more accurate, better
written, and produces nothing durable, because the effort that produces understanding is
precisely the effort it saves you.

So the scaffolding here is deliberately partial:

- **Given:** the note's title, its rung, why the rung matters, the question it answers, which
  source to open, and what it links to. All of this is *retrieval infrastructure* — knowing
  that index behaviour is a thing that exists and explains problems, and knowing the one book
  you would open to get precise.
- **Withheld:** what it is, how it breaks, and your paragraph. All of this is *understanding*,
  and it cannot be transferred, only built.

An empty section is honest signal. A section filled in by someone else is a lie with a
convincing surface.

## Using a language model against this kasten

Use it as a tutor, not an oracle. The productive prompt is:

> "Here is my paragraph on backpressure. Where is it wrong?"

The prompt that quietly destroys the exercise is *"write the backpressure note."* You will get
something better than your first attempt, and you will have learned nothing, and you will not
be able to tell the difference for several months.

Two uses that are unambiguously good: having a model quiz you from `00-meta/indexes/Questions
— index.md` with instructions not to give answers, and asking it to attack a paragraph you
already wrote. Both put the work on your side of the table.

## Related

- [[How to use this kasten]] — the weekly loop
- [[Note contract]] — the format every note follows
- [[Kasten design]] — the structural decisions and what was left out
- [[The noise filter]] — what deserves an evening
- [[Write it down in your own words]] · [[Use AI as a tutor, not an oracle]]
