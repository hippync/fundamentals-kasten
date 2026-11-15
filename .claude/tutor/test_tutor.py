#!/usr/bin/env python3
"""Tests for tutor.py against a small fixture kasten.

    python3 .claude/tutor/test_tutor.py

Each test builds its own copy of the fixture in a temp folder, so tests that
write to _tutor/ can't affect each other. Standard library only.
"""
import contextlib, datetime, io, os, shutil, sys, tempfile, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tutor  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TODAY = datetime.date(2026, 11, 14)


def concept(cid, title, status, theme):
    return f'''---
id: "{cid}"
title: "{title}"
type: "concept"
status: "{status}"
theme:
  - "{theme}"
tags:
  - "concept"
---

# {title}

> [!question] Predict the failure
> *What breaks when this is absent, wrong, or misunderstood? One sentence, written by you. Until this line exists, the concept is not yours.*

## What it is


## Why it matters now

## How it breaks


## Questions I should be able to answer

- [ ] A question about {title}?

## In my own words

<!-- Closed book. One paragraph. If you can't, status stays 'drafted'. -->


## Where I'd look

## Related

- [[{"S01 — The machine" if theme == "S01" else "A1 — What a model actually is"}]]
'''


def theme(tid, title, code, concepts, questions):
    links = "\n".join(f"- [[{c}]]" for c in concepts)
    qs = "\n".join(f"- [ ] {q}" for q in questions)
    return f'''---
id: "{tid}"
title: "{title}"
type: "theme"
theme:
  - "{code}"
---

# {title}

## Concepts on this rung

{links}

## Answer these

{qs}

## Blocks
'''


def build(bid, title, status, concepts):
    links = "\n".join(f"- [[{c}]]" for c in concepts)
    return f'''---
id: "{bid}"
title: "{title}"
type: "build"
status: "{status}"
tags:
  - "build"
---

# {title}

> [!abstract] The exercise
> Do the thing.

## Plan

<!-- What are you building, in one paragraph, before you write any code. -->


## The failure I'm going to cause on purpose

<!-- Part 6, rule 2. Name it before you start. -->


## What actually happened



## What I got wrong

<!-- The most valuable section. Link the concept notes it corrects. -->


## Concepts this touched

{links}
'''


BLOCK = '''---
id: "blk-01-02"
title: "Block 01-02 — The machine"
type: "block"
theme:
  - "S01"
  - "A1"
---

# Block 01-02 — The machine

## Deliverable

Benchmark loops; write a tiny GPT

Related build notes: [[Measure cache locality]], [[Build a tiny GPT]]

## Log
'''

LEDGER = {   # concept -> (box, last-result, last-probed, next-due)
    "c-latency-numbers": (2, "pass", "2026-11-08", "2026-11-11"),
    "c-stack-vs-heap": (1, "fail", "2026-11-13", "2026-11-14"),
    "c-tokens": (3, "pass", "2026-11-13", "2026-11-20"),
    "c-system-calls": (1, "dont-know", "2026-11-09", "2026-11-10"),
}


def make_kasten(root):
    files = {
        "07-program/Block 01-02 — The machine.md": BLOCK,
        "01-systems/s01/S01 — The machine.md": theme(
            "t-s01", "S01 — The machine", "S01",
            ["Latency numbers", "Memory hierarchy and cache locality", "Stack vs heap",
             "System calls", "The OS scheduler and blocking IO"],
            ["Why is a cache miss slow?", "What is a system call?"]),
        "02-ai/a1/A1 — What a model actually is.md": theme(
            "t-a1", "A1 — What a model actually is", "A1",
            ["Tokens and tokenization", "Embeddings", "Attention"],
            ["What is a token?"]),
        "01-systems/s01/Latency numbers.md": concept("c-latency-numbers", "Latency numbers", "stub", "S01"),
        "01-systems/s01/Memory hierarchy and cache locality.md": concept(
            "c-memory-hierarchy", "Memory hierarchy and cache locality", "explained", "S01"),
        "01-systems/s01/Stack vs heap.md": concept("c-stack-vs-heap", "Stack vs heap", "drafted", "S01"),
        "01-systems/s01/System calls.md": concept("c-system-calls", "System calls", "stub", "S01"),
        "01-systems/s01/The OS scheduler and blocking IO.md": concept(
            "c-os-scheduler", "The OS scheduler and blocking IO", "stub", "S01"),
        "02-ai/a1/Tokens and tokenization.md": concept("c-tokens", "Tokens and tokenization", "tested", "A1"),
        "02-ai/a1/Embeddings.md": concept("c-embeddings", "Embeddings", "stub", "A1"),
        "02-ai/a1/Attention.md": concept("c-attention", "Attention", "drafted", "A1"),
        "06-builds/Measure cache locality.md": build(
            "b-measure-cache-locality", "Measure cache locality", "not started",
            ["Memory hierarchy and cache locality", "Latency numbers"]),
        "06-builds/Build a tiny GPT.md": build(
            "b-build-a-tiny-gpt", "Build a tiny GPT", "not started", ["Attention"]),
        "_tutor/progress.md": '---\nblock: "blk-01-02"\nprogram-start: "2026-11-02"\n'
                              'primary-language: "Go"\nsession-language: "English"\n---\n',
    }
    for concept_id, (box, result, probed, due) in LEDGER.items():
        files[f"_tutor/ledger/{concept_id}.md"] = (
            f"---\nconcept: {concept_id}\nbox: {box}\nlast-result: {result}\n"
            f"last-probed: {probed}\nnext-due: {due}\n---\n")
    for rel, text in files.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    os.makedirs(os.path.join(root, "_tutor/logs"), exist_ok=True)
    os.makedirs(os.path.join(root, "_tutor/templates"), exist_ok=True)
    shutil.copy(os.path.join(REPO, "_tutor/templates/progress.md"),
                os.path.join(root, "_tutor/templates/progress.md"))


class Base(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        make_kasten(self.root)
        self.k = tutor.Kasten(self.root)

    def tearDown(self):
        shutil.rmtree(self.root)

    def run_cli(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = tutor.main(["--root", self.root, "--today", TODAY.isoformat(), *args])
        return code, out.getvalue()


class Parsing(Base):
    def test_frontmatter_scalars_lists_and_comments(self):
        fm = tutor.frontmatter('---\nid: "x"\nbox: 3\nblock: "b"   # a comment\n'
                               'tags:\n  - "a"\n  - "b"\nempty: ""\n---\n')
        self.assertEqual(fm, {"id": "x", "box": 3, "block": "b", "tags": ["a", "b"], "empty": ""})

    def test_resolve_by_id_title_link_and_path(self):
        for ref in ("c-stack-vs-heap", "Stack vs heap", "[[Stack vs heap]]",
                    "01-systems/s01/Stack vs heap.md"):
            self.assertEqual(self.k.resolve(ref), "c-stack-vs-heap", ref)
        self.assertIsNone(self.k.resolve("Nope"))

    def test_the_real_kasten_parses(self):
        k = tutor.Kasten(REPO)
        self.assertEqual(len(k.of_type("concept")), 130)
        systems, ai, builds = k.block_parts("blk-01-02")
        self.assertTrue(systems and ai)
        self.assertEqual(builds, ["b-measure-cache-locality", "b-build-a-tiny-gpt"])


class Due(Base):
    def test_due_picks_exactly_on_or_before_today(self):
        due = [e["concept"] for e in self.k.due(TODAY)]
        self.assertEqual(due, ["c-system-calls", "c-latency-numbers", "c-stack-vs-heap"])

    def test_nothing_due_without_a_ledger(self):
        shutil.rmtree(os.path.join(self.root, "_tutor/ledger"))
        self.assertEqual(tutor.Kasten(self.root).due(TODAY), [])


class Plan(Base):
    def plan(self, minutes):
        return tutor.plan(self.k, "blk-01-02", minutes, TODAY)

    def test_order_revisits_then_two_systems_one_ai_then_build(self):
        p = self.plan(120)
        self.assertEqual([(s["skill"], s["ids"]) for s in p["now"]], [
            ("/revisit", ["c-system-calls", "c-latency-numbers", "c-stack-vs-heap"]),
            ("/probe", ["c-os-scheduler"]),          # the only systems candidates left:
            ("/critique", ["c-attention"]),          # due, explained and tested are skipped
            ("/build-coach", ["b-measure-cache-locality"]),
        ])
        self.assertEqual(p["now"][0]["minutes"], 6)

    def test_drafted_comes_before_stub(self):
        os.remove(os.path.join(self.root, "_tutor/ledger/c-stack-vs-heap.md"))
        p = tutor.plan(tutor.Kasten(self.root), "blk-01-02", 120, TODAY)
        self.assertEqual([s["ids"][0] for s in p["now"][1:3]], ["c-stack-vs-heap", "c-os-scheduler"])

    def test_same_order_twice(self):
        self.assertEqual(self.plan(45), self.plan(45))
        _, first = self.run_cli("plan", "--minutes", "45")
        _, second = self.run_cli("plan", "--minutes", "45")
        self.assertEqual(first, second)

    def test_short_session_keeps_order_and_defers_the_rest(self):
        p = self.plan(25)
        self.assertEqual([s["skill"] for s in p["now"]], ["/revisit"])
        self.assertEqual([s["skill"] for s in p["later"]], ["/probe", "/critique", "/build-coach"])

    def test_revisit_shrinks_to_fit(self):
        p = self.plan(4)
        self.assertEqual(p["now"][0]["ids"], ["c-system-calls", "c-latency-numbers"])
        self.assertEqual(p["later"][0]["ids"], ["c-stack-vs-heap"])

    def test_revisit_capped_at_ten_items_and_fifteen_minutes(self):
        for n in range(12):
            with open(os.path.join(self.root, f"_tutor/ledger/c-extra-{n:02}.md"), "w") as f:
                f.write(f"---\nconcept: c-extra-{n:02}\nbox: 1\nlast-result: fail\n"
                        f"last-probed: 2026-11-01\nnext-due: 2026-11-02\n---\n")
        p = tutor.plan(tutor.Kasten(self.root), "blk-01-02", 120, TODAY)
        self.assertEqual(len(p["now"][0]["ids"]), 10)
        self.assertEqual(p["now"][0]["minutes"], 15)
        self.assertEqual(p["due_total"], 15)

    def test_plan_uses_block_from_progress(self):
        code, out = self.run_cli("plan", "--minutes", "45")
        self.assertEqual(code, 0)
        self.assertIn("Plan for blk-01-02, 45 min (3 revisits due)", out)


class Progress(Base):
    def test_missing_progress_says_so(self):
        os.remove(os.path.join(self.root, "_tutor/progress.md"))
        code, out = self.run_cli("progress")
        self.assertEqual(code, 1)
        self.assertIn("missing", out)

    def test_init_progress_fills_the_template(self):
        os.remove(os.path.join(self.root, "_tutor/progress.md"))
        self.run_cli("init-progress", "--block", "blk-01-02", "--start", "2026-11-02",
                     "--language", "Français", "--primary", "Go")
        p = tutor.Kasten(self.root).progress()
        self.assertEqual((p["block"], p["program-start"], p["primary-language"], p["session-language"]),
                         ("blk-01-02", "2026-11-02", "Go", "Français"))

    def test_init_progress_never_overwrites(self):
        with self.assertRaises(SystemExit):
            self.run_cli("init-progress", "--block", "blk-01-02", "--start", "2026-11-02")


class LogPath(Base):
    def test_second_session_same_day_gets_a_suffix(self):
        _, first = self.run_cli("log-path", "probe")
        self.assertEqual(first.strip(), "_tutor/logs/2026-11-14-probe.md")
        open(os.path.join(self.root, first.strip()), "w").close()
        _, second = self.run_cli("log-path", "probe")
        self.assertEqual(second.strip(), "_tutor/logs/2026-11-14-probe-2.md")

    def test_unknown_skill_is_refused(self):
        with self.assertRaises(SystemExit):
            self.run_cli("log-path", "review")


if __name__ == "__main__":
    unittest.main(verbosity=1)
