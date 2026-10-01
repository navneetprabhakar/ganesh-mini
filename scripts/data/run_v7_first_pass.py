#!/usr/bin/env python3
"""Run and seal V7's exact ordered 60-call structural first pass."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.generate_expansion_qualification import verify_codex_version
from scripts.data.repair_delta_v7_readiness import (
    CONTRACT_ID, inject_controller_paths, test_author_projection,
    validate_lane_interface, validate_response,
)
from scripts.data.run_repair_delta_evidence import IsolatedCodexAdapter, StageInvocationFailure


def _load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value); claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field}")
    return value


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _thresholds(rows: list[dict[str, Any]]) -> dict[str, Any]:
    valid = [row for row in rows if row["status"] == "structurally-valid"]
    lane = Counter(row["lane"] for row in valid)
    capability = Counter(row["primary_capability"] for row in valid)
    dimension = Counter(row["assigned_cross_cutting_dimension"] for row in valid)
    structural_rejects = sum(row["status"] == "structural-rejected" for row in rows)
    unresolved = sum(row["status"] == "invocation-failed" for row in rows)
    gates = {
        "all_60_terminal": len(rows) == 60,
        "zero_unresolved": unresolved == 0,
        "aggregate_at_least_54": len(valid) >= 54,
        "every_lane_at_least_9": bool(lane) and min(lane.values()) >= 9 and len(lane) == 6,
        "every_capability_at_least_5": bool(capability) and min(capability.values()) >= 5 and len(capability) == 10,
        "every_dimension_at_least_10": bool(dimension) and min(dimension.values()) >= 10 and len(dimension) == 5,
        "structural_rejects_at_most_6": structural_rejects <= 6,
        "zero_visibility_lineage_source_or_evaluation_failures": all(row["evaluation_artifacts_read"] == 0 for row in rows),
    }
    return {
        "structurally_valid": len(valid),
        "structural_rejected": structural_rejects,
        "invocation_failed": unresolved,
        "by_lane": dict(sorted(lane.items())),
        "by_capability": dict(sorted(capability.items())),
        "by_dimension": dict(sorted(dimension.items())),
        "gates": gates,
        "structural_reauthoring_eligible": all(gates.values()) and structural_rejects > 0,
        "direct_final_stage_eligible": all(gates.values()) and structural_rejects == 0,
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    carry = _load_sealed(args.carry, "manifest_sha256")
    cohort = _load_sealed(args.cohort, "manifest_sha256")
    readiness = _load_sealed(args.readiness, "report_sha256")
    if (
        carry.get("contract_id") != CONTRACT_ID
        or cohort.get("contract_id") != CONTRACT_ID
        or readiness.get("contract_id") != CONTRACT_ID
        or readiness.get("status") != "passed"
        or carry.get("records") != 60
        or cohort.get("records") != 60
    ):
        raise ValueError("V7 carry/cohort/readiness gate is not sealed and passed")
    generated = _read_jsonl(args.candidates)
    assignments = _read_jsonl(args.assignments)
    ordered = cohort["ordered_candidate_ids"]
    if (
        len(generated) != 60 or len(assignments) != 60
        or [row["candidate"]["id"] for row in generated] != ordered
        or [row["id"] for row in assignments] != ordered
    ):
        raise ValueError("V7 source candidates/assignments differ from the ordered cohort")
    config = json.loads(args.codex_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    projections = [test_author_projection(row["candidate"], assignment) for row, assignment in zip(generated, assignments, strict=True)]

    def invoke(index: int) -> tuple[int, dict[str, Any] | StageInvocationFailure]:
        adapter = IsolatedCodexAdapter("test_author", config, args.codex_bin, args.run_dir, cli_identity, "v7")
        try:
            return index, adapter(projections[index])
        except StageInvocationFailure as exc:
            return index, exc

    results: list[dict[str, Any] | StageInvocationFailure | None] = [None] * 60
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        for index, response in executor.map(invoke, range(60)):
            results[index] = response

    terminal = []
    for ordinal, (generated_row, assignment, projection, outcome) in enumerate(zip(generated, assignments, projections, results, strict=True)):
        candidate = generated_row["candidate"]
        base = {
            "schema_version": "ganesh-mini-gate2-v7-first-pass-terminal/v1",
            "contract_id": CONTRACT_ID,
            "ordinal": ordinal,
            "candidate_id": candidate["id"],
            "cell_id": assignment["cell_id"],
            "lane": candidate["lane"],
            "primary_capability": assignment["primary_capability"],
            "assigned_cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"],
            "projection_sha256": canonical_sha256(projection),
            "evaluation_artifacts_read": 0,
        }
        if isinstance(outcome, StageInvocationFailure):
            row = {**base, "status": "invocation-failed", "reason": str(outcome), "invocation_artifact_sha256": outcome.evidence["artifact_sha256"]}
        else:
            assert isinstance(outcome, dict)
            response = dict(outcome)
            run_sha = response.pop("_run_sha256")
            try:
                validate_response(response)
                injection = inject_controller_paths(candidate["lane"], response)
                findings = {
                    role["role"]: validate_lane_interface(candidate["lane"], role["content"])
                    for role in injection["roles"]
                }
                codes = sorted({finding["code"] for values in findings.values() for finding in values})
                if codes:
                    row = {**base, "status": "structural-rejected", "reason": "static-lane-interface", "finding_codes": codes, "findings": findings}
                else:
                    row = {**base, "status": "structurally-valid", "injection": injection, "finding_codes": [], "findings": findings}
            except (TypeError, ValueError) as exc:
                row = {**base, "status": "structural-rejected", "reason": f"response-contract: {exc}", "finding_codes": ["response-contract"]}
            row.update({"response": response, "response_sha256": canonical_sha256(response), "run_evidence_sha256": run_sha})
        row["artifact_sha256"] = canonical_sha256(row)
        terminal.append(row)
    thresholds = _thresholds(terminal)
    report = {
        "schema_version": "ganesh-mini-gate2-v7-first-pass-report/v1",
        "contract_id": CONTRACT_ID,
        "status": "passed-first-pass-thresholds" if (thresholds["structural_reauthoring_eligible"] or thresholds["direct_final_stage_eligible"]) else "failed-first-pass-thresholds",
        "carry_manifest_sha256": carry["manifest_sha256"],
        "cohort_manifest_sha256": cohort["manifest_sha256"],
        "readiness_report_sha256": readiness["report_sha256"],
        "test_author_calls": 60,
        "terminal_records": 60,
        "thresholds": thresholds,
        "terminal_rows_sha256": canonical_sha256(terminal),
        "cli_identity": cli_identity,
        "config_sha256": canonical_sha256(config),
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "terminal-artifacts.jsonl").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in terminal), encoding="utf-8")
    (args.output_dir / "first-pass-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--carry", type=Path, required=True)
    parser.add_argument("--cohort", type=Path, required=True)
    parser.add_argument("--readiness", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--assignments", type=Path, required=True)
    parser.add_argument("--codex-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()
    report = run(args)
    print(json.dumps({"status": report["status"], "thresholds": report["thresholds"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] == "passed-first-pass-thresholds" else 2


if __name__ == "__main__":
    raise SystemExit(main())
