# Breakpoint guard

`guard_own_words.py` enforces Rule 1 from [ADR 0001](../../docs/adr/0001-breakpoint.md): Claude never writes the learner's sections. A rule in `CLAUDE.md` is a request; this hook is the guarantee.

## What it protects

| Note `type` | Sections |
|---|---|
| `concept` | the *Predict the failure* callout, *What it is*, *How it breaks*, *In my own words* |
| `build` | *Plan*, *The failure I'm going to cause on purpose*, *What actually happened*, *What I got wrong* |

Before every `Edit`, `MultiEdit` and `Write`, the hook applies the change to a copy of the note and compares those sections before and after, every copy of each heading. Any difference blocks the call, including deleting a heading or changing the note's `type`, and Claude is told to explain in chat or offer `/critique` instead. A new note, or a file that becomes one, may be written only with those sections empty. The check goes by what the file contains, not its name, so a `.MD` path, a symlink or a `.txt` draft gets the same check.

Frontmatter (`status`, tags), every other section and every other file pass through. If the hook itself crashes, it blocks: a broken guard must not wave edits through.

**Shell commands:** `guard_shell.py` runs before and after every Bash call. It snapshots the notes in `01-`–`04-` and `06-builds/` first, and afterwards puts back any note whose protected sections or `type` changed. A deleted note is restored, and a new note with filled sections is removed. The version the command left is saved to `_tutor/guard/` first, so nothing is lost if you were typing in Obsidian at the same time.

## Running the tests

```bash
python3 .claude/hooks/test_guard_own_words.py
python3 .claude/hooks/test_guard_shell.py
```

Standard library only. The fixtures are copies of a real concept note and a real build note. The attacks behind these tests are in [docs/evals/redteam.md](../../docs/evals/redteam.md).

## What it can't catch

The hooks see Claude Code's file tools and Bash, nothing else.

- **Writes after a command returns.** The shell guard compares when the Bash call ends. A process left running in the background (`nohup … &`) that writes later, or a write by an MCP server, isn't caught. Rule 1 in `CLAUDE.md` covers those. `.claude/settings.json` also denies the common in-place editors (`sed -i`, `perl -i`, `awk -i`, `tee`, `truncate`, `dd`), so Claude reaches for its Edit tool instead.
- **Notes outside the note folders.** The shell guard watches `01-`–`04-` and `06-builds/`. A concept note somewhere else is protected from the file tools only.
- **Untrusted folder.** Claude Code runs project hooks only after you choose *Yes, I trust this folder* the first time you open it. Answer no and only Rule 1 protects your notes.
- **Other assistants.** Cursor, Copilot and others don't read `.claude/`. They get no protection at all.
- **You.** Nothing stops you pasting a model's answer into *In my own words* yourself. That's what `/probe` is for.
- **Renamed headings.** The hook finds sections by their exact heading text from the [Note contract](../../00-meta/Note%20contract.md). Rename a heading and that section is no longer protected; the rename itself is blocked, so only you can do it.
