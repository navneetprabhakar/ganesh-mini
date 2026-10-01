#!/usr/bin/env python3
"""Account for an interrupted V5 attempt without reconstructing outcomes."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.run_repair_delta_evidence import (
    SEMANTIC_BOOLEANS, _stage_prompt, semantic_projection,
)
from scripts.data.run_repair_delta_two_phase import load_v5_semantic_dispatch
from scripts.eval.contracts import sha256_text


SCHEMA = "ganesh-mini-gate2-v5-interruption-accounting/v1"
CONTRACT_ID = "capability-stratified-v5-interface-replay/v1"
PLAN_SHA256 = "132501466e58e88b6aaebc412aac37e561b103ae8df8f50a9ac43d3aab7cc04b"
SOURCE_ADDENDUM_SHA256 = "01a8415fa9122f163aa58f5cf6578bb1ff2502346cb197a11af14b373d922da3"
BUDGET_ADDENDUM_SHA256 = "1933b409b656ab90cf4a82e44b0b2b7dc29d4701d3a162add64db179319a4899"
STAGE_SCHEMA = "ganesh-mini-repair-delta-codex-stage/v1"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value); claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field}")
    return value


def validate_completed_semantic(
    path: Path, candidate: dict[str, Any], assignment: dict[str, Any],
    config: dict[str, Any], cli_identity: str,
) -> dict[str, Any]:
    artifact = load_sealed(path, "artifact_sha256")
    projection = semantic_projection(candidate, assignment)
    prompt = _stage_prompt("semantic_review", projection, "v5")
    input_sha = canonical_sha256({
        "stage": "semantic_review", "projection": projection,
        "prompt": prompt, "contract_version": "v5",
    })
    response = artifact.get("response")
    run = artifact.get("run")
    if (
        artifact.get("schema_version") != STAGE_SCHEMA
        or artifact.get("stage") != "semantic_review"
        or artifact.get("contract_version") != "v5"
        or artifact.get("candidate_id") != candidate.get("id")
        or artifact.get("input_sha256") != input_sha
        or artifact.get("prompt_sha256") != sha256_text(prompt)
        or artifact.get("config_sha256") != canonical_sha256(config)
        or artifact.get("cli_identity") != cli_identity
        or artifact.get("evaluation_artifacts_read") != 0
        or not isinstance(response, dict)
        or set(response) != {*SEMANTIC_BOOLEANS, "rationale"}
        or any(type(response.get(field)) is not bool for field in SEMANTIC_BOOLEANS)
        or not isinstance(response.get("rationale"), str) or not response["rationale"].strip()
        or not isinstance(run, dict)
    ):
        raise ValueError(f"{path}: semantic stage identity, input, or response differs")
    run_body = dict(run); run_claimed = run_body.pop("run_evidence_sha256", None)
    if (
        run_claimed != canonical_sha256(run_body)
        or run.get("returncode") != 0 or run.get("timed_out") is not False
        or run.get("event_parse_error") is not None
        or run.get("disallowed_tool_item_types") != []
        or run.get("prompt") != prompt or run.get("prompt_sha256") != sha256_text(prompt)
        or run.get("final_output_sha256") != sha256_text(run.get("final_output", ""))
        or not isinstance(run.get("events"), list)
        or not any(event.get("type") == "turn.completed" for event in run["events"] if isinstance(event, dict))
    ):
        raise ValueError(f"{path}: semantic run is incomplete, failed, or unsealed")
    return {
        "candidate_id": candidate["id"], "cell_id": assignment["cell_id"],
        "stage_artifact": {"path": str(path), "sha256": file_sha256(path),
                           "artifact_sha256": artifact["artifact_sha256"]},
        "input_sha256": input_sha, "prompt_sha256": artifact["prompt_sha256"],
        "run_evidence_sha256": run_claimed,
        "response_sha256": canonical_sha256(response),
        "all_six_semantic_booleans_true": all(response[field] is True for field in SEMANTIC_BOOLEANS),
        "carry_eligible": True,
    }


def build(args: argparse.Namespace) -> dict[str, Any]:
    for path, expected, label in (
        (args.plan, PLAN_SHA256, "base plan"),
        (args.source_addendum, SOURCE_ADDENDUM_SHA256, "source addendum"),
        (args.budget_addendum, BUDGET_ADDENDUM_SHA256, "budget addendum"),
    ):
        if file_sha256(path) != expected:
            raise ValueError(f"V5 {label} hash differs")
    manifest = load_sealed(args.execution_manifest, "manifest_sha256")
    if (
        manifest.get("contract_id") != CONTRACT_ID
        or manifest.get("plan_sha256") != PLAN_SHA256
        or manifest.get("budget_clarification_addendum_sha256") != BUDGET_ADDENDUM_SHA256
        or manifest.get("records") != 60
        or manifest.get("immutable_carries") != 58
        or manifest.get("fresh_teacher_primaries") != 2
        or manifest.get("evaluation_artifacts_read") != 0
        or manifest.get("candidate_output", {}).get("sha256") != file_sha256(args.candidates)
        or manifest.get("assignment_output", {}).get("sha256") != file_sha256(args.assignments)
    ):
        raise ValueError("V5 execution cohort manifest identity or input bindings differ")
    generated = read_jsonl(args.candidates)
    assignments_list = read_jsonl(args.assignments)
    assignments = {row.get("id"): row for row in assignments_list}
    ordered_ids = manifest.get("ordered_candidate_ids")
    actual_ids = [row.get("candidate", {}).get("id") for row in generated]
    if (
        actual_ids != ordered_ids or len(actual_ids) != 60 or len(set(actual_ids)) != 60
        or set(assignments) != set(actual_ids)
    ):
        raise ValueError("V5 execution inputs do not preserve the exact ordered 60 cohort")
    _, required = load_v5_semantic_dispatch(args.semantic_equivalence, generated, assignments)
    config = json.loads(args.codex_config.read_text(encoding="utf-8"))
    cli_identity = f"codex-cli {config.get('codex_cli_version')}"
    by_id = {row["candidate"]["id"]: row["candidate"] for row in generated}
    files = sorted(args.run_dir.glob("*.semantic_review.json"))
    completed = []
    seen: set[str] = set()
    for path in files:
        raw = json.loads(path.read_text(encoding="utf-8"))
        identifier = raw.get("candidate_id") if isinstance(raw, dict) else None
        if identifier not in required or identifier in seen:
            raise ValueError(f"{path}: artifact is duplicated or not one of the 23 required reviews")
        seen.add(identifier)
        completed.append(validate_completed_semantic(
            path, by_id[identifier], assignments[identifier], config, cli_identity,
        ))
    unexpected = sorted(
        str(path) for path in args.run_dir.iterdir()
        if path.is_file() and path not in files
    )
    if unexpected:
        raise ValueError("interrupted attempt contains unexpected unaccounted stage files")
    absent = [identifier for identifier in ordered_ids if identifier in required and identifier not in seen]
    report: dict[str, Any] = {
        "schema_version": SCHEMA, "status": "interrupted-incomplete-no-candidate-dispositions",
        "contract_id": CONTRACT_ID, "plan_sha256": PLAN_SHA256,
        "source_feasibility_addendum_sha256": SOURCE_ADDENDUM_SHA256,
        "budget_clarification_addendum_sha256": BUDGET_ADDENDUM_SHA256,
        "inputs": {
            "execution_manifest": {"path": str(args.execution_manifest),
                                   "sha256": file_sha256(args.execution_manifest),
                                   "manifest_sha256": manifest["manifest_sha256"]},
            "semantic_equivalence": {"path": str(args.semantic_equivalence),
                                     "sha256": file_sha256(args.semantic_equivalence)},
            "codex_config": {"path": str(args.codex_config), "sha256": file_sha256(args.codex_config),
                             "config_sha256": canonical_sha256(config)},
            "run_directory": str(args.run_dir),
        },
        "frozen_cohort": {"records": 60, "immutable_carries": 58, "fresh_teacher_primaries": 2,
                          "ordered_candidate_ids_sha256": manifest["ordered_candidate_ids_sha256"],
                          "changed": False},
        "interruption": {
            "cause": "unknown-not-evidenced", "candidate_outcomes_available": 0,
            "qualification_metrics_available": False,
            "pre_separation_artifacts_available": 0,
            "test_author_artifacts_available": 0, "delta_audit_artifacts_available": 0,
        },
        "semantic_review_accounting": {
            "carried_v4_equivalences": 37, "new_reviews_required": 23,
            "completed_new_review_artifacts": len(completed),
            "absent_new_review_artifacts": len(absent),
            "completed": completed, "absent_candidate_ids": absent,
            "completed_artifacts_may_be_reused": len(completed),
            "remaining_new_calls": len(absent),
        },
        "classification": (
            "Only sealed completed stage artifacts are evidence. Missing artifacts are uncommitted work, "
            "not failures, rejections, unresolved candidates, or reconstructed metrics."
        ),
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--source-addendum", type=Path, required=True)
    parser.add_argument("--budget-addendum", type=Path, required=True)
    parser.add_argument("--execution-manifest", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--assignments", type=Path, required=True)
    parser.add_argument("--semantic-equivalence", type=Path, required=True)
    parser.add_argument("--codex-config", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    report = build(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "report_sha256": report["report_sha256"],
                      "completed": report["semantic_review_accounting"]["completed_new_review_artifacts"]},
                     sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
