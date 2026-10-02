from __future__ import annotations

import json
import os
import subprocess
import sys
import webbrowser
from datetime import date, timedelta
from pathlib import Path

import click

from cli import items as it
from cli.config import load_config

PROJECT_ROOT = Path(__file__).parent.parent
TYPES = sorted(it.ITEM_TYPES)


def _vault() -> Path:
    config_path = os.environ.get("LPT_CONFIG", "config.yaml")
    try:
        return load_config(config_path).vault_path
    except FileNotFoundError:
        raise click.ClickException(f"Config file not found: {config_path}")
    except Exception as e:
        raise click.ClickException(f"Error loading config: {e}")


def _item(query: str) -> Path:
    path = it.find_item(_vault(), query)
    if not path:
        raise click.ClickException(f"No item matching '{query}'")
    return path


def _apply(query: str, action: str, **kw) -> dict:
    try:
        return it.apply(_item(query), action, **kw)
    except ValueError as e:
        raise click.ClickException(str(e))


def _day(value: str | None) -> date:
    if not value or value == "today":
        return date.today()
    if value == "yesterday":
        return date.today() - timedelta(days=1)
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise click.BadParameter("use today, yesterday or YYYY-MM-DD", param_hint="--date")


def _month(value: str | None) -> str | None:
    today = date.today()
    if value in (None, "", "this", "now"):
        return today.isoformat()[:7]
    if value == "next":
        return (today.replace(day=1) + timedelta(days=32)).isoformat()[:7]
    if value == "none":
        return None
    return value


def _total(item: dict) -> str:
    return it.format_minutes(sum(s["m"] for s in item["sessions"])) if item["sessions"] else "no time"


@click.group()
def cli():
    """Learning workbench: collect things, pick them up, log time, plan the month."""


# ---------- capture ----------

@cli.command()
@click.argument("entries", nargs=-1)
@click.option("--note", default="", help="Why you care (applies to every entry)")
@click.option("--type", "type_", type=click.Choice(TYPES), default="article", show_default=True)
@click.option("--prio", type=click.Choice(["now", "soon", "someday"]), default=None)
def add(entries, note, type_, prio):
    """Add links or titles to the library (Unsorted). With no arguments, reads one per line from stdin."""
    lines = list(entries) or (sys.stdin.read().splitlines() if not sys.stdin.isatty() else [])
    if not lines:
        raise click.UsageError("Give a link or title, or pipe several lines in")
    added, skipped = it.add_items(_vault(), lines, note=note, type_=type_, prio=prio)
    for a in added:
        click.echo(f"+ {a['title']}")
    for s in skipped:
        click.echo(f"= already in the library: {s}")
    click.echo(f"Added {len(added)} to Unsorted" + (f", skipped {len(skipped)}" if skipped else ""))


@cli.command()
@click.argument("item_id", required=False)
@click.option("--from", "from_file", type=click.Path(exists=True, dir_okay=False),
              help="JSON with title, medium, domain, topic, concepts, summary, key_takeaways")
def enrich(item_id, from_file):
    """List captured items waiting to be filed, or file one from a JSON result."""
    vault = _vault()
    if not item_id:
        pending = it.pending_enrichment(vault)
        if not pending:
            click.echo("Nothing waiting to be filed")
        for p in pending:
            click.echo(json.dumps({k: p[k] for k in ("id", "title", "type", "source", "note")}, ensure_ascii=False))
        return
    if not from_file:
        raise click.UsageError("Use --from result.json to file an item")
    try:
        filed = it.apply_enrichment(vault, item_id, json.loads(Path(from_file).read_text()))
    except ValueError as e:
        raise click.ClickException(str(e))
    click.echo(f"Filed '{filed['title']}' under {filed['area']} / {filed['topic'] or '—'}")


# ---------- states ----------

def _state_command(name, action, verb, help_text):
    @cli.command(name, help=help_text)
    @click.argument("title")
    def command(title):
        item = _apply(title, action)
        click.echo(f"{verb} '{item['title']}'")
    return command


_state_command("pick", "pick", "Picked up", "Start working on an item (adds it to this month's plan).")
_state_command("done", "done", "Done:", "Mark an item done.")
_state_command("drop", "drop", "Dropped", "Drop an item: not for you. It stops counting towards its topic.")
_state_command("back", "back", "Put back", "Put an item back to not started. It stays in the plan.")


# ---------- working on an item ----------

@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("title")
@click.argument("amount", default="30m")
@click.option("--date", "day", default=None, help="today (default), yesterday or YYYY-MM-DD")
def time(title, amount, day):
    """Add time to an item: 30m (default), 1h, 1h30m, or -30m to take it back."""
    try:
        minutes = it.parse_minutes(amount)
    except ValueError as e:
        raise click.BadParameter(str(e), param_hint="AMOUNT")
    item = _apply(title, "time", minutes=minutes, day=_day(day))
    today = next((s["m"] for s in item["sessions"] if s["d"] == _day(day).isoformat()), 0)
    click.echo(f"'{item['title']}': {it.format_minutes(today)} on {_day(day).isoformat()}, {_total(item)} total")


@cli.command()
@click.argument("title")
@click.argument("text", required=False)
@click.option("--toggle", type=int, help="Tick or untick item N (1-based)")
@click.option("--remove", type=int, help="Remove item N (1-based)")
def check(title, text, toggle, remove):
    """Show an item's checklist, add to it, or tick / remove an entry."""
    if text:
        item = _apply(title, "check_add", text=text)
    elif toggle:
        item = _apply(title, "check_toggle", index=toggle - 1)
    elif remove:
        item = _apply(title, "check_remove", index=remove - 1)
    else:
        item = it.to_json(it.Page(_item(title)))
    click.echo(item["title"])
    for n, c in enumerate(item["checks"], 1):
        click.echo(f"  {n}. [{'x' if c['done'] else ' '}] {c['t']}")
    if not item["checks"]:
        click.echo("  (empty)")


@cli.command()
@click.argument("title")
@click.argument("text")
def note(title, text):
    """Append a line to an item's notes."""
    path = _item(title)
    page = it.Page(path)
    it.append_note(page, text)
    page.save()
    click.echo(f"Noted on '{page.get('title')}'")


@cli.command()
@click.argument("title")
@click.argument("level", type=click.Choice(["now", "soon", "someday", "none"]))
def prio(title, level):
    """Set your priority for an item."""
    item = _apply(title, "prio", prio=level)
    click.echo(f"'{item['title']}': priority {item['prio'] or 'none'}")


@cli.command()
@click.argument("title")
@click.argument("month", required=False)
def plan(title, month):
    """Plan an item for this month (default), next, a YYYY-MM month, or none."""
    item = _apply(title, "plan", month=_month(month))
    click.echo(f"'{item['title']}': " + (f"planned for {item['planned']}" if item["planned"] else "not planned"))


# ---------- looking ----------

@cli.command()
@click.argument("title")
def show(title):
    """Everything about one item."""
    item = it.to_json(it.Page(_item(title)))
    click.echo(item["title"])
    click.echo(f"  {item['area']}{' / ' + item['topic'] if item['topic'] else ''} · {item['type']} · {item['state']}"
               + (f" · priority {item['prio']}" if item["prio"] else "")
               + (f" · planned {item['planned']}" if item["planned"] else ""))
    click.echo(f"  time: {_total(item)}" + (f", last {item['sessions'][-1]['d']}" if item["sessions"] else ""))
    for n, c in enumerate(item["checks"], 1):
        click.echo(f"  {n}. [{'x' if c['done'] else ' '}] {c['t']}")
    if item["notes"]:
        click.echo("  notes:")
        for line in item["notes"].split("\n"):
            click.echo(f"    {line}")


@cli.command("ls")
@click.option("--state", type=click.Choice(list(it.STATES)), default=None)
@click.option("--unsorted", is_flag=True, help="Only items waiting to be filed")
def ls_cmd(state, unsorted):
    """List items. Default: what's in progress and the rest of this month's plan."""
    all_items = it.load_items(_vault())
    month = date.today().isoformat()[:7]
    if unsorted:
        rows = [i for i in all_items if i["area"] == "Unsorted"]
    elif state:
        rows = [i for i in all_items if i["state"] == state]
    else:
        rows = [i for i in all_items if i["state"] == "picked"
                or (i["planned"] and i["planned"] <= month and i["state"] == "collected")]
    order = {"picked": 0, "collected": 1, "done": 2, "dropped": 3}
    for i in sorted(rows, key=lambda i: (order[i["state"]], i["title"].lower())):
        click.echo(f"{i['state']:<9}  {i['title']}  ({i['area']}, {_total(i)})")
    if not rows:
        click.echo("Nothing here")


@cli.command()
def status():
    """Counts by state."""
    all_items = it.load_items(_vault())
    for s in it.STATES:
        click.echo(f"{s:<10} {sum(1 for i in all_items if i['state'] == s)}")
    click.echo(f"{'unsorted':<10} {sum(1 for i in all_items if i['area'] == 'Unsorted')}")
    click.echo(f"{'to file':<10} {sum(1 for i in all_items if i['enrich'])}")


@cli.command()
def migrate():
    """One-off: convert progress-percentage pages to states. Every item starts as not started."""
    stats = it.migrate(_vault())
    click.echo(f"Migrated {stats['items']} items, cleaned {stats['other_pages']} other pages")


# ---------- the app ----------

def _build_site(vault: Path) -> Path:
    from cli.build_graph import build_site, load_meta
    meta = load_meta(os.environ.get("LPT_CONFIG", "config.yaml"))
    return build_site(str(vault), str(PROJECT_ROOT / "site"), meta)


@cli.command()
@click.option("--no-open", is_flag=True, help="Build without opening in a browser")
def graph(no_open):
    """Build the workbench into site/ (read-only when opened as a file)."""
    path = _build_site(_vault())
    if not no_open:
        subprocess.run(["open", str(path)], check=False)


@cli.command()
@click.option("--port", default=8765, show_default=True)
@click.option("--no-open", is_flag=True, help="Don't open a browser")
def serve(port, no_open):
    """Run the workbench locally with editing: time, notes, checklist, plan and add all write to the vault."""
    from cli.server import make_server
    vault = _vault()
    _build_site(vault)
    server = make_server(vault, PROJECT_ROOT / "site", rebuild=lambda: _build_site(vault), port=port)
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    click.echo(f"Workbench at {url}  (Ctrl+C to stop)")
    if not no_open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        click.echo("\nStopped")
    finally:
        server.server_close()
