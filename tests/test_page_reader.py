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
