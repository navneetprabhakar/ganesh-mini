#!/usr/bin/env python3
"""Attach V7 first-pass tests and run the exact 60 fresh blind delta audits."""

from __future__ import annotations

import argparse
import concurrent.futures
import copy
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.generate_expansion_qualification import verify_codex_version
from scripts.data.repair_delta_v7_readiness import CONTRACT_ID
from scripts.data.run_repair_delta_evidence import (
    IsolatedCodexAdapter, StageInvocationFailure, _delta_evidence, delta_projection,
)
from scripts.eval.contracts import sha256_text


def _sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value); claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field}")
    return value


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _attach(candidate: dict[str, Any], terminal: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate = copy.deepcopy(candidate)
    support = [row for row in candidate["verification_task"]["files"] if row.get("role") == "support"]
    files, roles = [], []
    for row in terminal["injection"]["roles"]:
        content = row["content"].rstrip() + "\n"
        digest = sha256_text(content)
        files.append({"path": row["logical_path"], "role": "test", "content": content, "sha256": digest})
        roles.append({
            "path": row["logical_path"], "canonical_path": row["canonical_execution_path"],
            "file_sha256": digest, "role": row["role"], "case_ids": row["case_ids"],
            "valid_domain_only": row["role"] == "primary_discrimination",
            "scheduled_dimension_only": row["role"] == "cross_cutting",
        })
    candidate["verification_task"]["files"] = [*support, *files]
    evidence = {
        "schema_version": "ganesh-mini-gate2-v7-test-author-evidence/v1",
        "candidate_sha256": canonical_sha256(candidate),
        "pre_test_candidate_sha256": terminal["injection"]["roles"][0].get("candidate_sha256"),
        "raw_response_sha256": terminal["response_sha256"],
        "test_author_run_evidence_sha256": terminal["run_evidence_sha256"],
        "injection_sha256": terminal["injection"]["injection_sha256"],
        "test_roles": roles,
        "visibility": {
            "reference_visible": False, "teacher_proof_visible": False,
            "semantic_review_visible": False, "verifier_outputs_visible": False,
            "evaluation_artifacts_read": 0,
        },
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    return candidate, evidence


def run(args: argparse.Namespace) -> dict[str, Any]:
    first = _sealed(args.first_pass_report, "report_sha256")
    terminal = _jsonl(args.first_pass_terminal)
    generated = _jsonl(args.candidates)
    assignments = _jsonl(args.assignments)
    if (
        first.get("contract_id") != CONTRACT_ID
        or first.get("status") != "passed-first-pass-thresholds"
        or first.get("thresholds", {}).get("direct_final_stage_eligible") is not True
        or len(terminal) != len(generated) != 60
    ):
        raise ValueError("V7 first pass is not exact, clean, and direct-stage eligible")
    if not (len(terminal) == len(generated) == len(assignments) == 60):
        raise ValueError("V7 delta inputs are not exact 60")
    attached, test_evidence = [], []
    for raw, assignment, terminal_row in zip(generated, assignments, terminal, strict=True):
        candidate = raw["candidate"]
        if candidate["id"] != assignment["id"] or candidate["id"] != terminal_row["candidate_id"] or terminal_row["status"] != "structurally-valid":
            raise ValueError("V7 delta input identity/order drift")
        updated, evidence = _attach(candidate, terminal_row)
        attached.append(updated); test_evidence.append(evidence)

    config = json.loads(args.codex_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    projections = [delta_projection(candidate, assignment) for candidate, assignment in zip(attached, assignments, strict=True)]

    def invoke(index: int) -> tuple[int, dict[str, Any] | StageInvocationFailure]:
        adapter = IsolatedCodexAdapter("delta_audit", config, args.codex_bin, args.run_dir, cli_identity, "v7")
        try:
            return index, adapter(projections[index])
        except StageInvocationFailure as exc:
            return index, exc

    outcomes: list[dict[str, Any] | StageInvocationFailure | None] = [None] * 60
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        for index, value in executor.map(invoke, range(60)):
            outcomes[index] = value

    rows = []
    for ordinal, (candidate, assignment, projection, outcome) in enumerate(zip(attached, assignments, projections, outcomes, strict=True)):
        base = {"ordinal": ordinal, "candidate_id": candidate["id"], "cell_id": assignment["cell_id"], "projection_sha256": canonical_sha256(projection), "evaluation_artifacts_read": 0}
        if isinstance(outcome, StageInvocationFailure):
            row = {**base, "status": "invocation-failed", "reason": str(outcome), "invocation_artifact_sha256": outcome.evidence["artifact_sha256"]}
        else:
            assert isinstance(outcome, dict)
            response = dict(outcome); run_sha = response.pop("_run_sha256")
            try:
                evidence = _delta_evidence(candidate, assignment, response, run_sha)
                passed = (
                    evidence["independent_semantic_delta_count"] == 1
                    and evidence["delta_is_capability_specific"] is True
                    and evidence["introduces_multiple_independent_fixes"] is False
                )
                row = {**base, "status": "passed" if passed else "semantic-rejected", "delta_evidence": evidence}
            except (TypeError, ValueError) as exc:
                row = {**base, "status": "response-contract-rejected", "reason": str(exc)}
        row["artifact_sha256"] = canonical_sha256(row)
        rows.append(row)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    report = {
        "schema_version": "ganesh-mini-gate2-v7-delta-audit-report/v1",
        "contract_id": CONTRACT_ID,
        "status": "passed" if counts == {"passed": 60} else "failed",
        "first_pass_report_sha256": first["report_sha256"],
        "calls": 60, "counts": counts,
        "rows_sha256": canonical_sha256(rows),
        "attached_candidates_sha256": canonical_sha256(attached),
        "test_author_evidence_sha256": canonical_sha256(test_evidence),
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, values in (("attached-candidates.jsonl", attached), ("test-author-evidence.jsonl", test_evidence), ("delta-terminal-artifacts.jsonl", rows)):
        (args.output_dir / name).write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in values), encoding="utf-8")
    (args.output_dir / "delta-audit-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first-pass-report", type=Path, required=True)
    parser.add_argument("--first-pass-terminal", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--assignments", type=Path, required=True)
    parser.add_argument("--codex-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()
    report = run(args)
    print(json.dumps({"status": report["status"], "counts": report["counts"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
