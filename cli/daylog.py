"""The day's local Claude Code conversations, condensed for the end-of-day learning routine.

Reads ~/.claude/projects/*/*.jsonl and keeps only what people said: user prompts and the assistant's
text replies (no tool calls, tool output or thinking), for messages timestamped on the given local day.
Sessions about this project itself are skipped, so the routine doesn't learn from its own runs.
"""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"
SKIP_DIRS = ("learning-progress-tracker",)
MAX_CHARS = 1500  # per message; long pastes and replies are cut


def _text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text")
    return ""


def _local_day(stamp: str) -> date | None:
    try:
        return datetime.fromisoformat(stamp.replace("Z", "+00:00")).astimezone().date()
    except (ValueError, AttributeError):
        return None


def sessions(day: date, root: Path = PROJECTS) -> list[dict]:
    out = []
    for path in sorted(root.glob("*/*.jsonl")):
        if any(s in path.parent.name for s in SKIP_DIRS):
            continue
        try:
            if date.fromtimestamp(path.stat().st_mtime) < day:
                continue
            lines = path.read_text(errors="replace").splitlines()
        except OSError:
            continue
        cwd, msgs = "", []
        for line in lines:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("type") not in ("user", "assistant") or d.get("isSidechain") or d.get("isMeta"):
                continue
            if _local_day(d.get("timestamp", "")) != day:
                continue
            text = _text((d.get("message") or {}).get("content")).strip()
            if not text or text.startswith(("<command-", "<local-command", "<system-reminder>", "Caveat:")):
                continue
            cwd = cwd or d.get("cwd", "")
            if len(text) > MAX_CHARS:
                text = text[:MAX_CHARS] + " …[cut]"
            msgs.append({"role": d["type"], "text": text})
        if any(m["role"] == "user" for m in msgs):
            out.append({"session": path.stem, "cwd": cwd, "messages": msgs})
    return out


def render(day: date, root: Path = PROJECTS) -> str:
    parts = []
    for s in sessions(day, root):
        parts.append(f"=== session {s['session']} · {s['cwd']}")
        parts += [f"[{m['role']}] {m['text']}" for m in s["messages"]]
    return "\n\n".join(parts)
