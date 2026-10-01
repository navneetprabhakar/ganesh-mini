from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts.eval.adjudicate_gate3_capability_canary import (
    MODEL_REVISION, PREPARED_DATA_SHA256, PREPARED_MANIFEST_SHA256, adjudicate,
)
from scripts.eval.contracts import ContractError, sha256_object, sha256_text


ROOT = Path(__file__).resolve().parents[2]
CANARY = ROOT / "eval/private/development/gate3_canary_manifest.json"
WORKSPACE = ROOT / "measurement/gate3/capability-scale-v1/full-pilot-eval/evaluation-workspace-v1.manifest.json"
BASE = ROOT / "measurement/inference/development/qwen3.5-2b-base-v1/tasks"


def _sealed(path: Path, value: dict, field: str) -> None:
    value[field] = sha256_object(value)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _run(path: Path, lr: str) -> dict:
    value = {
        "schema_version": "ganesh-mini-sft-run/v2", "status": "complete", "planned_end_row": 900,
        "state": {"seen_tokens": 651639, "optimizer_steps": 113},
        "save_reload": {"passed": True},
        "identities": {"phase": "lr-candidate", "learning_rate": {"1e-5": "1e-05", "3e-5": "3e-05"}[lr],
                       "prepared_data_sha256": PREPARED_DATA_SHA256,
                       "prepared_manifest_sha256": PREPARED_MANIFEST_SHA256,
                       "model_revision": MODEL_REVISION},
        "adapter_files": {"README.md": "a" * 64, "adapter_config.json": "b" * 64,
                          "adapter_model.safetensors": ("c" if lr == "1e-5" else "d") * 64},
    }
    _sealed(path, value, "evidence_sha256")
    return value


def _fixture(tmp_path: Path) -> tuple[Path, Path, Path, Path, str]:
    low_run, high_run = tmp_path / "low-run.json", tmp_path / "high-run.json"
    low, high = _run(low_run, "1e-5"), _run(high_run, "3e-5")
    low_dir, high_dir = tmp_path / "low", tmp_path / "high"
    low_dir.mkdir(); high_dir.mkdir()
    manifest = json.loads(CANARY.read_text())
    task_ids = [item["task_id"] for item in manifest["tasks"]]
    base_model = json.loads((BASE / f"{task_ids[0]}.json").read_text())["verification"]["result"]["model"]
    for lr, run, directory in (("1e-5", low, low_dir), ("3e-5", high, high_dir)):
        artifact = sha256_object({"base": base_model["artifact_sha256"], "adapter": run["adapter_files"],
                                  "run_evidence_sha256": run["evidence_sha256"]})
        for task_id in task_ids:
            envelope = copy.deepcopy(json.loads((BASE / f"{task_id}.json").read_text()))
            result = envelope["verification"]["result"]
            result["model"]["model_id"] = f"ganesh-mini-gate3-{lr}"
            result["model"]["artifact_sha256"] = artifact
            envelope["model"]["model_id"] = result["model"]["model_id"]
            envelope["model"]["artifact_sha256"] = artifact
            result.pop("result_sha256")
            result["result_sha256"] = sha256_object(result)
            envelope.pop("evidence_sha256")
            _sealed(directory / f"{task_id}.json", envelope, "evidence_sha256")
    return low_run, low_dir, high_run, high_dir, task_ids[0]


def _flip_pass(path: Path) -> None:
    envelope = json.loads(path.read_text())
    assert envelope["verification"]["result"]["passed"] is False
    result = envelope["verification"]["result"]
    verifier = result["verifier"]
    verifier["exit_codes"] = [0] * len(verifier["commands"])
    verifier["stdout"] = ""
    verifier["stdout_sha256"] = sha256_text("")
    result["passed"] = True
    result.pop("result_sha256")
    result["result_sha256"] = sha256_object(result)
    envelope.pop("evidence_sha256")
    _sealed(path, envelope, "evidence_sha256")


def _adjudicate(fixture: tuple[Path, Path, Path, Path, str]) -> dict:
    low_run, low_dir, high_run, high_dir, _ = fixture
    return adjudicate(CANARY, WORKSPACE, BASE, low_run, low_dir, high_run, high_dir)


def test_selects_lower_on_tie_and_binds_full_evidence(tmp_path: Path) -> None:
    fixture = _fixture(tmp_path)
    report = _adjudicate(fixture)
    assert report["status"] == "selected"
    assert report["selected_learning_rate"] == "1e-5"
    assert report["gate3_quality_passed"] is False
    assert report["decision_tasks_opened"] == 0
    assert report["authority"] == "selected-candidate-180-task-development-evaluation-only"
    assert len(report["task_ids"]) == 30
    assert len(report["selected_candidate"]["task_evidence"]) == 30
    seal = report.pop("report_sha256")
    assert seal == sha256_object(report)


def test_selects_higher_for_one_extra_pass_and_zero_lane_regression(tmp_path: Path) -> None:
    fixture = _fixture(tmp_path)
    _, low_dir, _, high_dir, _ = fixture
    failed = next(path for path in sorted(high_dir.glob("*.json"))
                  if json.loads(path.read_text())["verification"]["result"]["passed"] is False)
    _flip_pass(failed)
    report = _adjudicate(fixture)
    assert report["selected_learning_rate"] == "3e-5"
    assert report["decision"] == "higher_lr_improved_without_lane_regression"
    assert report["candidates"]["3e-5"]["passes"] == report["candidates"]["1e-5"]["passes"] + 1


def test_rejects_tampered_result_and_missing_task(tmp_path: Path) -> None:
    fixture = _fixture(tmp_path)
    _, low_dir, _, high_dir, task_id = fixture
    path = low_dir / f"{task_id}.json"
    data = json.loads(path.read_text()); data["verification"]["result"]["passed"] = not data["verification"]["result"]["passed"]
    path.write_text(json.dumps(data))
    with pytest.raises(ContractError):
        _adjudicate(fixture)
    path.unlink()
    with pytest.raises(ContractError, match="exactly 30"):
        _adjudicate(fixture)


def test_rejects_wrong_adapter_and_incomplete_training(tmp_path: Path) -> None:
    fixture = _fixture(tmp_path)
    high_run, high_dir = fixture[2], fixture[3]
    run = json.loads(high_run.read_text())
    run.pop("evidence_sha256"); run["save_reload"]["passed"] = False
    _sealed(high_run, run, "evidence_sha256")
    with pytest.raises(ContractError, match="incomplete"):
        _adjudicate(fixture)
    run["save_reload"]["passed"] = True
    run["adapter_files"]["adapter_model.safetensors"] = "e" * 64
    run.pop("evidence_sha256")
    _sealed(high_run, run, "evidence_sha256")
    with pytest.raises(ContractError, match="not bound"):
        _adjudicate(fixture)


def test_rejects_mutated_unselected_baseline_neither_loaded_nor_scored(tmp_path: Path) -> None:
    fixture = _fixture(tmp_path)
    baseline = tmp_path / "base"
    baseline.mkdir()
    ids = json.loads(CANARY.read_text())["tasks"]
    for item in ids:
        path = BASE / f"{item['task_id']}.json"
        (baseline / path.name).write_bytes(path.read_bytes())
    (baseline / "unselected.json").write_text("not json")
    assert adjudicate(CANARY, WORKSPACE, baseline, fixture[0], fixture[1], fixture[2], fixture[3])["status"] == "selected"
