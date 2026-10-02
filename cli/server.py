"""`lpt serve`: the built workbench plus a small JSON API so it can edit the vault.

Bound to 127.0.0.1. Writes must be application/json (a cross-site page can't send that without a
CORS preflight, which is never answered here) and the Host header must be local, so other sites
and DNS-rebinding tricks can't drive it.

    GET  /api/items                       every item, fresh from disk
    POST /api/item  {id, action, ...}     one change to one item -> {ok, item}
    POST /api/add   {text, note, type, prio}   capture, one item per line -> {ok, added, skipped}
    GET  /api/save                        {ok, available, pending}: unsaved vault changes
    POST /api/save  {}                    commit the vault and push it (see cli/sync.py) -> {ok, committed, pushed}
"""

from __future__ import annotations

import json
import socket
import threading
from datetime import date
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from cli import items as it
from cli import sync

_LOCAL_HOSTS = {"127.0.0.1", "localhost"}
_write_lock = threading.Lock()


class _NotFound(Exception):
    pass


class _Debounce:
    """Rebuild site/ a moment after the last write, so the file copy stays fresh without slowing clicks."""

    def __init__(self, fn, delay=1.5):
        self.fn, self.delay, self.timer = fn, delay, None

    def __call__(self):
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(self.delay, self._run)
        self.timer.daemon = True
        self.timer.start()

    def _run(self):
        try:
            self.fn()
        except Exception:  # a failed rebuild must never take the server down
            pass


class _Handler(SimpleHTTPRequestHandler):
    vault: Path
    rebuild = None
    save_to: tuple[str, str] | None = None

    def log_message(self, fmt, *args):  # keep the terminal quiet
        pass

    def _json(self, status, body):
        data = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _local(self):
        return self.headers.get("Host", "").rsplit(":", 1)[0].strip("[]") in _LOCAL_HOSTS

    def end_headers(self):
        if not self.path.startswith("/api/"):
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_GET(self):
        route = self.path.split("?")[0]
        if route.startswith("/api/"):
            if not self._local():
                return self._json(403, {"error": "Local requests only"})
            if route == "/api/ping":
                return self._json(200, {"ok": True})
            if route == "/api/items":
                return self._json(200, {"ok": True, "today": date.today().isoformat(),
                                        "items": it.load_items(self.vault)})
            if route == "/api/save":
                if not self.save_to:
                    return self._json(200, {"ok": True, "available": False, "pending": 0})
                return self._json(200, {"ok": True, **sync.status(self.vault, *self.save_to)})
            return self._json(404, {"error": f"No route {route}"})
        return super().do_GET()

    def do_POST(self):
        if not self._local():
            return self._json(403, {"error": "Local requests only"})
        if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
            return self._json(415, {"error": "Content-Type must be application/json"})
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length) or b"{}")
            if not isinstance(body, dict):
                raise ValueError
        except (ValueError, json.JSONDecodeError):
            return self._json(400, {"error": "Invalid JSON"})

        route = self.path.split("?")[0]
        try:
            with _write_lock:
                if route == "/api/item":
                    result = self._item(body)
                elif route == "/api/add":
                    result = self._add(body)
                elif route == "/api/save":
                    if not self.save_to:
                        raise ValueError("Saving isn't set up for this server")
                    result = sync.save(self.vault, *self.save_to)
                else:
                    return self._json(404, {"error": f"No route {route}"})
        except _NotFound as e:
            return self._json(404, {"error": str(e)})
        except KeyError as e:
            return self._json(400, {"error": f"Missing {e}"})
        except (ValueError, TypeError) as e:
            return self._json(400, {"error": str(e) or "Bad request"})
        except sync.SaveError as e:
            return self._json(409, {"error": str(e)})
        type(self).rebuild()
        return self._json(200, {"ok": True, **result})

    def _item(self, body):
        path = it.item_paths(self.vault).get(str(body.get("id", "")))
        if not path:
            raise _NotFound(f"No item '{body.get('id')}'")
        action = str(body.get("action", ""))
        if action not in it.ACTIONS:
            raise ValueError(f"Unknown action '{action}'")
        kw = {k: body[k] for k in ("minutes", "text", "index", "prio", "month") if k in body}
        if "day" in body:
            kw["day"] = date.fromisoformat(str(body["day"]))
        return {"item": it.apply(path, action, **kw)}

    def _add(self, body):
        text = body.get("text", "")
        lines = text.split("\n") if isinstance(text, str) else [str(x) for x in text]
        added, skipped = it.add_items(self.vault, lines, note=str(body.get("note") or ""),
                                      type_=str(body.get("type") or "article"), prio=body.get("prio") or None)
        return {"added": added, "skipped": skipped}


class _Server(ThreadingHTTPServer):
    daemon_threads = True

    def server_bind(self):
        # HTTPServer.server_bind does a reverse-DNS getfqdn() that can stall ~30s on macOS.
        # Keep TCPServer's SO_REUSEADDR so a restarted `lpt serve` can rebind straight away.
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()
        self.server_name, self.server_port = self.server_address[:2]


def make_server(vault: Path, site_dir: Path, rebuild=lambda: None, port: int = 8765, debounce: float = 1.5,
                save_to: tuple[str, str] | None = None):
    handler = type("Handler", (_Handler,), {
        "vault": Path(vault), "save_to": save_to, "rebuild": staticmethod(_Debounce(rebuild, debounce) if debounce else rebuild),
    })
    return _Server(("127.0.0.1", port), partial(handler, directory=str(site_dir)))
