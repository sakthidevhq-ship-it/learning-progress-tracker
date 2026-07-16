import json
import re
import sys
from pathlib import Path

PROP_RE = re.compile(r"^([a-zA-Z_-]+)::\s*(.*)$")
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")

def parse_links(val):
    return LINK_RE.findall(val) if val else []

def parse_page(path):
    content = path.read_text()
    props = {}
    body_lines = []
    in_body = False
    for line in content.split("\n"):
        if not in_body:
            m = PROP_RE.match(line)
            if m:
                props[m.group(1)] = m.group(2).strip()
            elif line.strip() == "":
                continue
            else:
                in_body = True
                body_lines.append(line)
        else:
            body_lines.append(line)

    summary = ""
    in_summary = False
    for line in body_lines:
        if line.startswith("## Summary"):
            in_summary = True
            continue
        elif line.startswith("## ") and in_summary:
            break
        elif in_summary and line.strip():
            summary += line.strip() + " "

    return {
        "title": props.get("title", path.stem),
        "type": props.get("type", ""),
        "domain": props.get("domain", ""),
        "topic": props.get("topic", ""),
        "status": props.get("status", ""),
        "progress": props.get("progress", ""),
        "complexity": props.get("complexity", ""),
        "size": props.get("size", ""),
        "goal": props.get("goal", ""),
        "priority": props.get("priority", ""),
        "engagement": props.get("engagement", ""),
        "prerequisites": props.get("prerequisites", ""),
        "concepts": props.get("concepts", ""),
        "referencedBy": props.get("referenced-by", ""),
        "summary": summary.strip(),
    }

RES_TYPES = {"paper", "article", "video", "docs", "tweet"}

def compute_resource_prereqs(data):
    resources = [d for d in data if d["type"] in RES_TYPES]

    # Build: concept -> list of resource titles that teach it
    concept_teachers = {}
    for r in resources:
        for c in parse_links(r["concepts"]):
            concept_teachers.setdefault(c, []).append(r["title"])

    # For each resource, find which other resources teach its prerequisites
    for r in resources:
        prereq_concepts = parse_links(r["prerequisites"])
        prereq_resources = set()
        for pc in prereq_concepts:
            for teacher in concept_teachers.get(pc, []):
                if teacher != r["title"]:
                    prereq_resources.add(teacher)
        r["prereqResources"] = sorted(prereq_resources)

    # Learning-depth levels: intrinsic floor + SCC-condensed chain propagation
    try:
        from cli.levels import assign_levels
    except ImportError:
        from levels import assign_levels
    title_to_idx = {r["title"]: i for i, r in enumerate(resources)}
    level_nodes = [
        {
            "complexity": r.get("complexity", ""),
            "prereq_count": len(parse_links(r["prerequisites"])),
            "size": r.get("size", ""),
        }
        for r in resources
    ]
    level_edges = []
    for i, r in enumerate(resources):
        for t in r["prereqResources"]:
            j = title_to_idx.get(t)
            if j is not None:
                level_edges.append((j, i))
    levels = assign_levels(level_nodes, level_edges)
    for r, lv in zip(resources, levels):
        r["level"] = round(lv, 2)

    # Sibling edges: resources that share prerequisites (but no direct prereq link)
    # These create weaker "related" connections
    prereq_sets = {}
    for r in resources:
        prereq_sets[r["title"]] = set(parse_links(r["prerequisites"]))

    siblings = []
    titles = [r["title"] for r in resources]
    for i in range(len(titles)):
        for j in range(i + 1, len(titles)):
            if not prereq_sets[titles[i]] or not prereq_sets[titles[j]]:
                continue
            shared = prereq_sets[titles[i]] & prereq_sets[titles[j]]
            if len(shared) >= 2:
                # Only if they don't already have a direct prereq edge
                a_prereqs = set(next(r for r in resources if r["title"] == titles[i])["prereqResources"])
                b_prereqs = set(next(r for r in resources if r["title"] == titles[j])["prereqResources"])
                if titles[j] not in a_prereqs and titles[i] not in b_prereqs:
                    siblings.append({"a": titles[i], "b": titles[j], "shared": sorted(shared)})

    for r in resources:
        r["siblingResources"] = [
            {"title": s["b"] if s["a"] == r["title"] else s["a"], "shared": s["shared"]}
            for s in siblings
            if s["a"] == r["title"] or s["b"] == r["title"]
        ]

def build(vault_path, html_template, output_path):
    pages_dir = Path(vault_path) / "pages"
    data = []
    for f in sorted(pages_dir.glob("*.md")):
        page = parse_page(f)
        if page["type"] in ("dashboard", "queries", ""):
            continue
        data.append(page)

    compute_resource_prereqs(data)

    html = Path(html_template).read_text()
    html = html.replace("VAULT_PLACEHOLDER", json.dumps(data, indent=2))
    Path(output_path).write_text(html)

    res_count = sum(1 for d in data if d["type"] in RES_TYPES)
    prereq_edges = sum(len(d.get("prereqResources", [])) for d in data)
    print(f"Built graph: {output_path} ({len(data)} nodes, {res_count} resources, {prereq_edges} prerequisite edges)")

if __name__ == "__main__":
    vault = sys.argv[1] if len(sys.argv) > 1 else "/Users/sakthi/logseq"
    template = sys.argv[2] if len(sys.argv) > 2 else "graph.html"
    output = sys.argv[3] if len(sys.argv) > 3 else "knowledge-graph.html"
    build(vault, template, output)
