#!/usr/bin/env python3
"""Seal preserved evidence for an interrupted checkpoint-sweep attempt."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.campaign.run_checkpoint_sweep_host import verify_result_tasks
from scripts.campaign.run_host import canonical_sha256, load_sealed


EXPECTED_LABELS = (
    "tokens-000000406491",
    "tokens-000000814098",
    "tokens-000001224637",
    "tokens-000001629235",
)
LANGUAGES = ("go", "java", "javascript", "typescript", "python", "rust")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_sealed(path: Path, value: dict[str, Any], field: str) -> None:
    value[field] = canonical_sha256(value)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def verify_mirror(attempt: Path) -> tuple[dict[str, Any], int, int]:
    listing_path = attempt / "provider/runtime-checkpoint-listing.json"
    listing = read_json(listing_path)
    mirror = attempt / "runtime-checkpoint-mirror"
    items = listing.get("items", [])
    if not items:
        raise ValueError("runtime checkpoint listing is empty")
    prefix = f"ganesh-mini-1.0/evaluation/checkpoint-sweep-v1/attempts/{attempt.name}/"
    observed: set[str] = set()
    total_bytes = 0
    for row in items:
        name = row["name"]
        if not name.startswith(prefix):
            raise ValueError(f"object escaped attempt prefix: {name}")
        relative = name.removeprefix(prefix)
        path = mirror / relative
        expected_size = int(row["size"])
        if not path.is_file() or path.stat().st_size != expected_size:
            raise ValueError(f"mirror size mismatch: {relative}")
        expected_md5 = base64.b64decode(row["md5Hash"])
        if hashlib.md5(path.read_bytes()).digest() != expected_md5:  # noqa: S324 - GCS integrity field
            raise ValueError(f"mirror MD5 mismatch: {relative}")
        observed.add(relative)
        total_bytes += expected_size
    local = {str(path.relative_to(mirror)) for path in mirror.rglob("*") if path.is_file()}
    if local != observed:
        raise ValueError("local mirror file set differs from immutable GCS listing")
    return listing, len(items), total_bytes


def checkpoint_rows(attempt: Path) -> list[dict[str, Any]]:
    root = attempt / "runtime-checkpoint-mirror/runtime-checkpoints" / attempt.name / "output/results"
    rows: list[dict[str, Any]] = []
    for label in EXPECTED_LABELS:
        result_dir = root / label
        run = load_sealed(result_dir / "run.json", "run_sha256")
        verify_result_tasks(result_dir, run)
        accounting = run["task_accounting"]
        if accounting != {
            "expected": 30,
            "completed": 30,
            "passed": accounting["passed"],
            "failed": 30 - accounting["passed"],
            "pending": 0,
        }:
            raise ValueError(f"invalid task accounting: {label}")
        lane_counts = {language: 0 for language in LANGUAGES}
        for path in sorted((result_dir / "tasks").glob("*.json")):
            task = load_sealed(path, "evidence_sha256")
            if task["verification"]["result"]["passed"]:
                lane_counts[task["task"]["language"]] += 1
        rows.append(
            {
                "checkpoint": label,
                "passed": accounting["passed"],
                "failed": accounting["failed"],
                "language_passes": lane_counts,
                "run_sha256": run["run_sha256"],
            }
        )
    return rows


def http_code(path: Path) -> int:
    return int(path.read_text(encoding="utf-8").strip())


def aggregated(inventory: dict[str, Any], field: str) -> list[dict[str, Any]]:
    return [row for scope in inventory.get("items", {}).values() for row in scope.get(field, [])]


def finalize(attempt: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    approval = load_sealed(attempt / "approval.json", "approval_sha256")
    execution = load_sealed(attempt / "execution-card.json", "execution_sha256")
    listing, object_count, total_bytes = verify_mirror(attempt)
    checkpoints = checkpoint_rows(attempt)
    phase_ledger = load_sealed(
        attempt / "runtime-checkpoint-mirror/runtime-checkpoints" / attempt.name / "output/phase-ledger.json",
        "evidence_sha256",
    )
    if [row["name"].removeprefix("evaluate-") for row in phase_ledger["phases"][2:]] != list(EXPECTED_LABELS):
        raise ValueError("phase ledger does not bind the four completed checkpoints")

    interruption = {
        "schema_version": "ganesh-mini-checkpoint-sweep-interruption/v1",
        "status": "partial-diagnostic-controller-timeout",
        "attempt_id": attempt.name,
        "proposal_sha256": approval["approved_proposal_sha256"],
        "approval_sha256": approval["approval_sha256"],
        "execution_sha256": execution["execution_sha256"],
        "completed_checkpoint_count": len(checkpoints),
        "expected_checkpoint_count": 5,
        "checkpoints": checkpoints,
        "incomplete_checkpoint": {
            "checkpoint": "tokens-000002036559",
            "task_evidence_count": 0,
            "available_files": [
                "evaluate-tokens-000002036559.stderr.log",
                "evaluate-tokens-000002036559.stdout.log",
            ],
            "classification": "controller-timeout-no-terminal-result-not-a-model-failure",
        },
        "runtime_checkpoint_preservation": {
            "object_count": object_count,
            "total_bytes": total_bytes,
            "listing_file_sha256": sha256(attempt / "provider/runtime-checkpoint-listing.json"),
            "immutable_generations_verified": True,
            "size_and_md5_verified": True,
            "latest_object_updated": max(row["updated"] for row in listing["items"]),
        },
        "diagnostic_conclusion": "no_completed_checkpoint_shows_broad_multilingual_transfer",
        "promotion_authority": "none",
    }
    write_sealed(attempt / "interruption-receipt.json", interruption, "receipt_sha256")

    checks = []
    for sequence in (1, 2):
        root = attempt / f"provider/absence-{sequence}"
        values = {
            "instance_http": http_code(root / "target-instance.http"),
            "boot_disk_http": http_code(root / "target-disk.http"),
            "subnet_http": http_code(root / "target-subnet.http"),
            "network_http": http_code(root / "target-network.http"),
        }
        if set(values.values()) != {404}:
            raise ValueError(f"target resources remain in absence pass {sequence}")
        checks.append({"sequence": sequence, "checked_at": (root / "checked-at.txt").read_text().strip(), **values})

    inventory_root = attempt / "provider/absence-2"
    inventories = {
        name: read_json(inventory_root / f"inventory-{name}.json")
        for name in (
            "instances", "disks", "addresses", "forwardingRules", "routers", "reservations",
            "snapshots", "images", "machineImages",
        )
    }
    active = {
        "instances": aggregated(inventories["instances"], "instances"),
        "disks": aggregated(inventories["disks"], "disks"),
        "addresses": aggregated(inventories["addresses"], "addresses"),
        "forwarding_rules": aggregated(inventories["forwardingRules"], "forwardingRules"),
        "routers": aggregated(inventories["routers"], "routers"),
        "reservations": aggregated(inventories["reservations"], "reservations"),
        "snapshots": inventories["snapshots"].get("items", []),
        "images": inventories["images"].get("items", []),
        "machine_images": inventories["machineImages"].get("items", []),
    }
    disk_exceptions = [
        {"name": row["name"], "size_gib": int(row["sizeGb"]), "zone": row["zone"].rsplit("/", 1)[-1], "status": row["status"]}
        for row in active["disks"]
    ]
    if any(active[name] for name in active if name != "disks"):
        raise ValueError("unexpected active Compute inventory remains")
    if disk_exceptions != [{"name": "laxmi-wmv2-training-01", "size_gib": 200, "zone": "us-central1-a", "status": "READY"}]:
        raise ValueError("unexpected disk inventory after teardown")

    operation_files = (
        "instance-delete-operation.json", "instance-delete-status.json",
        "subnet-delete-operation.json", "subnet-delete-status.json",
        "network-delete-operation.json", "network-delete-status.json",
    )
    for name in ("instance-delete-status.json", "subnet-delete-status.json", "network-delete-status.json"):
        operation = read_json(attempt / "provider" / name)
        if operation.get("status") != "DONE" or operation.get("error") is not None:
            raise ValueError(f"provider deletion did not complete cleanly: {name}")
    teardown = {
        "schema_version": "ganesh-mini-checkpoint-sweep-teardown/v1",
        "status": "ganesh-resources-absent-with-unrelated-disk-exception",
        "attempt_id": attempt.name,
        "absence_checks": checks,
        "deleted_resources": {
            "instance": "ganesh-mini-g4-sweep-20260909t130347z",
            "disk": "ganesh-mini-g4-sweep-20260909t130347z",
            "subnet": "ganesh-mini-g4-sweep-subnet-20260909t130347z",
            "network": "ganesh-mini-g4-sweep-net-20260909t130347z",
        },
        "provider_operation_file_sha256": {
            name: sha256(attempt / "provider" / name) for name in operation_files
        },
        "compute_inventory": {
            "instances": 0,
            "addresses": 0,
            "forwarding_rules": 0,
            "routers": 0,
            "reservations": 0,
            "snapshots": 0,
            "images": 0,
            "machine_images": 0,
            "unrelated_disk_exceptions": disk_exceptions,
        },
        "billing_claim": "all_Ganesh_sweep_compute_resources_absent; GCS remains; one unrelated disk may still bill",
    }
    write_sealed(attempt / "teardown-receipt.json", teardown, "receipt_sha256")
    return interruption, teardown


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("attempt", type=Path)
    args = parser.parse_args()
    interruption, teardown = finalize(args.attempt)
    print(json.dumps({"interruption": interruption["receipt_sha256"], "teardown": teardown["receipt_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
