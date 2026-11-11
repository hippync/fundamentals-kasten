# Breakpoint guard

`guard_own_words.py` enforces Rule 1 from [ADR 0001](../../docs/adr/0001-breakpoint.md): Claude never writes the learner's sections. A rule in `CLAUDE.md` is a request; this hook is the guarantee.

## What it protects

| Note `type` | Sections |
|---|---|
| `concept` | the *Predict the failure* callout, *What it is*, *How it breaks*, *In my own words* |
| `build` | *Plan*, *The failure I'm going to cause on purpose*, *What actually happened*, *What I got wrong* |

Before every `Edit`, `MultiEdit` and `Write`, the hook applies the change to a copy of the note and compares those sections before and after. Any difference, including deleting a heading, blocks the call, and Claude is told to explain in chat or offer `/critique` instead. A new note may be written only with those sections empty.

Frontmatter (`status`, tags), every other section and every other file pass through. If the hook itself crashes, it blocks: a broken guard must not wave edits through.

## Running the tests

```bash
python3 .claude/hooks/test_guard_own_words.py
```

Standard library only. The fixtures are copies of a real concept note and a real build note.

## What it can't catch

The hook sees Claude Code's file tools, nothing else.

- **Shell writes.** `.claude/settings.json` denies the common in-place editors (`sed -i`, `perl -i`, `awk -i`, `tee`, `truncate`, `dd`). Permission rules match a command's start, not its target, so these are denied everywhere in the repo, not only in note folders. Claude uses its Edit tool instead, which the hook checks. A redirect (`echo … > note.md`), a Python one-liner or a script Claude writes and runs can still get through. Rule 1 in `CLAUDE.md` covers those.
- **Untrusted folder.** Claude Code runs project hooks only after you choose *Yes, I trust this folder* the first time you open it. Answer no and only Rule 1 protects your notes.
- **Other assistants.** Cursor, Copilot and others don't read `.claude/`. They get no protection at all.
- **You.** Nothing stops you pasting a model's answer into *In my own words* yourself. That's what `/probe` is for.
- **Renamed headings.** The hook finds sections by their exact heading text from the [Note contract](../../00-meta/Note%20contract.md). Rename a heading and that section is no longer protected; the rename itself is blocked, so only you can do it.
