# Learning Workbench: Design

Date: 2026-10-03. Implements `2026-10-03-workbench-requirements.md`.

## Summary

- Keep the vault as markdown pages with `key:: value` properties. State and dates live **on each item page**, with no
  separate log.
- Replace progress percentages, the computed priority score and XP with: a state, a date per state, and optional
  priority, note, time and plan fields.
- Build one new view, `ui/workbench.html`, with four tabs: **Workbench**, **Plan**, **Library** and **Insights**. It replaces
  Atlas, Constellation and Character as the home page.
- Capture writes a page straight into the vault. Claude fills in the details later.

## 1. Data model

### Item properties

| Property | Values | Notes |
|---|---|---|
| `type::` | paper, article, video, docs, tweet, **project**, **practice** | project and practice are new |
| `domain::`, `topic::` | `[[Area]]`, `[[Topic]]` | missing or `[[Unsorted]]` → Unsorted shelf |
| `state::` | `collected`, `picked`, `done`, `dropped` | replaces `status::` and `progress::` |
| `ingested::` | `[[YYYY-MM-DD]]` | the collected date (existing property, kept) |
| `picked::` | `[[YYYY-MM-DD]]` | set by pick |
| `done::` | `[[YYYY-MM-DD]]` | set by done |
| `dropped::` | `[[YYYY-MM-DD]]` | set by drop |
| `my-priority::` | `now`, `soon`, `someday` | optional, only ever set by me |
| `note::` | free text | optional "why I care" |
| `planned::` | `[[YYYY-MM]]` | optional: the month it was first planned for. Unfinished items carry over (see Plan) |
| `enrich::` | `pending` | set by quick capture until Claude fills the details |

Working on an item adds three plain sections to its page:

```
## Notes
Single binary, 3 nodes on localhost, tokio for networking.
Read half of §5, stopped at 5.4.1.

## Checklist
- [x] Leader election with 3 nodes
- [ ] Log replication
- [ ] Read 2-3 other Rust Raft implementations

## Time
- 2026-10-02 · 1h30m
- 2026-10-03 · 1h
```

- **Notes** is free text that you keep editing. It's one running note per item, not one per session. Existing
  `## My Notes` sections become `## Notes`.
- **Checklist** is a plain markdown checklist. A ticked item is done, with no dates and no link to planning. Moving a
  subtask anywhere else is up to you.
- **Time** has one line per day. **+30m** adds to today's line and **−30m** takes it back off. Total time, "last worked"
  and the Insights tab are worked out from these lines. Adding time to a collected item picks it up.

Everything else on a page stays as it is: `concepts::`, `source::`, summary, takeaways, notes. Concept, domain and topic
stub pages aren't items. Concepts are only used to find similar items.

### Rules

- **pick:** `state=picked`, set `picked::` to today, clear `done::` and `dropped::`. Re-picking overwrites the earlier
  pickup date. The history of earlier attempts isn't kept, which is acceptable for now.
- **done:** `state=done`, set `done::`. Sets `picked::` to the same day if it was never picked.
- **drop:** `state=dropped`, set `dropped::`.
- **collect** (put back): `state=collected`, clear `picked::`, `done::` and `dropped::`.
- **Counting:** coverage = done ÷ (collected + picked + done). Dropped items are excluded, and picked items appear as
  their own "in progress" count.
- **Coverage on any past day** can be worked out from the dates alone. Count the items collected by that day, minus
  those dropped by then, and the done items among them. That's what lets the review show how coverage moved
  without storing any history.

### Why it all lives on the item page

One file per item, holding its dates, notes, checklist and time, holds up to items written by hand, by agents or by
Claude, and is easy to review in git. Insights reads the `## Time` lines from every page.

## 2. CLI

| Command | Effect |
|---|---|
| `lpt add <url-or-title>... [--note "..."] [--type project] [--prio now\|soon\|someday]` | writes one page per argument (or per stdin line) into Unsorted, `enrich=pending` |
| `lpt pick "Title"` | pick up |
| `lpt done "Title"` | finish |
| `lpt drop "Title"` | drop |
| `lpt back "Title"` | put back: not started, stays in the plan |
| `lpt time "Title" [+30m\|-30m\|1h]` | adds to or removes from today's line in `## Time` (default +30m) |
| `lpt check "Title" "text"` / `lpt check "Title" --toggle N` | adds a checklist item / ticks or unticks one |
| `lpt note "Title" "text"` | appends a line to `## Notes` |
| `lpt plan "Title" [--month 2026-11]` / `lpt unplan "Title"` | defaults to next month |
| `lpt prio "Title" now\|soon\|someday\|none` | my priority |
| `lpt enrich` / `lpt enrich <id> --from result.json` | lists items waiting to be filed / files one (renames the file to its title) |
| `lpt show "Title"`, `lpt ls`, `lpt status` | one item / in progress and this month's plan / counts |
| `lpt migrate` | one-off conversion of the old properties (see §5) |
| `lpt graph`, `lpt serve` | build site/ and open it read-only, or serve the app with editing |

**Retired:** `progress` (replaced by pick/done), `recompute`, `cli/priority.py` and `cli/levels.py`. The two-step
inbox → `result.json` → `write` flow is replaced by direct writes plus `enrich`. The `processed/` folder is no longer used.

**Server API** (`lpt serve`):
- `GET /api/items`: every item, fresh from disk. The page loads it on start; if it fails, the page is read-only.
- `POST /api/item {id, action, ...}` with action pick, done, drop, back, time, check_add, check_toggle, check_remove,
  notes, prio or plan. Returns the updated item.
- `POST /api/add {text, note, type, prio}`: one item per line.
- The Host header must be local (blocks DNS rebinding).
- Same localhost-only and same-origin checks as today.
- Opened as a plain file, the buttons copy the matching command, as they do now.

**Claude's job when filling details** (`CLAUDE.md` gets updated): for each pending item, fill in title, summary, type,
area, topic and concepts using existing names where possible, then clear `enrich`. If an item doesn't fit, leave it
in Unsorted rather than inventing a new area.

## 3. The view: `ui/workbench.html`

The style is calm and dense, built for reading: dark by default, one accent colour per area, no game elements. The
shared `core.js` is cut down to the new model: states, dates, coverage, the week windows and similar items.

### Workbench tab (opens here)

The evening flow: open it, see what's in progress, continue one for an hour or two (adding time, notes and subtasks),
or pick the next one if it's done. Save anything that comes up for later, then close.

- **In progress:** cards, most recently worked first. Each shows area · topic, total and today's time, the checklist
  count, the latest line of the notes and days since last worked. Its only button is **+30m**; tap the card to open it.
- **Up next:** the not-started items in this month's plan, in priority order, each with **Pick up**.
- **Opening an item:**
  - **Done / Put back / Drop**, with a priority chip on the right
  - a work panel: time box (−30m / +30m), notes, checklist, and "+ Save something for later to the library"
  - for not-started items: **+ October plan / + November plan**, the source link, and items on the same topic
- **Not shown,** to keep things light: the plan month, the state timeline, and stats beyond "time this week".

### Add (from any tab)

- A text box for a link or title. **Several lines add several items,** for pasting a batch collected in WhatsApp,
  from tweets or from conversations.
- An optional "why I care" note, a type (resource / project / practice) and a priority.
- Everything lands in Unsorted. Claude files each item into an area and topic later.

### Phone

- On a phone the tabs move to a bottom tab bar, and **+** stays in the header.
- Every tab works one column wide. The item panel opens full screen, so time, notes and the checklist can be used on
  the go. Extra columns (dates, plan buttons, side stats) are hidden.

### Library tab

```
 Unsorted · 2                                                   [File with Claude]
   https://arxiv.org/abs/2410.xxxxx  "saw on X, MoE routing"     added today  NEW

 ML Infrastructure       ███████░░░░░░░░  3/21 done · 1 in progress
   ▸ Inference Optimization   1/6  ·  KV Cache Design 0/4  ·  LLM Serving 2/5 …
 Systems                 ██░░░░░░░░░░░░░  1/23 done · 1 in progress
   ▾ Distributed Consensus  0/3 · 1 in progress
       Raft: In Search of an Understandable…   paper   collected 9 Jul   soon
       Build a toy Raft in Rust                project picked 28 Sep
       Paxos Made Simple                       paper   collected 9 Jul   NEW
```

- Areas, then topics, then items, each with a coverage bar and counts.
- Within each topic, items are ordered in-progress first, then by **my priority** (now / soon / someday, then none).
- Each row has a priority chip (click to cycle it). Hovering a row shows **+ Oct / + Nov**, or a tag if the item is already planned.
- Sort by area, my priority or date added. Filter by state, type and search.
- **NEW** marks items added since I last opened this tab. That's stored in the browser, so nothing in the vault changes.
- Clicking an item opens a side panel: summary, note, source link, the actions, "My priority", "Plan for…", and
  **"Already in your library on this topic"**: items sharing the topic or two or more concepts, with their states.
  That panel is where "should I pick this up?" gets answered.

### Plan tab: this month only

- **This month's plan:** everything planned for this month or earlier that isn't finished, plus items finished this
  month. **Unfinished items carry over automatically** and get a small "from Sep" tag. Nothing has to be decided at
  the month boundary.
- Grouped as **In progress**, **Not started** (in priority order, each with **Remove**) and **Done**.
- **Picking an item up adds it to this month's plan,** so there's no separate "unplanned" list.
- **Next month:** items added with "+ Nov". They join the plan on the 1st.
- **How much fits:** items finished in each of the last two months next to the open items in this plan.
- **Add from library:** grouped by priority (Now / Soon / Someday), each with **+ Oct / + Nov**.

### Insights tab: six weeks, read-only

- **Four plain-sentence insights** from the data, not judgements: the biggest share of time, how much time went to
  the top career focus, the building share, and collected vs finished.
- **Time per week:** hours as bars split by area, a thin line for the share spent building, and what was finished
  that week.
- **Learning vs building:** hours on resources against projects and practice.
- **Stalled:** items picked up with no session in 14+ days.
- **Direction:** areas in order of career focus (the weights in `config.yaml`), each with share of time, items
  finished and coverage (with its change).
- A note when finished items have no time logged, since the time figures will undercount.

## 4. What happens to the existing views

- `index.html` (the picker) and the Atlas, Constellation and Character views are **removed**. They're built on
  progress percentages, XP and unlocks, which are now out of scope. The workbench becomes `site/index.html`.
- The classic Map and Skill Tree are removed too. The Map's "what's related" job moves to the library side panel.
- Deploy is unchanged: push to `main` builds `_site/` and publishes it.

## 5. Migration (`lpt migrate`, one run, committed as one change)

**Every item starts as `collected` (not started),** including the 2 done and 2 in-progress ones, so October can be
planned from a clean slate.

- Remove `status::`, `progress::`, `priority::`, `started::` and `completed::`.
- Rename `## My Notes` to `## Notes`.
- Concept and topic stub pages keep `status:: stub` and lose `priority::`.

## 6. Build order

1. **Model and CLI:** state functions, the new commands, migration, and tests for the date rules and counting.
2. **Capture:** `add` writes pages directly, `enrich` lists pending items, `CLAUDE.md` gets the filing rules.
3. **`core.js`:** the new model, coverage on any past day, week windows, similar items.
4. **Workbench view:** the three tabs, the API endpoints, and the copy-command fallback for file mode.
5. **Remove the old views,** and update deploy and `CLAUDE.md`.
6. **Check:** screenshots on desktop and phone, and a full run through `lpt serve` against a copy of the vault.

## Open choices

- "New" tracking is per browser, not stored in the vault.
