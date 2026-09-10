#!/usr/bin/env python3
"""Bind an approved lane-probe proposal to its outer execution card."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


PROPOSAL_SHA = "8184f4694efdfab2da3b895393caec4c753d6b782f8c810067824f5d957926fa"


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop(field, None)
    if claimed != canonical_sha256(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(proposal: dict[str, Any], approval: dict[str, Any], training_card_path: Path, training_card_uri: str) -> dict[str, Any]:
    if proposal.get("proposal_sha256") != PROPOSAL_SHA or proposal.get("status") != "pending-explicit-execution-approval" or proposal["cost"]["absolute_cost_ceiling_usd"] != "2.25":
        raise ValueError("proposal escaped the approved boundary")
    if approval.get("status") != "approved" or approval.get("approved_proposal_sha256") != PROPOSAL_SHA or approval.get("absolute_incremental_ceiling_usd") != "2.25":
        raise ValueError("approval does not bind exact proposal and ceiling")
    training = load_sealed(training_card_path, "card_sha256")
    provider = training.get("provider_execution") or {}
    if training.get("schema_version") != "ganesh-mini-expansion-pilot-card/v3" or training.get("status") != "ready" or provider.get("cost_ceiling_usd") != 2.25:
        raise ValueError("training card is not provider-bound to approved v3 ceiling")
    if not training_card_uri.startswith("gs://") or not training_card_uri.rsplit("#", 1)[-1].isdigit():
        raise ValueError("training card URI must be generation-pinned")

    input_map = {
        "eval_workspace_archive": "evaluation_workspace_archive",
        "eval_workspace_manifest": "evaluation_workspace_manifest",
        "train_workspace_archive": "train_workspace_archive",
        "train_workspace_manifest": "train_workspace_manifest",
        "model_archive": "model_archive",
        "cuda_image_archive": "cuda_image_archive",
        "docker_bundle": "docker_bundle",
        "verifier_archive": "verifier_archive",
        "verifier_manifest": "verifier_manifest",
    }
    inputs = {target: proposal["inputs"][source] for target, source in input_map.items()}
    inputs["training_execution_card"] = {"uri": training_card_uri, "sha256": file_sha256(training_card_path), "size_bytes": training_card_path.stat().st_size}
    resource, cost, runtime = proposal["resource"], proposal["cost"], proposal["runtime"]
    card: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate4-gcloud-execution/v1",
        "status": "authorized-executable",
        "source_commit": proposal["source_commit"],
        "approval": {
            "proposal_sha256": PROPOSAL_SHA,
            "approval_sha256": approval["approval_sha256"],
            "approval_evidence_sha256": provider["approval_evidence_sha256"],
        },
        "cuda_image": {"ref": "ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1-liger082", "image_id": "sha256:cdaf068ffcb933120181168ebf6ae1546ddf81e01b2ad006a1a18dd2e43d9860"},
        "cost": {
            "compute_hourly_usd": float(cost["compute_hourly_usd"]),
            "boot_disk_upper_usd": float(cost["boot_disk_upper_usd"]),
            "support_reserve_usd": float(cost["support_reserve_usd"]),
            "absolute_cost_ceiling_usd": float(cost["absolute_cost_ceiling_usd"]),
        },
        "inputs": inputs,
        "execution": {
            "project": resource["project"], "zone": resource["zone"],
            "machine_type": resource["machine_type"], "provisioning_model": resource["provisioning_model"],
            "gcs_bucket": "ganesh-gate0-model-transfer-1061994342941",
            "gcs_prefix": "ganesh-mini-1.0/training/lane-stratified-probe-v3/attempts/20260910T043000Z",
            "attempt_id": "20260910T043000Z",
            "maximum_vm_lifetime_seconds": resource["maximum_vm_lifetime_seconds"],
            "controller_budget_seconds": runtime["controller_budget_seconds"],
            "backup_reserve_seconds": runtime["terminal_backup_reserve_seconds"],
            "automatic_restart": False, "external_ip": False, "boot_disk_auto_delete": True,
        },
    }
    card["execution_sha256"] = canonical_sha256(card)
    return card


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proposal", type=Path, required=True)
    parser.add_argument("--approval", type=Path, required=True)
    parser.add_argument("--training-card", type=Path, required=True)
    parser.add_argument("--training-card-uri", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    card = build(load_sealed(args.proposal, "proposal_sha256"), load_sealed(args.approval, "approval_sha256"), args.training_card, args.training_card_uri)
    args.output.write_text(json.dumps(card, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": card["status"], "execution_sha256": card["execution_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
