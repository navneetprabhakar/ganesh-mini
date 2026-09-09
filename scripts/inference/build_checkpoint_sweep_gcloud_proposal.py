#!/usr/bin/env python3
"""Build a sealed, non-executable GCloud proposal for the Gate 4 checkpoint sweep."""

from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal
from pathlib import Path
from typing import Any


COMPUTE_HOURLY_USD = Decimal("0.853624312")
DISK_GIB = 200
DISK_GIB_HOURLY_USD = Decimal("0.000136986")
MAXIMUM_SECONDS = 7200
ABSOLUTE_CEILING_USD = Decimal("2.25")
RECOVERY_GENERATION = "1788935240864459"
RECOVERY_SHA256 = "24abdb78753ad59a25adbc3ca1ddab31da0176c3de935b02b874e5638dab8e31"
RECOVERY_SIZE = 51674173
INPUT_KEYS = {
    "workspace_archive", "workspace_manifest", "recovery_archive", "model_archive",
    "cuda_image_archive", "docker_bundle", "verifier_archive", "verifier_manifest",
    "controller", "metadata_wrapper",
}


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


def load_bindings(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop("bindings_sha256", None)
    if claimed != canonical_sha256(value):
        raise ValueError("checkpoint-sweep input bindings seal mismatch")
    value["bindings_sha256"] = claimed
    return value


def require_generation_row(name: str, row: Any) -> dict[str, Any]:
    if not isinstance(row, dict) or set(row) != {"uri", "sha256", "size_bytes"}:
        raise ValueError(f"{name} must contain only uri, sha256, and size_bytes")
    uri = row["uri"]
    if not isinstance(uri, str) or not uri.startswith("gs://") or not uri.rsplit("#", 1)[-1].isdigit():
        raise ValueError(f"{name} URI is not generation-pinned")
    if not isinstance(row["sha256"], str) or len(row["sha256"]) != 64:
        raise ValueError(f"{name} SHA-256 is invalid")
    if not isinstance(row["size_bytes"], int) or row["size_bytes"] <= 0:
        raise ValueError(f"{name} size is invalid")
    return row


def build(bindings: dict[str, Any]) -> dict[str, Any]:
    unsigned = {key: value for key, value in bindings.items() if key != "bindings_sha256"}
    if bindings.get("bindings_sha256") != canonical_sha256(unsigned):
        raise ValueError("checkpoint-sweep input bindings seal mismatch")
    if bindings.get("schema_version") != "ganesh-mini-checkpoint-sweep-gcloud-bindings/v1":
        raise ValueError("unsupported checkpoint-sweep bindings")
    inputs = bindings.get("inputs")
    if not isinstance(inputs, dict) or set(inputs) != INPUT_KEYS:
        raise ValueError("checkpoint-sweep bindings have the wrong input set")
    checked = {key: require_generation_row(key, value) for key, value in inputs.items()}
    recovery = checked["recovery_archive"]
    if (
        recovery["uri"].rsplit("#", 1)[-1] != RECOVERY_GENERATION
        or recovery["sha256"] != RECOVERY_SHA256
        or recovery["size_bytes"] != RECOVERY_SIZE
    ):
        raise ValueError("recovery archive is not the verified Gate 4 terminal generation")

    hours = Decimal(MAXIMUM_SECONDS) / Decimal(3600)
    compute_upper = COMPUTE_HOURLY_USD * hours
    disk_upper = DISK_GIB_HOURLY_USD * DISK_GIB * hours
    provider_upper = compute_upper + disk_upper
    if provider_upper >= ABSOLUTE_CEILING_USD:
        raise ValueError("checkpoint-sweep provider upper bound does not fit the ceiling")
    proposal: dict[str, Any] = {
        "schema_version": "ganesh-mini-checkpoint-sweep-gcloud-proposal/v1",
        "status": "pending-explicit-execution-approval",
        "purpose": "evaluation-only diagnostic sweep of five saved Gate 4 checkpoints",
        "promotion_authority": "none",
        "training_allowed": False,
        "decision_surface_allowed": False,
        "bindings_sha256": bindings["bindings_sha256"],
        "resource": {
            "project": bindings["project"], "region": "us-east1", "zone": "us-east1-c",
            "machine_type": "g2-standard-8", "accelerator": "1x NVIDIA L4",
            "provisioning_model": "STANDARD", "boot_disk_gib": DISK_GIB,
            "boot_disk_type": "pd-balanced", "boot_disk_auto_delete": True,
            "external_ip": False, "automatic_restart": False,
            "maximum_vm_lifetime_seconds": MAXIMUM_SECONDS,
        },
        "cost": {
            "compute_hourly_usd": str(COMPUTE_HOURLY_USD),
            "pd_balanced_gib_hourly_usd": str(DISK_GIB_HOURLY_USD),
            "compute_upper_usd": str(compute_upper),
            "boot_disk_upper_usd": str(disk_upper),
            "provider_upper_usd": str(provider_upper),
            "absolute_cost_ceiling_usd": str(ABSOLUTE_CEILING_USD),
        },
        "runtime": {
            "controller_budget_seconds": 6000, "terminal_backup_reserve_seconds": 1200,
            "checkpoint_interval_seconds": 120, "docker_network": "none",
            "expected_checkpoint_evaluations": 5, "tasks_per_checkpoint": 30,
            "guest_shutdown_after_terminal_backup": True,
        },
        "inputs": checked,
        "hard_stops": [
            "no GCloud action before explicit approval of this exact sealed proposal",
            "no training, full-development evaluation, decision-task opening, promotion, or publication",
            "no provider creation unless exact resource absence, price, quota, IAM, and bucket roundtrip pass",
            "terminal GCS backup must complete before guest shutdown",
        ],
    }
    proposal["proposal_sha256"] = canonical_sha256(proposal)
    return proposal


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bindings", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    proposal = build(load_bindings(args.bindings))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(proposal, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
