---
id: "idx-builds"
title: "Builds — index"
type: "index"
tags:
  - "index"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# Builds — index

> Reading produces recognition; building produces knowledge. Every theme has a *build to learn* item — those are the actual curriculum. The books are reference.

19 of them. None of them are optional.

## [[S01 — The machine]]

- [[Measure cache locality]] — Write the same tight loop two ways — one cache-friendly, one not — and measure.

## [[S02 — Concurrency and time]]

- [[Hand-built bounded queue]] — Write a bounded producer-consumer queue by hand. Then break it deliberately and watch it corrupt.

## [[S03 — Networking]]

- [[Raw-socket HTTP server]] — Implement a minimal HTTP server on raw sockets. No framework. It's a weekend and it removes all the magic.

## [[S04 — Data and storage]]

- [[Index tuning on real volume]] — Load a few million rows. Write a slow query. Read the plan. Add the index. Read the plan again.

## [[S05 — Distributed systems]]

- [[Idempotent job queue]] — Build a job queue with at-least-once delivery. Make the consumer idempotent. Then kill the consumer mid-job and prove it recovers.

## [[S06 — Design and architecture]]

- [[Architecture autopsy]] — Take something you wrote a year ago. Write down every reason it's hard to change now.

## [[S07 — Security]]

- [[Attack a vulnerable app]] — Set up OWASP Juice Shop and exploit it yourself. Attacking teaches defense faster than reading does.

## [[S08 — Operations and correctness]]

- [[Instrument and break]] — Instrument something you own with traces. Then cause an incident on purpose and see if your telemetry actually tells you what happened.

## [[S09 — The toolchain]]

- [[Bisect and build from scratch]] — Break a repo deliberately five commits back, then find it with `git bisect`. Build a container from a scratch base image and understand every layer you added.

## [[S10 — Debugging and reading unfamiliar code]]

- [[Fix a real OSS bug]] — Pick an open-source project you use and fix a real bug in it. The bug is irrelevant; the navigation skill is the point.

## [[A1 — What a model actually is]]

- [[Build a tiny GPT]] — Follow Karpathy's Zero to Hero end to end and build a GPT from scratch.

## [[A2 — Inference mechanics]]

- [[Cost model for one workload]] — Build a cost model for one real workload: tokens in, tokens out, cache hit rate, dollars per request.

## [[A3 — Prompting as interface design]]

- [[One prompt as a strict contract]] — Rewrite one prompt you use regularly as a strict contract: inputs, output schema, failure behaviour.

## [[A4 — Grounding and retrieval]]

- [[A retrieval pipeline you can explain]] — Build a retrieval pipeline end to end, then document exactly where its retrieval breaks.

## [[A5 — Tools and agents]]

- [[Three-step agent with real error handling]] — Build a 3-step agent with real error handling. Measure compounding failure across the loop.

## [[A6 — Evaluation]]

- [[A 30-case eval set]] — Take any prompt you use regularly. Build a 30-case eval set. Change the prompt. Measure.

## [[A7 — Production concerns]]

- [[Attack your own agent]] — Attack your own agent with prompt injection. Then enforce one guardrail in code rather than in the prompt.

## [[A8 — Knowing where not to use it]]

- [[Replace a model call with determinism]] — Take one model call in something you've built and replace it with a deterministic solution. Compare cost, latency, and testability.

## [[A9 — The economics of intelligence]]

- [[Route by tier and measure savings]] — Route calls by difficulty tier and measure the savings. Instrument cost per request the way you'd instrument latency.
