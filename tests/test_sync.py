import subprocess

import pytest

from cli import sync


def git(cwd, *args):
    return subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True).stdout.strip()


def clone(remote, path):
    subprocess.run(["git", "clone", "-q", str(remote), str(path)], check=True)
    git(path, "config", "user.email", "t@example.com")
    git(path, "config", "user.name", "Test")
    return path


@pytest.fixture
def repo(tmp_path):
    """A checkout on main with a vault, pushed to a bare 'origin'."""
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], check=True)
    work = clone(remote, tmp_path / "work")
    (work / "vault" / "pages").mkdir(parents=True)
    (work / "vault" / "pages" / "Raft.md").write_text("title:: Raft\ntype:: paper\nstate:: collected\n")
    (work / "app.py").write_text("print(1)\n")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "init")
    git(work, "push", "-q", "origin", "HEAD:main")
    return {"remote": remote, "work": work, "vault": work / "vault", "tmp": tmp_path}


def remote_log(repo):
    return git(repo["remote"], "log", "--format=%s", "main").splitlines()


def test_status_counts_unsaved_vault_files(repo):
    assert sync.status(repo["vault"], "origin", "main") == {"available": True, "pending": 0, "unpushed": 0,
                                                             "target": "origin/main"}
    (repo["vault"] / "pages" / "Raft.md").write_text("title:: Raft\ntype:: paper\nstate:: picked\n")
    (repo["vault"] / "pages" / "New.md").write_text("title:: New\ntype:: article\n")
    (repo["work"] / "app.py").write_text("print(2)\n")  # not in the vault: doesn't count
    assert sync.status(repo["vault"], "origin", "main")["pending"] == 2


def test_status_unavailable_outside_git_or_without_remote(repo, tmp_path):
    loose = tmp_path / "loose"
    loose.mkdir()
    assert sync.status(loose, "origin", "main")["available"] is False
    assert sync.status(repo["vault"], "nope", "main")["available"] is False


def test_save_commits_only_the_vault_and_pushes(repo):
    (repo["vault"] / "pages" / "Raft.md").write_text("title:: Raft\ntype:: paper\nstate:: picked\n")
    (repo["work"] / "app.py").write_text("print(2)\n")
    r = sync.save(repo["vault"], "origin", "main")
    assert r["committed"] == 1 and r["pushed"] == 1
    assert remote_log(repo)[0] == "Update library: Raft"
    assert git(repo["remote"], "show", "--name-only", "--format=", "main") == "vault/pages/Raft.md"
    assert sync.pending(repo["vault"]) == []
    assert git(repo["work"], "status", "--porcelain") == "M app.py"  # code change left alone


def test_save_with_nothing_to_do(repo):
    r = sync.save(repo["vault"], "origin", "main")
    assert r["committed"] == 0 and r["pushed"] == 0
    assert remote_log(repo) == ["init"]


def test_save_rebases_onto_a_save_from_another_machine(repo):
    other = clone(repo["remote"], repo["tmp"] / "other")
    (other / "vault" / "pages" / "Other.md").write_text("title:: Other\ntype:: article\n")
    git(other, "add", "-A")
    git(other, "commit", "-q", "-m", "from phone laptop")
    git(other, "push", "-q", "origin", "HEAD:main")

    (repo["vault"] / "pages" / "Raft.md").write_text("title:: Raft\ntype:: paper\nstate:: done\n")
    r = sync.save(repo["vault"], "origin", "main")
    assert r["pushed"] == 1
    assert remote_log(repo) == ["Update library: Raft", "from phone laptop", "init"]
    assert (repo["vault"] / "pages" / "Other.md").exists()


def test_save_refuses_a_branch_with_unmerged_code(repo):
    git(repo["work"], "checkout", "-q", "-b", "feature")
    (repo["work"] / "app.py").write_text("print('half done')\n")
    git(repo["work"], "commit", "-qam", "wip")
    (repo["vault"] / "pages" / "Raft.md").write_text("title:: Raft\ntype:: paper\nstate:: done\n")
    with pytest.raises(sync.SaveError, match="code changes.*app.py"):
        sync.save(repo["vault"], "origin", "main")
    assert remote_log(repo) == ["init"]


def test_save_reports_a_conflict_and_leaves_the_repo_usable(repo):
    other = clone(repo["remote"], repo["tmp"] / "other")
    (other / "vault" / "pages" / "Raft.md").write_text("title:: Raft\ntype:: paper\nstate:: dropped\n")
    git(other, "commit", "-qam", "dropped elsewhere")
    git(other, "push", "-q", "origin", "HEAD:main")

    (repo["vault"] / "pages" / "Raft.md").write_text("title:: Raft\ntype:: paper\nstate:: done\n")
    with pytest.raises(sync.SaveError, match="Couldn't combine"):
        sync.save(repo["vault"], "origin", "main")
    assert git(repo["work"], "status", "--porcelain") == ""  # rebase aborted, local commit kept
    assert sync.status(repo["vault"], "origin", "main")["unpushed"] == 1  # the app keeps offering to save
    assert "state:: done" in (repo["vault"] / "pages" / "Raft.md").read_text()


def test_save_handles_non_ascii_and_renamed_pages(repo):
    pages = repo["vault"] / "pages"
    (pages / "Raft — Consensus.md").write_text("title:: Raft — Consensus\ntype:: paper\n")
    sync.save(repo["vault"], "origin", "main")
    git(repo["work"], "mv", "vault/pages/Raft — Consensus.md", "vault/pages/Raft — Renamed.md")
    assert sync.pending(repo["vault"]) == ["vault/pages/Raft — Renamed.md"]
    r = sync.save(repo["vault"], "origin", "main")
    assert r["pushed"] == 1 and remote_log(repo)[0] == "Update library: Raft — Renamed"
