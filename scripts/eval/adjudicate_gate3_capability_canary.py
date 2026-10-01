#!/usr/bin/env python3
"""Select one completed Gate 3 capability LR from the frozen 30-task canary.

This is checkpoint triage, not a Gate 3 quality pass.  The only downstream
authority conveyed by a successful report is to evaluate the selected adapter
on the complete 180-task private development surface.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.eval.contracts import ContractError, sha256_object, validate_result, write_json


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
LEARNING_RATES = ("1e-5", "3e-5")
RULE = "select_0.00003_only_if_30_task_canary_improves_by_at_least_one_pass_with_no_lane_regression_else_0.00001"
PREPARED_DATA_SHA256 = "6f43f373c34fd61749b44ef73eb8803f9f0df33ad13b2358ee6efde95fe5fa1f"
PREPARED_MANIFEST_SHA256 = "4bae0de2096ce8ae973d0f7b3ecc9214d8b6ef2e3addfb31cc4afd37446c2d01"
MODEL_REVISION = "15852e8c16360a2fea060d615a32b45270f8a8fc"
CANARY_MANIFEST_SHA256 = "0b7483141ba64ba223bc976ed7711ad847bc1056888be0e7bd9d261b85cffa44"
EVALUATION_WORKSPACE_SHA256 = "8ed2f45d87b3b867a59c6eca03be6e9d991bd1070037bd52311ed63a07585edc"


def _sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ContractError(f"not an object: {path}")
    unsigned = dict(value)
    claimed = unsigned.pop(field, None)
    if claimed != sha256_object(unsigned):
        raise ContractError(f"invalid {field}: {path}")
    return value


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _manifest(canary_path: Path, workspace_path: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, dict[str, Any]]]:
    canary = _sealed(canary_path, "manifest_sha256")
    workspace = _sealed(workspace_path, "manifest_sha256")
    if canary["manifest_sha256"] != CANARY_MANIFEST_SHA256 or workspace["manifest_sha256"] != EVALUATION_WORKSPACE_SHA256:
        raise ContractError("canary or evaluation workspace differs from frozen Gate 3 input")
    if (canary.get("schema_version"), canary.get("status"), canary.get("surface"), canary.get("records")) != (
        "ganesh-mini-gate3-canary/v1", "frozen", "development", 30
    ):
        raise ContractError("not the frozen 30-task development canary")
    if canary.get("promotion_selection_allowed") is not False or canary.get("training_admission_allowed") is not False:
        raise ContractError("canary authority must exclude promotion and training")
    if (workspace.get("schema_version"), workspace.get("status"), workspace.get("surface"), workspace.get("task_count")) != (
        "ganesh-mini-development-evaluation-workspace/v1", "sealed", "development", 180
    ):
        raise ContractError("not the sealed development-only evaluation workspace")
    canary_file = next((item for item in workspace.get("files", []) if item.get("path") == "eval/private/development/gate3_canary_manifest.json"), None)
    if canary_file is None or canary_file.get("sha256") != _sha256_file(canary_path):
        raise ContractError("canary bytes are not bound by the evaluation workspace")
    tasks = canary.get("tasks")
    if not isinstance(tasks, list) or len(tasks) != 30:
        raise ContractError("invalid canary task list")
    by_id = {item.get("task_id"): item for item in tasks if isinstance(item, dict)}
    if len(by_id) != 30 or any(not isinstance(task_id, str) for task_id in by_id):
        raise ContractError("duplicate or invalid canary task IDs")
    if Counter(item.get("language") for item in tasks) != Counter({lane: 5 for lane in LANES}):
        raise ContractError("canary must have five tasks in each lane")
    if any(not task_id.startswith("dev-t1-") for task_id in by_id):
        raise ContractError("canary must contain only tranche-1 development tasks")
    return canary, workspace, by_id


def _run(path: Path, learning_rate: str) -> dict[str, Any]:
    run = _sealed(path, "evidence_sha256")
    identity = run.get("identities", {})
    if (
        run.get("schema_version") != "ganesh-mini-sft-run/v2"
        or run.get("status") != "complete"
        or run.get("planned_end_row") != 900
        or run.get("state", {}).get("seen_tokens") != 651639
        or run.get("state", {}).get("optimizer_steps") != 113
        or run.get("save_reload", {}).get("passed") is not True
        or identity.get("phase") != "lr-candidate"
        or identity.get("learning_rate") != {"1e-5": "1e-05", "3e-5": "3e-05"}[learning_rate]
        or identity.get("prepared_data_sha256") != PREPARED_DATA_SHA256
        or identity.get("prepared_manifest_sha256") != PREPARED_MANIFEST_SHA256
        or identity.get("model_revision") != MODEL_REVISION
    ):
        raise ContractError(f"incomplete or mismatched {learning_rate} training evidence")
    files = run.get("adapter_files")
    if not isinstance(files, dict) or set(files) != {"README.md", "adapter_config.json", "adapter_model.safetensors"}:
        raise ContractError("completed run lacks exact final adapter inventory")
    if any(not isinstance(digest, str) or len(digest) != 64 for digest in files.values()):
        raise ContractError("invalid final adapter digest")
    return run


def _task(path: Path, task: dict[str, Any]) -> tuple[dict[str, Any], str]:
    envelope = _sealed(path, "evidence_sha256")
    if envelope.get("schema_version") != "ganesh-mini-task-evidence/v2":
        raise ContractError(f"expected raw task evidence: {path}")
    binding = envelope.get("task", {})
    result = validate_result(envelope.get("verification", {}).get("result"))
    if (
        binding.get("task_id") != task["task_id"]
        or binding.get("language") != task["language"]
        or binding.get("surface") != "development"
        or result["task_id"] != task["task_id"]
        or result["language"] != task["language"]
        or result["surface"] != "development"
        or result["prompt_sha256"] != task["prompt_sha256"]
        or result["model"] != {k: envelope.get("model", {}).get(k) for k in result["model"]}
    ):
        raise ContractError(f"task/result/manifest binding mismatch: {path}")
    if not isinstance(binding.get("task_sha256"), str) or len(binding["task_sha256"]) != 64:
        raise ContractError(f"missing source task digest: {path}")
    result["_source_task_sha256"] = binding["task_sha256"]
    return result, envelope["evidence_sha256"]


def _cohort(directory: Path, tasks: dict[str, dict[str, Any]], *, exact_files: bool) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    expected = {f"{task_id}.json" for task_id in tasks}
    if exact_files and {path.name for path in directory.glob("*.json")} != expected:
        raise ContractError(f"candidate cohort must contain exactly {len(expected)} selected task files: {directory}")
    results: dict[str, dict[str, Any]] = {}
    seals: dict[str, str] = {}
    for task_id in sorted(tasks):
        path = directory / f"{task_id}.json"
        if not path.is_file():
            raise ContractError(f"missing selected task evidence: {path}")
        results[task_id], seals[task_id] = _task(path, tasks[task_id])
    identities = {json.dumps(row["model"], sort_keys=True) for row in results.values()}
    if len(identities) != 1:
        raise ContractError(f"mixed model identities in {directory}")
    return results, seals


def _collection(rows: dict[str, dict[str, Any]]) -> str:
    return sha256_object([row["result_sha256"] for _, row in sorted(rows.items())])


def _lane_passes(rows: dict[str, dict[str, Any]]) -> dict[str, int]:
    return {lane: sum(int(row["passed"]) for row in rows.values() if row["language"] == lane) for lane in LANES}


def adjudicate(
    canary_manifest: Path, evaluation_workspace_manifest: Path, base_tasks: Path,
    low_run_path: Path, low_tasks: Path, high_run_path: Path, high_tasks: Path,
) -> dict[str, Any]:
    canary, workspace, tasks = _manifest(canary_manifest, evaluation_workspace_manifest)
    runs = {"1e-5": _run(low_run_path, "1e-5"), "3e-5": _run(high_run_path, "3e-5")}
    base, base_seals = _cohort(base_tasks, tasks, exact_files=False)
    candidates = {
        "1e-5": _cohort(low_tasks, tasks, exact_files=True),
        "3e-5": _cohort(high_tasks, tasks, exact_files=True),
    }
    base_model = next(iter(base.values()))["model"]
    if base_model["revision"] != MODEL_REVISION:
        raise ContractError("wrong upstream baseline revision")
    for learning_rate, (rows, _) in candidates.items():
        run = runs[learning_rate]
        expected_artifact = sha256_object({
            "base": base_model["artifact_sha256"],
            "adapter": run["adapter_files"],
            "run_evidence_sha256": run["evidence_sha256"],
        })
        for task_id, row in rows.items():
            baseline = base[task_id]
            if row["model"]["artifact_sha256"] != expected_artifact:
                raise ContractError(f"{learning_rate}: candidate model is not bound to completed adapter")
            if row["model"]["revision"] != base_model["revision"] or row["model"]["serving_contract_sha256"] != base_model["serving_contract_sha256"]:
                raise ContractError(f"{learning_rate}: serving contract differs from baseline")
            if row["_source_task_sha256"] != baseline["_source_task_sha256"]:
                raise ContractError(f"{learning_rate}: source task differs for {task_id}")
            if row["rendered_prompt_sha256"] != baseline["rendered_prompt_sha256"]:
                raise ContractError(f"{learning_rate}: rendered prompt differs for {task_id}")
    low_rows = candidates["1e-5"][0]
    high_rows = candidates["3e-5"][0]
    low_lanes, high_lanes = _lane_passes(low_rows), _lane_passes(high_rows)
    low_total, high_total = sum(low_lanes.values()), sum(high_lanes.values())
    higher_wins = high_total >= low_total + 1 and all(high_lanes[lane] >= low_lanes[lane] for lane in LANES)
    selected_lr = "3e-5" if higher_wins else "1e-5"
    selected_rows, selected_seals = candidates[selected_lr]
    selected_run = runs[selected_lr]
    selected_model = next(iter(selected_rows.values()))["model"]
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-canary-selection/v1",
        "status": "selected",
        "authority": "selected-candidate-180-task-development-evaluation-only",
        "rule": RULE,
        "canary_manifest_sha256": canary["manifest_sha256"],
        "evaluation_workspace_manifest_sha256": workspace["manifest_sha256"],
        "task_ids": sorted(tasks),
        "base": {"model": base_model, "passes": sum(_lane_passes(base).values()), "lanes": _lane_passes(base),
                 "result_collection_sha256": _collection(base), "task_evidence": base_seals},
        "candidates": {
            lr: {"run_evidence_sha256": runs[lr]["evidence_sha256"], "adapter_files": runs[lr]["adapter_files"],
                 "model": next(iter(rows.values()))["model"], "passes": sum(_lane_passes(rows).values()),
                 "lanes": _lane_passes(rows), "result_collection_sha256": _collection(rows),
                 "task_evidence": seals}
            for lr, (rows, seals) in candidates.items()
        },
        "selected_learning_rate": selected_lr,
        "selected_candidate": {"run_evidence_sha256": selected_run["evidence_sha256"],
                               "adapter_files": selected_run["adapter_files"], "model": selected_model,
                               "result_collection_sha256": _collection(selected_rows),
                               "task_evidence": selected_seals},
        "decision": "higher_lr_improved_without_lane_regression" if higher_wins else "conservative_lower_lr_default",
        "gate3_quality_passed": False,
        "decision_tasks_opened": 0,
    }
    report["report_sha256"] = sha256_object(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("canary_manifest", "evaluation_workspace_manifest", "base_tasks", "low_run", "low_tasks", "high_run", "high_tasks", "output"):
        parser.add_argument("--" + name.replace("_", "-"), type=Path, required=True)
    args = parser.parse_args()
    report = adjudicate(args.canary_manifest, args.evaluation_workspace_manifest, args.base_tasks,
                        args.low_run, args.low_tasks, args.high_run, args.high_tasks)
    if args.output.exists():
        raise ContractError(f"refusing to overwrite immutable adjudication: {args.output}")
    write_json(args.output, report)
    print(json.dumps({"status": report["status"], "selected_learning_rate": report["selected_learning_rate"],
                      "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
