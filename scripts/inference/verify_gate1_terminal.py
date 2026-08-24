#!/usr/bin/env python3
"""Validate the downloaded Gate 1 terminal backup before VM deletion."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.inference.run_development_baseline_host import (
    canonical_sha256,
    load_sealed,
    validate_completed_run,
)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_inventory(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split(None, 1)
        relative = relative.lstrip("*").removeprefix("./")
        if len(digest) != 64 or relative in rows or not relative:
            raise ValueError("runtime inventory contains an invalid or duplicate row")
        rows[relative] = digest
    if not rows:
        raise ValueError("runtime inventory is empty")
    return rows


def verify(
    backup_manifest_path: Path,
    download_root: Path,
    execution_card_path: Path,
    expected_prefix: str,
) -> dict[str, Any]:
    manifest = load_sealed(backup_manifest_path, "evidence_sha256")
    card = load_sealed(execution_card_path, "execution_sha256")
    if manifest.get("status") != "verified" or manifest.get("prefix") != expected_prefix:
        raise ValueError("terminal backup manifest status or prefix mismatch")
    if card.get("schema_version") != "ganesh-mini-gate1-gcloud-execution/v1" or card.get("status") != "authorized-executable":
        raise ValueError("execution card contract mismatch")
    objects = manifest.get("objects", [])
    if not objects or not all(row.get("verified") is True for row in objects):
        raise ValueError("terminal backup contains unverified objects")
    object_rows = {
        row["object_uri"].removeprefix(expected_prefix.rstrip("/") + "/"): row
        for row in objects
        if row["object_uri"].startswith(expected_prefix.rstrip("/") + "/")
    }
    if len(object_rows) != len(objects):
        raise ValueError("terminal backup contains duplicate or out-of-prefix objects")
    inventory_path = download_root / "runtime-files.sha256"
    inventory = parse_inventory(inventory_path)
    inventory_row = object_rows.get("runtime-files.sha256")
    if inventory_row is None or inventory_row.get("downloaded_sha256") != file_sha256(inventory_path):
        raise ValueError("terminal inventory object is missing or mismatched")
    for relative, digest in inventory.items():
        path = download_root / relative
        if not path.is_file() or file_sha256(path) != digest:
            raise ValueError(f"downloaded terminal artifact mismatch: {relative}")
        row = object_rows.get(relative)
        if row is None or row.get("downloaded_sha256") != digest:
            raise ValueError(f"GCS terminal artifact mismatch: {relative}")

    startup_code = int((download_root / "startup-exit-code.txt").read_text().strip())
    controller_code_path = download_root / "controller-exit-code.txt"
    controller_code = int(controller_code_path.read_text().strip()) if controller_code_path.is_file() else None
    successful = startup_code == controller_code == 0
    run_summary: dict[str, Any] | None = None
    if successful:
        run = validate_completed_run(download_root / "output/run.json")
        host = load_sealed(download_root / "output/host-execution.json", "evidence_sha256")
        execution = card["execution"]
        if (
            host.get("status") != "passed"
            or host.get("attempt_id") != execution["attempt_id"]
            or host.get("run", {}).get("run_sha256") != run["run_sha256"]
            or host.get("run", {}).get("task_accounting") != run["task_accounting"]
        ):
            raise ValueError("host execution does not bind the completed baseline run")
        run_summary = {
            "run_sha256": run["run_sha256"],
            "host_execution_sha256": host["evidence_sha256"],
            "task_accounting": run["task_accounting"],
        }
    else:
        diagnostics = [download_root / "controller.stderr.log", download_root / "startup.stderr.log"]
        if startup_code == 0 and controller_code is None:
            raise ValueError("controller exit code is missing from an otherwise successful startup")
        if not any(path.is_file() and path.stat().st_size > 0 for path in diagnostics):
            raise ValueError("failed baseline is missing startup/controller diagnostics")

    evidence: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate1-terminal-validation/v1",
        "status": "passed" if successful else "sealed-failure",
        "attempt_id": card["execution"]["attempt_id"],
        "expected_prefix": expected_prefix,
        "execution_sha256": card["execution_sha256"],
        "backup_manifest_sha256": manifest["evidence_sha256"],
        "runtime_inventory_sha256": file_sha256(inventory_path),
        "runtime_inventory_entries": len(inventory),
        "terminal_object_count": len(objects),
        "startup_exit_code": startup_code,
        "controller_exit_code": controller_code,
        "run": run_summary,
        "deletion_eligible": True,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backup-manifest", type=Path, required=True)
    parser.add_argument("--download-root", type=Path, required=True)
    parser.add_argument("--execution-card", type=Path, required=True)
    parser.add_argument("--expected-prefix", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    evidence = verify(
        args.backup_manifest,
        args.download_root,
        args.execution_card,
        args.expected_prefix,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if evidence["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
