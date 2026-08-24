#!/usr/bin/env python3
"""Build the local, non-executable preparation record for Gate 1 on GCloud."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def file_identity(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return {"path": relative, "size_bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def load_sealed(relative: str, field: str) -> dict[str, Any]:
    value = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    claimed = value.pop(field, None)
    if claimed != canonical_sha256(value):
        raise ValueError(f"invalid {field}: {relative}")
    value[field] = claimed
    return value


def build() -> dict[str, Any]:
    workspace = load_sealed("measurement/gate1/development_workspace_20260823.json", "manifest_sha256")
    training_workspace = load_sealed("measurement/gate1/training_workspace_20260825.json", "manifest_sha256")
    verifier = load_sealed("measurement/gate1/verifier_image_bundle_amd64_v1.json", "manifest_sha256")
    gate0 = load_sealed("measurement/cuda/gcloud/20260824T180957Z/gpu_run_plan.json", "plan_sha256")
    gate0_result = load_sealed("measurement/cuda/gcloud/20260824T180957Z/run-result.json", "evidence_sha256")
    if gate0_result.get("status") != "passed" or gate0_result.get("gate") != "0B":
        raise ValueError("qualified Gate 0B evidence is missing")
    local_inputs = {
        "workspace_archive": file_identity("artifacts/eval/workspaces/development-v1.tar.gz"),
        "workspace_manifest": file_identity("measurement/gate1/development_workspace_20260823.json"),
        "verifier_archive": file_identity("artifacts/eval/verifier-images/amd64-v1/verifier-images-amd64-v1.tar"),
        "verifier_manifest": file_identity("measurement/gate1/verifier_image_bundle_amd64_v1.json"),
        "training_workspace_archive": file_identity("artifacts/train/workspaces/seed-pilot-v1.tar.gz"),
        "training_workspace_manifest": file_identity("measurement/gate1/training_workspace_20260825.json"),
        "gate0_report": file_identity("measurement/gate0/readiness.json"),
        "gate2_report": file_identity("measurement/gate2/readiness.json"),
        "controller": file_identity("scripts/inference/gcloud_startup_development_baseline.sh"),
        "metadata_wrapper": file_identity("scripts/inference/gcloud_baseline_metadata_wrapper.sh"),
        "execution_card_builder": file_identity("scripts/inference/build_gate1_gcloud_execution.py"),
        "terminal_validator": file_identity("scripts/inference/verify_gate1_terminal.py"),
        "finalizer": file_identity("scripts/inference/gcloud_finalize_gate1.sh"),
        "baseline_admitter": file_identity("scripts/inference/admit_gate1_baseline.py"),
        "price_evidence_builder": file_identity("scripts/inference/build_gate1_price_evidence.py"),
        "launcher": file_identity("scripts/inference/gcloud_launch_gate1.sh"),
        "baseline_admission_schema": file_identity("schemas/eval/gate1-baseline-admission.schema.json"),
        "execution_schema": file_identity("schemas/eval/gate1-gcloud-execution.schema.json"),
        "price_evidence_schema": file_identity("schemas/eval/gate1-price-evidence.schema.json"),
        "terminal_validation_schema": file_identity("schemas/eval/gate1-terminal-validation.schema.json"),
    }
    if local_inputs["workspace_archive"]["sha256"] != workspace["archive"]["sha256"]:
        raise ValueError("workspace archive no longer matches its sealed manifest")
    if local_inputs["training_workspace_archive"]["sha256"] != training_workspace["archive_sha256"]:
        raise ValueError("training workspace archive no longer matches its sealed manifest")
    if local_inputs["verifier_archive"]["sha256"] != verifier["archive"]["sha256"]:
        raise ValueError("verifier archive no longer matches its sealed manifest")
    record: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate1-gcloud-preparation/v1",
        "status": "prepared-not-executable",
        "gate": 1,
        "purpose": "staged exact-base baseline, two-point LR pilot, main seed SFT, and development adjudication on one L4",
        "model": {"model_id": "Qwen/Qwen3.5-2B", "revision": "15852e8c16360a2fea060d615a32b45270f8a8fc"},
        "resource_proposal": {
            "region": "us-east1",
            "zone": "us-east1-b",
            "machine_type": "g2-standard-12",
            "accelerator": "1x nvidia-l4",
            "provisioning_model": "FLEX_START",
            "request_valid_for_seconds": 7200,
            "maximum_run_seconds": 64800,
            "controller_budget_seconds": 63000,
            "backup_reserve_seconds": 1800,
            "instance_termination_action": "DELETE",
            "external_ip": False,
            "temporary_private_network": True,
        },
        "public_price_bound": {
            "checked_at": "2026-08-25",
            "region": "us-east1",
            "machine_type": "g2-standard-12",
            "published_on_demand_hourly_usd": 1.000416348,
            "published_dws_flex_start_hourly_usd": 0.790328877,
            "controller_conservative_hourly_usd": 1.000416348,
            "support_reserve_usd": 0.35,
            "eighteen_hour_conservative_upper_usd": 18.357494264,
            "proposed_absolute_ceiling_usd": 19.00,
            "source": "https://cloud.google.com/products/compute/pricing/accelerator-optimized",
            "fresh_account_preflight_still_required": True,
        },
        "utilization": {
            "generation_batch_size": 4,
            "verifier_workers": 12,
            "length_bucketing": True,
            "generation_and_verification_overlap": True,
            "sequential_gpu_phases": ["base-baseline", "lr-1e-4-train", "lr-1e-4-eval", "lr-2e-4-train", "lr-2e-4-eval", "main-train", "main-eval"],
            "evaluation_training_mount_isolation": True,
            "nvml_interval_seconds": 5,
            "checkpoint_interval_seconds": 120,
        },
        "local_inputs": local_inputs,
        "reused_generation_pinned_inputs": {
            "model": gate0["input"]["model_uri"],
            "qualified_cuda_image": gate0["input"]["image_uri"],
            "docker_bundle": gate0["input"]["docker_bundle_uri"],
            "cuda_image_id": gate0["input"]["cuda_image_id"],
            "cuda_image_ref": gate0["input"]["cuda_image_ref"],
            "qualified_gate0b_plan_seal": gate0["plan_sha256"],
            "qualified_gate0b_result_seal": gate0_result["evidence_sha256"],
        },
        "lifecycle": [
            "price, quota, exact-resource-absence, and bucket round-trip preflight",
            "upload local inputs and bind immutable GCS generations",
            "double-verify preflight evidence in GCS before any resource creation",
            "create temporary private network and Flex-start VM",
            "on launch failure, double-verify failure evidence, delete exact temporary resources, then prove absence and double-verify teardown evidence",
            "run offline baseline and require Gate 1 admission before training",
            "run both frozen LR candidates sequentially and evaluate each on development",
            "seal LR selection, run the exact main seed-token budget, evaluate, and adjudicate Gate 3",
            "checkpoint the complete campaign evidence to GCS every two minutes",
            "write terminal inventory and verified terminal GCS backup",
            "request guest shutdown only after terminal backup succeeds",
            "delete the stopped VM and disk, with provider max-run deletion as a backstop",
            "prove instance and disk absent, delete network, and prove all exact resources absent",
            "download every terminal object twice by immutable generation before Gate 1 admission",
            "atomically admit only a successful finalized baseline and rebuild the fail-closed Gate 1 readiness report",
        ],
        "hard_stops": [
            "no GCloud action without a fresh explicit execution approval",
            "no create until current price and quota preflight fit the approved ceiling",
            "no Gate 1 pass without all 180 task evidence seals",
            "no pilot training before Gate 1 passes",
            "no next phase after any anomaly or failed frozen gate",
        ],
        "failed_checks": [
            "current_g2_standard_12_price_and_quota_preflight",
            "generation_pinned_uploads_for_staged_campaign_inputs",
            "final_executable_card_and_metadata_bindings",
        ],
    }
    record["preparation_sha256"] = canonical_sha256(record)
    return record


def main() -> int:
    output = ROOT / "measurement/gate1/gcloud/preparation.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
