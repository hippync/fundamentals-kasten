#!/usr/bin/env python3
"""Reset every note in this kasten back to its shipped, empty state.

Use this to hand someone a clean copy, or to start over on a rung.
Destructive: it deletes the sections you wrote. Commit first.

    python scripts/reset.py --dry-run        # show what would change
    python scripts/reset.py                  # reset everything
    python scripts/reset.py 01-systems/s01-the-machine   # reset one rung
"""
import argparse, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    args = ap.parse_args()
    roots = [os.path.join(ROOT, p) for p in args.paths] or [ROOT]
    changed = 0
    for r in roots:
        for dirpath, dirnames, filenames in os.walk(r):
            dirnames[:] = [d for d in dirnames if d not in (".git", ".obsidian", "_templates")]
            for fn in sorted(filenames):
                if not fn.endswith(".md"):
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
    print("\n%d file(s) %s" % (changed, "would change" if args.dry_run else "reset"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
