#!/usr/bin/env python3
"""Breakpoint shell guard: undo shell writes to the learner's sections (Rule 1).

guard_own_words.py checks Claude Code's file tools before they run. A shell
command can't be checked that way (`echo >> note.md`, `python3 -c …`, `mv`), so
this hook runs around every Bash call instead:

    PreToolUse  Bash   snapshot every note in the note folders
    PostToolUse Bash   compare; any note whose protected sections or type changed
                       is put back as it was, and a note created with filled
                       sections is removed. The version the command left is
                       saved to _tutor/guard/ first, so nothing is lost even if
                       the learner was typing in Obsidian during the command.

The same comparison as guard_own_words.py: protected sections by every copy of
their heading, and the frontmatter type. Standard library only.
"""
import datetime, hashlib, json, os, shutil, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guard_own_words import changed_sections, label  # noqa: E402

NOTE_DIRS = ("01-systems", "02-ai", "03-methodologies", "04-senior-multipliers", "06-builds")


def root():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))


def notes(base):
    out = {}
    for d in NOTE_DIRS:
        for dirpath, _, files in os.walk(os.path.join(base, d)):
            for name in files:
                if name.lower().endswith(".md"):
                    p = os.path.join(dirpath, name)
                    with open(p, encoding="utf-8", errors="replace") as f:
                        out[os.path.relpath(p, base)] = f.read()
    return out


def snapshot_path(event):
    key = f"{event.get('session_id', '')}:{event.get('tool_use_id', '')}"
    folder = os.path.join(tempfile.gettempdir(), "breakpoint-guard")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, hashlib.sha256(key.encode()).hexdigest()[:24] + ".json")


def backup(base, rel, text):
    stamp = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
    dst = os.path.join(base, "_tutor", "guard", f"{stamp}-{os.path.basename(rel)}")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(text)
    return os.path.relpath(dst, base)


def check(base, before, after):
    """Undo every protected change; return one line per note put back."""
    lines = []
    for rel in sorted(set(before) | set(after)):
        old, new = before.get(rel), after.get(rel)
        path = os.path.join(base, rel)
        if old is not None and new is None:
            hit = changed_sections(old, "")             # deleted: protected if it was a note
            if hit:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(old)
                lines.append(f"{rel}: deleted; restored")
            continue
        hit = changed_sections(old or "", new)
        if not hit:
            continue
        saved = backup(base, rel, new)
        if old is None:
            os.remove(path)
            lines.append(f"{rel}: created with {', '.join(label(h) for h in hit)} filled; "
                         f"removed (copy in {saved})")
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(old)
            lines.append(f"{rel}: changed {', '.join(label(h) for h in hit)}; "
                         f"restored (the changed version is in {saved})")
    return lines


def main():
    event = json.load(sys.stdin)
    if event.get("tool_name") != "Bash":
        return 0
    base, snap = root(), snapshot_path(event)
    if event.get("hook_event_name") == "PreToolUse":
        with open(snap, "w", encoding="utf-8") as f:
            json.dump(notes(base), f)
        return 0
    if not os.path.exists(snap):
        return 0
    with open(snap, encoding="utf-8") as f:
        before = json.load(f)
    os.remove(snap)
    lines = check(base, before, notes(base))
    if not lines:
        return 0
    print("Breakpoint (Rule 1): that shell command changed the learner's sections, so the "
          "notes were put back:\n  " + "\n  ".join(lines) + "\nThose sections are the "
          "learner's to write. Tell the learner what happened; don't retry another way.",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:              # fail closed, like guard_own_words.py
        print(f"Breakpoint shell guard failed ({e!r}); blocking to be safe. "
              "Run .claude/hooks/test_guard_shell.py.", file=sys.stderr)
        sys.exit(2)
