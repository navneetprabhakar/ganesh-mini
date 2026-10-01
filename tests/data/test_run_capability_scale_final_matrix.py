from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.run_capability_scale_final_matrix import EXPECTED, run
from scripts.eval.contracts import sha256_text


def _seal(value: dict, field: str) -> dict:
    value[field] = canonical_sha256(value)
    return value


def _candidate() -> dict:
    prompt = "Implement total so it sums signed integers and rejects None."
    reference = "def total(values):\n    if values is None: raise TypeError()\n    return sum(values)\n"
    known_bad = "def total(values):\n    if values is None: raise TypeError()\n    return max(values)\n"
    return {
        "schema_version": "ganesh-mini-expansion-candidate/v1",
        "id": "scale-python-1", "lane": "python", "task_type": "repair",
        "messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": reference}],
        "source": {"dataset": "fixture", "revision": "r1", "record_id": "1", "source_record_sha256": "a" * 64},
        "rights": {"prompt": True, "answer": True, "tests": True, "redistribution": True, "model_training": True},
        "test_origin": "pending-v9-canonical-independent-author",
        "qualification_assignment": {
            "cell_id": "numeric_reasoning/python/repair", "primary_capability": "numeric_reasoning",
            "primary_capability_definition": "perform exact numeric operations",
            "assigned_cross_cutting_dimension": "malformed_input",
        },
        "verification_task": {
            "schema_version": "1.0", "task_id": "scale-python-1", "surface": "training_admission",
            "language": "python", "family": "python", "task_type": "repair",
            "prompt": {"text": prompt, "sha256": sha256_text(prompt)},
            "rendered_prompt": {"text": prompt, "sha256": sha256_text(prompt)},
            "candidate_path": "solution.py", "files": [], "runtime_id": "python-locked",
            "limits": {"timeout_seconds": 30, "memory_mb": 512, "cpus": 1, "pids": 64, "output_bytes": 65536},
            "validation": {
                "reference": {"label": "reference", "code": reference, "sha256": sha256_text(reference)},
                "known_bad": [{"label": "maximum", "code": known_bad, "sha256": sha256_text(known_bad)}],
            },
        },
    }


def _inputs(tmp_path: Path) -> argparse.Namespace:
    teacher = _candidate()
    attached = deepcopy(teacher)
    attached["test_origin"] = "independent_author-v9-canonical"
    role_values = [
        ("primary_discrimination", "roles/01-primary_discrimination/test_solution.py", "from solution import total\nassert total([2, 3]) == 5\n", ["sum", "signed"]),
        ("cross_cutting", "roles/02-cross_cutting/test_solution.py", "from solution import total\ntry:\n total(None)\nexcept TypeError:\n pass\n", ["none"]),
    ]
    roles = []
    for role, path, content, cases in role_values:
        digest = sha256_text(content)
        attached["verification_task"]["files"].append({"path": path, "role": "test", "content": content, "sha256": digest})
        roles.append({"path": path, "canonical_path": "test_solution.py", "file_sha256": digest, "role": role, "case_ids": cases})
    test_evidence = _seal({
        "candidate_sha256": canonical_sha256(attached), "test_roles": roles,
        "test_author_run_evidence_sha256": "1" * 64, "evaluation_artifacts_read": 0,
    }, "evidence_sha256")
    test_row = _seal({
        "schema_version": "fixture", "status": "structurally-valid", "candidate_id": teacher["id"],
        "evaluation_artifacts_read": 0,
    }, "artifact_sha256")
    test_evidence["test_author_artifact_sha256"] = test_row["artifact_sha256"]
    test_evidence["evidence_sha256"] = canonical_sha256({
        key: value for key, value in test_evidence.items() if key != "evidence_sha256"
    })
    delta_evidence = _seal({
        "candidate_sha256": canonical_sha256(attached), "independent_semantic_delta_count": 1,
        "delta_is_capability_specific": True, "introduces_multiple_independent_fixes": False,
        "delta_description": "sum replaces maximum", "evaluation_artifacts_read": 0,
    }, "evidence_sha256")
    delta_row = _seal({
        "schema_version": "fixture", "status": "passed", "candidate_id": teacher["id"],
        "test_attachment": test_evidence, "delta_evidence": delta_evidence, "evaluation_artifacts_read": 0,
    }, "artifact_sha256")
    candidates = tmp_path / "candidates.jsonl"
    tests = tmp_path / "tests.jsonl"
    deltas = tmp_path / "deltas.jsonl"
    attached_candidates = tmp_path / "attached-candidates.jsonl"
    runtime = tmp_path / "runtimes.json"
    candidates.write_text(json.dumps(teacher) + "\n")
    tests.write_text(json.dumps(test_row) + "\n")
    deltas.write_text(json.dumps(delta_row) + "\n")
    attached_candidates.write_text(json.dumps(attached) + "\n")
    runtime.write_text("{}")
    return argparse.Namespace(
        candidates=candidates, teacher_report=None, test_author_artifacts=tests,
        test_author_report=None, attached_candidates=attached_candidates,
        delta_artifacts=deltas, delta_report=None,
        runtimes=runtime, workers=1, run_dir=tmp_path / "runs", output_dir=tmp_path / "out",
    )


def _executor_with(outcomes: dict[str, str], calls: list[str]):
    def execute(candidate, _test, _runtime, _verifier):
        calls.append(candidate["id"])
        results = {implementation: {} for implementation in ("reference", "known_bad")}
        for implementation in results:
            for role in ("primary_discrimination", "cross_cutting"):
                passed = outcomes[f"{implementation}.{role}"] == "pass"
                results[implementation][role] = {"exit_codes": [0 if passed else 1], "timed_out": False}
        retry = _seal({"candidate_sha256": canonical_sha256(candidate), "unresolved": False}, "ledger_sha256")
        executable = _seal({
            "candidate_sha256": canonical_sha256(candidate),
            "retry_ledger_sha256": retry["ledger_sha256"], "results": results,
        }, "evidence_sha256")
        return executable, retry
    return execute


def test_passes_exact_matrix_and_resumes_without_execution(tmp_path: Path) -> None:
    args = _inputs(tmp_path)
    calls: list[str] = []
    first = run(args, executor_fn=_executor_with(EXPECTED, calls), verifier_fn=lambda *_: {})
    second = run(args, executor_fn=_executor_with(EXPECTED, calls), verifier_fn=lambda *_: {})
    assert first["status"] == "passed"
    assert first == second
    assert calls == ["scale-python-1"]
    terminal = json.loads((args.output_dir / "terminal-artifacts.jsonl").read_text())
    assert terminal["status"] == "admitted"
    assert terminal["outcomes"] == EXPECTED


def test_rejects_when_known_bad_cross_cutting_fails(tmp_path: Path) -> None:
    args = _inputs(tmp_path)
    wrong = dict(EXPECTED)
    wrong["known_bad.cross_cutting"] = "fail"
    report = run(args, executor_fn=_executor_with(wrong, []), verifier_fn=lambda *_: {})
    assert report["status"] == "failed"
    assert report["counts"] == {"rejected": 1}


def test_fails_closed_on_unsealed_delta_artifact(tmp_path: Path) -> None:
    args = _inputs(tmp_path)
    row = json.loads(args.delta_artifacts.read_text())
    row["delta_evidence"]["delta_description"] = "tampered"
    args.delta_artifacts.write_text(json.dumps(row) + "\n")
    with pytest.raises(ValueError, match="invalid artifact_sha256"):
        run(args, executor_fn=_executor_with(EXPECTED, []), verifier_fn=lambda *_: {})
