#!/usr/bin/env python3
"""Create a deterministic development-only evaluation workspace archive."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ALLOWLIST = (
    "AGENTS.md", "pyproject.toml", "uv.lock",
    "configs/eval/runtimes.json",
    "configs/inference/qwen_base_development.json",
    "configs/model/qwen3_5_2b.contract.json",
    "configs/model/qwen3_5_2b.inventory.json",
    "scripts/__init__.py",
    "scripts/cuda/__init__.py", "scripts/cuda/qualify.py",
    "scripts/eval/__init__.py", "scripts/eval/contracts.py", "scripts/eval/run_task.py",
    "scripts/eval/verify_runtime_images.py",
    "scripts/inference", "scripts/verify",
    "eval/private/development",
    "manifests/evaluation/private/development-tranche1.json",
    "manifests/evaluation/private/development-tranche2.json",
    "manifests/evaluation/private/development-tranche3.json",
    "manifests/evaluation/private/development-tranche4.json",
    "manifests/evaluation/private/development-tranche5.json",
    "manifests/evaluation/private/development-tranche6.json",
)
FORBIDDEN_PARTS = {
    ".git", ".gcloud-staging", "__pycache__", "artifacts", "checkpoints",
    "decision", "measurement", "outputs", "retention", "seed", "train",
}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect(root: Path) -> list[Path]:
    files: set[Path] = set()
    for relative in ALLOWLIST:
        path = root / relative
        if path.is_file():
            if FORBIDDEN_PARTS & set(path.relative_to(root).parts):
                raise ValueError(f"forbidden evaluation workspace allowlist entry: {relative}")
            files.add(path)
        elif path.is_dir():
            files.update(
                item for item in path.rglob("*")
                if item.is_file() and not FORBIDDEN_PARTS & set(item.relative_to(root).parts)
            )
        else:
            raise ValueError(f"evaluation workspace allowlist entry is missing: {relative}")
    selected: list[Path] = []
    for path in sorted(files):
        relative = path.relative_to(root)
        selected.append(path)
    task_count = sum(path.name.endswith(".task.json") for path in selected)
    if task_count != 180:
        raise ValueError(f"evaluation workspace requires exactly 180 development tasks, found {task_count}")
    if any("authoring" in path.relative_to(root).parts for path in selected):
        raise ValueError("evaluation authoring code must not enter the execution workspace")
    return selected


def build(root: Path, archive: Path, manifest_path: Path) -> dict[str, object]:
    files = collect(root)
    entries = [
        {"path": str(path.relative_to(root)), "size_bytes": path.stat().st_size, "sha256": file_sha256(path)}
        for path in files
    ]
    archive.parent.mkdir(parents=True, exist_ok=True)
    with archive.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as output:
                for path in files:
                    relative = str(path.relative_to(root))
                    info = output.gettarinfo(str(path), arcname=relative)
                    info.uid = info.gid = 0
                    info.uname = info.gname = ""
                    info.mtime = 0
                    with path.open("rb") as handle:
                        output.addfile(info, handle)
    try:
        archive_label = str(archive.relative_to(root))
    except ValueError:
        archive_label = str(archive)
    manifest: dict[str, object] = {
        "schema_version": "ganesh-mini-development-evaluation-workspace/v1",
        "status": "sealed",
        "surface": "development",
        "task_count": 180,
        "archive": {"path": archive_label, "size_bytes": archive.stat().st_size, "sha256": file_sha256(archive)},
        "forbidden_parts": sorted(FORBIDDEN_PARTS),
        "files": entries,
    }
    payload = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
    manifest["manifest_sha256"] = hashlib.sha256(payload).hexdigest()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    manifest = build(args.root.resolve(), args.archive.resolve(), args.manifest.resolve())
    print(json.dumps({"status": manifest["status"], "manifest_sha256": manifest["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
