"""The two everyday flows end to end, through the CLI, on a copy of the real vault when available."""
import json
import shutil
from datetime import date
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from cli.items import load_items
from cli.main import cli

REAL_VAULT = Path(__file__).resolve().parent.parent / "vault"


@pytest.fixture
def project(tmp_path, monkeypatch):
    if (REAL_VAULT / "pages").exists():
        shutil.copytree(REAL_VAULT, tmp_path / "vault")
    else:
        (tmp_path / "vault" / "pages").mkdir(parents=True)
        (tmp_path / "vault" / "pages" / "Raft Paper.md").write_text("title:: Raft Paper\ntype:: paper\nstatus:: unread\n")
    (tmp_path / "config.yaml").write_text(yaml.dump({"vault_path": str(tmp_path / "vault")}))
    monkeypatch.setenv("LPT_CONFIG", str(tmp_path / "config.yaml"))
    return tmp_path


def run(*args, input=None):
    r = CliRunner().invoke(cli, list(args), input=input, catch_exceptions=False)
    assert r.exit_code == 0, r.output
    return r.output


def test_capture_then_evening_session(project, tmp_path):
    run("migrate")
    before = len(load_items(project / "vault"))
    assert all(i["state"] == "collected" for i in load_items(project / "vault"))

    # capture: a batch of links from WhatsApp
    run("add", "--note", "from WhatsApp", input="https://example.com/event-loops\nhttps://example.com/tcp\n")
    unsorted = [i for i in load_items(project / "vault") if i["area"] == "Unsorted"]
    assert len(unsorted) == 2 and len(load_items(project / "vault")) == before + 2

    # file one with Claude's result
    pending = [json.loads(l) for l in run("enrich").splitlines()]
    result = tmp_path / "r.json"
    result.write_text(json.dumps({"title": "Event Loops Explained", "medium": "article", "domain": "Systems",
                                  "topic": "Concurrency", "concepts": ["Concurrency Basics"], "summary": "How loops work."}))
    run("enrich", pending[0]["id"], "--from", str(result))

    # plan, pick up, work, finish
    run("prio", "Event Loops Explained", "now")
    run("plan", "Event Loops Explained")
    run("time", "Event Loops Explained", "1h")
    run("check", "Event Loops Explained", "Read others' implementations of the event loop")
    run("note", "Event Loops Explained", "Read half, epoll next")
    run("check", "Event Loops Explained", "--toggle", "1")
    run("done", "Event Loops Explained")

    it = next(i for i in load_items(project / "vault") if i["title"] == "Event Loops Explained")
    today = date.today().isoformat()
    assert (it["state"], it["done"], it["planned"], it["prio"]) == ("done", today, today[:7], "now")
    assert it["sessions"] == [{"d": today, "m": 60}] and it["checks"][0]["done"]
    assert it["notes"] == "Read half, epoll next"
    page = (project / "vault" / "pages" / "Event Loops Explained.md").read_text()
    assert "## Time\n- " + today + " · 1h" in page and "## Checklist\n- [x] Read others'" in page
