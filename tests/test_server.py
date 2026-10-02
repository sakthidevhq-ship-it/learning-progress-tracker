import json
import threading
import urllib.error
import urllib.request
from datetime import date

import pytest

from cli.items import load_items
from cli.server import make_server


@pytest.fixture
def served(tmp_path):
    vault = tmp_path / "vault"
    (vault / "pages").mkdir(parents=True)
    (vault / "pages" / "Raft Paper.md").write_text(
        "title:: Raft Paper\ntype:: paper\ndomain:: [[Systems]]\nstate:: collected\n"
    )
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text("<h1>hello</h1>")
    rebuilds = []
    server = make_server(vault, site, rebuild=lambda: rebuilds.append(1), port=0, debounce=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    yield {"base": base, "vault": vault, "rebuilds": rebuilds}
    server.shutdown()
    server.server_close()


def call(url, body=None, content_type="application/json", host=None):
    data = None if body is None else json.dumps(body).encode()
    headers = {"Content-Type": content_type}
    if host:
        headers["Host"] = host
    req = urllib.request.Request(url, data=data, method="POST" if body is not None else "GET", headers=headers)
    try:
        with urllib.request.urlopen(req) as res:
            return res.status, json.loads(res.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def raft(served):
    return next(i for i in load_items(served["vault"]) if i["title"] == "Raft Paper")


def test_serves_the_site(served):
    with urllib.request.urlopen(served["base"] + "/") as res:
        assert b"hello" in res.read()


def test_items_endpoint(served):
    status, body = call(served["base"] + "/api/items")
    assert status == 200
    assert body["today"] == date.today().isoformat()
    assert [i["id"] for i in body["items"]] == ["Raft Paper"]


def test_item_actions_write_the_vault_and_return_the_item(served):
    status, body = call(served["base"] + "/api/item", {"id": "Raft Paper", "action": "time", "minutes": 30})
    assert status == 200 and body["item"]["state"] == "picked"
    assert body["item"]["sessions"] == [{"d": date.today().isoformat(), "m": 30}]
    call(served["base"] + "/api/item", {"id": "Raft Paper", "action": "notes", "text": "Read half"})
    call(served["base"] + "/api/item", {"id": "Raft Paper", "action": "check_add", "text": "Implement"})
    call(served["base"] + "/api/item", {"id": "Raft Paper", "action": "prio", "prio": "now"})
    it = raft(served)
    assert (it["notes"], it["checks"], it["prio"]) == ("Read half", [{"t": "Implement", "done": False}], "now")
    assert served["rebuilds"] == [1, 1, 1, 1]


def test_time_on_a_given_day(served):
    status, body = call(served["base"] + "/api/item", {"id": "Raft Paper", "action": "time", "minutes": 60, "day": "2026-10-01"})
    assert status == 200 and body["item"]["sessions"] == [{"d": "2026-10-01", "m": 60}]


def test_unknown_item_404_and_bad_action_400(served):
    assert call(served["base"] + "/api/item", {"id": "../../etc/passwd", "action": "pick"})[0] == 404
    assert call(served["base"] + "/api/item", {"id": "Raft Paper", "action": "explode"})[0] == 400
    assert call(served["base"] + "/api/item", {"id": "Raft Paper", "action": "time"})[0] == 400
    assert call(served["base"] + "/api/item", {"id": "Raft Paper", "action": "plan", "month": "soon"})[0] == 400


def test_add_lines(served):
    status, body = call(served["base"] + "/api/add",
                        {"text": "https://example.com/x\nBuild a thing\nhttps://example.com/x", "note": "n", "type": "article", "prio": "soon"})
    assert status == 200
    assert [a["title"] for a in body["added"]] == ["https://example.com/x", "Build a thing"]
    assert body["skipped"] == ["https://example.com/x"]


def test_add_rejects_bad_type(served):
    assert call(served["base"] + "/api/add", {"text": "x", "type": "spaceship"})[0] == 400


def test_rejects_non_json_posts(served):
    # Blocks simple cross-site form posts: those can't send application/json without a CORS preflight
    status, _ = call(served["base"] + "/api/item", {"id": "Raft Paper", "action": "pick"}, content_type="text/plain")
    assert status == 415
    assert raft(served)["state"] == "collected"


def test_rejects_foreign_host_header(served):
    # DNS rebinding: a page on evil.example resolving to 127.0.0.1 still sends its own Host
    status, _ = call(served["base"] + "/api/item", {"id": "Raft Paper", "action": "pick"}, host="evil.example")
    assert status == 403
    assert call(served["base"] + "/api/items", host="evil.example:8765")[0] == 403
    assert raft(served)["state"] == "collected"


def test_restart_can_rebind_the_same_port_immediately(tmp_path):
    # A client connection leaves the port in TIME_WAIT after shutdown; restarting must still work
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text("x")
    first = make_server(tmp_path, site, port=0, debounce=0)
    port = first.server_address[1]
    t = threading.Thread(target=first.serve_forever, daemon=True)
    t.start()
    urllib.request.urlopen(f"http://127.0.0.1:{port}/").read()
    first.shutdown()
    first.server_close()
    second = make_server(tmp_path, site, port=port, debounce=0)
    second.server_close()


def test_save_endpoints_off_without_a_target(served):
    assert call(served["base"] + "/api/save") == (200, {"ok": True, "available": False, "pending": 0})
    status, body = call(served["base"] + "/api/save", {})
    assert status == 400


def test_save_endpoints_commit_and_push(tmp_path):
    import subprocess
    run = lambda *a, cwd=None: subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout
    remote, work = tmp_path / "remote.git", tmp_path / "work"
    run("git", "init", "-q", "--bare", "-b", "main", str(remote))
    run("git", "clone", "-q", str(remote), str(work))
    run("git", "config", "user.email", "t@example.com", cwd=work)
    run("git", "config", "user.name", "Test", cwd=work)
    (work / "vault" / "pages").mkdir(parents=True)
    (work / "vault" / "pages" / "Raft Paper.md").write_text("title:: Raft Paper\ntype:: paper\nstate:: collected\n")
    run("git", "add", "-A", cwd=work)
    run("git", "commit", "-qm", "init", cwd=work)
    run("git", "push", "-q", "origin", "HEAD:main", cwd=work)

    site = tmp_path / "site"
    site.mkdir()
    server = make_server(work / "vault", site, port=0, debounce=0, save_to=("origin", "main"))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        assert call(base + "/api/item", {"id": "Raft Paper", "action": "pick"})[0] == 200
        assert call(base + "/api/save")[1]["pending"] == 1
        status, body = call(base + "/api/save", {})
        assert status == 200 and body["committed"] == 1 and body["pushed"] == 1
        assert call(base + "/api/save")[1]["pending"] == 0
        assert run("git", "log", "--format=%s", "main", cwd=remote).splitlines()[0] == "Update library: Raft Paper"
    finally:
        server.shutdown()
        server.server_close()
