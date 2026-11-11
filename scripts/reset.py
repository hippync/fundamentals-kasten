#!/usr/bin/env python3
"""Reset every note in this kasten back to its shipped, empty state.

Use this to hand someone a clean copy, or to start over on a rung.
Destructive: it deletes the sections you wrote. Commit first.

    python scripts/reset.py --dry-run        # show what would change
    python scripts/reset.py                  # reset everything
    python scripts/reset.py 01-systems/s01-the-machine   # reset one rung
    python scripts/reset.py --tutor          # also delete Breakpoint's session history

Breakpoint's files (_tutor/, .claude/, CLAUDE.md) are never touched unless you pass --tutor,
and then only the session history in _tutor/ is deleted.
"""
import argparse, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", ".obsidian", "_templates", "_tutor", ".claude"}
SKIP_FILES = {"CLAUDE.md"}
TUTOR = os.path.join(ROOT, "_tutor")
TUTOR_HISTORY = ("progress.md", "ledger", "logs", "viz")   # what a session writes
CLEARED = {
    "## What it is": "\n\n\n",
    "## How it breaks": "\n\n\n",
    "## In my own words":
        "\n\n<!-- Closed book. One paragraph. If you can't, status stays 'drafted'. -->\n\n\n",
}
PREDICT = ("> [!question] Predict the failure\n"
           "> *What breaks when this is absent, wrong, or misunderstood? One sentence, "
           "written by you. Until this line exists, the concept is not yours.*\n\n")
KEEP = {"## What it is", "## Why it matters now", "## How it breaks",
        "## Questions I should be able to answer", "## In my own words",
        "## Where I'd look", "## Related"}


def reset(text):
    if '\ntype: "concept"' not in text:
        return text.replace("- [x]", "- [ ]")
    text = re.sub(r'(?m)^status: ".*"$', 'status: "stub"', text)
    text = re.sub(r'(?m)^updated: ".*"$', 'updated: ""', text)
    parts = re.split(r'(?m)^(## .*)$', text)
    head = re.sub(r'(?ms)^> \[!question\] Predict the failure\n.*?\n\n(?=\S|\Z)',
                  PREDICT, parts[0])
    out = []
    for h, body in ((parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)):
        if h not in KEEP:
            continue                      # drop sections you added
        out.append(h + CLEARED.get(h, body).replace("- [x]", "- [ ]"))
    return head + "".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", default=[], help="subpaths to reset (default: all)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--tutor", action="store_true",
                    help="also delete _tutor/ session history (progress, ledger, logs, viz)")
    args = ap.parse_args()
    roots = [os.path.join(ROOT, p) for p in args.paths] or [ROOT]
    changed = 0
    for r in roots:
        for dirpath, dirnames, filenames in os.walk(r):
            if skipped(dirpath):
                dirnames[:] = []
                continue
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in sorted(filenames):
                if not fn.endswith(".md") or fn in SKIP_FILES:
                    continue
                p = os.path.join(dirpath, fn)
                with open(p, encoding="utf-8") as f:
                    before = f.read()
                after = reset(before)
                if after != before:
                    changed += 1
                    print(("would reset " if args.dry_run else "reset ") +
                          os.path.relpath(p, ROOT))
                    if not args.dry_run:
                        with open(p, "w", encoding="utf-8", newline="\n") as f:
                            f.write(after)
    if args.tutor:
        changed += clear_tutor(args.dry_run)
    print("\n%d file(s) %s" % (changed, "would change" if args.dry_run else "changed"))
    return 0


def skipped(path):
    """True if path is inside one of SKIP_DIRS, even when passed as a root."""
    rel = os.path.relpath(path, ROOT)
    return any(part in SKIP_DIRS for part in rel.split(os.sep))


def clear_tutor(dry_run):
    """Delete what sessions wrote to _tutor/. Keeps README, templates and .gitkeep."""
    removed = 0
    for name in TUTOR_HISTORY:
        top = os.path.join(TUTOR, name)
        if os.path.isfile(top):
            files = [top]
        else:
            files = [os.path.join(d, f) for d, _, fs in os.walk(top) for f in fs
                     if f != ".gitkeep"]
        for p in sorted(files):
            removed += 1
            print(("would delete " if dry_run else "delete ") + os.path.relpath(p, ROOT))
            if not dry_run:
                os.remove(p)
        if not dry_run and os.path.isdir(top):
            for d, _, _ in sorted(os.walk(top), reverse=True):
                if d != top and not os.listdir(d):
                    os.rmdir(d)
    return removed


if __name__ == "__main__":
    sys.exit(main())
