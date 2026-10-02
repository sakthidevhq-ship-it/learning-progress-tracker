"""Items: everything in the library you might work on, and what you've done with it.

All state lives on the item's own page so the vault stays plain, hand-editable markdown:

    state:: collected | picked | done | dropped
    picked:: [[2026-10-03]]     done:: [[...]]     dropped:: [[...]]
    planned:: 2026-10           my-priority:: now | soon | someday
    note:: why I saved it       enrich:: pending (captured, not filed yet)

    ## Notes        free text
    ## Checklist    - [ ] / - [x] lines
    ## Time         - 2026-10-03 · 1h30m   (one line per day)

Imported by the CI site build, which only has PyYAML, so keep third-party imports lazy.
"""

import re
from datetime import date
from pathlib import Path

from cli.config import title_to_filename

ITEM_TYPES = {"paper", "article", "video", "docs", "tweet", "project", "practice"}
STATES = ("collected", "picked", "done", "dropped")
PRIORITIES = ("now", "soon", "someday")

_PROP_RE = re.compile(r"^([a-zA-Z_-]+)::\s*(.*)$")
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
_LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
_MONTH_RE = re.compile(r"^\d{4}-\d{2}$")
_CHECK_RE = re.compile(r"^- \[([ xX])\] (.*)$")
_TIME_RE = re.compile(r"^- (\d{4}-\d{2}-\d{2})\s*[·|:-]\s*(\S+)")
_DURATION_RE = re.compile(r"^(?:(\d+(?:\.\d+)?)h)?(?:(\d+)m)?$")
_URL_RE = re.compile(r"^https?://", re.I)


# ---------- durations ----------

def parse_minutes(text: str) -> int:
    """'1h30m' -> 90, '45m' -> 45, '1.5h' -> 90, '2' -> 120 (bare numbers are hours)."""
    t = text.strip().lower().replace(" ", "")
    sign = -1 if t.startswith("-") else 1
    t = t.lstrip("+-")
    if re.fullmatch(r"\d+(\.\d+)?", t):
        return sign * round(float(t) * 60)
    m = _DURATION_RE.match(t)
    if not t or not m or not (m.group(1) or m.group(2)):
        raise ValueError(f"Can't read duration '{text}' (try 30m, 1h, 1h30m)")
    return sign * (round(float(m.group(1) or 0) * 60) + int(m.group(2) or 0))


def format_minutes(minutes: int) -> str:
    h, m = divmod(int(minutes), 60)
    return f"{h}h{m}m" if h and m else f"{h}h" if h else f"{m}m"


# ---------- page file ----------

class Page:
    """A vault page split into its property block and `## ` sections, written back losslessly."""

    def __init__(self, path: Path):
        self.path = Path(path)
        lines = self.path.read_text().split("\n")
        i, self.props = 0, []
        while i < len(lines):
            m = _PROP_RE.match(lines[i])
            if m:
                self.props.append([m.group(1), m.group(2).strip()])
            elif lines[i].strip():
                break
            i += 1
        self.preamble, self.sections = [], []
        for line in lines[i:]:
            if line.startswith("## "):
                self.sections.append([line[3:].strip(), []])
            elif self.sections:
                self.sections[-1][1].append(line)
            else:
                self.preamble.append(line)

    # properties
    def get(self, key, default=""):
        return next((v for k, v in self.props if k == key), default)

    def set(self, key, value):
        for p in self.props:
            if p[0] == key:
                p[1] = value
                return
        self.props.append([key, value])

    def remove(self, *keys):
        self.props = [p for p in self.props if p[0] not in keys]

    # sections
    def section(self, name):
        for n, body in self.sections:
            if n == name:
                return _trim(body)
        return None

    def set_section(self, name, lines):
        body = _trim(lines) + [""]
        for s in self.sections:
            if s[0] == name:
                s[1] = body
                return
        self.sections.append([name, body])

    def rename_section(self, old, new):
        for s in self.sections:
            if s[0] == old:
                s[0] = new

    def save(self):
        out = [f"{k}:: {v}" for k, v in self.props]
        rest = list(self.preamble)
        for name, body in self.sections:
            if rest and rest[-1].strip():
                rest.append("")
            rest.append(f"## {name}")
            rest.extend(body)
        rest = _trim(rest)
        text = "\n\n".join(part for part in ("\n".join(out), "\n".join(rest)) if part) + "\n"
        self.path.write_text(text)


def _trim(lines):
    lines = list(lines)
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def _link_date(d: date | str) -> str:
    return f"[[{d if isinstance(d, str) else d.isoformat()}]]"


def _plain_date(value: str) -> str:
    m = _DATE_RE.search(value or "")
    return m.group(0) if m else ""


def _month(d: date) -> str:
    return d.isoformat()[:7]


# ---------- finding items ----------

def is_item(page: Page) -> bool:
    return page.get("type") in ITEM_TYPES


def item_paths(vault: Path) -> dict[str, Path]:
    """{id: path} for every item. The id is the file name without .md, stable until the file is renamed."""
    pages = Path(vault) / "pages"
    out = {}
    for f in sorted(pages.glob("*.md")) if pages.exists() else []:
        props = {}
        for line in f.read_text().split("\n"):
            m = _PROP_RE.match(line)
            if m:
                props[m.group(1)] = m.group(2).strip()
            elif line.strip():
                break
        if props.get("type") in ITEM_TYPES:
            out[f.stem] = f
    return out


def find_item(vault: Path, query: str) -> Path | None:
    """By id, exact title, then fuzzy title (the CLI's 'lpt done "raft paper"')."""
    paths = item_paths(vault)
    if query in paths:
        return paths[query]
    titles = {p: Page(p).get("title", p.stem) for p in paths.values()}
    q = query.strip().lower()
    for p, t in titles.items():
        if t.lower() == q:
            return p
    from thefuzz import fuzz
    best, best_score = None, 0
    for p, t in titles.items():
        score = fuzz.partial_ratio(q, t.lower())
        if score > best_score:
            best, best_score = p, score
    return best if best_score >= 70 else None


# ---------- reading ----------

def checklist(page: Page) -> list[dict]:
    out = []
    for line in page.section("Checklist") or []:
        m = _CHECK_RE.match(line.strip())
        if m:
            out.append({"t": m.group(2).strip(), "done": m.group(1) != " "})
    return out


def sessions(page: Page) -> list[dict]:
    out = []
    for line in page.section("Time") or []:
        m = _TIME_RE.match(line.strip())
        if m:
            try:
                out.append({"d": m.group(1), "m": parse_minutes(m.group(2))})
            except ValueError:
                continue
    return sorted(out, key=lambda s: s["d"])


def notes(page: Page) -> str:
    return "\n".join(page.section("Notes") or [])


def to_json(page: Page) -> dict:
    """What the UI needs for one item."""
    domain = (_LINK_RE.findall(page.get("domain")) or [page.get("domain")])[0].strip()
    topic = (_LINK_RE.findall(page.get("topic")) or [page.get("topic")])[0].strip()
    summary = " ".join(l.strip() for l in (page.section("Summary") or []) if l.strip())
    source = page.get("source")
    planned = page.get("planned")
    prio = page.get("my-priority")
    return {
        "id": page.path.stem,
        "title": page.get("title", page.path.stem),
        "type": page.get("type"),
        "area": domain or "Unsorted",
        "topic": topic,
        "state": page.get("state") if page.get("state") in STATES else "collected",
        "ingested": _plain_date(page.get("ingested")),
        "picked": _plain_date(page.get("picked")),
        "done": _plain_date(page.get("done")),
        "dropped": _plain_date(page.get("dropped")),
        "planned": planned if _MONTH_RE.match(planned or "") else "",
        "prio": prio if prio in PRIORITIES else "",
        "note": page.get("note"),
        "enrich": page.get("enrich") == "pending",
        "source": "" if source in ("", "unknown") else source,
        "summary": summary,
        "concepts": _LINK_RE.findall(page.get("concepts")),
        "sessions": sessions(page),
        "checks": checklist(page),
        "notes": notes(page),
    }


def load_items(vault: Path) -> list[dict]:
    return [to_json(Page(p)) for p in item_paths(vault).values()]


# ---------- changing ----------

def _plan_into(page: Page, today: date):
    """Working on something puts it in this month's plan (carry-over keeps earlier months)."""
    planned = page.get("planned")
    if not _MONTH_RE.match(planned or "") or planned > _month(today):
        page.set("planned", _month(today))


def pick(page: Page, today: date):
    page.set("state", "picked")
    page.set("picked", _link_date(today))
    page.remove("done", "dropped")
    _plan_into(page, today)


def finish(page: Page, today: date):
    page.set("state", "done")
    page.set("done", _link_date(today))
    if not page.get("picked"):
        page.set("picked", _link_date(today))
    page.remove("dropped")
    _plan_into(page, today)


def drop(page: Page, today: date):
    page.set("state", "dropped")
    page.set("dropped", _link_date(today))


def put_back(page: Page, today: date | None = None):
    """Back to not started. Stays in the plan, so it carries over like anything unfinished."""
    page.set("state", "collected")
    page.remove("picked", "done", "dropped")


def add_time(page: Page, minutes: int, day: date):
    """Add (or with a negative value, take back) time on a day. One line per day."""
    d = day.isoformat()
    entries = {s["d"]: s["m"] for s in sessions(page)}
    entries[d] = max(0, entries.get(d, 0) + minutes)
    if not entries[d]:
        del entries[d]
    page.set_section("Time", [f"- {k} · {format_minutes(v)}" for k, v in sorted(entries.items())])
    if not entries:
        page.sections = [s for s in page.sections if s[0] != "Time"]
    if minutes > 0 and page.get("state", "collected") == "collected":
        pick(page, day)


def _write_checks(page: Page, checks):
    page.set_section("Checklist", [f"- [{'x' if c['done'] else ' '}] {c['t']}" for c in checks])
    if not checks:
        page.sections = [s for s in page.sections if s[0] != "Checklist"]


def check_add(page: Page, text: str):
    text = " ".join(text.split())
    if not text:
        raise ValueError("Checklist item can't be empty")
    _write_checks(page, checklist(page) + [{"t": text, "done": False}])


def _check_index(page, index):
    checks = checklist(page)
    if not 0 <= index < len(checks):
        raise ValueError(f"No checklist item {index + 1} (there are {len(checks)})")
    return checks


def check_toggle(page: Page, index: int):
    checks = _check_index(page, index)
    checks[index]["done"] = not checks[index]["done"]
    _write_checks(page, checks)


def check_remove(page: Page, index: int):
    checks = _check_index(page, index)
    del checks[index]
    _write_checks(page, checks)


def set_notes(page: Page, text: str):
    lines = text.replace("\r\n", "\n").split("\n")
    # a line starting with '## ' would become a new section on the next read
    lines = [("\\" + l) if l.startswith("## ") else l for l in lines]
    if any(l.strip() for l in lines):
        page.set_section("Notes", lines)
    else:
        page.set_section("Notes", [])


def append_note(page: Page, text: str):
    current = page.section("Notes") or []
    set_notes(page, "\n".join(current + [text]))


def set_priority(page: Page, prio: str | None):
    if prio in (None, "", "none"):
        page.remove("my-priority")
    elif prio in PRIORITIES:
        page.set("my-priority", prio)
    else:
        raise ValueError(f"Priority must be one of {', '.join(PRIORITIES)} or none")


def set_plan(page: Page, month: str | None):
    if month in (None, "", "none"):
        page.remove("planned")
    elif _MONTH_RE.match(month):
        page.set("planned", month)
    else:
        raise ValueError("Month must look like 2026-10")


ACTIONS = {"pick", "done", "drop", "back", "time", "check_add", "check_toggle", "check_remove",
           "notes", "prio", "plan"}


def apply(path: Path, action: str, today: date | None = None, **kw) -> dict:
    """One change to one item, saved. Returns the item's new JSON. Used by the CLI and `lpt serve`."""
    today = today or date.today()
    page = Page(path)
    if not is_item(page):
        raise ValueError(f"{path.name} is not an item")
    if action == "pick":
        pick(page, today)
    elif action == "done":
        finish(page, today)
    elif action == "drop":
        drop(page, today)
    elif action == "back":
        put_back(page, today)
    elif action == "time":
        add_time(page, int(kw["minutes"]), kw.get("day") or today)
    elif action == "check_add":
        check_add(page, str(kw["text"]))
    elif action == "check_toggle":
        check_toggle(page, int(kw["index"]))
    elif action == "check_remove":
        check_remove(page, int(kw["index"]))
    elif action == "notes":
        set_notes(page, str(kw.get("text", "")))
    elif action == "prio":
        set_priority(page, kw.get("prio"))
    elif action == "plan":
        set_plan(page, kw.get("month"))
    else:
        raise ValueError(f"Unknown action '{action}'")
    page.save()
    return to_json(page)


# ---------- capture ----------

def _slug(text: str) -> str:
    t = _URL_RE.sub("", text.strip())
    t = re.sub(r"[^\w.\- ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()[:90] or "Untitled"


def add_items(vault: Path, entries: list[str], today: date | None = None, note: str = "",
              type_: str = "article", prio: str | None = None) -> tuple[list[dict], list[str]]:
    """Capture: one page per non-empty line, straight into Unsorted. Returns (added, skipped duplicates)."""
    today = today or date.today()
    if type_ not in ITEM_TYPES:
        raise ValueError(f"Type must be one of {', '.join(sorted(ITEM_TYPES))}")
    if prio not in (None, "", "none") and prio not in PRIORITIES:
        raise ValueError(f"Priority must be one of {', '.join(PRIORITIES)}")
    pages_dir = Path(vault) / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    existing = [Page(p) for p in item_paths(vault).values()]
    seen = {p.get("source").strip().rstrip("/").lower() for p in existing if p.get("source")}
    seen |= {p.get("title").strip().lower() for p in existing}

    added, skipped = [], []
    for raw in entries:
        line = raw.strip().lstrip("-•*").strip()
        if not line:
            continue
        is_url = bool(_URL_RE.match(line))
        key = line.rstrip("/").lower()
        if key in seen:
            skipped.append(line)
            continue
        seen.add(key)
        stem = _slug(line) if is_url else title_to_filename(line)[:-3]
        path, n = pages_dir / f"{stem}.md", 2
        while path.exists():
            path, n = pages_dir / f"{stem} {n}.md", n + 1
        props = [f"title:: {line}", f"type:: {type_}", "state:: collected"]
        if is_url:
            props.append(f"source:: {line}")
        props.append(f"ingested:: {_link_date(today)}")
        if prio and prio != "none":
            props.append(f"my-priority:: {prio}")
        if note.strip():
            props.append(f"note:: {' '.join(note.split())}")
        props.append("enrich:: pending")
        path.write_text("\n".join(props) + "\n")
        added.append(to_json(Page(path)))
    return added, skipped


def pending_enrichment(vault: Path) -> list[dict]:
    return [i for i in load_items(vault) if i["enrich"]]


def apply_enrichment(vault: Path, item_id: str, meta: dict) -> dict:
    """File a captured item: fill in title, area, topic, concepts and summary, then rename the file to the title."""
    from cli.page_writer import ensure_linked_pages
    paths = item_paths(vault)
    if item_id not in paths:
        raise ValueError(f"No item '{item_id}'")
    page = Page(paths[item_id])
    title = " ".join(str(meta.get("title") or page.get("title")).split())
    page.set("title", title)
    if page.get("type") not in ("project", "practice") and meta.get("medium"):
        page.set("type", meta["medium"])
    for key in ("domain", "topic"):
        if meta.get(key):
            page.set(key, f"[[{meta[key]}]]")
    for key in ("complexity", "size"):
        if meta.get(key):
            page.set(key, meta[key])
    for key in ("concepts", "prerequisites"):
        if meta.get(key):
            page.set(key, ", ".join(f"[[{c}]]" for c in meta[key]))
    if meta.get("summary"):
        page.set_section("Summary", [meta["summary"].strip()])
    if meta.get("key_takeaways"):
        page.set_section("Key Takeaways", [f"- {t}" for t in meta["key_takeaways"]])
    page.remove("enrich")
    page.save()

    target = page.path.with_name(title_to_filename(title))
    if target != page.path and not target.exists():
        page.path.rename(target)
        page.path = target
    ensure_linked_pages(Path(vault), {**meta, "title": title}, title)
    return to_json(Page(page.path))


# ---------- migration ----------

_OLD_PROPS = ("status", "progress", "priority", "started", "completed", "goal")


def migrate(vault: Path) -> dict:
    """One-off move from progress percentages to states. Every item starts as not started.

    Only touches items without a `state::`, so running it twice changes nothing.
    """
    stats = {"items": 0, "other_pages": 0}
    pages = Path(vault) / "pages"
    for f in sorted(pages.glob("*.md")):
        page = Page(f)
        if page.get("type") in ITEM_TYPES:
            if page.get("state"):
                continue
            page.remove(*_OLD_PROPS)
            page.set("state", "collected")
            if page.section("Notes") is None:
                page.rename_section("My Notes", "Notes")
            page.save()
            stats["items"] += 1
        elif page.get("priority"):
            page.remove("priority")
            page.save()
            stats["other_pages"] += 1
    return stats
