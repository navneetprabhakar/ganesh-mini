import hashlib
import json
from pathlib import Path

from scripts.eval.build_expansion_evaluation import build, canonical_digest
from scripts.inference.run_evaluation import validate_config


def seal(path: Path, value: dict, field: str) -> dict:
    value[field] = canonical_digest(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))
    return value


def inputs(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path]:
    adapter = tmp_path / "training/adapter-final"; adapter.mkdir(parents=True)
    weights = adapter / "adapter.safetensors"; weights.write_bytes(b"weights")
    files = {"adapter.safetensors": hashlib.sha256(weights.read_bytes()).hexdigest()}
    card_path = tmp_path / "card.json"
    card = seal(card_path, {"status": "ready", "schema_version": "ganesh-mini-expansion-pilot-card/v1"}, "card_sha256")
    run_path = tmp_path / "training/run-evidence.json"
    run = seal(run_path, {"status": "complete", "adapter_files": files}, "evidence_sha256")
    terminal_path = tmp_path / "terminal.json"
    seal(terminal_path, {"status": "passed", "card_sha256": card["card_sha256"], "run_evidence_sha256": run["evidence_sha256"], "adapter_files": files}, "report_sha256")
    return tmp_path, card_path, terminal_path, run_path, adapter


def test_builds_frozen_canary_and_blocked_full_configs(tmp_path: Path) -> None:
    canary, full, manifest = build(*inputs(tmp_path))
    assert canary["expected_task_count"] == 30
    assert canary["task_globs"] == ["eval/private/development/tranche1/*.task.json"]
    assert full["expected_task_count"] == 180
    assert manifest["status"] == "canary-ready-full-blocked"
    assert manifest["canary_config_sha256"] == canonical_digest(canary)
    validate_config(canary)
    validate_config(full)


def test_rejects_adapter_mutation(tmp_path: Path) -> None:
    args = inputs(tmp_path)
    (args[-1] / "adapter.safetensors").write_bytes(b"changed")
    try:
        build(*args)
    except ValueError as error:
        assert "adapter files" in str(error)
    else:
        raise AssertionError("mutated adapter was accepted")


def test_capacity_probe_never_authorizes_full_evaluation(tmp_path: Path) -> None:
    root, card_path, terminal_path, run_path, adapter = inputs(tmp_path)
    card = json.loads(card_path.read_text())
    card.pop("card_sha256")
    card["schema_version"] = "ganesh-mini-expansion-pilot-card/v2"
    card["selected_recipe"] = {"recipe_id": "bf16-lora-capacity-probe-v2"}
    seal(card_path, card, "card_sha256")
    terminal = json.loads(terminal_path.read_text())
    terminal.pop("report_sha256")
    terminal["card_sha256"] = json.loads(card_path.read_text())["card_sha256"]
    seal(terminal_path, terminal, "report_sha256")
    canary, _, manifest = build(root, card_path, terminal_path, run_path, adapter)
    assert canary["adapter"]["served_model_id"] == "bf16-lora-capacity-probe-v2"
    assert manifest["full_release_condition"] == "prohibited-for-capacity-probe"


def test_lane_stratified_probe_never_authorizes_full_evaluation(tmp_path: Path) -> None:
    root, card_path, terminal_path, run_path, adapter = inputs(tmp_path)
    card = json.loads(card_path.read_text())
    card.pop("card_sha256")
    card["schema_version"] = "ganesh-mini-expansion-pilot-card/v3"
    card["selected_recipe"] = {"recipe_id": "bf16-lora-lane-stratified-probe-v3"}
    seal(card_path, card, "card_sha256")
    terminal = json.loads(terminal_path.read_text())
    terminal.pop("report_sha256")
    terminal["card_sha256"] = json.loads(card_path.read_text())["card_sha256"]
    seal(terminal_path, terminal, "report_sha256")
    canary, _, manifest = build(root, card_path, terminal_path, run_path, adapter)
    assert canary["adapter"]["served_model_id"] == "bf16-lora-lane-stratified-probe-v3"
    assert manifest["full_release_condition"] == "prohibited-for-capacity-probe"
