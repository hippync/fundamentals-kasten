---
id: "idx-questions"
title: "Questions — index"
type: "index"
tags:
  - "index"
  - "recall"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# Questions — index

Every "answer these" question in the manual, in one place. This is the recall drill.

**How to use it:** pick a theme, close the vault, answer out loud. Anything you fumble, open the concept note and move its status back. The manual's rule — *if you can't explain it in a paragraph without the source open, you don't have it yet* — applies here first.

For a real drill, hand this list to a model and say *"quiz me on these, one at a time, don't give me the answers."*

## [[S01 — The machine]]

- [ ] What's the actual cost difference between a CPU cycle, an L1 cache hit, a RAM access, an SSD read, and a network round trip? (Orders of magnitude, not numbers.)
- [ ] Stack vs heap: what determines which one your data lands in, and why do you care?
- [ ] What is a system call, and why is it expensive?
- [ ] What does the OS scheduler do when your thread blocks on I/O?
- [ ] Why is iterating an array faster than iterating a linked list of the same size?

## [[S02 — Concurrency and time]]

- [ ] Concurrency vs parallelism — what's the actual distinction?
- [ ] What is a data race, and why can't tests reliably catch one?
- [ ] Mutex, semaphore, atomic operation — when does each apply?
- [ ] What is an event loop, and why is blocking inside one catastrophic?
- [ ] What is backpressure, and what happens to a system that has none?
- [ ] Why is 'just add a retry' often how you turn a small outage into a large one?

## [[S03 — Networking]]

- [ ] What actually happens between typing a URL and the first byte arriving? Every step.
- [ ] TCP handshake, TLS handshake — how many round trips before any data moves?
- [ ] Latency vs bandwidth: which one do you fix by upgrading the connection? (Trick question.)
- [ ] HTTP/1.1 vs 2 vs 3 — what problem did each one solve?
- [ ] What is connection pooling actually pooling, and what breaks without it?
- [ ] Why is DNS the answer to so many outages?

## [[S04 — Data and storage]]

- [ ] Normalization: what problems does it solve, and when do you deliberately denormalize?
- [ ] How does a B-tree index work well enough to predict which queries it helps and which it doesn't?
- [ ] Why does a composite index on (a, b) help `WHERE a = ? AND b = ?` but not `WHERE b = ?`
- [ ] Read a query plan. Explain why the planner made that choice.
- [ ] ACID: define each letter precisely. Then define the isolation levels and what anomaly each one permits.
- [ ] What does a transaction actually hold, and for how long, and what does that do to concurrency?
- [ ] When is a document store, key-value store, or column store genuinely the right call — and when is it fashion?

## [[S05 — Distributed systems]]

- [ ] The eight fallacies of distributed computing — can you name the failures each one causes?
- [ ] CAP: what it actually says, and why the popular summary is misleading.
- [ ] Strong vs eventual consistency: what does each cost the user, and the developer?
- [ ] Why is exactly-once delivery impossible, and what do people mean when they claim it?
- [ ] What is idempotency, and why is it the single most important property in any retry-capable system?
- [ ] What is a partial failure, and why is it harder than total failure?

## [[S06 — Design and architecture]]

- [ ] Coupling and cohesion — can you point at real code and say precisely which kind of coupling it has?
- [ ] What makes an interface deep vs shallow? Why does depth matter?
- [ ] Which direction should dependencies point, and why?
- [ ] When does a module boundary belong in the code vs across a network?
- [ ] Microservices solve an organizational problem before a technical one — do you have that problem?
- [ ] What's the difference between essential and accidental complexity in your current codebase?

## [[S07 — Security]]

- [ ] Threat modeling: what are you protecting, from whom, and what's the attack surface?
- [ ] AuthN vs AuthZ — and why is authorization the one that actually gets breached?
- [ ] The OWASP Top 10 — for each, the mechanism and the mitigation.
- [ ] Why do parameterized queries work? (Not 'they escape input' — the real reason.)
- [ ] How do secrets get into and out of a system safely?
- [ ] Supply chain: what is your actual dependency tree, and who can push to it?

## [[S08 — Operations and correctness]]

- [ ] Logs, metrics, traces — what question does each one answer that the others can't?
- [ ] What's an SLO, and how does it turn into an engineering decision?
- [ ] What does your rollback procedure look like, and have you actually run it?
- [ ] The test pyramid: what's the right shape, and why do most codebases get it upside down?
- [ ] What's a property-based test, and when is it stronger than example-based testing?
- [ ] What invariants does your system have, and are any of them enforced by the type system?

## [[S09 — The toolchain]]

- [ ] The Unix philosophy: small composable tools, text streams, pipes. Why has this design survived fifty years?
- [ ] Enough shell to be dangerous: pipes, redirection, `grep` / `sed` / `awk` / `find` / `xargs`. Not memorized — composable.
- [ ] Git: what is a commit? (A content-addressed snapshot in a directed acyclic graph. Once you see that, rebase vs merge stops being scary.)
- [ ] `git bisect` — do you know it exists? It finds the breaking commit in log(n) steps and most people have never run it.
- [ ] What is a container, actually? (Namespaces + cgroups + a filesystem layer. Not a VM.)
- [ ] What happens between `git push` and running code in production? Every step.

## [[S10 — Debugging and reading unfamiliar code]]

- [ ] Debugging is the scientific method: observe → hypothesize → design the minimal experiment → test → repeat. Can you name the hypothesis you're currently testing? If not, you're guessing.
- [ ] How do you bisect a problem in space (which component) as well as in time (which change)?
- [ ] Can you read a stack trace all the way down and say what each frame was doing?
- [ ] What's your strategy for entering a 200k-line codebase you've never seen?
- [ ] When do you reach for a debugger vs logging vs a profiler vs a packet capture?
- [ ] What's a heisenbug, and what does its existence tell you about the system?

## [[A1 — What a model actually is]]

- [ ] What is a token, and why does tokenization explain so much weird model behavior?
- [ ] What is an embedding, and what does 'similar' mean in that space?
- [ ] Attention, at block-diagram level: what is a transformer doing when it processes a sequence?
- [ ] Training vs fine-tuning vs inference — what changes in each?
- [ ] Why is a model fundamentally a next-token predictor, and what does that imply about its failure modes?

## [[A2 — Inference mechanics]]

- [ ] What is the context window, physically? Why does cost scale the way it does with it?
- [ ] What is a KV cache, and why does it make prompt caching possible?
- [ ] Temperature and sampling: what are you actually adjusting?
- [ ] Where does latency come from — time to first token vs tokens per second — and which does your use case care about?
- [ ] Why is the same prompt not guaranteed to give the same output, and when does that matter?

## [[A3 — Prompting as interface design]]

- [ ] Why does decomposing a task into steps beat asking for the whole thing?
- [ ] When do examples outperform instructions, and vice versa?
- [ ] How do you constrain output format so downstream code can rely on it?
- [ ] What's the difference between a prompt that fails loudly and one that fails silently? (The second is the dangerous one.)

## [[A4 — Grounding and retrieval]]

- [ ] Why does a model need external grounding at all?
- [ ] Vector search: what is it doing, and where does it fail? (Hint: exact terms, negation, recency.)
- [ ] Chunking strategy — why does it dominate retrieval quality?
- [ ] When is hybrid search (keyword + vector) the right answer?
- [ ] Why is retrieval quality usually a bigger lever than model choice?

## [[A5 — Tools and agents]]

- [ ] What is function/tool calling actually doing at the protocol level?
- [ ] In a multi-step loop, how do errors compound? (If each step is 95% reliable, what's a 10-step chain?)
- [ ] Where does state live between steps, and what happens when a step fails halfway?
- [ ] What's your stopping condition, and what happens without one?
- [ ] Which tasks genuinely need a loop, and which are one call with better prompting?

## [[A6 — Evaluation]]

- [ ] What's your golden dataset, and how did you build it?
- [ ] What are you measuring — correctness, format compliance, latency, cost, refusal rate?
- [ ] When is LLM-as-judge valid, and what are its biases?
- [ ] How do you catch a regression when you change a prompt? (You have a test suite for code. Where's the one for prompts?)
- [ ] How do you evaluate a system, not a model, given that the model is one component?

## [[A7 — Production concerns]]

- [ ] What's your cost per request, and what's the biggest term in that equation?
- [ ] What's your fallback when the model API is down or slow?
- [ ] Prompt injection — why is it structurally the SQL injection of this decade, and why is it harder to fix?
- [ ] Where do you need a human in the loop, and what does the interface for that look like?
- [ ] What are your guardrails, and are they enforced in code or hoped for in the prompt? (Only one of those is real.)

## [[A8 — Knowing where not to use it]]

- [ ] Is this problem genuinely fuzzy, or am I reaching for a model because it's available?
- [ ] What would the deterministic version cost to build, and what would it cost to run?
- [ ] Can I test and debug the solution I'm proposing?

## [[A9 — The economics of intelligence]]

- [ ] What is your cost per user task, and which call in the chain dominates it?
- [ ] Which of your calls could be served by a model 20x cheaper with no quality loss? Have you tested, or assumed?
- [ ] What's your caching hit rate, and what would it be with better prompt structure?
- [ ] If your provider tripled prices tomorrow, what breaks, and how portable are you?

## [[P — Process]]

- [ ] Which of the six is a values statement, which is a management framework, which is a set of engineering practices, and which is a manufacturing philosophy?
- [ ] Why does 'we're Agile' so often mean 'we have standups'?
- [ ] Why does XP become the most relevant methodology on the list in the AI era, not the least?
- [ ] Why does a WIP limit become a survival tool when starting things is trivially fast?
- [ ] Why does Scrum age worst when typing time stops being the variable?
- [ ] What is the new waste category Lean gains?

## [[M — The senior multipliers]]

- [ ] Can I write an unambiguous spec for the thing I'm about to build?
- [ ] What are the three options, what does each cost, what does each buy, and which risk are we accepting?
- [ ] Do I understand the problem well enough to know the proposed solution doesn't address it?
