import tarfile
from pathlib import Path

from scripts.train.package_workspace import build


def test_training_workspace_excludes_all_evaluation_surfaces(tmp_path: Path) -> None:
    root=tmp_path/"repo"
    for relative,content in {"AGENTS.md":"rules","scripts/train/run_sft.py":"code","data/seed/train.jsonl":"{}\n","eval/private/decision/secret.task.json":"secret","measurement/result.json":"secret"}.items():
        path=root/relative; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(content)
    archive=tmp_path/"workspace.tar.gz"; manifest=build(root,archive,tmp_path/"manifest.json")
    with tarfile.open(archive) as value: names=value.getnames()
    assert "AGENTS.md" in names and "data/seed/train.jsonl" in names
    assert not any(name.startswith("eval/") or name.startswith("measurement/") for name in names)
    assert not any(name.startswith("scripts/cuda/") or name.startswith("scripts/model/") for name in names)
    assert all(not row["path"].startswith("eval/") for row in manifest["files"])


def test_training_workspace_archive_is_reproducible(tmp_path: Path) -> None:
    root=tmp_path/"repo"; (root/"scripts/train").mkdir(parents=True); (root/"scripts/train/run_sft.py").write_text("code")
    first=build(root,tmp_path/"first.tar.gz",tmp_path/"first.json")
    second=build(root,tmp_path/"second.tar.gz",tmp_path/"second.json")
    assert first["archive_sha256"]==second["archive_sha256"]


def test_training_workspace_uses_a_repository_relative_archive_path(tmp_path: Path) -> None:
    root=tmp_path/"repo"; (root/"scripts/train").mkdir(parents=True); (root/"scripts/train/run_sft.py").write_text("code")
    manifest=build(root,root/"artifacts/train/workspaces/workspace.tar.gz",tmp_path/"manifest.json")
    assert manifest["archive_path"]=="artifacts/train/workspaces/workspace.tar.gz"
