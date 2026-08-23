from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.inference.run_development_baseline_host import (
    MODEL_RELATIVE,
    OUTPUT_RELATIVE,
    build_container_argv,
    canonical_sha256,
    file_sha256,
    require_fresh_container_name,
    validate_completed_run,
    verify_workspace,
)


def write_sealed(path: Path, value: dict, field: str) -> dict:
    value = dict(value)
    value[field] = canonical_sha256(value)
    path.write_text(json.dumps(value), encoding="utf-8")
    return value


def test_workspace_preflight_binds_archive_and_exact_extracted_files(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    source = root / "scripts/inference/run_evaluation.py"
    source.parent.mkdir(parents=True)
    source.write_text("runner", encoding="utf-8")
    archive = tmp_path / "workspace.tar.gz"
    archive.write_bytes(b"archive")
    manifest_path = tmp_path / "manifest.json"
    manifest = write_sealed(manifest_path, {
        "schema_version": "ganesh-mini-development-evaluation-workspace/v1",
        "status": "sealed",
        "surface": "development",
        "task_count": 180,
        "archive": {"path": "workspace.tar.gz", "size_bytes": 7, "sha256": file_sha256(archive)},
        "forbidden_parts": [],
        "files": [{"path": str(source.relative_to(root)), "size_bytes": 6, "sha256": file_sha256(source)}],
    }, "manifest_sha256")
    assert verify_workspace(root, manifest_path, archive)["manifest_sha256"] == manifest["manifest_sha256"]
    (root / "unexpected.txt").write_text("drift", encoding="utf-8")
    with pytest.raises(ValueError, match="file set mismatch"):
        verify_workspace(root, manifest_path, archive)


def test_outer_container_is_offline_and_shares_host_verifier_paths() -> None:
    shared = Path("/var/lib/ganesh-baseline/shared-tmp")
    argv = build_container_argv(
        docker="/usr/bin/docker",
        image="ganesh-cuda:sealed",
        container_name="ganesh-qwen-base-attempt-1",
        workspace=Path("/opt/ganesh/workspace"),
        model=Path("/opt/ganesh/model"),
        output=Path("/var/lib/ganesh-baseline/output"),
        shared_tmp=shared,
        docker_socket=Path("/var/run/docker.sock"),
    )
    joined = " ".join(map(str, argv))
    assert "--network none" in joined and "--pull=never" in joined
    assert "--cap-drop ALL" in joined and "no-new-privileges" in joined
    assert f"src={shared},dst={shared}" in joined
    assert f"TMPDIR={shared}" in argv
    assert f"dst=/workspace/{MODEL_RELATIVE},readonly" in joined
    assert f"dst=/workspace/{OUTPUT_RELATIVE}" in joined
    assert "src=/var/run/docker.sock,dst=/var/run/docker.sock" in joined
    assert "--entrypoint python" in joined


def test_completed_run_requires_exact_base_and_all_180_tasks(tmp_path: Path) -> None:
    path = tmp_path / "run.json"
    run = {
        "schema_version": "ganesh-mini-inference-run/v2",
        "classification": "private_development_baseline",
        "model": {
            "model_id": "Qwen/Qwen3.5-2B",
            "revision": "15852e8c16360a2fea060d615a32b45270f8a8fc",
        },
        "task_accounting": {"expected": 180, "completed": 180, "pending": 0},
        "tasks": [{"task_id": f"task-{index}"} for index in range(180)],
    }
    write_sealed(path, run, "run_sha256")
    assert validate_completed_run(path)["task_accounting"]["completed"] == 180
    run["task_accounting"]["pending"] = 1
    write_sealed(path, run, "run_sha256")
    with pytest.raises(ValueError, match="completion contract"):
        validate_completed_run(path)


def test_controller_refuses_to_delete_or_reuse_an_existing_container() -> None:
    existing = subprocess.CompletedProcess([], 0, "{}", "")
    with patch("scripts.inference.run_development_baseline_host.subprocess.run", return_value=existing):
        with pytest.raises(RuntimeError, match="not fresh"):
            require_fresh_container_name("/usr/bin/docker", "ganesh-qwen-base-attempt-1")
