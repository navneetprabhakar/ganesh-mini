from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.finalize_capability_replacements import build
from scripts.data.review_capability_qualification import candidate_sha256
from scripts.eval.contracts import sha256_text


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows))


def test_combines_one_independently_reviewed_replacement_and_fails_on_review_tamper(tmp_path: Path) -> None:
    originals = [{"id": f"q-{index}"} for index in range(240)]
    original_path = tmp_path / "original.jsonl"; write_jsonl(original_path, originals)
    original_report = {
        "schema_version": "ganesh-mini-capability-semantic-review-report/v1", "status": "complete",
        "candidate_input_sha256": hashlib.sha256(original_path.read_bytes()).hexdigest(),
        "records": [{"id": row["id"]} for row in originals], "report_sha256": "a" * 64,
    }
    replacement = {
        "id": "replacement-1", "messages": [{"role": "user", "content": "spec"}],
        "qualification_assignment": {"primary_capability": "parser", "assigned_cross_cutting_dimension": "malformed_input"},
        "teacher_evidence": {},
    }
    replacement_path = tmp_path / "replacement.jsonl"; write_jsonl(replacement_path, [replacement])
    manifest = {
        "schema_version": "ganesh-mini-capability-replacement-queue-manifest/v1",
        "semantic_report_sha256": original_report["report_sha256"], "replacement_attempt": 1,
        "candidate_ids": ["replacement-1"],
        "batches": [{"candidates": str(replacement_path), "records": 1}],
        "manifest_sha256": "b" * 64,
    }
    review = {
        "id": "replacement-1", "candidate_sha256": candidate_sha256(replacement),
        "specification_sha256": sha256_text("spec"), "primary_capability": "parser",
        "assigned_cross_cutting_dimension": "malformed_input", "verdict": "pass",
        "primary_capability_is_substantive": True, "generic_edge_case_boilerplate_is_primary": False,
        "visibility": {"specification_and_assigned_labels_only": True, "verifier_outputs_visible": False, "evaluation_artifacts_read": 0},
    }
    review["evidence_sha256"] = canonical_sha256(review)
    review_path = tmp_path / "review.jsonl"; write_jsonl(review_path, [review])
    combined, augmented = build(original_path, original_report, manifest, [review_path])
    assert len(combined) == 241 and len(augmented["records"]) == 241
    assert augmented["records"][-1]["id"] == "replacement-1"

    review["verdict"] = "reject"; review_path.write_text(json.dumps(review) + "\n")
    with pytest.raises(ValueError, match="seal"):
        build(original_path, original_report, manifest, [review_path])

