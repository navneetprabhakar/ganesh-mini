#!/usr/bin/env python3
"""Build the authorized, generation-pinned Gate 1 GCloud execution card."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any

ROOT_HINT = Path(__file__).resolve().parents[2]
if str(ROOT_HINT) not in sys.path:
    sys.path.insert(0, str(ROOT_HINT))

from scripts.inference.build_gate1_gcloud_preparation import ROOT, canonical_sha256, load_sealed


INPUT_KEYS = {
    "workspace_archive",
    "workspace_manifest",
    "training_workspace_archive",
    "training_workspace_manifest",
    "completed_candidate_archive",
    "completed_candidate_manifest",
    "gate0_report",
    "gate1_report",
    "gate2_report",
    "model_archive",
    "cuda_image_archive",
    "docker_bundle",
    "verifier_archive",
    "verifier_manifest",
}
LOCAL_INPUT_MAPPING = {
    "workspace_archive": "workspace_archive",
    "workspace_manifest": "workspace_manifest",
    "verifier_archive": "verifier_archive",
    "verifier_manifest": "verifier_manifest",
    "training_workspace_archive": "training_workspace_archive",
    "training_workspace_manifest": "training_workspace_manifest",
    "completed_candidate_archive": "completed_candidate_archive",
    "completed_candidate_manifest": "completed_candidate_manifest",
    "gate0_report": "gate0_report",
    "gate1_report": "gate1_report",
    "gate2_report": "gate2_report",
    "model_archive": "model_archive",
    "cuda_image_archive": "cuda_image_archive",
    "docker_bundle": "docker_bundle",
}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def load_bindings(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop("bindings_sha256", None)
    if claimed != canonical_sha256(value):
        raise ValueError("input bindings seal mismatch")
    value["bindings_sha256"] = claimed
    return value


def current_head(root: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True
    ).stdout.strip()


def tracked_worktree_clean(root: Path) -> bool:
    return not subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def validate_approval(text: str, zone: str) -> None:
    normalized = " ".join(text.lower().split())
    required = ("approved", "gate 3", "g2-standard-12", zone.lower(), "3 hours", "usd 3.50")
    missing = [token for token in required if token not in normalized]
    if missing:
        raise ValueError(f"approval text does not bind the prepared execution: {missing}")


def build(
    bindings: dict[str, Any],
    approval_text: str,
    source_commit: str,
    root: Path = ROOT,
    *,
    require_clean: bool = True,
) -> dict[str, Any]:
    claimed_bindings = bindings.get("bindings_sha256")
    unsigned_bindings = {key: value for key, value in bindings.items() if key != "bindings_sha256"}
    if claimed_bindings != canonical_sha256(unsigned_bindings):
        raise ValueError("input bindings seal mismatch")
    preparation = load_sealed("measurement/gate3/gcloud/preparation.json", "preparation_sha256")
    if source_commit != current_head(root):
        raise ValueError("source commit is not the current repository HEAD")
    if require_clean and not tracked_worktree_clean(root):
        raise ValueError("tracked worktree must be clean before sealing an executable card")
    if bindings.get("schema_version") != "ganesh-mini-gate3-gcloud-bindings/v3" or bindings.get("status") != "verified-generation-pinned":
        raise ValueError("unsupported or incomplete Gate 1 bindings")
    if not re.fullmatch(r"[0-9]{8}T[0-9]{6}Z", str(bindings.get("run_id", ""))):
        raise ValueError("Gate 3 run ID must be an exact UTC timestamp")
    if bindings.get("preparation_sha256") != preparation["preparation_sha256"]:
        raise ValueError("bindings do not reference the current preparation")

    proposal = preparation["resource_proposal"]
    preflight = bindings.get("preflight", {})
    zone = preflight.get("zone")
    if zone not in proposal["allowed_zones"]:
        raise ValueError("preflight zone is not an allowed G2/L4 zone")
    validate_approval(approval_text, zone)
    expected_preflight = {
        "region": proposal["region"],
        "zone": zone,
        "machine_type": proposal["machine_type"],
        "service_account": proposal["service_account"],
    }
    for key, expected in expected_preflight.items():
        if preflight.get(key) != expected:
            raise ValueError(f"preflight {key} mismatch")
    for key in (
        "price_passed",
        "quota_passed",
        "machine_type_available",
        "exact_resources_absent",
        "bucket_round_trip_passed",
        "service_account_bucket_access_passed",
    ):
        if preflight.get(key) is not True:
            raise ValueError(f"preflight did not pass: {key}")
    for key in ("project", "gcs_bucket", "gcs_prefix", "boot_image"):
        if not isinstance(preflight.get(key), str) or not preflight[key]:
            raise ValueError(f"preflight is missing {key}")
    if "/images/" not in preflight["boot_image"] or "/family/" in preflight["boot_image"]:
        raise ValueError("boot image must be an exact image, not a family")

    cost = bindings.get("cost", {})
    hourly = Decimal(str(cost.get("conservative_hourly_usd")))
    reserve = Decimal(str(cost.get("support_reserve_usd")))
    ceiling = Decimal(str(cost.get("absolute_cost_ceiling_usd")))
    approved_ceiling = Decimal("3.50")
    upper = hourly * Decimal(proposal["maximum_run_seconds"]) / Decimal(3600) + reserve
    if hourly <= 0 or reserve < 0 or ceiling <= upper or ceiling > approved_ceiling:
        raise ValueError("cost preflight exceeds the approved bound")

    inputs = bindings.get("inputs", {})
    if set(inputs) != INPUT_KEYS:
        raise ValueError("bindings do not contain the exact Gate 1 input set")
    for key in INPUT_KEYS:
        require_generation_row(key, inputs[key])
    for card_key, local_key in LOCAL_INPUT_MAPPING.items():
        expected = preparation["local_inputs"][local_key]
        row = inputs[card_key]
        if row["sha256"] != expected["sha256"] or row["size_bytes"] != expected["size_bytes"]:
            raise ValueError(f"uploaded local input mismatch: {card_key}")

    launch = bindings.get("launch", {})
    if set(launch) != {"controller", "metadata_wrapper"}:
        raise ValueError("launch bindings are incomplete")
    for key in launch:
        row = require_generation_row(key, launch[key])
        expected = preparation["local_inputs"][key]
        if row["sha256"] != expected["sha256"] or row["size_bytes"] != expected["size_bytes"]:
            raise ValueError(f"launch input mismatch: {key}")

    resources = bindings.get("resources", {})
    if set(resources) != {"instance", "disk", "network", "subnet"} or not all(
        isinstance(resources[key], str) and resources[key] for key in resources
    ):
        raise ValueError("exact temporary resource names are missing")
    execution = {
        "attempt_id": bindings["run_id"],
        "gcp_project": preflight["project"],
        "gcs_bucket": preflight["gcs_bucket"],
        "gcs_prefix": preflight["gcs_prefix"],
        "region": proposal["region"],
        "zone": zone,
        "machine_type": proposal["machine_type"],
        "provisioning_model": proposal["provisioning_model"],
        "request_valid_for_seconds": proposal["request_valid_for_seconds"],
        "maximum_run_seconds": proposal["maximum_run_seconds"],
        "controller_budget_seconds": proposal["controller_budget_seconds"],
        "backup_reserve_seconds": proposal["backup_reserve_seconds"],
        "instance_termination_action": proposal["instance_termination_action"],
        "automatic_restart": proposal["automatic_restart"],
        "service_account": preflight["service_account"],
        "external_ip": False,
        "resources": resources,
    }
    card: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate3-gcloud-execution/v3",
        "status": "authorized-executable",
        "gate": 3,
        "gate_range": [3, 3],
        "source_commit": source_commit,
        "preparation_sha256": preparation["preparation_sha256"],
        "bindings_sha256": bindings["bindings_sha256"],
        "approval": {"verbatim": approval_text, "maximum_incremental_cost_usd": "3.50"},
        "model": preparation["model"],
        "evaluation": {
            "classification": "private_candidate_development",
            "surface": "development",
            "expected_task_count": 180,
            "decision_prompts_exposed": False,
        },
        "training": {
            "mechanism": "bf16-lora-conservative-v2",
            "objective": "unique-row-token-weighted-five-family-v2",
            "unique_train_records": 1399,
            "lr_candidates": [0.00001, 0.00003],
            "imported_lr_candidates": [0.00001],
            "trained_lr_candidates": [0.00003],
            "lr_candidate_seen_tokens_each": 461235,
            "main_seen_tokens": 0,
            "candidate_selection_tasks": 30,
            "selected_candidate_full_evaluation_tasks": 180,
            "evaluation_training_mount_isolation": True,
            "decision_prompts_exposed": False,
            "completed_candidate_manifest_sha256": preparation["completed_candidate"]["manifest_sha256"],
            "completed_candidate_run_evidence_sha256": preparation["completed_candidate"]["run_evidence_sha256"],
        },
        "execution": execution,
        "cost": {
            "conservative_hourly_usd": str(cost["conservative_hourly_usd"]),
            "support_reserve_usd": str(cost["support_reserve_usd"]),
            "conservative_upper_usd": str(upper),
            "absolute_cost_ceiling_usd": str(cost["absolute_cost_ceiling_usd"]),
        },
        "inputs": inputs,
        "launch": launch,
        "cuda_image": {
            "ref": preparation["rehydrated_inputs"]["cuda_image_ref"],
            "image_id": preparation["rehydrated_inputs"]["cuda_image_id"],
        },
        "boot_image": preflight["boot_image"],
        "required_terminal_state": [
            "exact 180-task run or sealed bounded failure",
            "terminal GCS inventory verified twice by immutable generation",
            "guest shutdown only after terminal backup",
            "provider maximum runtime stops rather than deletes the VM",
            "automatic restart is disabled; any host failure terminates this attempt",
            "VM and disk deleted only after independent backup verification",
            "temporary subnet and network deleted",
            "exact resource absence sealed and backed to GCS",
        ],
    }
    card["execution_sha256"] = canonical_sha256(card)
    return card


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bindings", type=Path, required=True)
    parser.add_argument("--approval-text-file", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    bindings = load_bindings(args.bindings)
    approval = args.approval_text_file.read_text(encoding="utf-8").strip()
    card = build(bindings, approval, args.source_commit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(card, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
