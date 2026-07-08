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
