from datetime import date
from pathlib import Path

from cli.config import title_to_filename
from cli.page_reader import read_page, update_property


def _format_link_list(items: list[str]) -> str:
    return ", ".join(f"[[{item}]]" for item in items)


def write_resource_page(vault_path: Path, metadata: dict, job: dict) -> Path:
    title = metadata["title"]
    domain = job.get("domain") or metadata.get("domain")
    topic = job.get("topic") or metadata.get("topic")
    engagement = job.get("engagement") or metadata.get("engagement_suggestion") or ""
    tags = job.get("tags", [])

    props = [
        f"title:: {title}",
        f"type:: {metadata.get('medium', 'article')}",
    ]
    if domain:
        props.append(f"domain:: [[{domain}]]")
    if topic:
        props.append(f"topic:: [[{topic}]]")
    if engagement:
        props.append(f"engagement:: {engagement}")
    props.append("status:: unread")
    props.append("progress:: 0")
    if metadata.get("complexity"):
        props.append(f"complexity:: {metadata['complexity']}")
    if metadata.get("size"):
        props.append(f"size:: {metadata['size']}")
    if metadata.get("medium"):
        props.append(f"medium:: {metadata['medium']}")
    prerequisites = metadata.get("prerequisites", [])
    if prerequisites:
        props.append(f"prerequisites:: {_format_link_list(prerequisites)}")
    concepts = metadata.get("concepts", [])
    if concepts:
        props.append(f"concepts:: {_format_link_list(concepts)}")
    if tags:
        props.append(f"tags:: {', '.join(tags)}")
    if job.get("source"):
        props.append(f"source:: {job['source']}")
    props.append(f"ingested:: [[{date.today().isoformat()}]]")

    body_parts = []
    if metadata.get("summary"):
        body_parts.append(f"## Summary\n{metadata['summary']}")
    takeaways = metadata.get("key_takeaways", [])
    if takeaways:
        items = "\n".join(f"- {t}" for t in takeaways)
        body_parts.append(f"## Key Takeaways\n{items}")
    if prerequisites:
        items = "\n".join(f"- [[{p}]]" for p in prerequisites)
        body_parts.append(f"## Prerequisites\n{items}")
    body_parts.append("## My Notes\n")

    content = "\n".join(props) + "\n\n" + "\n\n".join(body_parts)

    pages_dir = vault_path / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    file_path = pages_dir / title_to_filename(title)
    file_path.write_text(content)
    return file_path


def write_concept_stub(
    vault_path: Path,
    concept: str,
    domain: str | None,
    topic: str | None,
    referenced_by: str,
) -> Path:
    existing = read_page(vault_path, concept)
    if existing is not None:
        ref_prop = existing.properties.get("referenced-by", "")
        link = f"[[{referenced_by}]]"
        existing_links = [s.strip() for s in ref_prop.split(",") if s.strip()]
        if link not in existing_links:
            existing_links.append(link)
            update_property(vault_path, concept, "referenced-by", ", ".join(existing_links))
        return existing.file_path

    props = [
        f"title:: {concept}",
        "type:: concept",
        "status:: stub",
    ]
    if domain:
        props.append(f"domain:: [[{domain}]]")
    if topic:
        props.append(f"topic:: [[{topic}]]")
    props.append(f"referenced-by:: [[{referenced_by}]]")

    content = (
        "\n".join(props)
        + "\n\n## About\nAuto-generated stub. This concept is a prerequisite for items in your learning queue.\n"
    )

    pages_dir = vault_path / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    file_path = pages_dir / title_to_filename(concept)
    file_path.write_text(content)
    return file_path


def write_domain_page(vault_path: Path, domain: str, topics: list[str]) -> Path:
    existing = read_page(vault_path, domain)
    if existing is not None:
        content = existing.file_path.read_text()
        for topic in topics:
            link = f"[[{topic}]]"
            if link not in content:
                content = content.rstrip("\n") + f"\n- {link}\n"
        existing.file_path.write_text(content)
        return existing.file_path

    props = [f"title:: {domain}", "type:: domain"]
    topic_list = "\n".join(f"- [[{t}]]" for t in topics)
    content = "\n".join(props) + f"\n\n## Topics\n{topic_list}\n"

    pages_dir = vault_path / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    file_path = pages_dir / title_to_filename(domain)
    file_path.write_text(content)
    return file_path


def write_topic_page(vault_path: Path, topic: str, domain: str) -> Path:
    existing = read_page(vault_path, topic)
    if existing is not None:
        return existing.file_path

    props = [f"title:: {topic}", "type:: topic", f"domain:: [[{domain}]]"]
    content = "\n".join(props) + "\n"

    pages_dir = vault_path / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    file_path = pages_dir / title_to_filename(topic)
    file_path.write_text(content)
    return file_path


def ensure_linked_pages(vault_path: Path, metadata: dict, title: str) -> None:
    domain = metadata.get("domain")
    topic = metadata.get("topic")

    all_concepts = list(set(metadata.get("concepts", []) + metadata.get("prerequisites", [])))
    for concept in all_concepts:
        existing = read_page(vault_path, concept)
        if existing is None or existing.properties.get("type") == "concept":
            write_concept_stub(vault_path, concept, domain, topic, title)

    if domain:
        topics_list = [topic] if topic else []
        write_domain_page(vault_path, domain, topics_list)

    if topic and domain:
        write_topic_page(vault_path, topic, domain)
