import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from cli.build_graph import build_site, render

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def vault(tmp_path):
    pages = tmp_path / "vault" / "pages"
    pages.mkdir(parents=True)
    (pages / "Paper A.md").write_text(
        "title:: Paper A </script><b>\n"
        "type:: paper\ndomain:: [[Systems]]\nstate:: done\ndone:: [[2026-09-20]]\n"
        "\n## Summary\nA paper.\n\n## Time\n- 2026-09-20 · 1h\n"
    )
    (pages / "Some Concept.md").write_text("title:: Some Concept\ntype:: concept\nstatus:: stub\n")
    return tmp_path / "vault"


def embedded(html):
    return json.loads(re.search(r"const RAW = (\[.*?\]);\n", html, re.S).group(1))


def test_build_site_writes_the_workbench_with_items_only(vault, tmp_path):
    path = build_site(str(vault), str(tmp_path / "site"), meta={"domainWeights": {"Systems": 0.8}})
    html = path.read_text()
    assert path.name == "index.html"
    assert "VAULT_PLACEHOLDER" not in html and "META_PLACEHOLDER" not in html
    data = embedded(html)
    assert [d["title"] for d in data] == ["Paper A </script><b>"]
    assert data[0]["sessions"] == [{"d": "2026-09-20", "m": 60}]
    meta = json.loads(re.search(r"const META = (\{.*?\});\n", html, re.S).group(1))
    assert meta["domainWeights"] == {"Systems": 0.8} and "builtAt" in meta


def test_titles_cannot_close_the_script_tag(vault, tmp_path):
    html = build_site(str(vault), str(tmp_path / "site")).read_text()
    script = html[html.index("const RAW"):]
    assert "</script><b>" not in script.split("\n")[0]


def test_render_fills_placeholders():
    out = render("A VAULT_PLACEHOLDER B META_PLACEHOLDER", [{"x": 1}], {"y": 2})
    assert out.startswith('A [{"x":1}] B {"y": 2')


@pytest.mark.parametrize("argv,out", [
    (["--site", "{vault}", "{tmp}/_site"], "_site/index.html"),
    (["{vault}", "graph.html", "{tmp}/knowledge-graph.html"], "knowledge-graph.html"),  # .github/workflows/deploy.yml
])
def test_ci_entry_points_run_on_bare_python(vault, tmp_path, argv, out):
    # The Pages workflow runs this with a bare Python: no click, thefuzz or PyYAML
    argv = [a.format(vault=vault, tmp=tmp_path) for a in argv]
    code = ("import sys, runpy; sys.modules['click'] = None; sys.modules['thefuzz'] = None; sys.modules['yaml'] = None; "
            f"sys.argv = ['build_graph.py'] + {argv!r}; "
            f"runpy.run_path({str(ROOT / 'cli' / 'build_graph.py')!r}, run_name='__main__')")
    subprocess.run([sys.executable, "-c", code], check=True, cwd=ROOT)
    html = (tmp_path / out).read_text()
    assert "Paper A" in html and "VAULT_PLACEHOLDER" not in html


def test_load_meta_without_yaml_matches_with_yaml(tmp_path, monkeypatch):
    from cli.build_graph import load_meta
    cfg = ROOT / "config.yaml"
    with_yaml = load_meta(str(cfg))
    monkeypatch.setitem(sys.modules, "yaml", None)
    assert load_meta(str(cfg)) == with_yaml and with_yaml["domainWeights"]
