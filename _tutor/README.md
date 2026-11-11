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
└── templates/      starting copies, e.g. progress.md
```

`progress.md` doesn't exist in a fresh copy. The first session creates it from [`templates/progress.md`](templates/progress.md), or you can copy that file here yourself.

## Why it's separate from the notes

- **Your notes stay readable.** A concept note holds your understanding, not a probe history.
- **Renames don't lose history.** Ledger entries are keyed by the concept's frontmatter `id`, which never changes, not by its filename.
- **One folder to delete.** Removing Breakpoint means deleting `_tutor/`, `.claude/` and `CLAUDE.md`. No note needs cleaning up.

## Is it in git?

Not by default. `.gitignore` keeps everything here out of git except this README, the `templates/` and the `.gitkeep` files that hold the empty folders. Running a session leaves `git status` clean, so a public fork never publishes your session history by accident.

If your fork is private and you want your history versioned, delete the `_tutor/` lines in `.gitignore`.
