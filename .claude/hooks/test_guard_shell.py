#!/usr/bin/env python3
"""Tests for guard_shell.py. Each test runs a real shell command between the
PreToolUse and PostToolUse events, in a throwaway kasten. Standard library only.

    python3 .claude/hooks/test_guard_shell.py
"""
import json, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(HERE, "guard_shell.py")
FIX = os.path.join(HERE, "fixtures")
OW = "## In my own words\n"


class Shell(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.root, "02-ai"))
        os.makedirs(os.path.join(self.root, "06-builds"))
        self.rel = os.path.join("02-ai", "Error compounding in loops.md")
        self.note = os.path.join(self.root, self.rel)
        shutil.copy(os.path.join(FIX, "concept.md"), self.note)
        shutil.copy(os.path.join(FIX, "build.md"), os.path.join(self.root, "06-builds", "A 30-case eval set.md"))
        self.text = self.read(self.note)

    def tearDown(self):
        shutil.rmtree(self.root)

    def read(self, p):
        with open(p, encoding="utf-8") as f:
            return f.read()

    def hook(self, phase):
        event = {"hook_event_name": phase, "tool_name": "Bash", "session_id": "s",
                 "tool_use_id": self.id(), "tool_input": {"command": "…"}}
        p = subprocess.run([sys.executable, HOOK], input=json.dumps(event), capture_output=True,
                           text=True, env={**os.environ, "CLAUDE_PROJECT_DIR": self.root})
        return p.returncode, p.stderr

    def bash(self, command):
        self.assertEqual(self.hook("PreToolUse")[0], 0)
        subprocess.run(command, shell=True, cwd=self.root, check=True)
        return self.hook("PostToolUse")

    def backups(self):
        d = os.path.join(self.root, "_tutor", "guard")
        return os.listdir(d) if os.path.isdir(d) else []

    # --- put back --------------------------------------------------------------

    def test_python_write_into_own_words_is_undone(self):
        code, err = self.bash(f"""python3 -c "
p='{self.rel}'; t=open(p).read(); open(p,'w').write(t.replace('{OW.strip()}', '{OW.strip()}\\\\nAI text', 1))" """)
        self.assertEqual(code, 2)
        self.assertIn("Rule 1", err)
        self.assertEqual(self.read(self.note), self.text)
        self.assertEqual(len(self.backups()), 1)
        self.assertIn("AI text", self.read(os.path.join(self.root, "_tutor", "guard", self.backups()[0])))

    def test_echo_into_build_section_is_undone(self):
        build = os.path.join(self.root, "06-builds", "A 30-case eval set.md")
        before = self.read(build)
        code, _ = self.bash("printf '%s' \"$(sed 's/^## What I got wrong$/## What I got wrong\\nAI post-mortem/' "
                            "'06-builds/A 30-case eval set.md')\" > b.tmp && mv b.tmp '06-builds/A 30-case eval set.md'")
        self.assertEqual(code, 2)
        self.assertEqual(self.read(build).rstrip("\n"), before.rstrip("\n"))

    def test_mv_over_the_note_is_undone(self):
        filled = self.text.replace(OW, OW + "AI text\n", 1)
        draft = os.path.join(self.root, "draft.txt")
        with open(draft, "w", encoding="utf-8") as f:
            f.write(filled)
        code, _ = self.bash(f"mv draft.txt '{self.rel}'")
        self.assertEqual(code, 2)
        self.assertEqual(self.read(self.note), self.text)

    def test_type_flip_is_undone(self):
        code, err = self.bash(f"""python3 -c "
p='{self.rel}'; t=open(p).read(); open(p,'w').write(t.replace('type: \\"concept\\"', 'type: \\"x\\"'))" """)
        self.assertEqual(code, 2)
        self.assertIn("type", err)
        self.assertEqual(self.read(self.note), self.text)

    def test_deleted_note_is_restored(self):
        code, _ = self.bash(f"rm '{self.rel}'")
        self.assertEqual(code, 2)
        self.assertEqual(self.read(self.note), self.text)

    def test_new_note_with_filled_section_is_removed(self):
        filled = self.text.replace(OW, OW + "AI text\n", 1)
        src = os.path.join(self.root, "src.txt")
        with open(src, "w", encoding="utf-8") as f:
            f.write(filled)
        code, _ = self.bash("cp src.txt '02-ai/New concept.md'")
        self.assertEqual(code, 2)
        self.assertFalse(os.path.exists(os.path.join(self.root, "02-ai", "New concept.md")))
        self.assertEqual(len(self.backups()), 1)

    # --- left alone ------------------------------------------------------------

    def test_status_change_passes(self):
        code, err = self.bash(f"""python3 -c "
p='{self.rel}'; t=open(p).read(); open(p,'w').write(t.replace('status: \\"stub\\"', 'status: \\"drafted\\"'))" """)
        self.assertEqual(code, 0, err)
        self.assertIn('status: "drafted"', self.read(self.note))

    def test_append_to_unprotected_last_section_passes(self):
        # The build note ends on Concepts this touched, which Claude may edit.
        code, err = self.bash("echo '- [[Idempotency]]' >> '06-builds/A 30-case eval set.md'")
        self.assertEqual(code, 0, err)

    def test_new_blank_note_passes(self):
        code, err = self.bash(f"cp '{self.rel}' '02-ai/Copy.md'")
        self.assertEqual(code, 0, err)

    def test_command_outside_the_notes_passes(self):
        code, err = self.bash("echo hi > scratch.txt")
        self.assertEqual(code, 0, err)
        self.assertEqual(self.backups(), [])

    def test_post_without_snapshot_passes(self):
        self.assertEqual(self.hook("PostToolUse")[0], 0)


if __name__ == "__main__":
    unittest.main(verbosity=1)
