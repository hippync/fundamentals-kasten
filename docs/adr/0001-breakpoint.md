# ADR 0001: Breakpoint, an examiner layer for the kasten

*Status: accepted · Date: 2026-11-10 · Epic: [#4](https://github.com/hippync/fundamentals-kasten/issues/4)*

This is a decision about **this repository**, not one of the kasten's notes. The kasten's own `08-decisions/` belongs to whoever forks it, and its ADR-0001 stays blank.

## Context

The kasten works because the learner writes the hard parts: *Predict the failure*, the body and *In my own words* in every concept note, and the plan, the deliberate failure and the post-mortem in every build note. A notebook full of correct paragraphs you didn't write gives recognition, not knowledge ([Kasten design](../../00-meta/Kasten%20design.md)).

An AI assistant pointed at the kasten is pulled the other way. Asked for help, it writes the answer. [Use AI as a tutor, not an oracle](../../00-meta/principles/Use%20AI%20as%20a%20tutor%2C%20not%20an%20oracle.md) says what to do instead, but a principle the learner has to remember every session doesn't stop that.

Breakpoint is meant to make the tutor stance the default: Claude finds where the learner's understanding breaks, critiques what they wrote, schedules re-probes and coaches builds. It never writes the learner's sections.

## Options considered

| Option | Buys | Costs |
|---|---|---|
| **Claude Code layer** (`CLAUDE.md` + `.claude/`) | Lives in the repo as plain files. Hooks can enforce rules, not just request them. Delete two paths and it's gone. | Requires Claude Code. Terminal first. |
| Prompt only (a `CLAUDE.md` asking nicely) | Smallest possible change | One "just write it for me" undoes it. Nothing is enforced. |
| Obsidian community plugin | Lives where the learner reads | Plugins are the top row of the half-life table, and the kasten promises to work with none. Ties the kasten to one editor. |
| Web app with closed-book mode | Can actually hide the notes during a probe | A server, accounts and hosting, before the idea is proven. |
| Retrieval over the learner's notes | Answers in the learner's own words | Only useful once *In my own words* is filled in. Needs an index and an embedding pipeline. |

## Decision

Breakpoint is an optional Claude Code layer that examines the learner and never authors their understanding. Its write access is limited by a hook, not by the prompt alone.

1. **Optional.** Breakpoint is `CLAUDE.md` plus `.claude/` and nothing else the kasten depends on. Without them the kasten works exactly as before: plain markdown, Obsidian optional, nothing to install.
2. **The learner's sections are off limits.** In a concept note Claude never writes *Predict the failure*, *What it is*, *How it breaks* or *In my own words*. These are the sections `reset.py` clears, so they're the learner's by the kasten's own definition. In a build note it never writes *Plan*, *The failure I'm going to cause on purpose*, *What actually happened* or *What I got wrong*. A `PreToolUse` hook rejects any edit that touches them ([#12](https://github.com/hippync/fundamentals-kasten/issues/12)), so the rule holds even when the prompt is talked out of it.
3. **Frontmatter changes go through rules.** Claude may change `status` and tags, and only along the transition rules ([#9](https://github.com/hippync/fundamentals-kasten/issues/9)). For example, a note reaches 🌳 `explained` only after a closed-book probe the learner passes, never because Claude judged the prose good.
4. **Tutor state lives in `_tutor/`**, keyed by each concept's frontmatter `id`. Ids never change ([Note contract](../../00-meta/Note%20contract.md)), so renaming a note doesn't orphan its history. Notes stay free of tutor bookkeeping.
5. **Skill names:**

   | Skill | Does |
   |---|---|
   | `/next` | Picks what to work on next from the current block and due re-probes |
   | `/probe` | Asks closed-book questions until the learner's understanding breaks |
   | `/critique` | Critiques what the learner wrote, without rewriting it |
   | `/revisit` | Re-probes concepts that are due |
   | `/drill` | Quick-fire questions across a theme |
   | `/build-coach` | Coaches a build without doing it |

   Names that read as Claude Code built-ins, such as `/review`, are avoided.
6. **English by default.** The learner can set another session language. Notes are written in whatever language the learner chooses.

## Consequences

- **Easier:** the tutor stance is the default and doesn't depend on willpower. Removing Breakpoint is one deleted folder and one deleted file. Tutor history survives renames.
- **Harder:** Breakpoint is only as strong as the hook. A section-matching bug is a hole, which is why the guard rail gets its own red-team issue ([#25](https://github.com/hippync/fundamentals-kasten/issues/25)). Learners on other assistants get only the principle, not the enforcement.
- **Accepted risk:** a learner can still paste a model's answer into *In my own words* by hand. Breakpoint stops Claude writing it, not the learner copying it. `/probe` is what catches it.
- `graph.py` and `reset.py` must ignore Breakpoint's files ([#10](https://github.com/hippync/fundamentals-kasten/issues/10)) so the graph and a reset stay about the notes.

**Rejected for v1:**

- **Web app:** later ([#28](https://github.com/hippync/fundamentals-kasten/issues/28)). Worth building only once the examiner loop is shown to work in the terminal.
- **Obsidian community plugin:** top row of the half-life table. The kasten's "no plugins" rule applies to its own tooling too.
- **Retrieval over notes:** later ([#29](https://github.com/hippync/fundamentals-kasten/issues/29)). It has nothing to retrieve until the learner has written their own words.

## Revisit when

- The guard rail is bypassed in red-teaming or in real use.
- Dogfooding one block ([#26](https://github.com/hippync/fundamentals-kasten/issues/26)) shows the skills overlap or a different split works better.
- Claude Code's hook or skill model changes in a way that breaks the enforcement.
