---
id: "idx-concepts"
title: "Concepts — index"
type: "index"
tags:
  - "index"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# Concepts — index

130 atomic notes. Every one starts at `status: stub`.

## [[S01 — The machine]]

- [[Latency numbers]]
- [[Memory hierarchy and cache locality]]
- [[Stack vs heap]]
- [[System calls]]
- [[The OS scheduler and blocking IO]]

## [[S02 — Concurrency and time]]

- [[Concurrency vs parallelism]]
- [[Data races]]
- [[Mutexes, semaphores, and atomics]]
- [[Event loops and blocking]]
- [[Backpressure]]
- [[Retries and retry storms]]
- [[Memory models]]
- [[Bounded queues]]

## [[S03 — Networking]]

- [[URL to first byte]]
- [[TCP handshake]]
- [[TLS handshake]]
- [[Latency vs bandwidth]]
- [[HTTP versions]]
- [[Connection pooling]]
- [[DNS]]

## [[S04 — Data and storage]]

- [[Normalization and denormalization]]
- [[B-tree indexes]]
- [[Composite indexes and the leftmost prefix]]
- [[Query plans]]
- [[ACID]]
- [[Isolation levels and anomalies]]
- [[Transaction scope]]
- [[Storage engine choices]]

## [[S05 — Distributed systems]]

- [[The eight fallacies of distributed computing]]
- [[CAP theorem]]
- [[Strong vs eventual consistency]]
- [[Exactly-once delivery]]
- [[Idempotency]]
- [[Partial failure]]
- [[Consensus and Raft]]
- [[Circuit breakers]]
- [[Bulkheads]]
- [[Timeouts]]

## [[S06 — Design and architecture]]

- [[Coupling]]
- [[Cohesion]]
- [[Deep vs shallow interfaces]]
- [[Dependency direction]]
- [[Module boundaries]]
- [[Microservices]]
- [[Essential vs accidental complexity]]

## [[S07 — Security]]

- [[Threat modeling]]
- [[Authentication vs authorization]]
- [[OWASP Top 10]]
- [[Parameterized queries]]
- [[Secrets management]]
- [[Supply chain security]]

## [[S08 — Operations and correctness]]

- [[Logs, metrics, and traces]]
- [[SLOs]]
- [[Rollback procedures]]
- [[The test pyramid]]
- [[Property-based testing]]
- [[Invariants]]

## [[S09 — The toolchain]]

- [[The Unix philosophy]]
- [[Shell composition]]
- [[Git objects and the commit DAG]]
- [[Rebase vs merge]]
- [[git bisect]]
- [[Containers]]
- [[The path from push to production]]

## [[S10 — Debugging and reading unfamiliar code]]

- [[Debugging as the scientific method]]
- [[Bisecting in space and time]]
- [[Reading a stack trace]]
- [[Entering an unfamiliar codebase]]
- [[Debugger vs logging vs profiler vs packet capture]]
- [[Heisenbugs]]

## [[A1 — What a model actually is]]

- [[Tokens and tokenization]]
- [[Embeddings]]
- [[Attention]]
- [[The transformer block]]
- [[Training vs fine-tuning vs inference]]
- [[Next-token prediction]]

## [[A2 — Inference mechanics]]

- [[The context window]]
- [[KV cache]]
- [[Prompt caching]]
- [[Temperature and sampling]]
- [[Time to first token vs tokens per second]]
- [[Model non-determinism]]

## [[A3 — Prompting as interface design]]

- [[Prompting as specification]]
- [[Task decomposition]]
- [[Examples vs instructions]]
- [[Structured output]]
- [[Loud vs silent failure]]

## [[A4 — Grounding and retrieval]]

- [[Grounding]]
- [[Vector search]]
- [[Retrieval failure modes]]
- [[Chunking strategy]]
- [[Hybrid search]]

## [[A5 — Tools and agents]]

- [[What an agent actually is]]
- [[Tool calling at the protocol level]]
- [[Error compounding in loops]]
- [[Agent state]]
- [[Stopping conditions]]

## [[A6 — Evaluation]]

- [[Golden datasets]]
- [[What to measure in an eval]]
- [[LLM as judge]]
- [[Prompt regression testing]]
- [[Evaluating a system, not a model]]

## [[A7 — Production concerns]]

- [[Cost per request]]
- [[Model fallback]]
- [[Prompt injection]]
- [[Human in the loop]]
- [[Guardrails in code]]

## [[A8 — Knowing where not to use it]]

- [[The determinism boundary]]

## [[A9 — The economics of intelligence]]

- [[Jevons paradox in AI]]
- [[Market bifurcation]]
- [[Model tiering as architecture]]
- [[Cache hit rate]]
- [[Provider portability]]

## [[P — Process]]

- [[Waterfall]]
- [[Agile]]
- [[Scrum]]
- [[Kanban]]
- [[Extreme Programming]]
- [[Lean]]
- [[WIP limits]]
- [[TDD as specification]]
- [[Refactoring]]
- [[Continuous integration]]
- [[Pair programming with a model]]
- [[YAGNI and small releases]]
- [[Cheap to generate, expensive to own]]

## [[M — The senior multipliers]]

- [[Writing as engineering]]
- [[Architecture decision records]]
- [[Estimation and tradeoff articulation]]
- [[Saying no with a reason]]
