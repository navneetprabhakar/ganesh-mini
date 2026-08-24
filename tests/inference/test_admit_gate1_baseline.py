from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.inference.admit_gate1_baseline import admit, canonical_sha256, file_sha256


EXECUTION_SHA = "a" * 64
RUN_SHA = "b" * 64


def write_sealed(path: Path, value: dict, field: str) -> dict:
    value = dict(value)
    value[field] = canonical_sha256(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return value


def finalization_fixture(tmp_path: Path, *, terminal_status: str = "passed") -> tuple[Path, dict, dict]:
    run_dir = tmp_path / "finalization"
    output = run_dir / "terminal-download" / "output" / "campaign" / "baseline"
    output.mkdir(parents=True)
    (output / "run.json").write_text("{}\n", encoding="utf-8")
    (output / "tasks").mkdir()
    (output / "tasks" / "task.json").write_text("{}\n", encoding="utf-8")
    validation = write_sealed(
        run_dir / "terminal-validation.json",
        {
            "schema_version": "ganesh-mini-gate1-terminal-validation/v1",
            "status": terminal_status,
            "attempt_id": "gate1-test",
            "expected_prefix": "gs://bucket/gate1/run/runtime-terminal-gate1-test",
            "execution_sha256": EXECUTION_SHA,
            "run": {"run_sha256": RUN_SHA} if terminal_status == "passed" else None,
        },
        "evidence_sha256",
    )
    finalization = write_sealed(
        run_dir / "finalization.json",
        {
            "schema_version": "ganesh-mini-gate1-gcloud-finalization/v1",
            "status": "complete",
            "execution_sha256": EXECUTION_SHA,
            "terminal_validation_sha256": validation["evidence_sha256"],
        },
        "evidence_sha256",
    )
    finalization_path = run_dir / "finalization.json"
    write_sealed(
        run_dir / "post-delete-final-backup-manifest.json",
        {
            "status": "verified",
            "prefix": "gs://bucket/gate1/run/post-delete",
            "objects": [
                {
                    "object_uri": "gs://bucket/gate1/run/post-delete/finalization.json",
                    "downloaded_sha256": file_sha256(finalization_path),
                    "verified": True,
                }
            ],
        },
        "evidence_sha256",
    )
    return run_dir, validation, finalization


@patch("scripts.inference.admit_gate1_baseline.validate_completed_run", return_value={"run_sha256": RUN_SHA})
@patch("scripts.inference.admit_gate1_baseline.build_readiness")
def test_admits_successful_finalized_baseline_atomically(
    build_readiness, _validate, tmp_path: Path
) -> None:
    run_dir, validation, finalization = finalization_fixture(tmp_path)
    root = tmp_path / "repo"
    readiness = {"schema_version": "ganesh-mini-readiness/v1", "status": "ready", "failed_checks": []}
    readiness["evidence_sha256"] = canonical_sha256(readiness)
    build_readiness.return_value = readiness

    evidence = admit(run_dir, root)

    target = root / "measurement/inference/development/qwen3.5-2b-base-v1"
    assert (target / "run.json").read_text() == "{}\n"
    assert (target / "tasks/task.json").is_file()
    assert evidence["status"] == "admitted"
    assert evidence["terminal_validation_sha256"] == validation["evidence_sha256"]
    assert evidence["finalization_sha256"] == finalization["evidence_sha256"]
    assert evidence["admitted_file_count"] == 2
    assert json.loads((root / "measurement/gate1/readiness.json").read_text())["status"] == "ready"
    assert json.loads((root / "measurement/gate1/baseline_admission.json").read_text())["evidence_sha256"] == evidence["evidence_sha256"]


def test_rejects_sealed_failure_before_copy(tmp_path: Path) -> None:
    run_dir, _, _ = finalization_fixture(tmp_path, terminal_status="sealed-failure")
    root = tmp_path / "repo"
    with pytest.raises(ValueError, match="validated Gate 1 baseline"):
        admit(run_dir, root)
    assert not (root / "measurement/inference/development/qwen3.5-2b-base-v1").exists()


@patch("scripts.inference.admit_gate1_baseline.validate_completed_run", return_value={"run_sha256": RUN_SHA})
def test_refuses_to_overwrite_existing_canonical_baseline(_validate, tmp_path: Path) -> None:
    run_dir, _, _ = finalization_fixture(tmp_path)
    root = tmp_path / "repo"
    target = root / "measurement/inference/development/qwen3.5-2b-base-v1"
    target.mkdir(parents=True)
    with pytest.raises(FileExistsError, match="already exists"):
        admit(run_dir, root)
