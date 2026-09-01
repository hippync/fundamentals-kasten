# The capstone

The exam is not a test you sit. It is a document you write.

**Build something real, then explain it completely.** Every boundary it crosses, every failure
mode it has, what each one costs, and every tradeoff you consciously accepted — including the
ones you got wrong and kept anyway, with the reason.

That document *is* the fundamentals, demonstrated. It is also, not coincidentally, the artifact
that does more for you in a hiring conversation than any certificate, because it is very hard
to fake and immediately obvious when it is real.

The block note in this folder — **Block 27-28 — Consolidation** — is the two-week slot for it in
the program. You do not have to wait until week 27 to start; you have to wait until you have
built something worth explaining.

## What "explaining it completely" means

Concretely, someone reading your document should be able to answer:

- Where does this system cross a boundary — process to kernel, machine to network, service to
  database, deterministic to probabilistic — and what does each crossing cost?
- What happens when each dependency is slow rather than down? (Slow is the harder case, and the
  one most designs ignore.)
- Which piece fails first under load, and how would you know before your users did?
- What did you choose *not* to build, and what would have to change for that to be wrong?
- Which numbers did you measure, and which did you assume?

If a section of that document is thin, you have found the rung to go back to. That is the
capstone working correctly — it is a diagnostic, not a graduation.
