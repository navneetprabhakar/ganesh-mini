import hashlib
import json
from collections import Counter
from pathlib import Path

import pytest

from scripts.data.summarize_capability_qualification import canonical_json, canonical_sha256, summarize


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
CAPABILITIES = tuple(f"capability-{index}" for index in range(10))
TASK_TYPES = ("generation", "repair")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in rows))


def queue_rows() -> list[dict]:
    rows = []
    for capability in CAPABILITIES:
        for lane in LANES:
            for task_type in TASK_TYPES:
                cell = f"{capability}-{lane}-{task_type}"
                for ordinal in (1, 2):
                    rows.append({
                        "id": f"{cell}-{ordinal}", "cell_id": cell,
                        "primary_capability": capability, "lane": lane, "task_type": task_type,
                    })
    return rows


def make_report(path: Path, candidate_path: Path, rejected: list[str]) -> None:
    rows = [json.loads(line) for line in candidate_path.read_text().splitlines()]
    accepted_rows = [row for row in rows if row["id"] not in set(rejected)]
    admitted_path = path.with_suffix(".admitted.jsonl")
    write_jsonl(admitted_path, [{"id": row["id"]} for row in accepted_rows])
    report = {
        "schema_version": "ganesh-mini-expansion-admission/v1", "status": "passed",
        "input": str(candidate_path),
        "input_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
        "output": {
            "path": str(admitted_path), "bytes": len(admitted_path.read_bytes()),
            "sha256": hashlib.sha256(admitted_path.read_bytes()).hexdigest(),
        },
        "accepted": len(accepted_rows),
        "rejected": [{"id": item, "reason": "test rejection"} for item in rejected],
    }
    report["report_sha256"] = canonical_sha256(report)
    path.write_text(json.dumps(report))


def make_capability_report(path: Path, candidate_path: Path, rejected: list[str]) -> None:
    rows = [json.loads(line) for line in candidate_path.read_text().splitlines()]
    item = lambda row: row.get("candidate", row)
    identifier = lambda row: item(row)["id"]
    accepted_rows = [row for row in rows if identifier(row) not in set(rejected)]
    admitted_path = path.with_suffix(".admitted.jsonl")
    cell = lambda row: row.get("qualification", {}).get(
        "cell_id", item(row).get("cell_id", item(row).get("qualification_assignment", {}).get("cell_id")),
    )
    admitted = [{
        "qualification": {"queue_id": identifier(row), "cell_id": cell(row)},
        "record": {"id": identifier(row)},
    } for row in accepted_rows]
    write_jsonl(admitted_path, admitted)
    rejected_path = path.with_suffix(".rejected.json")
    rejected_rows = [{"id": item, "reason": "test rejection"} for item in rejected]
    rejected_path.write_text(json.dumps(rejected_rows) + "\n")
    report = {
        "schema_version": "ganesh-mini-capability-qualification-admission/v1",
        "status": "candidate-admission-complete", "mode": "candidate",
        "input": {"path": str(candidate_path), "sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest()},
        "accepted": len(accepted_rows), "rejected": len(rejected_rows),
        "counts_by_cell": dict(sorted(Counter(cell(row) for row in accepted_rows).items())),
        "outputs": {
            "admitted": {"path": str(admitted_path), "bytes": len(admitted_path.read_bytes()), "sha256": hashlib.sha256(admitted_path.read_bytes()).hexdigest()},
            "rejected": {"path": str(rejected_path), "bytes": len(rejected_path.read_bytes()), "sha256": hashlib.sha256(rejected_path.read_bytes()).hexdigest()},
        },
    }
    report["report_sha256"] = canonical_sha256(report)
    path.write_text(json.dumps(report))


def fixture(tmp_path: Path) -> tuple[Path, list[dict]]:
    rows = queue_rows()
    queue = tmp_path / "queue.jsonl"
    write_jsonl(queue, rows)
    return queue, rows


def test_partial_report_tracks_yields_dimensions_and_hashes(tmp_path: Path) -> None:
    queue, rows = fixture(tmp_path)
    candidates = tmp_path / "partial.jsonl"
    write_jsonl(candidates, rows[:10])
    admission = tmp_path / "partial.admission.json"
    make_report(admission, candidates, [row["id"] for row in rows[2:10]])

    report = summarize(queue, [candidates], [admission])

    assert report["status"] == "qualification-in-progress"
    assert report["gate_passed"] is False
    assert report["totals"]["generated"] == 10
    assert report["totals"]["admitted"] == 2
    assert report["totals"]["generation_yield"] == 10 / 240
    assert report["by_lane"]["go"]["generated"] == 4
    assert report["by_task_type"]["generation"]["admitted"] == 2
    assert report["inputs"]["evaluation_surfaces_read"] == 0
    assert report["report_sha256"] == canonical_sha256(report)


def test_gate_pass_requires_all_original_dispositions_and_every_cell(tmp_path: Path) -> None:
    queue, rows = fixture(tmp_path)
    candidates = tmp_path / "all.jsonl"
    write_jsonl(candidates, rows)
    admission = tmp_path / "all.admission.json"
    make_report(admission, candidates, [row["id"] for row in rows if row["id"].endswith("-2")])

    report = summarize(queue, [candidates], [admission])

    assert report["status"] == "qualification-passed"
    assert report["totals"]["admitted"] == 120
    assert report["coverage"]["admitted_cells"] == 120
    assert report["by_family"]["javascript_typescript"] == {
        "drafted": 80, "generated": 80, "original_generated": 80,
        "replacement_generated": 0, "corrected": 0, "dispositioned": 80,
        "admitted": 40, "rejected": 40, "generation_yield": 1.0,
        "admission_yield_from_generated": 0.5,
        "admission_yield_from_dispositioned": 0.5,
    }
    assert all(report["pass_requirements"].values())


def test_empty_completed_cell_becomes_eligible_for_one_replacement(tmp_path: Path) -> None:
    queue, rows = fixture(tmp_path)
    candidates = tmp_path / "all.jsonl"
    write_jsonl(candidates, rows)
    empty_cell = rows[0]["cell_id"]
    rejected = [row["id"] for row in rows if row["id"].endswith("-2") or row["cell_id"] == empty_cell]
    admission = tmp_path / "all.admission.json"
    make_report(admission, candidates, rejected)

    report = summarize(queue, [candidates], [admission])

    assert report["status"] == "qualification-in-progress"
    assert report["bounded_replacements"]["eligible_cells"] == [empty_cell]
    assert report["gate_passed"] is False


def test_rejected_replacement_exhausts_cell_and_fails(tmp_path: Path) -> None:
    queue, rows = fixture(tmp_path)
    originals = tmp_path / "all.jsonl"
    write_jsonl(originals, rows)
    empty_cell = rows[0]["cell_id"]
    original_report = tmp_path / "all.admission.json"
    make_report(original_report, originals, [row["id"] for row in rows if row["id"].endswith("-2") or row["cell_id"] == empty_cell])
    replacement = tmp_path / "replacement.jsonl"
    replacement_id = "replacement-1"
    write_jsonl(replacement, [{
        "id": replacement_id, "cell_id": empty_cell,
        "replacement_for_cell_id": empty_cell, "replacement_attempt": 1,
    }])
    replacement_report = tmp_path / "replacement.admission.json"
    make_report(replacement_report, replacement, [replacement_id])

    report = summarize(queue, [originals, replacement], [original_report, replacement_report])

    assert report["status"] == "qualification-failed"
    assert report["bounded_replacements"]["exhausted_cells"] == [empty_cell]


def test_unsealed_or_unbound_admission_report_fails_closed(tmp_path: Path) -> None:
    queue, rows = fixture(tmp_path)
    candidates = tmp_path / "partial.jsonl"
    write_jsonl(candidates, rows[:2])
    admission = tmp_path / "bad.admission.json"
    make_report(admission, candidates, [])
    payload = json.loads(admission.read_text())
    payload["accepted"] = 1
    admission.write_text(json.dumps(payload))

    with pytest.raises(ValueError, match="invalid admission report seal"):
        summarize(queue, [candidates], [admission])


def test_more_than_one_replacement_for_a_cell_fails_closed(tmp_path: Path) -> None:
    queue, rows = fixture(tmp_path)
    cell = rows[0]["cell_id"]
    replacements = tmp_path / "replacements.jsonl"
    write_jsonl(replacements, [
        {"id": "r1", "cell_id": cell, "replacement_for_cell_id": cell, "replacement_attempt": 1},
        {"id": "r2", "cell_id": cell, "replacement_for_cell_id": cell, "replacement_attempt": 1},
    ])
    with pytest.raises(ValueError, match="more than one bounded replacement"):
        summarize(queue, [replacements], [])


def test_capability_report_reconciles_hashed_output_artifacts_and_assignment(tmp_path: Path) -> None:
    queue, rows = fixture(tmp_path)
    source = rows[:4]
    generated = []
    for row in source:
        assignment = {
            "cell_id": row["cell_id"], "primary_capability": row["primary_capability"],
            "queue_row_sha256": hashlib.sha256(canonical_json(row)).hexdigest(),
        }
        assignment["assignment_sha256"] = hashlib.sha256(canonical_json(assignment)).hexdigest()
        generated.append({
            "id": row["id"], "lane": row["lane"], "task_type": row["task_type"],
            "qualification_assignment": assignment,
        })
    candidates = tmp_path / "teacher.candidates.jsonl"
    write_jsonl(candidates, generated)
    admission = tmp_path / "capability.admission.json"
    make_capability_report(admission, candidates, [generated[-1]["id"]])

    report = summarize(queue, [candidates], [admission])

    assert report["totals"]["generated"] == 4
    assert report["totals"]["admitted"] == 3
    assert report["totals"]["rejected"] == 1
    assert report["inputs"]["admission_reports"][0]["rejected_output"]["sha256"]


def test_capability_report_output_hash_mismatch_fails_closed(tmp_path: Path) -> None:
    queue, rows = fixture(tmp_path)
    candidates = tmp_path / "candidate.jsonl"
    write_jsonl(candidates, rows[:2])
    admission = tmp_path / "capability.admission.json"
    make_capability_report(admission, candidates, [])
    payload = json.loads(admission.read_text())
    Path(payload["outputs"]["admitted"]["path"]).write_text("{}\n")

    with pytest.raises(ValueError, match="artifact hash mismatch"):
        summarize(queue, [candidates], [admission])


def test_sealed_admission_envelopes_preserve_input_binding_and_correction_closure(tmp_path: Path) -> None:
    queue, rows = fixture(tmp_path)
    envelopes = []
    for index, row in enumerate(rows):
        candidate = {
            "id": row["id"], "lane": row["lane"], "task_type": row["task_type"],
        }
        correction = None
        correction_passes = 1 if index == 0 else 0
        if correction_passes:
            correction = {
                "candidate_sha256": hashlib.sha256(canonical_json(candidate)).hexdigest(),
                "parent_candidate_sha256": "b" * 64, "outcome": "changed",
            }
            correction["evidence_sha256"] = hashlib.sha256(canonical_json(correction)).hexdigest()
        envelopes.append({
            "schema_version": "ganesh-mini-capability-qualification-envelope/v1",
            "candidate": candidate,
            "qualification": {
                "queue_id": row["id"], "cell_id": row["cell_id"],
                "primary_capability": row["primary_capability"],
                "correction_passes": correction_passes, "correction": correction,
            },
        })
    candidate_path = tmp_path / "qualification-envelopes.jsonl"
    write_jsonl(candidate_path, envelopes)
    admission = tmp_path / "final-admission.json"
    make_capability_report(
        admission, candidate_path, [row["id"] for row in rows if row["id"].endswith("-2")],
    )

    report = summarize(queue, [candidate_path], [admission])

    assert report["status"] == "qualification-passed"
    assert report["totals"]["corrected"] == 1
    assert report["pass_requirements"]["all_corrections_dispositioned"] is True
    assert report["inputs"]["admission_reports"][0]["candidate_input_sha256"] == hashlib.sha256(
        candidate_path.read_bytes(),
    ).hexdigest()


def test_envelope_with_unsealed_or_second_correction_fails_closed(tmp_path: Path) -> None:
    queue, rows = fixture(tmp_path)
    row = rows[0]
    envelope = {
        "schema_version": "ganesh-mini-capability-qualification-envelope/v1",
        "candidate": {"id": row["id"], "lane": row["lane"], "task_type": row["task_type"]},
        "qualification": {
            "queue_id": row["id"], "cell_id": row["cell_id"],
            "primary_capability": row["primary_capability"],
            "correction_passes": 2, "correction": {},
        },
    }
    candidate_path = tmp_path / "bad-envelope.jsonl"
    write_jsonl(candidate_path, [envelope])
    with pytest.raises(ValueError, match="correction passes exceed"):
        summarize(queue, [candidate_path], [])


def test_terminal_no_change_envelope_cannot_be_reported_admitted(tmp_path: Path) -> None:
    queue, rows = fixture(tmp_path)
    envelopes = []
    for index, row in enumerate(rows):
        candidate = {"id": row["id"], "lane": row["lane"], "task_type": row["task_type"]}
        candidate_sha = hashlib.sha256(canonical_json(candidate)).hexdigest()
        correction = None
        passes = 1 if index == 0 else 0
        if passes:
            correction = {
                "candidate_sha256": candidate_sha, "parent_candidate_sha256": candidate_sha,
                "outcome": "terminal-no-change",
            }
            correction["evidence_sha256"] = hashlib.sha256(canonical_json(correction)).hexdigest()
        envelopes.append({
            "schema_version": "ganesh-mini-capability-qualification-envelope/v1",
            "candidate": candidate,
            "qualification": {
                "queue_id": row["id"], "cell_id": row["cell_id"],
                "primary_capability": row["primary_capability"],
                "correction_passes": passes, "correction": correction,
            },
        })
    candidate_path = tmp_path / "terminal-no-change-envelopes.jsonl"
    write_jsonl(candidate_path, envelopes)
    admission = tmp_path / "terminal-no-change-admission.json"
    make_capability_report(
        admission, candidate_path, [row["id"] for row in rows if row["id"].endswith("-2")],
    )
    with pytest.raises(ValueError, match="terminal no-change correction was admitted"):
        summarize(queue, [candidate_path], [admission])


def test_terminal_no_change_may_be_rejected_by_an_earlier_gate(tmp_path: Path) -> None:
    queue, rows = fixture(tmp_path)
    envelopes = []
    for index, row in enumerate(rows):
        candidate = {"id": row["id"], "lane": row["lane"], "task_type": row["task_type"]}
        candidate_sha = hashlib.sha256(canonical_json(candidate)).hexdigest()
        correction = None
        passes = 1 if index == 0 else 0
        if passes:
            correction = {
                "candidate_sha256": candidate_sha, "parent_candidate_sha256": candidate_sha,
                "outcome": "terminal-no-change",
            }
            correction["evidence_sha256"] = hashlib.sha256(canonical_json(correction)).hexdigest()
        envelopes.append({
            "schema_version": "ganesh-mini-capability-qualification-envelope/v1",
            "candidate": candidate,
            "qualification": {
                "queue_id": row["id"], "cell_id": row["cell_id"],
                "primary_capability": row["primary_capability"],
                "correction_passes": passes, "correction": correction,
            },
        })
    candidate_path = tmp_path / "terminal-no-change-rejected-envelopes.jsonl"
    write_jsonl(candidate_path, envelopes)
    admission = tmp_path / "terminal-no-change-rejected-admission.json"
    rejected = [rows[0]["id"], *[row["id"] for row in rows if row["id"].endswith("-2")]]
    make_capability_report(admission, candidate_path, rejected)

    report = summarize(queue, [candidate_path], [admission])

    assert report["totals"]["corrected"] == 1
    assert report["pass_requirements"]["all_corrections_dispositioned"] is True
