import pytest

from scripts.data.repair_expansion_rejections import (
    ANSWER_SUFFIX,
    architecture,
    base_problem,
    classify_rejection,
    corrected_source,
    reference_repair_prompt,
)


def candidate() -> dict:
    return {
        "id": "x", "lane": "python", "task_type": "generation",
        "source": {"dataset": "pinned", "transformation": "source-driven synthesis"},
        "messages": [{"role": "user", "content": "Implement x." + ANSWER_SUFFIX}, {"role": "assistant", "content": "GOOD"}],
        "verification_task": {
            "files": [{"role": "test", "content": "assert x() == 1"}],
            "validation": {
                "reference": {"code": "GOOD"},
                "known_bad": [{"code": "BAD", "label": "returns zero"}],
            },
        },
    }


def test_classifies_only_teacher_repairable_rejections() -> None:
    assert classify_rejection("reference solution failed behavioral verification") == "reference"
    assert classify_rejection("tests accepted known-bad implementation: bug") == "tests"
    with pytest.raises(ValueError, match="not teacher-repairable"):
        classify_rejection("exact evaluation prompt overlap")


def test_extracts_architecture_and_frozen_problem() -> None:
    row = candidate()
    assert base_problem(row) == "Implement x."
    assert architecture(row) == {
        "id": "x", "problem": "Implement x.", "reference_code": "GOOD",
        "known_bad_code": "BAD", "known_bad_label": "returns zero",
    }


def test_corrected_source_preserves_lineage_without_mutating_input() -> None:
    row = candidate()
    corrected = corrected_source(row, "reference corrected")
    assert corrected == {"dataset": "pinned", "transformation": "source-driven synthesis; reference corrected"}
    assert row["source"]["transformation"] == "source-driven synthesis"


def test_reference_repair_uses_independent_test_evidence() -> None:
    row = candidate()
    rejection = {
        "x": {"evidence": {"reference": {"exit_codes": [1], "stderr": "failed"}}},
    }
    prompt = reference_repair_prompt("python", [row], rejection)
    assert "assert x() == 1" in prompt
    assert "GOOD" in prompt
    assert "BAD" in prompt
    assert "failed" in prompt
