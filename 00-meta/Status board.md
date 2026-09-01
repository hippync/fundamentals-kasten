---
id: "status-board"
title: "Status board"
type: "meta"
tags:
  - "meta"
  - "dashboard"
source-doc: "The Fundamentals Reset (Field Manual, Edition 2026)"
updated: ""
---

# Status board

The queries below are live if you have the **Dataview** plugin enabled. If you don't, ignore
them and keep the manual table — nothing else here depends on either.

## The bar

`explained` means you wrote it in your own words with the book closed. `tested` means you
predicted a failure and then caused it.

Aim for **every concept in the current block at `explained`, and the block's build at
`tested`** before moving on. Do not aim for a full kasten of `explained` — that's collecting,
and collecting is the trap.

## Everything, by status

```dataview
TABLE status, row["theme-name"] AS "Theme", updated
FROM "01-systems" OR "02-ai" OR "03-methodologies" OR "04-senior-multipliers"
WHERE type = "concept"
SORT status ASC, file.name ASC
```

## Concepts you've never touched

```dataview
LIST
FROM "01-systems" OR "02-ai" OR "03-methodologies" OR "04-senior-multipliers"
WHERE type = "concept" AND status = "stub"
```

## Concepts you claim to know but never tested by breaking something

```dataview
LIST
FROM "01-systems" OR "02-ai" OR "03-methodologies" OR "04-senior-multipliers"
WHERE status = "explained"
```

## Count by status

```dataview
TABLE length(rows) AS "Count"
FROM "01-systems" OR "02-ai" OR "03-methodologies" OR "04-senior-multipliers"
WHERE type = "concept"
GROUP BY status
```

## Builds not started

```dataview
TABLE status, row["theme-name"] AS "Theme"
FROM "06-builds"
WHERE type = "build" AND status != "done"
```

## Sources you haven't read

```dataview
TABLE author, cost, priority
FROM "05-sources"
WHERE status = "unread"
SORT priority ASC, author ASC
```

## Blocks

```dataview
TABLE status, row["theme-name"] AS "Themes"
FROM "07-program" OR "capstone"
WHERE type = "block"
SORT block ASC
```

## Manual version (no plugin)

Update the right-hand column yourself. The starting state of a fresh fork:

| Status | Target at end of cycle | Count today |
|---|---|---|
| 🌱 `stub` | 0 in completed blocks | 130 |
| 🌿 `drafted` | — | 0 |
| 🌳 `explained` | all concepts in completed blocks | 0 |
| 🔥 `tested` | every concept a build touched | 0 |

## If a query renders as plain text instead of a table

Three causes, in order of likelihood:

1. **The fence isn't tagged.** It must be exactly ` ```dataview ` on the opening line — not
   `dataview` on its own line inside a plain fence, and not nested inside a wider fence.
2. **You're in Source mode.** Dataview only executes in Reading view and Live Preview.
   `Ctrl+E` toggles.
3. **A field name has a hyphen.** `theme-name` parses as subtraction. Write `row["theme-name"]`.
   This is why the queries above look slightly awkward.

## The honest metric

Not notes written. Not blocks checked off. The metric is: **how many concepts can you predict
the failure mode for, out loud, right now?**

Everything else here is scaffolding for that number.
