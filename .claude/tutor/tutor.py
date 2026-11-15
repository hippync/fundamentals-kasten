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
    python3 .claude/tutor/tutor.py concept "Stack vs heap"
    python3 .claude/tutor/tutor.py record c-stack-vs-heap partial
    python3 .claude/tutor/tutor.py sections "Stack vs heap"
    python3 .claude/tutor/tutor.py set-status c-stack-vs-heap explained

set-status is the one command that writes to a note: frontmatter status and
tags only, along the transitions in _tutor/README.md. Run it after the learner
confirms. Every command takes --root (default: this repo) and --today (default: today).
Standard library only, like scripts/.
"""
import argparse, datetime, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "hooks"))
from guard_own_words import PROTECTED, CALLOUT, sections as protected_sections, is_blank  # noqa: E402
DEFAULT_ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(HERE))
NOTE_DIRS = ("01-systems", "02-ai", "03-methodologies", "04-senior-multipliers",
             "06-builds", "07-program")
STATUS_ORDER = ("stub", "drafted", "explained", "tested")
INTERVALS = {1: 1, 2: 3, 3: 7, 4: 14, 5: 30}          # box -> days until next due
RESULTS = ("pass", "partial", "fail", "dont-know")
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


def concept_info(k, ref):
    cid = k.resolve(ref)
    if not cid or k.notes[cid]["fm"].get("type") != "concept":
        raise SystemExit(f"No concept note matches {ref!r}. Try its id or exact title.")
    note = k.notes[cid]
    related = [k.resolve(t) for t in wikilinks(section(note["text"], "## Related"))]
    prereqs = [r for r in related if r and k.notes[r]["fm"].get("type") == "concept"]
    questions = re.findall(r"(?m)^- \[[ x]\] (.+)$",
                           section(note["text"], "## Questions I should be able to answer"))
    entry = next((e for e in k.ledger() if e["concept"] == cid), None)
    return {"id": cid, "title": note["fm"].get("title"), "path": k.rel(cid),
            "status": note["fm"].get("status", "stub"), "prerequisites": prereqs,
            "questions": questions, "ledger": entry}


def show_concept(k, info):
    out = [f"id: {info['id']}", f"title: {info['title']}", f"path: {info['path']}",
           f"status: {info['status']}"]
    e = info["ledger"]
    out.append(f"ledger: box {e['box']}, last {e['last-result']} on {e['last-probed']}, "
               f"due {e['next-due']}" if e else "ledger: never probed")
    out.append("prerequisites (from Related, in order):")
    out += [f"  {p}  ({k.notes[p]['fm'].get('title')}, {k.notes[p]['fm'].get('status', 'stub')})"
            for p in info["prerequisites"]] or ["  (none)"]
    out.append("questions:")
    out += [f"  - {q}" for q in info["questions"]] or ["  (none)"]
    return "\n".join(out)


def record(k, concept_id, result, today):
    """Apply one probe result to a concept's ledger file; return the new entry."""
    if result not in RESULTS:
        raise SystemExit(f"Unknown result {result!r}; one of {', '.join(RESULTS)}.")
    if concept_id not in k.of_type("concept"):
        raise SystemExit(f"{concept_id!r} is not a concept id. Use the id from the note's frontmatter.")
    old = next((e for e in k.ledger() if e["concept"] == concept_id), None)
    box = int(old["box"]) if old else 1                     # a first probe starts in box 1
    if result == "pass":
        box = min(box + 1, 5)
    elif result != "partial":                               # fail, dont-know
        box = 1
    entry = {"concept": concept_id, "box": box, "last-result": result,
             "last-probed": today.isoformat(),
             "next-due": (today + datetime.timedelta(days=INTERVALS[box])).isoformat()}
    folder = os.path.join(k.tutor, "ledger")
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, f"{concept_id}.md"), "w", encoding="utf-8") as f:
        f.write("---\n" + "".join(f"{key}: {value}\n" for key, value in entry.items()) + "---\n")
    return old, entry


# ---------------------------------------------------------------- status

def filled(k, ref):
    """{label: True/False} for the learner's sections of a concept or build note."""
    nid = k.resolve(ref)
    kind = k.notes[nid]["fm"].get("type") if nid else None
    if kind not in PROTECTED:
        raise SystemExit(f"No concept or build note matches {ref!r}.")
    found = protected_sections(k.notes[nid]["text"], kind)
    label = lambda h: "Predict the failure" if h == CALLOUT else h[3:]
    return nid, {label(h): not is_blank(found[h]) for h in PROTECTED[kind]}


BODY = ("Predict the failure", "What it is", "How it breaks")
POSTMORTEM = ("What actually happened", "What I got wrong")


def builds_done_for(k, concept_id):
    """Builds listing this concept under Concepts this touched, with a post-mortem written."""
    out = []
    for bid, note in sorted(k.of_type("build").items()):
        touched = [k.resolve(t) for t in wikilinks(section(note["text"], "## Concepts this touched"))]
        if concept_id in touched and all(filled(k, bid)[1][h] for h in POSTMORTEM):
            out.append(bid)
    return out


def check_transition(k, cid, new, reread):
    """Why the move is allowed, or SystemExit saying why not."""
    if cid not in k.of_type("concept"):
        raise SystemExit(f"{cid!r} is not a concept id.")
    old = k.notes[cid]["fm"].get("status", "stub")
    if new not in STATUS_ORDER:
        raise SystemExit(f"Unknown status {new!r}; one of {', '.join(STATUS_ORDER)}.")
    step = STATUS_ORDER.index(new) - STATUS_ORDER.index(old)
    if step == -1:
        if not reread:
            raise SystemExit("A step back only follows a failed /revisit: pass --reread.")
        return old, "one step back after a failed /revisit, tagged reread"
    if step != 1 or reread:
        raise SystemExit(f"{old} -> {new} is not a transition. Allowed: one step forward, "
                         "or one step back with --reread.")
    _, have = filled(k, cid)
    if new == "drafted":
        missing = [h for h in BODY if not have[h]]
        if missing:
            raise SystemExit(f"stub -> drafted needs {', '.join(missing)} written first.")
        return old, "body sections filled"
    if new == "explained":
        if not have["In my own words"]:
            raise SystemExit("drafted -> explained needs In my own words written.")
        return old, ("In my own words written; closed book and no blocking hole from /critique "
                     "are the learner's confirmation, not checked here")
    builds = builds_done_for(k, cid)
    if not builds:
        raise SystemExit("explained -> tested needs a build that lists this concept under "
                         "Concepts this touched, with What actually happened and What I got wrong filled.")
    return old, "post-mortem written in " + ", ".join(builds)


def set_status(k, cid, new, reread=False):
    old, why = check_transition(k, cid, new, reread)
    path = k.notes[cid]["path"]
    text = read(path)
    end = text.find("\n---", 4)
    head, rest = text[:end], text[end:]
    head, n = re.subn(r'(?m)^status:.*$', f'status: "{new}"', head, count=1)
    if not n:
        raise SystemExit(f"{k.rel(cid)} has no status line in its frontmatter.")
    if reread and "reread" not in (k.notes[cid]["fm"].get("tags") or []):
        lines = head.split("\n")
        if "tags:" in lines:                    # append after the last item of the tags list
            at = lines.index("tags:") + 1
            while at < len(lines) and re.match(r"^\s+-", lines[at]):
                at += 1
            lines.insert(at, '  - "reread"')
        else:
            lines += ["tags:", '  - "reread"']
        head = "\n".join(lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + rest)
    return old, why


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
    dp = sub.add_parser("due", help="ledger entries with next-due on or before today, oldest first")
    dp.add_argument("--limit", type=int, help="at most this many (/revisit takes %d)" % REVISIT_CAP_ITEMS)
    pp = sub.add_parser("plan", help="what to do now, in order, for the time available")
    pp.add_argument("--minutes", type=int, default=60)
    pp.add_argument("--block", help="default: block in progress.md")
    cp = sub.add_parser("concept", help="a concept's status, ledger entry, prerequisites and questions")
    cp.add_argument("ref", help="id, title, [[link]] or path")
    rp = sub.add_parser("record", help="apply a probe result to the concept's ledger file")
    rp.add_argument("concept")
    rp.add_argument("result", choices=RESULTS)
    fp = sub.add_parser("sections", help="which of the learner's sections are written")
    fp.add_argument("ref")
    sp = sub.add_parser("set-status", help="change a concept's status along the transition rules")
    sp.add_argument("concept")
    sp.add_argument("status", choices=STATUS_ORDER)
    sp.add_argument("--reread", action="store_true", help="the step back after a failed /revisit")
    sp.add_argument("--check", action="store_true", help="say whether it's allowed; write nothing")
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
        print(f"{len(due)} due on {args.today.isoformat()}"
              + (f", showing {min(args.limit, len(due))}" if args.limit else ""))
        for e in due[:args.limit]:
            print(f"  {e['concept']}  box {e['box']}  due {e['next-due']}  last {e['last-result']}")
    elif args.cmd == "plan":
        block = args.block or (k.progress() or {}).get("block")
        if not block:
            raise SystemExit("No block: pass --block or create _tutor/progress.md first.")
        print(show_plan(plan(k, block, args.minutes, args.today)))
    elif args.cmd == "concept":
        print(show_concept(k, concept_info(k, args.ref)))
    elif args.cmd == "record":
        old, new = record(k, args.concept, args.result, args.today)
        before = f"box {old['box']}" if old else "new"
        print(f"{new['concept']}: {args.result}, {before} -> box {new['box']}, next due {new['next-due']}")
    elif args.cmd == "sections":
        nid, have = filled(k, args.ref)
        print(nid)
        for h, ok in have.items():
            print(f"  {'written' if ok else 'empty  '}  {h}")
    elif args.cmd == "set-status":
        if args.check:
            old, why = check_transition(k, args.concept, args.status, args.reread)
            print(f"allowed: {args.concept} {old} -> {args.status} ({why})")
        else:
            old, why = set_status(k, args.concept, args.status, args.reread)
            print(f"{args.concept}: {old} -> {args.status} ({why})")
    elif args.cmd == "log-path":
        print(log_path(k, args.skill, args.today))
    return 0


if __name__ == "__main__":
    sys.exit(main())
