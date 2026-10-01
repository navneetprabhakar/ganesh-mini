from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.data.run_capability_scale_test_author import (
    load_teacher_inputs,
    run_one,
    write_response_schema,
)


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "measurement/gate3/capability-scale-v1"
QUEUE = BASE / "source-queue.jsonl"
QUEUE_MANIFEST = BASE / "source-queue-manifest.json"
TEACHER = BASE / "canary-v1/teacher"


def _inputs() -> tuple[list[dict], dict]:
    return load_teacher_inputs(
        QUEUE,
        QUEUE_MANIFEST,
        TEACHER / "candidates.jsonl",
        TEACHER / "teacher-report.json",
    )


def _valid_go_response() -> dict:
    return {
        "cross_cutting": {
            "content": "package solution\nimport \"testing\"\nfunc TestCross(t *testing.T) {}\n",
            "case_ids": ["cross-one"],
        },
        "primary_discrimination": {
            "content": "package solution\nimport \"testing\"\nfunc TestPrimary(t *testing.T) {}\n",
            "case_ids": ["primary-one", "primary-two"],
        },
    }


def test_load_teacher_inputs_binds_exact_canary_cohort() -> None:
    candidates, report = _inputs()
    assert len(candidates) == 12
    assert report["status"] == "passed"
    assert [candidate["teacher_evidence"]["request_sha256"] for candidate in candidates] == report[
        "selected_request_sha256s"
    ]


def test_load_teacher_inputs_rejects_candidate_drift(tmp_path: Path) -> None:
    candidates = [json.loads(line) for line in (TEACHER / "candidates.jsonl").read_text().splitlines()]
    candidates[0]["lane"] = "python"
    path = tmp_path / "candidates.jsonl"
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in candidates))
    with pytest.raises(ValueError, match="sealed aggregate"):
        load_teacher_inputs(QUEUE, QUEUE_MANIFEST, path, TEACHER / "teacher-report.json")


def test_run_one_seals_and_resumes_structurally_valid_response(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    candidate = _inputs()[0][0]
    config = json.loads((ROOT / "configs/data/expansion_teacher.json").read_text())
    schema = tmp_path / "schema.json"
    schema_sha = write_response_schema(schema)
    calls = []

    def fake_invoke(*args, **kwargs):
        calls.append((args, kwargs))
        return _valid_go_response(), {"command": ["codex"], "exit_code": 0}

    monkeypatch.setattr("scripts.data.run_capability_scale_test_author.invoke_codex", fake_invoke)
    artifact = run_one(
        candidate, config, "codex", "codex-cli 0.144.4", schema, schema_sha, tmp_path,
    )
    assert artifact["status"] == "structurally-valid"
    assert [role["role"] for role in artifact["injection"]["roles"]] == [
        "primary_discrimination", "cross_cutting",
    ]
    assert artifact["evaluation_artifacts_read"] == 0
    resumed = run_one(
        candidate, config, "codex", "codex-cli 0.144.4", schema, schema_sha, tmp_path,
    )
    assert resumed == artifact
    assert len(calls) == 1


def test_run_one_seals_structural_rejection(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    candidate = _inputs()[0][0]
    config = json.loads((ROOT / "configs/data/expansion_teacher.json").read_text())
    schema = tmp_path / "schema.json"
    schema_sha = write_response_schema(schema)
    invalid = _valid_go_response()
    invalid["primary_discrimination"]["content"] = "package main\n"
    monkeypatch.setattr(
        "scripts.data.run_capability_scale_test_author.invoke_codex",
        lambda *args, **kwargs: (invalid, {"command": ["codex"], "exit_code": 0}),
    )
    artifact = run_one(
        candidate, config, "codex", "codex-cli 0.144.4", schema, schema_sha, tmp_path,
    )
    assert artifact["status"] == "structural-rejected"
    assert "go-package" in artifact["reason"]
    assert artifact["artifact_sha256"]


def test_run_one_seals_provider_output_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    candidate = _inputs()[0][0]
    config = json.loads((ROOT / "configs/data/expansion_teacher.json").read_text())
    schema = tmp_path / "schema.json"
    schema_sha = write_response_schema(schema)

    def reject(*args, **kwargs):
        raise ValueError("structured output is not an object")

    monkeypatch.setattr("scripts.data.run_capability_scale_test_author.invoke_codex", reject)
    artifact = run_one(
        candidate, config, "codex", "codex-cli 0.144.4", schema, schema_sha, tmp_path,
    )
    assert artifact["status"] == "invocation-failed"
    assert artifact["reason"] == "provider-output-contract: structured output is not an object"
    assert artifact["artifact_sha256"]
