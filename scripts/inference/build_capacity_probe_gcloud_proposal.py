#!/usr/bin/env python3
"""Build the sealed, non-executable Gate 4 capacity-probe GCloud proposal."""

from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "measurement/gate4/capacity-probe-20260909/gcloud-readonly-inspection-report.json"
LOCAL_CARD = ROOT / "artifacts/train/expansion-capacity-probe-v2/local-execution-card.json"
ATTEMPT_ID = "20260909T173721Z"
BUCKET = "ganesh-gate0-model-transfer-1061994342941"
PREFIX = f"ganesh-mini-1.0/training/capacity-probe-v2/attempts/{ATTEMPT_ID}"
COMPUTE_HOURLY_USD = Decimal("0.853624312")
DISK_GIB_HOURLY_USD = Decimal("0.000136986")
DISK_GIB = 200
MAXIMUM_SECONDS = 7200
ABSOLUTE_CEILING_USD = Decimal("2.25")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop(field, None)
    if claimed != canonical_sha256(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def build(report_path: Path = REPORT, card_path: Path = LOCAL_CARD) -> dict[str, Any]:
    report = load_sealed(report_path, "report_sha256")
    local_card = load_sealed(card_path, "card_sha256")
    if report.get("status") != "complete-ready-for-separate-proposal" or report["conclusion"].get("execution_authorized") is not False:
        raise ValueError("read-only report does not permit proposal construction")
    if local_card.get("status") != "prepared-not-executable" or local_card.get("provider_execution") is not None or local_card.get("failed_checks"):
        raise ValueError("local training card is not an intact non-executable card")

    hours = Decimal(MAXIMUM_SECONDS) / Decimal(3600)
    compute_upper = COMPUTE_HOURLY_USD * hours
    disk_upper = DISK_GIB_HOURLY_USD * DISK_GIB * hours
    provider_upper = compute_upper + disk_upper
    support_reserve = ABSOLUTE_CEILING_USD - provider_upper
    if support_reserve <= 0:
        raise ValueError("provider upper bound exceeds the absolute ceiling")

    campaign_inputs = {}
    for key in (
        "evaluation_workspace_archive", "evaluation_workspace_manifest",
        "train_workspace_archive", "train_workspace_manifest", "model_archive",
        "cuda_image_archive", "docker_bundle", "verifier_archive", "verifier_manifest",
    ):
        row = report["inputs"][key]
        campaign_inputs[key] = {"uri": row["generation_uri"], "sha256": row["sha256"], "size_bytes": row["size_bytes"]}

    resource_names = {
        "instance": "ganesh-mini-g4-capacity-20260909t173721z",
        "disk": "ganesh-mini-g4-capacity-20260909t173721z",
        "network": "ganesh-mini-g4-capacity-20260909t173721z-net",
        "subnet": "ganesh-mini-g4-capacity-20260909t173721z-subnet",
    }
    proposal: dict[str, Any] = {
        "schema_version": "ganesh-mini-capacity-probe-gcloud-execution-proposal/v1",
        "status": "pending-explicit-execution-approval",
        "purpose": "one bounded Gate 4 capacity probe followed only by its frozen 30-task continuation screen",
        "inspection_report_sha256": report["report_sha256"],
        "local_training_card_sha256": local_card["card_sha256"],
        "source_commit": "3cbdccf86962654f20d2fd885fa05b573c2625ce",
        "model": local_card["model"],
        "experiment": {
            "recipe_id": local_card["selected_recipe"]["recipe_id"],
            "records": local_card["data"]["records"],
            "input_tokens": local_card["data"]["input_tokens"],
            "trainable_parameters": 7520256,
            "expected_training_seconds": local_card["throughput"]["expected_training_seconds"],
            "conservative_training_seconds": local_card["throughput"]["conservative_training_seconds"],
            "canary_tasks": 30,
            "full_development_tasks": 0,
            "promotion_authority": "continuation-planning-only",
        },
        "resource": {
            "project": "executespecv1", "region": "us-east1", "zone": "us-east1-c",
            "names": resource_names,
            "machine_type": "g2-standard-8", "accelerator": "1x NVIDIA L4",
            "provisioning_model": "STANDARD", "boot_disk_gib": DISK_GIB,
            "boot_disk_type": "pd-balanced", "boot_disk_auto_delete": True,
            "boot_image": "projects/deeplearning-platform-release/global/images/common-cu129-ubuntu-2204-nvidia-580-v20260831",
            "service_account": "1061994342941-compute@developer.gserviceaccount.com",
            "external_ip": False, "private_google_access": True, "cloud_nat": False,
            "automatic_restart": False,
            "maximum_vm_lifetime_seconds": MAXIMUM_SECONDS,
        },
        "cost": {
            "compute_hourly_usd": str(COMPUTE_HOURLY_USD),
            "pd_balanced_gib_hourly_usd": str(DISK_GIB_HOURLY_USD),
            "compute_upper_usd": str(compute_upper), "boot_disk_upper_usd": str(disk_upper),
            "provider_upper_usd": str(provider_upper), "support_reserve_usd": str(support_reserve),
            "absolute_cost_ceiling_usd": str(ABSOLUTE_CEILING_USD), "prior_cost_usd": "0",
            "price_evidence_sha256": report["pricing"]["same_day_price_evidence_sha256"],
        },
        "runtime": {
            "controller_budget_seconds": 6000, "terminal_backup_reserve_seconds": 1200,
            "checkpoint_interval_seconds": 120, "docker_network": "none",
            "guest_shutdown_after_terminal_backup": True,
        },
        "inputs": campaign_inputs,
        "launch": {
            "controller": {k: report["inputs"]["controller"][src] for k, src in (("uri", "generation_uri"), ("sha256", "sha256"), ("size_bytes", "size_bytes"))},
            "metadata_wrapper": report["embedded_metadata_wrapper"],
        },
        "post_approval_create_only_uploads": {
            "training_execution_card": {
                "destination": f"gs://{BUCKET}/{PREFIX}/input/training-execution-card.json",
                "derivation": "bind the sealed local card to this proposal approval, exact provider price, prior cost 0, and ceiling 2.25",
            },
            "outer_execution_card": {
                "destination": f"gs://{BUCKET}/{PREFIX}/input/execution-card.json",
                "derivation": "bind this proposal, its approval evidence, all generation-pinned inputs, and the assigned training-card generation",
            },
            "precondition": "both objects are uploaded create-only and exact-generation roundtrip verified before resource creation",
        },
        "output_prefix": f"gs://{BUCKET}/{PREFIX}",
        "allowed_sequence": [
            "record exact approval evidence for this proposal",
            "derive, create-only upload, and exact-generation verify the two declared execution cards",
            "recheck exact resource absence and create only the four named temporary resources plus the single VM",
            "run the bounded 624-row training probe and save/reload verification",
            "run only the frozen 30-task continuation screen; never run the 180-task development surface",
            "back up all artifacts, logs, hashes, verifier results, and provider evidence to GCS",
            "independently download and verify the terminal package before teardown",
            "delete the VM, auto-delete disk, subnet, and network, then verify absence twice",
            "verify no Ganesh billable resource remains; preserve GCS and do not touch unrelated disk laxmi-wmv2-training-01",
        ],
        "hard_stops": [
            "no GCloud mutation or upload before explicit approval of this exact proposal seal and USD 2.25 ceiling",
            "no full-development evaluation, decision-set opening, main training, correction pass, merge, quantization, publication, or release claim",
            "no teardown until terminal evidence is independently recovered and verified",
            "capacity is not guaranteed; a provider capacity refusal is infrastructure evidence, not a model failure",
        ],
        "approval": {
            "approved": False,
            "requested_format": "I approve GCloud capacity-probe execution proposal <proposal_sha256> with the $2.25 absolute incremental ceiling.",
        },
    }
    proposal["proposal_sha256"] = canonical_sha256(proposal)
    return proposal


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    proposal = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(proposal, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": proposal["status"], "proposal_sha256": proposal["proposal_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
