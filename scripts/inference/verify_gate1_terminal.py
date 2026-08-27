#!/usr/bin/env python3
"""Validate the downloaded Gate 1 terminal backup before VM deletion."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.inference.run_development_baseline_host import (
    canonical_sha256,
    load_sealed,
    validate_completed_run,
)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_inventory(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split(None, 1)
        relative = relative.lstrip("*").removeprefix("./")
        if len(digest) != 64 or relative in rows or not relative:
            raise ValueError("runtime inventory contains an invalid or duplicate row")
        rows[relative] = digest
    if not rows:
        raise ValueError("runtime inventory is empty")
    return rows


def validate_gate3_evaluation_run(
    path: Path, card: dict[str, Any], expected_tasks: int
) -> tuple[dict[str, Any], str, frozenset[str], dict[str, int]]:
    run = load_sealed(path, "run_sha256")
    accounting = run.get("task_accounting", {})
    model = run.get("model", {})
    summaries = run.get("tasks", [])
    if (
        run.get("schema_version") != "ganesh-mini-inference-run/v2"
        or run.get("classification") != "private_candidate_development"
        or model.get("revision") != card.get("model", {}).get("revision")
        or accounting.get("expected") != expected_tasks
        or accounting.get("completed") != expected_tasks
        or accounting.get("pending") != 0
        or len(summaries) != expected_tasks
    ):
        raise ValueError("Gate 3 candidate run did not satisfy the frozen completion contract")
    summary_by_id = {row.get("task_id"): row for row in summaries}
    if None in summary_by_id or len(summary_by_id) != expected_tasks:
        raise ValueError("Gate 3 candidate run contains duplicate or missing task IDs")
    result_seals: list[str] = []
    lanes = ("go", "java", "javascript", "typescript", "python", "rust")
    lane_counts = {lane: 0 for lane in lanes}
    lane_passes = {lane: 0 for lane in lanes}
    task_root = path.parent / "tasks"
    for task_id in sorted(summary_by_id):
        evidence_path = task_root / f"{task_id}.json"
        evidence = load_sealed(evidence_path, "evidence_sha256")
        result = evidence.get("verification", {}).get("result")
        if not isinstance(result, dict):
            raise ValueError("Gate 3 candidate task evidence is missing its verifier result")
        result_copy = dict(result)
        result_seal = result_copy.pop("result_sha256", None)
        if result_seal != canonical_sha256(result_copy):
            raise ValueError("Gate 3 candidate verifier result seal mismatch")
        summary = summary_by_id[task_id]
        if (
            evidence["evidence_sha256"] != summary.get("evidence_sha256")
            or result.get("task_id") != task_id
            or result.get("passed") is not summary.get("passed")
            or result.get("language") not in lane_counts
        ):
            raise ValueError("Gate 3 candidate task evidence does not bind its run summary")
        result_seals.append(result_seal)
        lane_counts[result["language"]] += 1
        lane_passes[result["language"]] += result.get("passed") is True
    if accounting.get("passed") != sum(row.get("passed") is True for row in summaries):
        raise ValueError("Gate 3 candidate pass accounting mismatch")
    expected_per_lane = expected_tasks // len(lanes)
    if expected_tasks % len(lanes) or set(lane_counts.values()) != {expected_per_lane}:
        raise ValueError("Gate 3 candidate evaluation is not balanced across six lanes")
    return run, canonical_sha256(result_seals), frozenset(summary_by_id), lane_passes


def validate_gate3_training_run(
    path: Path, card: dict[str, Any], learning_rate: float
) -> dict[str, Any]:
    training = load_sealed(path, "evidence_sha256")
    minimum_tokens = card.get("training", {}).get("lr_candidate_seen_tokens_each")
    if (
        training.get("schema_version") != "ganesh-mini-sft-run/v2"
        or training.get("status") != "complete"
        or training.get("identities", {}).get("phase") != "lr-candidate"
        or training.get("identities", {}).get("learning_rate") != str(learning_rate)
        or not isinstance(minimum_tokens, int)
        or training.get("state", {}).get("seen_tokens") != minimum_tokens
        or training.get("planned_end_row") != card.get("training", {}).get("unique_train_records")
        or training.get("save_reload", {}).get("passed") is not True
    ):
        raise ValueError("Gate 3 training run is incomplete or escaped its exact epoch")
    return training


def validate_gate3_success(campaign_root: Path, card: dict[str, Any]) -> dict[str, Any]:
    campaign = load_sealed(campaign_root / "campaign-result.json", "evidence_sha256")
    if (
        campaign.get("schema_version") != "ganesh-mini-staged-campaign-result/v1"
        or campaign.get("status") != "passed"
        or campaign.get("attempt_id") != card["execution"]["attempt_id"]
    ):
        raise ValueError("Gate 3 campaign result is incomplete")
    selection = load_sealed(campaign_root / "lr-selection.json", "evidence_sha256")
    selected = selection.get("selected_learning_rate")
    expected_lrs = card.get("training", {}).get("lr_candidates", [])
    if (
        selection.get("schema_version") != "ganesh-mini-lr-selection/v2"
        or selection.get("status") != "selected"
        or selection.get("surface") != "development-canary"
        or selection.get("expected_task_count") != 30
        or selected not in expected_lrs
        or set(selection.get("candidates", {})) != {str(value) for value in expected_lrs}
    ):
        raise ValueError("Gate 3 LR selection is incomplete or escaped the executable card")
    validated_training: dict[float, dict[str, Any]] = {}
    validated_canaries: dict[float, tuple[dict[str, Any], str, frozenset[str], dict[str, int]]] = {}
    for learning_rate in expected_lrs:
        label = f"lr-{float(learning_rate):.0e}".replace("e-0", "e-").replace("e+0", "e+")
        training = validate_gate3_training_run(
            campaign_root / "training" / label / "run-evidence.json", card, learning_rate
        )
        canary = validate_gate3_evaluation_run(
            campaign_root / "evaluation" / f"{label}-canary" / "run.json", card, 30
        )
        selection_row = selection["candidates"].get(str(learning_rate), {})
        if (
            selection_row.get("run_evidence_sha256") != training["evidence_sha256"]
            or selection_row.get("result_collection_sha256") != canary[1]
            or selection_row.get("passed") != canary[0]["task_accounting"]["passed"]
            or selection_row.get("lanes") != canary[3]
        ):
            raise ValueError("Gate 3 LR selection does not bind its candidate evidence")
        validated_training[learning_rate] = training
        validated_canaries[learning_rate] = canary
    if len({proof[2] for proof in validated_canaries.values()}) != 1:
        raise ValueError("Gate 3 LR canaries do not cover the same frozen tasks")
    label = f"lr-{float(selected):.0e}".replace("e-0", "e-").replace("e+0", "e+")
    training = validated_training[selected]
    candidate, _, _, _ = validate_gate3_evaluation_run(
        campaign_root / "evaluation" / f"{label}-full" / "run.json", card, 180
    )
    promotion = load_sealed(campaign_root / "pilot-promotion.json", "evidence_sha256")
    expected_promotion_checks = {
        "four_of_five_families_improve", "no_lane_regression",
        "quality_failures_do_not_increase", "retention_slice",
        "sft_complete_and_reload_reproduced",
    }
    promotion_checks = promotion.get("checks", [])
    if (
        promotion.get("schema_version") != "ganesh-mini-pilot-promotion/v1"
        or promotion.get("status") != "promote"
        or promotion.get("failed_checks") != []
        or {row.get("name") for row in promotion_checks} != expected_promotion_checks
        or any(row.get("passed") is not True for row in promotion_checks)
    ):
        raise ValueError("Gate 3 promotion evidence is not a pass")
    candidate_labels = {
        f"lr-{float(value):.0e}".replace("e-0", "e-").replace("e+0", "e+")
        for value in expected_lrs
    }
    required_phases = {
        "workspace-isolation", "gate1-canonical-baseline", "verifier-runtime-images",
        "gate3-training-admission",
        "lr-selection", f"evaluate-{label}-full", "gate3-promotion",
        *(f"train-{candidate_label}" for candidate_label in candidate_labels),
        *(f"evaluate-{candidate_label}-canary" for candidate_label in candidate_labels),
    }
    passed_phases = {
        row.get("name") for row in campaign.get("phases", []) if row.get("status") == "passed"
    }
    if not required_phases <= passed_phases:
        raise ValueError("Gate 3 campaign result omits required passed phases")
    return {
        "campaign_result_sha256": campaign["evidence_sha256"],
        "lr_selection_sha256": selection["evidence_sha256"],
        "selected_learning_rate": selected,
        "training_run_sha256": training["evidence_sha256"],
        "run_sha256": candidate["run_sha256"],
        "task_accounting": candidate["task_accounting"],
        "promotion_sha256": promotion["evidence_sha256"],
    }


def verify(
    backup_manifest_path: Path,
    download_root: Path,
    execution_card_path: Path,
    expected_prefix: str,
) -> dict[str, Any]:
    manifest = load_sealed(backup_manifest_path, "evidence_sha256")
    card = load_sealed(execution_card_path, "execution_sha256")
    if manifest.get("status") != "verified" or manifest.get("prefix") != expected_prefix:
        raise ValueError("terminal backup manifest status or prefix mismatch")
    if card.get("schema_version") not in {"ganesh-mini-staged-gcloud-execution/v1", "ganesh-mini-gate3-gcloud-execution/v2"} or card.get("status") != "authorized-executable":
        raise ValueError("execution card contract mismatch")
    objects = manifest.get("objects", [])
    if not objects or not all(row.get("verified") is True for row in objects):
        raise ValueError("terminal backup contains unverified objects")
    object_rows = {
        row["object_uri"].removeprefix(expected_prefix.rstrip("/") + "/"): row
        for row in objects
        if row["object_uri"].startswith(expected_prefix.rstrip("/") + "/")
    }
    if len(object_rows) != len(objects):
        raise ValueError("terminal backup contains duplicate or out-of-prefix objects")
    inventory_path = download_root / "runtime-files.sha256"
    inventory = parse_inventory(inventory_path)
    inventory_row = object_rows.get("runtime-files.sha256")
    if inventory_row is None or inventory_row.get("downloaded_sha256") != file_sha256(inventory_path):
        raise ValueError("terminal inventory object is missing or mismatched")
    for relative, digest in inventory.items():
        path = download_root / relative
        if not path.is_file() or file_sha256(path) != digest:
            raise ValueError(f"downloaded terminal artifact mismatch: {relative}")
        row = object_rows.get(relative)
        if row is None or row.get("downloaded_sha256") != digest:
            raise ValueError(f"GCS terminal artifact mismatch: {relative}")

    startup_code = int((download_root / "startup-exit-code.txt").read_text().strip())
    controller_code_path = download_root / "controller-exit-code.txt"
    controller_code = int(controller_code_path.read_text().strip()) if controller_code_path.is_file() else None
    successful = startup_code == controller_code == 0
    run_summary: dict[str, Any] | None = None
    campaign_root=download_root / "output/campaign"
    is_gate3 = card.get("schema_version") == "ganesh-mini-gate3-gcloud-execution/v2"
    if not is_gate3 and (campaign_root / "baseline/run.json").is_file():
        run = validate_completed_run(campaign_root / "baseline/run.json")
        host = load_sealed(campaign_root / "baseline/host-execution.json", "evidence_sha256")
        execution = card["execution"]
        if (
            host.get("status") != "passed"
            or host.get("attempt_id") != execution["attempt_id"]
            or host.get("run", {}).get("run_sha256") != run["run_sha256"]
            or host.get("run", {}).get("task_accounting") != run["task_accounting"]
        ):
            raise ValueError("host execution does not bind the completed baseline run")
        run_summary = {
            "run_sha256": run["run_sha256"],
            "host_execution_sha256": host["evidence_sha256"],
            "task_accounting": run["task_accounting"],
        }
    if successful:
        if is_gate3:
            run_summary = validate_gate3_success(campaign_root, card)
        else:
            if run_summary is None:
                raise ValueError("successful campaign is missing the completed baseline")
            campaign = load_sealed(campaign_root / "campaign-result.json", "evidence_sha256")
            if campaign.get("status") != "passed" or campaign.get("attempt_id") != card["execution"]["attempt_id"]:
                raise ValueError("staged campaign result is incomplete")
            run_summary["campaign_result_sha256"] = campaign["evidence_sha256"]
    else:
        diagnostics = [download_root / "controller.stderr.log", download_root / "startup.stderr.log"]
        if startup_code == 0 and controller_code is None:
            raise ValueError("controller exit code is missing from an otherwise successful startup")
        if not any(path.is_file() and path.stat().st_size > 0 for path in diagnostics):
            raise ValueError("failed baseline is missing startup/controller diagnostics")

    evidence: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate3-terminal-validation/v2" if is_gate3 else "ganesh-mini-gate1-terminal-validation/v1",
        "status": "passed" if successful else "sealed-failure",
        "attempt_id": card["execution"]["attempt_id"],
        "expected_prefix": expected_prefix,
        "execution_sha256": card["execution_sha256"],
        "backup_manifest_sha256": manifest["evidence_sha256"],
        "runtime_inventory_sha256": file_sha256(inventory_path),
        "runtime_inventory_entries": len(inventory),
        "terminal_object_count": len(objects),
        "startup_exit_code": startup_code,
        "controller_exit_code": controller_code,
        "run": run_summary,
        "deletion_eligible": True,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backup-manifest", type=Path, required=True)
    parser.add_argument("--download-root", type=Path, required=True)
    parser.add_argument("--execution-card", type=Path, required=True)
    parser.add_argument("--expected-prefix", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    evidence = verify(
        args.backup_manifest,
        args.download_root,
        args.execution_card,
        args.expected_prefix,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if evidence["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
