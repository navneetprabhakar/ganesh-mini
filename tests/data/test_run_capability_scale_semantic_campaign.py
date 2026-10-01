from __future__ import annotations

import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.run_capability_scale_semantic_campaign import (
    batch_descriptor,
    build_report,
    build_terminal_artifacts,
    build_work,
    combine,
    load_teacher_candidates,
    run_batch,
    verify_completed,
)
from scripts.data.review_capability_qualification import candidate_sha256
from scripts.data.select_capability_scale_stage import select_stage
from scripts.eval.contracts import sha256_text


LANES = ("go", "java", "javascript", "typescript", "python", "rust")


def candidate(identifier: str, lane: str, request_sha: str) -> dict:
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
        "teacher_evidence": {"request_sha256": request_sha, "evaluation_artifacts_read": 0},
    }


def semantic(row: dict, verdict: str = "pass") -> dict:
    value = {
        "candidate_sha256": candidate_sha256(row),
        "specification_sha256": sha256_text(row["messages"][0]["content"]),
        "primary_capability": row["qualification_assignment"]["primary_capability"],
        "assigned_cross_cutting_dimension": row["qualification_assignment"]["assigned_cross_cutting_dimension"],
        "verdict": verdict, "primary_capability_is_substantive": verdict == "pass",
        "generic_edge_case_boilerplate_is_primary": verdict != "pass", "rationale": "Specific behavior.",
        "visibility": {"specification_and_assigned_labels_only": True, "evaluation_artifacts_read": 0},
    }
    value["evidence_sha256"] = canonical_sha256(value)
    return value


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join(
        json.dumps(row, sort_keys=True, separators=(",", ":")).encode() + b"\n" for row in rows
    ))


def write_teacher(tmp_path: Path, rows: list[dict]) -> tuple[Path, Path]:
    candidates = tmp_path / "candidates.jsonl"
    report_path = tmp_path / "teacher-report.json"
    write_jsonl(candidates, rows)
    report = {
        "schema_version": "ganesh-mini-capability-scale-teacher-report/v1",
        "status": "passed", "mode": "remaining-first-pass", "requested": len(rows),
        "counts": {"generated": len(rows)}, "queue_manifest_sha256": "q" * 64,
        "selected_request_sha256s": [row["teacher_evidence"]["request_sha256"] for row in rows],
        "terminal_artifact_sha256s": [str(index) * 64 for index in range(1, len(rows) + 1)],
        "candidates_sha256": canonical_sha256(rows), "cli_identity": "fixture",
        "config_sha256": "c" * 64, "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    report_path.write_text(json.dumps(report))
    return candidates, report_path


def seal_batch(
    output: Path, evidence: Path, rows: list[dict], campaign_sha: str, lane: str, index: int,
) -> str:
    descriptor = batch_descriptor(campaign_sha, lane, index, rows)
    semantic_rows = [semantic(row) for row in rows]
    write_jsonl(output, semantic_rows)
    outer = {
        "schema_version": "ganesh-mini-capability-semantic-review-batch/v1",
        "campaign": {"campaign_sha256": campaign_sha}, "campaign_sha256": campaign_sha,
        "batch": descriptor, "batch_sha256": canonical_sha256(descriptor),
        "requested_ids": [row["id"] for row in rows], "reviewed": len(rows),
        "semantic_output_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "evaluation_artifacts_read": 0, "runs": [], "failures": [],
    }
    outer["evidence_sha256"] = canonical_sha256(outer)
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text(json.dumps(outer))
    return outer["batch_sha256"]


def rows_fixture() -> list[dict]:
    counts = {"go": 11, "java": 3, "javascript": 1, "typescript": 10, "python": 4, "rust": 2}
    rows = []
    for lane in LANES:
        for index in range(counts[lane]):
            rows.append(candidate(f"{lane}-{index:02d}", lane, f"{len(rows) + 1:064x}"))
    return rows


def test_loads_any_valid_sealed_teacher_cohort_and_rejects_drift(tmp_path: Path) -> None:
    rows = rows_fixture()
    candidates, report = write_teacher(tmp_path, rows)
    loaded, sealed = load_teacher_candidates(candidates, report)
    assert loaded == rows
    assert sealed["requested"] == 31

    changed = json.loads(report.read_text()); changed["evaluation_artifacts_read"] = 1
    report.write_text(json.dumps(changed))
    with pytest.raises(ValueError, match="sealed scale contract"):
        load_teacher_candidates(candidates, report)


def test_dynamic_work_is_lane_homogeneous_and_at_most_ten(tmp_path: Path) -> None:
    rows = rows_fixture()
    work = build_work(rows, tmp_path, "a" * 64)
    assert len(work) == 7
    assert sum(len(item[4]) for item in work) == len(rows)
    assert all(1 <= len(item[4]) <= 10 for item in work)
    assert all({row["lane"] for row in item[4]} == {item[0]} for item in work)


def test_sealed_batches_reuse_and_combine_in_exact_candidate_order(tmp_path: Path) -> None:
    rows = rows_fixture()
    campaign_sha = "b" * 64
    work = build_work(rows, tmp_path, campaign_sha)
    for lane, index, output, evidence, selected, batch_sha in work:
        assert seal_batch(output, evidence, selected, campaign_sha, lane, index) == batch_sha
        with patch("scripts.data.run_capability_scale_semantic_campaign.subprocess.run") as invoked:
            result = run_batch(["never"], output, evidence, selected, campaign_sha, batch_sha)
        invoked.assert_not_called()
        assert result["reviewed"] == len(selected)

    reordered = list(reversed(rows))
    combined, batches = combine(work, reordered, campaign_sha)
    assert [row["candidate_sha256"] for row in combined] == [candidate_sha256(row) for row in reordered]
    assert sum(batch["reviewed"] for batch in batches) == len(rows)


def test_report_is_deterministic_and_zero_eval_read(tmp_path: Path) -> None:
    rows = rows_fixture()
    candidates, report_path = write_teacher(tmp_path, rows)
    _, teacher = load_teacher_candidates(candidates, report_path)
    campaign = {
        "campaign_sha256": "d" * 64, "ordered_candidate_ids": [row["id"] for row in rows],
    }
    combined = [semantic(row) for row in rows]
    combined[1] = semantic(rows[1], "reject")
    terminal = build_terminal_artifacts(rows, combined)
    batches = [{"lane": "go", "batch_index": 0, "reviewed": len(rows)}]
    one = build_report(candidates, teacher, campaign, combined, terminal, batches, "e" * 64)
    two = build_report(candidates, teacher, campaign, combined, terminal, batches, "e" * 64)
    assert one == two
    assert one["evaluation_artifacts_read"] == 0
    assert one["counts"] == {"reviewed": 31, "passed": 30, "rejected": 1}
    assert one["terminal_rows_sha256"] == canonical_sha256(terminal)
    assert one["terminal_artifact_sha256s"] == [row["artifact_sha256"] for row in terminal]
    body = dict(one); claimed = body.pop("report_sha256")
    assert claimed == canonical_sha256(body)


def test_terminal_artifacts_feed_generic_stage_selector_with_mixed_verdicts(tmp_path: Path) -> None:
    rows = rows_fixture()[:3]
    candidates, teacher_path = write_teacher(tmp_path, rows)
    _, teacher = load_teacher_candidates(candidates, teacher_path)
    semantic_rows = [semantic(rows[0]), semantic(rows[1], "reject"), semantic(rows[2])]
    terminal = build_terminal_artifacts(rows, semantic_rows)
    assert [row["status"] for row in terminal] == ["passed", "semantic-rejected", "passed"]
    assert all(row["semantic_evidence_sha256"] == row["semantic_evidence"]["evidence_sha256"] for row in terminal)

    terminal_path = tmp_path / "terminal.jsonl"
    write_jsonl(terminal_path, terminal)
    campaign = {"campaign_sha256": "d" * 64, "ordered_candidate_ids": [row["id"] for row in rows]}
    report = build_report(candidates, teacher, campaign, semantic_rows, terminal, [], "e" * 64)
    report_path = tmp_path / "semantic-report.json"
    report_path.write_text(json.dumps(report))
    selected, selection = select_stage(
        terminal_path, report_path, {"semantic-rejected"},
        stage="semantic", rows_hash_field="terminal_rows_sha256",
    )
    assert [row["candidate_id"] for row in selected] == [rows[1]["id"]]
    assert selection["selected_artifact_sha256s"] == [terminal[1]["artifact_sha256"]]


def test_completed_batch_rejects_reordered_semantic_rows(tmp_path: Path) -> None:
    rows = rows_fixture()[:2]
    output, evidence = tmp_path / "x.semantic.jsonl", tmp_path / "x.evidence.json"
    batch_sha = seal_batch(output, evidence, rows, "f" * 64, "go", 0)
    values = list(reversed([semantic(row) for row in rows]))
    write_jsonl(output, values)
    outer = json.loads(evidence.read_text())
    outer["semantic_output_sha256"] = hashlib.sha256(output.read_bytes()).hexdigest()
    outer.pop("evidence_sha256"); outer["evidence_sha256"] = canonical_sha256(outer)
    evidence.write_text(json.dumps(outer))
    with pytest.raises(ValueError, match="campaign contract"):
        verify_completed(output, evidence, rows, "f" * 64, batch_sha)
