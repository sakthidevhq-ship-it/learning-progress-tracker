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


def _write_page(project, title, **props):
    from cli.config import title_to_filename
    defaults = {"type": "paper", "status": "unread", "progress": "0"}
    defaults.update(props)
    lines = [f"title:: {title}"]
    for k, v in defaults.items():
        lines.append(f"{k}:: {v}")
    vault = project / "vault"
    (vault / "pages" / title_to_filename(title)).write_text("\n".join(lines) + "\n")


def test_progress_command(project):
    _write_page(project, "Test Paper")
    result = run(project, ["progress", "Test Paper", "50"])
    assert result.exit_code == 0
    content = (project / "vault" / "pages" / "Test Paper.md").read_text()
    assert "progress:: 50" in content
    assert "status:: in-progress" in content


def test_progress_command_no_match(project):
    result = run(project, ["progress", "Nonexistent Page", "50"])
    assert result.exit_code != 0


def test_done_command(project):
    _write_page(project, "Test Paper", status="in-progress", progress="40")
    result = run(project, ["done", "Test Paper"])
    assert result.exit_code == 0
    content = (project / "vault" / "pages" / "Test Paper.md").read_text()
    assert "progress:: 100" in content
    assert "status:: completed" in content


def test_done_command_no_match(project):
    result = run(project, ["done", "Nonexistent Page"])
    assert result.exit_code != 0


def test_dashboard_command(project):
    _write_page(project, "Test Paper", domain="[[ML/Infrastructure]]")
    result = run(project, ["dashboard"])
    assert result.exit_code == 0
    dashboard_file = project / "vault" / "pages" / "Learning Dashboard.md"
    assert dashboard_file.exists()
    assert "Learning Dashboard" in dashboard_file.read_text()


def test_recompute_command(project):
    _write_page(project, "Test Paper", domain="[[ML/Infrastructure]]")
    result = run(project, ["recompute"])
    assert result.exit_code == 0
    content = (project / "vault" / "pages" / "Test Paper.md").read_text()
    assert "priority::" in content
