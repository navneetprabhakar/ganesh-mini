from pathlib import Path

import pytest

from scripts.eval.contracts import load_json
from scripts.inference.run_evaluation import validate_config


ROOT=Path(__file__).resolve().parents[2]


def test_development_config_is_batched_and_parallel() -> None:
    config=load_json(ROOT/"configs/inference/qwen_base_development.json"); validate_config(config)
    assert config["expected_task_count"]==180
    assert config["execution"]["batch_size"]>1 and config["execution"]["verifier_workers"]>1


def test_decision_requires_one_sealed_opening() -> None:
    config=load_json(ROOT/"configs/inference/qwen_base_development.json")
    config.update({"classification":"private_decision_final","allowed_surface":"decision"})
    with pytest.raises(ValueError,match="sealed final opening"): validate_config(config)
