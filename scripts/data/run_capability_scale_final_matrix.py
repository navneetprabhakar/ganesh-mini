#!/usr/bin/env python3
"""Run resumable executable matrices for capability-scale candidates.

This is deliberately a new Gate 3 controller.  Historical V7/V9 controllers
and their sealed evidence remain immutable; only their canonical staging and
sandbox execution primitive is reused.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import copy
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.repair_delta_v7_readiness import validate_lane_interface
from scripts.data.run_repair_delta_evidence import _executable_evidence
from scripts.eval.contracts import sha256_text
from scripts.verify.sandbox import verify


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
ROLES = ("primary_discrimination", "cross_cutting")
EXPECTED = {
    "reference.primary_discrimination": "pass",
    "reference.cross_cutting": "pass",
    "known_bad.primary_discrimination": "fail",
    "known_bad.cross_cutting": "pass",
}
PASS_STATUSES = {
    "passed", "complete", "structurally-valid", "ready-for-delta",
    "ready-for-execution", "accepted",
}
ExecutorFn = Callable[
    [dict[str, Any], dict[str, Any], Path, Callable[..., dict[str, Any]]],
    tuple[dict[str, Any], dict[str, Any]],
]


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _load_artifacts(path: Path) -> list[dict[str, Any]]:
    """Load one JSONL/aggregate JSON or a directory of candidate artifacts."""
    if path.is_dir():
        rows = []
        for child in sorted(path.glob("*.json")):
            value = json.loads(child.read_text(encoding="utf-8"))
            if isinstance(value, dict) and "candidate_id" in value and "artifact_sha256" in value:
                rows.append(value)
        if not rows:
            raise ValueError(f"{path}: no sealed candidate artifacts")
        return rows
    if path.suffix == ".jsonl":
        return _jsonl(path)
    value = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        for key in ("rows", "artifacts", "terminal_artifacts", "records"):
            if isinstance(value.get(key), list):
                return value[key]
        if "candidate_id" in value:
            return [value]
    raise ValueError(f"{path}: unsupported artifact container")


def _sealed(value: dict[str, Any], field: str, label: str) -> dict[str, Any]:
    body = copy.deepcopy(value)
    claimed = body.pop(field, None)
    if not isinstance(claimed, str) or claimed != canonical_sha256(body):
        raise ValueError(f"{label}: invalid {field}")
    return value


def _optional_report(path: Path | None, expected_records: int, label: str) -> dict[str, Any] | None:
    if path is None:
        return None
    report = _sealed(json.loads(path.read_text(encoding="utf-8")), "report_sha256", label)
    if report.get("status") != "passed":
        raise ValueError(f"{label}: upstream report did not pass")
    observed = report.get("requested", report.get("records", report.get("generated")))
    if observed is not None and observed != expected_records:
        raise ValueError(f"{label}: record count differs from candidates")
    if report.get("evaluation_artifacts_read", 0) != 0:
        raise ValueError(f"{label}: evaluation-artifact read count is nonzero")
    return report


def _candidate(value: dict[str, Any]) -> dict[str, Any]:
    candidate = value.get("candidate") if isinstance(value.get("candidate"), dict) else value
    if not isinstance(candidate, dict) or not isinstance(candidate.get("id"), str):
        raise ValueError("teacher input is missing a candidate identity")
    return candidate


def _attached_candidate(row: dict[str, Any]) -> dict[str, Any]:
    for key in ("candidate", "attached_candidate"):
        if isinstance(row.get(key), dict):
            return row[key]
    envelope = row.get("envelope")
    if isinstance(envelope, dict) and isinstance(envelope.get("candidate"), dict):
        return envelope["candidate"]
    raise ValueError(f"{row.get('candidate_id')}: test-author artifact lacks attached candidate")


def _evidence(row: dict[str, Any], names: tuple[str, ...], stage: str) -> dict[str, Any]:
    for name in names:
        if isinstance(row.get(name), dict):
            return row[name]
    nested = row.get("evidence")
    if isinstance(nested, dict):
        for name in names:
            if isinstance(nested.get(name), dict):
                return nested[name]
    raise ValueError(f"{row.get('candidate_id')}: {stage} evidence is missing")


def _stable_teacher_projection(candidate: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(candidate)
    value.pop("test_origin", None)
    task = value.get("verification_task", {})
    task["files"] = [item for item in task.get("files", []) if item.get("role") != "test"]
    return value


def _validate_test_evidence(candidate: dict[str, Any], evidence: dict[str, Any]) -> None:
    _sealed(evidence, "evidence_sha256", f"{candidate['id']}: test-author evidence")
    if evidence.get("candidate_sha256") != canonical_sha256(candidate):
        raise ValueError(f"{candidate['id']}: test-author candidate hash mismatch")
    roles = evidence.get("test_roles")
    if not isinstance(roles, list) or [row.get("role") for row in roles] != list(ROLES):
        raise ValueError(f"{candidate['id']}: test roles are not in canonical order")
    files = {row.get("path"): row for row in candidate["verification_task"].get("files", [])}
    for role in roles:
        file = files.get(role.get("path"))
        if (
            not isinstance(file, dict) or file.get("role") != "test"
            or file.get("sha256") != role.get("file_sha256")
            or file.get("sha256") != sha256_text(file.get("content", ""))
            or not isinstance(role.get("case_ids"), list) or not role["case_ids"]
        ):
            raise ValueError(f"{candidate['id']}: {role.get('role')} file binding differs")
        findings = validate_lane_interface(candidate["lane"], file["content"])
        if findings:
            raise ValueError(f"{candidate['id']}: lane interface rejected {role['role']}: {findings}")


def _validate_delta(candidate: dict[str, Any], evidence: dict[str, Any]) -> None:
    _sealed(evidence, "evidence_sha256", f"{candidate['id']}: delta evidence")
    if evidence.get("candidate_sha256") != canonical_sha256(candidate):
        raise ValueError(f"{candidate['id']}: delta candidate hash mismatch")
    outcome = (
        evidence.get("independent_semantic_delta_count"),
        evidence.get("delta_is_capability_specific"),
        evidence.get("introduces_multiple_independent_fixes"),
    )
    if outcome != (1, True, False):
        raise ValueError(f"{candidate['id']}: blind delta audit did not pass")


def _outcomes(executable: dict[str, Any]) -> dict[str, str]:
    return {
        f"{implementation}.{role}": (
            "pass" if executable["results"][implementation][role].get("exit_codes")
            and all(code == 0 for code in executable["results"][implementation][role]["exit_codes"])
            else "fail"
        )
        for implementation in ("reference", "known_bad") for role in ROLES
    }


def _atomic(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def _atomic_text(path: Path, value: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def _execute_one(
    candidate: dict[str, Any], test: dict[str, Any], delta: dict[str, Any],
    runtime_path: Path, run_dir: Path, executor_fn: ExecutorFn, verifier_fn: Callable[..., dict[str, Any]],
) -> dict[str, Any]:
    input_sha = canonical_sha256({
        "candidate_sha256": canonical_sha256(candidate),
        "test_author_evidence_sha256": test["evidence_sha256"],
        "delta_evidence_sha256": delta["evidence_sha256"],
        "runtime_config_sha256": __import__("hashlib").sha256(runtime_path.read_bytes()).hexdigest(),
        "expected_matrix": EXPECTED,
    })
    path = run_dir / f"{candidate['id']}.matrix.json"
    if path.exists():
        artifact = _sealed(json.loads(path.read_text(encoding="utf-8")), "artifact_sha256", str(path))
        if artifact.get("input_sha256") != input_sha:
            raise ValueError(f"{candidate['id']}: sealed matrix artifact input drift")
        return artifact
    executable, retry = executor_fn(candidate, test, runtime_path, verifier_fn)
    _sealed(executable, "evidence_sha256", f"{candidate['id']}: executable evidence")
    _sealed(retry, "ledger_sha256", f"{candidate['id']}: retry ledger")
    if (
        executable.get("candidate_sha256") != canonical_sha256(candidate)
        or executable.get("retry_ledger_sha256") != retry["ledger_sha256"]
    ):
        raise ValueError(f"{candidate['id']}: executable/retry binding differs")
    outcomes = _outcomes(executable)
    status = "unresolved" if retry.get("unresolved") else ("admitted" if outcomes == EXPECTED else "rejected")
    assignment = candidate["qualification_assignment"]
    artifact = {
        "schema_version": "ganesh-mini-capability-scale-matrix-artifact/v1",
        "status": status, "candidate_id": candidate["id"],
        "cell_id": assignment["cell_id"], "lane": candidate["lane"],
        "task_type": candidate["task_type"],
        "primary_capability": assignment["primary_capability"],
        "assigned_cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"],
        "input_sha256": input_sha, "outcomes": outcomes,
        "candidate_sha256": canonical_sha256(candidate),
        "test_author_evidence_sha256": test["evidence_sha256"],
        "delta_evidence_sha256": delta["evidence_sha256"],
        "executable_evidence": executable, "retry_ledger": retry,
        "evaluation_artifacts_read": 0,
    }
    artifact["artifact_sha256"] = canonical_sha256(artifact)
    _atomic(path, artifact)
    return artifact


def run(
    args: argparse.Namespace, executor_fn: ExecutorFn = _executable_evidence,
    verifier_fn: Callable[..., dict[str, Any]] = verify,
) -> dict[str, Any]:
    teachers = [_candidate(row) for row in _jsonl(args.candidates)]
    if not teachers or len({row["id"] for row in teachers}) != len(teachers):
        raise ValueError("teacher candidates are empty or duplicate")
    delta_selection_path = getattr(args, "delta_selection_report", None)
    delta_selection: dict[str, Any] | None = None
    if delta_selection_path is not None:
        delta_selection = _sealed(
            json.loads(delta_selection_path.read_text(encoding="utf-8")),
            "report_sha256", "delta selection report",
        )
        if (
            delta_selection.get("schema_version") != "ganesh-mini-capability-scale-stage-selection/v1"
            or delta_selection.get("evaluation_artifacts_read") != 0
        ):
            raise ValueError("delta selection report is invalid")
        teacher_by_id = {row["id"]: row for row in teachers}
        if any(identifier not in teacher_by_id for identifier in delta_selection.get("selected_ids", [])):
            raise ValueError("delta selection differs from teacher candidates")
        teachers = [teacher_by_id[identifier] for identifier in delta_selection["selected_ids"]]
    ordered_ids = [row["id"] for row in teachers]
    teacher_report = _optional_report(args.teacher_report, len(teachers), "teacher report")
    if teacher_report is not None and teacher_report.get("candidates_sha256") != canonical_sha256(teachers):
        raise ValueError("teacher report: candidate aggregate hash differs")
    tests = _load_artifacts(args.test_author_artifacts)
    deltas = _load_artifacts(args.delta_artifacts)
    attached_path = getattr(args, "attached_candidates", None)
    attached_rows = _jsonl(attached_path) if attached_path is not None else []
    if delta_selection is not None:
        selected = set(ordered_ids)
        tests = [row for row in tests if row.get("candidate_id") in selected]
        deltas = [row for row in deltas if row.get("candidate_id") in selected]
        attached_rows = [row for row in attached_rows if row.get("id") in selected]
        if (
            delta_selection.get("selected_rows_sha256") != canonical_sha256(deltas)
            or delta_selection.get("selected_artifact_sha256s")
            != [row.get("artifact_sha256") for row in deltas]
        ):
            raise ValueError("delta selection does not bind delta artifacts")
    attached_by_id = {row.get("id"): row for row in attached_rows}
    if attached_rows and (len(attached_by_id) != len(attached_rows) or set(attached_by_id) != set(ordered_ids)):
        raise ValueError("attached candidates differ from the teacher cohort")
    test_report = _optional_report(args.test_author_report, len(teachers), "test-author report")
    delta_report = _optional_report(args.delta_report, len(teachers), "delta report")

    def index(rows: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}
        for row in rows:
            _sealed(row, "artifact_sha256", f"{label}/{row.get('candidate_id')}")
            identifier = row.get("candidate_id")
            if not isinstance(identifier, str) or identifier in result:
                raise ValueError(f"{label}: missing or duplicate candidate identity")
            if row.get("status") not in PASS_STATUSES:
                raise ValueError(f"{identifier}: {label} stage did not pass")
            if row.get("evaluation_artifacts_read", 0) != 0:
                raise ValueError(f"{identifier}: {label} read evaluation artifacts")
            result[identifier] = row
        if set(result) != set(ordered_ids):
            raise ValueError(f"{label}: candidate set differs from teacher input")
        return result

    test_by_id, delta_by_id = index(tests, "test-author"), index(deltas, "delta")
    for report, indexed, label in (
        (test_report, test_by_id, "test-author"), (delta_report, delta_by_id, "delta"),
    ):
        if report is not None and report.get("terminal_artifact_sha256s") != [
            indexed[identifier]["artifact_sha256"] for identifier in ordered_ids
        ]:
            raise ValueError(f"{label} report: ordered artifact hashes differ")
    prepared: list[tuple[dict[str, Any], dict[str, Any], dict[str, Any]]] = []
    for teacher in teachers:
        test_row, delta_row = test_by_id[teacher["id"]], delta_by_id[teacher["id"]]
        candidate = attached_by_id.get(teacher["id"])
        if candidate is None:
            candidate = _attached_candidate(test_row)
        if candidate.get("id") != teacher["id"] or candidate.get("lane") not in LANES:
            raise ValueError(f"{teacher['id']}: attached candidate identity or lane differs")
        if canonical_sha256(_stable_teacher_projection(candidate)) != canonical_sha256(_stable_teacher_projection(teacher)):
            raise ValueError(f"{teacher['id']}: test author changed non-test candidate content")
        try:
            test = _evidence(delta_row, ("test_attachment", "test_author_evidence", "test_evidence"), "test-author")
        except ValueError:
            test = _evidence(test_row, ("test_author_evidence", "test_evidence", "test_author"), "test-author")
        delta = _evidence(delta_row, ("delta_evidence", "delta_audit"), "delta")
        _validate_test_evidence(candidate, test)
        if (
            test.get("test_author_artifact_sha256") is not None
            and test["test_author_artifact_sha256"] != test_row["artifact_sha256"]
        ):
            raise ValueError(f"{teacher['id']}: test attachment does not bind the test-author artifact")
        _validate_delta(candidate, delta)
        prepared.append((candidate, test, delta))

    args.run_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any] | None] = [None] * len(prepared)

    def execute(index_value: int) -> tuple[int, dict[str, Any]]:
        candidate, test, delta = prepared[index_value]
        return index_value, _execute_one(
            candidate, test, delta, args.runtimes, args.run_dir, executor_fn, verifier_fn,
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        for ordinal, artifact in executor.map(execute, range(len(prepared))):
            results[ordinal] = artifact
    terminal = [row for row in results if row is not None]
    counts = dict(sorted(Counter(row["status"] for row in terminal).items()))
    admitted_by_lane = dict(sorted(Counter(row["lane"] for row in terminal if row["status"] == "admitted").items()))
    report = {
        "schema_version": "ganesh-mini-capability-scale-final-matrix-report/v1",
        "status": "passed" if counts == {"admitted": len(teachers)} else "failed",
        "requested": len(teachers), "counts": counts,
        "admitted_by_lane": admitted_by_lane,
        "ordered_candidate_ids": ordered_ids,
        "terminal_artifact_sha256s": [row["artifact_sha256"] for row in terminal],
        "terminal_rows_sha256": canonical_sha256(terminal),
        "teacher_report_sha256": teacher_report["report_sha256"] if teacher_report else None,
        "test_author_report_sha256": test_report["report_sha256"] if test_report else None,
        "delta_report_sha256": delta_report["report_sha256"] if delta_report else None,
        "delta_selection_report_sha256": delta_selection["report_sha256"] if delta_selection else None,
        "expected_matrix": EXPECTED, "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _atomic_text(
        args.output_dir / "terminal-artifacts.jsonl",
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in terminal),
    )
    _atomic_text(
        args.output_dir / "admitted.jsonl",
        "".join(json.dumps(candidate, sort_keys=True) + "\n" for candidate, _, _ in prepared
                if next(row for row in terminal if row["candidate_id"] == candidate["id"])["status"] == "admitted"),
    )
    _atomic(args.output_dir / "matrix-report.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--teacher-report", type=Path)
    parser.add_argument("--test-author-artifacts", type=Path, required=True)
    parser.add_argument("--test-author-report", type=Path)
    parser.add_argument("--attached-candidates", type=Path, required=True)
    parser.add_argument("--delta-artifacts", type=Path, required=True)
    parser.add_argument("--delta-report", type=Path)
    parser.add_argument("--delta-selection-report", type=Path)
    parser.add_argument("--runtimes", type=Path, default=Path("configs/eval/runtimes.json"))
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    report = run(args)
    print(json.dumps({"status": report["status"], "counts": report["counts"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
