import copy
import hashlib
import json
from pathlib import Path

import pytest

from scripts.data.aggregate_capability_scale_admission import aggregate, EXPECTED_MATRIX
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.review_capability_qualification import candidate_sha256
from scripts.eval.contracts import sha256_text


def seal(value: dict, field: str) -> dict:
    value[field] = canonical_sha256(value)
    return value


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def queue_row(identifier: str, source_n: int, cohort: str = "first_pass") -> dict:
    source = {
        "dataset": "fixture", "revision": "r1", "record_id": f"source-{source_n}",
        "source_record_sha256": f"{source_n:064x}", "license": "MIT",
    }
    row = {
        "schema_version": "ganesh-mini-capability-scale-request/v1", "id": identifier,
        "cell_id": "associative_aggregation/go/generation", "lane": "go", "task_type": "generation",
        "primary_capability": "associative_aggregation", "primary_capability_definition": "aggregate by key",
        "assigned_cross_cutting_dimension": "duplicate_handling", "source_queue_id": f"queue-{source_n}",
        "source": source, "cohort": cohort, "evaluation_artifacts_read": 0,
    }
    row["request_sha256"] = canonical_sha256(row)
    return row


def candidate(row: dict) -> dict:
    assignment = {
        "cell_id": row["cell_id"], "primary_capability": row["primary_capability"],
        "primary_capability_definition": row["primary_capability_definition"],
        "assigned_cross_cutting_dimension": row["assigned_cross_cutting_dimension"],
        "source_queue_id": row["source_queue_id"],
        "source_identity": {key: row["source"][key] for key in ("dataset", "revision", "record_id")},
        "source_record_sha256": row["source"]["source_record_sha256"],
        "queue_row_sha256": canonical_sha256(row),
    }
    assignment["assignment_sha256"] = canonical_sha256(assignment)
    prompt, answer, bad = f"solve {row['id']}", "package solution\n", "package solution // bad\n"
    return {
        "schema_version": "ganesh-mini-expansion-candidate/v1", "id": row["id"], "lane": "go",
        "task_type": "generation", "messages": [
            {"role": "user", "content": prompt}, {"role": "assistant", "content": answer},
        ],
        "source": copy.deepcopy(row["source"]), "rights": {"model_training": True},
        "qualification_assignment": assignment,
        "teacher_evidence": {"request_sha256": row["request_sha256"], "evaluation_artifacts_read": 0},
        "test_origin": "pending-v9-canonical-independent-author",
        "verification_task": {
            "prompt": {"text": prompt, "sha256": sha256_text(prompt)},
            "validation": {
                "reference": {"code": answer, "sha256": sha256_text(answer)},
                "known_bad": [{"label": "bad", "code": bad, "sha256": sha256_text(bad)}],
            },
            "files": [],
        },
    }


def semantic(row: dict, verdict: str = "pass") -> dict:
    assignment = row["qualification_assignment"]
    return seal({
        "candidate_sha256": candidate_sha256(row),
        "specification_sha256": sha256_text(row["messages"][0]["content"]),
        "primary_capability": assignment["primary_capability"],
        "assigned_cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"],
        "verdict": verdict, "primary_capability_is_substantive": verdict == "pass",
        "generic_edge_case_boilerplate_is_primary": verdict != "pass", "rationale": "fixture",
        "visibility": {"evaluation_artifacts_read": 0},
    }, "evidence_sha256")


def stage_rows(base: dict, matrix_status: str = "admitted", delta_status: str = "passed", suffix: str = "a"):
    attached = copy.deepcopy(base)
    content = f"package solution // test {suffix}\n"
    attached["verification_task"]["files"] = [{
        "path": "solution_test.go", "role": "test", "content": content, "sha256": sha256_text(content),
    }]
    test = seal({
        "candidate_id": base["id"], "candidate_sha256": canonical_sha256(base),
        "cell_id": base["qualification_assignment"]["cell_id"], "status": "structurally-valid",
        "evaluation_artifacts_read": 0,
    }, "artifact_sha256")
    attachment = seal({
        "candidate_id": base["id"], "candidate_sha256": canonical_sha256(attached),
        "test_author_artifact_sha256": test["artifact_sha256"], "evaluation_artifacts_read": 0,
    }, "evidence_sha256")
    delta_evidence = seal({
        "candidate_sha256": canonical_sha256(attached), "independent_semantic_delta_count": 1,
        "delta_is_capability_specific": True, "introduces_multiple_independent_fixes": False,
    }, "evidence_sha256")
    assignment = base["qualification_assignment"]
    delta = seal({
        "candidate_id": base["id"], "candidate_sha256": canonical_sha256(attached),
        "cell_id": assignment["cell_id"], "status": delta_status, "test_attachment": attachment,
        "delta_evidence": delta_evidence,
        "lineage": {key: assignment[key] for key in (
            "cell_id", "source_queue_id", "source_record_sha256", "queue_row_sha256", "assignment_sha256",
        )},
        "evaluation_artifacts_read": 0,
    }, "artifact_sha256")
    matrix = seal({
        "candidate_id": base["id"], "candidate_sha256": canonical_sha256(attached),
        "cell_id": assignment["cell_id"], "status": matrix_status,
        "outcomes": EXPECTED_MATRIX if matrix_status == "admitted" else {
            **EXPECTED_MATRIX, "reference.primary_discrimination": "fail",
        },
        "test_author_evidence_sha256": attachment["evidence_sha256"],
        "delta_evidence_sha256": delta_evidence["evidence_sha256"], "evaluation_artifacts_read": 0,
    }, "artifact_sha256")
    return attached, test, delta, matrix


def stage_report(rows: list[dict], field: str) -> dict:
    return seal({field: canonical_sha256(rows), "evaluation_artifacts_read": 0}, "report_sha256")


def add_attempt(root: Path, name: str, kind: str, candidates: list[dict], outcomes: list[tuple], parent=None) -> dict:
    directory = root / name; directory.mkdir()
    attached, tests, deltas, matrices = map(list, zip(*outcomes))
    semantics = [semantic(row) for row in candidates]
    for filename, rows in (
        ("candidates.jsonl", candidates), ("attached.jsonl", attached), ("semantic.jsonl", semantics),
        ("test.jsonl", tests), ("delta.jsonl", deltas), ("matrix.jsonl", matrices),
    ):
        write_jsonl(directory / filename, rows)
    reports = {}
    if kind != "correction":
        reports["teacher"] = "teacher-report.json"
        write_json(directory / reports["teacher"], seal({
            "candidates_sha256": canonical_sha256(candidates), "evaluation_artifacts_read": 0,
        }, "report_sha256"))
    reports.update({"semantic": "semantic-report.json", "test": "test-report.json", "delta": "delta-report.json", "matrix": "matrix-report.json"})
    write_json(directory / reports["semantic"], seal({
        "semantic_evidence_sha256s": [row["evidence_sha256"] for row in semantics],
        "evaluation_artifacts_read": 0,
    }, "report_sha256"))
    write_json(directory / reports["test"], stage_report(tests, "terminal_rows_sha256"))
    write_json(directory / reports["delta"], stage_report(deltas, "rows_sha256"))
    write_json(directory / reports["matrix"], stage_report(matrices, "terminal_rows_sha256"))
    value = {
        "name": name, "kind": kind, "correction_count": 1 if kind == "correction" else 0,
        "candidates": f"{name}/candidates.jsonl", "attached_candidates": f"{name}/attached.jsonl",
        "semantic_evidence": f"{name}/semantic.jsonl", "test_artifacts": f"{name}/test.jsonl",
        "delta_artifacts": f"{name}/delta.jsonl", "matrix_artifacts": f"{name}/matrix.jsonl",
        "reports": {key: f"{name}/{path}" for key, path in reports.items()},
    }
    if parent is not None:
        value["parent_attempt"] = parent
    return value


def fixture(tmp_path: Path) -> Path:
    queue = [queue_row("original-admit", 1), queue_row("corrected", 2), queue_row("failed", 3), queue_row("reserve", 4, "reserve")]
    bases = {row["id"]: candidate(row) for row in queue}
    original = add_attempt(tmp_path, "original", "original", [bases[key] for key in ("original-admit", "corrected", "failed")], [
        stage_rows(bases["original-admit"]),
        stage_rows(bases["corrected"], matrix_status="rejected"),
        stage_rows(bases["failed"], delta_status="semantic-rejected"),
    ])
    replacement = add_attempt(tmp_path, "replacement", "replacement", [bases["reserve"]], [stage_rows(bases["reserve"])])
    correction = add_attempt(tmp_path, "correction", "correction", [bases["corrected"]], [stage_rows(bases["corrected"], suffix="fixed")], "original")
    correction.pop("semantic_evidence")
    correction["reports"].pop("semantic")
    write_jsonl(tmp_path / "queue.jsonl", queue)
    queue_bytes = (tmp_path / "queue.jsonl").read_bytes()
    write_json(tmp_path / "queue-report.json", seal({
        "queue_sha256": hashlib.sha256(queue_bytes).hexdigest(), "records": len(queue),
        "source_exclusion": {"evaluation_surfaces_read": 0},
    }, "manifest_sha256"))
    selected = [stage_rows(bases["original-admit"])[0], stage_rows(bases["corrected"], suffix="fixed")[0], stage_rows(bases["reserve"])[0]]
    separation = {
        "evaluation_artifacts_read_by_construction": 0,
        "comparison_manifest": {"content_exposure": {
            "evaluation_content_serialized": 0, "evaluation_paths_or_task_ids_serialized": 0,
            "collision_identities_serialized": 0,
        }},
        "records": [{"id": row["id"], "candidate_sha256": canonical_sha256(row), **{
            field: True for field in (
                "exact_training_passed", "normalized_training_passed", "fuzzy_training_passed",
                "exact_evaluation_passed", "normalized_evaluation_passed", "fuzzy_evaluation_passed",
            )
        }} for row in selected],
    }
    separation["comparison_manifest_sha256"] = canonical_sha256(separation["comparison_manifest"])
    write_json(tmp_path / "separation.json", seal(separation, "report_sha256"))
    manifest = {
        "source_queue": "queue.jsonl", "source_queue_manifest": "queue-report.json",
        "separation_report": "separation.json",
        "cell_targets": {"associative_aggregation/go/generation": 3},
        "attempts": [original, replacement, correction], "evaluation_artifacts_read": 0,
    }
    write_json(tmp_path / "manifest.json", seal(manifest, "manifest_sha256"))
    return tmp_path / "manifest.json"


def test_aggregates_original_replacement_and_single_correction(tmp_path: Path) -> None:
    admitted, records, failures, cells, report = aggregate(fixture(tmp_path))
    assert {row["id"] for row in admitted} == {"original-admit", "corrected", "reserve"}
    assert [(row["candidate_id"], row["stage"], row["status"]) for row in failures] == [
        ("failed", "delta-audit", "semantic-rejected"),
    ]
    assert cells == [{"cell_id": "associative_aggregation/go/generation", "target": 3, "admitted": 3, "deficit": 0}]
    assert {row["candidate_id"] for row in records} == {"original-admit", "corrected", "reserve"}
    assert next(row for row in records if row["candidate_id"] == "corrected")["correction_count"] == 1
    assert report["status"] == "complete" and report["incomplete"] == 0
    body = dict(report); claimed = body.pop("report_sha256")
    assert claimed == canonical_sha256(body)


def test_rejects_second_correction(tmp_path: Path) -> None:
    path = fixture(tmp_path)
    manifest = json.loads(path.read_text())
    manifest.pop("manifest_sha256")
    duplicate = copy.deepcopy(manifest["attempts"][-1]); duplicate["name"] = "correction-two"
    manifest["attempts"].append(duplicate)
    write_json(path, seal(manifest, "manifest_sha256"))
    with pytest.raises(ValueError, match="more than one correction"):
        aggregate(path)


def test_rejects_source_reuse_and_cell_overfill(tmp_path: Path) -> None:
    path = fixture(tmp_path)
    manifest = json.loads(path.read_text()); manifest.pop("manifest_sha256")
    manifest["cell_targets"]["associative_aggregation/go/generation"] = 2
    write_json(path, seal(manifest, "manifest_sha256"))
    with pytest.raises(ValueError, match="overfill"):
        aggregate(path)


def test_rejects_nonzero_evaluation_read_or_tampered_artifact(tmp_path: Path) -> None:
    path = fixture(tmp_path)
    artifact_path = tmp_path / "replacement/test.jsonl"
    row = json.loads(artifact_path.read_text().splitlines()[0])
    row["evaluation_artifacts_read"] = 1
    write_jsonl(artifact_path, [row])
    with pytest.raises(ValueError, match="invalid artifact_sha256"):
        aggregate(path)
