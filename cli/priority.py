import re
from datetime import date
from pathlib import Path

from cli.config import Config
from cli.page_reader import PageData, list_pages, update_property


_LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def _parse_links(value: str) -> list[str]:
    return _LINK_RE.findall(value)


def _strip_link(value: str) -> str:
    m = _LINK_RE.match(value.strip())
    return m.group(1) if m else value.strip()


def compute_priority(page: PageData, all_pages: list[PageData], config: Config) -> int:
    my_concepts = set(_parse_links(page.properties.get("concepts", "")))
    my_prereqs = set(_parse_links(page.properties.get("prerequisites", "")))
    my_all = my_concepts | my_prereqs
    title = page.title

    overlap_count = 0
    prereq_demand = 0
    for other in all_pages:
        if other.title == title:
            continue
        other_concepts = set(_parse_links(other.properties.get("concepts", "")))
        other_prereqs = set(_parse_links(other.properties.get("prerequisites", "")))
        overlap_count += len(my_all & (other_concepts | other_prereqs))
        if title in other_prereqs or my_concepts & other_prereqs:
            prereq_demand += 1

    max_others = max(len(all_pages) - 1, 1)
    overlap_score = min(overlap_count / (max_others * 2), 1.0) * 25
    prereq_score = min(prereq_demand / max_others, 1.0) * 25

    domain_raw = _strip_link(page.properties.get("domain", ""))
    domain_w = config.domain_weights.get(domain_raw, config.default_weight)
    domain_score = domain_w * 20

    topic_raw = _strip_link(page.properties.get("topic", ""))
    topic_w = config.topic_weights.get(topic_raw, config.default_weight)
    topic_score = topic_w * 15

    ingested_raw = page.properties.get("ingested", "")
    recency_score = 0.0
    ingested_date_str = _LINK_RE.search(ingested_raw)
    if ingested_date_str:
        try:
            ing_date = date.fromisoformat(ingested_date_str.group(1))
            days_old = (date.today() - ing_date).days
            recency_score = max(0, 1.0 - days_old / 90) * 5
        except ValueError:
            pass

    complexity = page.properties.get("complexity", "intermediate")
    complexity_map = {"beginner": 5, "intermediate": 2.5, "advanced": 0}
    inverse_complexity_score = complexity_map.get(complexity, 2.5)

    engagement = page.properties.get("engagement", "")
    engagement_map = {"background": 5, "read": 2.5, "implement": 2.5}
    engagement_score = engagement_map.get(engagement, 2.5)

    total = (
        overlap_score
        + prereq_score
        + domain_score
        + topic_score
        + recency_score
        + inverse_complexity_score
        + engagement_score
    )
    return min(round(total), 100)


def recompute_all(vault_path: Path, config: Config) -> int:
    resource_types = {"paper", "article", "tweet", "video", "docs", "concept"}
    all_pages = [
        p for p in list_pages(vault_path)
        if p.properties.get("type") in resource_types
    ]
    for page in all_pages:
        score = compute_priority(page, all_pages, config)
        update_property(vault_path, page.title, "priority", str(score))
    return len(all_pages)
