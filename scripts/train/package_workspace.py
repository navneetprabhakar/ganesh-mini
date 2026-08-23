#!/usr/bin/env python3
"""Create a content-sealed training workspace that cannot contain evaluation data."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import tarfile
from pathlib import Path


ALLOWLIST = (
    "AGENTS.md", "pyproject.toml", "uv.lock",
    "configs/cuda", "configs/model", "configs/train", "configs/data",
    "containers/cuda", "scripts/cuda", "scripts/model", "scripts/train",
    "data/seed", "manifests/datasets", "schemas/train",
    "artifacts/train/seed-pilot/prepared-train.jsonl",
    "artifacts/train/seed-pilot/prepared-validation.jsonl",
    "artifacts/train/seed-pilot/prepared-dataset-manifest.json",
)
FORBIDDEN_PARTS = {"eval", "measurement", "outputs", ".git", ".gcloud-staging", "__pycache__"}


def sha256(path: Path) -> str:
    digest=hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda:handle.read(1024*1024),b""): digest.update(chunk)
    return digest.hexdigest()


def collect(root: Path) -> list[Path]:
    files=set()
    for relative in ALLOWLIST:
        path=root/relative
        if path.is_file(): files.add(path)
        elif path.is_dir(): files.update(item for item in path.rglob("*") if item.is_file())
    result=[]
    for path in sorted(files):
        relative=path.relative_to(root)
        if FORBIDDEN_PARTS & set(relative.parts): continue
        result.append(path)
    if not result: raise ValueError("training workspace allowlist is empty")
    if any("eval" in path.relative_to(root).parts for path in result): raise ValueError("evaluation data escaped training workspace isolation")
    return result


def build(root: Path, archive: Path, manifest_path: Path) -> dict:
    files=collect(root)
    entries=[{"path":str(path.relative_to(root)),"size":path.stat().st_size,"sha256":sha256(path)} for path in files]
    archive.parent.mkdir(parents=True,exist_ok=True)
    with archive.open("wb") as raw:
        with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=0) as compressed:
            with tarfile.open(fileobj=compressed,mode="w",format=tarfile.PAX_FORMAT) as output:
                for path in files:
                    info=output.gettarinfo(str(path),arcname=str(path.relative_to(root))); info.uid=info.gid=0; info.uname=info.gname=""; info.mtime=0
                    with path.open("rb") as handle: output.addfile(info,handle)
    manifest={"schema_version":"ganesh-mini-training-workspace/v1","status":"sealed","archive_path":str(archive),"archive_size":archive.stat().st_size,"archive_sha256":sha256(archive),"forbidden_roots":sorted(FORBIDDEN_PARTS),"files":entries}
    payload=json.dumps(manifest,sort_keys=True,separators=(",", ":")).encode(); manifest["manifest_sha256"]=hashlib.sha256(payload).hexdigest()
    manifest_path.parent.mkdir(parents=True,exist_ok=True); manifest_path.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    return manifest


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[2]); parser.add_argument("--archive",type=Path,required=True); parser.add_argument("--manifest",type=Path,required=True); args=parser.parse_args(); build(args.root.resolve(),args.archive.resolve(),args.manifest.resolve()); return 0


if __name__=="__main__": raise SystemExit(main())
