from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class Config:
    vault_path: Path
    domain_weights: dict[str, float] = field(default_factory=dict)
    topic_weights: dict[str, float] = field(default_factory=dict)
    default_weight: float = 0.5
    on_duplicate: str = "skip"


def load_config(path: str | None = None) -> Config:
    if path is None:
        path = "config.yaml"
    with open(path) as f:
        raw = yaml.safe_load(f) or {}

    if "vault_path" not in raw:
        raise ValueError("config.yaml must specify vault_path")

    return Config(
        vault_path=Path(raw["vault_path"]).expanduser(),
        domain_weights=raw.get("domain_weights", {}),
        topic_weights=raw.get("topic_weights", {}),
        default_weight=raw.get("default_weight", 0.5),
        on_duplicate=raw.get("on_duplicate", "skip"),
    )


def title_to_filename(title: str) -> str:
    return title.replace("/", "___") + ".md"


def filename_to_title(filename: str) -> str:
    if filename.endswith(".md"):
        filename = filename[:-3]
    return filename.replace("___", "/")
