from datetime import date
from pathlib import Path

from thefuzz import fuzz

from cli.config import Config
from cli.page_reader import list_pages, update_property
from cli.priority import recompute_all


def find_page_by_title(vault_path: Path, query: str) -> str | None:
    pages = list_pages(vault_path)
    if not pages:
        return None
    for page in pages:
        if page.title.lower() == query.lower():
            return page.title
    best_score = 0
    best_title = None
    for page in pages:
        score = fuzz.partial_ratio(query.lower(), page.title.lower())
        if score > best_score:
            best_score = score
            best_title = page.title
    if best_score >= 70:
        return best_title
    return None


def update_progress(vault_path: Path, title: str, value: int, config: Config) -> None:
    update_property(vault_path, title, "progress", str(value))
    if value >= 100:
        update_property(vault_path, title, "status", "completed")
    elif value > 0:
        update_property(vault_path, title, "status", "in-progress")
    recompute_all(vault_path, config)


def mark_done(vault_path: Path, title: str, config: Config) -> None:
    update_progress(vault_path, title, 100, config)


def generate_dashboard(vault_path: Path, config: Config) -> Path:
    all_pages = list_pages(vault_path)
    resource_types = {"paper", "article", "tweet", "video", "docs"}

    resources = [p for p in all_pages if p.properties.get("type") in resource_types]
    stubs = [p for p in all_pages if p.properties.get("status") == "stub"]

    domain_stats: dict[str, dict] = {}
    topic_stats: dict[str, dict] = {}

    for page in resources:
        domain_raw = page.properties.get("domain", "")
        domain = domain_raw.strip()
        if domain:
            if domain not in domain_stats:
                domain_stats[domain] = {"items": 0, "done": 0, "in_progress": 0}
            domain_stats[domain]["items"] += 1
            if page.properties.get("status") == "completed":
                domain_stats[domain]["done"] += 1
            elif page.properties.get("status") == "in-progress":
                domain_stats[domain]["in_progress"] += 1

        topic_raw = page.properties.get("topic", "")
        topic = topic_raw.strip()
        if topic:
            key = (topic, domain)
            if key not in topic_stats:
                topic_stats[key] = {"items": 0, "done": 0}
            topic_stats[key]["items"] += 1
            if page.properties.get("status") == "completed":
                topic_stats[key]["done"] += 1

    lines = [
        f"title:: Learning Dashboard",
        "type:: dashboard",
        f"generated:: [[{date.today().isoformat()}]]",
        "",
        "## Domain Progress",
        "| Domain | Items | Done | In Progress | Progress |",
        "|--------|-------|------|-------------|----------|",
    ]
    for domain, stats in sorted(domain_stats.items()):
        pct = round(stats["done"] / stats["items"] * 100) if stats["items"] else 0
        lines.append(f"| {domain} | {stats['items']} | {stats['done']} | {stats['in_progress']} | {pct}% |")

    lines.extend(["", "## Topic Progress",
                   "| Topic | Domain | Items | Done | Progress |",
                   "|-------|--------|-------|------|----------|"])
    for (topic, domain), stats in sorted(topic_stats.items()):
        pct = round(stats["done"] / stats["items"] * 100) if stats["items"] else 0
        lines.append(f"| {topic} | {domain} | {stats['items']} | {stats['done']} | {pct}% |")

    if stubs:
        lines.extend(["", "## Knowledge Gaps (Stubs)"])
        for stub in stubs:
            ref = stub.properties.get("referenced-by", "")
            lines.append(f"- [[{stub.title}]] — needed by: {ref}")

    queue = sorted(resources,
                   key=lambda p: int(p.properties.get("priority", "0")),
                   reverse=True)
    queue = [p for p in queue if p.properties.get("status") != "completed"][:10]
    if queue:
        lines.extend(["", "## Queue (Top 10 by Priority)"])
        for i, page in enumerate(queue, 1):
            pri = page.properties.get("priority", "?")
            eng = page.properties.get("engagement", "?")
            comp = page.properties.get("complexity", "?")
            lines.append(f"{i}. [[{page.title}]] (priority: {pri}, {eng}, {comp})")

    content = "\n".join(lines) + "\n"
    pages_dir = vault_path / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    path = pages_dir / "Learning Dashboard.md"
    path.write_text(content)
    return path
