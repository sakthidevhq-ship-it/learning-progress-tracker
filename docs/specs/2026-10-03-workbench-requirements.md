# Learning Workbench: Requirements

Date: 2026-10-03. Status: agreed.

## Problem

The current views (Atlas, Constellation, Character) motivate and show how knowledge connects, but they don't help run
the work. What's missing:

1. A **workbench**: where things are and what I'm working on.
2. A **review**: what I did over the last six weeks, so I can plan next month.
3. **Calm capture**: saving a shiny new thing must not force a decision about it.

## Principles

- **Collecting is not committing.** The library is a collection, not a backlog. Unread items are not a debt.
- **I decide priority.** The tool files, counts and dates things; it never ranks them for me.
- **No judging quality.** No per-item percentage, XP or level. Progress is counted, not estimated.
- **Coverage corrects itself.** A topic's progress is done ÷ collected. If a topic turns out deep, I add items and its
  number drops. If I ignore a topic, that shows too.

## Items

- An item is anything I might work on: a resource (paper, article, video, docs, book), a **project** or **practice**.
- Every item is filed under **area → topic**. Items without a home go to an **Unsorted** shelf.
- Items can land in the vault any way (CLI, Claude, an agent, hand-written). Anything that lands is filed or goes to Unsorted.
- **Optional fields:** my priority (empty by default), a short "why I care" note.
- **Working on an item** means three plain things:
  - add time in 30-minute steps, saved per day
  - one running notes box
  - a checklist of subtasks with checkboxes and a way to add more

  The checklist has nothing to do with planning: ticked is done. Time is optional, and done and coverage don't
  depend on it.

## States

`collected → picked up → done`, or `→ dropped` at any point after collecting.

- Every state change records its date.
- Picking up is a deliberate action, separate from doing any work.
- There's no limit on how many items are picked up at once.
- A dropped or done item can be picked up again. The new pickup date replaces the old one.

## Counting

- **Coverage** = done ÷ (collected + picked up + done), per topic, per area and overall.
- **Dropped items leave the count**, so saying "not for me" doesn't count as failing the topic.
- **Picked-up items are shown as a separate "in progress" count**, but don't add to coverage.

## Capabilities

1. **Library:** everything filed by area → topic, with the Unsorted shelf. "New" items stand out until I've looked at
   them. I can sort by area, my priority or date added. When something new arrives, I see the items I already have
   on the same topic.
2. **Workbench:** what I've picked up, with +30m, notes and a checklist on each, plus the items planned for this month that I haven't started. The library is one
   click away but off-screen.
3. **Plan (this month):** this month's items, with unfinished ones carrying over automatically. Picking something up
   adds it to the plan. Add to this month or next from the library, guided by my priority and the topic.
4. **Insights (six weeks, read-only):** time per week, learning vs building, time against career focus, stalled
   items, collected vs finished.
5. **Capture:** adding an item takes a URL or title and an optional note and priority. Pasting several lines adds
   several items (e.g. a batch of links from WhatsApp). Details are filled in later.
6. **Phone:** every tab is usable on a phone, at minimum to read.
7. **Low cognitive load:** show only what the current task needs.

## Out of scope (for now)

- Per-item progress percentages, XP, levels, unlocks and prerequisite gating.
- Rating quality or expertise.
- Limits on how many items can be active.
- A specific capture channel (phone, browser extension). Capture is anything that writes to the vault.
- A computed priority score.
