from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.generate_capability_replacements import actual_empty_cells, build_replacement_queue, empty_cells


def queue() -> list[dict]:
    rows = []
    for cell in range(2):
        for ordinal in range(2):
            rows.append({
                "id": f"q-{cell}-{ordinal}", "cell_id": f"cap-{cell}/python/generation",
                "primary_capability": f"cap-{cell}", "primary_capability_definition": "definition",
                "assigned_cross_cutting_dimension": "malformed_input", "lane": "python",
                "task_type": "generation", "source_queue_id": f"source-{cell}-{ordinal}",
                "source": {"dataset": "fixture", "revision": "r", "record_id": f"old-{cell}-{ordinal}"},
                "stimulus": "old",
            })
    return rows


def semantic() -> dict:
    return {
        "schema_version": "ganesh-mini-capability-semantic-review-report/v1",
        "status": "complete", "evaluation_artifacts_read": 0,
        "records": [
            {
                "id": row["id"], "primary_capability": row["primary_capability"],
                "assigned_cross_cutting_dimension": row["assigned_cross_cutting_dimension"],
                "verdict": "reject" if row["cell_id"].startswith("cap-0/") else "pass",
            }
            for row in queue()
        ],
    }


def sources() -> list[dict]:
    return [
        {
            "id": f"fresh-{index}", "lane": "python", "task_type": "generation",
            "source": {"dataset": "fixture", "revision": "r", "record_id": f"fresh-{index}"},
            "stimulus": f"fresh {index}",
        }
        for index in range(3)
    ]


def test_derives_only_empty_cells_and_assigns_one_fresh_bound_replacement() -> None:
    rows = build_replacement_queue(queue(), semantic(), sources(), [], "a" * 64)
    assert len(rows) == 1
    assert rows[0]["cell_id"] == "cap-0/python/generation"
    assert rows[0]["replacement_attempt"] == 1
    assert rows[0]["original_queue_ids"] == ["q-0-0", "q-0-1"]
    assert rows[0]["source"]["record_id"].startswith("fresh-")
    assert rows[0]["id"] not in {row["id"] for row in queue()}


def test_rejects_incomplete_or_duplicate_disposition_evidence() -> None:
    missing = semantic(); missing["records"].pop()
    with pytest.raises(ValueError, match="all 240 originals"):
        empty_cells(queue(), missing)
    duplicate = semantic(); duplicate["records"][1] = deepcopy(duplicate["records"][0])
    with pytest.raises(ValueError, match="all 240 originals|duplicate"):
        empty_cells(queue(), duplicate)


def test_replacement_source_cannot_reuse_original_or_prior_lineage() -> None:
    reused = [{
        "id": "only", "lane": "python", "task_type": "generation",
        "source": queue()[0]["source"], "stimulus": "same",
    }]
    with pytest.raises(ValueError, match="no collision-free"):
        build_replacement_queue(queue(), semantic(), reused, [], "a" * 64)


def test_actual_empty_cells_requires_sealed_post_correction_executable_disposition(tmp_path: Path) -> None:
    rows = queue()
    plan = {
        "plan_sha256": "p" * 64, "qualification": {"drafts": 4},
        "matrix": {"cell_contracts": [{"cell_id": f"cap-{index}/python/generation"} for index in range(2)]},
    }
    envelopes = []
    for index, row in enumerate(rows):
        envelopes.append({
            "qualification": {"queue_id": row["id"], "correction_passes": 1 if index == 0 else 0},
        })
    envelope_path = tmp_path / "envelopes.jsonl"
    envelope_path.write_text("".join(json.dumps(row) + "\n" for row in envelopes))
    admitted_path = tmp_path / "admitted.jsonl"
    admitted_path.write_text(json.dumps({
        "qualification": {"cell_id": "cap-1/python/generation"},
        "record": {"id": rows[3]["id"]},
    }) + "\n")
    rejected_path = tmp_path / "rejected.json"
    rejected_path.write_text(json.dumps([{"id": row["id"]} for row in rows[:3]]))
    corrected_path = tmp_path / "corrected.jsonl"; corrected_path.write_text("{}\n")
    correction = {
        "schema_version": "ganesh-mini-capability-qualification-correction-report/v1",
        "status": "corrected-not-reviewed-not-admitted", "evaluation_artifacts_read": 0,
        "failure": None, "requested_corrections": 1, "completed_corrections": 1,
        "output": {"path": str(corrected_path), "sha256": hashlib.sha256(corrected_path.read_bytes()).hexdigest(), "bytes": corrected_path.stat().st_size},
        "output_sha256": hashlib.sha256(corrected_path.read_bytes()).hexdigest(),
        "corrections": [{"id": rows[0]["id"]}],
    }
    correction["report_sha256"] = canonical_sha256(correction)
    correction_path = tmp_path / "correction.json"; correction_path.write_text(json.dumps(correction))
    admission = {
        "schema_version": "ganesh-mini-capability-qualification-admission/v1", "mode": "final",
        "status": "failed", "plan_sha256": plan["plan_sha256"], "evaluation_artifacts_read": 0,
        "queue_disposition": {"all_originals_dispositioned": True, "sealed_originals": 4, "bounded_replacements": 0},
        "input": {"path": str(envelope_path), "sha256": hashlib.sha256(envelope_path.read_bytes()).hexdigest()},
        "outputs": {
            "admitted": {"path": str(admitted_path), "sha256": hashlib.sha256(admitted_path.read_bytes()).hexdigest(), "bytes": admitted_path.stat().st_size},
            "rejected": {"path": str(rejected_path), "sha256": hashlib.sha256(rejected_path.read_bytes()).hexdigest(), "bytes": rejected_path.stat().st_size},
        },
        "accepted": 1, "rejected": 3, "missing_cells": ["cap-0/python/generation"],
    }
    admission["report_sha256"] = canonical_sha256(admission)
    admission_path = tmp_path / "admission.json"; admission_path.write_text(json.dumps(admission))
    missing, _, _ = actual_empty_cells(plan, rows, admission_path, correction_path)
    assert missing == ["cap-0/python/generation"]

    timed_out_rejections = [{"id": row["id"]} for row in rows[:3]]
    timed_out_rejections[0]["evidence"] = {"reference": {"timed_out": True}}
    rejected_path.write_text(json.dumps(timed_out_rejections))
    admission["outputs"]["rejected"] = {
        "path": str(rejected_path),
        "sha256": hashlib.sha256(rejected_path.read_bytes()).hexdigest(),
        "bytes": rejected_path.stat().st_size,
    }
    admission.pop("report_sha256")
    admission["report_sha256"] = canonical_sha256(admission)
    admission_path.write_text(json.dumps(admission))
    with pytest.raises(ValueError, match="unresolved reference timeouts"):
        actual_empty_cells(plan, rows, admission_path, correction_path)

    rejected_path.write_text(json.dumps([{"id": row["id"]} for row in rows[:3]]))
    admission["outputs"]["rejected"] = {
        "path": str(rejected_path),
        "sha256": hashlib.sha256(rejected_path.read_bytes()).hexdigest(),
        "bytes": rejected_path.stat().st_size,
    }
    admission.pop("report_sha256")
    admission["report_sha256"] = canonical_sha256(admission)
    admission_path.write_text(json.dumps(admission))

    correction["completed_corrections"] = 0
    correction.pop("report_sha256"); correction["report_sha256"] = canonical_sha256(correction)
    correction_path.write_text(json.dumps(correction))
    with pytest.raises(ValueError, match="correction path"):
        actual_empty_cells(plan, rows, admission_path, correction_path)
