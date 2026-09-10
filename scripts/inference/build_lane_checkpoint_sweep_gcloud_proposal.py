#!/usr/bin/env python3
"""Build the sealed diagnostic-only VM proposal for the v3 checkpoint sweep."""

from __future__ import annotations

import argparse
import json
from decimal import Decimal
from pathlib import Path
from typing import Any

from scripts.inference.build_lane_checkpoint_sweep_upload_plan import canonical_sha256
from scripts.inference.build_lane_checkpoint_sweep_upload_receipt import load_sealed


MAXIMUM_SECONDS = 7200
DISK_GIB = 200
ABSOLUTE_CEILING_USD = Decimal("2.25")
INPUT_MAP = {
    "uploaded_workspace.tar.gz": "workspace_archive",
    "uploaded_workspace.manifest.json": "workspace_manifest",
    "uploaded_recovery.tar.gz": "recovery_archive",
    "uploaded_startup.sh": "controller",
    "model_archive": "model_archive",
    "cuda_image_archive": "cuda_image_archive",
    "docker_bundle": "docker_bundle",
    "verifier_archive": "verifier_archive",
    "verifier_manifest": "verifier_manifest",
    "metadata_wrapper": "metadata_wrapper",
}


def build(report: dict[str, Any]) -> dict[str, Any]:
    unsigned = {key: value for key, value in report.items() if key != "report_sha256"}
    if report.get("report_sha256") != canonical_sha256(unsigned):
        raise ValueError("inspection report seal mismatch")
    if (
        report.get("status") != "complete-ready-for-separate-proposal"
        or report.get("conclusion", {}).get("prerequisites_passed") is not True
        or report.get("conclusion", {}).get("execution_authorized") is not False
    ):
        raise ValueError("inspection did not pass the proposal boundary")
    inputs = {target: report["inputs"][source] for source, target in INPUT_MAP.items()}
    if len(inputs) != len(INPUT_MAP) or any(not row["uri"].rsplit("#", 1)[-1].isdigit() for row in inputs.values()):
        raise ValueError("proposal inputs are not exact-generation bound")
    compute_hourly = Decimal(report["pricing"]["compute_hourly_usd"])
    disk_hourly = Decimal(report["pricing"]["pd_balanced_gib_hourly_usd"])
    hours = Decimal(MAXIMUM_SECONDS) / Decimal(3600)
    compute_upper = compute_hourly * hours
    disk_upper = disk_hourly * DISK_GIB * hours
    provider_upper = compute_upper + disk_upper
    if provider_upper >= ABSOLUTE_CEILING_USD:
        raise ValueError("provider upper bound does not fit the absolute ceiling")
    proposal: dict[str, Any] = {
        "schema_version": "ganesh-mini-lane-checkpoint-sweep-gcloud-proposal/v1",
        "status": "pending-explicit-execution-approval",
        "purpose": "diagnostic-only serial evaluation of five earlier v3 checkpoints on the frozen 30-task development screen",
        "promotion_authority": "none",
        "checkpoint_selection_authority": "none",
        "training_allowed": False,
        "full_development_allowed": False,
        "decision_surface_allowed": False,
        "inspection_report_sha256": report["report_sha256"],
        "resource": {
            "project": report["provider"]["project"],
            "region": report["provider"]["region"],
            "zone": report["provider"]["zone"],
            "resource_names": report["planned_resource_names"],
            "machine_type": "g2-standard-8",
            "accelerator": "1x NVIDIA L4",
            "provisioning_model": "STANDARD",
            "boot_disk_gib": DISK_GIB,
            "boot_disk_type": "pd-balanced",
            "boot_disk_auto_delete": True,
            "external_ip": False,
            "automatic_restart": False,
            "maximum_vm_lifetime_seconds": MAXIMUM_SECONDS,
        },
        "cost": {
            "compute_hourly_usd": str(compute_hourly),
            "pd_balanced_gib_hourly_usd": str(disk_hourly),
            "compute_upper_usd": str(compute_upper),
            "boot_disk_upper_usd": str(disk_upper),
            "provider_upper_usd": str(provider_upper),
            "absolute_cost_ceiling_usd": str(ABSOLUTE_CEILING_USD),
        },
        "runtime": {
            "controller_budget_seconds": 6000,
            "terminal_backup_reserve_seconds": 1200,
            "checkpoint_interval_seconds": 120,
            "docker_network": "none",
            "expected_checkpoint_evaluations": 5,
            "tasks_per_checkpoint": 30,
            "guest_shutdown_after_terminal_backup": True,
        },
        "inputs": inputs,
        "hard_stops": [
            "no GCloud mutation or compute before explicit approval of this exact sealed proposal and $2.25 ceiling",
            "no training, checkpoint selection, full-development evaluation, decision-task opening, promotion, or publication",
            "no provider creation unless exact resource absence, quota, IAM, price, and all input bindings remain valid",
            "terminal and checkpoint GCS backup plus independent recovery must complete before teardown",
            "delete the exact VM, auto-delete disk, subnet, and network after preservation, then verify absence twice",
        ],
    }
    proposal["proposal_sha256"] = canonical_sha256(proposal)
    return proposal


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    proposal = build(load_sealed(args.report, "report_sha256"))
    args.output.write_text(json.dumps(proposal, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "absolute_cost_ceiling_usd": proposal["cost"]["absolute_cost_ceiling_usd"],
        "proposal_sha256": proposal["proposal_sha256"],
        "provider_upper_usd": proposal["cost"]["provider_upper_usd"],
        "status": proposal["status"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
