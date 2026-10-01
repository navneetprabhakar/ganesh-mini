from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.eval.contracts import sha256_object
from scripts.eval import prepare_gate3_candidate_evaluation as stage


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def seal(value: dict, field: str) -> dict:
    value = dict(value)
    value[field] = sha256_object(value)
    return value


def fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path, Path, Path, Path]:
    monkeypatch.setattr(stage, "ROOT", tmp_path)
    write_json(tmp_path / "configs/model/qwen3_5_2b.contract.json", {"revision": "pinned"})
    archive = tmp_path / "workspace.tar.gz"
    archive.write_bytes(b"development-only archive")
    task_rows = []
    canary_rows = []
    for index in range(180):
        path = f"eval/private/development/tranche{1 if index < 30 else 2}/task-{index:03}.task.json"
        task_rows.append({"path": path, "sha256": "a" * 64})
        if index < 30:
            canary_rows.append({"path": path, "task_id": f"dev-{index:03}",
                                "task_file_sha256": "a" * 64})
    workspace = seal({"schema_version": "ganesh-mini-development-evaluation-workspace/v1",
                      "status": "sealed", "surface": "development", "task_count": 180,
                      "archive": {"path": "workspace.tar.gz", "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()},
                      "files": task_rows + [{"path": f"scripts/eval/file-{index}.py", "sha256": "b" * 64}
                                            for index in range(407)]},
                     "manifest_sha256")
    monkeypatch.setattr(stage, "WORKSPACE_SEAL", workspace["manifest_sha256"])
    workspace_path = tmp_path / "workspace.json"
    write_json(workspace_path, workspace)
    canary = seal({"schema_version": "ganesh-mini-gate3-canary/v1", "status": "frozen",
                   "surface": "development", "records": 30, "training_admission_allowed": False,
                   "tasks": canary_rows}, "manifest_sha256")
    canary_path = tmp_path / "canary.json"
    write_json(canary_path, canary)
    run_paths = []
    for lr, name in (("1e-5", "a"), ("3e-5", "b")):
        attempt = tmp_path / f"attempt-{lr}"
        adapter = attempt / "terminal-roundtrip/output/training/adapter-final"
        adapter.mkdir(parents=True)
        (adapter / "adapter_config.json").write_text(name, encoding="utf-8")
        run = seal({"schema_version": "ganesh-mini-sft-run/v2", "status": "complete",
                    "planned_end_row": 900,
                    "state": {"next_row": 900, "seen_tokens": 651639, "optimizer_steps": 113},
                    "save_reload": {"passed": True},
                    "identities": {"learning_rate": stage.EXPECTED_RUNS[lr], "model_revision": "pinned",
                                   "prepared_data_sha256": "data", "prepared_manifest_sha256": "manifest",
                                   "recipe_sha256": "recipe", "validation_data_sha256": "validation"},
                    "adapter_files": {"adapter_config.json": hashlib.sha256(name.encode()).hexdigest()}},
                   "evidence_sha256")
        run_path = adapter.parent / "run-evidence.json"
        write_json(run_path, run)
        write_json(attempt / "finalization.json", {
            "status": "terminal-backup-verified-and-exact-resources-absent-twice", "training_exit_code": 0})
        objects = [{"object_uri": f"gs://test/terminal/output/training/{relative}",
                    "verified": True, "verified_download_sha256": hashlib.sha256(source.read_bytes()).hexdigest()}
                   for source, relative in ((run_path, "run-evidence.json"),
                                            (adapter / "adapter_config.json", "adapter-final/adapter_config.json"))]
        objects += [{"object_uri": f"gs://test/terminal/other-{index}", "verified": True}
                    for index in range(52)]
        write_json(attempt / "terminal-backup-verification.json",
                   seal({"schema_version": "ganesh-mini-gcs-backup-manifest/v1", "status": "verified",
                         "object_count": 54, "objects": objects}, "evidence_sha256"))
        run_paths.append(run_path)
    return workspace_path, canary_path, run_paths[0], run_paths[1], tmp_path / "stage"


def test_prepare_canary_only_and_reject_overwrite(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    args = fixture(tmp_path, monkeypatch)
    card = stage.prepare(*args)
    assert card["status"] == "prepared-only"
    assert sorted(card["configs"]) == ["canary-1e-5.json", "canary-3e-5.json"]
    assert card["decision_tasks_opened"] == 0
    assert card["candidate_input_bundle"]["sha256"] == stage.file_sha256(args[4] / "candidate-inputs.tar.gz")
    with pytest.raises(ValueError, match="output already exists"):
        stage.prepare(*args)


def test_prepare_rejects_unsealed_training_or_missing_backup(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    args = fixture(tmp_path, monkeypatch)
    run = json.loads(args[2].read_text())
    run["state"]["seen_tokens"] -= 1
    write_json(args[2], run)
    with pytest.raises(ValueError, match="invalid evidence_sha256"):
        stage.prepare(*args)
    run["evidence_sha256"] = sha256_object({key: value for key, value in run.items() if key != "evidence_sha256"})
    write_json(args[2], run)
    with pytest.raises(ValueError, match="completed"):
        stage.prepare(*args)


def test_development_requires_exact_selected_run(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    args = fixture(tmp_path, monkeypatch)
    workspace = json.loads(args[0].read_text())
    canary = json.loads(args[1].read_text())
    low = json.loads(args[2].read_text())
    high = json.loads(args[3].read_text())
    task_evidence = {row["task_id"]: "c" * 64 for row in canary["tasks"]}
    base_artifact = "f" * 64
    models = {lr: {"artifact_sha256": sha256_object({
        "base": base_artifact, "adapter": run["adapter_files"],
        "run_evidence_sha256": run["evidence_sha256"]}), "revision": "pinned"}
        for lr, run in (("1e-5", low), ("3e-5", high))}
    selected = {"run_evidence_sha256": low["evidence_sha256"], "adapter_files": low["adapter_files"],
                "model": models["1e-5"],
                "result_collection_sha256": "d" * 64, "task_evidence": task_evidence}
    selection = seal({"schema_version": "ganesh-mini-capability-canary-selection/v1",
                      "status": "selected", "authority": "selected-candidate-180-task-development-evaluation-only",
                      "gate3_quality_passed": False, "decision_tasks_opened": 0,
                      "evaluation_workspace_manifest_sha256": workspace["manifest_sha256"],
                      "canary_manifest_sha256": canary["manifest_sha256"],
                      "base": {"model": {"artifact_sha256": base_artifact}},
                      "selected_learning_rate": "1e-5", "selected_candidate": selected,
                      "candidates": {lr: {"run_evidence_sha256": run["evidence_sha256"],
                                          "adapter_files": run["adapter_files"],
                                          "model": models[lr],
                                          "task_evidence": task_evidence,
                                          "result_collection_sha256": "d" * 64 if lr == "1e-5" else "e" * 64}
                                     for lr, run in (("1e-5", low), ("3e-5", high))},
                      "task_ids": sorted(row["task_id"] for row in canary["tasks"])}, "report_sha256")
    selection_path = tmp_path / "selection.json"
    write_json(selection_path, selection)
    card = stage.prepare(*args, selection_path)
    assert "development-1e-5.json" in card["configs"]
    assert (args[4] / "selection-report.json").read_bytes() == selection_path.read_bytes()
    assert card["selection_report_artifact"] == {
        "path": "selection-report.json",
        "sha256": hashlib.sha256(selection_path.read_bytes()).hexdigest(),
        "report_sha256": selection["report_sha256"],
    }
    selection["selected_candidate"]["run_evidence_sha256"] = "0" * 64
    selection["report_sha256"] = sha256_object({key: value for key, value in selection.items() if key != "report_sha256"})
    write_json(selection_path, selection)
    with pytest.raises(ValueError, match="exact sealed canary selection"):
        stage.prepare(*args[:-1], tmp_path / "other-stage", selection_path)
