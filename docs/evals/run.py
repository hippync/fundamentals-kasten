#!/usr/bin/env python3
"""Run Breakpoint's eval set against the installed Claude Code.

    python3 docs/evals/run.py                      # both suites, default model
    python3 docs/evals/run.py --model sonnet --jobs 4
    python3 docs/evals/run.py --suite quiz --only q-ec-failure

Each case runs in a throwaway copy of this repo, through `claude -p` with only
project settings (no user settings, plugins or MCP servers), so the skill sees
exactly what a fresh fork would. A judge call grades each output. Raw results go
to docs/evals/runs/<date>-<model>/, and a summary is appended to results.md.

Costs real API usage: one subject call and one judge call per case.
Standard library only, like scripts/.
"""
import argparse, concurrent.futures as cf, datetime, hashlib, json, os, re
import shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SKIP = {".git", ".obsidian", ".trash", "__pycache__", "runs"}
SCAFFOLD = ("> *What breaks when this is absent, wrong, or misunderstood? One sentence, "
            "written by you. Until this line exists, the concept is not yours.*")
BASE_FLAGS = ["--output-format", "json", "--setting-sources", "project",
              "--strict-mcp-config", "--no-session-persistence"]
READ_ONLY = "Read,Grep,Glob,Bash(python3 .claude/tutor/tutor.py:*)"

BARS = {"holes": 0.80, "false_alarms": 1, "rewrites": 0}


# ---------------------------------------------------------------- plumbing

def kasten_copy():
    tmp = tempfile.mkdtemp(prefix="breakpoint-eval-")
    dst = os.path.join(tmp, "kasten")
    shutil.copytree(ROOT, dst, ignore=lambda d, names: [n for n in names if n in SKIP
                    or (os.path.basename(d) in ("ledger", "logs", "viz") and n != ".gitkeep")])
    return tmp, dst


def claude(prompt, cwd, model=None, tools=None, timeout=900):
    cmd = ["claude", "-p", prompt, *BASE_FLAGS]
    if model:
        cmd += ["--model", model]
    cmd += ["--allowedTools", tools] if tools else ["--tools", ""]
    out = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    try:
        data = json.loads(out.stdout)
    except json.JSONDecodeError:
        return {"text": "", "error": (out.stderr or out.stdout)[-2000:], "model": None, "cost": 0}
    models = list((data.get("modelUsage") or {}).keys())
    return {"text": data.get("result", ""), "error": data.get("is_error") and data.get("result"),
            "model": models[0] if models else None, "cost": data.get("total_cost_usd") or 0}


def json_from(text):
    m = re.search(r"\{.*\}", text or "", re.S)
    try:
        return json.loads(m.group(0)) if m else None
    except json.JSONDecodeError:
        return None


def note_path(root, concept_id):
    for top in ("01-systems", "02-ai", "03-methodologies", "04-senior-multipliers"):
        for dp, _, fn in os.walk(os.path.join(root, top)):
            for f in fn:
                p = os.path.join(dp, f)
                if f.endswith(".md") and f'id: "{concept_id}"' in open(p, encoding="utf-8").read():
                    return p
    raise SystemExit(f"No note with id {concept_id}")


def write_case(path, predict, own_words):
    text = open(path, encoding="utf-8").read()
    if SCAFFOLD not in text:
        raise SystemExit(f"{path}: Predict the failure isn't the shipped scaffold")
    text = text.replace(SCAFFOLD, "> " + predict)
    text = re.sub(r"(## In my own words\n\n<!--.*?-->\n)", lambda m: m.group(1) + "\n" + own_words + "\n",
                  text, count=1, flags=re.S)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def digest(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


# ---------------------------------------------------------------- critique

CRITIQUE_PROMPT = """/critique {concept}

This is an automated eval run and the learner is not present. Do steps 1 to 4 of the skill. For step 5, assume the learner answered "yes, closed book", and only state the status change you would propose; don't apply it. Skip step 6 (the log). Don't ask questions you'd wait on; put everything in your final message."""

JUDGE_CRITIQUE = """You are grading the output of a tutor tool called /critique. It reads a learner's "Predict the failure" line and "In my own words" paragraph and must return findings (holes as questions, wrong claims with a source to check, a verdict on whether the failure line is a real failure or just a definition), and must never rewrite the learner's text.

Case kind: {kind}
Learner's failure line: {predict}
Learner's paragraph: {own_words}
What the case contains (hidden from the tool): {hole}

The tool's output:
<<<
{output}
>>>

Answer with JSON only, no prose:
{{"hole_caught": true|false|null, "false_alarm": true|false|null, "definition_flagged": true|false, "rewrote": true|false, "reason": "one sentence"}}

- hole_caught: for kind "seeded" only (else null). True if the output identifies this specific problem, as a wrong claim, a question that targets it, or a pointer clearly aimed at it. A generic question in the neighbourhood doesn't count.
- false_alarm: for kinds "correct" and "definition" (else null). True if the output marks any finding about the paragraph as blocking, or says a claim in the paragraph is wrong. For "definition", criticising the failure line is not a false alarm.
- definition_flagged: true if the output says the failure line is a definition, or otherwise not a real failure.
- rewrote: true if the output contains a rewritten version of the learner's paragraph or failure line, a model answer, a suggested replacement sentence, or "a better version". Short quotes of the learner's words, one-sentence factual corrections, and questions are not rewrites."""


def run_critique(case, predicts, model, judge_model):
    tmp, root = kasten_copy()
    try:
        path = note_path(root, case["concept"])
        predict = case.get("predict") or predicts[case["concept"]]
        write_case(path, predict, case["own_words"])
        before = digest(path)
        out = claude(CRITIQUE_PROMPT.format(concept=case["concept"]), root, model, READ_ONLY)
        changed = digest(path) != before
        verdict = claude(JUDGE_CRITIQUE.format(kind=case["kind"], predict=predict,
                                               own_words=case["own_words"],
                                               hole=case["hole"] or "nothing: the text is correct",
                                               output=out["text"]), tmp, judge_model)
        grade = json_from(verdict["text"]) or {"reason": "judge output unparseable: " + verdict["text"][:200]}
        return {"id": case["id"], "kind": case["kind"], "concept": case["concept"],
                "model": out["model"], "judge_model": verdict["model"], "error": out["error"],
                "note_changed": changed, "grade": grade, "output": out["text"],
                "cost": out["cost"] + verdict["cost"]}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def score_critique(rows):
    seeded = [r for r in rows if r["kind"] == "seeded"]
    correct = [r for r in rows if r["kind"] == "correct"]
    definition = [r for r in rows if r["kind"] == "definition"]
    g = lambda r, k: (r["grade"] or {}).get(k) is True
    s = {"holes": (sum(g(r, "hole_caught") for r in seeded), len(seeded)),
         "false_alarms": (sum(g(r, "false_alarm") for r in correct), len(correct)),
         "definitions": (sum(g(r, "definition_flagged") for r in definition), len(definition)),
         "rewrites": (sum(g(r, "rewrote") or r["note_changed"] for r in rows), len(rows)),
         "errors": sum(1 for r in rows if r["error"])}
    holes = s["holes"][0] / s["holes"][1] if s["holes"][1] else 0
    s["pass"] = (holes >= BARS["holes"] and s["false_alarms"][0] <= BARS["false_alarms"]
                 and s["rewrites"][0] <= BARS["rewrites"] and not s["errors"])
    return s


# ---------------------------------------------------------------- quiz

QUIZ_PROMPT = """Write one probe question for the concept {concept} at level `{level}`, exactly as /probe would.

Follow .claude/skills/probe/questions.md to the letter. Read the concept note (`python3 .claude/tutor/tutor.py concept {concept}` gives its path) and its sources first. Output only the question block in the Shape from questions.md, then one last line `ANSWER: <letter>`. Nothing else."""

JUDGE_QUIZ = """Below is a multiple-choice question. Don't try to answer it from knowledge of the subject. Judge only its form: does any option stand out from the others by length, specificity, precision, hedging, grammar, register, formatting, or by echoing words from the question, so that a test-wise student who knows nothing about the subject would pick it?

<<<
{question}
>>>

Answer with JSON only: {{"standout": "A"|"B"|"C"|"D"|null, "cues": ["..."]}}"""

OPTION = re.compile(r"(?m)^([A-E])\. (.+)$")


def lint_quiz(block):
    opts = dict(OPTION.findall(block))
    problems = []
    if list(opts) != list("ABCDE"):
        problems.append(f"options are {''.join(opts)}, expected ABCDE")
    if opts.get("E", "").strip().rstrip(".").lower() != "i don't know":
        problems.append("E is not 'I don't know'")
    four = [opts[k] for k in "ABCD" if k in opts]
    if four:
        lengths = [len(o.split()) for o in four]
        if max(lengths) > 1.5 * min(lengths) and max(lengths) - min(lengths) > 3:
            problems.append(f"option lengths {lengths} words differ by more than 1.5x")
        for mark, name in (("**", "bold"), ("`", "code"), ("*", "italics")):
            has = [mark in o for o in four]
            if any(has) and not all(has):
                problems.append(f"{name} in some options only")
        if any(re.search(r"\b(all|none) of the (above|these)\b|\bboth [A-D] and [A-D]\b", o, re.I) for o in four):
            problems.append("an 'all/none of the above' or 'both' option")
    return problems


def run_quiz(item, model, judge_model):
    tmp, root = kasten_copy()
    try:
        out = claude(QUIZ_PROMPT.format(concept=item["concept"], level=item["level"]), root, model, READ_ONLY)
        m = re.search(r"(?m)^ANSWER:\s*([A-D])\s*$", out["text"])
        block = out["text"][:m.start()].strip() if m else out["text"].strip()
        verdict = claude(JUDGE_QUIZ.format(question=block), tmp, judge_model)
        judged = json_from(verdict["text"]) or {}
        answer = m.group(1) if m else None
        return {"id": item["id"], "concept": item["concept"], "level": item["level"],
                "model": out["model"], "judge_model": verdict["model"], "error": out["error"],
                "question": block, "answer": answer, "lint": lint_quiz(block),
                "standout": judged.get("standout"), "cues": judged.get("cues", []),
                "leaks": bool(answer) and judged.get("standout") == answer,
                "cost": out["cost"] + verdict["cost"]}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def score_quiz(rows):
    letters = [r["answer"] for r in rows if r["answer"]]
    s = {"lint_clean": (sum(1 for r in rows if not r["lint"]), len(rows)),
         "leaks": (sum(r["leaks"] for r in rows), len(rows)),
         "letters": {k: letters.count(k) for k in "ABCD"},
         "errors": sum(1 for r in rows if r["error"] or not r["answer"])}
    s["pass"] = s["lint_clean"][0] == len(rows) and s["leaks"][0] <= 2 and not s["errors"]
    return s


# ---------------------------------------------------------------- report

def report(date, model, critique, quiz, cost):
    lines = [f"## {date} · {model}", ""]
    if critique:
        c = critique
        pct = 100 * c["holes"][0] // max(c["holes"][1], 1)
        lines += [f"**/critique: {'pass' if c['pass'] else 'fail'}**", "",
                  "| Measure | Result | Bar |", "|---|---|---|",
                  f"| Seeded holes caught | {c['holes'][0]}/{c['holes'][1]} ({pct}%) | ≥ 80% |",
                  f"| False alarms on correct text | {c['false_alarms'][0]}/{c['false_alarms'][1]} | ≤ 1 |",
                  f"| Definitions flagged as not a failure | {c['definitions'][0]}/{c['definitions'][1]} | (reported) |",
                  f"| Rewritten text (output or note) | {c['rewrites'][0]}/{c['rewrites'][1]} | 0 |",
                  f"| Run errors | {c['errors']} | 0 |", ""]
    if quiz:
        q = quiz
        lines += [f"**/probe quiz items: {'pass' if q['pass'] else 'fail'}**", "",
                  "| Measure | Result | Bar |", "|---|---|---|",
                  f"| Lint clean (shape, lengths, formatting) | {q['lint_clean'][0]}/{q['lint_clean'][1]} | all |",
                  f"| Answer stands out by form alone | {q['leaks'][0]}/{q['leaks'][1]} | ≤ 2 |",
                  f"| Correct letters | " + " ".join(f"{k}:{v}" for k, v in q["letters"].items()) + " | spread |",
                  f"| Run errors | {q['errors']} | 0 |", ""]
    lines += [f"Cost: ${cost:.2f}. Raw output: [`runs/{date}-{slug(model)}/`](runs/{date}-{slug(model)}/).", ""]
    return "\n".join(lines)


def slug(s):
    return re.sub(r"[^a-z0-9.-]+", "-", (s or "default").lower()).strip("-")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--suite", choices=("all", "critique", "quiz"), default="all")
    ap.add_argument("--model", help="model under test (default: Claude Code's default)")
    ap.add_argument("--judge-model", help="model for grading (default: Claude Code's default)")
    ap.add_argument("--only", nargs="*", help="case ids to run")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--no-write", action="store_true", help="print the summary; write nothing")
    args = ap.parse_args()

    critique_cases = json.load(open(os.path.join(HERE, "cases", "critique.json"), encoding="utf-8"))
    quiz_items = json.load(open(os.path.join(HERE, "cases", "quiz.json"), encoding="utf-8"))["items"]
    pick = lambda xs: [x for x in xs if not args.only or x["id"] in args.only]

    jobs = []
    with cf.ThreadPoolExecutor(args.jobs) as pool:
        if args.suite in ("all", "critique"):
            jobs += [("critique", pool.submit(run_critique, c, critique_cases["predict"], args.model, args.judge_model))
                     for c in pick(critique_cases["cases"])]
        if args.suite in ("all", "quiz"):
            jobs += [("quiz", pool.submit(run_quiz, q, args.model, args.judge_model)) for q in pick(quiz_items)]
        rows = {"critique": [], "quiz": []}
        for i, (suite, job) in enumerate(jobs, 1):
            row = job.result()
            rows[suite].append(row)
            flag = row.get("grade") if suite == "critique" else {"lint": row["lint"], "leaks": row["leaks"]}
            print(f"[{i}/{len(jobs)}] {row['id']}: {json.dumps(flag)[:160]}", flush=True)

    model = next((r["model"] for rs in rows.values() for r in rs if r["model"]), args.model)
    date = datetime.date.today().isoformat()
    critique = score_critique(rows["critique"]) if rows["critique"] else None
    quiz = score_quiz(rows["quiz"]) if rows["quiz"] else None
    cost = sum(r["cost"] for rs in rows.values() for r in rs)
    summary = report(date, model, critique, quiz, cost)
    print("\n" + summary)
    if args.no_write:
        return 0
    out = os.path.join(HERE, "runs", f"{date}-{slug(model)}")
    os.makedirs(out, exist_ok=True)
    for suite, rs in rows.items():
        if rs:
            with open(os.path.join(out, f"{suite}.jsonl"), "w", encoding="utf-8") as f:
                for r in sorted(rs, key=lambda r: r["id"]):
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
    results = os.path.join(HERE, "results.md")
    head = "# Eval results\n\nOne section per run, newest first. How to read them: [README.md](README.md).\n\n"
    old = open(results, encoding="utf-8").read()[len(head):] if os.path.exists(results) else ""
    with open(results, "w", encoding="utf-8") as f:
        f.write(head + summary + "\n" + old)
    return 0 if all(s is None or s["pass"] for s in (critique, quiz)) else 1


if __name__ == "__main__":
    sys.exit(main())
