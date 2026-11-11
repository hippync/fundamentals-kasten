#!/usr/bin/env python3
"""Tests for guard_own_words.py. Standard library only.

    python3 .claude/hooks/test_guard_own_words.py
"""
import json, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(HERE, "guard_own_words.py")
FIX = os.path.join(HERE, "fixtures")

PREDICT_PLACEHOLDER = ("> *What breaks when this is absent, wrong, or misunderstood? One sentence, "
                       "written by you. Until this line exists, the concept is not yours.*")
OWN_WORDS_PLACEHOLDER = "<!-- Closed book. One paragraph. If you can't, status stays 'drafted'. -->"


def run(tool, path, **tool_input):
    event = {"tool_name": tool, "tool_input": {"file_path": path, **tool_input}}
    p = subprocess.run([sys.executable, HOOK], input=json.dumps(event),
                       capture_output=True, text=True)
    return p.returncode, p.stderr


class Guard(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.concept = os.path.join(self.dir, "Error compounding in loops.md")
        self.build = os.path.join(self.dir, "A 30-case eval set.md")
        shutil.copy(os.path.join(FIX, "concept.md"), self.concept)
        shutil.copy(os.path.join(FIX, "build.md"), self.build)
        with open(self.concept, encoding="utf-8") as f:
            self.text = f.read()

    def tearDown(self):
        shutil.rmtree(self.dir)

    def allowed(self, *a, **k):
        code, err = run(*a, **k)
        self.assertEqual(code, 0, err)

    def blocked(self, *a, **k):
        code, err = run(*a, **k)
        self.assertEqual(code, 2, "expected the guard to block this")
        self.assertIn("Rule 1", err)
        return err

    # --- allowed -------------------------------------------------------------

    def test_status_change(self):
        self.allowed("Edit", self.concept, old_string='status: "stub"', new_string='status: "drafted"')

    def test_tag_added(self):
        self.allowed("Edit", self.concept, old_string='  - "reliability"',
                     new_string='  - "reliability"\n  - "reread"')

    def test_related_link_added(self):
        self.allowed("Edit", self.concept, old_string="- [[Backpressure]]",
                     new_string="- [[Backpressure]]\n- [[Idempotency]]")

    def test_unprotected_section(self):
        self.allowed("Edit", self.concept, old_string="- [ ] In a multi-step loop, how do errors compound?",
                     new_string="- [x] In a multi-step loop, how do errors compound?")

    def test_full_write_leaving_sections_alone(self):
        self.allowed("Write", self.concept, content=self.text.replace('"stub"', '"drafted"'))

    def test_other_file(self):
        path = os.path.join(self.dir, "notes.txt")
        self.allowed("Write", path, content="anything")

    def test_non_note_markdown(self):
        path = os.path.join(self.dir, "README.md")
        self.allowed("Write", path, content="# Readme\n\n## In my own words\n\nfree text here\n")

    def test_new_concept_with_blank_sections(self):
        path = os.path.join(self.dir, "New concept.md")
        self.allowed("Write", path, content=self.text)

    def test_build_concepts_touched(self):
        self.allowed("Edit", self.build, old_string="- [[Golden datasets]]",
                     new_string="- [[Golden datasets]]\n- [[Overfitting to the eval]]")

    def test_edit_that_does_not_apply(self):
        self.allowed("Edit", self.concept, old_string="text that is not there", new_string="x")

    # --- blocked -------------------------------------------------------------

    def test_edit_inside_own_words(self):
        err = self.blocked("Edit", self.concept, old_string=OWN_WORDS_PLACEHOLDER,
                           new_string="Errors multiply: 0.95 to the 10th is about 0.6.")
        self.assertIn("In my own words", err)

    def test_edit_predict_the_failure(self):
        err = self.blocked("Edit", self.concept, old_string=PREDICT_PLACEHOLDER,
                           new_string="> A 20-step agent at 95% per step fails two runs in three.")
        self.assertIn("Predict the failure", err)

    def test_edit_what_it_is(self):
        self.blocked("Edit", self.concept, old_string="## What it is\n",
                     new_string="## What it is\n\nReliability multiplies across steps.\n")

    def test_edit_how_it_breaks(self):
        self.blocked("Edit", self.concept, old_string="## How it breaks\n",
                     new_string="## How it breaks\n\nLong loops fail silently.\n")

    def test_delete_protected_heading(self):
        self.blocked("Edit", self.concept, old_string="## In my own words\n", new_string="")

    def test_full_write_changing_section(self):
        self.blocked("Write", self.concept,
                     content=self.text.replace(OWN_WORDS_PLACEHOLDER, "A model answer."))

    def test_multiedit_touching_both(self):
        err = self.blocked("MultiEdit", self.concept, edits=[
            {"old_string": 'status: "stub"', "new_string": 'status: "explained"'},
            {"old_string": PREDICT_PLACEHOLDER, "new_string": "> Loops amplify small error rates."},
            {"old_string": OWN_WORDS_PLACEHOLDER, "new_string": "A model answer."},
        ])
        self.assertIn("Predict the failure", err)
        self.assertIn("In my own words", err)

    def test_replace_all_reaching_a_section(self):
        self.blocked("Edit", self.concept, old_string="<!--", new_string="<!-- edited", replace_all=True)

    def test_new_concept_with_filled_section(self):
        path = os.path.join(self.dir, "New concept.md")
        self.blocked("Write", path, content=self.text.replace(OWN_WORDS_PLACEHOLDER, "A model answer."))

    def test_build_learner_sections(self):
        for head in ("## Plan\n", "## The failure I'm going to cause on purpose\n",
                     "## What actually happened\n", "## What I got wrong\n"):
            with self.subTest(head=head):
                self.blocked("Edit", self.build, old_string=head, new_string=head + "\nFilled in.\n")

    def test_garbage_input_fails_closed(self):
        p = subprocess.run([sys.executable, HOOK], input="not json", capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
