"""`lpt save` / the app's Save button: commit vault changes and push them to the branch GitHub Pages builds from.

Only files under the vault are ever committed. If the remote moved on (a save from another machine), local commits
are rebased onto it first. Saving refuses when the current branch carries code commits the remote doesn't have, so
a Save click can never ship half-done work to the live site.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


class SaveError(Exception):
    pass


def _git(root: Path, *args: str, check: bool = True) -> str:
    res = subprocess.run(["git", "-C", str(root), "-c", "core.quotepath=off", *args], capture_output=True, text=True)
    if check and res.returncode:
        raise SaveError((res.stderr or res.stdout).strip() or f"git {args[0]} failed")
    return res.stdout.strip()


def repo_root(vault: Path) -> Path | None:
    res = subprocess.run(["git", "-C", str(vault), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return Path(res.stdout.strip()) if res.returncode == 0 else None


def _vault_spec(root: Path, vault: Path) -> str:
    return str(Path(vault).resolve().relative_to(root.resolve())) or "."


def pending(vault: Path) -> list[str]:
    """Vault files changed since the last commit (repo-relative paths)."""
    root = repo_root(vault)
    if not root:
        return []
    fields = _git(root, "status", "--porcelain", "-z", "-uall", "--", _vault_spec(root, vault)).split("\0")
    paths = []
    while fields:
        entry = fields.pop(0)
        if not entry:
            continue
        paths.append(entry[3:])
        if entry[0] in "RC":  # a rename is followed by its old path
            fields.pop(0)
    return paths


def _unpushed(root: Path, upstream: str) -> int:
    """Commits not on the remote branch as of the last fetch (a save whose push failed)."""
    out = _git(root, "rev-list", "--count", f"{upstream}..HEAD", check=False)
    return int(out) if out.isdigit() else 0


def status(vault: Path, remote: str, branch: str) -> dict:
    root = repo_root(vault)
    if not root or remote not in _git(root, "remote").split():
        return {"available": False, "pending": 0}
    return {"available": True, "pending": len(pending(vault)), "unpushed": _unpushed(root, f"{remote}/{branch}"),
            "target": f"{remote}/{branch}"}


def _message(paths: list[str]) -> str:
    names = sorted({Path(p).stem.replace("___", "/") for p in paths})
    shown = ", ".join(names[:3]) + (f" and {len(names) - 3} more" if len(names) > 3 else "")
    return f"Update library: {shown}"


def save(vault: Path, remote: str, branch: str, message: str | None = None) -> dict:
    root = repo_root(vault)
    if not root:
        raise SaveError(f"{vault} isn't inside a git repository")
    if remote not in _git(root, "remote").split():
        raise SaveError(f"No git remote called '{remote}' (set save.remote in config.yaml)")
    spec = _vault_spec(root, vault)

    changed = pending(vault)
    if changed:
        _git(root, "add", "-A", "--", spec)
        _git(root, "commit", "-q", "-m", message or _message(changed), "--", spec)

    _git(root, "fetch", "-q", remote, branch)
    upstream = f"{remote}/{branch}"
    base = _git(root, "merge-base", upstream, "HEAD", check=False)
    if not base:
        raise SaveError(f"This branch shares no history with {upstream}")
    code = [p for p in _git(root, "diff", "--name-only", base, "HEAD").splitlines()
            if p != spec and not p.startswith(spec.rstrip("/") + "/")]
    if code:
        raise SaveError(f"This branch has code changes that aren't on {upstream} yet "
                        f"({', '.join(code[:3])}{'…' if len(code) > 3 else ''}). Merge them first, or save from {branch}.")
    if base != _git(root, "rev-parse", upstream):  # the remote has commits this branch lacks
        try:
            _git(root, "rebase", "-q", "--autostash", upstream)
        except SaveError:
            _git(root, "rebase", "--abort", check=False)
            raise SaveError(f"Couldn't combine with changes already on {upstream}: the same page changed in both "
                            "places. Resolve it in git, then save again.")

    ahead = _unpushed(root, upstream)
    if ahead:
        _git(root, "push", "-q", remote, f"HEAD:{branch}")
    return {"committed": len(changed), "pushed": ahead, "target": upstream,
            "commit": _git(root, "rev-parse", "--short", "HEAD")}
