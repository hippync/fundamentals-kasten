---
name: visualize
description: Draws one verified diagram of a single idea for a Breakpoint session and embeds it in the session log, never in a note. Use when a picture would show the learner's gap faster than words during /probe, /critique, /revisit, /drill or /build-coach, or the learner asks to see it drawn.
argument-hint: "<the one idea to show>"
---

# /visualize

One idea, fewest elements, every fact verified. The diagram goes in `_tutor/viz/` and is embedded only in the session log, because the learner's notes hold only what they write. If they want it in a note, they redraw it there themselves; that's the point.

## Steps

1. **Name the idea** in one sentence: the relationship the learner's answer got wrong or couldn't produce ("each step multiplies the success rate, so 20 steps at 95% is about 36%"). If it takes two sentences, it's two diagrams; draw the one the break point needs.
2. **Verify.** List the facts the diagram will show (every number, every arrow that claims causation) and dispatch the `researcher` agent with them. Drop or correct anything it doesn't return as `supported`; an `unsourced` fact stays out of the picture.
3. **Pick the maker.**

   | Idea is about | Agent |
   |---|---|
   | steps, flow, messages over time, states and transitions | `mermaid-maker` |
   | space or scale: memory layout, cache lines, a timeline, a log axis, proportions | `svg-maker` |

4. **Draw.** Dispatch that agent with the idea, the verified facts and the base name `_tutor/viz/<YYYY-MM-DD>-<concept-id>-<slug>`. It renders, looks at the PNG and fixes it. If it returns a setup error, tell the learner the diagram needs [SETUP.md](SETUP.md), carry on without the picture, and log that.
5. **Show and embed.** Read the PNG to check it shows the idea from step 1, then point the learner at the file. In the session's log body, embed it on its own line: `![[<file name>.png|500]]` (the file name alone; Obsidian finds it in `_tutor/viz/`).

Done when the PNG exists, the researcher supported every fact in it, and the session log embeds it.
