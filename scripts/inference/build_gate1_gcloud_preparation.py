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


def require_workspace_matches_source(manifest: dict[str, Any], label: str) -> dict[str, Any]:
    """Reject a sealed workspace whose files differ from the current source tree."""
    identities: list[dict[str, Any]] = []
    for row in manifest.get("files", []):
        relative = row.get("path")
        expected_size = row.get("size_bytes", row.get("size"))
        expected_sha256 = row.get("sha256")
        if not isinstance(relative, str) or not isinstance(expected_size, int) or not isinstance(expected_sha256, str):
            raise ValueError(f"invalid {label} workspace file identity")
        path = ROOT / relative
        if not path.is_file():
            raise ValueError(f"{label} workspace source file is missing: {relative}")
        observed = file_identity(relative)
        if observed["size_bytes"] != expected_size or observed["sha256"] != expected_sha256:
            raise ValueError(f"{label} workspace is stale relative to source: {relative}")
        identities.append(observed)
    if not identities:
        raise ValueError(f"{label} workspace has no source files")
    return {
        "file_count": len(identities),
        "source_collection_sha256": canonical_sha256(identities),
    }


def build() -> dict[str, Any]:
    workspace = load_sealed("measurement/gate3/development_workspace_v2.json", "manifest_sha256")
    training_workspace = load_sealed("measurement/gate3/training_workspace_v2.json", "manifest_sha256")
    verifier = load_sealed("measurement/gate1/verifier_image_bundle_amd64_v1.json", "manifest_sha256")
    runtime_rehearsal = load_sealed("measurement/gate3/runtime_bundle_rehearsal_v2.json", "evidence_sha256")
    gate0 = load_sealed("measurement/cuda/gcloud/20260824T180957Z/gpu_run_plan.json", "plan_sha256")
    gate0_result = load_sealed("measurement/cuda/gcloud/20260824T180957Z/run-result.json", "evidence_sha256")
    rehydrated = load_sealed("measurement/gate3/gcloud/rehydrated_inputs.json", "evidence_sha256")
    if gate0_result.get("status") != "passed" or gate0_result.get("gate") != "0B":
        raise ValueError("qualified Gate 0B evidence is missing")
    local_inputs = {
        "workspace_archive": file_identity("artifacts/eval/workspaces/development-v2.tar.gz"),
        "workspace_manifest": file_identity("measurement/gate3/development_workspace_v2.json"),
        "verifier_archive": file_identity("artifacts/eval/verifier-images/amd64-v1/verifier-images-amd64-v1.tar"),
        "verifier_manifest": file_identity("measurement/gate1/verifier_image_bundle_amd64_v1.json"),
        "training_workspace_archive": file_identity("artifacts/train/workspaces/seed-pilot-v2.tar.gz"),
        "training_workspace_manifest": file_identity("measurement/gate3/training_workspace_v2.json"),
        "gate0_report": file_identity("measurement/gate0/readiness.json"),
        "gate1_report": file_identity("measurement/gate1/readiness.json"),
        "gate2_report": file_identity("measurement/gate2/readiness.json"),
        "model_archive": file_identity("artifacts/gcloud-inputs/gate3/model.tar.gz"),
        "cuda_image_archive": file_identity("artifacts/gcloud-inputs/gate3/cuda-image.docker.tar.zst"),
        "docker_bundle": file_identity("artifacts/gcloud-inputs/gate3/docker-bundle.tar.gz"),
        "controller": file_identity("scripts/inference/gcloud_startup_development_baseline.sh"),
        "metadata_wrapper": file_identity("scripts/inference/gcloud_baseline_metadata_wrapper.sh"),
        "execution_card_builder": file_identity("scripts/inference/build_gate1_gcloud_execution.py"),
        "terminal_validator": file_identity("scripts/inference/verify_gate1_terminal.py"),
        "wrapper_terminal_synthesizer": file_identity("scripts/inference/synthesize_gate1_wrapper_terminal.py"),
        "finalizer": file_identity("scripts/inference/gcloud_finalize_gate1.sh"),
        "baseline_admitter": file_identity("scripts/inference/admit_gate1_baseline.py"),
        "price_evidence_builder": file_identity("scripts/inference/build_gate1_price_evidence.py"),
        "launcher": file_identity("scripts/inference/gcloud_launch_gate1.sh"),
        "rehydration_builder": file_identity("scripts/inference/build_gate3_rehydrated_inputs.py"),
        "rehydration_evidence": file_identity("measurement/gate3/gcloud/rehydrated_inputs.json"),
        "runtime_bundle_rehearsal": file_identity("measurement/gate3/runtime_bundle_rehearsal_v2.json"),
        "baseline_admission_schema": file_identity("schemas/eval/gate1-baseline-admission.schema.json"),
        "execution_schema": file_identity("schemas/eval/gate3-gcloud-execution.schema.json"),
        "price_evidence_schema": file_identity("schemas/eval/gate3-price-evidence.schema.json"),
        "terminal_validation_schema": file_identity("schemas/eval/gate3-terminal-validation.schema.json"),
    }
    if local_inputs["workspace_archive"]["sha256"] != workspace["archive"]["sha256"]:
        raise ValueError("workspace archive no longer matches its sealed manifest")
    if local_inputs["training_workspace_archive"]["sha256"] != training_workspace["archive_sha256"]:
        raise ValueError("training workspace archive no longer matches its sealed manifest")
    if local_inputs["verifier_archive"]["sha256"] != verifier["archive"]["sha256"]:
        raise ValueError("verifier archive no longer matches its sealed manifest")
    if rehydrated.get("status") != "verified-local-rehydration":
        raise ValueError("rehydrated input evidence is incomplete")
    for key in ("model_archive", "cuda_image_archive", "docker_bundle"):
        expected = rehydrated["artifacts"][key]
        observed = local_inputs[key]
        if observed["sha256"] != expected["sha256"] or observed["size_bytes"] != expected["size_bytes"]:
            raise ValueError(f"rehydrated artifact no longer matches its seal: {key}")
    if (
        runtime_rehearsal.get("status") != "passed"
        or runtime_rehearsal.get("workspace_manifest_sha256") != workspace["manifest_sha256"]
        or runtime_rehearsal.get("workspace_archive_sha256") != workspace["archive"]["sha256"]
    ):
        raise ValueError("sealed runtime bundle rehearsal does not bind the current evaluation workspace")
    workspace_source_alignment = {
        "evaluation": require_workspace_matches_source(workspace, "evaluation"),
        "training": require_workspace_matches_source(training_workspace, "training"),
    }
    record: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate3-gcloud-preparation/v2",
        "status": "prepared-not-executable",
        "gate": 3,
        "purpose": "Gate 3 v2 two-point conservative LoRA pilot, deterministic canary selection, and full development adjudication on one L4",
        "model": {"model_id": "Qwen/Qwen3.5-2B", "revision": "15852e8c16360a2fea060d615a32b45270f8a8fc"},
        "resource_proposal": {
            "region": "us-east1",
            "allowed_zones": ["us-east1-b", "us-east1-c", "us-east1-d"],
            "machine_type": "g2-standard-12",
            "accelerator": "1x nvidia-l4",
            "provisioning_model": "FLEX_START",
            "request_valid_for_seconds": 7200,
            "maximum_run_seconds": 14400,
            "controller_budget_seconds": 12600,
            "backup_reserve_seconds": 1800,
            "instance_termination_action": "STOP",
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
            "four_hour_conservative_upper_usd": 4.351665392,
            "proposed_absolute_ceiling_usd": 5.00,
            "source": "https://cloud.google.com/products/compute/pricing/accelerator-optimized",
            "fresh_account_preflight_still_required": True,
        },
        "utilization": {
            "generation_batch_size": 4,
            "verifier_workers": 12,
            "length_bucketing": True,
            "generation_and_verification_overlap": True,
            "sequential_gpu_phases": ["lr-1e-5-train", "lr-1e-5-canary", "lr-3e-5-train", "lr-3e-5-canary", "selected-candidate-full-eval"],
            "evaluation_training_mount_isolation": True,
            "nvml_interval_seconds": 5,
            "checkpoint_interval_seconds": 120,
            "historical_timing_basis": {
                "400652_token_candidate_seconds": 1845.013,
                "180_task_candidate_evaluation_seconds": 1709.522,
                "source_attempt": "20260826T042539Z"
            },
        },
        "local_inputs": local_inputs,
        "workspace_source_alignment": workspace_source_alignment,
        "rehydrated_inputs": {
            "evidence_sha256": rehydrated["evidence_sha256"],
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
            "on launch failure, double-verify failure evidence; preserve any created STOP-bounded VM and attached resources, otherwise clean unattached temporary resources",
            "verify the canonical Gate 1 readiness report and sealed 180-task base evidence before training",
            "run both frozen one-epoch LR candidates sequentially and evaluate each on the 30-task deterministic canary",
            "seal LR selection, evaluate only the selected candidate on all 180 development tasks, and adjudicate Gate 3",
            "checkpoint the complete campaign evidence to GCS every two minutes",
            "write terminal inventory and verified terminal GCS backup",
            "request guest shutdown only after terminal backup succeeds",
            "keep the VM and disk stopped until independent terminal-backup verification, then delete them",
            "prove instance and disk absent, delete network, and prove all exact resources absent",
            "download every terminal object twice by immutable generation before admitting Gate 3 evidence",
            "admit only a successful, finalized Gate 3 campaign",
        ],
        "hard_stops": [
            "no GCloud action without a fresh explicit execution approval",
            "no create until current price and quota preflight fit the approved ceiling",
            "no pilot training unless the existing Gate 1 report and all 180 base task evidence seals verify",
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
    output = ROOT / "measurement/gate3/gcloud/preparation.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
