#!/usr/bin/env python3
"""Breakpoint's bookkeeping: the deterministic parts of every skill.

The skills ask the questions and judge the answers. This script does what must
come out the same every time: which revisits are due, what order to work in,
where the session log goes. It reads the kasten and writes only to _tutor/.
Formats: _tutor/README.md.

    python3 .claude/tutor/tutor.py progress
    python3 .claude/tutor/tutor.py init-progress --block blk-01-02 --start 2026-11-02 \\
        --language English [--primary Go]
    python3 .claude/tutor/tutor.py due
    python3 .claude/tutor/tutor.py plan --minutes 45
    python3 .claude/tutor/tutor.py log-path probe

Every command takes --root (default: this repo) and --today (default: today).
Standard library only, like scripts/.
"""
import argparse, datetime, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(HERE))
NOTE_DIRS = ("01-systems", "02-ai", "03-methodologies", "04-senior-multipliers",
             "06-builds", "07-program")
STATUS_ORDER = ("stub", "drafted", "explained", "tested")
INTERVALS = {1: 1, 2: 3, 3: 7, 4: 14, 5: 30}          # box -> days until next due
SKILLS = ("next", "probe", "critique", "revisit", "drill", "build-coach")

# Plan budget, in minutes.
REVISIT_PER_ITEM, REVISIT_CAP_MIN, REVISIT_CAP_ITEMS = 2, 15, 10
CONCEPT_MIN = 20
BUILD_MIN = 30
# Which concept statuses the plan picks up, and with which skill. A drafted note
# is closer to explained, so it comes before a fresh stub. Explained notes wait
# for the block's build; tested notes are done.
CONCEPT_STEP = {"drafted": "/critique", "stub": "/probe"}


# ---------------------------------------------------------------- parsing

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def frontmatter(text):
    """The YAML subset the kasten uses: scalars and lists of scalars."""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    data, key = {}, None
    for line in text[4:end].split("\n"):
        item = re.match(r"^\s+-\s+(.*)$", line)
        if item and key:
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(scalar(item.group(1)))
            continue
        kv = re.match(r"^([\w-]+):\s*(.*)$", line)
        if kv:
            key, value = kv.group(1), scalar(kv.group(2))
            data[key] = value if value != "" else []
    return {k: ("" if v == [] else v) for k, v in data.items()}


def scalar(raw):
    raw = raw.strip()
    if raw.startswith('"'):
        end = raw.find('"', 1)
        return raw[1:end] if end > 0 else raw[1:]
    raw = re.sub(r"\s+#.*$", "", raw)
    return int(raw) if re.fullmatch(r"-?\d+", raw) else raw


def section(text, heading):
    """The body under an H2, up to the next H1/H2."""
    lines = text.split("\n")
    try:
        start = lines.index(heading)
    except ValueError:
        return ""
    out = []
    for line in lines[start + 1:]:
        if line.startswith("## ") or line.startswith("# "):
            break
        out.append(line)
    return "\n".join(out)


def wikilinks(text):
    return [m.split("|")[0].split("#")[0].strip() for m in re.findall(r"\[\[([^\]]+)\]\]", text)]


def parse_date(s):
    return datetime.date.fromisoformat(str(s))


# ---------------------------------------------------------------- the kasten

class Kasten:
    def __init__(self, root):
        self.root = root
        self.tutor = os.path.join(root, "_tutor")
        self.notes = {}          # id -> {"path", "text", "fm"}
        self.by_title = {}       # title -> id
        for top in NOTE_DIRS:
            for dirpath, _, files in os.walk(os.path.join(root, top)):
                for name in sorted(files):
                    if not name.endswith(".md"):
                        continue
                    path = os.path.join(dirpath, name)
                    text = read(path)
                    fm = frontmatter(text)
                    if not fm.get("id"):
                        continue
                    self.notes[fm["id"]] = {"path": path, "text": text, "fm": fm}
                    self.by_title[fm.get("title") or name[:-3]] = fm["id"]

    def of_type(self, kind):
        return {i: n for i, n in self.notes.items() if n["fm"].get("type") == kind}

    def resolve(self, ref):
        """A note id from an id, a title, a [[wikilink]] or a path."""
        ref = ref.strip().strip("[]")
        if ref in self.notes:
            return ref
        base = os.path.basename(ref)
        base = base[:-3] if base.endswith(".md") else base
        return self.by_title.get(ref) or self.by_title.get(base)

    def rel(self, note_id):
        return os.path.relpath(self.notes[note_id]["path"], self.root)

    # -- _tutor/

    def progress(self):
        path = os.path.join(self.tutor, "progress.md")
        return frontmatter(read(path)) if os.path.exists(path) else None

    def ledger(self):
        folder = os.path.join(self.tutor, "ledger")
        out = []
        if os.path.isdir(folder):
            for name in sorted(os.listdir(folder)):
                if name.endswith(".md"):
                    fm = frontmatter(read(os.path.join(folder, name)))
                    if fm.get("concept"):
                        out.append(fm)
        return out

    def due(self, today):
        items = [e for e in self.ledger() if parse_date(e["next-due"]) <= today]
        return sorted(items, key=lambda e: (str(e["next-due"]), int(e["box"]), e["concept"]))

    # -- the program

    def block_parts(self, block_id):
        """(systems concepts, AI concepts, builds) for a block, in note order."""
        block = self.notes.get(block_id)
        if not block or block["fm"].get("type") != "block":
            raise SystemExit(f"No block note with id {block_id!r} in 07-program/.")
        themes = block["fm"].get("theme") or []
        theme_notes = {t: n for n in self.of_type("theme").values()
                       for t in (n["fm"].get("theme") or [])}
        systems, ai = [], []
        for theme in themes:
            note = theme_notes.get(theme)
            if not note:
                continue
            ids = [self.resolve(t) for t in wikilinks(section(note["text"], "## Concepts on this rung"))]
            ids = [i for i in ids if i and self.notes[i]["fm"].get("type") == "concept"]
            (systems if theme.startswith("S") else ai).extend(ids)
        deliverable = section(block["text"], "## Deliverable")
        builds = [self.resolve(t) for t in wikilinks(deliverable)]
        builds = [b for b in builds if b and self.notes[b]["fm"].get("type") == "build"]
        return systems, ai, builds


# ---------------------------------------------------------------- commands

def plan(k, block_id, minutes, today):
    """Due revisits, then two systems concepts and one AI concept, then the build."""
    due = k.due(today)
    due_ids = {e["concept"] for e in due}
    systems, ai, builds = k.block_parts(block_id)

    def candidates(ids):
        picked = [i for i in ids if i not in due_ids
                  and k.notes[i]["fm"].get("status", "stub") in CONCEPT_STEP]
        rank = list(CONCEPT_STEP)
        return sorted(picked, key=lambda i: rank.index(k.notes[i]["fm"].get("status", "stub")))

    steps = []
    if due:
        n = min(len(due), REVISIT_CAP_ITEMS)
        steps.append({"skill": "/revisit", "minutes": min(REVISIT_CAP_MIN, REVISIT_PER_ITEM * n),
                      "ids": [e["concept"] for e in due[:n]], "per_item": REVISIT_PER_ITEM})
    for i in candidates(systems)[:2] + candidates(ai)[:1]:
        status = k.notes[i]["fm"].get("status", "stub")
        steps.append({"skill": CONCEPT_STEP[status], "minutes": CONCEPT_MIN, "ids": [i],
                      "status": status})
    for b in builds:
        if k.notes[b]["fm"].get("status") != "done":
            steps.append({"skill": "/build-coach", "minutes": BUILD_MIN, "ids": [b]})
            break

    # Strict order: once one step doesn't fit, it and everything after it wait.
    now, later, left = [], [], minutes
    for step in steps:
        if later:
            later.append(step)
        elif step["minutes"] <= left:
            now.append(step)
            left -= step["minutes"]
        elif step["skill"] == "/revisit" and left >= REVISIT_PER_ITEM:
            fit = left // REVISIT_PER_ITEM          # shrink the revisit to what fits
            now.append(dict(step, ids=step["ids"][:fit], minutes=fit * REVISIT_PER_ITEM))
            later.append(dict(step, ids=step["ids"][fit:],
                              minutes=min(REVISIT_CAP_MIN, REVISIT_PER_ITEM * (len(step["ids"]) - fit))))
            left -= fit * REVISIT_PER_ITEM
        elif step["skill"] == "/build-coach" and left >= BUILD_MIN // 2:
            now.append(dict(step, minutes=left))      # a short build session still counts
            left = 0
        else:
            later.append(step)
    return {"block": block_id, "minutes": minutes, "now": now, "later": later,
            "due_total": len(due), "spare": left}


def show_plan(p):
    def line(step):
        names = ", ".join(step["ids"])
        extra = f" (status {step['status']})" if "status" in step else ""
        if step["skill"] == "/revisit":
            names = f"{len(step['ids'])} due: {names}"
        return f"{step['minutes']:>3} min  {step['skill']} {names}{extra}"
    out = [f"Plan for {p['block']}, {p['minutes']} min ({p['due_total']} revisits due)", "", "Now:"]
    out += [f"  {i}. {line(s)}" for i, s in enumerate(p["now"], 1)] or ["  (nothing fits)"]
    if p["spare"]:
        out.append(f"  spare: {p['spare']} min")
    if p["later"]:
        out += ["", "Next session:"] + [f"  - {line(s)}" for s in p["later"]]
    return "\n".join(out)


def log_path(k, skill, today):
    if skill not in SKILLS:
        raise SystemExit(f"Unknown skill {skill!r}; one of {', '.join(SKILLS)}.")
    folder = os.path.join(k.tutor, "logs")
    base, n = f"{today.isoformat()}-{skill}", 1
    while True:
        name = base + (f"-{n}" if n > 1 else "") + ".md"
        if not os.path.exists(os.path.join(folder, name)):
            return os.path.relpath(os.path.join(folder, name), k.root)
        n += 1


def init_progress(k, block, start, language, primary):
    path = os.path.join(k.tutor, "progress.md")
    if os.path.exists(path):
        raise SystemExit("_tutor/progress.md already exists; edit it instead.")
    if block not in k.of_type("block"):
        raise SystemExit(f"No block note with id {block!r} in 07-program/.")
    parse_date(start)
    text = read(os.path.join(k.tutor, "templates", "progress.md"))
    for key, value in (("block", block), ("program-start", start),
                       ("primary-language", primary or ""), ("session-language", language)):
        text = re.sub(rf'(?m)^({re.escape(key)}:\s*)"[^"]*"', lambda m: f'{m.group(1)}"{value}"', text)
    os.makedirs(k.tutor, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return os.path.relpath(path, k.root)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--today", type=parse_date, default=datetime.date.today())
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("progress", help="print _tutor/progress.md, or say it's missing")
    ip = sub.add_parser("init-progress", help="create _tutor/progress.md from the template")
    ip.add_argument("--block", required=True)
    ip.add_argument("--start", required=True)
    ip.add_argument("--language", default="English")
    ip.add_argument("--primary", default="")
    sub.add_parser("due", help="ledger entries with next-due on or before today")
    pp = sub.add_parser("plan", help="what to do now, in order, for the time available")
    pp.add_argument("--minutes", type=int, default=60)
    pp.add_argument("--block", help="default: block in progress.md")
    lp = sub.add_parser("log-path", help="the next free session-log path for a skill")
    lp.add_argument("skill")
    args = ap.parse_args(argv)
    k = Kasten(args.root)

    if args.cmd == "progress":
        p = k.progress()
        if p is None:
            print("missing: _tutor/progress.md (ask for block, start date and session language, "
                  "then run init-progress)")
            return 1
        for key, value in p.items():
            print(f"{key}: {value}")
    elif args.cmd == "init-progress":
        print("wrote", init_progress(k, args.block, args.start, args.language, args.primary))
    elif args.cmd == "due":
        due = k.due(args.today)
        print(f"{len(due)} due on {args.today.isoformat()}")
        for e in due:
            print(f"  {e['concept']}  box {e['box']}  due {e['next-due']}  last {e['last-result']}")
    elif args.cmd == "plan":
        block = args.block or (k.progress() or {}).get("block")
        if not block:
            raise SystemExit("No block: pass --block or create _tutor/progress.md first.")
        print(show_plan(plan(k, block, args.minutes, args.today)))
    elif args.cmd == "log-path":
        print(log_path(k, args.skill, args.today))
    return 0


if __name__ == "__main__":
    sys.exit(main())
