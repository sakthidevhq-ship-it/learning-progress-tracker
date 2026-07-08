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
