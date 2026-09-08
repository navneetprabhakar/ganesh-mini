import copy
import json

import pytest

from scripts.data import correct_recovery_tests as correction
from scripts.data.generate_expansion_qualification import build_candidate, CodexInvocationFailure


def fixture():
    source = build_candidate("python", "old", "generation", {"id": "old", "problem": "Return one.",
        "reference_code": "SECRET_REFERENCE", "known_bad_code": "SECRET_MUTANT", "known_bad_label": "bad"}, "OLD_TEST")
    row = {"id": "new", "lane": "python", "parent_id": "parent", "parent_source": source["source"],
           "parent_candidate_sha256": "0" * 64}
    feedback = {"new": {"specification_review": "Cover the required boundary."}}
    return source, {"records": [row]}, feedback


def test_correction_context_is_specification_tests_only(monkeypatch, tmp_path):
    source, plan, feedback = fixture()
    unchanged = copy.deepcopy(source)
    def invoke(binary, config, schema, prompt, phase, lane):
        assert "SECRET_REFERENCE" not in prompt and "SECRET_MUTANT" not in prompt
        assert "OLD_TEST" in prompt and "Cover the required boundary" in prompt
        return {"items": [{"id": "new", "test_code": "NEW_TEST"}]}, {"prompt": prompt}
    monkeypatch.setattr(correction, "invoke_codex", invoke)
    rows = correction.correct(plan, {"new": source}, feedback, {"execution": {}}, "unused", tmp_path)
    assert source == unchanged
    assert rows[0]["messages"] == source["messages"]
    assert rows[0]["verification_task"]["validation"] == source["verification_task"]["validation"]
    assert rows[0]["verification_task"]["files"][0]["content"] == "NEW_TEST\n"
    assert rows[0]["verification_task"]["task_id"] == "new"
    assert json.loads((tmp_path / "new.candidate.json").read_text()) == rows[0]


def test_failed_correction_preserves_raw_evidence(monkeypatch, tmp_path):
    source, plan, feedback = fixture()
    def fail(*args):
        raise CodexInvocationFailure("failed", {"raw": "partial"})
    monkeypatch.setattr(correction, "invoke_codex", fail)
    with pytest.raises(CodexInvocationFailure):
        correction.correct(plan, {"new": source}, feedback, {"execution": {}}, "unused", tmp_path)
    assert json.loads((tmp_path / "python-recovery-test-correction-evidence.json").read_text()) == {"raw": "partial"}
    assert not (tmp_path / "candidates.jsonl").exists()
