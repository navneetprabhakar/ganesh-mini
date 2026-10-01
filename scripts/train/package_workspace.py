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
    "configs/model", "configs/train", "configs/data",
    "scripts/__init__.py",
    "scripts/train/__init__.py",
    "scripts/train/pilot.py",
    "scripts/train/expansion_pilot.py",
    "scripts/train/gradient_conflict.py",
    "scripts/train/build_gradient_conflict_config.py",
    "scripts/train/build_lane_stratified_probe.py",
    "scripts/train/prepare_expansion.py",
    "scripts/train/qwen_runtime.py",
    "scripts/train/response_only.py",
    "scripts/train/run_sft.py",
    "scripts/train/preflight_gate3_capability_pilot.py",
    "scripts/train/build_gate3_capability_card.py",
    "scripts/train/build_gate3_gcloud_provider_evidence.py",
    "scripts/train/cuda_host_floor.py",
    "scripts/train/measure_gate3_capability_throughput.py",
    "scripts/train/verify_expansion_pilot.py",
    "data/seed", "manifests/datasets", "schemas/train",
    "artifacts/train/seed-pilot/prepared-train.jsonl",
    "artifacts/train/seed-pilot/prepared-validation.jsonl",
    "artifacts/train/seed-pilot/prepared-dataset-manifest.json",
    "artifacts/train/seed-pilot-v2/prepared-train.jsonl",
    "artifacts/train/seed-pilot-v2/prepared-validation.jsonl",
    "artifacts/train/seed-pilot-v2/prepared-dataset-manifest.json",
    "artifacts/train/expansion-pilot-v1/prepared-train.jsonl",
    "artifacts/train/expansion-pilot-v1/prepared-validation.jsonl",
    "artifacts/train/expansion-pilot-v1/prepared-dataset-manifest.json",
    "artifacts/train/expansion-pilot-v1/local-execution-card.json",
    "artifacts/train/expansion-capacity-probe-v2/local-execution-card.json",
    "artifacts/train/expansion-lane-stratified-probe-v3/prepared-train.jsonl",
    "artifacts/train/expansion-lane-stratified-probe-v3/prepared-retention.jsonl",
    "artifacts/train/expansion-lane-stratified-probe-v3/prepared-dataset-manifest.json",
    "artifacts/train/expansion-lane-stratified-probe-v3/local-execution-card.json",
    "artifacts/train/gradient-conflict-probe-v4/local-execution-card.json",
    "artifacts/train/gate3-capability-pilot-v2/prepared-train.jsonl",
    "artifacts/train/gate3-capability-pilot-v2/prepared-manifest.json",
    "measurement/gate3/capability-scale-v1/token-length-replacement-v1/final-package/data-package-seal.json",
    "measurement/data/expansion-v1/PILOT_SUFFICIENCY_AND_THROUGHPUT_20260909.json",
)
FORBIDDEN_PARTS = {"eval", "measurement", "outputs", ".git", ".gcloud-staging", "__pycache__"}
SAFE_MEASUREMENTS = {
    Path("measurement/data/expansion-v1/PILOT_SUFFICIENCY_AND_THROUGHPUT_20260909.json"),
    Path("measurement/gate3/capability-scale-v1/token-length-replacement-v1/final-package/data-package-seal.json"),
}


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
        if FORBIDDEN_PARTS & set(relative.parts) and relative not in SAFE_MEASUREMENTS: continue
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
    try:
        archive_label = str(archive.relative_to(root))
    except ValueError:
        archive_label = str(archive)
    manifest={"schema_version":"ganesh-mini-training-workspace/v1","status":"sealed","archive_path":archive_label,"archive_size":archive.stat().st_size,"archive_sha256":sha256(archive),"forbidden_roots":sorted(FORBIDDEN_PARTS),"files":entries}
    payload=json.dumps(manifest,sort_keys=True,separators=(",", ":")).encode(); manifest["manifest_sha256"]=hashlib.sha256(payload).hexdigest()
    manifest_path.parent.mkdir(parents=True,exist_ok=True); manifest_path.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    return manifest


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[2]); parser.add_argument("--archive",type=Path,required=True); parser.add_argument("--manifest",type=Path,required=True); args=parser.parse_args(); build(args.root.resolve(),args.archive.resolve(),args.manifest.resolve()); return 0


if __name__=="__main__": raise SystemExit(main())
