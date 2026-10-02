from datetime import date
from pathlib import Path

import pytest

from cli import items
from cli.items import Page, add_items, apply, find_item, load_items, migrate, parse_minutes, format_minutes

TODAY = date(2026, 10, 3)
REAL_VAULT = Path(__file__).resolve().parent.parent / "vault"


@pytest.fixture
def vault(tmp_path):
    pages = tmp_path / "vault" / "pages"
    pages.mkdir(parents=True)
    (pages / "Raft Paper.md").write_text(
        "title:: Raft Paper\n"
        "type:: paper\n"
        "domain:: [[Systems]]\n"
        "topic:: [[Distributed Consensus]]\n"
        "state:: collected\n"
        "concepts:: [[Raft Consensus]], [[Consistency Models]]\n"
        "source:: https://raft.github.io/raft.pdf\n"
        "ingested:: [[2026-07-09]]\n"
        "\n## Summary\nUnderstandable consensus.\n\n## Key Takeaways\n- Leaders\n\n## Notes\n"
    )
    (pages / "Raft Consensus.md").write_text("title:: Raft Consensus\ntype:: concept\nstatus:: stub\n")
    return tmp_path / "vault"


def item(vault, name="Raft Paper"):
    return vault / "pages" / f"{name}.md"


# ---------- durations ----------

@pytest.mark.parametrize("text,minutes", [
    ("30m", 30), ("1h", 60), ("1h30m", 90), ("1.5h", 90), ("2", 120), ("+30m", 30), ("-30m", -30), ("90m", 90),
])
def test_parse_minutes(text, minutes):
    assert parse_minutes(text) == minutes


@pytest.mark.parametrize("bad", ["", "abc", "1x", "h", "m"])
def test_parse_minutes_rejects_garbage(bad):
    with pytest.raises(ValueError):
        parse_minutes(bad)


def test_format_minutes():
    assert [format_minutes(m) for m in (30, 60, 90, 125)] == ["30m", "1h", "1h30m", "2h5m"]


# ---------- page round trip ----------

def test_page_round_trip_is_lossless(vault):
    p = item(vault)
    before = p.read_text()
    Page(p).save()
    assert p.read_text() == before


@pytest.mark.skipif(not (REAL_VAULT / "pages").exists(), reason="no real vault")
def test_real_vault_pages_round_trip(tmp_path):
    # Loading and saving must never rewrite a page you didn't touch
    changed = []
    for f in sorted((REAL_VAULT / "pages").glob("*.md")):
        copy = tmp_path / f.name
        copy.write_text(f.read_text())
        Page(copy).save()
        if copy.read_text().rstrip("\n") != f.read_text().rstrip("\n"):
            changed.append(f.name)
    assert changed == []


# ---------- states ----------

def test_pick_sets_date_and_this_months_plan(vault):
    it = apply(item(vault), "pick", TODAY)
    assert it["state"] == "picked"
    assert it["picked"] == "2026-10-03"
    assert it["planned"] == "2026-10"


def test_pick_keeps_an_earlier_plan_month(vault):
    apply(item(vault), "plan", TODAY, month="2026-09")
    assert apply(item(vault), "pick", TODAY)["planned"] == "2026-09"


def test_pick_pulls_a_later_plan_into_this_month(vault):
    apply(item(vault), "plan", TODAY, month="2026-11")
    assert apply(item(vault), "pick", TODAY)["planned"] == "2026-10"


def test_done_without_pick_fills_picked(vault):
    it = apply(item(vault), "done", TODAY)
    assert (it["state"], it["picked"], it["done"]) == ("done", "2026-10-03", "2026-10-03")


def test_drop_then_pick_clears_dropped(vault):
    apply(item(vault), "drop", TODAY)
    assert apply(item(vault), "pick", TODAY)["dropped"] == ""


def test_back_returns_to_not_started_but_stays_planned(vault):
    apply(item(vault), "pick", TODAY)
    it = apply(item(vault), "back", TODAY)
    assert (it["state"], it["picked"], it["planned"]) == ("collected", "", "2026-10")


def test_dates_are_written_as_journal_links(vault):
    apply(item(vault), "pick", TODAY)
    assert "picked:: [[2026-10-03]]" in item(vault).read_text()


# ---------- time ----------

def test_time_adds_to_todays_line(vault):
    apply(item(vault), "time", TODAY, minutes=30)
    it = apply(item(vault), "time", TODAY, minutes=30)
    assert it["sessions"] == [{"d": "2026-10-03", "m": 60}]
    assert "- 2026-10-03 · 1h" in item(vault).read_text()


def test_time_on_collected_item_picks_it_up(vault):
    it = apply(item(vault), "time", TODAY, minutes=30)
    assert it["state"] == "picked"


def test_time_can_be_taken_back_to_zero(vault):
    apply(item(vault), "time", TODAY, minutes=30)
    it = apply(item(vault), "time", TODAY, minutes=-30)
    assert it["sessions"] == []
    assert "## Time" not in item(vault).read_text()


def test_time_on_another_day_keeps_lines_sorted(vault):
    apply(item(vault), "time", TODAY, minutes=60)
    it = apply(item(vault), "time", TODAY, minutes=90, day=date(2026, 10, 1))
    assert [s["d"] for s in it["sessions"]] == ["2026-10-01", "2026-10-03"]


# ---------- checklist & notes ----------

def test_checklist_add_toggle_remove(vault):
    apply(item(vault), "check_add", TODAY, text="Read §5")
    apply(item(vault), "check_add", TODAY, text="Implement log replication")
    apply(item(vault), "check_toggle", TODAY, index=0)
    text = item(vault).read_text()
    assert "- [x] Read §5" in text and "- [ ] Implement log replication" in text
    it = apply(item(vault), "check_remove", TODAY, index=0)
    assert it["checks"] == [{"t": "Implement log replication", "done": False}]


def test_checklist_bad_index(vault):
    with pytest.raises(ValueError):
        apply(item(vault), "check_toggle", TODAY, index=3)


def test_notes_replace_and_keep_other_sections(vault):
    it = apply(item(vault), "notes", TODAY, text="Read half of §5.\nStopped at 5.4.1")
    assert it["notes"] == "Read half of §5.\nStopped at 5.4.1"
    assert it["summary"] == "Understandable consensus."
    assert "## Key Takeaways\n- Leaders" in item(vault).read_text()


def test_notes_cannot_inject_a_section(vault):
    apply(item(vault), "notes", TODAY, text="## Time\n- 2026-10-03 · 9h")
    it = items.to_json(Page(item(vault)))
    assert it["sessions"] == []


def test_priority_and_plan(vault):
    assert apply(item(vault), "prio", TODAY, prio="soon")["prio"] == "soon"
    assert apply(item(vault), "prio", TODAY, prio="none")["prio"] == ""
    assert apply(item(vault), "plan", TODAY, month="2026-11")["planned"] == "2026-11"
    with pytest.raises(ValueError):
        apply(item(vault), "plan", TODAY, month="November")
    with pytest.raises(ValueError):
        apply(item(vault), "prio", TODAY, prio="urgent")


def test_apply_rejects_non_items(vault):
    with pytest.raises(ValueError):
        apply(vault / "pages" / "Raft Consensus.md", "pick", TODAY)


# ---------- finding & loading ----------

def test_find_item_by_id_title_and_fuzzy(vault):
    assert find_item(vault, "Raft Paper") == item(vault)
    assert find_item(vault, "raft paper") == item(vault)
    assert find_item(vault, "raft") == item(vault)
    assert find_item(vault, "zzz quantum") is None


def test_find_item_ignores_concept_pages(vault):
    assert find_item(vault, "Raft Consensus") is None  # the concept page exists but isn't an item


def test_load_items_json(vault):
    [it] = load_items(vault)
    assert it["id"] == "Raft Paper"
    assert (it["area"], it["topic"]) == ("Systems", "Distributed Consensus")
    assert it["concepts"] == ["Raft Consensus", "Consistency Models"]
    assert it["source"] == "https://raft.github.io/raft.pdf"


# ---------- capture ----------

def test_add_items_one_per_line_into_unsorted(vault):
    added, skipped = add_items(vault, ["https://jvns.ca/blog/tcp/", "", "Build a toy Raft in Rust"],
                               TODAY, note="from WhatsApp", type_="article", prio="soon")
    assert skipped == []
    assert [a["area"] for a in added] == ["Unsorted", "Unsorted"]
    assert added[0]["source"] == "https://jvns.ca/blog/tcp/"
    assert added[0]["enrich"] and added[0]["prio"] == "soon" and added[0]["note"] == "from WhatsApp"
    assert added[1]["title"] == "Build a toy Raft in Rust"
    assert (vault / "pages" / "jvns.ca blog tcp.md").exists()


def test_add_items_skips_duplicates(vault):
    added, skipped = add_items(vault, ["https://raft.github.io/raft.pdf", "Raft Paper", "New thing", "New thing"], TODAY)
    assert [a["title"] for a in added] == ["New thing"]
    assert len(skipped) == 3


def test_add_items_strips_list_bullets(vault):
    added, _ = add_items(vault, ["- https://a.example/x", "• Another idea"], TODAY)
    assert [a["title"] for a in added] == ["https://a.example/x", "Another idea"]


def test_add_project(vault):
    [a], _ = add_items(vault, ["Write an HTTP/2 frame parser"], TODAY, type_="project")
    assert a["type"] == "project"
    assert (vault / "pages" / "Write an HTTP___2 frame parser.md").exists()


def test_apply_enrichment_files_and_renames(vault):
    [a], _ = add_items(vault, ["https://example.com/post"], TODAY)
    it = items.apply_enrichment(vault, a["id"], {
        "title": "Event Loops Explained", "medium": "article", "domain": "Systems", "topic": "Concurrency",
        "concepts": ["Concurrency Basics"], "summary": "How event loops work.", "key_takeaways": ["epoll"],
    })
    assert (it["title"], it["area"], it["topic"], it["enrich"]) == ("Event Loops Explained", "Systems", "Concurrency", False)
    assert it["id"] == "Event Loops Explained"
    assert (vault / "pages" / "Event Loops Explained.md").exists()
    assert (vault / "pages" / "Concurrency Basics.md").exists()  # concept stub


# ---------- migration ----------

def test_migrate_resets_everything_to_not_started(vault):
    old = vault / "pages" / "Old Book.md"
    old.write_text(
        "title:: Old Book\ntype:: docs\nstatus:: completed\nprogress:: 100\npriority:: 37\n"
        "started:: [[2026-07-01]]\ncompleted:: [[2026-07-09]]\ningested:: [[2026-07-01]]\n"
        "\n## Summary\nA book.\n\n## My Notes\nchapter 3 was good\n"
    )
    stub = vault / "pages" / "Some Concept.md"
    stub.write_text("title:: Some Concept\ntype:: concept\nstatus:: stub\npriority:: 22\n")
    stats = migrate(vault)
    assert stats == {"items": 1, "other_pages": 1}
    text = old.read_text()
    assert "state:: collected" in text
    for gone in ("status::", "progress::", "priority::", "started::", "completed::"):
        assert gone not in text
    assert "## Notes\nchapter 3 was good" in text
    assert stub.read_text() == "title:: Some Concept\ntype:: concept\nstatus:: stub\n"


def test_migrate_twice_changes_nothing(vault):
    (vault / "pages" / "Old.md").write_text("title:: Old\ntype:: paper\nstatus:: in-progress\nprogress:: 30\n")
    migrate(vault)
    apply(vault / "pages" / "Old.md", "pick", TODAY)
    before = (vault / "pages" / "Old.md").read_text()
    assert migrate(vault) == {"items": 0, "other_pages": 0}
    assert (vault / "pages" / "Old.md").read_text() == before
