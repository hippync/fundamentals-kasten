# `_tutor/`: Breakpoint's workspace

Everything Breakpoint remembers about your sessions lives here and nowhere else. Your notes stay yours: Breakpoint never adds its bookkeeping to them, and the only thing it may change in a note is `status` and tags, by the transition rules. See [ADR 0001](../docs/adr/0001-breakpoint.md).

You don't need this folder unless you use Breakpoint. Without Claude Code it stays empty and the kasten works exactly the same.

## What lives here

```
_tutor/
├── progress.md     where you are: current block, start date, languages
├── ledger/         one file per concept you've been probed on: its box and when it's next due
├── logs/           one file per session: what was probed and how it went
├── viz/            diagrams drawn for you during sessions
└── templates/      a starting progress.md, plus an example ledger file and log
```

`progress.md` doesn't exist in a fresh copy. The first session creates it from [`templates/progress.md`](templates/progress.md), or you can copy that file here yourself.

## Formats

Every Breakpoint skill reads and writes these files, so these formats are the contract between them. Ids are always frontmatter `id`s (`c-…` for concepts, `blk-…` for blocks), never filenames. Dates are `YYYY-MM-DD`.

### Ledger: `ledger/<concept-id>.md`

One file per concept you've been probed on, frontmatter only. Separate files rather than one big table, so [Obsidian Bases](https://help.obsidian.md/bases) can query them and git diffs stay one line per probe. Example: [`templates/ledger.md`](templates/ledger.md).

```yaml
concept: c-error-compounding-in-loops   # the concept's frontmatter id; matches the filename
box: 1                                  # 1–5, how well it's holding
last-result: fail                       # pass | partial | fail | dont-know
last-probed: 2026-11-10
next-due: 2026-11-11                    # last-probed + the new box's interval
```

**Boxes.** A concept's first probe creates its file in box 1, then applies the result:

| Result | New box |
|---|---|
| `pass` | one up, at most 5 |
| `partial` | unchanged |
| `fail` or `dont-know` | back to 1 |

| Box | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Next due after | 1 day | 3 days | 7 days | 14 days | 30 days |

A pass in box 5 stays in box 5 and comes back in 30 days.

### Session log: `logs/<date>-<skill>.md`

One file per session, for example `logs/2026-11-10-probe.md`. A second session of the same skill that day gets `-2`. Example: [`templates/log.md`](templates/log.md).

```yaml
date: 2026-11-10
skill: probe                  # next | probe | critique | revisit | drill | build-coach
block: blk-01-02              # the block you were in
concepts:                     # ids of the concepts the session touched
  - c-error-compounding-in-loops
result: fail                  # the worst result across concepts, or none if nothing was probed
minutes: 20
```

The body is a short record in plain prose: what was asked, where your understanding broke, what to reread. It may link notes with `[[wikilinks]]`. Breakpoint's skills are what write it; it is not one of your notes.

### Status transitions

Breakpoint may change a concept note's `status` only along these steps. Claude proposes the change and says why; nothing is written until you confirm.

| From → to | Requires |
|---|---|
| `stub` → `drafted` | You filled in the body sections |
| `drafted` → `explained` | You wrote *In my own words* with the book closed (you confirm), and `/critique` found no blocking hole |
| `explained` → `tested` | A build in the concept's notes has *What actually happened* and *What I got wrong* filled in |
| any → one step back, plus `#reread` | You failed a `/revisit` on it |

No other transition exists. In particular, Breakpoint never skips a step, and never moves a note forward because it judged your prose good.

## Why it's separate from the notes

- **Your notes stay readable.** A concept note holds your understanding, not a probe history.
- **Renames don't lose history.** Ledger entries are keyed by the concept's frontmatter `id`, which never changes, not by its filename.
- **One folder to delete.** Removing Breakpoint means deleting `_tutor/`, `.claude/` and `CLAUDE.md`. No note needs cleaning up.

## Is it in git?

Not by default. `.gitignore` keeps everything here out of git except this README, the `templates/` and the `.gitkeep` files that hold the empty folders. Running a session leaves `git status` clean, so a public fork never publishes your session history by accident.

If your fork is private and you want your history versioned, delete the `_tutor/` lines in `.gitignore`.
