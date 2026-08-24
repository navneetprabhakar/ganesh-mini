#!/usr/bin/env python3
"""Atomically admit a successfully finalized Gate 1 baseline into the repository."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT_HINT = Path(__file__).resolve().parents[2]
if str(ROOT_HINT) not in sys.path:
    sys.path.insert(0, str(ROOT_HINT))

from scripts.eval.build_gate1_readiness import build as build_readiness
from scripts.inference.run_development_baseline_host import (
    canonical_sha256,
    load_sealed,
    validate_completed_run,
)


CANONICAL_BASELINE = Path("measurement/inference/development/qwen3.5-2b-base-v1")
READINESS_PATH = Path("measurement/gate1/readiness.json")
ADMISSION_PATH = Path("measurement/gate1/baseline_admission.json")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def file_manifest(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): file_sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def require_final_backup(
    manifest_path: Path,
    finalization_path: Path,
    expected_prefix: str,
) -> dict[str, Any]:
    manifest = load_sealed(manifest_path, "evidence_sha256")
    if manifest.get("status") != "verified" or manifest.get("prefix") != expected_prefix:
        raise ValueError("final post-delete backup is not verified for the expected prefix")
    finalization_uri = expected_prefix.rstrip("/") + "/finalization.json"
    matches = [row for row in manifest.get("objects", []) if row.get("object_uri") == finalization_uri]
    if len(matches) != 1 or matches[0].get("verified") is not True:
        raise ValueError("final post-delete backup does not contain one verified finalization receipt")
    if matches[0].get("downloaded_sha256") != file_sha256(finalization_path):
        raise ValueError("backed finalization receipt does not match the local receipt")
    return manifest


def admit(finalization_dir: Path, root: Path = ROOT_HINT) -> dict[str, Any]:
    root = root.resolve()
    finalization_dir = finalization_dir.resolve(strict=True)
    finalization_path = finalization_dir / "finalization.json"
    validation_path = finalization_dir / "terminal-validation.json"
    final_backup_path = finalization_dir / "post-delete-final-backup-manifest.json"
    source = finalization_dir / "terminal-download" / "output" / "campaign" / "baseline"
    finalization = load_sealed(finalization_path, "evidence_sha256")
    validation = load_sealed(validation_path, "evidence_sha256")
    if finalization.get("schema_version") != "ganesh-mini-gate1-gcloud-finalization/v1" or finalization.get("status") != "complete":
        raise ValueError("Gate 1 teardown finalization is incomplete")
    if validation.get("schema_version") != "ganesh-mini-gate1-terminal-validation/v1" or validation.get("status") not in {"passed", "sealed-failure"} or not validation.get("run"):
        raise ValueError("only a terminal result with a validated Gate 1 baseline can be admitted")
    if finalization.get("execution_sha256") != validation.get("execution_sha256"):
        raise ValueError("finalization and terminal validation execution seals differ")
    if finalization.get("terminal_validation_sha256") != validation.get("evidence_sha256"):
        raise ValueError("finalization does not bind the terminal validation receipt")
    prefix = validation.get("expected_prefix")
    if not isinstance(prefix, str) or "/runtime-terminal-" not in prefix:
        raise ValueError("terminal validation prefix is invalid")
    base_prefix = prefix.split("/runtime-terminal-", 1)[0]
    final_backup = require_final_backup(final_backup_path, finalization_path, base_prefix + "/post-delete")

    if not source.is_dir():
        raise ValueError("downloaded terminal output directory is missing")
    run = validate_completed_run(source / "run.json")
    validation_run = validation.get("run") or {}
    if run.get("run_sha256") != validation_run.get("run_sha256"):
        raise ValueError("downloaded baseline does not match terminal validation")
    source_manifest = file_manifest(source)
    if not source_manifest or "run.json" not in source_manifest:
        raise ValueError("downloaded baseline output is empty or incomplete")

    target = root / CANONICAL_BASELINE
    if target.exists():
        raise FileExistsError(f"canonical baseline already exists: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = target.with_name(f".{target.name}.admission-{os.getpid()}")
    if staging.exists():
        raise FileExistsError(f"admission staging path already exists: {staging}")
    shutil.copytree(source, staging, copy_function=shutil.copy2)
    if file_manifest(staging) != source_manifest:
        raise ValueError("staged baseline copy differs from downloaded terminal output")
    os.replace(staging, target)

    readiness = build_readiness(root, target / "run.json")
    if readiness.get("status") != "ready" or readiness.get("failed_checks"):
        raise ValueError(f"admitted baseline did not open Gate 1: {readiness.get('failed_checks')}")
    atomic_json(root / READINESS_PATH, readiness)
    evidence: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate1-baseline-admission/v1",
        "status": "admitted",
        "attempt_id": validation["attempt_id"],
        "execution_sha256": validation["execution_sha256"],
        "terminal_validation_sha256": validation["evidence_sha256"],
        "finalization_sha256": finalization["evidence_sha256"],
        "post_delete_final_backup_sha256": final_backup["evidence_sha256"],
        "baseline_run_sha256": run["run_sha256"],
        "canonical_path": str(CANONICAL_BASELINE),
        "admitted_file_count": len(source_manifest),
        "admitted_files_sha256": canonical_sha256(source_manifest),
        "gate1_readiness_sha256": readiness["evidence_sha256"],
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    atomic_json(root / ADMISSION_PATH, evidence)
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--finalization-dir", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=ROOT_HINT)
    args = parser.parse_args()
    evidence = admit(args.finalization_dir, args.root)
    print(json.dumps(evidence, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
