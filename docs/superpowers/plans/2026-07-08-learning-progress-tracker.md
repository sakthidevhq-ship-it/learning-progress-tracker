# Learning Progress Tracker Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a CLI tool (`lpt`) that ingests learning resources into a Logseq-compatible vault with priority scoring and progress tracking.

**Architecture:** A Python CLI (Click) drops job files into an `inbox/` directory. A page writer consumes processor result JSON and writes Logseq-compatible markdown pages with properties and backlinks. A priority engine scores items based on concept overlap, prerequisite demand, and configurable domain/topic weights. Progress tracking aggregates completion per item, topic, and domain.

**Tech Stack:** Python 3.11+, Click (CLI), PyYAML (config), pytest (testing), thefuzz (fuzzy title matching)

## Global Constraints

- Python 3.11+ required
- All page files are Logseq-compatible markdown with `property:: value` syntax
- Page filenames use title with `/` replaced by `___`
- Logseq page links use `[[Page Name]]` syntax
- Job IDs follow `YYYYMMDD-HHMMSS-XXXX` format (timestamp + 4-char hex)
- Processor is out of scope — only the JSON interface it must conform to is defined
- No external network calls in any component (fetching is processor's job)

---

### Task 1: Project Scaffolding + Config Loader

**Files:**
- Create: `pyproject.toml`
- Create: `cli/__init__.py`
- Create: `cli/config.py`
- Create: `config.yaml`
- Create: `tests/__init__.py`
- Create: `tests/test_config.py`

**Interfaces:**
- Consumes: nothing
- Produces: `load_config(path: str | None = None) -> Config` where `Config` is a dataclass with fields `vault_path: Path`, `domain_weights: dict[str, float]`, `topic_weights: dict[str, float]`, `default_weight: float`, `on_duplicate: str`. Also `title_to_filename(title: str) -> str` and `filename_to_title(filename: str) -> str`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_config.py
import os
import tempfile
from pathlib import Path

import pytest
import yaml

from cli.config import Config, load_config, title_to_filename, filename_to_title


def test_load_config_from_file(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.dump({
        "vault_path": str(tmp_path / "vault"),
        "domain_weights": {"ML/Infrastructure": 0.9, "Systems": 0.8},
        "topic_weights": {"Inference Optimization": 0.95},
        "default_weight": 0.5,
    }))
    config = load_config(str(config_file))
    assert config.vault_path == tmp_path / "vault"
    assert config.domain_weights["ML/Infrastructure"] == 0.9
    assert config.topic_weights["Inference Optimization"] == 0.95
    assert config.default_weight == 0.5


def test_load_config_defaults(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.dump({"vault_path": str(tmp_path / "vault")}))
    config = load_config(str(config_file))
    assert config.domain_weights == {}
    assert config.topic_weights == {}
    assert config.default_weight == 0.5
    assert config.on_duplicate == "skip"


def test_load_config_expands_tilde():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump({"vault_path": "~/my-vault"}, f)
        path = f.name
    try:
        config = load_config(path)
        assert config.vault_path == Path.home() / "my-vault"
    finally:
        os.unlink(path)


def test_load_config_missing_vault_path(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.dump({}))
    with pytest.raises(ValueError, match="vault_path"):
        load_config(str(config_file))


def test_title_to_filename():
    assert title_to_filename("ML/Infrastructure") == "ML___Infrastructure.md"
    assert title_to_filename("KV Cache") == "KV Cache.md"
    assert title_to_filename("Gemma 4 Technical Report") == "Gemma 4 Technical Report.md"


def test_filename_to_title():
    assert filename_to_title("ML___Infrastructure.md") == "ML/Infrastructure"
    assert filename_to_title("KV Cache.md") == "KV Cache"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/sakthi/conductor/workspaces/learning-progress-tracker/hat-yai && python -m pytest tests/test_config.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'cli.config'`

- [ ] **Step 3: Create pyproject.toml**

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "learning-progress-tracker"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "click>=8.1",
    "pyyaml>=6.0",
    "thefuzz>=0.22",
]

[project.scripts]
lpt = "cli.main:cli"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 4: Create config.yaml**

```yaml
# config.yaml
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
on_duplicate: skip
```

- [ ] **Step 5: Create cli/__init__.py and tests/__init__.py**

Both are empty files.

- [ ] **Step 6: Implement config.py**

```python
# cli/config.py
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class Config:
    vault_path: Path
    domain_weights: dict[str, float] = field(default_factory=dict)
    topic_weights: dict[str, float] = field(default_factory=dict)
    default_weight: float = 0.5
    on_duplicate: str = "skip"


def load_config(path: str | None = None) -> Config:
    if path is None:
        path = "config.yaml"
    with open(path) as f:
        raw = yaml.safe_load(f) or {}

    if "vault_path" not in raw:
        raise ValueError("config.yaml must specify vault_path")

    return Config(
        vault_path=Path(raw["vault_path"]).expanduser(),
        domain_weights=raw.get("domain_weights", {}),
        topic_weights=raw.get("topic_weights", {}),
        default_weight=raw.get("default_weight", 0.5),
        on_duplicate=raw.get("on_duplicate", "skip"),
    )


def title_to_filename(title: str) -> str:
    return title.replace("/", "___") + ".md"


def filename_to_title(filename: str) -> str:
    if filename.endswith(".md"):
        filename = filename[:-3]
    return filename.replace("___", "/")
```

- [ ] **Step 7: Create stub cli/main.py**

```python
# cli/main.py
import click


@click.group()
def cli():
    pass
```

- [ ] **Step 8: Install package and run tests**

Run: `cd /Users/sakthi/conductor/workspaces/learning-progress-tracker/hat-yai && pip install -e ".[dev]" && python -m pytest tests/test_config.py -v`
Expected: All 6 tests PASS

- [ ] **Step 9: Commit**

```bash
git add pyproject.toml config.yaml cli/ tests/
git commit -m "feat: project scaffolding with config loader and title/filename helpers"
```

---

### Task 2: Page Reader — Parse Logseq Markdown

**Files:**
- Create: `cli/page_reader.py`
- Create: `tests/test_page_reader.py`

**Interfaces:**
- Consumes: `title_to_filename(title: str) -> str` and `filename_to_title(filename: str) -> str` from `cli.config`
- Produces: `PageData` dataclass with `title: str`, `properties: dict[str, str]`, `body: str`, `file_path: Path | None`. Functions: `parse_page(content: str) -> PageData`, `read_page(vault_path: Path, title: str) -> PageData | None`, `list_pages(vault_path: Path, type_filter: str | None = None) -> list[PageData]`, `update_property(vault_path: Path, title: str, key: str, value: str) -> None`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_page_reader.py
from pathlib import Path

import pytest

from cli.page_reader import PageData, parse_page, read_page, list_pages, update_property


SAMPLE_PAGE = """title:: Gemma 4 Technical Report
type:: paper
domain:: [[ML/Infrastructure]]
topic:: [[Inference Optimization]]
status:: unread
progress:: 0
priority:: 85
prerequisites:: [[Attention Mechanisms]], [[KV Cache]]
concepts:: [[MoE]], [[RLHF]]
source:: https://arxiv.org/abs/2504.00958

## Summary
This is the summary.

## My Notes
"""


def test_parse_page_properties():
    page = parse_page(SAMPLE_PAGE)
    assert page.title == "Gemma 4 Technical Report"
    assert page.properties["type"] == "paper"
    assert page.properties["domain"] == "[[ML/Infrastructure]]"
    assert page.properties["status"] == "unread"
    assert page.properties["progress"] == "0"
    assert page.properties["priority"] == "85"
    assert page.properties["prerequisites"] == "[[Attention Mechanisms]], [[KV Cache]]"


def test_parse_page_body():
    page = parse_page(SAMPLE_PAGE)
    assert "## Summary" in page.body
    assert "This is the summary." in page.body
    assert "## My Notes" in page.body


def test_parse_page_empty_properties():
    page = parse_page("## Just a body\nSome content")
    assert page.properties == {}
    assert page.title == ""
    assert "Just a body" in page.body


def test_read_page_exists(tmp_path):
    pages_dir = tmp_path / "pages"
    pages_dir.mkdir()
    (pages_dir / "KV Cache.md").write_text("title:: KV Cache\ntype:: concept\nstatus:: stub\n")
    page = read_page(tmp_path, "KV Cache")
    assert page is not None
    assert page.title == "KV Cache"
    assert page.properties["type"] == "concept"


def test_read_page_not_found(tmp_path):
    pages_dir = tmp_path / "pages"
    pages_dir.mkdir()
    assert read_page(tmp_path, "Nonexistent") is None


def test_read_page_with_slash_in_title(tmp_path):
    pages_dir = tmp_path / "pages"
    pages_dir.mkdir()
    (pages_dir / "ML___Infrastructure.md").write_text("title:: ML/Infrastructure\ntype:: domain\n")
    page = read_page(tmp_path, "ML/Infrastructure")
    assert page is not None
    assert page.title == "ML/Infrastructure"


def test_list_pages_all(tmp_path):
    pages_dir = tmp_path / "pages"
    pages_dir.mkdir()
    (pages_dir / "A.md").write_text("title:: A\ntype:: paper\n")
    (pages_dir / "B.md").write_text("title:: B\ntype:: concept\n")
    (pages_dir / "C.md").write_text("title:: C\ntype:: paper\n")
    pages = list_pages(tmp_path)
    assert len(pages) == 3


def test_list_pages_with_filter(tmp_path):
    pages_dir = tmp_path / "pages"
    pages_dir.mkdir()
    (pages_dir / "A.md").write_text("title:: A\ntype:: paper\n")
    (pages_dir / "B.md").write_text("title:: B\ntype:: concept\n")
    (pages_dir / "C.md").write_text("title:: C\ntype:: paper\n")
    pages = list_pages(tmp_path, type_filter="paper")
    assert len(pages) == 2
    assert all(p.properties["type"] == "paper" for p in pages)


def test_update_property(tmp_path):
    pages_dir = tmp_path / "pages"
    pages_dir.mkdir()
    page_file = pages_dir / "KV Cache.md"
    page_file.write_text("title:: KV Cache\nstatus:: unread\nprogress:: 0\n\n## Notes\n")
    update_property(tmp_path, "KV Cache", "progress", "50")
    content = page_file.read_text()
    assert "progress:: 50" in content
    assert "progress:: 0" not in content
    assert "## Notes" in content


def test_update_property_adds_if_missing(tmp_path):
    pages_dir = tmp_path / "pages"
    pages_dir.mkdir()
    page_file = pages_dir / "KV Cache.md"
    page_file.write_text("title:: KV Cache\nstatus:: unread\n\n## Notes\n")
    update_property(tmp_path, "KV Cache", "progress", "25")
    content = page_file.read_text()
    assert "progress:: 25" in content
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_page_reader.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'cli.page_reader'`

- [ ] **Step 3: Implement page_reader.py**

```python
# cli/page_reader.py
import re
from dataclasses import dataclass, field
from pathlib import Path

from cli.config import title_to_filename


@dataclass
class PageData:
    title: str = ""
    properties: dict[str, str] = field(default_factory=dict)
    body: str = ""
    file_path: Path | None = None


_PROP_RE = re.compile(r"^([a-zA-Z_-]+)::\s*(.*)$")


def parse_page(content: str) -> PageData:
    lines = content.split("\n")
    properties: dict[str, str] = {}
    body_start = 0

    for i, line in enumerate(lines):
        m = _PROP_RE.match(line)
        if m:
            properties[m.group(1)] = m.group(2).strip()
            body_start = i + 1
        elif line.strip() == "":
            body_start = i + 1
        else:
            break

    body = "\n".join(lines[body_start:])
    return PageData(
        title=properties.get("title", ""),
        properties=properties,
        body=body,
    )


def read_page(vault_path: Path, title: str) -> PageData | None:
    filename = title_to_filename(title)
    file_path = vault_path / "pages" / filename
    if not file_path.exists():
        return None
    page = parse_page(file_path.read_text())
    page.file_path = file_path
    return page


def list_pages(vault_path: Path, type_filter: str | None = None) -> list[PageData]:
    pages_dir = vault_path / "pages"
    if not pages_dir.exists():
        return []
    result = []
    for f in sorted(pages_dir.glob("*.md")):
        page = parse_page(f.read_text())
        page.file_path = f
        if type_filter is None or page.properties.get("type") == type_filter:
            result.append(page)
    return result


def update_property(vault_path: Path, title: str, key: str, value: str) -> None:
    filename = title_to_filename(title)
    file_path = vault_path / "pages" / filename
    content = file_path.read_text()
    lines = content.split("\n")

    found = False
    prop_end = 0
    for i, line in enumerate(lines):
        m = _PROP_RE.match(line)
        if m:
            prop_end = i + 1
            if m.group(1) == key:
                lines[i] = f"{key}:: {value}"
                found = True
                break
        elif line.strip() == "":
            continue
        else:
            break

    if not found:
        lines.insert(prop_end, f"{key}:: {value}")

    file_path.write_text("\n".join(lines))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_page_reader.py -v`
Expected: All 10 tests PASS

- [ ] **Step 5: Commit**

```bash
git add cli/page_reader.py tests/test_page_reader.py
git commit -m "feat: page reader — parse and update Logseq markdown properties"
```

---

### Task 3: Page Writer — Write Logseq Markdown Pages

**Files:**
- Create: `cli/page_writer.py`
- Create: `tests/test_page_writer.py`

**Interfaces:**
- Consumes: `title_to_filename(title: str) -> str` from `cli.config`, `read_page(vault_path: Path, title: str) -> PageData | None` and `list_pages(...)` from `cli.page_reader`
- Produces: `write_resource_page(vault_path: Path, metadata: dict, job: dict) -> Path` (returns path of written page), `write_concept_stub(vault_path: Path, concept: str, domain: str | None, topic: str | None, referenced_by: str) -> Path`, `write_domain_page(vault_path: Path, domain: str, topics: list[str]) -> Path`, `write_topic_page(vault_path: Path, topic: str, domain: str) -> Path`, `ensure_linked_pages(vault_path: Path, metadata: dict, title: str) -> None` (creates stubs, domain, topic pages as needed)

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_page_writer.py
from pathlib import Path
from datetime import date

import pytest

from cli.page_writer import (
    write_resource_page,
    write_concept_stub,
    write_domain_page,
    write_topic_page,
    ensure_linked_pages,
)
from cli.page_reader import parse_page, read_page


@pytest.fixture
def vault(tmp_path):
    (tmp_path / "pages").mkdir()
    return tmp_path


def make_metadata(**overrides):
    base = {
        "title": "Gemma 4 Technical Report",
        "summary": "A report about Gemma 4.",
        "medium": "paper",
        "complexity": "advanced",
        "size": "deep-dive",
        "domain": "ML/Infrastructure",
        "topic": "Inference Optimization",
        "concepts": ["MoE", "RLHF"],
        "prerequisites": ["Attention Mechanisms", "KV Cache"],
        "key_takeaways": ["Takeaway 1", "Takeaway 2"],
        "engagement_suggestion": "read",
    }
    base.update(overrides)
    return base


def make_job(**overrides):
    base = {
        "id": "20260708-143022-a1b2",
        "source": "https://arxiv.org/abs/2504.00958",
        "source_type": "url",
        "domain": None,
        "topic": None,
        "engagement": None,
        "tags": ["transformers", "inference"],
        "created_at": "2026-07-08T14:30:22",
        "status": "pending",
    }
    base.update(overrides)
    return base


def test_write_resource_page_full(vault):
    metadata = make_metadata()
    job = make_job()
    path = write_resource_page(vault, metadata, job)
    assert path.exists()
    page = parse_page(path.read_text())
    assert page.title == "Gemma 4 Technical Report"
    assert page.properties["type"] == "paper"
    assert page.properties["domain"] == "[[ML/Infrastructure]]"
    assert page.properties["topic"] == "[[Inference Optimization]]"
    assert page.properties["engagement"] == "read"
    assert page.properties["status"] == "unread"
    assert page.properties["progress"] == "0"
    assert page.properties["complexity"] == "advanced"
    assert page.properties["size"] == "deep-dive"
    assert page.properties["medium"] == "paper"
    assert page.properties["source"] == "https://arxiv.org/abs/2504.00958"
    assert "[[MoE]]" in page.properties["concepts"]
    assert "[[RLHF]]" in page.properties["concepts"]
    assert "[[Attention Mechanisms]]" in page.properties["prerequisites"]
    assert "[[KV Cache]]" in page.properties["prerequisites"]
    assert "transformers" in page.properties["tags"]
    assert "A report about Gemma 4." in page.body
    assert "Takeaway 1" in page.body
    assert "## My Notes" in page.body


def test_write_resource_page_job_overrides_metadata(vault):
    metadata = make_metadata(domain="ML/Training", engagement_suggestion="background")
    job = make_job(domain="ML/Infrastructure", engagement="read")
    path = write_resource_page(vault, metadata, job)
    page = parse_page(path.read_text())
    assert page.properties["domain"] == "[[ML/Infrastructure]]"
    assert page.properties["engagement"] == "read"


def test_write_resource_page_minimal_metadata(vault):
    metadata = {"title": "Quick Note"}
    job = make_job(source="/tmp/note.md", source_type="file", tags=[])
    path = write_resource_page(vault, metadata, job)
    page = parse_page(path.read_text())
    assert page.title == "Quick Note"
    assert page.properties["status"] == "unread"
    assert page.properties["progress"] == "0"


def test_write_concept_stub(vault):
    path = write_concept_stub(vault, "KV Cache", "ML/Infrastructure", "Inference Optimization", "Gemma 4 Technical Report")
    assert path.exists()
    page = parse_page(path.read_text())
    assert page.title == "KV Cache"
    assert page.properties["type"] == "concept"
    assert page.properties["status"] == "stub"
    assert page.properties["domain"] == "[[ML/Infrastructure]]"
    assert "[[Gemma 4 Technical Report]]" in page.properties["referenced-by"]


def test_write_concept_stub_appends_referenced_by(vault):
    write_concept_stub(vault, "KV Cache", "ML/Infrastructure", None, "Paper A")
    write_concept_stub(vault, "KV Cache", "ML/Infrastructure", None, "Paper B")
    page = read_page(vault, "KV Cache")
    assert "[[Paper A]]" in page.properties["referenced-by"]
    assert "[[Paper B]]" in page.properties["referenced-by"]


def test_write_domain_page(vault):
    path = write_domain_page(vault, "ML/Infrastructure", ["Inference Optimization", "Distributed Training"])
    page = parse_page(path.read_text())
    assert page.title == "ML/Infrastructure"
    assert page.properties["type"] == "domain"
    assert "[[Inference Optimization]]" in page.body
    assert "[[Distributed Training]]" in page.body


def test_write_domain_page_adds_topic(vault):
    write_domain_page(vault, "ML/Infrastructure", ["Inference Optimization"])
    write_domain_page(vault, "ML/Infrastructure", ["Distributed Training"])
    page = read_page(vault, "ML/Infrastructure")
    assert "[[Inference Optimization]]" in page.body
    assert "[[Distributed Training]]" in page.body


def test_write_topic_page(vault):
    path = write_topic_page(vault, "Inference Optimization", "ML/Infrastructure")
    page = parse_page(path.read_text())
    assert page.title == "Inference Optimization"
    assert page.properties["type"] == "topic"
    assert page.properties["domain"] == "[[ML/Infrastructure]]"


def test_ensure_linked_pages_creates_stubs(vault):
    metadata = make_metadata()
    ensure_linked_pages(vault, metadata, "Gemma 4 Technical Report")
    for concept in ["MoE", "RLHF", "Attention Mechanisms", "KV Cache"]:
        page = read_page(vault, concept)
        assert page is not None, f"Stub for {concept} not created"
        assert page.properties["type"] == "concept"
    domain_page = read_page(vault, "ML/Infrastructure")
    assert domain_page is not None
    topic_page = read_page(vault, "Inference Optimization")
    assert topic_page is not None


def test_ensure_linked_pages_skips_existing(vault):
    (vault / "pages" / "MoE.md").write_text("title:: MoE\ntype:: paper\nstatus:: completed\n")
    metadata = make_metadata(concepts=["MoE"], prerequisites=[])
    ensure_linked_pages(vault, metadata, "Gemma 4 Technical Report")
    page = read_page(vault, "MoE")
    assert page.properties["type"] == "paper"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_page_writer.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'cli.page_writer'`

- [ ] **Step 3: Implement page_writer.py**

```python
# cli/page_writer.py
from datetime import date
from pathlib import Path

from cli.config import title_to_filename
from cli.page_reader import read_page


def _format_link_list(items: list[str]) -> str:
    return ", ".join(f"[[{item}]]" for item in items)


def write_resource_page(vault_path: Path, metadata: dict, job: dict) -> Path:
    title = metadata["title"]
    domain = job.get("domain") or metadata.get("domain")
    topic = job.get("topic") or metadata.get("topic")
    engagement = job.get("engagement") or metadata.get("engagement_suggestion") or ""
    tags = job.get("tags", [])

    props = [
        f"title:: {title}",
        f"type:: {metadata.get('medium', 'article')}",
    ]
    if domain:
        props.append(f"domain:: [[{domain}]]")
    if topic:
        props.append(f"topic:: [[{topic}]]")
    if engagement:
        props.append(f"engagement:: {engagement}")
    props.append("status:: unread")
    props.append("progress:: 0")
    if metadata.get("complexity"):
        props.append(f"complexity:: {metadata['complexity']}")
    if metadata.get("size"):
        props.append(f"size:: {metadata['size']}")
    if metadata.get("medium"):
        props.append(f"medium:: {metadata['medium']}")
    prerequisites = metadata.get("prerequisites", [])
    if prerequisites:
        props.append(f"prerequisites:: {_format_link_list(prerequisites)}")
    concepts = metadata.get("concepts", [])
    if concepts:
        props.append(f"concepts:: {_format_link_list(concepts)}")
    if tags:
        props.append(f"tags:: {', '.join(tags)}")
    props.append(f"source:: {job['source']}")
    props.append(f"ingested:: [[{date.today().isoformat()}]]")

    body_parts = []
    if metadata.get("summary"):
        body_parts.append(f"## Summary\n{metadata['summary']}")
    takeaways = metadata.get("key_takeaways", [])
    if takeaways:
        items = "\n".join(f"- {t}" for t in takeaways)
        body_parts.append(f"## Key Takeaways\n{items}")
    if prerequisites:
        items = "\n".join(f"- [[{p}]]" for p in prerequisites)
        body_parts.append(f"## Prerequisites\n{items}")
    body_parts.append("## My Notes\n")

    content = "\n".join(props) + "\n\n" + "\n\n".join(body_parts)

    pages_dir = vault_path / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    file_path = pages_dir / title_to_filename(title)
    file_path.write_text(content)
    return file_path


def write_concept_stub(
    vault_path: Path,
    concept: str,
    domain: str | None,
    topic: str | None,
    referenced_by: str,
) -> Path:
    existing = read_page(vault_path, concept)
    if existing is not None:
        ref_prop = existing.properties.get("referenced-by", "")
        link = f"[[{referenced_by}]]"
        if link not in ref_prop:
            new_ref = f"{ref_prop}, {link}" if ref_prop else link
            lines = existing.file_path.read_text().split("\n")
            updated = False
            for i, line in enumerate(lines):
                if line.startswith("referenced-by::"):
                    lines[i] = f"referenced-by:: {new_ref}"
                    updated = True
                    break
            if not updated:
                for i, line in enumerate(lines):
                    if line.strip() == "" or (not line.startswith(("title::", "type::", "status::", "domain::", "topic::"))):
                        if not line.strip().startswith("#") and line.strip() == "":
                            lines.insert(i, f"referenced-by:: {new_ref}")
                            break
                else:
                    lines.append(f"referenced-by:: {new_ref}")
            existing.file_path.write_text("\n".join(lines))
        return existing.file_path

    props = [
        f"title:: {concept}",
        "type:: concept",
        "status:: stub",
    ]
    if domain:
        props.append(f"domain:: [[{domain}]]")
    if topic:
        props.append(f"topic:: [[{topic}]]")
    props.append(f"referenced-by:: [[{referenced_by}]]")

    content = "\n".join(props) + "\n\n## About\nAuto-generated stub. This concept is a prerequisite for items in your learning queue.\n"

    pages_dir = vault_path / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    file_path = pages_dir / title_to_filename(concept)
    file_path.write_text(content)
    return file_path


def write_domain_page(vault_path: Path, domain: str, topics: list[str]) -> Path:
    existing = read_page(vault_path, domain)
    if existing is not None:
        content = existing.file_path.read_text()
        for topic in topics:
            link = f"[[{topic}]]"
            if link not in content:
                content = content.rstrip() + f"\n- {link}\n"
        existing.file_path.write_text(content)
        return existing.file_path

    props = [f"title:: {domain}", "type:: domain"]
    topic_list = "\n".join(f"- [[{t}]]" for t in topics)
    content = "\n".join(props) + f"\n\n## Topics\n{topic_list}\n"

    pages_dir = vault_path / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    file_path = pages_dir / title_to_filename(domain)
    file_path.write_text(content)
    return file_path


def write_topic_page(vault_path: Path, topic: str, domain: str) -> Path:
    existing = read_page(vault_path, topic)
    if existing is not None:
        return existing.file_path

    props = [f"title:: {topic}", "type:: topic", f"domain:: [[{domain}]]"]
    content = "\n".join(props) + "\n"

    pages_dir = vault_path / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    file_path = pages_dir / title_to_filename(topic)
    file_path.write_text(content)
    return file_path


def ensure_linked_pages(vault_path: Path, metadata: dict, title: str) -> None:
    domain = metadata.get("domain")
    topic = metadata.get("topic")

    all_concepts = list(set(metadata.get("concepts", []) + metadata.get("prerequisites", [])))
    for concept in all_concepts:
        existing = read_page(vault_path, concept)
        if existing is None:
            write_concept_stub(vault_path, concept, domain, topic, title)
        elif existing.properties.get("type") == "concept":
            write_concept_stub(vault_path, concept, domain, topic, title)

    if domain:
        topics_list = [topic] if topic else []
        write_domain_page(vault_path, domain, topics_list)

    if topic and domain:
        write_topic_page(vault_path, topic, domain)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_page_writer.py -v`
Expected: All 12 tests PASS

- [ ] **Step 5: Commit**

```bash
git add cli/page_writer.py tests/test_page_writer.py
git commit -m "feat: page writer — write resource, stub, domain, and topic pages"
```

---

### Task 4: Priority Engine

**Files:**
- Create: `cli/priority.py`
- Create: `tests/test_priority.py`

**Interfaces:**
- Consumes: `Config` from `cli.config`, `PageData` and `list_pages(vault_path: Path, type_filter: str | None) -> list[PageData]` from `cli.page_reader`, `update_property(vault_path: Path, title: str, key: str, value: str) -> None` from `cli.page_reader`
- Produces: `compute_priority(page: PageData, all_pages: list[PageData], config: Config) -> int` (returns 0-100), `recompute_all(vault_path: Path, config: Config) -> int` (returns count of pages updated)

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_priority.py
from datetime import date, timedelta

import pytest

from cli.page_reader import PageData, read_page
from cli.priority import compute_priority, recompute_all, _parse_links
from cli.config import Config
from pathlib import Path


def make_config(**overrides):
    defaults = {
        "vault_path": Path("/tmp"),
        "domain_weights": {"ML/Infrastructure": 0.9, "Systems": 0.5},
        "topic_weights": {"Inference Optimization": 0.95},
        "default_weight": 0.5,
    }
    defaults.update(overrides)
    return Config(**defaults)


def make_page(title, **props):
    properties = {"title": title}
    properties.update(props)
    return PageData(title=title, properties=properties)


def test_parse_links():
    assert _parse_links("[[A]], [[B]], [[C]]") == ["A", "B", "C"]
    assert _parse_links("[[A]]") == ["A"]
    assert _parse_links("") == []
    assert _parse_links("no links") == []


def test_compute_priority_basic():
    config = make_config()
    page = make_page(
        "Test Page",
        type="paper",
        domain="[[ML/Infrastructure]]",
        topic="[[Inference Optimization]]",
        concepts="[[A]], [[B]]",
        prerequisites="",
        complexity="beginner",
        engagement="background",
        ingested=f"[[{date.today().isoformat()}]]",
    )
    other = make_page("Other", concepts="[[A]], [[C]]", prerequisites="[[Test Page]]")
    score = compute_priority(page, [page, other], config)
    assert 0 <= score <= 100


def test_high_overlap_increases_priority():
    config = make_config()
    shared_page = make_page("Shared", concepts="[[A]], [[B]], [[C]]",
                            domain="[[Systems]]", ingested=f"[[{date.today().isoformat()}]]",
                            complexity="intermediate")
    isolated_page = make_page("Isolated", concepts="[[Z]]",
                              domain="[[Systems]]", ingested=f"[[{date.today().isoformat()}]]",
                              complexity="intermediate")
    others = [
        make_page("O1", concepts="[[A]], [[B]]"),
        make_page("O2", concepts="[[B]], [[C]]"),
        make_page("O3", concepts="[[A]]"),
    ]
    all_pages = [shared_page, isolated_page] + others
    shared_score = compute_priority(shared_page, all_pages, config)
    isolated_score = compute_priority(isolated_page, all_pages, config)
    assert shared_score > isolated_score


def test_prerequisite_demand_increases_priority():
    config = make_config()
    needed = make_page("Foundational", concepts="[[X]]",
                       domain="[[Systems]]", ingested=f"[[{date.today().isoformat()}]]",
                       complexity="beginner")
    not_needed = make_page("Niche", concepts="[[Y]]",
                           domain="[[Systems]]", ingested=f"[[{date.today().isoformat()}]]",
                           complexity="beginner")
    dependents = [
        make_page("D1", prerequisites="[[Foundational]]"),
        make_page("D2", prerequisites="[[Foundational]]"),
        make_page("D3", prerequisites="[[Foundational]]"),
    ]
    all_pages = [needed, not_needed] + dependents
    needed_score = compute_priority(needed, all_pages, config)
    not_needed_score = compute_priority(not_needed, all_pages, config)
    assert needed_score > not_needed_score


def test_domain_weight_affects_priority():
    config = make_config()
    high_domain = make_page("A", domain="[[ML/Infrastructure]]",
                            ingested=f"[[{date.today().isoformat()}]]", complexity="intermediate")
    low_domain = make_page("B", domain="[[Systems]]",
                           ingested=f"[[{date.today().isoformat()}]]", complexity="intermediate")
    score_high = compute_priority(high_domain, [high_domain, low_domain], config)
    score_low = compute_priority(low_domain, [high_domain, low_domain], config)
    assert score_high > score_low


def test_recompute_all(tmp_path):
    config = make_config(vault_path=tmp_path)
    pages_dir = tmp_path / "pages"
    pages_dir.mkdir()
    (pages_dir / "A.md").write_text(
        f"title:: A\ntype:: paper\ndomain:: [[ML/Infrastructure]]\ncomplexity:: beginner\n"
        f"ingested:: [[{date.today().isoformat()}]]\nconcepts:: [[X]]\n"
    )
    (pages_dir / "B.md").write_text(
        f"title:: B\ntype:: paper\ndomain:: [[Systems]]\ncomplexity:: advanced\n"
        f"ingested:: [[{date.today().isoformat()}]]\nprerequisites:: [[A]]\n"
    )
    count = recompute_all(tmp_path, config)
    assert count == 2
    page_a = read_page(tmp_path, "A")
    page_b = read_page(tmp_path, "B")
    assert "priority" in page_a.properties
    assert "priority" in page_b.properties
    assert int(page_a.properties["priority"]) > 0
    assert int(page_b.properties["priority"]) > 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_priority.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'cli.priority'`

- [ ] **Step 3: Implement priority.py**

```python
# cli/priority.py
import re
from datetime import date, timedelta
from pathlib import Path

from cli.config import Config
from cli.page_reader import PageData, list_pages, update_property


_LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def _parse_links(value: str) -> list[str]:
    return _LINK_RE.findall(value)


def _strip_link(value: str) -> str:
    m = _LINK_RE.match(value.strip())
    return m.group(1) if m else value.strip()


def compute_priority(page: PageData, all_pages: list[PageData], config: Config) -> int:
    my_concepts = set(_parse_links(page.properties.get("concepts", "")))
    my_prereqs = set(_parse_links(page.properties.get("prerequisites", "")))
    my_all = my_concepts | my_prereqs
    title = page.title

    overlap_count = 0
    prereq_demand = 0
    for other in all_pages:
        if other.title == title:
            continue
        other_concepts = set(_parse_links(other.properties.get("concepts", "")))
        other_prereqs = set(_parse_links(other.properties.get("prerequisites", "")))
        overlap_count += len(my_all & (other_concepts | other_prereqs))
        if title in other_prereqs or my_concepts & other_prereqs:
            prereq_demand += 1

    max_others = max(len(all_pages) - 1, 1)
    overlap_score = min(overlap_count / (max_others * 2), 1.0) * 25
    prereq_score = min(prereq_demand / max_others, 1.0) * 25

    domain_raw = _strip_link(page.properties.get("domain", ""))
    domain_w = config.domain_weights.get(domain_raw, config.default_weight)
    domain_score = domain_w * 20

    topic_raw = _strip_link(page.properties.get("topic", ""))
    topic_w = config.topic_weights.get(topic_raw, config.default_weight)
    topic_score = topic_w * 15

    ingested_raw = page.properties.get("ingested", "")
    recency_score = 0.0
    ingested_date_str = _LINK_RE.search(ingested_raw)
    if ingested_date_str:
        try:
            ing_date = date.fromisoformat(ingested_date_str.group(1))
            days_old = (date.today() - ing_date).days
            recency_score = max(0, 1.0 - days_old / 90) * 5
        except ValueError:
            pass

    complexity = page.properties.get("complexity", "intermediate")
    complexity_map = {"beginner": 5, "intermediate": 2.5, "advanced": 0}
    inverse_complexity_score = complexity_map.get(complexity, 2.5)

    engagement = page.properties.get("engagement", "")
    engagement_map = {"background": 5, "read": 2.5, "implement": 2.5}
    engagement_score = engagement_map.get(engagement, 2.5)

    total = (
        overlap_score
        + prereq_score
        + domain_score
        + topic_score
        + recency_score
        + inverse_complexity_score
        + engagement_score
    )
    return min(round(total), 100)


def recompute_all(vault_path: Path, config: Config) -> int:
    resource_types = {"paper", "article", "tweet", "video", "docs", "concept"}
    all_pages = [
        p for p in list_pages(vault_path)
        if p.properties.get("type") in resource_types
    ]
    for page in all_pages:
        score = compute_priority(page, all_pages, config)
        update_property(vault_path, page.title, "priority", str(score))
    return len(all_pages)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_priority.py -v`
Expected: All 7 tests PASS

- [ ] **Step 5: Commit**

```bash
git add cli/priority.py tests/test_priority.py
git commit -m "feat: priority engine — compute scores from overlap, demand, and config weights"
```

---

### Task 5: Progress Tracking + Dashboard

**Files:**
- Create: `cli/progress.py`
- Create: `tests/test_progress.py`

**Interfaces:**
- Consumes: `Config` from `cli.config`, `PageData`, `list_pages(...)`, `read_page(...)`, `update_property(...)` from `cli.page_reader`, `_parse_links(value: str) -> list[str]` from `cli.priority`, `recompute_all(...)` from `cli.priority`
- Produces: `update_progress(vault_path: Path, title: str, value: int, config: Config) -> None`, `mark_done(vault_path: Path, title: str, config: Config) -> None`, `find_page_by_title(vault_path: Path, query: str) -> str | None` (fuzzy match, returns exact title or None), `generate_dashboard(vault_path: Path, config: Config) -> Path`

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_progress.py
from pathlib import Path
from datetime import date

import pytest

from cli.progress import update_progress, mark_done, find_page_by_title, generate_dashboard
from cli.page_reader import read_page
from cli.config import Config


def make_config(vault_path):
    return Config(
        vault_path=vault_path,
        domain_weights={"ML/Infrastructure": 0.9},
        topic_weights={"Inference Optimization": 0.95},
        default_weight=0.5,
    )


@pytest.fixture
def vault(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    return tmp_path


def write_page(vault, title, **props):
    from cli.config import title_to_filename
    defaults = {"type": "paper", "status": "unread", "progress": "0"}
    defaults.update(props)
    lines = [f"title:: {title}"]
    for k, v in defaults.items():
        lines.append(f"{k}:: {v}")
    (vault / "pages" / title_to_filename(title)).write_text("\n".join(lines) + "\n")


def test_update_progress(vault):
    write_page(vault, "Test Paper")
    config = make_config(vault)
    update_progress(vault, "Test Paper", 50, config)
    page = read_page(vault, "Test Paper")
    assert page.properties["progress"] == "50"
    assert page.properties["status"] == "in-progress"


def test_update_progress_to_100_completes(vault):
    write_page(vault, "Test Paper")
    config = make_config(vault)
    update_progress(vault, "Test Paper", 100, config)
    page = read_page(vault, "Test Paper")
    assert page.properties["progress"] == "100"
    assert page.properties["status"] == "completed"


def test_mark_done(vault):
    write_page(vault, "Test Paper", status="in-progress", progress="40")
    config = make_config(vault)
    mark_done(vault, "Test Paper", config)
    page = read_page(vault, "Test Paper")
    assert page.properties["progress"] == "100"
    assert page.properties["status"] == "completed"


def test_find_page_by_title_exact(vault):
    write_page(vault, "Gemma 4 Technical Report")
    result = find_page_by_title(vault, "Gemma 4 Technical Report")
    assert result == "Gemma 4 Technical Report"


def test_find_page_by_title_fuzzy(vault):
    write_page(vault, "Gemma 4 Technical Report")
    result = find_page_by_title(vault, "gemma 4 report")
    assert result == "Gemma 4 Technical Report"


def test_find_page_by_title_no_match(vault):
    write_page(vault, "Gemma 4 Technical Report")
    result = find_page_by_title(vault, "Completely Unrelated Topic")
    assert result is None


def test_generate_dashboard(vault):
    write_page(vault, "Paper A", domain="[[ML/Infrastructure]]", topic="[[Inference Optimization]]",
               status="completed", progress="100", type="paper")
    write_page(vault, "Paper B", domain="[[ML/Infrastructure]]", topic="[[Inference Optimization]]",
               status="unread", progress="0", type="paper")
    write_page(vault, "Paper C", domain="[[ML/Infrastructure]]", topic="[[Inference Optimization]]",
               status="in-progress", progress="50", type="paper")
    write_page(vault, "Stub X", type="concept", status="stub", **{"referenced-by": "[[Paper A]]"})

    config = make_config(vault)
    path = generate_dashboard(vault, config)
    assert path.exists()
    content = path.read_text()
    assert "Learning Dashboard" in content
    assert "ML/Infrastructure" in content
    assert "Inference Optimization" in content
    assert "Knowledge Gaps" in content
    assert "Stub X" in content
    assert "Queue" in content


def test_generate_dashboard_empty_vault(vault):
    config = make_config(vault)
    path = generate_dashboard(vault, config)
    assert path.exists()
    content = path.read_text()
    assert "Learning Dashboard" in content
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_progress.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'cli.progress'`

- [ ] **Step 3: Implement progress.py**

```python
# cli/progress.py
from datetime import date
from pathlib import Path

from thefuzz import fuzz

from cli.config import Config, title_to_filename
from cli.page_reader import PageData, list_pages, read_page, update_property
from cli.priority import _parse_links, recompute_all


def find_page_by_title(vault_path: Path, query: str) -> str | None:
    pages = list_pages(vault_path)
    if not pages:
        return None
    for page in pages:
        if page.title.lower() == query.lower():
            return page.title
    best_score = 0
    best_title = None
    for page in pages:
        score = fuzz.partial_ratio(query.lower(), page.title.lower())
        if score > best_score:
            best_score = score
            best_title = page.title
    if best_score >= 70:
        return best_title
    return None


def update_progress(vault_path: Path, title: str, value: int, config: Config) -> None:
    update_property(vault_path, title, "progress", str(value))
    if value >= 100:
        update_property(vault_path, title, "status", "completed")
    elif value > 0:
        update_property(vault_path, title, "status", "in-progress")
    recompute_all(vault_path, config)


def mark_done(vault_path: Path, title: str, config: Config) -> None:
    update_progress(vault_path, title, 100, config)


def generate_dashboard(vault_path: Path, config: Config) -> Path:
    all_pages = list_pages(vault_path)
    resource_types = {"paper", "article", "tweet", "video", "docs"}

    resources = [p for p in all_pages if p.properties.get("type") in resource_types]
    stubs = [p for p in all_pages if p.properties.get("status") == "stub"]

    domain_stats: dict[str, dict] = {}
    topic_stats: dict[str, dict] = {}

    for page in resources:
        domain_raw = page.properties.get("domain", "")
        domain = domain_raw.strip()
        if domain:
            if domain not in domain_stats:
                domain_stats[domain] = {"items": 0, "done": 0, "in_progress": 0}
            domain_stats[domain]["items"] += 1
            if page.properties.get("status") == "completed":
                domain_stats[domain]["done"] += 1
            elif page.properties.get("status") == "in-progress":
                domain_stats[domain]["in_progress"] += 1

        topic_raw = page.properties.get("topic", "")
        topic = topic_raw.strip()
        if topic:
            key = (topic, domain)
            if key not in topic_stats:
                topic_stats[key] = {"items": 0, "done": 0}
            topic_stats[key]["items"] += 1
            if page.properties.get("status") == "completed":
                topic_stats[key]["done"] += 1

    lines = [
        f"title:: Learning Dashboard",
        "type:: dashboard",
        f"generated:: [[{date.today().isoformat()}]]",
        "",
        "## Domain Progress",
        "| Domain | Items | Done | In Progress | Progress |",
        "|--------|-------|------|-------------|----------|",
    ]
    for domain, stats in sorted(domain_stats.items()):
        pct = round(stats["done"] / stats["items"] * 100) if stats["items"] else 0
        lines.append(f"| {domain} | {stats['items']} | {stats['done']} | {stats['in_progress']} | {pct}% |")

    lines.extend(["", "## Topic Progress",
                   "| Topic | Domain | Items | Done | Progress |",
                   "|-------|--------|-------|------|----------|"])
    for (topic, domain), stats in sorted(topic_stats.items()):
        pct = round(stats["done"] / stats["items"] * 100) if stats["items"] else 0
        lines.append(f"| {topic} | {domain} | {stats['items']} | {stats['done']} | {pct}% |")

    if stubs:
        lines.extend(["", "## Knowledge Gaps (Stubs)"])
        for stub in stubs:
            ref = stub.properties.get("referenced-by", "")
            lines.append(f"- [[{stub.title}]] — needed by: {ref}")

    queue = sorted(resources,
                   key=lambda p: int(p.properties.get("priority", "0")),
                   reverse=True)
    queue = [p for p in queue if p.properties.get("status") != "completed"][:10]
    if queue:
        lines.extend(["", "## Queue (Top 10 by Priority)"])
        for i, page in enumerate(queue, 1):
            pri = page.properties.get("priority", "?")
            eng = page.properties.get("engagement", "?")
            comp = page.properties.get("complexity", "?")
            lines.append(f"{i}. [[{page.title}]] (priority: {pri}, {eng}, {comp})")

    content = "\n".join(lines) + "\n"
    pages_dir = vault_path / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    path = pages_dir / "Learning Dashboard.md"
    path.write_text(content)
    return path
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_progress.py -v`
Expected: All 8 tests PASS

- [ ] **Step 5: Commit**

```bash
git add cli/progress.py tests/test_progress.py
git commit -m "feat: progress tracking and dashboard generation"
```

---

### Task 6: CLI Commands — `lpt add`, `lpt status`, `lpt write`, `lpt init`

**Files:**
- Modify: `cli/main.py`
- Create: `tests/test_cli.py`

**Interfaces:**
- Consumes: `load_config(...)` from `cli.config`, `write_resource_page(...)` and `ensure_linked_pages(...)` from `cli.page_writer`, `recompute_all(...)` from `cli.priority`, `update_progress(...)`, `mark_done(...)`, `find_page_by_title(...)`, `generate_dashboard(...)` from `cli.progress`
- Produces: Click CLI group `cli` with commands: `add`, `status`, `write`, `init`, `progress`, `done`, `dashboard`, `recompute`

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_cli.py
import json
import os
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from cli.main import cli


@pytest.fixture
def project(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "pages").mkdir()
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    processed = tmp_path / "processed"
    processed.mkdir()
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.dump({
        "vault_path": str(vault),
        "domain_weights": {"ML/Infrastructure": 0.9},
        "topic_weights": {},
        "default_weight": 0.5,
    }))
    return tmp_path


def run(project, args, env=None):
    runner = CliRunner()
    full_env = {"LPT_CONFIG": str(project / "config.yaml"),
                "LPT_INBOX": str(project / "inbox"),
                "LPT_PROCESSED": str(project / "processed")}
    if env:
        full_env.update(env)
    return runner.invoke(cli, args, env=full_env, catch_exceptions=False)


def test_add_url(project):
    result = run(project, ["add", "https://arxiv.org/abs/2504.00958", "--tag", "ml"])
    assert result.exit_code == 0
    assert "Added" in result.output
    inbox = project / "inbox"
    jobs = list(inbox.glob("*.json"))
    assert len(jobs) == 1
    job = json.loads(jobs[0].read_text())
    assert job["source"] == "https://arxiv.org/abs/2504.00958"
    assert job["source_type"] == "url"
    assert "ml" in job["tags"]


def test_add_local_file(project):
    local_file = project / "test.pdf"
    local_file.write_text("fake pdf")
    result = run(project, ["add", str(local_file)])
    assert result.exit_code == 0
    inbox = project / "inbox"
    jobs = list(inbox.glob("*.json"))
    assert len(jobs) == 1
    job = json.loads(jobs[0].read_text())
    assert job["source_type"] == "file"


def test_add_local_file_not_found(project):
    result = run(project, ["add", "/nonexistent/file.pdf"])
    assert result.exit_code != 0
    assert "not found" in result.output.lower() or "does not exist" in result.output.lower()


def test_add_with_domain_topic_engagement(project):
    result = run(project, ["add", "https://example.com",
                           "--domain", "ML/Infrastructure",
                           "--topic", "Inference",
                           "--engagement", "implement"])
    assert result.exit_code == 0
    inbox = project / "inbox"
    job = json.loads(list(inbox.glob("*.json"))[0].read_text())
    assert job["domain"] == "ML/Infrastructure"
    assert job["topic"] == "Inference"
    assert job["engagement"] == "implement"


def test_status_empty(project):
    result = run(project, ["status"])
    assert result.exit_code == 0
    assert "0" in result.output


def test_status_with_jobs(project):
    job = {"id": "test-001", "source": "https://example.com", "status": "pending"}
    (project / "inbox" / "test-001.json").write_text(json.dumps(job))
    result_file = {"title": "Example"}
    (project / "inbox" / "test-001.result.json").write_text(json.dumps(result_file))
    result = run(project, ["status"])
    assert result.exit_code == 0


def test_write_single_job(project):
    job = {
        "id": "20260708-143022-a1b2",
        "source": "https://example.com/paper",
        "source_type": "url",
        "domain": None,
        "topic": None,
        "engagement": None,
        "tags": ["ml"],
        "created_at": "2026-07-08T14:30:22",
        "status": "pending",
    }
    result_data = {
        "title": "Example Paper",
        "summary": "A paper.",
        "medium": "paper",
        "complexity": "beginner",
        "size": "quick-read",
        "domain": "ML/Infrastructure",
        "topic": "Inference Optimization",
        "concepts": ["A"],
        "prerequisites": [],
        "key_takeaways": ["T1"],
        "engagement_suggestion": "read",
    }
    (project / "inbox" / "20260708-143022-a1b2.json").write_text(json.dumps(job))
    (project / "inbox" / "20260708-143022-a1b2.result.json").write_text(json.dumps(result_data))
    result = run(project, ["write", "20260708-143022-a1b2"])
    assert result.exit_code == 0
    vault = project / "vault"
    assert (vault / "pages" / "Example Paper.md").exists()
    assert (project / "processed" / "20260708-143022-a1b2.json").exists()
    assert not (project / "inbox" / "20260708-143022-a1b2.json").exists()


def test_write_missing_result(project):
    job = {"id": "test-002", "source": "https://example.com", "status": "pending"}
    (project / "inbox" / "test-002.json").write_text(json.dumps(job))
    result = run(project, ["write", "test-002"])
    assert result.exit_code != 0
    assert "result" in result.output.lower()


def test_init(project):
    vault = project / "vault"
    result = run(project, ["init"])
    assert result.exit_code == 0
    assert (vault / "pages" / "Learning Queue.md").exists()
    content = (vault / "pages" / "Learning Queue.md").read_text()
    assert "{{query" in content


def test_init_idempotent(project):
    run(project, ["init"])
    result = run(project, ["init"])
    assert result.exit_code == 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_cli.py -v`
Expected: FAIL — commands not yet implemented

- [ ] **Step 3: Implement cli/main.py**

```python
# cli/main.py
import json
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path

import click

from cli.config import load_config, title_to_filename
from cli.page_reader import read_page
from cli.page_writer import write_resource_page, ensure_linked_pages
from cli.priority import recompute_all
from cli.progress import update_progress, mark_done, find_page_by_title, generate_dashboard


def _get_config():
    config_path = os.environ.get("LPT_CONFIG", "config.yaml")
    return load_config(config_path)


def _get_inbox():
    return Path(os.environ.get("LPT_INBOX", "inbox"))


def _get_processed():
    return Path(os.environ.get("LPT_PROCESSED", "processed"))


@click.group()
def cli():
    pass


@cli.command()
@click.argument("source")
@click.option("--domain", default=None)
@click.option("--topic", default=None)
@click.option("--engagement", type=click.Choice(["read", "implement", "background"]), default=None)
@click.option("--tag", multiple=True)
def add(source, domain, topic, engagement, tag):
    is_url = source.startswith("http://") or source.startswith("https://")
    if not is_url:
        source_path = Path(source)
        if not source_path.exists():
            raise click.ClickException(f"File does not exist: {source}")
        source = str(source_path.resolve())

    now = datetime.now()
    job_id = f"{now.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:4]}"
    job = {
        "id": job_id,
        "source": source,
        "source_type": "url" if is_url else "file",
        "domain": domain,
        "topic": topic,
        "engagement": engagement,
        "tags": list(tag),
        "created_at": now.isoformat(timespec="seconds"),
        "status": "pending",
    }
    inbox = _get_inbox()
    inbox.mkdir(parents=True, exist_ok=True)
    job_file = inbox / f"{job_id}.json"
    job_file.write_text(json.dumps(job, indent=2))
    click.echo(f"Added {job_id} to inbox")


@cli.command()
def status():
    inbox = _get_inbox()
    processed = _get_processed()
    inbox.mkdir(parents=True, exist_ok=True)
    processed.mkdir(parents=True, exist_ok=True)

    jobs = list(inbox.glob("*.json"))
    job_files = [j for j in jobs if not j.name.endswith(".result.json")]
    result_files = [j for j in jobs if j.name.endswith(".result.json")]
    processed_files = list(processed.glob("*.json"))

    pending = len([j for j in job_files if not (inbox / f"{j.stem}.result.json").exists()])
    ready = len(result_files)
    done = len([p for p in processed_files if not p.name.endswith(".result.json")])

    click.echo(f"Pending (no result):  {pending}")
    click.echo(f"Ready to write:       {ready}")
    click.echo(f"Processed:            {done}")


@cli.command("write")
@click.argument("job_id", required=False)
@click.option("--all", "write_all", is_flag=True)
def write_cmd(job_id, write_all):
    config = _get_config()
    inbox = _get_inbox()
    processed = _get_processed()
    processed.mkdir(parents=True, exist_ok=True)

    if write_all:
        result_files = list(inbox.glob("*.result.json"))
        if not result_files:
            click.echo("No result files to process")
            return
        for rf in result_files:
            jid = rf.name.replace(".result.json", "")
            _write_single(jid, inbox, processed, config)
        return

    if not job_id:
        raise click.ClickException("Provide a job ID or use --all")

    _write_single(job_id, inbox, processed, config)


def _write_single(job_id: str, inbox: Path, processed: Path, config):
    job_file = inbox / f"{job_id}.json"
    result_file = inbox / f"{job_id}.result.json"

    if not result_file.exists():
        raise click.ClickException(f"No result file for {job_id}. Run the processor first.")

    job = json.loads(job_file.read_text()) if job_file.exists() else {"source": "unknown", "tags": []}
    metadata = json.loads(result_file.read_text())

    page_path = write_resource_page(config.vault_path, metadata, job)
    ensure_linked_pages(config.vault_path, metadata, metadata["title"])
    recompute_all(config.vault_path, config)

    shutil.move(str(job_file), str(processed / job_file.name))
    shutil.move(str(result_file), str(processed / result_file.name))
    click.echo(f"Wrote page: {page_path.name}")


@cli.command()
def init():
    config = _get_config()
    pages_dir = config.vault_path / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    queue_page = pages_dir / "Learning Queue.md"
    content = """title:: Learning Queue
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
"""
    queue_page.write_text(content)
    click.echo(f"Initialized vault at {config.vault_path}")


@cli.command("progress")
@click.argument("title")
@click.argument("value", type=int)
def progress_cmd(title, value):
    config = _get_config()
    matched = find_page_by_title(config.vault_path, title)
    if not matched:
        raise click.ClickException(f"No page found matching '{title}'")
    update_progress(config.vault_path, matched, value, config)
    click.echo(f"Updated '{matched}' progress to {value}")


@cli.command()
@click.argument("title")
def done(title):
    config = _get_config()
    matched = find_page_by_title(config.vault_path, title)
    if not matched:
        raise click.ClickException(f"No page found matching '{title}'")
    mark_done(config.vault_path, matched, config)
    click.echo(f"Marked '{matched}' as completed")


@cli.command()
def dashboard():
    config = _get_config()
    path = generate_dashboard(config.vault_path, config)
    click.echo(f"Dashboard written to {path}")


@cli.command()
def recompute():
    config = _get_config()
    count = recompute_all(config.vault_path, config)
    click.echo(f"Recomputed priorities for {count} pages")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_cli.py -v`
Expected: All 11 tests PASS

- [ ] **Step 5: Run all tests together**

Run: `python -m pytest tests/ -v`
Expected: All tests across all files PASS

- [ ] **Step 6: Commit**

```bash
git add cli/main.py tests/test_cli.py
git commit -m "feat: CLI commands — add, status, write, init, progress, done, dashboard, recompute"
```

---

### Task 7: Integration Test — End-to-End Flow

**Files:**
- Create: `tests/test_integration.py`

**Interfaces:**
- Consumes: all modules
- Produces: no new code — validates the full flow works together

- [ ] **Step 1: Write the integration test**

```python
# tests/test_integration.py
import json
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from cli.main import cli
from cli.page_reader import read_page, list_pages


@pytest.fixture
def full_project(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "pages").mkdir()
    for d in ["inbox", "processed", "failed"]:
        (tmp_path / d).mkdir()
    config = {
        "vault_path": str(vault),
        "domain_weights": {"ML/Infrastructure": 0.9, "Systems": 0.5},
        "topic_weights": {"Inference Optimization": 0.95, "Caching": 0.7},
        "default_weight": 0.5,
    }
    (tmp_path / "config.yaml").write_text(yaml.dump(config))
    return tmp_path


def env(project):
    return {
        "LPT_CONFIG": str(project / "config.yaml"),
        "LPT_INBOX": str(project / "inbox"),
        "LPT_PROCESSED": str(project / "processed"),
    }


def test_full_flow(full_project):
    runner = CliRunner()
    e = env(full_project)
    vault = full_project / "vault"

    # 1. Init
    result = runner.invoke(cli, ["init"], env=e, catch_exceptions=False)
    assert result.exit_code == 0
    assert (vault / "pages" / "Learning Queue.md").exists()

    # 2. Add two items
    result = runner.invoke(cli, ["add", "https://example.com/gemma4", "--domain", "ML/Infrastructure",
                                  "--topic", "Inference Optimization", "--tag", "llm"], env=e, catch_exceptions=False)
    assert result.exit_code == 0

    result = runner.invoke(cli, ["add", "https://example.com/kvcache", "--tag", "caching"], env=e, catch_exceptions=False)
    assert result.exit_code == 0

    # 3. Simulate processor output for both jobs
    inbox = full_project / "inbox"
    jobs = sorted(inbox.glob("*.json"))
    assert len(jobs) == 2

    job1 = json.loads(jobs[0].read_text())
    result1 = {
        "title": "Gemma 4 Technical Report",
        "summary": "A technical report.",
        "medium": "paper",
        "complexity": "advanced",
        "size": "deep-dive",
        "domain": "ML/Infrastructure",
        "topic": "Inference Optimization",
        "concepts": ["MoE", "RLHF"],
        "prerequisites": ["KV Cache", "Attention Mechanisms"],
        "key_takeaways": ["Key finding"],
        "engagement_suggestion": "read",
    }
    (inbox / f"{job1['id']}.result.json").write_text(json.dumps(result1))

    job2 = json.loads(jobs[1].read_text())
    result2 = {
        "title": "Understanding KV Cache",
        "summary": "Deep dive into KV cache.",
        "medium": "article",
        "complexity": "intermediate",
        "size": "medium",
        "domain": "ML/Infrastructure",
        "topic": "Caching",
        "concepts": ["KV Cache"],
        "prerequisites": ["Attention Mechanisms"],
        "key_takeaways": ["How caching works"],
        "engagement_suggestion": "read",
    }
    (inbox / f"{job2['id']}.result.json").write_text(json.dumps(result2))

    # 4. Write pages
    result = runner.invoke(cli, ["write", "--all"], env=e, catch_exceptions=False)
    assert result.exit_code == 0

    # Verify pages created
    gemma_page = read_page(vault, "Gemma 4 Technical Report")
    assert gemma_page is not None
    assert gemma_page.properties["type"] == "paper"
    assert "[[KV Cache]]" in gemma_page.properties["prerequisites"]

    kv_article = read_page(vault, "Understanding KV Cache")
    assert kv_article is not None

    # Verify stubs created
    attn_stub = read_page(vault, "Attention Mechanisms")
    assert attn_stub is not None
    assert attn_stub.properties["status"] == "stub"

    # Verify domain and topic pages
    domain_page = read_page(vault, "ML/Infrastructure")
    assert domain_page is not None

    # Verify jobs moved to processed
    assert len(list(inbox.glob("*.json"))) == 0
    assert len(list((full_project / "processed").glob("*.json"))) == 4  # 2 jobs + 2 results

    # 5. Check status
    result = runner.invoke(cli, ["status"], env=e, catch_exceptions=False)
    assert result.exit_code == 0

    # 6. Update progress
    result = runner.invoke(cli, ["progress", "Understanding KV Cache", "50"], env=e, catch_exceptions=False)
    assert result.exit_code == 0
    page = read_page(vault, "Understanding KV Cache")
    assert page.properties["progress"] == "50"
    assert page.properties["status"] == "in-progress"

    # 7. Mark done
    result = runner.invoke(cli, ["done", "Understanding KV Cache"], env=e, catch_exceptions=False)
    assert result.exit_code == 0
    page = read_page(vault, "Understanding KV Cache")
    assert page.properties["status"] == "completed"

    # 8. Generate dashboard
    result = runner.invoke(cli, ["dashboard"], env=e, catch_exceptions=False)
    assert result.exit_code == 0
    dashboard = read_page(vault, "Learning Dashboard")
    assert dashboard is not None
    assert "ML/Infrastructure" in dashboard.body or "ML/Infrastructure" in str(dashboard.properties)

    # 9. Recompute
    result = runner.invoke(cli, ["recompute"], env=e, catch_exceptions=False)
    assert result.exit_code == 0
    gemma_page = read_page(vault, "Gemma 4 Technical Report")
    assert "priority" in gemma_page.properties
```

- [ ] **Step 2: Run integration test**

Run: `python -m pytest tests/test_integration.py -v`
Expected: PASS

- [ ] **Step 3: Run full test suite**

Run: `python -m pytest tests/ -v --tb=short`
Expected: All tests PASS

- [ ] **Step 4: Commit**

```bash
git add tests/test_integration.py
git commit -m "test: add end-to-end integration test for full CLI flow"
```

- [ ] **Step 5: Verify CLI works manually**

```bash
cd /Users/sakthi/conductor/workspaces/learning-progress-tracker/hat-yai
pip install -e .
mkdir -p inbox processed
lpt init
lpt add https://arxiv.org/abs/2504.00958 --domain "ML/Infrastructure" --topic "Inference Optimization" --tag llm
lpt status
```

Expected: `lpt init` creates vault with Learning Queue page. `lpt add` creates a job in inbox. `lpt status` shows 1 pending job.
