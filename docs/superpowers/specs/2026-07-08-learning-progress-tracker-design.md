# Learning Progress Tracker — Design Spec

A CLI that ingests URLs and local documents into a Logseq-compatible vault, with defined directory structure, markdown page formats, priority scoring, and progress tracking. Content analysis/categorization is a pluggable processor added later.

## Architecture

```
[CLI: lpt add] → [inbox/] → [Processor (pluggable, later)] → [Logseq Vault pages/]
                                                                      ↑
[CLI: lpt progress/done/dashboard/recompute] ─────────────────────────┘
```

### What's in scope now
- **CLI (`lpt`)** — ingestion, progress tracking, dashboard, priority recomputation
- **Directory structure** — where every file lives, naming conventions
- **Markdown page format** — property schema, page templates for each type
- **Page writer** — given structured metadata, writes/updates Logseq pages
- **Priority engine** — computes scores from page properties and config weights
- **Progress tracking** — per-item, per-topic, per-domain aggregation + dashboard

### What's out of scope (plugged in later)
- **Processor** — the thing that reads raw content and produces structured metadata (concepts, prerequisites, complexity, etc.). Could be Claude, a routing agent, Paperclip agents, or anything else. The system defines a **Processor Interface** — a JSON schema the processor must output — and the page writer consumes it.

## Processor Interface

The processor (whatever it is) receives a job file and must output a JSON object conforming to this schema. The page writer uses this to create/update Logseq pages.

```json
{
  "title": "Gemma 4 Technical Report",
  "summary": "2-3 paragraph summary",
  "medium": "paper",
  "complexity": "advanced",
  "size": "deep-dive",
  "domain": "ML/Infrastructure",
  "topic": "Inference Optimization",
  "concepts": ["MoE", "Distillation", "RLHF"],
  "prerequisites": ["Attention Mechanisms", "KV Cache", "vLLM"],
  "key_takeaways": ["...", "..."],
  "engagement_suggestion": "read"
}
```

All fields are optional except `title`. The page writer fills in defaults for missing fields (`status: unread`, `progress: 0`, etc.). User-provided CLI flags (`--domain`, `--topic`, `--engagement`) override processor output.

The processor writes its output as a JSON file alongside the job file: `inbox/<job-id>.result.json`. The page writer picks it up from there.

## CLI

Python package using Click. Installed via `pip install -e .` as `lpt`.

### Commands

```bash
lpt add <url-or-path> [--domain X] [--topic Y] [--engagement read|implement|background] [--tag TAG...]
lpt status                     # show inbox queue: pending, processed, failed counts
lpt progress <title> <0-100>   # update progress on an item
lpt done <title>               # mark item complete (progress=100, status=completed)
lpt dashboard                  # regenerate the Learning Dashboard page
lpt recompute                  # recalculate all priorities after config weight changes
lpt write <job-id>             # run page writer for a processed job (has .result.json)
lpt write --all                # run page writer for all processed jobs missing pages
lpt init                       # initialize vault structure + generate Learning Queue page
```

### `lpt add` Behavior

1. Validates the source (file exists for local paths; for URLs, just records it — no fetching)
2. Creates a job file in `inbox/` as JSON:
   ```json
   {
     "id": "20260708-143022-a1b2",
     "source": "https://arxiv.org/abs/2504.00958",
     "source_type": "url",
     "domain": "ML/Infrastructure",
     "topic": "Inference Optimization",
     "engagement": "read",
     "tags": ["transformers", "inference"],
     "created_at": "2026-07-08T14:30:22",
     "status": "pending"
   }
   ```
3. Returns immediately
4. If `--domain`, `--topic`, or `--engagement` are omitted, they're left null in the job file — the processor or user fills them in later

### `lpt write` Behavior

Looks for `inbox/<job-id>.result.json`. If found:
1. Reads the result JSON (processor output)
2. Merges with job file (CLI flags override processor output)
3. Calls the page writer to create/update the Logseq page
4. Creates concept stub pages for any prerequisite/concept without an existing page
5. Computes priority score
6. Moves job + result files to `processed/`

### `lpt progress` / `lpt done` Behavior

Finds the matching Logseq page by title (fuzzy match), updates `progress::` and `status::` properties in the markdown file. Triggers priority recomputation for items that depend on this one as a prerequisite.

### `lpt dashboard` Behavior

Scans all pages in the vault, aggregates progress by domain and topic, writes/overwrites a `Learning Dashboard` page.

## Directory Structure

```
learning-progress-tracker/
├── cli/
│   ├── __init__.py
│   ├── main.py              # Click CLI entry point
│   ├── page_writer.py       # Writes Logseq markdown pages from structured metadata
│   ├── page_reader.py       # Reads/parses Logseq pages (properties + content)
│   ├── priority.py          # Priority score computation
│   └── progress.py          # Progress tracking + dashboard generation
├── config.yaml              # Vault path, domain/topic weights
├── inbox/                   # Job files (.json) and processor results (.result.json)
├── processed/               # Completed jobs (moved here after page is written)
├── failed/                  # Jobs that failed processing
├── tests/
│   ├── test_page_writer.py
│   ├── test_page_reader.py
│   ├── test_priority.py
│   └── test_progress.py
├── pyproject.toml
└── README.md
```

### Logseq Vault Structure (at `vault_path` from config)

```
vault/
├── pages/
│   ├── Gemma 4 Technical Report.md    # Resource page
│   ├── KV Cache.md                     # Concept stub or resource
│   ├── ML___Infrastructure.md          # Domain page (/ escaped as ___)
│   ├── Inference Optimization.md       # Topic page
│   ├── Learning Dashboard.md           # Generated dashboard
│   └── Learning Queue.md               # Pre-built queries page (generated once)
├── journals/                            # User's daily journals (untouched)
└── logseq/
    └── config.edn                       # Logseq config (untouched)
```

### File Naming Conventions

- Page filenames = page title with `/` replaced by `___` (Logseq convention)
- Job files: `<timestamp>-<4char-hex>.json` (e.g., `20260708-143022-a1b2.json`)
- Result files: `<job-id>.result.json` (same ID as the job file)

## Logseq Page Formats

### Resource Page (ingested item)

```markdown
title:: Gemma 4 Technical Report
type:: paper
domain:: [[ML/Infrastructure]]
topic:: [[Inference Optimization]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: deep-dive
medium:: paper
priority:: 85
prerequisites:: [[Attention Mechanisms]], [[KV Cache]], [[vLLM]]
concepts:: [[MoE]], [[Distillation]], [[RLHF]]
tags:: transformers, inference
source:: https://arxiv.org/abs/2504.00958
ingested:: [[2026-07-08]]

## Summary
Google DeepMind's Gemma 4 introduces...

## Key Takeaways
- Point 1
- Point 2

## Prerequisites
- [[Attention Mechanisms]] — needed to understand the architecture modifications
- [[KV Cache]] — the report assumes familiarity with KV cache optimization
- [[vLLM]] — serving benchmarks reference vLLM internals

## My Notes

```

### Concept Stub Page (auto-generated prerequisite)

Created when a prerequisite or concept is referenced but has no page yet.

```markdown
title:: KV Cache
type:: concept
status:: stub
domain:: [[ML/Infrastructure]]
topic:: [[Inference Optimization]]
referenced-by:: [[Gemma 4 Technical Report]]

## About
Auto-generated stub. This concept is a prerequisite for items in your learning queue.
```

### Domain Page

```markdown
title:: ML/Infrastructure
type:: domain

## Topics
- [[Inference Optimization]]
- [[Distributed Training]]
- [[Model Serving]]
```

Updated automatically when new topics are added under this domain.

### Topic Page

```markdown
title:: Inference Optimization
type:: topic
domain:: [[ML/Infrastructure]]
```

### Learning Dashboard Page (generated by `lpt dashboard`)

```markdown
title:: Learning Dashboard
type:: dashboard
generated:: [[2026-07-08]]

## Domain Progress
| Domain | Items | Done | In Progress | Progress |
|--------|-------|------|-------------|----------|
| [[ML/Infrastructure]] | 12 | 5 | 3 | 42% |
| [[Systems]] | 8 | 6 | 1 | 75% |
| [[Databases]] | 3 | 0 | 0 | 0% |

## Topic Progress
| Topic | Domain | Items | Done | Progress |
|-------|--------|-------|------|----------|
| [[Inference Optimization]] | [[ML/Infrastructure]] | 4 | 1 | 25% |
| [[KV Cache Design]] | [[ML/Infrastructure]] | 2 | 2 | 100% |

## Knowledge Gaps (Stubs)
- [[vLLM]] — needed by: [[Gemma 4 Technical Report]]
- [[Attention Mechanisms]] — needed by: [[Gemma 4 Technical Report]], [[Flash Attention Paper]]

## Queue (Top 10 by Priority)
1. [[KV Cache]] (priority: 95, background, beginner)
2. [[Attention Mechanisms]] (priority: 90, read, intermediate)
3. [[Gemma 4 Technical Report]] (priority: 85, read, advanced)
```

### Learning Queue Page (generated once by `lpt init`)

Contains pre-built Logseq queries:

```markdown
title:: Learning Queue
type:: queries

## Next Up (by priority)
{{query (and (property :status "unread") (not (property :type "concept")))}}

## Knowledge Gaps
{{query (property :status "stub")}}

## In Progress
{{query (property :status "in-progress")}}

## By Domain
{{query (and (property :domain "[[ML/Infrastructure]]") (property :status "unread"))}}

## Background Reading
{{query (and (property :status "unread") (property :engagement "background"))}}

## Quick Wins (beginner)
{{query (and (property :status "unread") (property :complexity "beginner"))}}
```

## Property Definitions

| Property | Values | Description |
|----------|--------|-------------|
| `type` | `paper`, `article`, `tweet`, `video`, `docs`, `concept`, `domain`, `topic`, `dashboard`, `queries` | Page type |
| `domain` | Logseq page link | Broad area: ML/Infrastructure, Systems, Databases, Security |
| `topic` | Logseq page link | Specific within domain: Inference Optimization, KV Cache Design |
| `engagement` | `read`, `implement`, `background` | How to interact with this item |
| `status` | `unread`, `in-progress`, `completed`, `stub` | Current learning status |
| `progress` | 0-100 | Percentage completion |
| `complexity` | `beginner`, `intermediate`, `advanced` | Difficulty level |
| `size` | `quick-read`, `medium`, `deep-dive` | Time investment required |
| `medium` | `paper`, `article`, `tweet`, `video`, `docs` | Content format |
| `priority` | 0-100 | Computed priority score |
| `prerequisites` | Comma-separated Logseq page links | What to learn first |
| `concepts` | Comma-separated Logseq page links | Concepts covered by this item |
| `source` | URL or file path | Original source |
| `ingested` | Logseq date link | When the item was added |
| `referenced-by` | Comma-separated Logseq page links | (stubs) Which items reference this concept |

## Priority Scoring

Priority is computed by the page writer when creating/updating a page, and recalculated by `lpt recompute`. Stored as the `priority::` property.

### Recalculation Triggers
- `lpt write` — new page added, recompute affected pages
- `lpt done` / `lpt progress` — item completed, dependents may shift
- `lpt recompute` — explicit full recomputation (after config weight changes)

### Formula

```
priority = (overlap_score * 25)
         + (prerequisite_demand * 25)
         + (domain_weight * 20)
         + (topic_weight * 15)
         + (recency * 5)
         + (inverse_complexity * 5)
         + (engagement_boost * 5)
```

### Components

- **overlap_score (0-25):** How many other items share concepts with this one. High overlap = hub concept, learning it unlocks many items.
- **prerequisite_demand (0-25):** How many items list this (or its concepts) as a prerequisite. High demand = foundational.
- **domain_weight (0-20):** From `config.yaml`. Higher weight = higher priority.
- **topic_weight (0-15):** From `config.yaml`. Higher weight = higher priority.
- **recency (0-5):** Newer items get a small boost.
- **inverse_complexity (0-5):** Simpler items get a slight boost (quick wins when other factors are equal).
- **engagement_boost (0-5):** `background` items get a small bump (easy to slot in).

## Progress Tracking

### Per-Item
`progress:: 0-100` on each resource page. Updated via `lpt progress <title> <value>` or directly in Logseq. When progress reaches 100, status flips to `completed`.

### Per-Topic (computed by `lpt dashboard`)
Aggregated from all resource items under a topic. 5 items, 3 completed = 60%.

### Per-Domain (computed by `lpt dashboard`)
Aggregated from all topics under a domain.

## Configuration

`config.yaml` at the project root:

```yaml
vault_path: ~/logseq-vault

domain_weights:
  ML/Infrastructure: 0.9
  Systems: 0.8
  Databases: 0.5
  Security: 0.6
  Frontend: 0.3

topic_weights:
  Inference Optimization: 0.95
  Distributed Training: 0.7
  KV Cache Design: 0.85
  RLHF: 0.6

default_weight: 0.5
```

New domains/topics encountered by the processor get `default_weight` until the user configures them.

## Error Handling

- **`lpt add` validation failures** (local file not found): Error message, no job file created.
- **`lpt write` with missing result**: Error message listing jobs without `.result.json` files.
- **`lpt progress`/`lpt done` title not found**: Fuzzy match with suggestions. If no match, error.
- **Duplicate detection**: Before writing a page, check if a page with the same `source::` already exists. If so, skip or update (configurable in `config.yaml` via `on_duplicate: skip | update`).
- **Failed jobs**: The processor (when implemented) moves failed jobs to `failed/` with a `.error.json` alongside.

## Testing Strategy

- **Unit tests**: Page writer (given metadata JSON → correct markdown), page reader (given markdown → correct parsed properties), priority calculator (given pages → correct scores), progress aggregation
- **Integration tests**: End-to-end from job file + result JSON → page writer → verify page content, links, and stub creation
- **No processor tests** — that's out of scope for now
