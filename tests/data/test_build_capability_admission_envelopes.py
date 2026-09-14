from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.data.admit_capability_qualification import validate_envelope
from scripts.data.build_capability_admission_envelopes import (
    build_envelopes,
    load_teacher_candidates,
)
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.correct_capability_qualification_rejections import (
    REPORT_SCHEMA as CORRECTION_REPORT_SCHEMA,
    _mark_correction,
    _replace_tests,
    reference_test_critic_prompt,
)
from scripts.data.generate_capability_qualification import (
    architect_prompt,
    build_candidate,
    qualification_metadata,
    test_prompt as independent_test_prompt,
)
from scripts.eval.contracts import sha256_text


def queue_row() -> dict:
    return {
        "schema_version": "ganesh-mini-capability-qualification-draft/v1",
        "id": "cap-v2-parser-python-generation-01",
        "cell_id": "parser/python/generation", "primary_capability": "parser",
        "primary_capability_definition": "parse a bounded record format",
        "assigned_cross_cutting_dimension": "malformed_input",
        "lane": "python", "task_type": "generation", "source_queue_id": "source-1",
        "source": {
            "dataset": "fixture", "uri": "https://example.invalid/source", "revision": "abc",
            "record_id": "record-1", "license": "MIT", "license_uri": "https://example.invalid/license",
            "source_record_sha256": "a" * 64, "transformation": "training-only transformation",
        },
        "stimulus": "Create a parser in an unrelated setting.",
    }


def architecture() -> dict[str, str]:
    return {
        "id": queue_row()["id"],
        "problem": "Implement parse_flag(text: str) -> bool. Accept yes and no; reject every other value with ValueError.",
        "reference_code": "def parse_flag(text: str) -> bool:\n    if text == 'yes': return True\n    if text == 'no': return False\n    raise ValueError('invalid')",
        "known_bad_code": "def parse_flag(text: str) -> bool:\n    return text == 'yes'",
        "known_bad_label": "accepts malformed values",
    }


def fixture_test_code() -> str:
    return "from solution import parse_flag\nassert parse_flag('yes') is True\nassert parse_flag('no') is False\ntry:\n    parse_flag('x')\n    assert False\nexcept ValueError:\n    pass"


def sealed_run(kind: str, prompt: str, payload: dict) -> dict:
    final = json.dumps(payload, separators=(",", ":"))
    stdout = '{"type":"turn.completed","usage":{"input_tokens":1}}\n'
    events = [{"type": "turn.completed", "usage": {"input_tokens": 1}}]
    run = {
        "run_kind": kind, "lane": "python",
        "command_identity": [
            "codex", "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
            "--sandbox", "read-only", "-C", "/tmp/isolated",
        ],
        "prompt": prompt, "prompt_sha256": sha256_text(prompt),
        "returncode": 0, "stdout_jsonl": stdout, "stdout_sha256": sha256_text(stdout),
        "stderr": "", "stderr_sha256": sha256_text(""),
        "final_output": final, "final_output_sha256": sha256_text(final),
        "events": events, "usage": {"input_tokens": 1}, "disallowed_tool_item_types": [],
        "event_parse_error": None, "timed_out": False,
    }
    run["run_evidence_sha256"] = hashlib.sha256(
        json.dumps(run, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()
    return run


def artifacts(tmp_path: Path) -> tuple[Path, Path, dict]:
    row = queue_row()
    architect_items = [architecture()]
    architect = sealed_run(
        "capability-source-architect", architect_prompt("python", [row]), {"items": architect_items},
    )
    tester = sealed_run(
        "capability-independent-test-author", independent_test_prompt("python", architect_items),
        {"items": [{"id": row["id"], "test_code": fixture_test_code()}]},
    )
    generated = build_candidate("python", row["id"], "generation", architecture(), fixture_test_code(), source=row["source"])
    generated["qualification_assignment"] = qualification_metadata(row)
    generated["teacher_evidence"] = {
        "architect_run_evidence_sha256": architect["run_evidence_sha256"],
        "test_author_run_evidence_sha256": tester["run_evidence_sha256"],
    }
    candidate_path = tmp_path / "batch.candidates.jsonl"
    candidate_path.write_text(json.dumps(generated, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    evidence = {
        "schema_version": "ganesh-mini-capability-qualification-teacher-run/v1",
        "candidate_output_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
        "generated": 1, "failures": [],
        "selection": {
            "requested_ids": [row["id"]], "queue_row_sha256s": [canonical_sha256(row)],
            "lane": "python", "batch_size": 1, "evaluation_surfaces_read": 0,
        },
        "runs": [architect, tester],
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    evidence_path = tmp_path / "batch.evidence.json"
    evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
    return candidate_path, evidence_path, generated


def external_reports(candidate_value: dict) -> tuple[dict, dict]:
    base = {key: value for key, value in candidate_value.items() if key not in {"qualification_assignment", "teacher_evidence"}}
    candidate_sha = canonical_sha256(base)
    spec_sha = sha256_text(base["messages"][0]["content"])
    semantic = {
        "status": "complete", "evaluation_artifacts_read": 0,
        "visibility": "specification-and-assigned-labels-only",
        "records": [{
            "id": base["id"], "candidate_sha256": candidate_sha, "specification_sha256": spec_sha,
            "primary_capability": "parser", "assigned_cross_cutting_dimension": "malformed_input",
            "verdict": "pass", "primary_capability_is_substantive": True,
            "generic_edge_case_boilerplate_is_primary": False,
            "verifier_outputs_visible": False, "evaluation_artifacts_read": 0,
            "correction_passes": 0,
        }],
    }
    separation = {
        "status": "passed", "evaluation_artifacts_read_by_construction": 0,
        "comparison_manifest_sha256": "b" * 64,
        "records": [{
            "id": base["id"], "candidate_sha256": candidate_sha,
            "exact_training_passed": True, "normalized_training_passed": True,
            "fuzzy_training_passed": True, "exact_evaluation_passed": True,
            "normalized_evaluation_passed": True, "fuzzy_evaluation_passed": True,
        }],
    }
    return semantic, separation


def config() -> dict:
    return {
        "allowed_test_origins": ["independent_teacher"],
        "allowed_licenses": ["MIT"],
        "required_rights": ["prompt", "answer", "tests", "redistribution", "model_training"],
        "sources": {"fixture": {"revision": "abc", "license": "MIT"}},
        "deduplication": {"prompt_simhash_max_hamming": 3, "minimum_fuzzy_tokens": 12},
    }


def test_assembles_exact_admission_envelope_from_sealed_teacher_and_external_reviews(tmp_path: Path) -> None:
    candidate_path, evidence_path, generated = artifacts(tmp_path)
    candidates, derived, inputs = load_teacher_candidates(
        {queue_row()["id"]: queue_row()}, [candidate_path], [evidence_path],
    )
    semantic, separation = external_reports(generated)
    envelopes = build_envelopes({queue_row()["id"]: queue_row()}, candidates, derived, semantic, separation)
    candidate_value, metadata, _ = validate_envelope(
        envelopes[0], {"matrix": {"cell_contracts": []}}, {queue_row()["id"]: queue_row()}, config(),
    )
    assert candidate_value["id"] == queue_row()["id"]
    assert metadata["cell_id"] == "parser/python/generation"
    assert inputs[0]["teacher_evidence"]["evidence_sha256"]


def test_assembles_one_pass_corrected_candidate_from_sealed_parent_and_critic(tmp_path: Path) -> None:
    candidate_path, evidence_path, generated = artifacts(tmp_path)
    test_item = {"id": generated["id"], "test_code": fixture_test_code() + "\nassert parse_flag('yes')"}
    critic = sealed_run(
        "capability-reference-test-critic",
        reference_test_critic_prompt("python", [generated]),
        {"items": [test_item]},
    )
    rejection = {"id": generated["id"], "reason": "reference solution failed behavioral verification"}
    replacement = _replace_tests(generated, test_item["test_code"])
    corrected, correction_evidence = _mark_correction(
        replacement, generated, "reference-verification", critic, rejection,
    )
    corrected_path = tmp_path / "corrected.jsonl"
    corrected_path.write_bytes(json.dumps(corrected, sort_keys=True, separators=(",", ":")).encode() + b"\n")
    report = {
        "schema_version": CORRECTION_REPORT_SCHEMA,
        "status": "corrected-not-reviewed-not-admitted",
        "input": {"sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(), "records": 1},
        "source_rejections": 1, "selection_mode": "all-must-be-supported",
        "ignored_unsupported_count": 0, "ignored_unsupported": [], "critic_workers": 1,
        "requested_corrections": 1, "completed_corrections": 1,
        "corrections": [correction_evidence], "runs": [critic],
        "critic_batches": [{
            "ordinal": 0, "lane": "python", "correction_class": "reference-verification",
            "candidate_ids": [generated["id"]], "records": 1,
            "run_evidence_sha256": critic["run_evidence_sha256"],
        }],
        "output_sha256": hashlib.sha256(corrected_path.read_bytes()).hexdigest(),
        "output": {
            "path": str(corrected_path), "bytes": corrected_path.stat().st_size, "records": 1,
            "sha256": hashlib.sha256(corrected_path.read_bytes()).hexdigest(),
        },
        "evaluation_artifacts_read": 0, "failure": None,
    }
    report["report_sha256"] = canonical_sha256(report)
    report_path = tmp_path / "correction-report.json"
    report_path.write_text(json.dumps(report), encoding="utf-8")

    candidates, derived, _ = load_teacher_candidates(
        {queue_row()["id"]: queue_row()}, [candidate_path], [evidence_path],
        correction_report_path=report_path,
    )
    semantic, separation = external_reports(corrected)
    envelopes = build_envelopes(
        {queue_row()["id"]: queue_row()}, candidates, derived, semantic, separation,
    )
    candidate_value, metadata, qualification = validate_envelope(
        envelopes[0], {"matrix": {"cell_contracts": []}},
        {queue_row()["id"]: queue_row()}, config(),
    )
    assert candidate_value["verification_task"]["files"][-1]["sha256"] == sha256_text(test_item["test_code"] + "\n")
    assert metadata["correction_passes"] == 1
    assert qualification["correction"]["parent_candidate_sha256"] == correction_evidence["parent_candidate_sha256"]


def test_rejects_tampered_corrected_candidate(tmp_path: Path) -> None:
    candidate_path, evidence_path, generated = artifacts(tmp_path)
    test_item = {"id": generated["id"], "test_code": fixture_test_code() + "\nassert parse_flag('yes')"}
    critic = sealed_run(
        "capability-reference-test-critic",
        reference_test_critic_prompt("python", [generated]),
        {"items": [test_item]},
    )
    rejection = {"id": generated["id"], "reason": "reference solution failed behavioral verification"}
    corrected, correction_evidence = _mark_correction(
        _replace_tests(generated, test_item["test_code"]), generated,
        "reference-verification", critic, rejection,
    )
    corrected_path = tmp_path / "corrected.jsonl"
    corrected_path.write_bytes(json.dumps(corrected, sort_keys=True, separators=(",", ":")).encode() + b"\n")
    report = {
        "schema_version": CORRECTION_REPORT_SCHEMA,
        "status": "corrected-not-reviewed-not-admitted",
        "input": {"sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(), "records": 1},
        "source_rejections": 1, "selection_mode": "all-must-be-supported",
        "ignored_unsupported_count": 0, "ignored_unsupported": [], "critic_workers": 1,
        "requested_corrections": 1, "completed_corrections": 1,
        "corrections": [correction_evidence], "runs": [critic],
        "critic_batches": [{
            "ordinal": 0, "lane": "python", "correction_class": "reference-verification",
            "candidate_ids": [generated["id"]], "records": 1,
            "run_evidence_sha256": critic["run_evidence_sha256"],
        }],
        "output_sha256": hashlib.sha256(corrected_path.read_bytes()).hexdigest(),
        "output": {"path": str(corrected_path), "bytes": corrected_path.stat().st_size, "records": 1,
                   "sha256": hashlib.sha256(corrected_path.read_bytes()).hexdigest()},
        "evaluation_artifacts_read": 0, "failure": None,
    }
    report["report_sha256"] = canonical_sha256(report)
    report_path = tmp_path / "correction-report.json"
    report_path.write_text(json.dumps(report), encoding="utf-8")
    corrected_path.write_text(json.dumps({**corrected, "lane": "go"}) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="differs from its sealed report"):
        load_teacher_candidates(
            {queue_row()["id"]: queue_row()}, [candidate_path], [evidence_path],
            correction_report_path=report_path,
        )


def test_rejects_teacher_hash_tampering_and_non_specification_only_test_prompt(tmp_path: Path) -> None:
    candidate_path, evidence_path, _ = artifacts(tmp_path)
    evidence = json.loads(evidence_path.read_text())
    evidence["runs"][1]["prompt"] += " reference follows"
    run = evidence["runs"][1]
    run.pop("run_evidence_sha256")
    run["run_evidence_sha256"] = hashlib.sha256(
        json.dumps(run, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()
    evidence.pop("evidence_sha256")
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
    with pytest.raises(ValueError, match="prompt hash mismatch"):
        load_teacher_candidates({queue_row()["id"]: queue_row()}, [candidate_path], [evidence_path])


@pytest.mark.parametrize(
    ("target", "field", "value", "reason"),
    [
        ("semantic", "verifier_outputs_visible", True, "semantic review"),
        ("semantic", "correction_passes", 2, "correction passes"),
        ("separation", "candidate_sha256", "c" * 64, "separation"),
    ],
)
def test_fails_closed_on_review_separation_and_correction_contract(
    tmp_path: Path, target: str, field: str, value, reason: str,
) -> None:
    candidate_path, evidence_path, generated = artifacts(tmp_path)
    candidates, derived, _ = load_teacher_candidates(
        {queue_row()["id"]: queue_row()}, [candidate_path], [evidence_path],
    )
    semantic, separation = external_reports(generated)
    selected = semantic if target == "semantic" else separation
    selected["records"][0][field] = value
    with pytest.raises(ValueError, match=reason):
        build_envelopes({queue_row()["id"]: queue_row()}, candidates, derived, semantic, separation)


def test_requires_identical_candidate_sets_in_all_external_attestations(tmp_path: Path) -> None:
    candidate_path, evidence_path, generated = artifacts(tmp_path)
    candidates, derived, _ = load_teacher_candidates(
        {queue_row()["id"]: queue_row()}, [candidate_path], [evidence_path],
    )
    semantic, separation = external_reports(generated)
    separation["records"] = []
    with pytest.raises(ValueError, match="identities differ"):
        build_envelopes({queue_row()["id"]: queue_row()}, candidates, derived, semantic, separation)


def test_candidate_level_semantic_or_separation_failure_reaches_admission_as_rejection(tmp_path: Path) -> None:
    candidate_path, evidence_path, generated = artifacts(tmp_path)
    candidates, derived, _ = load_teacher_candidates(
        {queue_row()["id"]: queue_row()}, [candidate_path], [evidence_path],
    )
    semantic, separation = external_reports(generated)
    semantic["records"][0].update(
        verdict="reject",
        primary_capability_is_substantive=False,
        generic_edge_case_boilerplate_is_primary=True,
    )
    separation["status"] = "failed"
    separation["records"][0]["fuzzy_evaluation_passed"] = False

    envelopes = build_envelopes(
        {queue_row()["id"]: queue_row()}, candidates, derived, semantic, separation,
    )

    with pytest.raises(Exception, match="semantic review"):
        validate_envelope(
            envelopes[0], {"matrix": {"cell_contracts": []}},
            {queue_row()["id"]: queue_row()}, config(),
        )
