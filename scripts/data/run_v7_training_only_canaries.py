#!/usr/bin/env python3
"""Run six fresh V7 training-only model-authored canaries and exact matrices."""

from __future__ import annotations

import argparse
import concurrent.futures
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.generate_expansion_qualification import verify_codex_version
from scripts.data.repair_delta_v7_readiness import (
    CANONICAL_LANE_INTERFACES, CONTRACT_ID, inject_controller_paths,
    test_author_projection, validate_lane_interface, validate_response,
)
from scripts.data.run_repair_delta_evidence import IsolatedCodexAdapter, _executable_evidence
from scripts.eval.contracts import sha256_text
from scripts.verify.sandbox import verify


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
EXPECTED = {
    "reference.primary_discrimination": "pass",
    "reference.cross_cutting": "pass",
    "known_bad.primary_discrimination": "fail",
    "known_bad.cross_cutting": "pass",
}


def _outcomes(executable: dict[str, Any]) -> dict[str, str]:
    return {
        f"{implementation}.{role}": (
            "pass" if executable["results"][implementation][role].get("exit_codes")
            and all(code == 0 for code in executable["results"][implementation][role]["exit_codes"])
            else "fail"
        )
        for implementation in ("reference", "known_bad")
        for role in ("primary_discrimination", "cross_cutting")
    }


def _attach(candidate: dict[str, Any], response: dict[str, Any], run_sha: str) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate = copy.deepcopy(candidate)
    lane = candidate["lane"]
    injected = inject_controller_paths(lane, response)
    support = [row for row in candidate["verification_task"]["files"] if row.get("role") == "support"]
    files = []
    roles = []
    for row in injected["roles"]:
        findings = validate_lane_interface(lane, row["content"])
        if findings:
            raise ValueError(f"{lane}/{row['role']}: static interface findings: {findings}")
        content = row["content"].rstrip() + "\n"
        logical_path = row["logical_path"]
        digest = sha256_text(content)
        files.append({"path": logical_path, "role": "test", "content": content, "sha256": digest})
        roles.append({
            "path": logical_path,
            "canonical_path": row["canonical_execution_path"],
            "file_sha256": digest,
            "role": row["role"],
            "case_ids": row["case_ids"],
        })
    candidate["verification_task"]["files"] = [*support, *files]
    evidence = {
        "schema_version": "ganesh-mini-gate2-v7-canary-test-author/v1",
        "candidate_sha256": canonical_sha256(candidate),
        "test_author_run_evidence_sha256": run_sha,
        "injection_sha256": injected["injection_sha256"],
        "test_roles": roles,
        "evaluation_artifacts_read": 0,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    return candidate, evidence


def build_report(
    bundle: dict[str, Any], config: dict[str, Any], cli_identity: str,
    run_dir: Path, runtime_path: Path, plan_sha256: str,
) -> dict[str, Any]:
    positives = [row for row in bundle["fixtures"] if row.get("expected") == "admitted"]
    by_lane = {row["envelope"]["candidate"]["lane"]: row for row in positives}
    if set(by_lane) != set(LANES):
        raise ValueError("canary source lacks exact six-lane training-only coverage")

    projections: dict[str, dict[str, Any]] = {}
    candidates: dict[str, dict[str, Any]] = {}
    for lane in LANES:
        fixture = by_lane[lane]
        candidate = copy.deepcopy(fixture["envelope"]["candidate"])
        candidate["id"] = f"v7-training-only-canary-{lane}"
        candidate["verification_task"]["task_id"] = candidate["id"]
        candidate["verification_task"]["surface"] = "synthetic_harness"
        projection = test_author_projection(candidate, fixture["envelope"]["assignment"])
        projection["id"] = candidate["id"]
        projections[lane] = projection
        candidates[lane] = candidate

    def invoke(lane: str) -> tuple[str, dict[str, Any]]:
        adapter = IsolatedCodexAdapter("test_author", config, "codex", run_dir, cli_identity, "v7")
        return lane, adapter(projections[lane])

    responses: dict[str, dict[str, Any]] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        for lane, response in executor.map(invoke, LANES):
            responses[lane] = response

    rows = []
    total_executions = 0
    for lane in LANES:
        response = responses[lane]
        run_sha = response.pop("_run_sha256")
        validate_response(response)
        candidate, evidence = _attach(candidates[lane], response, run_sha)
        executable, retry = _executable_evidence(candidate, evidence, runtime_path, verify)
        attempts = sum(len(row["attempts"]) for row in retry["attempts"])
        total_executions += attempts
        outcomes = _outcomes(executable)
        if retry["unresolved"] or attempts != 4 or outcomes != EXPECTED:
            raise ValueError(f"{lane}: canary executable matrix failed: {outcomes}")
        rows.append({
            "lane": lane,
            "candidate_id": candidate["id"],
            "projection_sha256": canonical_sha256(projections[lane]),
            "response_sha256": canonical_sha256(response),
            "test_author_evidence_sha256": evidence["evidence_sha256"],
            "executable_evidence_sha256": executable["evidence_sha256"],
            "retry_ledger_sha256": retry["ledger_sha256"],
            "sandbox_suite_executions": attempts,
            "outcomes": outcomes,
        })
    report = {
        "schema_version": "ganesh-mini-gate2-v7-training-only-canaries/v1",
        "contract_id": CONTRACT_ID,
        "plan_sha256": plan_sha256,
        "status": "passed",
        "coverage": {"canaries": 6, "lanes": list(LANES), "sandbox_suite_executions": total_executions},
        "rows": rows,
        "rows_sha256": canonical_sha256(rows),
        "cli_identity": cli_identity,
        "config_sha256": canonical_sha256(config),
        "runtime_config_sha256": hashlib.sha256(runtime_path.read_bytes()).hexdigest(),
        "training_records_emitted": 0,
        "qualification_candidates_admitted": 0,
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--codex-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--runtimes", type=Path, default=Path("configs/eval/runtimes.json"))
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.codex_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version("codex", config["codex_cli_version"])
    report = build_report(
        json.loads(args.fixtures.read_text(encoding="utf-8")), config, cli_identity,
        args.run_dir, args.runtimes, hashlib.sha256(args.plan.read_bytes()).hexdigest(),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
