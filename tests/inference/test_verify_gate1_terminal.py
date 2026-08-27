from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.inference.run_development_baseline_host import canonical_sha256
from scripts.inference.verify_gate1_terminal import validate_gate3_success, verify


PREFIX = "gs://bucket/gate1/runtime-terminal-attempt"


def write_sealed(path: Path, value: dict, field: str) -> dict:
    value = dict(value)
    value[field] = canonical_sha256(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")
    return value


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture(tmp_path: Path, controller_code: int | None = 0, startup_code: int | None = None) -> tuple[Path, Path, Path]:
    root = tmp_path / "download"
    output = root / "output" / "campaign" / "baseline"
    output.mkdir(parents=True)
    run = write_sealed(output / "run.json", {
        "schema_version": "ganesh-mini-inference-run/v2",
        "classification": "private_development_baseline",
        "model": {"model_id": "Qwen/Qwen3.5-2B", "revision": "15852e8c16360a2fea060d615a32b45270f8a8fc"},
        "task_accounting": {"expected": 180, "completed": 180, "passed": 1, "failed": 179, "pending": 0},
        "tasks": [{"task_id": f"task-{index}"} for index in range(180)],
    }, "run_sha256")
    write_sealed(output / "host-execution.json", {
        "schema_version": "ganesh-mini-development-baseline-host/v1",
        "status": "passed",
        "attempt_id": "attempt",
        "run": {"run_sha256": run["run_sha256"], "task_accounting": run["task_accounting"]},
    }, "evidence_sha256")
    write_sealed(root / "output" / "campaign" / "campaign-result.json", {
        "schema_version": "ganesh-mini-staged-campaign-result/v1", "status": "passed", "attempt_id": "attempt"
    }, "evidence_sha256")
    (root / "startup-exit-code.txt").write_text(f"{controller_code if startup_code is None else startup_code}\n")
    if controller_code is not None:
        (root / "controller-exit-code.txt").write_text(f"{controller_code}\n")
    (root / "controller.stderr.log").write_text("diagnostic\n")
    files = [path for path in root.rglob("*") if path.is_file()]
    inventory = root / "runtime-files.sha256"
    inventory.write_text("".join(f"{sha(path)}  ./{path.relative_to(root)}\n" for path in sorted(files)))
    files.append(inventory)
    rows = [{"object_uri": f"{PREFIX}/{path.relative_to(root)}", "downloaded_sha256": sha(path), "verified": True} for path in files]
    manifest = {"schema_version": "ganesh-mini-gcs-backup-manifest/v1", "status": "verified", "project": "p", "prefix": PREFIX, "object_count": len(rows), "objects": rows}
    manifest["evidence_sha256"] = canonical_sha256(manifest)
    manifest_path = tmp_path / "manifest.json"; manifest_path.write_text(json.dumps(manifest))
    card = {"schema_version": "ganesh-mini-staged-gcloud-execution/v1", "status": "authorized-executable", "gate": 1, "gate_range": [1,3], "execution": {"attempt_id": "attempt"}}
    card["execution_sha256"] = canonical_sha256(card)
    card_path = tmp_path / "card.json"; card_path.write_text(json.dumps(card))
    return root, manifest_path, card_path


def gate3_fixture(tmp_path: Path, promotion_status: str = "promote") -> tuple[Path, Path, Path]:
    root = tmp_path / "download"
    campaign_root = root / "output" / "campaign"
    card = {
        "schema_version": "ganesh-mini-gate3-gcloud-execution/v3",
        "status": "authorized-executable",
        "gate": 3,
        "gate_range": [3, 3],
        "model": {"model_id": "Qwen/Qwen3.5-2B", "revision": "15852e8c16360a2fea060d615a32b45270f8a8fc"},
        "training": {
            "lr_candidates": [0.00001, 0.00003],
            "imported_lr_candidates": [0.00001],
            "trained_lr_candidates": [0.00003],
            "lr_candidate_seen_tokens_each": 461235,
            "unique_train_records": 1399,
            "completed_candidate_manifest_sha256": "a" * 64,
        },
        "execution": {"attempt_id": "attempt"},
    }
    card_path = tmp_path / "card.json"
    selected = 0.00001
    label = "lr-1e-5"
    lanes = ("go", "java", "javascript", "typescript", "python", "rust")

    def evaluation(run_label: str, count: int) -> tuple[dict, str, dict[str, int]]:
        destination = campaign_root / "evaluation" / run_label
        summaries = []
        result_seals: dict[str, str] = {}
        lane_passes = {lane_name: 0 for lane_name in lanes}
        for index in range(count):
            task_id = f"task-{index}"
            lane_name = lanes[index % len(lanes)]
            passed = index < count // 6
            result = {"task_id": task_id, "language": lane_name, "passed": passed}
            result["result_sha256"] = canonical_sha256(result)
            evidence = write_sealed(destination / "tasks" / f"{task_id}.json", {
                "verification": {"result": result},
            }, "evidence_sha256")
            summaries.append({
                "task_id": task_id, "passed": passed, "status": "complete",
                "evidence_sha256": evidence["evidence_sha256"],
            })
            result_seals[task_id] = result["result_sha256"]
            lane_passes[lane_name] += passed
        run = write_sealed(destination / "run.json", {
            "schema_version": "ganesh-mini-inference-run/v2",
            "classification": "private_candidate_development",
            "model": {"model_id": "ganesh-mini-1.0-candidate", "revision": card["model"]["revision"]},
            "task_accounting": {"expected": count, "completed": count, "passed": sum(row["passed"] for row in summaries), "failed": sum(not row["passed"] for row in summaries), "pending": 0},
            "tasks": summaries,
        }, "run_sha256")
        return run, canonical_sha256([result_seals[task_id] for task_id in sorted(result_seals)]), lane_passes

    selection_candidates = {}
    for learning_rate in card["training"]["lr_candidates"]:
        candidate_label = f"lr-{learning_rate:.0e}".replace("e-0", "e-")
        adapter_path = campaign_root / "training" / candidate_label / "adapter-final" / "adapter_model.safetensors"
        adapter_path.parent.mkdir(parents=True, exist_ok=True)
        adapter_path.write_bytes(f"adapter-{learning_rate}".encode())
        training = write_sealed(campaign_root / "training" / candidate_label / "run-evidence.json", {
            "schema_version": "ganesh-mini-sft-run/v2", "status": "complete",
            "identities": {"phase": "lr-candidate", "learning_rate": str(learning_rate)},
            "state": {"seen_tokens": 461235}, "planned_end_row": 1399,
            "save_reload": {"passed": True},
            "adapter_files": {"adapter_model.safetensors": sha(adapter_path)},
        }, "evidence_sha256")
        canary, collection, lane_passes = evaluation(f"{candidate_label}-canary", 30)
        selection_candidates[str(learning_rate)] = {
            "run_evidence_sha256": training["evidence_sha256"],
            "result_collection_sha256": collection,
            "passed": canary["task_accounting"]["passed"],
            "lanes": lane_passes,
        }
        if learning_rate == 0.00001:
            card["training"]["completed_candidate_run_evidence_sha256"] = training["evidence_sha256"]
    write_sealed(campaign_root / "lr-selection.json", {
        "schema_version": "ganesh-mini-lr-selection/v2", "status": "selected",
        "surface": "development-canary", "expected_task_count": 30,
        "selected_learning_rate": selected, "candidates": selection_candidates,
    }, "evidence_sha256")
    evaluation(f"{label}-full", 180)
    promotion_checks = [
        "four_of_five_families_improve", "no_lane_regression",
        "quality_failures_do_not_increase", "retention_slice",
        "sft_complete_and_reload_reproduced",
    ]
    write_sealed(campaign_root / "pilot-promotion.json", {
        "schema_version": "ganesh-mini-pilot-promotion/v1", "status": promotion_status,
        "failed_checks": [] if promotion_status == "promote" else ["no_lane_regression"],
        "checks": [{"name": name, "passed": promotion_status == "promote"} for name in promotion_checks],
    }, "evidence_sha256")
    phase_names = {
        "workspace-isolation", "gate1-canonical-baseline", "verifier-runtime-images",
        "gate3-training-admission",
        "import-lr-1e-5", "evaluate-lr-1e-5-canary", "train-lr-3e-5",
        "evaluate-lr-3e-5-canary", "lr-selection", "evaluate-lr-1e-5-full",
        "gate3-promotion",
    }
    write_sealed(campaign_root / "campaign-result.json", {
        "schema_version": "ganesh-mini-staged-campaign-result/v1", "status": "passed",
        "attempt_id": "attempt", "phases": [
            {
                "name": name,
                "status": "passed",
                "evidence": {
                    "manifest_sha256": "a" * 64,
                    "run_evidence_sha256": card["training"]["completed_candidate_run_evidence_sha256"],
                } if name == "import-lr-1e-5" else {},
            }
            for name in sorted(phase_names)
        ],
    }, "evidence_sha256")
    card["execution_sha256"] = canonical_sha256(card)
    card_path.write_text(json.dumps(card))
    (root / "startup-exit-code.txt").write_text("0\n")
    (root / "controller-exit-code.txt").write_text("0\n")
    (root / "controller.stderr.log").write_text("diagnostic\n")
    files = [path for path in root.rglob("*") if path.is_file()]
    inventory = root / "runtime-files.sha256"
    inventory.write_text("".join(f"{sha(path)}  ./{path.relative_to(root)}\n" for path in sorted(files)))
    files.append(inventory)
    prefix = "gs://bucket/gate3/runtime-terminal-attempt"
    rows = [{"object_uri": f"{prefix}/{path.relative_to(root)}", "downloaded_sha256": sha(path), "verified": True} for path in files]
    manifest = {"schema_version": "ganesh-mini-gcs-backup-manifest/v1", "status": "verified", "project": "p", "prefix": prefix, "object_count": len(rows), "objects": rows}
    manifest["evidence_sha256"] = canonical_sha256(manifest)
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))
    return root, manifest_path, card_path


def test_accepts_exact_successful_terminal_backup(tmp_path: Path) -> None:
    root, manifest, card = fixture(tmp_path)
    evidence = verify(manifest, root, card, PREFIX)
    assert evidence["status"] == "passed"
    assert evidence["run"]["task_accounting"]["completed"] == 180
    assert evidence["deletion_eligible"] is True


def test_accepts_sealed_failure_for_deletion_but_not_as_gate1_pass(tmp_path: Path) -> None:
    root, manifest, card = fixture(tmp_path, controller_code=7)
    evidence = verify(manifest, root, card, PREFIX)
    assert evidence["status"] == "sealed-failure"
    assert evidence["run"]["task_accounting"]["completed"] == 180
    assert evidence["deletion_eligible"] is True


def test_accepts_sealed_failure_before_controller_start(tmp_path: Path) -> None:
    root, manifest, card = fixture(tmp_path, controller_code=None, startup_code=9)
    evidence = verify(manifest, root, card, PREFIX)
    assert evidence["status"] == "sealed-failure"
    assert evidence["controller_exit_code"] is None


def test_rejects_download_drift(tmp_path: Path) -> None:
    root, manifest, card = fixture(tmp_path)
    (root / "controller.stderr.log").write_text("changed\n")
    with pytest.raises(ValueError, match="downloaded terminal artifact mismatch"):
        verify(manifest, root, card, PREFIX)


def test_accepts_gate3_success_without_regenerating_a_baseline(tmp_path: Path) -> None:
    root, manifest, card = gate3_fixture(tmp_path)
    prefix = "gs://bucket/gate3/runtime-terminal-attempt"
    evidence = verify(manifest, root, card, prefix)
    assert evidence["schema_version"] == "ganesh-mini-gate3-terminal-validation/v2"
    assert evidence["status"] == "passed"
    assert evidence["run"]["task_accounting"]["completed"] == 180
    assert evidence["run"]["selected_learning_rate"] == 0.00001


def test_rejects_gate3_success_without_promotion(tmp_path: Path) -> None:
    root, manifest, card = gate3_fixture(tmp_path, promotion_status="reject")
    with pytest.raises(ValueError, match="promotion evidence"):
        verify(manifest, root, card, "gs://bucket/gate3/runtime-terminal-attempt")


def test_gate3_success_requires_the_nonselected_training_artifact(tmp_path: Path) -> None:
    root, _, card_path = gate3_fixture(tmp_path)
    (root / "output/campaign/training/lr-3e-5/run-evidence.json").unlink()
    with pytest.raises(FileNotFoundError):
        validate_gate3_success(root / "output/campaign", json.loads(card_path.read_text()))


def test_gate3_selection_must_bind_the_exact_canary_collection(tmp_path: Path) -> None:
    root, _, card_path = gate3_fixture(tmp_path)
    selection_path = root / "output/campaign/lr-selection.json"
    selection = json.loads(selection_path.read_text())
    selection.pop("evidence_sha256")
    selection["candidates"]["3e-05"]["result_collection_sha256"] = "0" * 64
    write_sealed(selection_path, selection, "evidence_sha256")
    with pytest.raises(ValueError, match="does not bind"):
        validate_gate3_success(root / "output/campaign", json.loads(card_path.read_text()))
