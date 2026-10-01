#!/usr/bin/env python3
"""Adjudicate selected Gate 3 capability pilot on all 180 development tasks.

This evaluates the frozen executable quality criteria. It does not open the
private decision set or claim a complete Gate 3 admission/release seal.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.eval.adjudicate_gate3_capability_canary import (
    CANARY_MANIFEST_SHA256, EVALUATION_WORKSPACE_SHA256, LANES, _cohort, _run, _sealed, _sha256_file,
)
from scripts.eval.contracts import ContractError, sha256_object, write_json
from scripts.eval.score import compare


FAMILIES = ("go", "java", "javascript_typescript", "python", "rust")


def _development_tasks(workspace: dict[str, Any], workspace_root: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for item in workspace.get("files", []):
        relative = item.get("path", "")
        if not (relative.startswith("eval/private/development/tranche") and relative.endswith(".task.json")):
            continue
        path = workspace_root / relative
        if not path.is_file() or _sha256_file(path) != item.get("sha256"):
            raise ContractError(f"development task differs from sealed workspace: {relative}")
        task = json.loads(path.read_text(encoding="utf-8"))
        task_id = task.get("task_id")
        if (
            not isinstance(task_id, str) or task_id in rows or task.get("surface") != "development"
            or task.get("language") not in LANES or task.get("prompt", {}).get("sha256") is None
        ):
            raise ContractError(f"invalid development task: {relative}")
        rows[task_id] = {"task_id": task_id, "language": task["language"],
                         "prompt_sha256": task["prompt"]["sha256"]}
    if len(rows) != 180 or any(sum(item["language"] == lane for item in rows.values()) != 30 for lane in LANES):
        raise ContractError("workspace must bind exactly 30 tasks per lane, 180 total")
    return rows


def adjudicate(
    selection_path: Path, workspace_path: Path, workspace_root: Path,
    selected_run_path: Path, base_admission_path: Path, base_run_path: Path,
    base_dir: Path, candidate_dir: Path,
) -> dict[str, Any]:
    selection = _sealed(selection_path, "report_sha256")
    workspace = _sealed(workspace_path, "manifest_sha256")
    if (
        selection.get("schema_version") != "ganesh-mini-capability-canary-selection/v1"
        or selection.get("status") != "selected"
        or selection.get("authority") != "selected-candidate-180-task-development-evaluation-only"
        or selection.get("gate3_quality_passed") is not False
        or selection.get("decision_tasks_opened") != 0
        or selection.get("evaluation_workspace_manifest_sha256") != workspace["manifest_sha256"]
        or selection.get("canary_manifest_sha256") != CANARY_MANIFEST_SHA256
        or workspace["manifest_sha256"] != EVALUATION_WORKSPACE_SHA256
        or workspace.get("schema_version") != "ganesh-mini-development-evaluation-workspace/v1"
        or workspace.get("status") != "sealed"
    ):
        raise ContractError("development adjudication requires sealed canary selection and same evaluation workspace")
    lr = selection.get("selected_learning_rate")
    if lr not in ("1e-5", "3e-5"):
        raise ContractError("invalid selected learning rate")
    run = _run(selected_run_path, lr)
    selected = selection.get("selected_candidate", {})
    chosen_summary = selection.get("candidates", {}).get(lr, {})
    for field in ("run_evidence_sha256", "adapter_files", "model", "result_collection_sha256", "task_evidence"):
        if selected.get(field) != chosen_summary.get(field):
            raise ContractError(f"selected canary binding differs from {lr} candidate summary: {field}")
    if selected.get("run_evidence_sha256") != run["evidence_sha256"] or selected.get("adapter_files") != run["adapter_files"]:
        raise ContractError("selected adapter differs from completed training evidence")
    tasks = _development_tasks(workspace, workspace_root)
    if not set(selection.get("task_ids", [])) <= set(tasks) or len(selection["task_ids"]) != 30:
        raise ContractError("selected canary tasks not part of the 180-task development surface")
    base, base_seals = _cohort(base_dir, tasks, exact_files=False)
    candidate, candidate_seals = _cohort(candidate_dir, tasks, exact_files=True)
    base_admission = _sealed(base_admission_path, "evidence_sha256")
    base_run = _sealed(base_run_path, "run_sha256")
    if (
        base_admission.get("schema_version") != "ganesh-mini-gate1-baseline-admission/v1"
        or base_admission.get("status") != "admitted"
        or base_admission.get("baseline_run_sha256") != base_run["run_sha256"]
        or base_run.get("schema_version") != "ganesh-mini-inference-run/v2"
        or base_run.get("task_accounting", {}).get("completed") != 180
        or base_run.get("task_accounting", {}).get("expected") != 180
        or base_run.get("task_accounting", {}).get("pending") != 0
    ):
        raise ContractError("exact admitted Gate 1 base 180-run binding is absent")
    run_tasks = {item.get("task_id"): item for item in base_run.get("tasks", []) if isinstance(item, dict)}
    if set(run_tasks) != set(tasks) or len(base_run.get("tasks", [])) != 180:
        raise ContractError("Gate 1 base run does not cover exactly the frozen 180 tasks")
    if any(run_tasks[task_id].get("evidence_sha256") != base_seals[task_id] or run_tasks[task_id].get("status") != "complete"
           for task_id in tasks):
        raise ContractError("base task evidence differs from admitted Gate 1 run")
    expected_model = selected.get("model")
    if not isinstance(expected_model, dict) or {json.dumps(row["model"], sort_keys=True) for row in candidate.values()} != {json.dumps(expected_model, sort_keys=True)}:
        raise ContractError("180-task candidate model differs from selected canary model")
    base_model = next(iter(base.values()))["model"]
    if any(base_run.get("model", {}).get(key) != value for key, value in base_model.items()):
        raise ContractError("base model differs from admitted Gate 1 run")
    expected_artifact = sha256_object({"base": base_model["artifact_sha256"], "adapter": run["adapter_files"],
                                      "run_evidence_sha256": run["evidence_sha256"]})
    if expected_model.get("artifact_sha256") != expected_artifact:
        raise ContractError("development model is not bound to selected adapter")
    for task_id, row in candidate.items():
        baseline = base[task_id]
        if (row["_source_task_sha256"] != baseline["_source_task_sha256"]
                or row["rendered_prompt_sha256"] != baseline["rendered_prompt_sha256"]
                or row["model"]["revision"] != baseline["model"]["revision"]
                or row["model"]["serving_contract_sha256"] != baseline["model"]["serving_contract_sha256"]):
            raise ContractError(f"development task or serving binding differs for {task_id}")
    paired = compare(list(base.values()), list(candidate.values()))
    base_metrics, cand_metrics = paired["base"], paired["candidate"]
    families_improved = [family for family in FAMILIES
                         if cand_metrics["families"][family]["decimal"] > base_metrics["families"][family]["decimal"]]
    lane_regressions = [lane for lane in LANES
                        if cand_metrics["lanes"][lane]["passed"] < base_metrics["lanes"][lane]["passed"]]
    quality = {key: {"base": base_metrics["quality_failures"][key], "candidate": cand_metrics["quality_failures"][key]}
               for key in ("malformed", "repetitive", "truncated", "non_code")}
    checks = {
        "minimum_four_improved_product_families": len(families_improved) >= 4,
        "zero_lane_pass_regression": not lane_regressions,
        "no_output_quality_increase": all(item["candidate"] <= item["base"] for item in quality.values()),
        "selected_adapter_save_reload": run["save_reload"]["passed"] is True,
        "decision_surface_closed": selection["decision_tasks_opened"] == 0,
    }
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-development-adjudication/v1",
        "status": "quality-criteria-passed" if all(checks.values()) else "quality-criteria-failed",
        "gate3_sealed": False,
        "decision_tasks_opened": 0,
        "selection_report_sha256": selection["report_sha256"],
        "gate1_baseline_admission_sha256": base_admission["evidence_sha256"],
        "gate1_baseline_run_sha256": base_run["run_sha256"],
        "evaluation_workspace_manifest_sha256": workspace["manifest_sha256"],
        "selected_learning_rate": lr,
        "selected_run_evidence_sha256": run["evidence_sha256"],
        "selected_model": expected_model,
        "task_count": len(tasks),
        "task_ids": sorted(tasks),
        "base_task_evidence": base_seals,
        "candidate_task_evidence": candidate_seals,
        "paired_report_sha256": paired["report_sha256"],
        "base": base_metrics,
        "candidate": cand_metrics,
        "paired_transitions": paired["paired"],
        "families_improved": families_improved,
        "lane_regressions": lane_regressions,
        "output_quality": quality,
        "checks": checks,
        "failed_checks": [name for name, passed in checks.items() if not passed],
    }
    report["report_sha256"] = sha256_object(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("selection", "evaluation_workspace_manifest", "evaluation_workspace_root", "selected_run", "base_admission", "base_run", "base_tasks", "candidate_tasks", "output"):
        parser.add_argument("--" + name.replace("_", "-"), type=Path, required=True)
    args = parser.parse_args()
    report = adjudicate(args.selection, args.evaluation_workspace_manifest, args.evaluation_workspace_root,
                        args.selected_run, args.base_admission, args.base_run, args.base_tasks, args.candidate_tasks)
    if args.output.exists():
        raise ContractError(f"refusing to overwrite immutable adjudication: {args.output}")
    write_json(args.output, report)
    print(json.dumps({"status": report["status"], "failed_checks": report["failed_checks"],
                      "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] == "quality-criteria-passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
