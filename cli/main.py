import json
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path

import click

from cli.config import load_config
from cli.page_writer import write_resource_page, ensure_linked_pages
from cli.priority import recompute_all
from cli.progress import update_progress, mark_done, find_page_by_title, generate_dashboard


def _get_config():
    config_path = os.environ.get("LPT_CONFIG", "config.yaml")
    return load_config(config_path)


def _get_inbox():
    return Path(os.environ.get("LPT_INBOX", "inbox"))


def _get_processed():
    return Path(os.environ.get("LPT_PROCESSED", "processed"))


@click.group()
def cli():
    pass


@cli.command()
@click.argument("source")
@click.option("--domain", default=None)
@click.option("--topic", default=None)
@click.option("--engagement", type=click.Choice(["read", "implement", "background"]), default=None)
@click.option("--tag", multiple=True)
def add(source, domain, topic, engagement, tag):
    is_url = source.startswith("http://") or source.startswith("https://")
    if not is_url:
        source_path = Path(source)
        if not source_path.exists():
            raise click.ClickException(f"File does not exist: {source}")
        source = str(source_path.resolve())

    now = datetime.now()
    job_id = f"{now.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:4]}"
    job = {
        "id": job_id,
        "source": source,
        "source_type": "url" if is_url else "file",
        "domain": domain,
        "topic": topic,
        "engagement": engagement,
        "tags": list(tag),
        "created_at": now.isoformat(timespec="seconds"),
        "status": "pending",
    }
    inbox = _get_inbox()
    inbox.mkdir(parents=True, exist_ok=True)
    job_file = inbox / f"{job_id}.json"
    job_file.write_text(json.dumps(job, indent=2))
    click.echo(f"Added {job_id} to inbox")


@cli.command()
def status():
    inbox = _get_inbox()
    processed = _get_processed()
    inbox.mkdir(parents=True, exist_ok=True)
    processed.mkdir(parents=True, exist_ok=True)

    jobs = list(inbox.glob("*.json"))
    job_files = [j for j in jobs if not j.name.endswith(".result.json")]
    result_files = [j for j in jobs if j.name.endswith(".result.json")]
    processed_files = list(processed.glob("*.json"))

    pending = len([j for j in job_files if not (inbox / f"{j.stem}.result.json").exists()])
    ready = len(result_files)
    done = len([p for p in processed_files if not p.name.endswith(".result.json")])

    click.echo(f"Pending (no result):  {pending}")
    click.echo(f"Ready to write:       {ready}")
    click.echo(f"Processed:            {done}")


@cli.command("write")
@click.argument("job_id", required=False)
@click.option("--all", "write_all", is_flag=True)
def write_cmd(job_id, write_all):
    config = _get_config()
    inbox = _get_inbox()
    processed = _get_processed()
    processed.mkdir(parents=True, exist_ok=True)

    if write_all:
        result_files = list(inbox.glob("*.result.json"))
        if not result_files:
            click.echo("No result files to process")
            return
        for rf in result_files:
            jid = rf.name.replace(".result.json", "")
            _write_single(jid, inbox, processed, config)
        return

    if not job_id:
        raise click.ClickException("Provide a job ID or use --all")

    _write_single(job_id, inbox, processed, config)


def _write_single(job_id: str, inbox: Path, processed: Path, config):
    job_file = inbox / f"{job_id}.json"
    result_file = inbox / f"{job_id}.result.json"

    if not result_file.exists():
        raise click.ClickException(f"No result file for {job_id}. Run the processor first.")

    job = json.loads(job_file.read_text()) if job_file.exists() else {"source": "unknown", "tags": []}
    metadata = json.loads(result_file.read_text())

    page_path = write_resource_page(config.vault_path, metadata, job)
    ensure_linked_pages(config.vault_path, metadata, metadata["title"])
    recompute_all(config.vault_path, config)

    shutil.move(str(job_file), str(processed / job_file.name))
    shutil.move(str(result_file), str(processed / result_file.name))
    click.echo(f"Wrote page: {page_path.name}")


@cli.command()
def init():
    config = _get_config()
    pages_dir = config.vault_path / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    queue_page = pages_dir / "Learning Queue.md"
    content = """title:: Learning Queue
type:: queries

## Next Up (by priority)
{{query (and (property :status "unread") (not (property :type "concept")))}}

## Knowledge Gaps
{{query (property :status "stub")}}

## In Progress
{{query (property :status "in-progress")}}

## By Domain
{{query (and (property :domain "[[ML/Infrastructure]]") (property :status "unread"))}}

## Background Reading
{{query (and (property :status "unread") (property :engagement "background"))}}

## Quick Wins (beginner)
{{query (and (property :status "unread") (property :complexity "beginner"))}}
"""
    queue_page.write_text(content)
    click.echo(f"Initialized vault at {config.vault_path}")


@cli.command("progress")
@click.argument("title")
@click.argument("value", type=int)
def progress_cmd(title, value):
    config = _get_config()
    matched = find_page_by_title(config.vault_path, title)
    if not matched:
        raise click.ClickException(f"No page found matching '{title}'")
    update_progress(config.vault_path, matched, value, config)
    click.echo(f"Updated '{matched}' progress to {value}")


@cli.command()
@click.argument("title")
def done(title):
    config = _get_config()
    matched = find_page_by_title(config.vault_path, title)
    if not matched:
        raise click.ClickException(f"No page found matching '{title}'")
    mark_done(config.vault_path, matched, config)
    click.echo(f"Marked '{matched}' as completed")


@cli.command()
def dashboard():
    config = _get_config()
    path = generate_dashboard(config.vault_path, config)
    click.echo(f"Dashboard written to {path}")


@cli.command()
def recompute():
    config = _get_config()
    count = recompute_all(config.vault_path, config)
    click.echo(f"Recomputed priorities for {count} pages")
