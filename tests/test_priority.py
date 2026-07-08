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
