from pathlib import Path

import pytest

from scripts.eval.contracts import load_json
from scripts.inference.run_evaluation import checkpoint_adapter_files, implementation_identity, rooted, trim_at_eos, validate_batch_outputs, validate_config, validate_resumed_generation


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


def test_batched_generation_drops_padding_after_first_eos() -> None:
    assert trim_at_eos([10, 248046, 248044, 248044], 248046) == [10, 248046]
    assert trim_at_eos([10, 11], 248046) == [10, 11]


def test_absolute_runtime_mounts_do_not_resolve_beneath_workspace() -> None:
    assert rooted("models/base") == ROOT / "models/base"
    assert rooted("/input/model") == Path("/input/model")


def test_checkpoint_adapter_is_bound_to_manifest_and_training_run(tmp_path: Path) -> None:
    import json

    from scripts.eval.contracts import sha256_object

    adapter = tmp_path / "checkpoint" / "adapter"
    adapter.mkdir(parents=True)
    (adapter / "adapter_model.safetensors").write_bytes(b"checkpoint")
    from scripts.inference.run_evaluation import file_sha256
    identities = {"card_sha256": "a" * 64, "recipe_sha256": "b" * 64}
    manifest = {
        "status": "complete",
        "identities": identities,
        "files": [{
            "path": "adapter/adapter_model.safetensors",
            "sha256": file_sha256(adapter / "adapter_model.safetensors"),
        }],
    }
    manifest["manifest_sha256"] = sha256_object(manifest)
    manifest_path = adapter.parent / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))

    observed, seal = checkpoint_adapter_files(adapter, manifest_path, {"identities": identities})

    assert observed == {"adapter_model.safetensors": manifest["files"][0]["sha256"]}
    assert seal == manifest["manifest_sha256"]


def test_checkpoint_adapter_rejects_wrong_training_identity(tmp_path: Path) -> None:
    import json

    from scripts.eval.contracts import sha256_object

    adapter = tmp_path / "checkpoint" / "adapter"
    adapter.mkdir(parents=True)
    manifest = {"status": "complete", "identities": {"recipe": "a"}, "files": []}
    manifest["manifest_sha256"] = sha256_object(manifest)
    manifest_path = adapter.parent / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))

    with pytest.raises(ValueError, match="training run identities"):
        checkpoint_adapter_files(adapter, manifest_path, {"identities": {"recipe": "b"}})
