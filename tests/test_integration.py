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
