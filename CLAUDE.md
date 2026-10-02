# Learning Workbench

A CLI (`lpt`) and a web app for a personal learning library: collect things, pick them up, log time, keep notes and
checklists, plan the month, look back over six weeks. Everything is stored as markdown in `vault/pages/`.
GitHub Pages serves a read-only copy: pushing to `main` rebuilds it when `vault/pages/`, `graph.html` or
`cli/build_graph.py` change (the workflow runs `cli/build_graph.py ./vault graph.html knowledge-graph.html`).
A change to `ui/workbench.html` alone doesn't trigger a deploy; run the workflow by hand or include a vault change.

Specs: `docs/specs/2026-10-03-workbench-requirements.md`, `docs/specs/2026-10-03-workbench-design.md`.

## Directory Structure

```
├── vault/pages/              # Markdown pages: items, plus concept/topic/domain stubs (git-tracked)
├── config.yaml               # Vault path, domain weights (= career focus in Insights)
├── ui/workbench.html         # The app: Workbench / Plan / Library / Insights tabs
├── cli/
│   ├── main.py               # CLI entry point
│   ├── items.py              # Item model: states, dates, notes, checklist, time, plan, capture, migration
│   ├── server.py             # `lpt serve`: the app plus a local JSON API that edits the vault
│   ├── build_graph.py        # Builds site/index.html from the vault (also run by CI)
│   ├── page_writer.py        # Concept/topic/domain stub pages (used when filing items)
│   ├── page_reader.py, config.py
├── tests/                    # pytest; tests/browser/ drives the real app in Chrome
├── docs/                     # Specs and the original clickable mockup
└── .github/workflows/        # Pages deploy (pushing workflow changes needs a token with `workflow` scope)
```

Gitignored: `.venv/`, `site/` (built), `processed/` (old inbox archive), editor/conductor artifacts.

## Item pages

An item is a page whose `type::` is paper, article, video, docs, tweet, **project** or **practice**.

```
title:: Raft — In Search of an Understandable Consensus Algorithm
type:: paper
domain:: [[Systems]]
topic:: [[Distributed Consensus]]
state:: picked                      # collected | picked | done | dropped
picked:: [[2026-10-03]]             # also done:: / dropped:: when they happen
planned:: 2026-10                   # month first planned; unfinished items carry over automatically
my-priority:: soon                  # now | soon | someday (only ever set by the user)
note:: why I saved it               # from capture
enrich:: pending                    # captured but not filed yet
ingested:: [[2026-07-09]]
concepts:: [[Raft Consensus]], ...

## Summary
...
## Notes
free text, one running note
## Checklist
- [x] Read §5
- [ ] Implement log replication
## Time
- 2026-10-03 · 1h30m               # one line per day
```

Rules (in `cli/items.py`): picking up or adding time puts an item in this month's plan; adding time to a collected
item picks it up; Done fills `picked::` if missing; "back" returns it to collected but keeps it planned; dropped
items stop counting towards coverage. Coverage = done ÷ (everything not dropped) per topic/area.
There is no per-item percentage and no computed priority. Don't add them back.

## Everyday use

```bash
lpt serve                         # the app at http://127.0.0.1:8765 with editing (time, notes, checklist, plan, add)
lpt graph                         # build site/ and open it read-only
```

Or from the terminal (titles match fuzzily):

```bash
lpt add <url-or-title>... [--note "why"] [--type project|practice|article] [--prio now|soon|someday]
pbpaste | lpt add                 # one item per line, e.g. a batch of links from WhatsApp
lpt pick "raft"   ·   lpt done "raft"   ·   lpt drop "raft"   ·   lpt back "raft"
lpt time "raft" [30m|1h|1h30m|-30m] [--date yesterday]
lpt check "raft" "Implement log replication"   ·   lpt check "raft" --toggle 1   ·   --remove 1
lpt note "raft" "Stopped at 5.4.1"
lpt prio "raft" now|soon|someday|none
lpt plan "raft" [next|2026-11|none]          # default: this month
lpt show "raft"   ·   lpt ls [--state picked|--unsorted]   ·   lpt status
```

Then commit and push the changed `vault/pages/` files to update the read-only site.

## Filing Unsorted items (Claude's job)

Captured items land in Unsorted with `enrich:: pending`. To file them:

1. `lpt enrich` lists them as JSON lines (`id`, `title`, `type`, `source`, `note`).
2. For each one, read the source and write a result JSON:
   ```json
   {"title": "Human-readable title", "medium": "paper|article|video|docs",
    "domain": "Systems", "topic": "Concurrency",
    "complexity": "beginner|intermediate|advanced", "size": "quick-read|medium|deep-dive",
    "concepts": ["What it teaches"], "prerequisites": ["What you need first"],
    "summary": "2-3 sentences", "key_takeaways": ["...", "..."]}
   ```
3. `lpt enrich <id> --from result.json` fills the page, clears `enrich`, renames the file to the title and creates
   concept/topic/domain stubs.

Use an existing domain where it fits; if nothing fits, leave the item in Unsorted (skip it) rather than inventing a
new area. Never change `state::`, dates, `my-priority::`, `planned::`, Notes, Checklist or Time while filing.
Projects and practice keep their type (`medium` is ignored for them).

Existing domains: ML/Infrastructure, ML/Agents, ML/Frameworks, ML/Foundations, ML/Voice, ML/Evaluation, Game AI,
Systems, Networking, Programming/Rust, Programming/Zig, Programming/Python, Programming/Compilers, Embedded/Gaming,
Mindset

Concept names for cross-linking (use these exact names when they apply): Transformer Architecture, Attention
Mechanisms, KV Cache, RLHF, Mixture of Experts, Multi-Head Attention, Self-Attention, LLM Basics, Prompt Engineering
Fundamentals, Neural Network Fundamentals, Linear Algebra Basics, Reinforcement Learning Basics, Networking
Fundamentals, TCP/IP Basics, Database Basics, Concurrency Basics, C Basics, Python, Memory Management Concepts, Linux
Basics, Data Structures, Game Theory Basics, Consistency Models, Transactions, Raft Consensus, Agent Architecture,
Tool Use, ReAct Pattern

## The app (`ui/workbench.html`)

One self-contained file. The build replaces `VAULT_PLACEHOLDER` (item JSON from `cli/items.load_items`) and
`META_PLACEHOLDER` (domain weights). On load it asks `/api/items`: if that answers (under `lpt serve`) the page is
editable and every change goes through `POST /api/item {id, action, ...}` or `POST /api/add`; otherwise (a file, or
GitHub Pages, or a phone) it is read-only and hides edit controls. Deep links: `#wb`, `#plan`, `#lib`, `#ins`,
`#item=<id>`. On phones the tabs move to a bottom bar.

## Tests

```bash
.venv/bin/python -m pytest -q          # model, CLI, server, build; round-trips every real vault page
bash tests/browser/run.sh              # drives Chrome against `lpt serve` on a migrated copy of the vault
```

Run both after changing `items.py`, `server.py` or `ui/workbench.html`.
