import copy
import json

import pytest

from scripts.train.build_gradient_conflict_config import build


def source() -> dict:
    return json.loads(open("configs/train/expansion_lane_stratified_probe_v3.json", encoding="utf-8").read())


def test_build_preserves_v3_data_capacity_and_gates_pcgrad() -> None:
    original = source()
    config = build(original)
    assert config["schema_version"] == "ganesh-mini-expansion-pilot-config/v4"
    assert config["data"] == original["data"]
    for key in ("lora_rank", "lora_alpha", "target_policy", "learning_rate", "gradient_accumulation_steps"):
        assert config["recipe"][key] == original["recipe"][key]
    conflict = config["recipe"]["gradient_conflict"]
    assert conflict["stage_1"]["selected_optimizer_groups"] == [0, 9, 18, 27, 36, 45, 54, 63]
    assert conflict["stage_1"]["optimizer_steps"] == 0
    assert conflict["stage_2"]["conditional_on_stage_1"] is True
    assert sum(conflict["stage_2"]["lane_weights"].values()) == 1.0
    assert config["evaluation"]["promotion_rule"]["rule_id"] == "gradient-conflict-probe-continuation-v4"


def test_build_rejects_mutated_v3_source() -> None:
    value = copy.deepcopy(source())
    value["control"]["maximum_seen_tokens"] += 1
    with pytest.raises(ValueError, match="exact v3"):
        build(value)
