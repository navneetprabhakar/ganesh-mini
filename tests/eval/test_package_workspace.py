from __future__ import annotations

import tarfile
from pathlib import Path

import pytest

from scripts.eval.package_workspace import ALLOWLIST, build


def create_workspace(root: Path) -> None:
    for relative in ALLOWLIST:
        path = root / relative
        if relative == "eval/private/development":
            for index in range(180):
                task = path / f"task-{index:03}.task.json"
                task.parent.mkdir(parents=True, exist_ok=True)
                task.write_text("{}")
        elif Path(relative).suffix:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(relative)
        else:
            path.mkdir(parents=True, exist_ok=True)
            (path / "module.py").write_text(relative)


def test_workspace_contains_only_development_execution_material(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    create_workspace(root)
    secret = root / "eval/private/decision/secret.task.json"
    secret.parent.mkdir(parents=True)
    secret.write_text("secret")
    cache = root / "scripts/inference/__pycache__/module.pyc"
    cache.parent.mkdir(parents=True)
    cache.write_bytes(b"cache")
    archive = tmp_path / "workspace.tar.gz"
    manifest = build(root, archive, tmp_path / "manifest.json")
    with tarfile.open(archive) as value:
        names = value.getnames()
    assert manifest["task_count"] == 180
    assert "eval/private/decision/secret.task.json" not in names
    assert "scripts/inference/__pycache__/module.pyc" not in names
    assert not any("decision" in Path(name).parts or "train" in Path(name).parts for name in names)


def test_workspace_archive_is_deterministic(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    create_workspace(root)
    first = build(root, tmp_path / "first.tar.gz", tmp_path / "first.json")
    second = build(root, tmp_path / "second.tar.gz", tmp_path / "second.json")
    assert first["archive"]["sha256"] == second["archive"]["sha256"]


def test_workspace_fails_closed_on_missing_allowlist_entry(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    create_workspace(root)
    (root / "AGENTS.md").unlink()
    with pytest.raises(ValueError, match="allowlist entry is missing"):
        build(root, tmp_path / "workspace.tar.gz", tmp_path / "manifest.json")
