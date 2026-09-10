import json
import shutil
from pathlib import Path

from scripts.train.expansion_pilot import ROOT, bind_provider, build_card


def test_repository_expansion_pilot_is_locally_prepared() -> None:
    card = build_card(ROOT / "configs/train/expansion_pilot_v1.json", ROOT, system="Linux")
    assert card["status"] == "prepared-not-executable"
    assert card["failed_checks"] == []
    assert card["provider_execution"] is None
    assert card["selected_recipe"]["learning_rate"] == 0.00001
    assert card["control"]["maximum_seen_tokens"] == 2438853
    assert card["evaluation"]["promotion_rule"]["minimum_improved_product_families"] == 4


def test_capacity_probe_is_prefix_bounded_and_has_no_promotion_authority() -> None:
    card = build_card(ROOT / "configs/train/expansion_capacity_probe_v2.json", ROOT, system="Linux")
    assert card["status"] == "prepared-not-executable"
    assert card["failed_checks"] == []
    assert card["schema_version"] == "ganesh-mini-expansion-pilot-card/v2"
    assert card["data"]["records"] == 624
    assert card["control"]["maximum_seen_tokens"] == 468601
    assert card["selected_recipe"]["lora_rank"] == 16
    assert card["selected_recipe"]["target_policy"]["scope"] == "all-attention-plus-last-n-mlp"
    assert card["evaluation"]["full_development_tasks"] == 0
    assert card["evaluation"]["promotion_rule"]["minimum_improved_product_families"] == 2


def test_lane_stratified_probe_is_exact_and_has_retention_guard() -> None:
    card = build_card(ROOT / "configs/train/expansion_lane_stratified_probe_v3.json", ROOT, system="Linux")
    assert card["status"] == "prepared-not-executable"
    assert card["failed_checks"] == []
    assert card["schema_version"] == "ganesh-mini-expansion-pilot-card/v3"
    assert card["data"]["records"] == 640
    assert card["control"]["maximum_seen_tokens"] == 466614
    assert card["selected_recipe"]["gradient_accumulation_steps"] == 10
    assert card["evaluation"]["retention_loss_guard"]["maximum_relative_loss_increase_per_lane"] == 0.05
    assert card["evaluation"]["full_development_tasks"] == 0


def test_expansion_pilot_fails_closed_on_data_mutation(tmp_path: Path) -> None:
    for relative in (
        "configs/train/expansion_pilot_v1.json",
        "configs/model/qwen3_5_2b.contract.json",
        "artifacts/train/expansion-pilot-v1/prepared-dataset-manifest.json",
        "artifacts/train/expansion-pilot-v1/prepared-train.jsonl",
        "artifacts/train/expansion-pilot-v1/prepared-validation.jsonl",
        "measurement/data/expansion-v1/PILOT_SUFFICIENCY_AND_THROUGHPUT_20260909.json",
    ):
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, destination)
    config = tmp_path / "configs/train/expansion_pilot_v1.json"
    payload = json.loads(config.read_text())
    (tmp_path / payload["data"]["prepared_train_path"]).write_text("mutated\n")
    card = build_card(config, tmp_path, system="Linux")
    assert card["status"] == "not-ready"
    assert "prepared_train_file" in card["failed_checks"]


def test_provider_binding_requires_exact_cost_and_approval_evidence() -> None:
    local = build_card(ROOT / "configs/train/expansion_pilot_v1.json", ROOT, system="Linux")
    executable = bind_provider(local, {
        "provider": "gcloud",
        "project": "approved-project",
        "zone": "asia-south1-a",
        "machine_type": "g2-standard-8",
        "accelerator": "NVIDIA_L4",
        "hourly_cost_usd": 1.0,
        "prior_cost_usd": 0.0,
        "cost_ceiling_usd": 8.0,
        "price_evidence_sha256": "a" * 64,
        "approval_evidence_sha256": "b" * 64,
    })
    assert executable["status"] == "ready"
    assert executable["provider_execution"]["cost_ceiling_usd"] == 8.0
    assert executable["card_sha256"] != local["card_sha256"]
