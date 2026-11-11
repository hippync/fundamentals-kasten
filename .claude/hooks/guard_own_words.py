#!/usr/bin/env python3
"""Breakpoint guard: block edits to the learner's sections (ADR 0001, Rule 1).

Claude Code runs this before every Edit, MultiEdit and Write. It simulates the
change, extracts the protected parts of the note before and after, and blocks
the tool call (exit 2) if any of them would change. Everything else passes:
frontmatter, the other sections, every other file.

Standard library only, like scripts/.
"""
import json, os, re, sys

PROTECTED = {
    "concept": ("> [!question] Predict the failure",
                "## What it is", "## How it breaks", "## In my own words"),
    "build": ("## Plan", "## The failure I'm going to cause on purpose",
              "## What actually happened", "## What I got wrong"),
}
CALLOUT = "> [!question] Predict the failure"
# Scaffolding that ships in an empty section; anything else is the learner's.
SCAFFOLD = re.compile(r"<!--.*?-->|^> \*What breaks when.*?\*$", re.S | re.M)


def note_type(text):
    m = re.search(r'(?m)^type:\s*"?(\w+)"?\s*$', text.split("\n---", 1)[0])
    return m.group(1) if m else None


def sections(text, kind):
    """Map each protected heading to its content, or None if it's missing."""
    lines = text.split("\n")
    out = {}
    for head in PROTECTED[kind]:
        try:
            start = lines.index(head)
        except ValueError:
            out[head] = None
            continue
        body = []
        for line in lines[start + 1:]:
            if head == CALLOUT:
                if not line.startswith(">"):
                    break
            elif line.startswith("## ") or line.startswith("# "):
                break
            body.append(line.rstrip())
        out[head] = "\n".join(body).strip()
    return out


def apply_edit(text, old, new, replace_all=False):
    if old not in text:
        return None                     # the tool itself will reject this edit
    return text.replace(old, new) if replace_all else text.replace(old, new, 1)


def simulate(tool, args, before):
    if tool == "Write":
        return args.get("content", "")
    if tool == "Edit":
        return apply_edit(before, args.get("old_string", ""), args.get("new_string", ""),
                          args.get("replace_all", False))
    if tool == "MultiEdit":
        text = before
        for e in args.get("edits", []):
            text = apply_edit(text, e.get("old_string", ""), e.get("new_string", ""),
                              e.get("replace_all", False))
            if text is None:
                return None
        return text
    return None


def is_blank(content):
    return content is None or not SCAFFOLD.sub("", content).strip()


def changed_sections(before, after):
    kind = note_type(before) if before else None
    kind = kind if kind in PROTECTED else note_type(after)
    if kind not in PROTECTED:
        return []
    old = sections(before, kind) if before else {}
    new = sections(after, kind)
    if not before:                      # a new note: only blank sections may be written
        return [h for h in PROTECTED[kind] if not is_blank(new[h])]
    return [h for h in PROTECTED[kind] if old[h] != new[h]]


def label(head):
    return "Predict the failure" if head == CALLOUT else head[3:]


def main():
    event = json.load(sys.stdin)
    tool = event.get("tool_name", "")
    args = event.get("tool_input", {}) or {}
    path = args.get("file_path", "")
    if tool not in ("Edit", "MultiEdit", "Write") or not path.endswith(".md"):
        return 0
    before = ""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            before = f.read()
    after = simulate(tool, args, before)
    if after is None:
        return 0
    hit = changed_sections(before, after)
    if not hit:
        return 0
    names = ", ".join(f"*{label(h)}*" for h in hit)
    print(f"Blocked by Breakpoint (Rule 1): this would change {names} in "
          f"{os.path.basename(path)}. Those sections are the learner's to write. "
          "Explain in chat, ask the question that gets them to the next sentence, "
          "or offer /critique on what they wrote. Frontmatter status and tags, and "
          "the other sections, can still be edited.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:              # fail closed: a broken guard must not wave edits through
        print(f"Breakpoint guard failed ({e!r}); blocking to be safe. "
              "Run .claude/hooks/test_guard_own_words.py.", file=sys.stderr)
        sys.exit(2)
