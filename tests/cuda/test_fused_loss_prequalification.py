from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "measurement/cuda/local/20260824T172717Z/fused-loss-prequalification.json"
CARD = ROOT / "measurement/cuda/gcloud/GATE0B_L4_V14_FUSED_LOSS_DRAFT_CARD.json"

def test_fused_loss_prequalification_is_sealed_and_binds_inputs() -> None:
    value=json.loads(EVIDENCE.read_text())
    claimed=value.pop("evidence_sha256")
    observed=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()
    assert observed==claimed
    assert all((ROOT/relative).is_file() and len(expected)==64 for relative,expected in value["input_sha256"].items())
    assert value["measured_diagnosis"]["bf16_logits_bytes"]==2944*248320*2
    assert value["measured_diagnosis"]["fp32_loss_logits_bytes"]==2944*248320*4
    assert value["repair_contract"]["materialize_training_logits"] is False
    assert value["container_image"]["offline_smoke_network"]=="none"
    assert value["qualification_claim"] is False
    assert value["next_gcloud_usage_requires_fresh_explicit_approval"] is True
    card=json.loads(CARD.read_text())
    card_claimed=card.pop("card_sha256")
    card_observed=hashlib.sha256(json.dumps(card,sort_keys=True,separators=(",", ":")).encode()).hexdigest()
    assert card_observed==card_claimed
    assert card["status"]=="approved-awaiting-generation-pinned-upload"
    assert card["authorization"]["status"]=="approved-for-one-us-east1-g2-l4-fused-loss-flex-start-request"
    assert card["container_image"]["id"]==value["container_image"]["id"]
    assert card["source"]["workspace_sha256"]=="806a5a400278bf7c13092514f5f7b4d8fa0909697ff0cf6a0f9c2b6e8d503310"
    assert card["source"]["local_prequalification_sha256"]==claimed
    assert card["source"]["qualification_config_sha256"]==value["input_sha256"]["configs/cuda/qwen3_5_2b_gate0.json"]
    assert card["source"]["training_config_sha256"]==value["input_sha256"]["configs/train/seed_pilot.json"]
    assert card["source"]["qualifier_sha256"]==value["input_sha256"]["scripts/cuda/qualify.py"]
    assert card["source"]["qwen_runtime_sha256"]==value["input_sha256"]["scripts/train/qwen_runtime.py"]
    assert card["source"]["production_sft_sha256"]==value["input_sha256"]["scripts/train/run_sft.py"]
