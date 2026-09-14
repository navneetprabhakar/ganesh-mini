from __future__ import annotations

import pytest

from scripts.data import correct_capability_qualification_rejections as correction
from scripts.data.build_capability_separation_attestations import _base_candidate
from scripts.data.generate_expansion_qualification import build_candidate
from scripts.data.review_capability_qualification import load_candidates


def candidate(identifier: str = "q-1") -> dict:
    architecture = {
        "id": identifier,
        "problem": "Implement add_one(value: int) -> int.",
        "reference_code": "def add_one(value: int) -> int:\n    return value + 1\n",
        "known_bad_code": "def add_one(value: int) -> int:\n    return value\n",
        "known_bad_label": "returns the input unchanged",
    }
    source = {
        "dataset": "fixture", "uri": "https://example.invalid/source", "revision": "abc",
        "record_id": identifier, "license": "MIT", "license_uri": "https://example.invalid/license",
        "source_record_sha256": "a" * 64, "transformation": "capability construction",
    }
    row = build_candidate(
        "python", identifier, "generation", architecture,
        "from solution import add_one\nassert add_one(2) == 3\n", source=source,
    )
    row["qualification_assignment"] = {
        "cell_id": "numeric/python/generation", "primary_capability": "numeric",
        "primary_capability_definition": "numeric transformations",
        "assigned_cross_cutting_dimension": "boundary", "source_queue_id": f"source-{identifier}",
    }
    row["teacher_evidence"] = {
        "architect_run_evidence_sha256": "b" * 64,
        "test_author_run_evidence_sha256": "c" * 64,
    }
    return row


def run_evidence(kind: str) -> dict:
    return {"run_kind": kind, "prompt": "fixture"}


def test_reference_failure_exposes_only_specification_and_tests_and_marks_one_pass(monkeypatch) -> None:
    original = candidate()
    parent_hash = correction.candidate_sha256(original)

    def invoke(_binary, _config, _schema, prompt, kind, _lane):
        assert kind == "capability-reference-test-critic"
        assert "specification" in prompt and "test_code" in prompt
        assert "return value + 1" not in prompt
        assert "returns the input unchanged" not in prompt
        assert "verifier" not in prompt.split("Items:", 1)[1]
        return ({"items": [{"id": "q-1", "test_code": "from solution import add_one\nassert add_one(0) == 1"}]}, run_evidence(kind))

    monkeypatch.setattr(correction, "invoke_codex", invoke)
    output, evidence, _runs = correction.correct_candidates(
        [original], [{"id": "q-1", "reason": "reference solution failed behavioral verification", "evidence": {"secret": "not-visible"}}],
        {}, "codex",
    )
    fixed = output[0]
    assert fixed["source"] == original["source"]
    assert fixed["qualification_assignment"] == original["qualification_assignment"]
    assert fixed["verification_task"]["validation"] == original["verification_task"]["validation"]
    assert fixed["teacher_evidence"]["correction_passes"] == 1
    assert fixed["teacher_evidence"]["correction"]["parent_candidate_sha256"] == parent_hash
    assert evidence[0]["visibility"] == {
        "specification_visible": True, "tests_visible": True, "reference_visible": False,
        "known_bad_visible": False, "verifier_output_visible": False, "evaluation_artifacts_read": 0,
    }
    assert evidence[0]["corrected_candidate_sha256"] == correction.candidate_sha256(fixed)


def test_known_bad_acceptance_exposes_contract_without_tests_and_rebuilds_hashes(monkeypatch) -> None:
    original = candidate()
    original_test = correction._test_file(original)["content"]

    def invoke(_binary, _config, _schema, prompt, kind, _lane):
        assert kind == "capability-known-bad-architect-critic"
        assert "reference_code" in prompt and "known_bad_code" in prompt
        assert original_test not in prompt and "test_code" not in prompt
        return ({"items": [{
            "id": "q-1", "problem": "Implement add_one(value: int) -> int.",
            "reference_code": "def add_one(value: int) -> int:\n    return value + 1",
            "known_bad_code": "def add_one(value: int) -> int:\n    return value + 2",
            "known_bad_label": "adds two instead of one",
        }]}, run_evidence(kind))

    monkeypatch.setattr(correction, "invoke_codex", invoke)
    output, evidence, _runs = correction.correct_candidates(
        [original], [{"id": "q-1", "reason": "tests accepted known-bad implementation: returns input"}],
        {}, "codex",
    )
    fixed = output[0]
    bad = fixed["verification_task"]["validation"]["known_bad"][0]
    assert bad["label"] == "adds two instead of one"
    assert bad["sha256"] != original["verification_task"]["validation"]["known_bad"][0]["sha256"]
    assert correction._test_file(fixed)["content"] == original_test
    assert evidence[0]["visibility"]["tests_visible"] is False
    assert evidence[0]["visibility"]["reference_visible"] is True
    assert evidence[0]["parent_candidate_sha256"] != evidence[0]["corrected_candidate_sha256"]


def test_fails_closed_for_unsafe_class_unknown_candidate_and_second_pass(monkeypatch) -> None:
    with pytest.raises(ValueError, match="not safely correctable"):
        correction.correct_candidates(
            [candidate()], [{"id": "q-1", "reason": "semantic review rejected candidate"}], {}, "codex",
        )
    with pytest.raises(ValueError, match="unknown candidate"):
        correction.correct_candidates(
            [candidate()], [{"id": "missing", "reason": "reference solution failed behavioral verification"}], {}, "codex",
        )
    already = candidate()
    already["teacher_evidence"]["correction_passes"] = 1
    with pytest.raises(ValueError, match="second correction"):
        correction.correct_candidates(
            [already], [{"id": "q-1", "reason": "reference solution failed behavioral verification"}], {}, "codex",
        )


def test_output_remains_consumable_by_semantic_review_and_separation(monkeypatch, tmp_path) -> None:
    first, second = candidate("q-1"), candidate("q-2")

    def invoke(*_args):
        return ({"items": [{"id": "q-1", "test_code": "assert True"}]}, run_evidence("test"))

    monkeypatch.setattr(correction, "invoke_codex", invoke)
    output, evidence, _runs = correction.correct_candidates(
        [first, second], [{"id": "q-1", "reason": "reference solution failed behavioral verification"}], {}, "codex",
    )
    assert output[1] == second
    assert "correction_passes" not in output[1]["teacher_evidence"]
    assert len(evidence) == 1
    path = tmp_path / "corrected.jsonl"
    path.write_bytes(b"".join(correction.canonical_json(row) + b"\n" for row in output))
    assert load_candidates(path) == output
    assert _base_candidate(output[0])["id"] == "q-1"


def test_architect_cannot_change_frozen_specification(monkeypatch) -> None:
    def invoke(*_args):
        item = correction._architecture(candidate())
        item["problem"] = "A different specification."
        return ({"items": [item]}, run_evidence("architect"))

    monkeypatch.setattr(correction, "invoke_codex", invoke)
    with pytest.raises(ValueError, match="changed the frozen specification"):
        correction.correct_candidates(
            [candidate()], [{"id": "q-1", "reason": "tests accepted known-bad implementation: label"}], {}, "codex",
        )


def test_critic_must_make_a_real_change(monkeypatch) -> None:
    original = candidate()

    def invoke(*_args):
        return ({"items": [{"id": "q-1", "test_code": correction._test_file(original)["content"]}]}, run_evidence("test"))

    monkeypatch.setattr(correction, "invoke_codex", invoke)
    with pytest.raises(ValueError, match="produced no candidate change"):
        correction.correct_candidates(
            [original], [{"id": "q-1", "reason": "reference solution failed behavioral verification"}], {}, "codex",
        )
