from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.inference.run_development_baseline_host import canonical_sha256
from scripts.inference.verify_gate1_terminal import verify


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
    output = root / "output"
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
    card = {"schema_version": "ganesh-mini-gate1-gcloud-execution/v1", "status": "authorized-executable", "gate": 1, "execution": {"attempt_id": "attempt"}}
    card["execution_sha256"] = canonical_sha256(card)
    card_path = tmp_path / "card.json"; card_path.write_text(json.dumps(card))
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
    assert evidence["run"] is None and evidence["deletion_eligible"] is True


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
