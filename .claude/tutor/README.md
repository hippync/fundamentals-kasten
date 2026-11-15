# `tutor.py`: Breakpoint's bookkeeping

The skills in `.claude/skills/` ask the questions and judge the answers. `tutor.py` does the parts that must come out the same every time: which revisits are due, the order of a plan, where a session log goes. It reads the kasten and writes only to `_tutor/`, in the formats in [`_tutor/README.md`](../../_tutor/README.md#formats).

```bash
python3 .claude/tutor/tutor.py --help          # every command
python3 .claude/tutor/tutor.py plan --minutes 45
```

Every command takes `--today YYYY-MM-DD` (default: today) and `--root` (default: this repo), so a run can be replayed exactly. `.claude/settings.json` allows the script without a permission prompt.

## Running the tests

```bash
python3 .claude/tutor/test_tutor.py
```

Standard library only. Each test builds a small fixture kasten in a temp folder; one test also parses the real kasten.
