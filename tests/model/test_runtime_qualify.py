from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts/model/runtime_qualify.py"
SPEC = importlib.util.spec_from_file_location("runtime_qualify", MODULE_PATH)
assert SPEC and SPEC.loader
runtime = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runtime)


def test_write_evidence_adds_digest_over_preidentity_payload(tmp_path: Path) -> None:
    path = tmp_path / "evidence.json"
    original = {"passed": True, "model_id": "example", "values": [1, 2]}
    runtime.write_evidence(original, path)
    observed = json.loads(path.read_text())
    identity = observed.pop("evidence_sha256")
    assert identity == runtime.digest(observed)
    assert len(identity) == 64


def test_apple_matrix_lock_identity_matches_repository_lock() -> None:
    matrix = json.loads((ROOT / "configs/model/gate0_apple_matrix.json").read_text())
    lock_identity = hashlib.sha256((ROOT / "uv.lock").read_bytes()).hexdigest()
    assert matrix["executed_uv_lock_sha256"] == "a4291094b0452aabe38a8fc26a76179d54bc7e516a92074d14eca07adbf32015"
    assert matrix["current_uv_lock_sha256"] == lock_identity
    assert matrix["current_lock_apple_projection_unchanged"] is True
    exported = subprocess.run(
        ["uv", "export", "--frozen", "--extra", "gate0-apple", "--no-dev", "--no-hashes", "--no-emit-project"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    ).stdout
    resolved = dict(line.split("==", 1) for line in exported.splitlines() if "==" in line)
    assert {name: resolved[name] for name in matrix["locked_packages"]} == matrix["locked_packages"]
    assert matrix["qualified"]["peft_bf16_lora_train_save_reload_merge_mps"] is True
    assert "nf4_qlora" in matrix["not_qualified"]
