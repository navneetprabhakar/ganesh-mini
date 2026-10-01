from __future__ import annotations

import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.data.admit_repair_delta import AdmissionFailure, validate_runtime_harness_closure
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.generate_expansion_qualification import CodexInvocationFailure
from scripts.data.run_repair_delta_evidence import (
    _add_tests,
    _add_tests_v5,
    _response_schema,
    _stage_prompt,
    add_tests_for_contract,
    IsolatedCodexAdapter,
    StageInvocationFailure,
    V5_CONTRACT_ID,
    V5_INVOCATION_CORRECTION_SCHEMA,
    V5_INVOCATION_FAILURE_SCHEMA,
    V5_TEST_AUTHOR_RESPONSE_SCHEMA_VERSION,
    load_campaign_inputs,
    load_separation_sidecars,
)


ROOT = Path(__file__).resolve().parents[2]


def write_primary_inputs(tmp_path: Path, records: int = 60):
    queue = []
    for index in range(120):
        role = "primary" if index < 60 else "reserve"
        cell_index = index if index < 60 else index - 60
        cell = f"cap-{cell_index // 6}/lane-{cell_index % 6}/repair"
        queue.append({
            "id": f"id-{index}", "role": role, "cell_id": cell,
            "contract_id": "capability-stratified-v3-repair-delta/v1",
        })
    queue_path = tmp_path / "queue.jsonl"
    queue_path.write_text("".join(json.dumps(row) + "\n" for row in queue))
    manifest = {
        "schema_version": "ganesh-mini-repair-delta-queue-manifest/v1",
        "plan_sha256": "4023a896300112f9f93f2a16698d549f203e3e75b4e71ae054f3a98463e2f0f0",
        "queue_sha256": hashlib.sha256(queue_path.read_bytes()).hexdigest(), "assignments": 120,
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    manifest_path = tmp_path / "queue-manifest.json"
    manifest_path.write_text(json.dumps(manifest))
    generated = [{"candidate": {"id": f"id-{index}"}, "repair_delta_proof": {}} for index in range(records)]
    candidate_path = tmp_path / "teacher.jsonl"
    candidate_path.write_text("".join(json.dumps(row) + "\n" for row in generated))
    evidence = {
        "schema_version": "ganesh-mini-repair-delta-teacher-batch/v1",
        "plan_sha256": manifest["plan_sha256"], "queue_manifest_sha256": manifest["manifest_sha256"],
        "role": "primary", "candidate_output_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
        "requested_ids": [f"id-{index}" for index in range(records)], "generated": records,
        "failures": [], "evaluation_artifacts_read": 0,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    evidence_path = tmp_path / "teacher-evidence.json"
    evidence_path.write_text(json.dumps(evidence))
    return queue_path, manifest_path, candidate_path, evidence_path, manifest


def test_loads_exact_sealed_primary_campaign_and_rejects_cardinality(tmp_path: Path) -> None:
    queue, manifest, candidates, evidence, sealed_manifest = write_primary_inputs(tmp_path)
    generated, assignments, loaded = load_campaign_inputs(
        queue, manifest, [candidates], [evidence], "primary",
    )
    assert len(generated) == len(assignments) == 60
    assert loaded["manifest_sha256"] == sealed_manifest["manifest_sha256"]

    other = tmp_path / "short"
    other.mkdir()
    queue, manifest, candidates, evidence, _ = write_primary_inputs(other, 59)
    with pytest.raises(ValueError, match="exactly all 60"):
        load_campaign_inputs(queue, manifest, [candidates], [evidence], "primary")


def test_teacher_batch_content_drift_and_unpaired_batches_fail_closed(tmp_path: Path) -> None:
    queue, manifest, candidates, evidence, _ = write_primary_inputs(tmp_path)
    with pytest.raises(ValueError, match="pairs"):
        load_campaign_inputs(queue, manifest, [candidates], [], "primary")
    candidates.write_text(candidates.read_text() + "{}\n")
    with pytest.raises(ValueError, match="teacher batch"):
        load_campaign_inputs(queue, manifest, [candidates], [evidence], "primary")


def test_isolated_codex_adapter_seals_and_resumes_exact_projection(tmp_path: Path) -> None:
    config = {"model": "fixture", "codex_cli_version": "fixture"}
    calls = []

    def invoke(binary, config_value, schema_path, prompt, stage, lane):
        calls.append((binary, stage, lane, json.loads(schema_path.read_text())))
        return {
            "repair_delta_requires_primary_capability": True,
            "scheduled_dimension_is_concrete_and_secondary": True,
            "known_bad_already_satisfies_scheduled_dimension": True,
            "cross_dimension_only_patch_cannot_solve": True,
            "capability_remains_substantive_without_cross_clause": True,
            "generic_boilerplate_is_not_primary": True,
            "rationale": "fixture",
        }, {"prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(), "raw_output": "fixture"}

    projection = {
        "id": "safe-id", "specification": "repair it", "embedded_known_bad": "bad",
        "primary_capability": "numeric", "assigned_cross_cutting_dimension": "malformed",
    }
    with patch("scripts.data.run_repair_delta_evidence.invoke_codex", side_effect=invoke):
        adapter = IsolatedCodexAdapter("semantic_review", config, "codex-fixture", tmp_path, "codex 1")
        first = adapter(projection)
        second = adapter(projection)
    assert first == second and len(calls) == 1
    artifact = json.loads((tmp_path / "safe-id.semantic_review.json").read_text())
    body = dict(artifact); claimed = body.pop("artifact_sha256")
    assert claimed == canonical_sha256(body)
    assert artifact["evaluation_artifacts_read"] == 0

    changed = dict(projection, specification="drift")
    with pytest.raises(ValueError, match="run drift"):
        adapter(changed)


def test_v5_test_author_adapter_uses_strict_schema_and_versioned_cache(tmp_path: Path) -> None:
    captured = {}

    def invoke(_binary, _config, schema_path, prompt, _stage, _lane):
        captured["schema"] = json.loads(schema_path.read_text())
        captured["prompt"] = prompt
        return {
            "primary_discrimination": {
                "path": "primary.py", "content": "assert True", "case_ids": ["a", "b"],
            },
            "cross_cutting": {
                "path": "cross.py", "content": "try:\n raise ValueError()\nexcept ValueError:\n pass",
                "case_ids": ["malformed"],
            },
        }, {"raw_output": "fixture"}

    projection = {
        "id": "v5-safe", "lane": "python", "specification": "repair",
        "embedded_known_bad": "bad", "primary_capability": "numeric",
        "assigned_cross_cutting_dimension": "malformed",
    }
    with patch("scripts.data.run_repair_delta_evidence.invoke_codex", side_effect=invoke):
        adapter = IsolatedCodexAdapter(
            "test_author", {"model": "fixture"}, "codex", tmp_path, "codex 1", "v5",
        )
        adapter(projection)
    assert captured["schema"]["$id"] == V5_TEST_AUTHOR_RESPONSE_SCHEMA_VERSION
    assert "exactly the two named objects" in captured["prompt"]
    artifact = json.loads((tmp_path / "v5-safe.test_author.json").read_text())
    assert artifact["contract_version"] == "v5"
    schema_sha = canonical_sha256(captured["schema"])
    assert artifact["response_schema_sha256"] == schema_sha
    assert artifact["input_sha256"] == canonical_sha256({
        "stage": "test_author", "projection": projection,
        "prompt": captured["prompt"], "contract_version": "v5",
        "response_schema_sha256": schema_sha,
    })

    changed_schema = json.loads(json.dumps(captured["schema"]))
    changed_schema["properties"]["cross_cutting"]["properties"]["case_ids"]["maxItems"] = 9
    with patch(
        "scripts.data.run_repair_delta_evidence._response_schema",
        return_value=changed_schema,
    ):
        with pytest.raises(ValueError, match="sealed Codex run drift"):
            adapter(projection)


def test_v5_adapter_persists_candidate_local_failure_and_resumes_without_reinvocation(
    tmp_path: Path,
) -> None:
    calls = []
    projection = {
        "id": "v5-failure", "lane": "python", "specification": "repair",
        "embedded_known_bad": "bad", "primary_capability": "numeric",
        "assigned_cross_cutting_dimension": "malformed",
    }

    def fail(*_args):
        calls.append(1)
        raise CodexInvocationFailure("transport failed", {
            "stdout_jsonl": "", "stderr": "connection reset", "events": [],
            "event_parse_error": None, "final_output": "", "timed_out": False,
        })

    with patch("scripts.data.run_repair_delta_evidence.invoke_codex", side_effect=fail):
        adapter = IsolatedCodexAdapter(
            "semantic_review", {"model": "fixture"}, "codex", tmp_path, "codex 1", "v5",
        )
        with pytest.raises(StageInvocationFailure) as first:
            adapter(projection)
        with pytest.raises(StageInvocationFailure) as second:
            adapter(projection)
    assert len(calls) == 1
    assert first.value.evidence == second.value.evidence
    artifact = first.value.evidence
    assert artifact["schema_version"] == V5_INVOCATION_FAILURE_SCHEMA
    assert artifact["response_schema_sha256"] == canonical_sha256(
        _response_schema("semantic_review", "v5")
    )
    assert artifact["attempts"][0]["structured_model_response_observed"] is False
    assert artifact["attempts"][0]["thread_observed"] is False
    assert artifact["attempts"][0]["run"]["stderr"] == "connection reset"


def test_v5_adapter_allows_one_explicit_identical_replay_only_without_response_or_thread(
    tmp_path: Path,
) -> None:
    correction_dir = tmp_path / "corrections"
    correction_dir.mkdir()
    run_dir = tmp_path / "runs"
    projection = {
        "id": "v5-replay", "lane": "python", "specification": "repair",
        "embedded_known_bad": "bad", "primary_capability": "numeric",
        "assigned_cross_cutting_dimension": "malformed",
    }
    response = {
        "repair_delta_requires_primary_capability": True,
        "scheduled_dimension_is_concrete_and_secondary": True,
        "known_bad_already_satisfies_scheduled_dimension": True,
        "cross_dimension_only_patch_cannot_solve": True,
        "capability_remains_substantive_without_cross_clause": True,
        "generic_boilerplate_is_not_primary": True,
        "rationale": "fixture",
    }
    calls = []

    def invoke(*_args):
        calls.append(1)
        if len(calls) == 1:
            raise CodexInvocationFailure("pre-thread transport failure", {
                "stdout_jsonl": "", "stderr": "unavailable", "events": [],
                "event_parse_error": None, "final_output": "", "timed_out": False,
            })
        return response, {"stdout_jsonl": "fixture", "events": [], "final_output": json.dumps(response)}

    with patch("scripts.data.run_repair_delta_evidence.invoke_codex", side_effect=invoke):
        adapter = IsolatedCodexAdapter(
            "semantic_review", {"model": "fixture"}, "codex", run_dir, "codex 1", "v5",
            correction_dir,
        )
        with pytest.raises(StageInvocationFailure) as caught:
            adapter(projection)
        failed = caught.value.evidence
        contract = {
            "schema_version": V5_INVOCATION_CORRECTION_SCHEMA,
            "contract_id": V5_CONTRACT_ID, "candidate_id": projection["id"],
            "stage": "semantic_review", "input_sha256": failed["input_sha256"],
            "failed_artifact_sha256": failed["artifact_sha256"],
            "maximum_total_attempts": 2, "identical_replay_required": True,
            "authorize_one_replay": True,
            "structured_model_response_observed": False, "thread_observed": False,
            "evaluation_artifacts_read": 0,
        }
        contract["contract_sha256"] = canonical_sha256(contract)
        (correction_dir / "v5-replay.semantic_review.json").write_text(json.dumps(contract))
        result = adapter(projection)
        cached = adapter(projection)
    assert result == cached
    assert len(calls) == 2
    artifact = json.loads((run_dir / "v5-replay.semantic_review.json").read_text())
    assert len(artifact["invocation_attempts"]) == 2
    assert artifact["invocation_attempts"][0] == failed["attempts"][0]
    assert artifact["correction_contract_sha256"] == contract["contract_sha256"]


@pytest.mark.parametrize("observed", ["thread", "response"])
def test_v5_adapter_refuses_replay_when_model_work_was_observed(
    tmp_path: Path, observed: str,
) -> None:
    correction_dir = tmp_path / "corrections"; correction_dir.mkdir()
    projection = {
        "id": "v5-ineligible", "lane": "python", "specification": "repair",
        "embedded_known_bad": "bad", "primary_capability": "numeric",
        "assigned_cross_cutting_dimension": "malformed",
    }
    calls = []
    run = {
        "stdout_jsonl": "fixture", "stderr": "failed", "event_parse_error": None,
        "events": ([{"type": "thread.started", "thread_id": "thread-1"}] if observed == "thread" else []),
        "final_output": ("{\"answer\":true}" if observed == "response" else ""),
    }

    def fail(*_args):
        calls.append(1)
        raise CodexInvocationFailure("failed", run)

    with patch("scripts.data.run_repair_delta_evidence.invoke_codex", side_effect=fail):
        adapter = IsolatedCodexAdapter(
            "semantic_review", {"model": "fixture"}, "codex", tmp_path / "runs", "codex 1",
            "v5", correction_dir,
        )
        with pytest.raises(StageInvocationFailure) as caught:
            adapter(projection)
        failed = caught.value.evidence
        contract = {
            "schema_version": V5_INVOCATION_CORRECTION_SCHEMA,
            "contract_id": V5_CONTRACT_ID, "candidate_id": projection["id"],
            "stage": "semantic_review", "input_sha256": failed["input_sha256"],
            "failed_artifact_sha256": failed["artifact_sha256"],
            "maximum_total_attempts": 2, "identical_replay_required": True,
            "authorize_one_replay": True,
            "structured_model_response_observed": False, "thread_observed": False,
            "evaluation_artifacts_read": 0,
        }
        contract["contract_sha256"] = canonical_sha256(contract)
        (correction_dir / "v5-ineligible.semantic_review.json").write_text(json.dumps(contract))
        with pytest.raises(StageInvocationFailure):
            adapter(projection)
    assert len(calls) == 1


def test_separation_sidecars_are_sealed_and_candidate_bound(tmp_path: Path) -> None:
    candidate = {"id": "safe-id", "value": 1}
    row = {
        "candidate_id": "safe-id", "candidate_sha256": canonical_sha256(candidate),
        "comparison_contract_sha256": "9" * 64,
        "evaluation_artifacts_read_by_construction": 0,
    }
    row["evidence_sha256"] = canonical_sha256(row)
    path = tmp_path / "separation.jsonl"
    path.write_text(json.dumps(row) + "\n")
    lookup = load_separation_sidecars(path, "9" * 64)
    assert lookup(candidate)["evidence_sha256"] == row["evidence_sha256"]
    with pytest.raises(ValueError, match="absent"):
        lookup({"id": "safe-id", "value": 2})


def test_pinned_runtime_commands_close_all_six_canonical_test_paths(tmp_path: Path) -> None:
    runtime_path = ROOT / "configs/eval/runtimes.json"
    assert validate_runtime_harness_closure(runtime_path) == {
        "go": "go-1.22.12", "java": "java-21.0.11",
        "javascript": "javascript-node-22.23.2",
        "typescript": "typescript-5.5.4-node-22", "python": "python-3.11.15",
        "rust": "rust-1.85.0",
    }

    broken = json.loads(runtime_path.read_text())
    broken["runtimes"]["java-21.0.11"]["commands"] = [["javac", "Solution.java"]]
    broken_path = tmp_path / "broken-runtimes.json"
    broken_path.write_text(json.dumps(broken))
    with pytest.raises(AdmissionFailure, match="does not consume canonical java"):
        validate_runtime_harness_closure(broken_path)


def test_test_author_requires_one_logical_file_per_role_and_java_entrypoint() -> None:
    candidate = {
        "lane": "python", "messages": [{"content": "repair"}],
        "verification_task": {
            "files": [],
            "validation": {"known_bad": [{"sha256": "a" * 64}]},
        },
    }
    assignment = {
        "primary_capability": "numeric_reasoning",
        "assigned_cross_cutting_dimension": "malformed_input",
    }
    primary = {
        "path": "authored-primary.py", "content": "assert True",
        "role": "primary_discrimination", "case_ids": ["a", "b"],
    }
    cross = {
        "path": "authored-cross.py", "content": "assert True",
        "role": "cross_cutting", "case_ids": ["c"],
    }
    updated, evidence = _add_tests(candidate, assignment, {"files": [primary, cross]}, "1" * 64)
    assert [row["canonical_path"] for row in evidence["test_roles"]] == [
        "test_solution.py", "test_solution.py",
    ]
    assert [item["path"] for item in updated["verification_task"]["files"]] == [
        "authored-primary.py", "authored-cross.py",
    ]

    with pytest.raises(ValueError, match="exactly one file"):
        _add_tests(candidate, assignment, {"files": [primary, cross, dict(primary, path="extra.py")]}, "1" * 64)

    java = dict(candidate, lane="java")
    with pytest.raises(ValueError, match="SolutionTest entry point"):
        _add_tests(java, assignment, {"files": [primary, cross]}, "1" * 64)


def v5_test_candidate(lane: str) -> dict:
    suffix = {
        "java": "java", "typescript": "ts", "go": "go", "python": "py",
    }[lane]
    return {
        "lane": lane, "messages": [{"content": "repair the implementation"}],
        "verification_task": {
            "files": [],
            "validation": {"known_bad": [{"sha256": "a" * 64}]},
        },
        "logical_suffix": suffix,
    }


def v5_assignment() -> dict:
    return {
        "primary_capability": "numeric_reasoning",
        "assigned_cross_cutting_dimension": "malformed_input",
    }


def test_v5_schema_has_exact_named_roles_and_prompt_agrees() -> None:
    schema = _response_schema("test_author", "v5")
    assert schema["$id"] == V5_TEST_AUTHOR_RESPONSE_SCHEMA_VERSION
    assert schema["additionalProperties"] is False
    assert schema["required"] == ["primary_discrimination", "cross_cutting"]
    assert set(schema["properties"]) == {"primary_discrimination", "cross_cutting"}
    assert schema["properties"]["primary_discrimination"]["properties"]["case_ids"] == {
        "type": "array", "minItems": 2,
        "items": {"type": "string", "minLength": 1},
    }
    assert "uniqueItems" not in json.dumps(schema)
    assert schema["properties"]["cross_cutting"]["properties"]["case_ids"]["minItems"] == 1
    prompt = _stage_prompt("test_author", {"lane": "typescript"}, "v5")
    assert "exactly the two named objects" in prompt
    assert "no files array" in prompt and "node:test" in prompt
    assert "primary defect" in prompt
    assert _response_schema("test_author", "v3") == _response_schema("test_author", "v4")


def test_v5_named_roles_build_exact_two_files_and_go_primary_cases() -> None:
    candidate = v5_test_candidate("go")
    response = {
        "primary_discrimination": {
            "path": "primary_test.go",
            "content": "package solution\nfunc TestPrimary(t *testing.T) { t.Run(\"a\", func(t *testing.T) {}); t.Run(\"b\", func(t *testing.T) {}) }",
            "case_ids": ["positive", "signed"],
        },
        "cross_cutting": {
            "path": "cross_test.go",
            "content": "package solution\nfunc TestMalformed(t *testing.T) { _, err := Compute(nil); if err == nil { t.Fatal(\"want error\") } }",
            "case_ids": ["nil"],
        },
    }
    updated, evidence = _add_tests_v5(candidate, v5_assignment(), response, "1" * 64)
    assert [row["path"] for row in updated["verification_task"]["files"]] == [
        "primary_test.go", "cross_test.go",
    ]
    assert [row["role"] for row in evidence["test_roles"]] == [
        "primary_discrimination", "cross_cutting",
    ]
    assert evidence["response_schema_version"] == V5_TEST_AUTHOR_RESPONSE_SCHEMA_VERSION

    duplicate_cases = json.loads(json.dumps(response))
    duplicate_cases["primary_discrimination"]["case_ids"] = ["same", "same"]
    with pytest.raises(ValueError, match="distinct case IDs"):
        _add_tests_v5(candidate, v5_assignment(), duplicate_cases, "1" * 64)


def test_v5_rejects_prior_three_file_array_response() -> None:
    old_response = {"files": [
        {"path": f"test-{index}.py", "content": "pass", "case_ids": [str(index)]}
        for index in range(3)
    ]}
    with pytest.raises(ValueError, match="exactly two named role objects"):
        _add_tests_v5(v5_test_candidate("python"), v5_assignment(), old_response, "1" * 64)
    assignment = {**v5_assignment(), "contract_id": V5_CONTRACT_ID}
    with pytest.raises(ValueError, match="exactly two named role objects"):
        add_tests_for_contract(v5_test_candidate("python"), assignment, old_response, "1" * 64)


def test_v5_rejects_bad_java_entrypoint() -> None:
    response = {
        "primary_discrimination": {
            "path": "Primary.java", "content": "class PrimaryTest { public static void main(String[] args) {} }",
            "case_ids": ["one", "two"],
        },
        "cross_cutting": {
            "path": "Cross.java", "content": "class SolutionTest { static void main(String[] args) {} }",
            "case_ids": ["malformed"],
        },
    }
    with pytest.raises(ValueError, match="SolutionTest"):
        _add_tests_v5(v5_test_candidate("java"), v5_assignment(), response, "1" * 64)


@pytest.mark.parametrize("module", ["node:test", "node:assert/strict", "external-test-package"])
def test_v5_rejects_typescript_unavailable_imports(module: str) -> None:
    response = {
        "primary_discrimination": {
            "path": "primary.ts", "content": f'import helper from "{module}";\nvoid helper;\n',
            "case_ids": ["one", "two"],
        },
        "cross_cutting": {
            "path": "cross.ts", "content": "import { compute } from './solution';\ntry { compute(null); } catch {}\n",
            "case_ids": ["malformed"],
        },
    }
    with pytest.raises(ValueError, match="self-contained"):
        _add_tests_v5(v5_test_candidate("typescript"), v5_assignment(), response, "1" * 64)


def test_v5_rejects_primary_dependent_cross_test() -> None:
    response = {
        "primary_discrimination": {
            "path": "primary_test.go",
            "content": "package solution\nfunc TestPrimary(t *testing.T) { t.Run(\"a\", func(t *testing.T) {}); t.Run(\"b\", func(t *testing.T) {}) }",
            "case_ids": ["positive", "signed"],
        },
        "cross_cutting": {
            "path": "cross_test.go",
            "content": "package solution\nfunc TestEmpty(t *testing.T) { got := ComputeTotal([]int{}); if got != 0 { t.Fatal(got) } }",
            "case_ids": ["empty"],
        },
    }
    with pytest.raises(ValueError, match="asserts primary behavior"):
        _add_tests_v5(v5_test_candidate("go"), v5_assignment(), response, "1" * 64)


def test_v5_rejects_extra_named_role_property() -> None:
    response = {
        "primary_discrimination": {
            "path": "primary.py", "content": "assert True", "case_ids": ["one", "two"],
            "extra": "forbidden",
        },
        "cross_cutting": {
            "path": "cross.py", "content": "try:\n raise ValueError()\nexcept ValueError:\n pass",
            "case_ids": ["malformed"],
        },
    }
    with pytest.raises(ValueError, match="only path, content, and case_ids"):
        _add_tests_v5(v5_test_candidate("python"), v5_assignment(), response, "1" * 64)
