from datetime import date, timedelta

import pytest
import yaml
from click.testing import CliRunner

from cli.items import load_items
from cli.main import cli

TODAY = date.today().isoformat()


@pytest.fixture
def project(tmp_path, monkeypatch):
    pages = tmp_path / "vault" / "pages"
    pages.mkdir(parents=True)
    (pages / "Raft Paper.md").write_text(
        "title:: Raft Paper\ntype:: paper\ndomain:: [[Systems]]\ntopic:: [[Distributed Consensus]]\n"
        "state:: collected\ningested:: [[2026-07-09]]\n"
    )
    (pages / "Attention Is All You Need.md").write_text(
        "title:: Attention Is All You Need\ntype:: paper\ndomain:: [[ML/Foundations]]\nstate:: collected\n"
    )
    config = tmp_path / "config.yaml"
    config.write_text(yaml.dump({"vault_path": str(tmp_path / "vault")}))
    monkeypatch.setenv("LPT_CONFIG", str(config))
    return tmp_path


def run(*args, input=None):
    result = CliRunner().invoke(cli, list(args), input=input, catch_exceptions=False)
    return result


def items_by_title(project):
    return {i["title"]: i for i in load_items(project / "vault")}


def test_add_entries_and_stdin(project):
    r = run("add", "https://example.com/a", "Build a toy Raft", "--note", "from WhatsApp", "--prio", "soon")
    assert r.exit_code == 0 and "Added 2 to Unsorted" in r.output
    r = run("add", input="https://example.com/b\n\nhttps://example.com/a\n")
    assert "Added 1 to Unsorted, skipped 1" in r.output
    got = items_by_title(project)
    assert got["Build a toy Raft"]["note"] == "from WhatsApp"
    assert got["https://example.com/b"]["area"] == "Unsorted"


def test_add_project_type(project):
    run("add", "Write an HTTP/2 parser", "--type", "project")
    assert items_by_title(project)["Write an HTTP/2 parser"]["type"] == "project"


def test_pick_done_drop_back(project):
    assert "Picked up 'Raft Paper'" in run("pick", "raft").output
    assert items_by_title(project)["Raft Paper"]["planned"] == TODAY[:7]
    run("back", "raft")
    assert items_by_title(project)["Raft Paper"]["state"] == "collected"
    run("done", "raft")
    assert items_by_title(project)["Raft Paper"]["state"] == "done"
    run("drop", "attention")
    assert items_by_title(project)["Attention Is All You Need"]["state"] == "dropped"


def test_unknown_item_errors(project):
    r = CliRunner().invoke(cli, ["pick", "zzz quantum basket"])
    assert r.exit_code != 0 and "No item matching" in r.output


def test_time_default_custom_negative_and_date(project):
    run("time", "raft")
    r = run("time", "raft", "1h")
    assert "1h30m on" in r.output
    run("time", "raft", "-30m")
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    run("time", "raft", "45m", "--date", "yesterday")
    s = {x["d"]: x["m"] for x in items_by_title(project)["Raft Paper"]["sessions"]}
    assert s == {TODAY: 60, yesterday: 45}
    assert items_by_title(project)["Raft Paper"]["state"] == "picked"


def test_time_rejects_bad_amount(project):
    r = CliRunner().invoke(cli, ["time", "raft", "lots"])
    assert r.exit_code != 0


def test_check_add_toggle_remove_and_list(project):
    run("check", "raft", "Read §5")
    run("check", "raft", "Implement it")
    r = run("check", "raft", "--toggle", "1")
    assert "1. [x] Read §5" in r.output and "2. [ ] Implement it" in r.output
    r = run("check", "raft", "--remove", "1")
    assert "Read §5" not in r.output
    assert "1. [ ] Implement it" in run("check", "raft").output


def test_note_appends(project):
    run("note", "raft", "Read half of §5")
    run("note", "raft", "Stopped at 5.4.1")
    assert items_by_title(project)["Raft Paper"]["notes"] == "Read half of §5\nStopped at 5.4.1"


def test_prio_and_plan(project):
    run("prio", "raft", "now")
    run("plan", "raft", "next")
    it = items_by_title(project)["Raft Paper"]
    assert it["prio"] == "now"
    assert it["planned"] > TODAY[:7]
    run("plan", "raft", "none")
    assert items_by_title(project)["Raft Paper"]["planned"] == ""


def test_show_ls_status(project):
    run("pick", "raft")
    run("time", "raft", "1h")
    run("check", "raft", "Read §5")
    out = run("show", "raft").output
    assert "Systems / Distributed Consensus" in out and "time: 1h" in out and "[ ] Read §5" in out
    assert "picked" in run("ls").output
    assert "Attention" in run("ls", "--state", "collected").output
    out = run("status").output
    assert "picked     1" in out and "collected  1" in out


def test_enrich_lists_and_files(project, tmp_path):
    run("add", "https://example.com/event-loops")
    out = run("enrich").output
    assert "example.com/event-loops" in out
    import json
    item_id = json.loads(out.splitlines()[0])["id"]
    result = tmp_path / "r.json"
    result.write_text(json.dumps({"title": "Event Loops", "medium": "article", "domain": "Systems",
                                  "topic": "Concurrency", "concepts": ["Concurrency Basics"], "summary": "Loops."}))
    r = run("enrich", item_id, "--from", str(result))
    assert "Filed 'Event Loops' under Systems / Concurrency" in r.output
    assert "Nothing waiting" in run("enrich").output


def test_migrate_command(project):
    (project / "vault" / "pages" / "Old.md").write_text("title:: Old\ntype:: docs\nstatus:: completed\nprogress:: 100\n")
    assert "Migrated 1 items" in run("migrate").output
    assert items_by_title(project)["Old"]["state"] == "collected"


def test_graph_builds_site(project, monkeypatch):
    from cli import main
    monkeypatch.setattr(main, "PROJECT_ROOT", project)
    (project / "ui").mkdir()
    import shutil
    from pathlib import Path
    shutil.copy(Path(__file__).resolve().parent.parent / "ui" / "workbench.html", project / "ui" / "workbench.html")
    monkeypatch.setattr("cli.build_graph.TEMPLATE", project / "ui" / "workbench.html")
    r = run("graph", "--no-open")
    assert r.exit_code == 0
    html = (project / "site" / "index.html").read_text()
    assert "Raft Paper" in html and "VAULT_PLACEHOLDER" not in html
