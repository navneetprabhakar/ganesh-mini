from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.repair_delta_v7_readiness import inject_controller_paths
from scripts.data.run_capability_scale_delta_audits import attach_tests, run
from scripts.eval.contracts import sha256_text


def _candidate() -> dict:
    reference = "package solution\n\nfunc Add(a, b int) int { return a + b }\n"
    known_bad = "package solution\n\nfunc Add(a, b int) int { return a - b }\n"
    source_sha = "a" * 64
    assignment = {
        "cell_id": "numeric_reasoning/go/generation",
        "primary_capability": "numeric_reasoning",
        "primary_capability_definition": "perform exact numeric computation",
        "assigned_cross_cutting_dimension": "boundary_conditions",
        "source_queue_id": "queue-1",
        "source_record_sha256": source_sha,
        "queue_row_sha256": "b" * 64,
        "assignment_sha256": "c" * 64,
    }
    prompt = "Implement Add with Go integers."
    return {
        "schema_version": "ganesh-mini-expansion-candidate/v1",
        "id": "scale-go-1",
        "lane": "go",
        "task_type": "generation",
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": reference},
        ],
        "source": {"source_record_sha256": source_sha},
        "qualification_assignment": assignment,
        "verification_task": {
            "files": [{
                "path": "go.mod", "role": "support",
                "content": "module invalid.local/test\n\ngo 1.22\n",
                "sha256": sha256_text("module invalid.local/test\n\ngo 1.22\n"),
            }],
            "validation": {
                "reference": {"code": reference, "sha256": sha256_text(reference)},
                "known_bad": [{"code": known_bad, "sha256": sha256_text(known_bad)}],
            },
        },
    }


def _test_artifact(candidate: dict) -> dict:
    response = {
        "primary_discrimination": {
            "content": "package solution\n\nimport \"testing\"\nfunc TestAdd(t *testing.T) { if Add(2, 3) != 5 { t.Fatal() }; if Add(-2, 3) != 1 { t.Fatal() } }\n",
            "case_ids": ["positive", "signed"],
        },
        "cross_cutting": {
            "content": "package solution\n\nimport \"testing\"\nfunc TestBoundary(t *testing.T) { if Add(0, 0) != 0 { t.Fatal() } }\n",
            "case_ids": ["zero-boundary"],
        },
    }
    value = {
        "schema_version": "ganesh-mini-capability-scale-test-author-artifact/v1",
        "candidate_id": candidate["id"],
        "candidate_sha256": canonical_sha256(candidate),
        "status": "structurally-valid",
        "injection": inject_controller_paths(candidate["lane"], response),
        "evaluation_artifacts_read": 0,
    }
    value["artifact_sha256"] = canonical_sha256(value)
    return value


def _args(tmp_path: Path, candidates: Path, tests: Path) -> argparse.Namespace:
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"codex_cli_version": "unused", "model": "test"}))
    return argparse.Namespace(
        candidates=candidates,
        test_author_artifacts=tests,
        test_author_report=None,
        codex_config=config,
        codex_bin="unused",
        workers=1,
        run_dir=tmp_path / "runs",
        output_dir=tmp_path / "out",
    )


def _write_inputs(tmp_path: Path) -> tuple[Path, Path, dict]:
    candidate = _candidate()
    test_artifact = _test_artifact(candidate)
    candidates = tmp_path / "candidates.jsonl"
    tests = tmp_path / "tests.jsonl"
    candidates.write_text(json.dumps(candidate) + "\n")
    tests.write_text(json.dumps(test_artifact) + "\n")
    return candidates, tests, candidate


def test_attach_tests_binds_canonical_roles_and_hashes() -> None:
    candidate = _candidate()
    attached, evidence = attach_tests(candidate, _test_artifact(candidate))
    tests = [row for row in attached["verification_task"]["files"] if row["role"] == "test"]
    assert [row["path"] for row in tests] == [
        "roles/01-primary_discrimination/solution_test.go",
        "roles/02-cross_cutting/solution_test.go",
    ]
    assert [row["role"] for row in evidence["test_roles"]] == [
        "primary_discrimination", "cross_cutting",
    ]
    assert evidence["evaluation_artifacts_read"] == 0


def test_run_seals_pass_and_resumes_without_another_call(tmp_path: Path) -> None:
    candidates, tests, _ = _write_inputs(tmp_path)
    args = _args(tmp_path, candidates, tests)
    calls: list[str] = []

    def factory(projection: dict, prompt: str):
        def invoke(_: dict):
            calls.append(projection["id"])
            return ({
                "independent_semantic_delta_count": 1,
                "delta_is_capability_specific": True,
                "introduces_multiple_independent_fixes": False,
                "delta_description": "subtraction is replaced by addition",
            }, {"prompt_sha256": sha256_text(prompt), "evaluation_artifacts_read": 0})
        return invoke

    first = run(args, factory)
    second = run(args, factory)
    assert first["status"] == "passed"
    assert first["new_calls"] == 1 and first["resumed"] == 0
    assert second["new_calls"] == 0 and second["resumed"] == 1
    assert calls == ["scale-go-1"]
    terminal = json.loads((args.run_dir / "scale-go-1.delta-audit.json").read_text())
    body = dict(terminal)
    assert body.pop("artifact_sha256") == canonical_sha256(body)
    assert terminal["lineage"]["queue_row_sha256"] == "b" * 64
    assert terminal["evaluation_artifacts_read"] == 0


def test_invalid_response_is_terminally_sealed(tmp_path: Path) -> None:
    candidates, tests, _ = _write_inputs(tmp_path)
    args = _args(tmp_path, candidates, tests)

    def factory(_projection: dict, _prompt: str):
        return lambda _: ({"unexpected": True}, {"raw": "preserved"})

    report = run(args, factory)
    assert report["status"] == "failed"
    assert report["counts"] == {"response-contract-rejected": 1}
    artifact = json.loads((args.run_dir / "scale-go-1.delta-audit.json").read_text())
    assert artifact["status"] == "response-contract-rejected"


def test_provider_shape_exception_is_terminally_sealed(tmp_path: Path) -> None:
    candidates, tests, _ = _write_inputs(tmp_path)
    args = _args(tmp_path, candidates, tests)

    def factory(_projection: dict, _prompt: str):
        def invoke(_: dict):
            raise ValueError("provider output is not an object")
        return invoke

    report = run(args, factory)
    assert report["counts"] == {"response-contract-rejected": 1}
    artifact = json.loads((args.run_dir / "scale-go-1.delta-audit.json").read_text())
    assert artifact["reason"] == "provider-output-contract: provider output is not an object"


def test_rejects_unbound_or_noncanonical_test_artifact() -> None:
    candidate = _candidate()
    artifact = _test_artifact(candidate)
    artifact["candidate_sha256"] = "0" * 64
    artifact.pop("artifact_sha256")
    artifact["artifact_sha256"] = canonical_sha256(artifact)
    with pytest.raises(ValueError, match="does not bind"):
        attach_tests(candidate, artifact)
