---
date: 2026-11-10
skill: probe
block: blk-01-02
concepts:
  - c-error-compounding-in-loops
result: fail
minutes: 20
---

# Probe: 2026-11-10

**Asked:** why a 95%-reliable step makes a 20-step agent loop fail most of the time.

**Where it broke:** you said the errors average out. They multiply instead: 0.95²⁰ is about 0.36, so roughly two runs in three go wrong somewhere.

**Reread:** the *How it breaks* sources for [[Error compounding in loops]]. Due again tomorrow.
