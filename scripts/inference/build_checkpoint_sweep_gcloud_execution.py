#!/usr/bin/env python3
"""Bind an approved checkpoint-sweep proposal to one executable attempt."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from scripts.inference.build_checkpoint_sweep_gcloud_proposal import canonical_sha256


CUDA_IMAGE = {
    "ref": "ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1-liger082",
    "image_id": "sha256:cdaf068ffcb933120181168ebf6ae1546ddf81e01b2ad006a1a18dd2e43d9860",
}


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop(field, None)
    if claimed != canonical_sha256(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def build(proposal: dict[str, Any], approval: dict[str, Any], attempt_id: str, source_commit: str) -> dict[str, Any]:
    if not re.fullmatch(r"[0-9]{8}T[0-9]{6}Z", attempt_id):
        raise ValueError("invalid attempt ID")
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("source commit must be a full Git SHA")
    proposal_sha = proposal.get("proposal_sha256")
    if (
        proposal.get("status") != "pending-explicit-execution-approval"
        or proposal.get("promotion_authority") != "none"
        or proposal.get("training_allowed") is not False
        or proposal.get("decision_surface_allowed") is not False
        or proposal.get("resource", {}).get("maximum_vm_lifetime_seconds") != 7200
        or proposal.get("cost", {}).get("absolute_cost_ceiling_usd") != "2.25"
    ):
        raise ValueError("proposal escaped the approved diagnostic boundary")
    if (
        approval.get("status") != "approved"
        or approval.get("approved_proposal_sha256") != proposal_sha
        or approval.get("absolute_incremental_ceiling_usd") != "2.25"
    ):
        raise ValueError("approval does not bind the exact proposal")
    resource = proposal["resource"]
    card: dict[str, Any] = {
        "schema_version": "ganesh-mini-checkpoint-sweep-gcloud-execution/v1",
        "status": "authorized-executable",
        "source_commit": source_commit,
        "approval": {
            "proposal_sha256": proposal_sha,
            "approval_sha256": approval["approval_sha256"],
        },
        "promotion_authority": "none",
        "training_allowed": False,
        "decision_surface_allowed": False,
        "cuda_image": CUDA_IMAGE,
        "cost": proposal["cost"],
        "inputs": proposal["inputs"],
        "execution": {
            "project": resource["project"],
            "zone": resource["zone"],
            "machine_type": resource["machine_type"],
            "provisioning_model": resource["provisioning_model"],
            "gcs_bucket": "ganesh-gate0-model-transfer-1061994342941",
            "gcs_prefix": f"ganesh-mini-1.0/evaluation/checkpoint-sweep-v1/attempts/{attempt_id}",
            "attempt_id": attempt_id,
            "maximum_vm_lifetime_seconds": 7200,
            "controller_budget_seconds": 6000,
            "backup_reserve_seconds": 1200,
            "automatic_restart": False,
            "external_ip": False,
            "boot_disk_auto_delete": True,
        },
    }
    card["execution_sha256"] = canonical_sha256(card)
    return card


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proposal", type=Path, required=True)
    parser.add_argument("--approval", type=Path, required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    card = build(
        load_sealed(args.proposal, "proposal_sha256"),
        load_sealed(args.approval, "approval_sha256"),
        args.attempt_id,
        args.source_commit,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(card, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": card["status"], "execution_sha256": card["execution_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
