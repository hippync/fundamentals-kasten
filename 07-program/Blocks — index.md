---
id: "idx-blocks"
title: "Blocks — index"
type: "index"
tags:
  - "index"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# Blocks — index

Two-week blocks. One systems theme paired with one AI theme, because the AI ladder rests on the systems ladder and pairing them makes the connection visible. Roughly 5–6 hours a week — sustainable beats heroic.

Process and the senior multipliers aren't blocks. They're **running practices** applied to every block: pick one XP practice per block and actually do it, and write an ADR for every block's main decision.

| ✓ | Block | Systems theme | AI theme | Deliverable |
|---|---|---|---|---|
| [ ] | [[Block 01-02 — The machine]] | The machine | What a model is | Benchmark cache-friendly vs unfriendly loops; write a tiny GPT |
| [ ] | [[Block 03-04 — The toolchain & shell]] | The toolchain & shell | Inference mechanics | `git bisect` a real break; build a container from scratch; cost model for one workload |
| [ ] | [[Block 05-06 — Concurrency]] | Concurrency | Prompting as spec | Hand-built bounded queue; one prompt rewritten as a strict contract |
| [ ] | [[Block 07-08 — Networking]] | Networking | Grounding & retrieval | Raw-socket HTTP server; a retrieval pipeline you can explain end to end |
| [ ] | [[Block 09-10 — Data & storage]] | Data & storage | Retrieval failure modes | Index tuning on millions of rows; document where your retrieval breaks |
| [ ] | [[Block 11-12 — Data, part 2 (transactions)]] | Data, part 2 (transactions) | Tools & agents | Demonstrate each isolation anomaly; a 3-step agent with real error handling |
| [ ] | [[Block 13-14 — Distributed systems]] | Distributed systems | Agent reliability | Idempotent job queue; measure compounding failure across your loop |
| [ ] | [[Block 15-16 — Distributed systems, part 2]] | Distributed systems, part 2 | Economics of intelligence | Circuit breaker + timeouts; route calls by tier and measure the savings |
| [ ] | [[Block 17-18 — Design & architecture]] | Design & architecture | Evaluation | Refactor one bad boundary; build a 30-case eval set |
| [ ] | [[Block 19-20 — Debugging & reading code]] | Debugging & reading code | Eval regression suite | Fix a real bug in an OSS project; gate prompt changes behind evals |
| [ ] | [[Block 21-22 — Security]] | Security | Prompt injection | Exploit a vulnerable app; then attack your own agent |
| [ ] | [[Block 23-24 — Operations]] | Operations | Production AI | Instrument with traces; add cost tracking, caching, fallback |
| [ ] | [[Block 25-26 — Correctness & testing]] | Correctness & testing | Guardrails & human-in-loop | Property tests on real code; enforce one guardrail in code, not prompt |
| [ ] | [[Block 27-28 — Consolidation]] | Consolidation | Consolidation | Write the doc: your architecture, its failure modes, its costs |

## Block 28 is the real exam

If you can write a document explaining a system you built — every boundary, every failure mode, every cost, every tradeoff you consciously accepted — you're done. That document *is* the fundamentals, demonstrated.

It's also your interview. Build it in your primary language and you've solved both problems at once.
