import json
import subprocess

import pytest

from scripts.data import generate_versioned_recovery as recovery
from scripts.data.generate_expansion_qualification import (
    ARCHITECT_SCHEMA, CodexInvocationFailure, build_candidate, invoke_codex,
)
from scripts.data.plan_versioned_recovery import digest, make_plan


def fixture():
    parent = build_candidate("python", "exp-v1-python-generation-0001", "generation", {
        "id": "exp-v1-python-generation-0001", "problem": "Implement x returning one.",
        "reference_code": "REFERENCE_SECRET", "known_bad_code": "BUG_SECRET", "known_bad_label": "wrong value",
    }, "PARENT_TEST_SECRET")
    parents = recovery.canonical_json(parent) + b"\n"
    holds = recovery.canonical_json({"holds": [{"id": parent["id"], "reason": "reference error"}]})
    request = {"version": "r1", "parent_corpus_sha256": digest(parents), "hold_ledger_sha256": digest(holds),
               "selections": [{"parent_id": parent["id"], "parent_candidate_sha256": digest(recovery.canonical_json(parent)),
                               "change_class": "reference-fix", "rationale": "Return the specified value",
                               "review_evidence": "review.md", "review_evidence_sha256": digest(b"review")}]}
    plan = make_plan(parents, holds, recovery.canonical_json(request))
    return parent, parents, holds, plan


def test_version_is_reserved_across_different_plans(tmp_path):
    *_, plan = fixture()
    directory = recovery.reserve_version(tmp_path, plan)
    with pytest.raises(FileExistsError):
        recovery.reserve_version(tmp_path, {**plan, "records": []})
    assert json.loads((directory / "plan.json").read_text()) == plan


def test_generation_separates_tests_and_preserves_lineage(monkeypatch, tmp_path):
    parent, _, _, plan = fixture()
    directory = recovery.reserve_version(tmp_path, plan)
    prompts = []
    def invoke(binary, config, schema, prompt, phase, lane):
        prompts.append(prompt)
        id = plan["records"][0]["id"]
        item = ({"id": id, "problem": parent["messages"][0]["content"],
                 "reference_code": "DERIVED_REFERENCE_SECRET", "known_bad_code": "DERIVED_BUG_SECRET", "known_bad_label": "bad"}
                if schema == ARCHITECT_SCHEMA else {"id": id, "test_code": "INDEPENDENT_TEST"})
        return {"items": [item]}, {"raw": phase, "prompt": prompt}
    monkeypatch.setattr(recovery, "invoke_codex", invoke)
    rows = recovery.generate(plan, {parent["id"]: parent}, {"execution": {"batch_size": 10}}, "unused", directory)
    assert len(rows) == 1
    assert "REFERENCE_SECRET" in prompts[0]
    assert all(secret not in prompts[1] for secret in ("REFERENCE_SECRET", "BUG_SECRET", "PARENT_TEST_SECRET"))
    assert rows[0]["messages"][0] == parent["messages"][0]
    assert rows[0]["source"]["revision"] == parent["source"]["revision"]
    assert rows[0]["rights"] == parent["rights"]
    assert plan["records"][0]["parent_candidate_sha256"] in rows[0]["source"]["transformation"]
    assert (directory / "python-recovery-architect-evidence.json").exists()
    assert (directory / "python-recovery-independent-tests-evidence.json").exists()


def test_failed_teacher_evidence_is_preserved(monkeypatch, tmp_path):
    parent, _, _, plan = fixture()
    directory = recovery.reserve_version(tmp_path, plan)
    def fail(*args):
        raise CodexInvocationFailure("failed", {"stdout_jsonl": "partial raw events"})
    monkeypatch.setattr(recovery, "invoke_codex", fail)
    with pytest.raises(CodexInvocationFailure):
        recovery.generate(plan, {parent["id"]: parent}, {"execution": {}}, "unused", directory)
    assert json.loads((directory / "python-recovery-architect-evidence.json").read_text())["stdout_jsonl"] == "partial raw events"
    assert not (directory / "candidates.jsonl").exists()


def test_reference_fix_cannot_change_prompt(monkeypatch, tmp_path):
    parent, _, _, plan = fixture()
    directory = recovery.reserve_version(tmp_path, plan)
    def changed(*args):
        return {"items": [{"id": plan["records"][0]["id"], "problem": "weakened", "reference_code": "R", "known_bad_code": "B", "known_bad_label": "bug"}]}, {"raw": "kept"}
    monkeypatch.setattr(recovery, "invoke_codex", changed)
    with pytest.raises(ValueError, match="changed the frozen problem"):
        recovery.generate(plan, {parent["id"]: parent}, {"execution": {}}, "unused", directory)


def test_quality_closure_is_bound_to_current_inputs(monkeypatch, tmp_path):
    parent, parents, holds, plan = fixture()
    (tmp_path / "review.md").write_bytes(b"review")
    closure = {"status": "original-systematic-review-complete-not-admission",
               "parent_corpus_sha256": digest(parents), "hold_ledger_sha256": digest(holds),
               "inputs": {"review.md": digest(b"review")}}
    closure["closure_sha256"] = digest(recovery.canonical_json(closure))
    monkeypatch.setattr(recovery, "EXPECTED_SHA", digest(parents))
    assert recovery.validate_inputs(plan, closure, parents, holds, tmp_path) == {parent["id"]: parent}
    with pytest.raises(ValueError, match="ledger changed"):
        recovery.validate_inputs(plan, closure, parents, holds + b" ", tmp_path)


def test_timeout_keeps_partial_streams_and_final_file(monkeypatch):
    def timeout(command, **kwargs):
        from pathlib import Path
        Path(command[command.index("-o") + 1]).write_text('{"partial":true}')
        raise subprocess.TimeoutExpired(command, 1, output=b"partial events", stderr=b"partial stderr")
    monkeypatch.setattr(subprocess, "run", timeout)
    config = {"model": "test", "reasoning_effort": "medium", "service_tier": "priority", "execution": {"timeout_seconds": 1}}
    with pytest.raises(CodexInvocationFailure) as caught:
        invoke_codex("unused", config, ARCHITECT_SCHEMA, "prompt", "test", "python")
    evidence = caught.value.evidence
    assert evidence["timed_out"] is True and evidence["returncode"] is None
    assert evidence["stdout_jsonl"] == "partial events"
    assert evidence["stderr"] == "partial stderr"
    assert evidence["final_output"] == '{"partial":true}'
