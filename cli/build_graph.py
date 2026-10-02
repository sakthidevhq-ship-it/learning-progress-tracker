"""Build the workbench from the vault.

    python cli/build_graph.py --site ./vault site            # site/index.html (lpt graph / serve)
    python cli/build_graph.py ./vault graph.html out.html     # one file (the Pages workflow)

CI runs this with a bare Python: no click, thefuzz or PyYAML at import time.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:  # when run as a script from CI
    sys.path.insert(0, str(PROJECT_ROOT))

from cli.items import load_items  # noqa: E402

TEMPLATE = PROJECT_ROOT / "ui" / "workbench.html"


def render(template_text: str, items: list[dict], meta: dict | None = None) -> str:
    meta = dict(meta or {})
    meta.setdefault("builtAt", datetime.now().isoformat(timespec="seconds"))
    # </script> inside a note or title must not end the script block
    data = json.dumps(items, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = template_text.replace("VAULT_PLACEHOLDER", data)
    return html.replace("META_PLACEHOLDER", json.dumps(meta).replace("</", "<\\/"))


def build_site(vault_path, out_dir, meta=None) -> Path:
    """Write out_dir/index.html. Returns its path."""
    items = load_items(Path(vault_path))
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "index.html"
    path.write_text(render(TEMPLATE.read_text(), items, meta))
    print(f"Built workbench: {path} ({len(items)} items)")
    return path


def load_meta(config_path="config.yaml") -> dict:
    """Career focus weights for Insights."""
    try:
        text = Path(config_path).read_text()
    except OSError:
        return {}
    try:
        import yaml
        weights = (yaml.safe_load(text) or {}).get("domain_weights", {})
    except ImportError:  # the Pages workflow has no PyYAML: read the one flat block by hand
        weights, inside = {}, False
        for line in text.splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if not line.startswith((" ", "\t")):
                inside = line.split(":")[0].strip() == "domain_weights"
            elif inside and ":" in line:
                key, _, value = line.strip().rpartition(":")
                try:
                    weights[key.strip().strip("'\"")] = float(value)
                except ValueError:
                    pass
    return {"domainWeights": weights}


def build_file(vault_path, output_path, meta=None) -> Path:
    """Write the workbench to a single file (the form the Pages workflow uses)."""
    items = load_items(Path(vault_path))
    out = Path(output_path)
    out.write_text(render(TEMPLATE.read_text(), items, meta))
    print(f"Built workbench: {out} ({len(items)} items)")
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--site":
        # build_graph.py --site [vault] [out_dir]
        build_site(args[1] if len(args) > 1 else "./vault", args[2] if len(args) > 2 else "site", load_meta())
    else:
        # build_graph.py [vault] [template, ignored] [output.html]: what .github/workflows/deploy.yml runs
        build_file(args[0] if args else "./vault", args[2] if len(args) > 2 else "knowledge-graph.html", load_meta())
