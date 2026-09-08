import json
from pathlib import Path

from scripts.train.expansion_pilot import bind_provider, build_card, canonical_digest
from scripts.train.verify_expansion_pilot import verify


ROOT = Path(__file__).resolve().parents[2]


def sealed(value: dict, field: str) -> dict:
    value[field] = canonical_digest(value)
    return value


def fixture(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    config_path = ROOT / "configs/train/expansion_pilot_v1.json"
    local = build_card(config_path, ROOT, system="Linux")
    card = bind_provider(local, {
        "provider": "gcloud", "project": "p", "zone": "z", "machine_type": "g2-standard-8", "accelerator": "NVIDIA_L4",
        "hourly_cost_usd": 1.0, "prior_cost_usd": 0.0, "cost_ceiling_usd": 8.0,
        "price_evidence_sha256": "a" * 64, "approval_evidence_sha256": "b" * 64,
    })
    card_path = tmp_path / "card.json"
    card_path.write_text(json.dumps(card))
    adapter = tmp_path / "adapter-final"
    adapter.mkdir()
    weights = adapter / "adapter_model.safetensors"
    weights.write_bytes(b"adapter")
    import hashlib
    adapter_hash = hashlib.sha256(weights.read_bytes()).hexdigest()
    recipe = card["selected_recipe"]
    run = sealed({
        "schema_version": "ganesh-mini-sft-run/v2", "status": "complete",
        "identities": {
            "card_sha256": card["card_sha256"], "config_sha256": card["inputs"]["config_sha256"],
            "prepared_manifest_sha256": card["inputs"]["prepared_manifest_sha256"], "prepared_data_sha256": card["inputs"]["prepared_data_sha256"],
            "validation_data_sha256": card["inputs"]["validation_data_sha256"], "model_revision": card["model"]["revision"],
            "recipe_sha256": canonical_digest(recipe), "learning_rate": str(recipe["learning_rate"]), "phase": "expansion-pilot",
        },
        "planned_end_row": 3225, "state": {"seen_tokens": 2438853}, "save_reload": {"passed": True},
        "cuda": {"peak_vram_bytes": 20 * 1024**3},
        "cost": {"hourly_usd": "1.0", "ceiling_usd": "8.0", "projected_final_usd": "3.5"},
        "adapter_files": {"adapter_model.safetensors": adapter_hash},
    }, "evidence_sha256")
    run_path = tmp_path / "run.json"
    run_path.write_text(json.dumps(run))
    return card_path, config_path, run_path, adapter


def test_terminal_verifier_accepts_exact_completed_run(tmp_path: Path) -> None:
    report = verify(*fixture(tmp_path))
    assert report["status"] == "passed"
    assert report["failed_checks"] == []


def test_terminal_verifier_rejects_mutated_adapter(tmp_path: Path) -> None:
    card, config, run, adapter = fixture(tmp_path)
    (adapter / "adapter_model.safetensors").write_bytes(b"mutated")
    report = verify(card, config, run, adapter)
    assert report["status"] == "failed"
    assert "adapter_identity" in report["failed_checks"]
