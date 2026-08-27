#!/usr/bin/env python3
"""Seal locally recovered Gate 3 inputs after the original GCS bucket disappeared."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tarfile
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = ROOT / "artifacts/gcloud-inputs/gate3"
OUTPUT = ROOT / "measurement/gate3/gcloud/rehydrated_inputs.json"
QUALIFIED_PLAN = ROOT / "measurement/cuda/gcloud/20260824T180957Z/gpu_run_plan.json"
MODEL_INVENTORY = ROOT / "configs/model/qwen3_5_2b.inventory.json"

HISTORICAL_BUNDLE_FILES = {
    "base-dpkg-packages.tsv": "2ee55f0e063a4018c1135041b900280958d3f791006c098bc371137e576de88b",
    "debs/containerd_2.2.1-0ubuntu1~22.04.2_amd64.deb": "08e309f0fb8ae6f798dc80e54f10e152c8dad6ee16ca6627805382fbb56cb5f1",
    "debs/docker.io_29.1.3-0ubuntu3~22.04.2_amd64.deb": "e2336d2596d18d6e1ae0cb80ae569a86019674b1b995c40a0c734be8081f275e",
    "debs/lock": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "debs/runc_1.3.4-0ubuntu1~22.04.1_amd64.deb": "1551d41d027969e141805f9687adcba746c332fa64e3c7ceb9261f842a33ff31",
}


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def identity(path: Path) -> dict[str, Any]:
    return {"path": str(path.relative_to(ROOT)), "size_bytes": path.stat().st_size, "sha256": sha256(path)}


def verify_model() -> dict[str, Any]:
    inventory = json.loads(MODEL_INVENTORY.read_text(encoding="utf-8"))
    model_root = ROOT / "models/qwen3.5-2b-15852e8"
    rows = []
    expected_paths = {row["path"] for row in inventory["files"]}
    actual_paths = {str(path.relative_to(model_root)) for path in model_root.iterdir() if path.is_file()}
    if actual_paths != expected_paths:
        raise ValueError("local model file set differs from the pinned upstream inventory")
    for expected in inventory["files"]:
        path = model_root / expected["path"]
        observed = {"path": expected["path"], "size_bytes": path.stat().st_size, "sha256": sha256(path)}
        if observed["size_bytes"] != expected["size"]:
            raise ValueError(f"model size mismatch: {expected['path']}")
        if expected.get("sha256") and observed["sha256"] != expected["sha256"]:
            raise ValueError(f"model hash mismatch: {expected['path']}")
        rows.append(observed)
    return {
        "revision": inventory["revision"],
        "file_count": len(rows),
        "total_bytes": sum(row["size_bytes"] for row in rows),
        "file_collection_sha256": canonical_sha256(rows),
    }


def verify_bundle(archive: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="ganesh-gate3-bundle-") as temp:
        root = Path(temp)
        with tarfile.open(archive, "r:gz") as bundle:
            for member in bundle.getmembers():
                target = (root / member.name).resolve()
                if root.resolve() not in target.parents and target != root.resolve():
                    raise ValueError("unsafe Docker bundle member")
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                elif member.isfile():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    source = bundle.extractfile(member)
                    if source is None:
                        raise ValueError("unreadable Docker bundle member")
                    with target.open("wb") as output:
                        for chunk in iter(lambda: source.read(1024 * 1024), b""):
                            output.write(chunk)
                else:
                    raise ValueError("unsupported Docker bundle member type")
        content = root / "docker-bundle"
        for relative, expected in HISTORICAL_BUNDLE_FILES.items():
            if sha256(content / relative) != expected:
                raise ValueError(f"rehydrated Docker bundle differs from historical content: {relative}")
    return {
        "historical_content": HISTORICAL_BUNDLE_FILES,
        "historical_content_collection_sha256": canonical_sha256(HISTORICAL_BUNDLE_FILES),
    }


def build() -> dict[str, Any]:
    plan = json.loads(QUALIFIED_PLAN.read_text(encoding="utf-8"))
    claimed = plan.pop("plan_sha256")
    if claimed != canonical_sha256(plan):
        raise ValueError("qualified Gate 0B plan seal is invalid")
    plan["plan_sha256"] = claimed
    expected_image_id = plan["input"]["cuda_image_id"]
    observed_image_id = subprocess.run(
        ["docker", "image", "inspect", "--format", "{{.Id}}", plan["input"]["cuda_image_ref"]],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if observed_image_id != expected_image_id:
        raise ValueError("local CUDA image is not the Gate 0B-qualified image")
    artifacts = {
        "model_archive": identity(ARTIFACT_DIR / "model.tar.gz"),
        "cuda_image_archive": identity(ARTIFACT_DIR / "cuda-image.docker.tar.zst"),
        "docker_bundle": identity(ARTIFACT_DIR / "docker-bundle.tar.gz"),
    }
    record: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate3-rehydrated-inputs/v1",
        "status": "verified-local-rehydration",
        "reason": "the original immutable transfer bucket was absent before resource creation",
        "qualified_gate0b_plan_sha256": claimed,
        "qualified_cuda_image": {"ref": plan["input"]["cuda_image_ref"], "image_id": observed_image_id},
        "model": verify_model(),
        "docker_bundle": verify_bundle(ARTIFACT_DIR / "docker-bundle.tar.gz"),
        "artifacts": artifacts,
        "required_runtime_rechecks": [
            "download each archive by immutable GCS generation and verify size and SHA-256",
            "load CUDA archive and require the qualified image ID",
            "extract model and require the pinned local model inventory",
            "verify every offline Docker package against its historical SHA-256",
        ],
    }
    record["evidence_sha256"] = canonical_sha256(record)
    return record


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(build(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
