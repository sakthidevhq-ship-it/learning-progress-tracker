# Learning Progress Tracker

A CLI tool (`lpt`) that tracks learning resources as markdown files and visualizes them as an interactive knowledge graph. Hosted via GitHub Pages — push to `main` triggers a rebuild.

## Directory Structure

```
learning-tracker/
├── vault/pages/              # Markdown files — the database (git-tracked)
├── inbox/                    # Pending jobs (lpt add creates these)
├── config.yaml               # Vault path, domain/topic weights
├── graph.html                # Graph HTML template
├── cli/                      # Python CLI + graph builder
│   ├── main.py               # CLI entry point
│   ├── build_graph.py        # Builds knowledge-graph.html from vault
│   ├── config.py             # Config loader
│   ├── page_writer.py        # Writes markdown pages
│   ├── page_reader.py        # Reads/parses markdown pages
│   ├── priority.py           # Priority scoring
│   └── progress.py           # Progress tracking
├── tests/                    # Test suite
├── .github/workflows/        # GitHub Actions — auto-deploy to Pages
└── pyproject.toml            # Python package config
```

**What gets deployed:** `vault/pages/*.md` → `cli/build_graph.py` → `knowledge-graph.html` → GitHub Pages

**What's gitignored:** `.venv/`, `processed/`, `knowledge-graph.html` (built artifact), editor/conductor artifacts

## How to Add a New Resource

### Step 1: Add to inbox
```bash
lpt add <url-or-filepath> [--domain "Domain/Name"] [--topic "Topic"] [--engagement read|implement|background] [--tag TAG...]
```

### Step 2: Create the processor result
Create `inbox/<job-id>.result.json`:
```json
{
  "title": "Human-readable title",
  "summary": "2-3 sentence description",
  "medium": "paper|article|video|docs",
  "complexity": "beginner|intermediate|advanced",
  "size": "quick-read|medium|deep-dive",
  "domain": "Domain/Subdomain",
  "topic": "Specific Topic",
  "concepts": ["What this resource teaches"],
  "prerequisites": ["What you need to know first"],
  "key_takeaways": ["Key insight 1", "Key insight 2"],
  "engagement_suggestion": "read|implement|background"
}
```

**Concept names for cross-linking** (use these exact names when they apply):

Transformer Architecture, Attention Mechanisms, KV Cache, RLHF, Mixture of Experts, Multi-Head Attention, Self-Attention, LLM Basics, Prompt Engineering Fundamentals, Neural Network Fundamentals, Linear Algebra Basics, Reinforcement Learning Basics, Networking Fundamentals, TCP/IP Basics, Database Basics, Concurrency Basics, C Basics, Python, Memory Management Concepts, Linux Basics, Data Structures, Game Theory Basics, Consistency Models, Transactions, Raft Consensus, Agent Architecture, Tool Use, ReAct Pattern

Resource-to-resource prerequisite edges are computed automatically: if Resource A's `concepts` includes "X" and Resource B's `prerequisites` includes "X", then the graph shows "read A before B."

### Step 3: Write to vault and rebuild
```bash
lpt write --all
lpt graph
```

### Step 4: Push to deploy
```bash
git add vault/pages/
git commit -m "Add: Resource Title"
git push
```
GitHub Actions rebuilds and deploys the graph automatically.

## How to Update Progress

```bash
lpt progress "Title" 50       # Set progress to 50% (fuzzy match)
lpt done "Title"              # Mark as 100% complete
lpt graph                     # Rebuild to see changes
```

Then commit + push the updated vault files.

## Existing Domains

ML/Infrastructure, ML/Agents, ML/Frameworks, ML/Foundations, ML/Voice, Game AI, Systems, Networking, Programming/Rust, Programming/Zig, Programming/Python, Programming/Compilers, Embedded/Gaming, Mindset

## CLI Reference

| Command | What it does |
|---------|-------------|
| `lpt add <source>` | Add URL or file to inbox |
| `lpt write --all` | Write all processed jobs to vault |
| `lpt status` | Show inbox counts |
| `lpt progress "title" N` | Set progress (0-100) |
| `lpt done "title"` | Mark complete |
| `lpt recompute` | Recalculate all priorities |
| `lpt graph` | Rebuild graph and open in browser |

## Graph Visualization

- **Position = relatedness** — resources sharing concepts cluster together
- **Color = status** — green (done), orange (in progress), blue (ready), dim (blocked)
- **Solid edges** = prerequisite ("read A before B")
- **Dashed edges** = siblings (shared prerequisites)
- **Click** = side panel with full detail, selectable text
- **Filters** = toggle by status, domain, engagement type, search
- **Pan/zoom** = drag + scroll
