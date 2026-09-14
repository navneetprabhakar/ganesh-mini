#!/usr/bin/env python3
"""Bind the approved gradient-conflict proposal to its executable cards."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
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


def validate_boundary(proposal: dict[str, Any], approval: dict[str, Any]) -> None:
    proposal_sha = proposal.get("proposal_sha256")
    if not isinstance(proposal_sha, str) or proposal.get("status") != "pending-explicit-execution-approval" or proposal["cost"]["absolute_cost_ceiling_usd"] != "2.25":
        raise ValueError("proposal escaped the approved boundary")
    if approval.get("status") != "approved" or approval.get("approved_proposal_sha256") != proposal_sha or approval.get("absolute_incremental_ceiling_usd") != "2.25":
        raise ValueError("approval does not bind exact proposal and ceiling")


def build_training(proposal: dict[str, Any], approval: dict[str, Any], local_card_path: Path) -> dict[str, Any]:
    validate_boundary(proposal, approval)
    local = load_sealed(local_card_path, "card_sha256")
    if local.get("schema_version") != "ganesh-mini-expansion-pilot-card/v4" or local.get("status") != "prepared-not-executable" or local.get("provider_execution") is not None or local.get("failed_checks"):
        raise ValueError("local v4 card is not intact and non-executable")
    provider = {
        "accelerator": "NVIDIA_L4",
        "approval_evidence_sha256": approval["approval_sha256"],
        "cost_ceiling_usd": 2.25,
        "hourly_cost_usd": float(proposal["cost"]["compute_hourly_usd"]),
        "machine_type": "g2-standard-8",
        "price_evidence_sha256": proposal["cost"]["price_evidence_sha256"],
        "prior_cost_usd": 0.0,
        "project": "executespecv1",
        "provider": "gcloud",
        "zone": "us-east1-c",
    }
    training = dict(local)
    training.pop("card_sha256")
    training["provider_execution"] = provider
    training["reason"] = "exact_gcloud_execution_proposal_and_ceiling_approved"
    training["status"] = "ready"
    training["card_sha256"] = canonical_sha256(training)
    return training


def build_execution(proposal: dict[str, Any], approval: dict[str, Any], training_card_path: Path, training_card_uri: str) -> dict[str, Any]:
    validate_boundary(proposal, approval)
    training = load_sealed(training_card_path, "card_sha256")
    provider = training.get("provider_execution") or {}
    if training.get("schema_version") != "ganesh-mini-expansion-pilot-card/v4" or training.get("status") != "ready" or provider.get("cost_ceiling_usd") != 2.25 or provider.get("approval_evidence_sha256") != approval["approval_sha256"]:
        raise ValueError("training card is not provider-bound to approved v4 ceiling")
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
    attempt_id = proposal["output_prefix"].rstrip("/").rsplit("/", 1)[-1]
    prefix = f"ganesh-mini-1.0/training/gradient-conflict-probe-v4/attempts/{attempt_id}"
    card: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate4-gcloud-execution/v1",
        "status": "authorized-executable",
        "source_commit": proposal["source_commit"],
        "approval": {
            "proposal_sha256": proposal["proposal_sha256"],
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
            "gcs_prefix": prefix, "attempt_id": attempt_id,
            "maximum_vm_lifetime_seconds": resource["maximum_vm_lifetime_seconds"],
            "controller_budget_seconds": runtime["controller_budget_seconds"],
            "backup_reserve_seconds": runtime["terminal_backup_reserve_seconds"],
            "automatic_restart": False, "external_ip": False, "boot_disk_auto_delete": True,
        },
    }
    card["execution_sha256"] = canonical_sha256(card)
    return card


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proposal", type=Path, required=True)
    parser.add_argument("--approval", type=Path, required=True)
    parser.add_argument("--local-card", type=Path, required=True)
    parser.add_argument("--training-output", type=Path, required=True)
    parser.add_argument("--training-card-uri")
    parser.add_argument("--execution-output", type=Path)
    args = parser.parse_args()
    proposal = load_sealed(args.proposal, "proposal_sha256")
    approval = load_sealed(args.approval, "approval_sha256")
    training = build_training(proposal, approval, args.local_card)
    write_json(args.training_output, training)
    result = {"training_card_sha256": training["card_sha256"]}
    if args.training_card_uri or args.execution_output:
        if not args.training_card_uri or not args.execution_output:
            parser.error("--training-card-uri and --execution-output are required together")
        execution = build_execution(proposal, approval, args.training_output, args.training_card_uri)
        write_json(args.execution_output, execution)
        result["execution_sha256"] = execution["execution_sha256"]
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
