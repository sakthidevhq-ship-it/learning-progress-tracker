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
