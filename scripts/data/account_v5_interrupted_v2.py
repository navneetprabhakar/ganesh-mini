#!/usr/bin/env python3
"""Seal the exact artifact inventory of interrupted V5 attempt V2."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.account_v5_interrupted_attempt import validate_completed_semantic
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.run_repair_delta_two_phase import load_v5_semantic_dispatch


SCHEMA = "ganesh-mini-gate2-v5-v2-interruption-accounting/v1"
CONTRACT_ID = "capability-stratified-v5-interface-replay/v1"
ATTEMPT_ID = "primary-two-phase-v2"
ATTEMPT_MANIFEST_SEAL = "c1ef2bf5d9b2a92a82b8819d03ef0e3a1b467786c52ecd7a58dec936dc70238a"
INVALID_SCHEMA_FRAGMENT = "Invalid schema for response_format 'codex_output_schema'"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def artifact_binding(path: Path, artifact: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": str(path),
        "sha256": file_sha256(path),
        "artifact_sha256": artifact["artifact_sha256"],
    }


def classify_failed_run(path: Path, artifact: dict[str, Any]) -> dict[str, Any]:
    attempts = artifact.get("attempts")
    if artifact.get("status") != "invocation-failed" or not isinstance(attempts, list) or len(attempts) != 1:
        raise ValueError(f"{path}: expected one sealed invocation failure")
    attempt = attempts[0]
    run = attempt.get("run")
    if not isinstance(run, dict):
        raise ValueError(f"{path}: missing failed run evidence")
    claimed = attempt.get("run_evidence_sha256")
    if claimed != canonical_sha256(run):
        raise ValueError(f"{path}: invalid run evidence seal")
    stdout = run.get("stdout_jsonl")
    if not isinstance(stdout, str):
        raise ValueError(f"{path}: missing stdout evidence")
    common = {
        "candidate_id": artifact.get("candidate_id"),
        "stage": artifact.get("stage"),
        "input_sha256": artifact.get("input_sha256"),
        "prompt_sha256": artifact.get("prompt_sha256"),
        "run_evidence_sha256": claimed,
        "structured_model_response_observed": attempt.get("structured_model_response_observed"),
        "usage": run.get("usage"),
        "artifact": artifact_binding(path, artifact),
    }
    if artifact.get("stage") == "test_author":
        if (
            INVALID_SCHEMA_FRAGMENT not in stdout
            or "invalid_json_schema" not in stdout
            or '"status": 400' not in stdout.replace('\\"', '"')
            or run.get("returncode") != 1
            or run.get("timed_out") is not False
            or attempt.get("structured_model_response_observed") is not False
            or run.get("usage") is not None
            or run.get("final_output") != ""
        ):
            raise ValueError(f"{path}: test-author failure is not the evidenced pre-inference schema rejection")
        return {**common, "classification": "provider-400-invalid_json_schema-pre-inference"}
    if artifact.get("stage") == "semantic_review":
        if (
            "invalid_json_schema" in stdout
            or run.get("returncode") != 1
            or attempt.get("structured_model_response_observed") is not False
            or run.get("usage") is not None
            or run.get("final_output") != ""
            or not any(event.get("type") == "turn.started" for event in run.get("events", []) if isinstance(event, dict))
            or any(event.get("type") in {"turn.completed", "turn.failed", "error"}
                   for event in run.get("events", []) if isinstance(event, dict))
        ):
            raise ValueError(f"{path}: semantic failure is not the evidenced operator-stop interruption")
        return {**common, "classification": "uncommitted-at-operator-stop"}
    raise ValueError(f"{path}: unexpected failed stage")


def build(args: argparse.Namespace) -> dict[str, Any]:
    attempt = load_sealed(args.attempt_manifest, "manifest_sha256")
    if (
        attempt.get("manifest_sha256") != ATTEMPT_MANIFEST_SEAL
        or attempt.get("attempt_id") != ATTEMPT_ID
        or attempt.get("contract_id") != CONTRACT_ID
        or attempt.get("records") != 60
        or attempt.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("V2 attempt manifest identity differs")
    execution = load_sealed(args.execution_manifest, "manifest_sha256")
    generated = read_jsonl(args.candidates)
    assignment_rows = read_jsonl(args.assignments)
    assignments = {row["id"]: row for row in assignment_rows}
    ordered_ids = execution.get("ordered_candidate_ids")
    by_id = {row["candidate"]["id"]: row["candidate"] for row in generated}
    actual_ids = [row["candidate"]["id"] for row in generated]
    if (
        execution.get("manifest_sha256") != attempt.get("execution_manifest_sha256")
        or actual_ids != ordered_ids
        or len(actual_ids) != 60
        or len(set(actual_ids)) != 60
        or set(assignments) != set(actual_ids)
    ):
        raise ValueError("V2 does not bind the frozen exact ordered 60")
    prior_semantics, required_semantics = load_v5_semantic_dispatch(
        args.semantic_equivalence, generated, assignments,
    )
    carry = load_sealed(args.semantic_carry_manifest, "manifest_sha256")
    carry_ids = {row["candidate_id"] for row in carry.get("rows", [])}
    if (
        len(prior_semantics) != 37
        or len(required_semantics) != 23
        or len(carry_ids) != 3
        or not carry_ids <= required_semantics
        or attempt.get("semantic_carry_manifest_sha256") != carry.get("manifest_sha256")
    ):
        raise ValueError("V2 starting semantic partition differs")

    config = json.loads(args.codex_config.read_text(encoding="utf-8"))
    cli_identity = f"codex-cli {config.get('codex_cli_version')}"
    successful: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    stage_paths = sorted(args.run_dir.glob("*.json"))
    for path in stage_paths:
        artifact = load_sealed(path, "artifact_sha256")
        candidate_id = artifact.get("candidate_id")
        if candidate_id not in by_id:
            raise ValueError(f"{path}: candidate is outside the frozen cohort")
        if artifact.get("schema_version") == "ganesh-mini-repair-delta-codex-stage/v1":
            if artifact.get("stage") != "semantic_review":
                raise ValueError(f"{path}: unexpected completed stage")
            completed = validate_completed_semantic(
                path, by_id[candidate_id], assignments[candidate_id], config, cli_identity,
            )
            successful.append({**completed, "stage": "semantic_review", "classification": "completed-structured-response"})
        elif artifact.get("schema_version") == "ganesh-mini-repair-delta-v5-stage-invocation-failure/v1":
            failed.append(classify_failed_run(path, artifact))
        else:
            raise ValueError(f"{path}: unknown stage artifact schema")
    if len(stage_paths) != 14 or len(successful) != 2 or len(failed) != 12:
        raise ValueError("V2 stage artifact cardinality differs from the interrupted attempt")
    if sum(row["classification"] == "provider-400-invalid_json_schema-pre-inference" for row in failed) != 11:
        raise ValueError("V2 must contain exactly eleven pre-inference schema rejections")
    if sum(row["classification"] == "uncommitted-at-operator-stop" for row in failed) != 1:
        raise ValueError("V2 must contain exactly one operator-stop semantic interruption")

    pre_rows = []
    for path in sorted(args.pre_separation_dir.glob("*.json")):
        artifact = load_sealed(path, "artifact_sha256")
        if (
            artifact.get("status") != "unresolved"
            or artifact.get("candidate_id") not in by_id
            or artifact.get("evaluation_artifacts_read") != 0
        ):
            raise ValueError(f"{path}: invalid pre-separation interruption wrapper")
        pre_rows.append({
            "candidate_id": artifact["candidate_id"],
            "cell_id": artifact["cell_id"],
            "terminal_stage": artifact["terminal_stage"],
            "status": artifact["status"],
            "artifact": artifact_binding(path, artifact),
        })
    if len(pre_rows) != 12 or len({row["candidate_id"] for row in pre_rows}) != 12:
        raise ValueError("V2 pre-separation interruption wrapper cardinality differs")
    materialized = {row["candidate_id"] for row in pre_rows}
    if materialized != {row["candidate_id"] for row in failed}:
        raise ValueError("V2 stage failures and pre-separation wrappers do not reconcile")

    success_ids = {row["candidate_id"] for row in successful}
    if success_ids & (set(prior_semantics) | carry_ids):
        raise ValueError("V2 completed semantic calls duplicate a prior semantic carry")
    completed_semantic_ids = set(prior_semantics) | carry_ids | success_ids
    remaining_semantic_ids = [identifier for identifier in ordered_ids if identifier not in completed_semantic_ids]
    if len(completed_semantic_ids) != 42 or len(remaining_semantic_ids) != 18:
        raise ValueError("V2 semantic carry accounting does not equal 42 completed plus 18 remaining")

    report: dict[str, Any] = {
        "schema_version": SCHEMA,
        "status": "interrupted-incomplete-no-qualification-metrics",
        "contract_id": CONTRACT_ID,
        "attempt_id": ATTEMPT_ID,
        "inputs": {
            "attempt_manifest": {"path": str(args.attempt_manifest), "sha256": file_sha256(args.attempt_manifest),
                                 "manifest_sha256": attempt["manifest_sha256"]},
            "execution_manifest": {"path": str(args.execution_manifest), "sha256": file_sha256(args.execution_manifest),
                                   "manifest_sha256": execution["manifest_sha256"]},
            "semantic_carry_manifest": {"path": str(args.semantic_carry_manifest),
                                        "sha256": file_sha256(args.semantic_carry_manifest),
                                        "manifest_sha256": carry["manifest_sha256"]},
            "codex_config": {"path": str(args.codex_config), "sha256": file_sha256(args.codex_config),
                             "config_sha256": canonical_sha256(config)},
        },
        "frozen_cohort": {
            "records": 60,
            "ordered_candidate_ids_sha256": execution["ordered_candidate_ids_sha256"],
            "changed": False,
        },
        "artifact_inventory": {
            "attempt_manifests": 2,
            "stage_run_artifacts": len(stage_paths),
            "pre_separation_artifacts": len(pre_rows),
            "post_test_cohort_artifacts": 0,
            "separation_artifacts": 0,
            "executable_result_artifacts": 0,
            "admission_artifacts": 0,
            "qualification_artifacts": 0,
            "stage_runs": sorted(successful + failed, key=lambda row: (
                ordered_ids.index(row["candidate_id"]), row.get("stage", "semantic_review")
            )),
            "pre_separation": sorted(pre_rows, key=lambda row: ordered_ids.index(row["candidate_id"])),
        },
        "attempt_accounting": {
            "materialized_pre_separation_candidates": 12,
            "not_materialized_pre_separation_candidates": 48,
            "attempt_local_unresolved_wrappers": 12,
            "rejected_candidates": 0,
            "admitted_candidates": 0,
            "provider_400_invalid_json_schema_pre_inference": 11,
            "uncommitted_at_operator_stop": 1,
            "successful_structured_responses": 2,
            "successful_test_author_responses": 0,
            "delta_audit_responses": 0,
            "qualification_metrics_available": False,
        },
        "carry_proposal": {
            "prior_v4_equivalent_semantics": 37,
            "prior_v1_completed_semantics": 3,
            "v2_completed_semantics": 2,
            "total_completed_semantics": 42,
            "remaining_semantic_calls": 18,
            "test_author_carries": 0,
            "v2_completed_semantic_rows": successful,
            "remaining_semantic_candidate_ids": remaining_semantic_ids,
            "rule": (
                "Carry only the 42 sealed completed semantic results after exact-input validation. "
                "The eleven provider schema rejections contain no structured response or usage and carry no "
                "test-author result. The operator-stopped semantic attempt is uncommitted and carries no response."
            ),
        },
        "classification": (
            "This is interrupted construction evidence, not candidate qualification and not a training/model result. "
            "Provider 400 schema rejection is classified separately from the operator-stopped semantic call."
        ),
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--attempt-manifest", type=Path, required=True)
    parser.add_argument("--execution-manifest", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--assignments", type=Path, required=True)
    parser.add_argument("--semantic-equivalence", type=Path, required=True)
    parser.add_argument("--semantic-carry-manifest", type=Path, required=True)
    parser.add_argument("--codex-config", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--pre-separation-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    report = build(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
