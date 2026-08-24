#!/usr/bin/env python3
"""Admit the sealed fused-loss Gate 0B run as canonical CUDA qualification evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop(field, None)
    if claimed != canonical_sha256(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def require_postrun_object(manifest: dict[str, Any], path: Path, suffix: str) -> None:
    rows = [row for row in manifest.get("objects", []) if row.get("object_uri", "").endswith(suffix)]
    digest = file_sha256(path)
    if len(rows) != 1 or rows[0].get("verified") is not True:
        raise ValueError(f"post-run backup is missing one verified {suffix}")
    if not (rows[0].get("local_sha256") == rows[0].get("downloaded_sha256") == rows[0].get("verified_download_sha256") == digest):
        raise ValueError(f"post-run backup hash mismatch: {suffix}")


def build(root: Path) -> dict[str, Any]:
    root = root.resolve()
    contract = json.loads((root / "configs/model/qwen3_5_2b.contract.json").read_text())
    prequalification = load_sealed(
        root / "measurement/cuda/local/20260824T172717Z/fused-loss-prequalification.json",
        "evidence_sha256",
    )
    card_path = root / "measurement/cuda/gcloud/GATE0B_L4_V14_FUSED_LOSS_DRAFT_CARD.json"
    card = load_sealed(card_path, "card_sha256")
    run_dir = root / "measurement/cuda/gcloud/20260824T180957Z"
    plan_path = run_dir / "gpu_run_plan.json"
    plan = load_sealed(plan_path, "plan_sha256")
    result = load_sealed(run_dir / "run-result.json", "evidence_sha256")
    backup = load_sealed(run_dir / "backup-verification.json", "evidence_sha256")
    inventory = load_sealed(run_dir / "inventory-verification.json", "evidence_sha256")
    teardown = load_sealed(run_dir / "teardown-proof.json", "evidence_sha256")
    postrun = load_sealed(run_dir / "postrun-backup-verification.json", "evidence_sha256")

    run_id = "20260824T180957Z"
    if prequalification.get("schema_version") != "ganesh-mini-fused-loss-prequalification/v1" or prequalification.get("status") != "ready-for-fresh-cuda-qualification" or prequalification.get("qualification_claim") is not False:
        raise ValueError("local fused-loss prequalification contract is invalid")
    if card.get("schema_version") != "ganesh-mini-gate0b-l4-flex-execution-card/v14" or card.get("run_id") != run_id:
        raise ValueError("Gate 0B execution card identity mismatch")
    if plan.get("schema_version") != "ganesh-mini-gate0b-flex-run-plan/v2" or plan.get("run_id") != run_id:
        raise ValueError("Gate 0B run plan identity mismatch")
    if plan.get("approval", {}).get("execution_card_internal_sha256") != card["card_sha256"]:
        raise ValueError("run plan does not bind the approved execution card")
    if plan.get("approval", {}).get("execution_card_file_sha256") != file_sha256(card_path):
        raise ValueError("run plan does not bind the execution-card bytes")
    sidecar = (run_dir / "gpu_run_plan.sha256").read_text(encoding="utf-8").split()
    if len(sidecar) != 2 or sidecar[0] != file_sha256(plan_path) or sidecar[1] != "gpu_run_plan.json":
        raise ValueError("run plan SHA-256 sidecar mismatch")
    if card.get("source", {}).get("local_prequalification_sha256") != prequalification["evidence_sha256"]:
        raise ValueError("execution card does not bind local fused-loss prequalification")
    card_image = card.get("container_image", {})
    prequal_image = prequalification.get("container_image", {})
    plan_input = plan.get("input", {})
    expected_image = {
        "ref": "ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1-liger082",
        "id": "sha256:cdaf068ffcb933120181168ebf6ae1546ddf81e01b2ad006a1a18dd2e43d9860",
    }
    if not (
        card_image.get("tag") == prequal_image.get("tag") == plan_input.get("cuda_image_ref") == expected_image["ref"]
        and card_image.get("id") == prequal_image.get("id") == plan_input.get("cuda_image_id") == expected_image["id"]
        and prequal_image.get("build_status") == prequal_image.get("offline_smoke_status") == "passed"
        and prequal_image.get("offline_smoke_network") == "none"
    ):
        raise ValueError("qualified CUDA image identity or offline smoke mismatch")
    required_versions = {
        "torch": "2.13.0",
        "transformers": "5.15.1",
        "liger-kernel": "0.8.2",
        "causal-conv1d": "1.7.0",
        "flash-linear-attention": "0.5.2",
    }
    if prequal_image.get("package_versions") != required_versions:
        raise ValueError("qualified CUDA package versions changed")

    if result.get("schema_version") != "ganesh-mini-gate0b-fused-loss-result/v14" or result.get("run_id") != run_id or result.get("status") != "passed" or result.get("gate") != "0B":
        raise ValueError("Gate 0B result did not pass")
    if result.get("approval", {}).get("verbatim") != card.get("authorization", {}).get("verbatim"):
        raise ValueError("Gate 0B result approval differs from the execution card")
    qualification = result.get("qualification", {})
    fused = qualification.get("fused_training_loss", {})
    serialization = qualification.get("serialization_equivalence", {})
    if not (
        qualification.get("status") == "passed"
        and qualification.get("recipe_id") == "bf16-lora-primary-v1"
        and qualification.get("records_completed") == 16
        and qualification.get("optimizer_steps") == 16
        and 0 < qualification.get("observed_peak_vram_bytes", 0) <= qualification.get("maximum_peak_vram_bytes", 0)
        and fused.get("passed") is True
        and fused.get("provider") == "liger-kernel"
        and fused.get("version") == "0.8.2"
        and fused.get("materialize_training_logits") is False
        and fused.get("other_liger_kernels_enabled") is False
        and serialization.get("passed") is True
        and serialization.get("reload_max_abs_logit_difference") == 0.0
        and serialization.get("merge_logits_finite") is True
    ):
        raise ValueError("Gate 0B qualification envelope is incomplete")

    if backup.get("status") != "verified" or backup.get("object_count") != 41:
        raise ValueError("Gate 0B terminal backup is incomplete")
    qualification_uri = qualification["uri"]
    qualification_object, generation = qualification_uri.rsplit("#", 1)
    qualification_rows = [row for row in backup.get("objects", []) if row.get("object_uri") == qualification_object]
    if len(qualification_rows) != 1:
        raise ValueError("qualified result is missing from terminal backup")
    qualification_row = qualification_rows[0]
    if not (
        qualification_row.get("generation") == generation
        and qualification_row.get("verified") is True
        and qualification_row.get("downloaded_sha256") == qualification_row.get("verified_download_sha256") == qualification.get("file_sha256")
        and backup.get("evidence_sha256") == result.get("backup", {}).get("backup_manifest_evidence_sha256")
    ):
        raise ValueError("qualified result backup identity mismatch")
    if not (
        inventory.get("status") == "verified"
        and inventory.get("backup_manifest_evidence_sha256") == backup["evidence_sha256"]
        and inventory.get("inventory_entries") == result.get("backup", {}).get("inventory_entries") == 40
        and inventory.get("hash_mismatches") == 0
    ):
        raise ValueError("Gate 0B runtime inventory verification failed")
    if not (
        teardown.get("status") == "verified"
        and teardown.get("backup_precondition", {}).get("backup_manifest_evidence_sha256") == backup["evidence_sha256"]
        and all(teardown.get("absence", {}).get(key) is True for key in ("instance", "disk", "subnet", "network", "matching_routers"))
        and all(result.get("teardown", {}).get(key) is True for key in ("instance_absent", "disk_absent", "subnet_absent", "network_absent", "matching_router_scope_absent"))
    ):
        raise ValueError("Gate 0B teardown proof is incomplete")
    if result.get("cost", {}).get("within_ceiling") is not True or result.get("cost", {}).get("incremental_upper_usd", 2) > result.get("cost", {}).get("approved_ceiling_usd", 1):
        raise ValueError("Gate 0B cost exceeded approval")
    if postrun.get("status") != "verified" or postrun.get("object_count") != 4:
        raise ValueError("Gate 0B post-run evidence backup is incomplete")
    for filename in ("backup-verification.json", "inventory-verification.json", "run-result.json", "teardown-proof.json"):
        require_postrun_object(postrun, run_dir / filename, "/" + filename)

    evidence: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate0b-admission/v1",
        "passed": True,
        "gate": 0,
        "model_id": contract["model_id"],
        "revision": contract["revision"],
        "run_id": run_id,
        "recipe_id": qualification["recipe_id"],
        "cuda_image": expected_image,
        "package_versions": required_versions,
        "qualification_evidence_sha256": qualification["evidence_sha256"],
        "execution_card_file_sha256": file_sha256(card_path),
        "execution_card_internal_sha256": card["card_sha256"],
        "run_plan_file_sha256": file_sha256(plan_path),
        "run_plan_internal_sha256": plan["plan_sha256"],
        "run_result_sha256": result["evidence_sha256"],
        "terminal_backup_sha256": backup["evidence_sha256"],
        "runtime_inventory_sha256": inventory["evidence_sha256"],
        "teardown_sha256": teardown["evidence_sha256"],
        "postrun_backup_sha256": postrun["evidence_sha256"],
        "records_completed": qualification["records_completed"],
        "optimizer_steps": qualification["optimizer_steps"],
        "observed_peak_vram_bytes": qualification["observed_peak_vram_bytes"],
        "fused_linear_cross_entropy": fused,
        "serialization_equivalence": serialization,
        "incremental_upper_usd": result["cost"]["incremental_upper_usd"],
        "approved_ceiling_usd": result["cost"]["approved_ceiling_usd"],
        "exact_resources_absent": True,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, default=Path("measurement/gate0/cuda_qualification.json"))
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    evidence = build(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
