from pathlib import Path

import pytest

from scripts.eval.contracts import load_json
from scripts.inference.run_evaluation import implementation_identity, validate_batch_outputs, validate_config, validate_resumed_generation


ROOT=Path(__file__).resolve().parents[2]


def test_development_config_is_batched_and_parallel() -> None:
    config=load_json(ROOT/"configs/inference/qwen_base_development.json"); validate_config(config)
    assert config["expected_task_count"]==180
    assert config["execution"]["batch_size"]>1 and config["execution"]["verifier_workers"]>1
    assert config["execution"]["required_device"]=="cuda"


def test_decision_requires_one_sealed_opening() -> None:
    config=load_json(ROOT/"configs/inference/qwen_base_development.json")
    config.update({"classification":"private_decision_final","allowed_surface":"decision"})
    with pytest.raises(ValueError,match="sealed final opening"): validate_config(config)


def test_length_bucket_width_must_be_positive() -> None:
    config=load_json(ROOT/"configs/inference/qwen_base_development.json")
    config["execution"]["length_bucket_width"]=0
    with pytest.raises(ValueError,match="length bucket width"): validate_config(config)


def test_resumed_generation_binds_runtime_and_implementation() -> None:
    backend=type("Backend",(),{"identity":{"backend":"fake","device":"cpu"}})()
    implementation=implementation_identity(); task={"task_id":"task","value":1}; model={"model_id":"model"}; config_sha="a"*64
    from scripts.eval.contracts import sha256_object
    generated={"task_id":"task","task_sha256":sha256_object(task),"config_sha256":config_sha,"model":model,"runtime":backend.identity,"implementation":implementation}
    validate_resumed_generation(generated,task,config_sha,model,backend,implementation)
    generated["implementation"]={**implementation,"runner_sha256":"0"*64}
    with pytest.raises(ValueError,match="implementation mismatch"):
        validate_resumed_generation(generated,task,config_sha,model,backend,implementation)


def test_generation_backend_must_return_one_output_per_input() -> None:
    with pytest.raises(RuntimeError,match="1 outputs for batch size 2"):
        validate_batch_outputs([([1],"x",1)],2)
