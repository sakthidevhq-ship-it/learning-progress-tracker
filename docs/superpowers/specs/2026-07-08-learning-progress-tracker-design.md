# Learning Progress Tracker — Design Spec

A CLI + async processor that writes Logseq-compatible markdown pages, turning a dump of URLs and documents into a structured knowledge graph with prerequisite chains, priority scoring, and progress tracking.

## Architecture

```
[CLI: lpt add] → [inbox/] → [Async Processor] → [Logseq Vault pages/]
                                    ↓
                              [Claude API]
```

Two components:
1. **CLI (`lpt`)** — accepts URLs or local file paths, drops job files into `inbox/`, provides progress/dashboard commands
2. **Async Processor** — watches `inbox/`, fetches content, calls Claude API for analysis, writes/updates Logseq pages, computes priority scores

Logseq is the UI for everything: graph visualization, learning queue (via queries), note-taking, and consumption.

## CLI

Python package using Click. Installed via `pip install -e .` as `lpt`.

### Commands

```bash
lpt add <url-or-path> [--domain X] [--topic Y] [--engagement read|implement|background] [--tag TAG...]
lpt status                     # show inbox/processing queue status
lpt progress <title> <0-100>   # update progress on an item
lpt done <title>               # mark item complete (progress=100, status=completed)
lpt dashboard                  # regenerate the Learning Dashboard page
lpt recompute                  # recalculate all priorities after config weight changes
lpt process                    # run the processor once (alternative to daemon mode)
lpt suggest <concept>          # (stretch goal) ask Claude for recommended resources to learn a concept
```

### `lpt add` Behavior

1. Validates the source (URL reachable, file exists)
2. Creates a job file in `inbox/` as JSON:
   ```json
   {
     "id": "20260708-143022-a1b2",
     "source": "https://arxiv.org/abs/2504.00958",
     "type": "url",
     "domain": "ML/Infrastructure",
     "topic": "Inference Optimization",
     "engagement": "read",
     "tags": ["transformers", "inference"],
     "created_at": "2026-07-08T14:30:22"
   }
   ```
3. Returns immediately — processing is async
4. If `--domain` or `--topic` are omitted, the LLM infers them during processing

### `lpt progress` / `lpt done` Behavior

Finds the matching Logseq page by title, updates the `progress::` and `status::` properties in the markdown file directly. Triggers a priority recomputation for items that depend on this one as a prerequisite.

### `lpt dashboard` Behavior

Scans all pages in the vault, aggregates progress by domain and topic, writes/overwrites a `Learning Dashboard` page in the vault.

## Async Processor

A Python process that can run as:
- **One-shot:** `lpt process` — processes all pending jobs in `inbox/` and exits
- **Watch mode:** `lpt process --watch` — uses filesystem watching (watchdog) to process jobs as they arrive

### Processing Pipeline

For each job file in `inbox/`:

1. **Fetch content**
   - Web articles: `trafilatura` for clean text extraction
   - Arxiv papers: `arxiv` API for metadata + PDF download, `pdfplumber` for text
   - Tweets/X posts: direct fetch with fallback to metadata-only
   - Local PDFs: `pdfplumber`
   - Local markdown/text: read directly

2. **Send to Claude API** with a structured prompt requesting JSON output:
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
   - If the user provided `--domain` / `--topic` / `--engagement` in the CLI, those override the LLM's suggestions
   - The prompt instructs Claude to identify prerequisites at the right granularity — not too broad ("machine learning") and not too narrow ("line 42 of vllm/engine.py")

3. **Write Logseq page** into `vault/pages/` (see Page Format below)

4. **Create/update concept stub pages** for any prerequisite or concept that doesn't have a page yet

5. **Compute priority score** for the new page and recompute for any pages affected by new concept links

6. **Move job file** from `inbox/` to `processed/`

### Content Fetching Details

| Source Type | Library | Extraction |
|-------------|---------|------------|
| Web article | `trafilatura` | Main content text, title, date |
| Arxiv | `arxiv` API + `pdfplumber` | Abstract, full text from PDF |
| Tweet/X | `httpx` with appropriate headers | Tweet text, thread if applicable |
| PDF (local) | `pdfplumber` | Full text extraction |
| Markdown (local) | Direct read | Raw content |

## Logseq Page Format

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

```markdown
title:: KV Cache
type:: concept
status:: stub
domain:: [[ML/Infrastructure]]
topic:: [[Inference Optimization]]
referenced-by:: [[Gemma 4 Technical Report]]

## About
Auto-generated stub. This concept is a prerequisite for items in your learning queue.
Add a resource with `lpt add` or run `lpt suggest "KV Cache"` to get recommendations.
```

### Domain Page (auto-generated)

```markdown
title:: ML/Infrastructure
type:: domain

## Topics
- [[Inference Optimization]]
- [[Distributed Training]]
- [[Model Serving]]
```

### Topic Page (auto-generated)

```markdown
title:: Inference Optimization
type:: topic
domain:: [[ML/Infrastructure]]
```

## Property Definitions

| Property | Values | Description |
|----------|--------|-------------|
| `type` | `paper`, `article`, `tweet`, `video`, `docs`, `concept`, `domain`, `topic` | What kind of page this is |
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

## Priority Scoring

Priority is computed by the processor and written as a page property. Recalculated when:
- A new item is added (affects items sharing concepts/prerequisites)
- Config weights change (`lpt recompute`)
- An item is marked complete (unlocks dependents)

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

- **overlap_score (0-25):** How many other items in the queue share concepts with this one. High overlap = this is a hub concept, learning it unlocks understanding across many items.
- **prerequisite_demand (0-25):** How many items list this (or its concepts) as a prerequisite. High demand = foundational, learn first.
- **domain_weight (0-20):** From `config.yaml`. Domains you care about more get higher priority.
- **topic_weight (0-15):** From `config.yaml`. Topics you care about more get higher priority.
- **recency (0-5):** Newer items get a small boost to keep the queue fresh.
- **inverse_complexity (0-5):** Simpler items get a slight boost when other factors are equal (quick wins).
- **engagement_boost (0-5):** `background` items get a small bump (easy to slot in). `implement` items are neutral. `read` items are neutral.

## Progress Tracking

### Per-Item
`progress:: 0-100` on each resource page. Updated via `lpt progress <title> <value>` or directly in Logseq. When progress hits 100, status flips to `completed`.

### Per-Topic (computed)
Aggregated from all items under a topic. If topic "Inference Optimization" has 5 items and 3 are completed, topic progress = 60%.

### Per-Domain (computed)
Aggregated from all topics under a domain.

### Learning Dashboard Page
Generated by `lpt dashboard`, written to `vault/pages/Learning Dashboard.md`:

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

## Logseq Queries

Pre-built queries for the user to add to their journal or a dedicated page:

**Learning queue (unread, by priority):**
```
{{query (and (property :status "unread") (not (property :type "concept")))}}
```

**Knowledge gaps (stubs to fill):**
```
{{query (property :status "stub")}}
```

**In progress:**
```
{{query (property :status "in-progress")}}
```

**By domain:**
```
{{query (and (property :domain "[[ML/Infrastructure]]") (property :status "unread"))}}
```

**By engagement type:**
```
{{query (and (property :status "unread") (property :engagement "background"))}}
```

**By complexity:**
```
{{query (and (property :status "unread") (property :complexity "beginner"))}}
```

## Configuration

`config.yaml` at the project root:

```yaml
vault_path: ~/logseq-vault
inbox_path: ./inbox
processed_path: ./processed

anthropic_api_key_env: ANTHROPIC_API_KEY

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

The API key is read from an environment variable (referenced by name in config, never stored in the file).

## Directory Structure

```
learning-progress-tracker/
├── cli/
│   ├── __init__.py
│   ├── main.py              # Click CLI entry point
│   ├── ingest.py            # Content fetching (URLs, PDFs, etc.)
│   ├── process.py           # LLM processing + page writing
│   ├── priority.py          # Priority score computation
│   ├── progress.py          # Progress tracking + dashboard generation
│   └── page_writer.py       # Logseq markdown page generation
├── config.yaml
├── inbox/                   # Pending job files
├── processed/               # Completed job files
├── tests/
│   ├── test_ingest.py
│   ├── test_process.py
│   ├── test_priority.py
│   └── test_page_writer.py
├── pyproject.toml
└── README.md
```

The Logseq vault lives at `vault_path` from config (outside this repo, or symlinked in).

## Error Handling

- **Fetch failures** (URL 404, PDF corrupt): Job moves to `failed/` with an error log. `lpt status` shows failed jobs.
- **Claude API errors**: Retried 3 times with exponential backoff. On persistent failure, job stays in `inbox/` and `lpt status` reports it.
- **Duplicate detection**: Before writing a page, check if a page with the same `source::` already exists. If so, skip or update (configurable).

## Testing Strategy

- **Unit tests**: Page writer (given LLM output JSON, produces correct markdown), priority calculator (given a set of pages, computes correct scores), config loading
- **Integration tests**: End-to-end from job file → Claude API (mocked) → written page → verify page content and links
- **Manual testing**: Add a real URL, process it, open in Logseq, verify graph links work
