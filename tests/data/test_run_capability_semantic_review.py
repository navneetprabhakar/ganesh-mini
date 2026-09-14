import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.run_capability_semantic_review import (
    batch_descriptor,
    build_work,
    combine,
    run_batch,
    verify_completed,
)
from scripts.data.review_capability_qualification import candidate_sha256
from scripts.eval.contracts import sha256_text


LANES = ("go", "java", "javascript", "typescript", "python", "rust")


def candidate(identifier: str, lane: str) -> dict:
    prompt = f"Implement parse_{identifier}(text)."
    return {
        "id": identifier, "lane": lane, "task_type": "generation",
        "messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": "source"}],
        "qualification_assignment": {
            "cell_id": f"parsing_and_encoding/{lane}/generation",
            "primary_capability": "parsing_and_encoding",
            "primary_capability_definition": "Parse a structured representation.",
            "assigned_cross_cutting_dimension": "malformed_input",
        },
    }


def semantic(row: dict, verdict: str = "pass") -> dict:
    value = {
        "candidate_sha256": candidate_sha256(row),
        "specification_sha256": sha256_text(row["messages"][0]["content"]),
        "primary_capability": row["qualification_assignment"]["primary_capability"],
        "assigned_cross_cutting_dimension": row["qualification_assignment"]["assigned_cross_cutting_dimension"],
        "verdict": verdict,
        "primary_capability_is_substantive": verdict == "pass",
        "generic_edge_case_boilerplate_is_primary": verdict != "pass",
        "rationale": "Bounded fixture review.",
        "visibility": {
            "specification_and_assigned_labels_only": True,
            "evaluation_artifacts_read": 0,
        },
    }
    value["evidence_sha256"] = canonical_sha256(value)
    return value


def write_batch(
    output: Path, evidence: Path, rows: list[dict], campaign_sha: str,
    lane: str, index: int, *, reverse: bool = False,
) -> str:
    expected_ids = [row["id"] for row in rows]
    descriptor = batch_descriptor(campaign_sha, lane, index, expected_ids)
    batch_sha = canonical_sha256(descriptor)
    reviews = [semantic(row) for row in rows]
    if reverse:
        reviews.reverse()
    payload = b"".join(
        json.dumps(row, sort_keys=True, separators=(",", ":")).encode() + b"\n"
        for row in reviews
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    evidence.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(payload)
    outer = {
        "schema_version": "ganesh-mini-capability-semantic-review-batch/v1",
        "campaign": {"campaign_sha256": campaign_sha},
        "campaign_sha256": campaign_sha,
        "batch": descriptor,
        "batch_sha256": batch_sha,
        "requested_ids": expected_ids,
        "reviewed": len(rows),
        "semantic_output_sha256": hashlib.sha256(payload).hexdigest(),
        "evaluation_artifacts_read": 0,
        "runs": [], "failures": [],
    }
    outer["evidence_sha256"] = canonical_sha256(outer)
    evidence.write_text(json.dumps(outer))
    return batch_sha


def all_candidates() -> list[dict]:
    return [candidate(f"{lane}-{index:02d}", lane) for lane in LANES for index in range(40)]


def test_verify_completed_accepts_exact_sealed_semantic_batch(tmp_path: Path) -> None:
    rows = [candidate(f"go-{index}", "go") for index in range(10)]
    output, evidence = tmp_path / "batch.jsonl", tmp_path / "evidence.json"
    batch_sha = write_batch(output, evidence, rows, "a" * 64, "go", 0)

    result = verify_completed(output, evidence, rows, "a" * 64, batch_sha)

    assert result == {
        "reviewed": 10, "passed": 10, "rejected": 0,
        "evidence_sha256": json.loads(evidence.read_text())["evidence_sha256"],
        "output_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
    }


def test_verify_completed_rejects_partial_and_reordered_candidate_evidence(tmp_path: Path) -> None:
    rows = [candidate(f"go-{index}", "go") for index in range(10)]
    output, evidence = tmp_path / "batch.jsonl", tmp_path / "evidence.json"
    output.write_text("")
    with pytest.raises(ValueError, match="partial"):
        verify_completed(output, evidence, rows, "a" * 64, "b" * 64)
    output.unlink()
    batch_sha = write_batch(output, evidence, rows, "a" * 64, "go", 0, reverse=True)
    with pytest.raises(ValueError, match="campaign contract"):
        verify_completed(output, evidence, rows, "a" * 64, batch_sha)


def test_run_batch_reuses_valid_artifacts_without_subprocess(tmp_path: Path) -> None:
    rows = [candidate(f"go-{index}", "go") for index in range(10)]
    output, evidence = tmp_path / "batch.jsonl", tmp_path / "evidence.json"
    batch_sha = write_batch(output, evidence, rows, "a" * 64, "go", 0)
    with patch("scripts.data.run_capability_semantic_review.subprocess.run") as invoked:
        result = run_batch(["never"], output, evidence, rows, "a" * 64, batch_sha)
    invoked.assert_not_called()
    assert result["status"] == "reused"


def test_build_work_is_exactly_24_batches_and_combine_restores_input_order(tmp_path: Path) -> None:
    canonical_rows = all_candidates()
    campaign_sha = "c" * 64
    work = build_work(canonical_rows, tmp_path / "out", tmp_path / "evidence", campaign_sha)
    assert len(work) == 24
    assert all(len(item[4]) == 10 for item in work)
    for lane, index, output, evidence, rows, batch_sha in reversed(work):
        assert write_batch(output, evidence, rows, campaign_sha, lane, index) == batch_sha

    combined, batches = combine(work, list(reversed(canonical_rows)), campaign_sha)

    assert [row["candidate_sha256"] for row in combined] == [
        candidate_sha256(row) for row in reversed(canonical_rows)
    ]
    assert len(batches) == 24


def test_build_work_rejects_incomplete_lane(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="expected exactly 40"):
        build_work(all_candidates()[:-1], tmp_path / "out", tmp_path / "evidence", "d" * 64)
