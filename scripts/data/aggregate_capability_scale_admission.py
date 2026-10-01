#!/usr/bin/env python3
"""Aggregate terminal Gate 3 scale attempts into a fail-closed admission set.

The input is a sealed JSON manifest whose ``attempts`` are ordered.  Original
and replacement attempts carry their own teacher report.  A correction names
an earlier ``parent_attempt`` and may reuse its exact pre-test candidate, but
may replace test, delta, and matrix evidence once.  Paths are resolved relative
to the manifest.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.review_capability_qualification import candidate_sha256, load_evidence
from scripts.eval.contracts import sha256_text
from scripts.data.build_capability_separation_attestations import PASS_FIELDS


EXPECTED_MATRIX = {
    "reference.primary_discrimination": "pass",
    "reference.cross_cutting": "pass",
    "known_bad.primary_discrimination": "fail",
    "known_bad.cross_cutting": "pass",
}
PASS_TEST_STATUSES = {"structurally-valid", "passed"}
PASS_DELTA_STATUSES = {"passed", "ready-for-execution"}
KINDS = {"original", "replacement", "correction"}


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _sealed(value: Any, field: str, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label}: expected object")
    body = copy.deepcopy(value)
    claimed = body.pop(field, None)
    if not isinstance(claimed, str) or claimed != canonical_sha256(body):
        raise ValueError(f"{label}: invalid {field}")
    return value


def _path(base: Path, value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label}: path is absent")
    path = Path(value)
    return path if path.is_absolute() else base / path


def _report(base: Path, value: Any, label: str) -> dict[str, Any]:
    report = _sealed(json.loads(_path(base, value, label).read_text(encoding="utf-8")), "report_sha256", label)
    if report.get("evaluation_artifacts_read") != 0:
        raise ValueError(f"{label}: evaluation-artifact read count is nonzero")
    return report


def _artifact_map(path: Path, label: str) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    rows = _jsonl(path)
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        _sealed(row, "artifact_sha256", f"{label}/{row.get('candidate_id')}")
        identifier = row.get("candidate_id")
        if not isinstance(identifier, str) or not identifier or identifier in indexed:
            raise ValueError(f"{label}: missing or duplicate candidate identity")
        if row.get("evaluation_artifacts_read") != 0:
            raise ValueError(f"{label}/{identifier}: evaluation-artifact read count is nonzero")
        indexed[identifier] = row
    return rows, indexed


def _assignment(candidate: dict[str, Any]) -> dict[str, Any]:
    identifier = candidate.get("id")
    assignment = candidate.get("qualification_assignment")
    source = candidate.get("source")
    if not isinstance(identifier, str) or not isinstance(assignment, dict) or not isinstance(source, dict):
        raise ValueError(f"{identifier}: candidate identity, assignment, or source is absent")
    body = copy.deepcopy(assignment)
    claimed = body.pop("assignment_sha256", None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{identifier}: assignment seal mismatch")
    expected_cell = f"{assignment.get('primary_capability')}/{candidate.get('lane')}/{candidate.get('task_type')}"
    if assignment.get("cell_id") != expected_cell:
        raise ValueError(f"{identifier}: cell identity differs from candidate labels")
    identity = {key: source.get(key) for key in ("dataset", "revision", "record_id")}
    if (
        assignment.get("source_identity") != identity
        or assignment.get("source_record_sha256") != source.get("source_record_sha256")
        or not all(isinstance(assignment.get(key), str) and assignment[key] for key in (
            "source_queue_id", "source_record_sha256", "queue_row_sha256", "assignment_sha256",
        ))
    ):
        raise ValueError(f"{identifier}: source or queue lineage mismatch")
    teacher = candidate.get("teacher_evidence")
    if not isinstance(teacher, dict) or teacher.get("evaluation_artifacts_read") != 0:
        raise ValueError(f"{identifier}: teacher evaluation-artifact read count is not zero")
    return assignment


def _stable_pretest(candidate: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(candidate)
    task = value.get("verification_task", {})
    task["files"] = [row for row in task.get("files", []) if row.get("role") != "test"]
    return value


def _lineage(assignment: dict[str, Any]) -> dict[str, Any]:
    return {key: assignment[key] for key in (
        "cell_id", "source_queue_id", "source_record_sha256", "queue_row_sha256", "assignment_sha256",
    )}


def _validate_attempt(base: Path, spec: dict[str, Any], prior: dict[str, dict[str, Any]]) -> dict[str, Any]:
    name, kind = spec.get("name"), spec.get("kind")
    correction_count = spec.get("correction_count")
    if not isinstance(name, str) or not name or name in prior or kind not in KINDS:
        raise ValueError("attempt name is absent/duplicate or kind is invalid")
    if correction_count not in (0, 1) or (kind == "correction") != (correction_count == 1):
        raise ValueError(f"{name}: correction count must be zero, or one only for correction attempts")
    candidates_path = _path(base, spec.get("candidates"), f"{name}/candidates")
    attached_path = _path(base, spec.get("attached_candidates"), f"{name}/attached_candidates")
    candidates, attached = _jsonl(candidates_path), _jsonl(attached_path)
    candidate_by_id = {row.get("id"): row for row in candidates}
    attached_by_id = {row.get("id"): row for row in attached}
    if not candidates or len(candidate_by_id) != len(candidates) or len(attached_by_id) != len(attached):
        raise ValueError(f"{name}: candidate inputs are empty or duplicate")
    if not set(attached_by_id) <= set(candidate_by_id):
        raise ValueError(f"{name}: attached candidates are not a subset of teacher candidates")
    assignments = {identifier: _assignment(row) for identifier, row in candidate_by_id.items()}
    for identifier, final in attached_by_id.items():
        if canonical_sha256(_stable_pretest(final)) != canonical_sha256(_stable_pretest(candidate_by_id[identifier])):
            raise ValueError(f"{name}/{identifier}: test attachment changed non-test candidate content")

    reports = spec.get("reports")
    if not isinstance(reports, dict):
        raise ValueError(f"{name}: report paths are absent")
    required_reports = {"test", "delta", "matrix"} | ({"teacher", "semantic"} if kind != "correction" else set())
    if not required_reports <= set(reports):
        raise ValueError(f"{name}: required stage report paths are absent")
    report_sha256s: dict[str, str] = {}
    teacher_report = None
    if kind != "correction":
        teacher_report = _report(base, reports.get("teacher"), f"{name}/teacher-report")
        report_sha256s["teacher"] = teacher_report["report_sha256"]
        if teacher_report.get("candidates_sha256") != canonical_sha256(candidates):
            raise ValueError(f"{name}: teacher report does not bind candidates")
    else:
        parent_name = spec.get("parent_attempt")
        parent = prior.get(parent_name)
        if parent is None:
            raise ValueError(f"{name}: correction parent must be an earlier attempt")
        for identifier, candidate in candidate_by_id.items():
            parent_candidate = parent["candidate_by_id"].get(identifier)
            if parent_candidate is None or canonical_sha256(candidate) != canonical_sha256(parent_candidate):
                raise ValueError(f"{name}/{identifier}: correction changed or invented the teacher candidate")

    semantic_by_id: dict[str, dict[str, Any]] = {}
    if kind == "correction" and spec.get("semantic_evidence") is None:
        semantic_by_id = {identifier: copy.deepcopy(parent["semantic"][identifier]) for identifier in candidate_by_id}
        report_sha256s["semantic_inherited"] = parent["report_sha256s"]["semantic"]
    else:
        semantic_path = _path(base, spec.get("semantic_evidence"), f"{name}/semantic")
        semantic_rows = _jsonl(semantic_path)
        by_semantic_hash = {candidate_sha256(row): identifier for identifier, row in candidate_by_id.items()}
        for row in semantic_rows:
            evidence = load_evidence(row)
            identifier = by_semantic_hash.get(row.get("candidate_sha256"))
            if evidence is None or identifier is None or identifier in semantic_by_id:
                raise ValueError(f"{name}: semantic evidence is unsealed, duplicate, or unbound")
            assignment = assignments[identifier]
            candidate = candidate_by_id[identifier]
            if (
                row.get("specification_sha256") != sha256_text(candidate["messages"][0]["content"])
                or row.get("primary_capability") != assignment["primary_capability"]
                or row.get("assigned_cross_cutting_dimension") != assignment["assigned_cross_cutting_dimension"]
                or row.get("visibility", {}).get("evaluation_artifacts_read") != 0
            ):
                raise ValueError(f"{name}/{identifier}: semantic binding or separation differs")
            semantic_by_id[identifier] = row
        semantic_report = _report(base, reports.get("semantic"), f"{name}/semantic-report")
        report_sha256s["semantic"] = semantic_report["report_sha256"]
        reported_semantic_hashes = semantic_report.get(
            "ordered_semantic_evidence_sha256s",
            semantic_report.get("semantic_evidence_sha256s"),
        )
        if (
            reported_semantic_hashes != [row["evidence_sha256"] for row in semantic_rows]
            or set(semantic_by_id) != set(candidate_by_id)
        ):
            raise ValueError(f"{name}: semantic report or coverage differs")

    stages: dict[str, dict[str, dict[str, Any]]] = {}
    for stage, path_key, report_key, rows_key in (
        ("test", "test_artifacts", "test", "terminal_rows_sha256"),
        ("delta", "delta_artifacts", "delta", "rows_sha256"),
        ("matrix", "matrix_artifacts", "matrix", "terminal_rows_sha256"),
    ):
        rows, indexed = _artifact_map(_path(base, spec.get(path_key), f"{name}/{stage}"), f"{name}/{stage}")
        if not set(indexed) <= set(candidate_by_id):
            raise ValueError(f"{name}/{stage}: artifact candidate set exceeds teacher candidates")
        report = _report(base, reports.get(report_key), f"{name}/{stage}-report")
        report_sha256s[stage] = report["report_sha256"]
        if report.get(rows_key) != canonical_sha256(rows):
            raise ValueError(f"{name}/{stage}: report does not bind terminal rows")
        stages[stage] = indexed

    for identifier, candidate in candidate_by_id.items():
        assignment, final = assignments[identifier], attached_by_id.get(identifier)
        test, delta, matrix = (stages[key].get(identifier) for key in ("test", "delta", "matrix"))
        for stage, artifact in (("test", test), ("delta", delta), ("matrix", matrix)):
            if artifact is not None and artifact.get("cell_id") != assignment["cell_id"]:
                raise ValueError(f"{name}/{identifier}: {stage} cell lineage differs")
        if test is not None and test.get("candidate_sha256") != canonical_sha256(candidate):
            raise ValueError(f"{name}/{identifier}: test artifact candidate hash differs")
        if delta is not None:
            if final is None or delta.get("candidate_sha256") != canonical_sha256(final):
                raise ValueError(f"{name}/{identifier}: delta attached-candidate hash differs")
            if delta.get("lineage") != _lineage(assignment):
                raise ValueError(f"{name}/{identifier}: delta lineage differs")
            attachment = delta.get("test_attachment")
            if not isinstance(attachment, dict):
                raise ValueError(f"{name}/{identifier}: delta test attachment is absent")
            _sealed(attachment, "evidence_sha256", f"{name}/{identifier}/test-attachment")
            if test is None or attachment.get("test_author_artifact_sha256") != test["artifact_sha256"]:
                raise ValueError(f"{name}/{identifier}: delta does not bind test artifact")
        if matrix is not None:
            delta_evidence = delta.get("delta_evidence") if isinstance(delta, dict) else None
            if final is None or matrix.get("candidate_sha256") != canonical_sha256(final):
                raise ValueError(f"{name}/{identifier}: matrix attached-candidate hash differs")
            if not isinstance(delta_evidence, dict):
                raise ValueError(f"{name}/{identifier}: matrix has no bound delta evidence")
            _sealed(delta_evidence, "evidence_sha256", f"{name}/{identifier}/delta-evidence")
            if (
                matrix.get("test_author_evidence_sha256") != delta["test_attachment"]["evidence_sha256"]
                or matrix.get("delta_evidence_sha256") != delta_evidence["evidence_sha256"]
            ):
                raise ValueError(f"{name}/{identifier}: matrix stage-chain hash differs")

    return {
        "name": name, "kind": kind, "correction_count": correction_count,
        "candidate_by_id": candidate_by_id, "attached_by_id": attached_by_id,
        "assignments": assignments, "semantic": semantic_by_id, **stages,
        "report_sha256s": report_sha256s,
    }


def _outcome(attempt: dict[str, Any], identifier: str) -> dict[str, Any]:
    semantic = attempt["semantic"].get(identifier)
    test, delta, matrix = (attempt[key].get(identifier) for key in ("test", "delta", "matrix"))
    chain = {
        "semantic_evidence_sha256": semantic.get("evidence_sha256") if semantic else None,
        "test_artifact_sha256": test.get("artifact_sha256") if test else None,
        "delta_artifact_sha256": delta.get("artifact_sha256") if delta else None,
        "matrix_artifact_sha256": matrix.get("artifact_sha256") if matrix else None,
    }
    if semantic is None:
        return {"stage": "semantic", "status": "missing-evidence", "incomplete": True, **chain}
    if semantic.get("verdict") != "pass":
        return {"stage": "semantic", "status": "rejected", "incomplete": False, **chain}
    if test is None:
        return {"stage": "test-author", "status": "missing-evidence", "incomplete": True, **chain}
    if test.get("status") not in PASS_TEST_STATUSES:
        return {"stage": "test-author", "status": str(test.get("status")), "incomplete": False, **chain}
    if delta is None:
        return {"stage": "delta-audit", "status": "missing-evidence", "incomplete": True, **chain}
    if delta.get("status") not in PASS_DELTA_STATUSES:
        return {"stage": "delta-audit", "status": str(delta.get("status")), "incomplete": False, **chain}
    if matrix is None:
        return {"stage": "matrix", "status": "missing-evidence", "incomplete": True, **chain}
    if matrix.get("status") == "admitted" and matrix.get("outcomes") == EXPECTED_MATRIX:
        return {"stage": "matrix", "status": "admitted", "incomplete": False, **chain}
    return {"stage": "matrix", "status": str(matrix.get("status")), "incomplete": matrix.get("status") == "unresolved", **chain}


def aggregate(manifest_path: Path) -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any],
]:
    manifest = _sealed(json.loads(manifest_path.read_text(encoding="utf-8")), "manifest_sha256", str(manifest_path))
    specs = manifest.get("attempts")
    if manifest.get("evaluation_artifacts_read") != 0 or not isinstance(specs, list) or not specs:
        raise ValueError("input manifest is empty or has nonzero evaluation reads")
    queue_path = _path(manifest_path.parent, manifest.get("source_queue"), "source_queue")
    queue_rows = _jsonl(queue_path)
    queue_report = _sealed(
        json.loads(_path(manifest_path.parent, manifest.get("source_queue_manifest"), "source_queue_manifest").read_text(encoding="utf-8")),
        "manifest_sha256", "source_queue_manifest",
    )
    if (
        queue_report.get("queue_sha256") != hashlib.sha256(queue_path.read_bytes()).hexdigest()
        or queue_report.get("records") != len(queue_rows)
        or queue_report.get("source_exclusion", {}).get("evaluation_surfaces_read") != 0
    ):
        raise ValueError("source queue manifest binding or separation differs")
    queue_by_id = {row.get("id"): row for row in queue_rows}
    if len(queue_by_id) != len(queue_rows):
        raise ValueError("source queue contains duplicate request IDs")

    targets = manifest.get("cell_targets")
    if (
        not isinstance(targets, dict) or not targets
        or any(not isinstance(cell, str) or type(count) is not int or count < 0 for cell, count in targets.items())
    ):
        raise ValueError("cell_targets must be a non-empty mapping of non-negative integers")

    attempts: dict[str, dict[str, Any]] = {}
    source_owners: dict[tuple[str, str], str] = {}
    histories: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = {}
    for spec in specs:
        attempt = _validate_attempt(manifest_path.parent, spec, attempts)
        attempts[attempt["name"]] = attempt
        for identifier, candidate in attempt["candidate_by_id"].items():
            assignment = attempt["assignments"][identifier]
            queue_row = queue_by_id.get(identifier)
            if (
                not isinstance(queue_row, dict)
                or canonical_sha256(queue_row) != assignment["queue_row_sha256"]
                or queue_row.get("cell_id") != assignment["cell_id"]
                or queue_row.get("source_queue_id") != assignment["source_queue_id"]
                or queue_row.get("source") != candidate.get("source")
                or queue_row.get("evaluation_artifacts_read") != 0
            ):
                raise ValueError(f"{identifier}: candidate does not bind the sealed source queue")
            key = (canonical_sha256(assignment["source_identity"]), assignment["source_record_sha256"])
            owner = source_owners.setdefault(key, identifier)
            if owner != identifier:
                raise ValueError(f"{identifier}: source lineage is already owned by {owner}")
            existing = histories.get(identifier, [])
            if existing and attempt["kind"] != "correction":
                raise ValueError(f"{identifier}: only a correction may repeat a candidate identity")
            if attempt["kind"] == "correction":
                parent_name = spec.get("parent_attempt")
                parent_outcomes = [outcome for prior_attempt, outcome in existing if prior_attempt["name"] == parent_name]
                if len(parent_outcomes) != 1 or parent_outcomes[0]["status"] == "admitted":
                    raise ValueError(f"{identifier}: correction does not follow one failed parent outcome")
            if existing:
                first_assignment = existing[0][0]["assignments"][identifier]
                if _lineage(first_assignment) != _lineage(assignment):
                    raise ValueError(f"{identifier}: attempt changed sealed source/cell lineage")
            histories.setdefault(identifier, []).append((attempt, _outcome(attempt, identifier)))

    admitted: list[dict[str, Any]] = []
    admission_context: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    failures: list[dict[str, Any]] = []
    for identifier in sorted(histories):
        history = histories[identifier]
        if len([attempt for attempt, _ in history if attempt["correction_count"] == 1]) > 1:
            raise ValueError(f"{identifier}: more than one correction attempt is present")
        attempt, outcome = history[-1]
        assignment = attempt["assignments"][identifier]
        if outcome["status"] == "admitted":
            candidate = attempt["attached_by_id"].get(identifier)
            if candidate is None:
                raise ValueError(f"{identifier}: admitted candidate lacks attached tests")
            admitted.append(candidate)
            admission_context[identifier] = (attempt, outcome)
            continue
        record = {
            "schema_version": "ganesh-mini-capability-scale-terminal-failure/v1",
            "candidate_id": identifier, "attempt": attempt["name"], "attempt_kind": attempt["kind"],
            "correction_count": attempt["correction_count"], "cell_id": assignment["cell_id"],
            "lane": attempt["candidate_by_id"][identifier]["lane"],
            "task_type": attempt["candidate_by_id"][identifier]["task_type"],
            "source_queue_id": assignment["source_queue_id"],
            "source_record_sha256": assignment["source_record_sha256"],
            **outcome, "evaluation_artifacts_read": 0,
        }
        record["record_sha256"] = canonical_sha256(record)
        failures.append(record)

    # Separation is a deliberately independent, content-free comparison stage.
    # It may inspect frozen evaluation tasks, but construction and this
    # aggregator must read zero evaluation artifacts and its output may contain
    # only pass bits and aggregate identities/counts.
    separation = _sealed(
        json.loads(_path(manifest_path.parent, manifest.get("separation_report"), "separation_report").read_text(encoding="utf-8")),
        "report_sha256", "separation_report",
    )
    comparison = separation.get("comparison_manifest")
    if (
        not isinstance(comparison, dict)
        or separation.get("comparison_manifest_sha256") != canonical_sha256(comparison)
        or separation.get("evaluation_artifacts_read_by_construction") != 0
        or comparison.get("content_exposure") != {
            "evaluation_content_serialized": 0,
            "evaluation_paths_or_task_ids_serialized": 0,
            "collision_identities_serialized": 0,
        }
    ):
        raise ValueError("separation report does not preserve the content-free boundary")
    separation_by_id = {row.get("id"): row for row in separation.get("records", []) if isinstance(row, dict)}
    if len(separation_by_id) != len(separation.get("records", [])) or set(separation_by_id) != {row["id"] for row in admitted}:
        raise ValueError("separation report does not exactly cover provisional admissions")
    separated: list[dict[str, Any]] = []
    admission_records: list[dict[str, Any]] = []
    for candidate in admitted:
        row = separation_by_id[candidate["id"]]
        if row.get("candidate_sha256") != canonical_sha256(candidate):
            raise ValueError(f"{candidate['id']}: separation candidate hash differs")
        if any(row.get(field) is not True for field in PASS_FIELDS):
            assignment = candidate["qualification_assignment"]
            record = {
                "schema_version": "ganesh-mini-capability-scale-terminal-failure/v1",
                "candidate_id": candidate["id"], "attempt": histories[candidate["id"]][-1][0]["name"],
                "attempt_kind": histories[candidate["id"]][-1][0]["kind"],
                "correction_count": histories[candidate["id"]][-1][0]["correction_count"],
                "cell_id": assignment["cell_id"], "lane": candidate["lane"], "task_type": candidate["task_type"],
                "source_queue_id": assignment["source_queue_id"],
                "source_record_sha256": assignment["source_record_sha256"],
                "stage": "separation", "status": "rejected", "incomplete": False,
                "separation_report_sha256": separation["report_sha256"],
                "failed_checks": [field for field in PASS_FIELDS if row.get(field) is not True],
                "evaluation_artifacts_read": 0,
            }
            record["record_sha256"] = canonical_sha256(record)
            failures.append(record)
        else:
            separated.append(candidate)
            attempt, outcome = admission_context[candidate["id"]]
            assignment = candidate["qualification_assignment"]
            record = {
                "schema_version": "ganesh-mini-capability-scale-admission-record/v1",
                "candidate_id": candidate["id"], "candidate_sha256": canonical_sha256(candidate),
                "attempt": attempt["name"], "attempt_kind": attempt["kind"],
                "correction_count": attempt["correction_count"], "cell_id": assignment["cell_id"],
                "source_queue_id": assignment["source_queue_id"],
                "source_record_sha256": assignment["source_record_sha256"],
                "assignment_sha256": assignment["assignment_sha256"],
                "semantic_evidence_sha256": outcome["semantic_evidence_sha256"],
                "test_artifact_sha256": outcome["test_artifact_sha256"],
                "delta_artifact_sha256": outcome["delta_artifact_sha256"],
                "matrix_artifact_sha256": outcome["matrix_artifact_sha256"],
                "separation_report_sha256": separation["report_sha256"],
                "evaluation_artifacts_read": 0,
            }
            record["record_sha256"] = canonical_sha256(record)
            admission_records.append(record)
    admitted = separated

    cell_counter = Counter(row["qualification_assignment"]["cell_id"] for row in admitted)
    unexpected = set(cell_counter) - set(targets)
    overfilled = {cell: cell_counter[cell] for cell, target in targets.items() if cell_counter[cell] > target}
    if unexpected or overfilled:
        raise ValueError(f"admission overfill or unexpected cells: unexpected={sorted(unexpected)}, overfilled={overfilled}")
    cell_counts = [
        {"cell_id": cell, "target": target, "admitted": cell_counter[cell], "deficit": target - cell_counter[cell]}
        for cell, target in sorted(targets.items())
    ]
    evidence_incomplete = sum(row["incomplete"] for row in failures)
    cell_deficit = sum(row["deficit"] for row in cell_counts)
    incomplete = evidence_incomplete + cell_deficit
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-scale-admission-report/v1",
        "status": "complete" if incomplete == 0 else "incomplete",
        "input_manifest_sha256": manifest["manifest_sha256"],
        "attempts": len(attempts), "distinct_candidates": len(histories),
        "admitted": len(admitted), "terminal_failures": len(failures), "incomplete": incomplete,
        "cells_with_admissions": len(cell_counts),
        "cell_deficit": cell_deficit,
        "admitted_candidates_sha256": canonical_sha256(admitted),
        "admission_records_sha256": canonical_sha256(admission_records),
        "terminal_failures_sha256": canonical_sha256(failures),
        "cell_counts_sha256": canonical_sha256(cell_counts),
        "attempt_report_sha256s": {name: value["report_sha256s"] for name, value in attempts.items()},
        "source_queue_manifest_sha256": queue_report["manifest_sha256"],
        "separation_report_sha256": separation["report_sha256"],
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return admitted, admission_records, failures, cell_counts, report


def _atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(text); temporary = Path(handle.name)
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    admitted, admission_records, failures, cells, report = aggregate(args.manifest)
    _atomic(args.output_dir / "admitted-candidates.jsonl", "".join(json.dumps(row, sort_keys=True) + "\n" for row in admitted))
    _atomic(args.output_dir / "admission-records.jsonl", "".join(json.dumps(row, sort_keys=True) + "\n" for row in admission_records))
    _atomic(args.output_dir / "terminal-failures.jsonl", "".join(json.dumps(row, sort_keys=True) + "\n" for row in failures))
    _atomic(args.output_dir / "cell-counts.json", json.dumps(cells, indent=2, sort_keys=True) + "\n")
    _atomic(args.output_dir / "admission-report.json", json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: report[key] for key in ("status", "admitted", "terminal_failures", "report_sha256")}, sort_keys=True))
    return 0 if report["status"] == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
