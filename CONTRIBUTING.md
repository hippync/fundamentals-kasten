# Contributing

Read this first, because this repo takes contributions in a narrower range than most.

## Why the range is narrow

A Zettelkasten is constitutionally not collaborative. The entire argument behind it — see
[00-meta/Methodology.md](00-meta/Methodology.md) — is that the value lives in *your*
reformulation of an idea, produced by the effort of writing it. A pull request containing a
filled-in **In my own words** section is therefore a category error: it would be your
understanding, delivered to someone else as a finished object, which is precisely the thing
this repo is built to prevent.

So content PRs that fill in notes will be declined. Not because they're bad — because merging
them would make the repo worse at its only job.

Fork it and fill in your own. That's the intended use, and the **Use this template** button is
right at the top.

## What is genuinely useful

**Scaffolding errors.** A concept filed on the wrong rung, a broken wikilink, a note whose
`Related` links point somewhere that doesn't make sense, a frontmatter field that doesn't
match [00-meta/Note contract.md](00-meta/Note%20contract.md). These are real bugs and I want
them.

**Better sources — with chapter numbers.** "Read OSTEP" is useless advice. "OSTEP ch. 6,
*Limited Direct Execution*" is a pointer someone can act on tonight. If a note points at a
weaker source than it could, say which chapter of which better one, and why. Free and primary
sources are strongly preferred; see the source hierarchy in `00-meta/principles/`.

**A missing concept or a thin rung.** A8 currently has one concept and is arguably not a rung
at all. If you think something is missing from a ladder, open an issue with the concept title,
the rung, the failure it explains, and the source you'd point at — not a written note.

**Builds.** A better build-to-learn exercise for a rung: the thing to make, the failure to
cause on purpose, and how you'd know it worked. Concrete commands beat descriptions.

**Translations and tooling.** Both welcome. Keep tooling optional — the repo has to keep
working with zero plugins and zero scripts.

## Proposing a change to a Breakpoint skill

Breakpoint's skills (`.claude/skills/`) and agents (`.claude/agents/`) are prompts, and a
prompt change that reads better can measure worse. That's the build *A 30-case eval set*,
applied to this repo. So a skill PR needs evidence, not just a diff:

- **Eval results, before and after.** Run the eval set in `docs/evals/` on `master` and on
  your branch, with the same model, and paste both into the PR. A change to `/probe` or
  `/critique` has to keep their bar: at least 80% of seeded holes caught, at most one false
  alarm on correct explanations, zero rewritten paragraphs.
- **Rule 1 holds.** No skill may write the learner's sections, and none may change a note
  beyond `status` (along the transitions in `_tutor/README.md`) and a drill checkbox.
  Changes to the guard hook also need `python3 .claude/hooks/test_guard_own_words.py`
  passing, plus a red-team case for whatever the change touches.
- **Deterministic parts stay in code.** If the change touches ordering, scheduling or the
  ledger, it goes in `.claude/tutor/tutor.py` with a test in `test_tutor.py`, not in a
  prompt.
- **New skills start as an issue.** Say which step of the weekly loop it serves and
  why an existing skill can't.

## House rules if you do open a PR

- One idea per note, one concern per PR.
- Don't rename files casually — filenames are wikilink targets, and a rename breaks every link
  pointing at it unless you fix them all in the same commit.
- Don't fill in a section that ships empty. If you're unsure whether a section is empty on
  purpose, it is.
- Keep the concept skeleton intact, in order: the *Predict the failure* callout and the seven H2s. An empty section is honest signal; a
  missing one breaks the chunking guarantees in the note contract.
- No plugin dependencies. Dataview queries stay commented out.
- Don't regenerate the graph. `docs/graph-*.svg` are built from your links by
  `scripts/graph.py`, and two people regenerating independently produce two unmergeable
  1,300-line diffs of shifted coordinates. Change the notes and leave the SVGs alone; the
  graph is redrawn on `master` once your PR lands.

## Issues are cheap

If you're not sure whether something is a bug or the design, open an issue and ask. That's
lower-friction for both of us than a PR that has to be closed.
