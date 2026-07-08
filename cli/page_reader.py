import re
from dataclasses import dataclass, field
from pathlib import Path

from cli.config import title_to_filename


@dataclass
class PageData:
    title: str = ""
    properties: dict[str, str] = field(default_factory=dict)
    body: str = ""
    file_path: Path | None = None


_PROP_RE = re.compile(r"^([a-zA-Z_-]+)::\s*(.*)$")


def parse_page(content: str) -> PageData:
    lines = content.split("\n")
    properties: dict[str, str] = {}
    body_start = 0

    for i, line in enumerate(lines):
        m = _PROP_RE.match(line)
        if m:
            properties[m.group(1)] = m.group(2).strip()
            body_start = i + 1
        elif line.strip() == "":
            body_start = i + 1
        else:
            break

    body = "\n".join(lines[body_start:])
    return PageData(
        title=properties.get("title", ""),
        properties=properties,
        body=body,
    )


def read_page(vault_path: Path, title: str) -> PageData | None:
    filename = title_to_filename(title)
    file_path = vault_path / "pages" / filename
    if not file_path.exists():
        return None
    page = parse_page(file_path.read_text())
    page.file_path = file_path
    return page


def list_pages(vault_path: Path, type_filter: str | None = None) -> list[PageData]:
    pages_dir = vault_path / "pages"
    if not pages_dir.exists():
        return []
    result = []
    for f in sorted(pages_dir.glob("*.md")):
        page = parse_page(f.read_text())
        page.file_path = f
        if type_filter is None or page.properties.get("type") == type_filter:
            result.append(page)
    return result


def update_property(vault_path: Path, title: str, key: str, value: str) -> None:
    filename = title_to_filename(title)
    file_path = vault_path / "pages" / filename
    content = file_path.read_text()
    lines = content.split("\n")

    found = False
    prop_end = 0
    for i, line in enumerate(lines):
        m = _PROP_RE.match(line)
        if m:
            prop_end = i + 1
            if m.group(1) == key:
                lines[i] = f"{key}:: {value}"
                found = True
                break
        elif line.strip() == "":
            continue
        else:
            break

    if not found:
        lines.insert(prop_end, f"{key}:: {value}")

    file_path.write_text("\n".join(lines))
