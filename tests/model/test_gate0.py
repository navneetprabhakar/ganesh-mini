from __future__ import annotations

import importlib.util
import json
from argparse import Namespace
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts/model/gate0.py"
SPEC = importlib.util.spec_from_file_location("gate0", MODULE_PATH)
assert SPEC and SPEC.loader
gate0 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate0)


@pytest.fixture
def contract() -> dict:
    return json.loads((ROOT / "configs/model/qwen3_5_2b.contract.json").read_text())


@pytest.fixture
def inventory() -> dict:
    return json.loads((ROOT / "configs/model/qwen3_5_2b.inventory.json").read_text())


def test_pinned_inventory_is_internally_consistent(contract: dict, inventory: dict) -> None:
    checks = gate0.validate_contract_inventory(contract, inventory)
    assert all(item["passed"] for item in checks), checks
    assert inventory["total_bytes"] == sum(item["size"] for item in inventory["files"])
    assert inventory["total_bytes"] == sum(inventory["byte_groups"].values())


def test_inventory_rejects_mutable_revision_and_unknown_size(contract: dict, inventory: dict) -> None:
    contract["revision"] = "main"
    inventory["revision"] = "main"
    inventory["files"][0].pop("size")
    checks = {item["name"]: item for item in gate0.validate_contract_inventory(contract, inventory)}
    assert not checks["model_identity"]["passed"]
    assert not checks["known_download_bytes"]["passed"]


def test_hugging_face_tree_metadata_normalizes_to_valid_inventory(
    tmp_path: Path, contract: dict, inventory: dict
) -> None:
    raw = []
    for item in inventory["files"]:
        entry = {"type": "file", "path": item["path"], "size": item["size"], "oid": item["git_oid"]}
        if "sha256" in item:
            entry["lfs"] = {"oid": item["sha256"], "size": item["size"]}
        raw.append(entry)
    metadata = tmp_path / "tree.json"
    output = tmp_path / "normalized.json"
    metadata.write_text(json.dumps(raw))
    args = Namespace(
        metadata=metadata,
        contract=ROOT / "configs/model/qwen3_5_2b.contract.json",
        source="test",
        license="apache-2.0",
        output=output,
    )
    assert gate0.command_inventory(args) == 0
    normalized = json.loads(output.read_text())
    assert normalized["byte_groups"] == inventory["byte_groups"]


def test_architecture_requires_exact_hybrid_pattern(contract: dict) -> None:
    config = {
        "model_type": "qwen3_5",
        "text_config": {
            "model_type": "qwen3_5_text",
            "num_hidden_layers": 24,
            "vocab_size": 248320,
            "layer_types": ["linear_attention"] * 18 + ["full_attention"] * 6,
        },
    }
    assert gate0.validate_architecture(config, contract["architecture"])["passed"]
    config["text_config"]["layer_types"].pop()
    assert not gate0.validate_architecture(config, contract["architecture"])["passed"]


def test_lora_inspection_excludes_vision_and_requires_gradient_probe(contract: dict) -> None:
    catalog = {
        "source_kind": "runtime_named_modules",
        "model_id": contract["model_id"],
        "revision": contract["revision"],
        "gradient_probe_passed": True,
        "modules": [
            {"name": "model.language_model.layers.0.self_attn.q_proj", "type": "torch.nn.Linear", "num_parameters": 100, "lora_targeted": True, "adapter_trainable_parameters": 10, "adapter_gradient_observed": True},
            {"name": "model.language_model.layers.0.linear_attn.in_proj_qkvz", "type": "torch.nn.Linear", "num_parameters": 200, "lora_targeted": True, "adapter_trainable_parameters": 20, "adapter_gradient_observed": True},
            {"name": "model.visual.blocks.0.attn.q_proj", "type": "torch.nn.Linear", "num_parameters": 300, "lora_targeted": True, "adapter_trainable_parameters": 30, "adapter_gradient_observed": True},
            {"name": "lm_head", "type": "torch.nn.Linear", "num_parameters": 400, "lora_targeted": False, "adapter_trainable_parameters": 0, "adapter_gradient_observed": False},
        ],
    }
    result = gate0.inspect_lora(catalog, contract)
    assert result["runtime_verified"]
    assert result["gradient_coverage_verified"]
    assert result["candidate_target_suffixes"] == {"in_proj_qkvz": 1, "q_proj": 1}
    assert result["language_linear_parameters"] == 300
    assert result["lora_trainable_parameters"] == 30
    assert result["excluded_linear_module_count"] == 2


def test_lora_inspection_does_not_treat_static_metadata_as_runtime_proof(contract: dict) -> None:
    catalog = {
        "source_kind": "safetensors_index",
        "model_id": contract["model_id"],
        "revision": contract["revision"],
        "gradient_probe_passed": True,
        "modules": [{"name": "model.layers.0.q_proj", "type": "torch.nn.Linear", "num_parameters": 1, "lora_targeted": True, "adapter_trainable_parameters": 1, "adapter_gradient_observed": True}],
    }
    assert not gate0.inspect_lora(catalog, contract)["runtime_verified"]


def test_gate_report_fails_closed_without_local_runtime_evidence(tmp_path: Path) -> None:
    args = Namespace(
        contract=ROOT / "configs/model/qwen3_5_2b.contract.json",
        inventory=ROOT / "configs/model/qwen3_5_2b.inventory.json",
        model_dir=None,
        lock_file=None,
        lora_report=None,
        inference_evidence=None,
        training_evidence=None,
        gguf_evidence=None,
        output=tmp_path / "report.json",
    )
    report = gate0.build_report(args)
    assert report["status"] == "not_ready"
    assert "local_inventory" in report["failed_checks"]
    assert "text_only_inference_smoke" in report["failed_checks"]
    assert "train_save_reload_merge_smoke" in report["failed_checks"]
    assert "base_gguf_f16_q8_smoke" in report["failed_checks"]
    assert len(report["report_sha256"]) == 64


def test_evidence_rejects_pass_without_identity(tmp_path: Path, contract: dict) -> None:
    evidence = tmp_path / "inference.json"
    evidence.write_text(json.dumps({"passed": True, "model_id": contract["model_id"], "revision": contract["revision"]}))
    result = gate0.evidence_check("inference", evidence, contract)
    assert not result["passed"]
