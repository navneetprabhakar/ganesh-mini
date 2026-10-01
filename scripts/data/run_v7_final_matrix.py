#!/usr/bin/env python3
"""Run V7 separation-bound final matrices and seal all 60 dispositions."""

from __future__ import annotations

import argparse
import concurrent.futures
import copy
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.admit_repair_delta import PROOF_BOOLEAN_OVERLAP, SEMANTIC_BOOLEANS, teacher_candidate_sha256
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_capability_separation_attestations import PASS_FIELDS
from scripts.data.repair_delta_v7_readiness import CONTRACT_ID, RESPONSE_SCHEMA_VERSION
from scripts.data.run_repair_delta_evidence import _executable_evidence, _rebind_semantic, seal
from scripts.data.run_repair_delta_two_phase import build_separation_sidecars
from scripts.eval.contracts import sha256_text
from scripts.verify.sandbox import verify


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
EXPECTED = {
    "reference.primary_discrimination": "pass", "reference.cross_cutting": "pass",
    "known_bad.primary_discrimination": "fail", "known_bad.cross_cutting": "pass",
}


def _sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value); claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field}")
    return value


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


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


def _test_evidence(candidate: dict[str, Any], assignment: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    return seal({
        "candidate_sha256": canonical_sha256(candidate),
        "specification_sha256": sha256_text(candidate["messages"][0]["content"]),
        "known_bad_sha256": candidate["verification_task"]["validation"]["known_bad"][0]["sha256"],
        "primary_capability": assignment["primary_capability"],
        "assigned_cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"],
        "response_schema_version": RESPONSE_SCHEMA_VERSION,
        "test_roles": copy.deepcopy(source["test_roles"]),
        "test_author_run_evidence_sha256": source["test_author_run_evidence_sha256"],
        "visibility": {
            "specification_visible": True, "embedded_known_bad_visible": True,
            "capability_definition_visible": True, "scheduled_dimension_visible": True,
            "reference_visible": False, "teacher_proof_visible": False,
            "semantic_review_visible": False, "verifier_outputs_visible": False,
            "evaluation_artifacts_read": 0,
        },
    })


def run(args: argparse.Namespace) -> dict[str, Any]:
    generated = _jsonl(args.generated)
    assignments = _jsonl(args.assignments)
    attached = _jsonl(args.attached)
    attached_test_sources = _jsonl(args.test_evidence)
    delta_rows = _jsonl(args.delta_terminal)
    carry = _sealed(args.carry, "manifest_sha256")
    delta_report = _sealed(args.delta_report, "report_sha256")
    separation_report = _sealed(args.separation_report, "report_sha256")
    if not all(len(rows) == 60 for rows in (generated, assignments, attached, attached_test_sources, delta_rows)):
        raise ValueError("V7 final inputs are not exact 60")
    if delta_report.get("status") != "passed" or separation_report.get("status") != "passed":
        raise ValueError("V7 delta or separation gate did not pass")
    ordered_ids = [row["candidate"]["id"] for row in generated]
    if any([
        [row["id"] for row in assignments] != ordered_ids,
        [row["id"] for row in attached] != ordered_ids,
        [row["candidate_id"] for row in delta_rows] != ordered_ids,
        [row["candidate_id"] for row in carry["rows"]] != ordered_ids,
    ]):
        raise ValueError("V7 final inputs differ from canonical order")
    sidecars, separation_contract = build_separation_sidecars(separation_report, attached, args.sidecars_output)
    separation_by_id = {row["candidate_id"]: row for row in sidecars}

    envelopes = []
    for raw, assignment, candidate, source_test, delta_row, carry_row in zip(
        generated, assignments, attached, attached_test_sources, delta_rows, carry["rows"], strict=True,
    ):
        proof = raw["repair_delta_proof"]
        proof_body = dict(proof); proof_claimed = proof_body.pop("evidence_sha256", None)
        semantic = carry_row["semantic_evidence"]
        if (
            proof_claimed != canonical_sha256(proof_body)
            or proof.get("candidate_id") != candidate["id"]
            or proof.get("teacher_candidate_sha256") != teacher_candidate_sha256(raw["candidate"])
            or any(proof.get(field) is not True for field in PROOF_BOOLEAN_OVERLAP)
            or any(semantic.get(field) is not True for field in SEMANTIC_BOOLEANS)
            or delta_row.get("status") != "passed"
        ):
            raise ValueError(f"{candidate['id']}: carried proof/semantic/delta gate differs")
        semantic = _rebind_semantic(semantic, candidate)
        test = _test_evidence(candidate, assignment, source_test)
        delta = delta_row["delta_evidence"]
        separation = separation_by_id[candidate["id"]]
        if any(separation[field] is not True for field in PASS_FIELDS):
            raise ValueError(f"{candidate['id']}: separation did not pass")
        envelopes.append({
            "schema_version": "ganesh-mini-gate2-v7-pre-execution-envelope/v1",
            "contract_id": CONTRACT_ID,
            "candidate": candidate,
            "assignment": {**assignment, "contract_id": CONTRACT_ID},
            "evidence": {"teacher_proof": proof, "semantic_review": semantic, "test_author": test, "delta_audit": delta, "separation": separation},
        })

    by_lane: dict[str, list[int]] = {lane: [] for lane in LANES}
    for index, envelope in enumerate(envelopes):
        by_lane[envelope["candidate"]["lane"]].append(index)

    def run_lane(lane: str) -> list[tuple[int, dict[str, Any], dict[str, Any]]]:
        values = []
        for index in by_lane[lane]:
            envelope = envelopes[index]
            executable, retry = _executable_evidence(
                envelope["candidate"], envelope["evidence"]["test_author"], args.runtimes, verify,
            )
            values.append((index, executable, retry))
        return values

    executions: list[tuple[dict[str, Any], dict[str, Any]] | None] = [None] * 60
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        for lane_results in executor.map(run_lane, LANES):
            for index, executable, retry in lane_results:
                executions[index] = (executable, retry)

    terminal = []
    for ordinal, (envelope, execution_pair) in enumerate(zip(envelopes, executions, strict=True)):
        assert execution_pair is not None
        executable, retry = execution_pair
        outcomes = _outcomes(executable)
        evidence = envelope["evidence"]
        evidence["executable"] = executable
        evidence["retry_ledger"] = retry
        candidate = envelope["candidate"]
        assignment = envelope["assignment"]
        lineage = seal({
            "candidate_sha256": canonical_sha256(candidate), "contract_id": CONTRACT_ID,
            "cell_id": assignment["cell_id"],
            "source_identity": {key: candidate["source"].get(key) for key in ("dataset", "revision", "record_id")},
            "source_record_sha256": candidate["source"]["source_record_sha256"], "complete": True,
            "teacher_proof_evidence_sha256": evidence["teacher_proof"]["evidence_sha256"],
            "semantic_review_evidence_sha256": evidence["semantic_review"]["evidence_sha256"],
            "test_author_evidence_sha256": evidence["test_author"]["evidence_sha256"],
            "delta_audit_evidence_sha256": evidence["delta_audit"]["evidence_sha256"],
            "separation_evidence_sha256": evidence["separation"]["evidence_sha256"],
            "executable_evidence_sha256": executable["evidence_sha256"],
        })
        evidence["lineage"] = lineage
        status = "admitted" if not retry["unresolved"] and outcomes == EXPECTED else ("unresolved" if retry["unresolved"] else "rejected")
        row = {
            "schema_version": "ganesh-mini-gate2-v7-terminal-artifact/v1",
            "contract_id": CONTRACT_ID, "ordinal": ordinal,
            "candidate_id": candidate["id"], "cell_id": assignment["cell_id"],
            "lane": candidate["lane"], "primary_capability": assignment["primary_capability"],
            "assigned_cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"],
            "status": status, "outcomes": outcomes, "envelope": envelope,
            "evaluation_artifacts_read": 0,
        }
        row["artifact_sha256"] = canonical_sha256(row)
        terminal.append(row)
    counts = Counter(row["status"] for row in terminal)
    lane_counts = Counter(row["lane"] for row in terminal if row["status"] == "admitted")
    cap_counts = Counter(row["primary_capability"] for row in terminal if row["status"] == "admitted")
    dim_counts = Counter(row["assigned_cross_cutting_dimension"] for row in terminal if row["status"] == "admitted")
    report = {
        "schema_version": "ganesh-mini-gate2-v7-final-admission-report/v1",
        "contract_id": CONTRACT_ID,
        "status": "passed" if counts == {"admitted": 60} else "failed",
        "generated": 60, "counts": dict(sorted(counts.items())),
        "admitted_by_lane": dict(sorted(lane_counts.items())),
        "admitted_by_capability": dict(sorted(cap_counts.items())),
        "admitted_by_dimension": dict(sorted(dim_counts.items())),
        "separation_contract_sha256": separation_contract,
        "separation_report_sha256": separation_report["report_sha256"],
        "delta_report_sha256": delta_report["report_sha256"],
        "terminal_rows_sha256": canonical_sha256(terminal),
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "terminal-artifacts.jsonl").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in terminal), encoding="utf-8")
    (args.output_dir / "admitted.jsonl").write_text("".join(json.dumps(row["envelope"]["candidate"], sort_keys=True) + "\n" for row in terminal if row["status"] == "admitted"), encoding="utf-8")
    (args.output_dir / "admission-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("generated", "assignments", "attached", "test-evidence", "delta-terminal", "delta-report", "carry", "separation-report", "runtimes", "sidecars-output", "output-dir"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    report = run(args)
    print(json.dumps({"status": report["status"], "counts": report["counts"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
