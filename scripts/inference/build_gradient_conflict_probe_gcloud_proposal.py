#!/usr/bin/env python3
"""Build the sealed, non-executable Gate 4 gradient-conflict GCloud proposal."""

from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "measurement/gate4/gradient-conflict-probe-20260911/gcloud-readonly-inspection-report.json"
LOCAL_CARD = ROOT / "artifacts/train/gradient-conflict-probe-v4/local-execution-card.json"
SOURCE_COMMIT = "3ae2ca8a1e00780226be935eaacfc87d618a96c4"
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
    card = load_sealed(card_path, "card_sha256")
    if report.get("status") != "complete-ready-for-separate-proposal" or report["conclusion"].get("execution_authorized") is not False:
        raise ValueError("read-only report does not permit proposal construction")
    if card.get("schema_version") != "ganesh-mini-expansion-pilot-card/v4" or card.get("status") != "prepared-not-executable" or card.get("provider_execution") is not None or card.get("failed_checks"):
        raise ValueError("local gradient-conflict card is not intact and non-executable")
    if report["pricing"]["compute_hourly_usd"] != str(COMPUTE_HOURLY_USD) or report["pricing"]["pd_balanced_gib_hourly_usd"] != str(DISK_GIB_HOURLY_USD):
        raise ValueError("inspection pricing escaped the proposal constants")

    hours = Decimal(MAXIMUM_SECONDS) / Decimal(3600)
    compute_upper = COMPUTE_HOURLY_USD * hours
    disk_upper = DISK_GIB_HOURLY_USD * DISK_GIB * hours
    provider_upper = compute_upper + disk_upper
    support_reserve = ABSOLUTE_CEILING_USD - provider_upper
    if support_reserve <= 0:
        raise ValueError("provider upper bound exceeds absolute ceiling")

    resource_names = {
        "instance": "ganesh-mini-g4-grad-20260911t020000z",
        "disk": "ganesh-mini-g4-grad-20260911t020000z",
        "network": "ganesh-mini-g4-grad-20260911t020000z-net",
        "subnet": "ganesh-mini-g4-grad-20260911t020000z-subnet",
    }
    if any(not report["resource_absence"][name]["absent"] for name in resource_names):
        raise ValueError("planned resource names are not all absent")

    proposal: dict[str, Any] = {
        "schema_version": "ganesh-mini-gradient-conflict-probe-gcloud-execution-proposal/v1",
        "status": "pending-explicit-execution-approval",
        "purpose": "one bounded Gate 4 gradient-conflict audit and, only if its frozen threshold passes, one PCGrad probe plus retention guard and frozen 30-task continuation screen",
        "inspection_report_sha256": report["report_sha256"],
        "local_training_card_sha256": card["card_sha256"],
        "source_commit": SOURCE_COMMIT,
        "model": card["model"],
        "experiment": {
            "recipe_id": card["selected_recipe"]["recipe_id"],
            "records": card["data"]["records"],
            "input_tokens": card["data"]["input_tokens"],
            "optimizer_groups": 64,
            "retention_records": card["data"]["retention_records"],
            "stage_1": card["selected_recipe"]["gradient_conflict"]["stage_1"],
            "stage_2": card["selected_recipe"]["gradient_conflict"]["stage_2"],
            "stage_1_audit_conservative_seconds": card["throughput"]["stage_1_audit_conservative_seconds"],
            "expected_training_seconds": card["throughput"]["expected_training_seconds"],
            "conservative_training_seconds": card["throughput"]["conservative_training_seconds"],
            "canary_tasks": card["evaluation"]["canary_tasks"],
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
            "automatic_restart": False, "maximum_vm_lifetime_seconds": MAXIMUM_SECONDS,
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
        "inputs": {name: {"uri": row["generation_uri"], "sha256": row["sha256"], "size_bytes": row["size_bytes"]} for name, row in report["inputs"].items()},
        "launch": {
            "controller": {key: report["inputs"]["controller"][source] for key, source in (("uri", "generation_uri"), ("sha256", "sha256"), ("size_bytes", "size_bytes"))},
            "metadata_wrapper": report["embedded_metadata_wrapper"],
        },
        "post_approval_create_only_uploads": {
            "training_execution_card": {
                "destination": "gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/gradient-conflict-probe-v4/attempts/20260911T020000Z/input/training-execution-card.json",
                "derivation": "bind the local v4 card to exact approval, provider price, prior cost 0, and ceiling 2.25",
            },
            "outer_execution_card": {
                "destination": "gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/gradient-conflict-probe-v4/attempts/20260911T020000Z/input/execution-card.json",
                "derivation": "bind proposal, approval, generation-pinned inputs, and assigned training-card generation",
            },
            "precondition": "both objects use create-only upload and exact-generation roundtrip verification before resource creation",
        },
        "output_prefix": "gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/gradient-conflict-probe-v4/attempts/20260911T020000Z",
        "allowed_sequence": [
            "record exact approval evidence for this proposal",
            "derive, create-only upload, and exact-generation verify the two declared execution cards",
            "recheck exact resource absence and create only the four named temporary resources plus the single VM",
            "run the eight-group gradient-conflict audit with zero optimizer steps",
            "if the audit threshold fails, stop without training or evaluation; otherwise run the bounded 640-row PCGrad probe and save/reload verification",
            "apply the sealed 60-row non-evaluation retention loss guard",
            "run only the frozen 30-task continuation screen; never run the 180-task development surface",
            "back up all artifacts, logs, hashes, verifier results, and provider evidence to GCS",
            "independently download and verify the terminal package before teardown",
            "delete the VM, auto-delete disk, subnet, and network, then verify absence twice",
            "verify no Ganesh billable resource remains; preserve GCS and do not touch unrelated disk laxmi-wmv2-training-01",
        ],
        "hard_stops": [
            "no GCloud mutation or upload before explicit approval of this exact proposal seal and USD 2.25 ceiling",
            "no optimizer step or canary evaluation if the gradient-conflict audit threshold fails",
            "no full-development evaluation, decision-set opening, main training, correction pass, merge, quantization, publication, or release claim",
            "no teardown until terminal evidence is independently recovered and verified",
            "capacity refusal is infrastructure evidence, not a model-quality failure",
        ],
        "approval": {
            "approved": False,
            "requested_format": "I approve GCloud gradient-conflict-probe execution proposal <proposal_sha256> with the $2.25 absolute incremental ceiling.",
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
