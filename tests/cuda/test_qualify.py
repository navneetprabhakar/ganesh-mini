import json
import sys
import types
from pathlib import Path

import pytest

from scripts.cuda.qualify import (
    FALLBACK_RECIPE,
    PRIMARY_RECIPE,
    canonical_sha256,
    append_journal,
    configure_qwen_training_structure,
    enforce_cuda_peak,
    install_fla_recurrent_compatibility,
    load_and_validate_config,
    restore_qwen_serving_cache,
    resolved_kernel_implementation,
    select_records,
    swift_identity,
    write_evidence,
)
from scripts.train.qwen_runtime import reload_and_merge_saved_adapter
from scripts.train.qwen_runtime import configure_cuda_allocator

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "configs/cuda/qwen3_5_2b_gate0.json"


def test_pinned_primary_and_fallback_validate() -> None:
    config = load_and_validate_config(CONFIG, ROOT)
    assert config["qualification_order"] == [PRIMARY_RECIPE, FALLBACK_RECIPE]
    primary = config["recipes"][PRIMARY_RECIPE]
    assert primary["minimum_vram_bytes"] == 22 * 1024**3
    assert primary["maximum_peak_vram_bytes"] == 21 * 1024**3
    assert primary["quantization"] is None
    assert primary["sequence_length"] == 2944
    assert (primary["micro_batch_size"], primary["rank"], primary["alpha"], primary["dropout"]) == (1, 32, 64, 0.05)
    assert primary["gradient_checkpointing"] and primary["response_only"]
    assert primary["cuda_allocator_config"] == "expandable_segments:True"
    fallback = config["recipes"][FALLBACK_RECIPE]
    assert fallback["sequence_length"] == 2944
    assert fallback["quantization"] == {"bits": 4, "type": "nf4", "double_quantization": True, "compute_dtype": "bfloat16"}
    assert fallback["cuda_allocator_config"] == "expandable_segments:True"
    assert config["packages"]["bitsandbytes"] == "0.49.2"
    assert config["packages"]["torchvision"] == "0.28.0"


def test_primary_recipe_mutation_fails_closed(tmp_path: Path) -> None:
    source = json.loads(CONFIG.read_text())
    source["recipes"][PRIMARY_RECIPE]["rank"] = 16
    path = tmp_path / "config.json"
    path.write_text(json.dumps(source))
    with pytest.raises(ValueError, match="primary recipe changed"):
        load_and_validate_config(path, ROOT)


def test_budget_increase_fails_closed(tmp_path: Path) -> None:
    source = json.loads(CONFIG.read_text())
    source["budget"]["maximum_usd"] = 5.01
    path = tmp_path / "config.json"
    path.write_text(json.dumps(source))
    with pytest.raises(ValueError, match="authorized bound"):
        load_and_validate_config(path, ROOT)


def test_cuda_environment_lock_mismatch_fails_closed(tmp_path: Path) -> None:
    source = json.loads(CONFIG.read_text())
    source["container"]["uv_lock_sha256"] = "0" * 64
    path = tmp_path / "config.json"
    path.write_text(json.dumps(source))
    with pytest.raises(ValueError, match="environment lock hash mismatch"):
        load_and_validate_config(path, ROOT)


def test_write_evidence_seals_canonical_bytes(tmp_path: Path) -> None:
    path = tmp_path / "evidence.json"
    write_evidence({"status": "failed", "reason": "no GPU"}, path)
    value = json.loads(path.read_text()); claimed = value.pop("evidence_sha256")
    assert claimed == canonical_sha256(value)


def test_journal_appends_durable_json_lines(tmp_path: Path) -> None:
    path = tmp_path / "qualification.journal.jsonl"
    append_journal(path, {"phase": "identity", "state": "started"})
    append_journal(path, {"phase": "identity", "state": "completed"})
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    assert [row["state"] for row in rows] == ["started", "completed"]
    assert all(row["recorded_at"] for row in rows)


class FakeTokenizer:
    def apply_chat_template(self, messages, *, tokenize, add_generation_prompt):
        assert not add_generation_prompt
        return messages[-1]["content"]

    def __call__(self, rendered, *, add_special_tokens):
        assert not add_special_tokens
        return type("Tokens", (), {"input_ids": rendered.split()})()


def test_record_selection_is_length_stratified(tmp_path: Path) -> None:
    path = tmp_path / "records.jsonl"
    rows = [
        {"id": "b", "messages": [{"role": "assistant", "content": "one two three"}]},
        {"id": "c", "messages": [{"role": "assistant", "content": "one two"}]},
        {"id": "a", "messages": [{"role": "assistant", "content": "one"}]},
    ]
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))
    selected = select_records(path, FakeTokenizer(), 2, 4096)
    assert [item["row"]["id"] for item in selected] == ["a", "b"]


def test_runner_defaults_primary_and_guards_fallback_order() -> None:
    runner = (ROOT / "scripts/cuda/run_qualification.sh").read_text()
    assert 'recipe="${4:-bf16-lora-primary-v1}"' in runner
    assert "GANESH_PRIMARY_QUALIFICATION_EVIDENCE" in runner
    assert '--recipe "$recipe"' in runner
    assert "GANESH_ABSOLUTE_CUMULATIVE_CEILING_USD" in runner
    assert 'GANESH_MAX_VM_LIFETIME_SECONDS' in runner
    assert "hourly * lifetime / Decimal(3600)" in runner
    assert "projected >= ceiling" in runner


def test_gpu_startup_is_prebuilt_generation_pinned_and_offline() -> None:
    startup = (ROOT / "scripts/cuda/gcloud_startup_gate0b.sh").read_text()
    assert "GANESH_IMAGE_ARCHIVE_URI" in startup
    assert startup.count("must include a GCS generation") == 1
    assert "download_verified" in startup
    assert "WORKSPACE_ARCHIVE_SHA256" in startup and "MODEL_ARCHIVE_SHA256" in startup
    assert "DOCKER_BUNDLE_SHA256" in startup
    assert "docker load" in startup
    assert "apt-get" not in startup
    assert "docker build" not in startup
    assert "docker pull" not in startup
    assert "nvidia-ctk runtime configure --runtime=docker" in startup


def test_runner_requires_exact_preloaded_image_and_disables_pull_and_network() -> None:
    runner = (ROOT / "scripts/cuda/run_qualification.sh").read_text()
    assert "GANESH_CUDA_IMAGE_ID" in runner
    assert "docker build" not in runner
    assert "--pull=never" in runner
    assert "--network none" in runner
    assert "--cpus 8 --memory 28g" in runner
    assert "--tmpfs /tmp:rw,noexec,nosuid,size=8g" in runner
    assert "--tmpfs /var/cache/triton:rw,exec,nosuid,nodev,size=1g" in runner
    assert "TRITON_CACHE_DIR=/var/cache/triton" in runner
    assert "-e PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True" in runner
    assert "-e PYTHONPATH=/workspace" in runner


def test_cuda_allocator_contract_sets_early_and_rejects_mutation(monkeypatch) -> None:
    monkeypatch.delenv("PYTORCH_CUDA_ALLOC_CONF", raising=False)
    evidence = configure_cuda_allocator("expandable_segments:True")
    assert evidence["passed"] is True
    assert evidence["value"] == "expandable_segments:True"
    monkeypatch.setenv("PYTORCH_CUDA_ALLOC_CONF", "max_split_size_mb:64")
    with pytest.raises(RuntimeError, match="allocator contract mismatch"):
        configure_cuda_allocator("expandable_segments:True")


def test_l4_startup_admits_bounded_host_and_fallback_only_on_sealed_memory_failure() -> None:
    startup = (ROOT / "scripts/cuda/gcloud_startup_gate0b.sh").read_text()
    assert "fewer than 8 CPUs" in startup and "less than 30 GiB RAM" in startup
    assert 'error_type in {"OutOfMemoryError","CUDAOutOfMemoryError"}' in startup
    assert 'error_type == "PeakVramExceeded"' in startup
    assert "GANESH_PRIMARY_QUALIFICATION_EVIDENCE" in startup
    assert "nf4-qlora-fallback-v1" in startup


def test_inference_and_training_share_one_model_load() -> None:
    source = (ROOT / "scripts/cuda/qualify.py").read_text()
    main = source[source.index("def main()") :]
    assert main.count("model = load_model(args.model_dir,args.recipe)") == 1
    assert "inference_smoke(model,tokenizer)" in main
    assert "run_training_smoke(config,args.recipe,args.model_dir,args.records,args.adapter_dir,model,tokenizer,model_load_peak,journal_path)" in main


def test_cpu_prebuild_has_a_hard_deadline_and_seals_oci_archive() -> None:
    prebuild = (ROOT / "scripts/cuda/prebuild_cuda_image.sh").read_text()
    startup = (ROOT / "scripts/cuda/gcloud_prebuild_gate0b.sh").read_text()
    assert "3600" in prebuild and "timeout --signal=TERM" in prebuild
    assert "docker save" in prebuild and "cuda-image.docker.tar.zst.sha256" in prebuild
    assert 'docker_package_version="29.1.3-0ubuntu3~22.04.2"' in startup
    assert "--download-only" in startup
    assert "base-dpkg-packages.tsv" in startup and "bundle-files.sha256" in startup
    assert "prebuild-manifest.json" in startup


def test_cuda_dockerfile_does_not_require_optional_buildx_component() -> None:
    dockerfile = (ROOT / "containers/cuda/Dockerfile").read_text()
    assert "--mount=type=cache" not in dockerfile
    assert "uv sync --frozen" in dockerfile
    assert '"torchvision": "0.28.0"' in dockerfile
    assert "import torchvision" in dockerfile
    assert "import qwen_vl_utils" in dockerfile


def test_gpu_identity_precedes_fla_import_and_kernel_check() -> None:
    source = (ROOT / "scripts/cuda/qualify.py").read_text()
    identity_loop = source[source.index('for component, check in'):source.index('append_journal(journal_path,{"phase":"identity","state":"completed"}')]
    assert identity_loop.index('(\"gpu\"') < identity_loop.index('(\"triton\"') < identity_loop.index('(\"fla_recurrent_compatibility\"') < identity_loop.index('(\"packages\"') < identity_loop.index('(\"kernels\"')
    assert "Triton CUDA backend initialization failed" in source
    assert 'backend != {"triton":"cuda","fla":"cuda","fla_is_nvidia":True}' in source
    assert "modeling_qwen3_5.torch_chunk_gated_delta_rule" in source
    assert "modeling_qwen3_5.torch_recurrent_gated_delta_rule" in source
    assert "modeling_qwen3_5.chunk_gated_delta_rule" not in source
    assert "is_fast_path_available" not in source
    runner = (ROOT / "scripts/cuda/run_qualification.sh").read_text()
    assert '-e GANESH_ATTEMPT_ID="${GANESH_ATTEMPT_ID:?GANESH_ATTEMPT_ID is required}"' in runner


def test_fla_recurrent_compatibility_installs_fused_alias(monkeypatch) -> None:
    class FakeModule:
        pass

    module = FakeModule()

    def fused_recurrent_gated_delta_rule():
        return None

    fused_recurrent_gated_delta_rule.__module__ = "fla.ops.gated_delta_rule.fused_recurrent"
    module.fused_recurrent_gated_delta_rule = fused_recurrent_gated_delta_rule
    monkeypatch.delitem(sys.modules, "transformers.models.qwen3_5.modeling_qwen3_5", raising=False)
    monkeypatch.setattr("scripts.cuda.qualify.importlib.import_module", lambda name: module)

    evidence = install_fla_recurrent_compatibility()

    assert module.recurrent_gated_delta_rule is fused_recurrent_gated_delta_rule
    assert evidence == {
        "requested_symbol": "fla.ops.gated_delta_rule.recurrent_gated_delta_rule",
        "resolved_symbol": "fla.ops.gated_delta_rule.fused_recurrent.fused_recurrent_gated_delta_rule",
        "installed_alias": True,
        "passed": True,
    }


def test_fla_recurrent_compatibility_fails_after_model_import(monkeypatch) -> None:
    monkeypatch.setitem(sys.modules, "transformers.models.qwen3_5.modeling_qwen3_5", object())
    with pytest.raises(RuntimeError, match="before Qwen3.5 model import"):
        install_fla_recurrent_compatibility()


def test_swift_identity_selects_qwen35_explicitly_without_download(monkeypatch, tmp_path: Path) -> None:
    observed = {}

    def get_model_info_meta(path, **kwargs):
        observed.update({"path": path, **kwargs})
        return (
            types.SimpleNamespace(model_type="qwen3_5"),
            types.SimpleNamespace(template=None, candidate_templates=["qwen3_5"]),
        )

    def get_template_meta(info, meta, *, template_type):
        observed.update({"template_info": info, "template_meta": meta, "template_type": template_type})
        return types.SimpleNamespace(template_type="qwen3_5")

    swift = types.ModuleType("swift")
    swift_model = types.ModuleType("swift.model")
    swift_template = types.ModuleType("swift.template")
    swift_model.get_model_info_meta = get_model_info_meta
    swift_template.get_template_meta = get_template_meta
    monkeypatch.setitem(sys.modules, "swift", swift)
    monkeypatch.setitem(sys.modules, "swift.model", swift_model)
    monkeypatch.setitem(sys.modules, "swift.template", swift_template)

    evidence = swift_identity(tmp_path)

    assert observed["path"] == str(tmp_path)
    assert observed["model_type"] == "qwen3_5"
    assert observed["download_model"] is False
    assert observed["template_type"] == "qwen3_5"
    assert observed["template_info"].model_type == "qwen3_5"
    assert observed["template_meta"].candidate_templates == ["qwen3_5"]
    assert evidence == {
        "requested_model_type": "qwen3_5",
        "requested_template": "qwen3_5",
        "selection": "explicit",
        "model_type": "qwen3_5",
        "model_meta_template": None,
        "candidate_templates": ["qwen3_5"],
        "resolved_template": "qwen3_5",
        "passed": True,
    }


def test_swift_identity_rejects_wrong_explicit_template(monkeypatch, tmp_path: Path) -> None:
    swift = types.ModuleType("swift")
    swift_model = types.ModuleType("swift.model")
    swift_template = types.ModuleType("swift.template")
    swift_model.get_model_info_meta = lambda *args, **kwargs: (
        types.SimpleNamespace(model_type="qwen3_5"),
        types.SimpleNamespace(template=None, candidate_templates=["qwen3_5"]),
    )
    swift_template.get_template_meta = lambda *args, **kwargs: types.SimpleNamespace(template_type="ovis_ocr2")
    monkeypatch.setitem(sys.modules, "swift", swift)
    monkeypatch.setitem(sys.modules, "swift.model", swift_model)
    monkeypatch.setitem(sys.modules, "swift.template", swift_template)

    with pytest.raises(RuntimeError, match="explicit Qwen3.5 identity"):
        swift_identity(tmp_path)


def test_qwen_training_structure_freezes_nested_vision_and_disables_language_cache() -> None:
    torch = pytest.importorskip("torch")

    language_model = torch.nn.Linear(2, 2)
    language_model.config = types.SimpleNamespace(use_cache=True)
    vision = torch.nn.Linear(2, 2)
    model = types.SimpleNamespace(model=types.SimpleNamespace(visual=vision, language_model=language_model))

    evidence = configure_qwen_training_structure(model)

    assert not any(parameter.requires_grad for parameter in vision.parameters())
    assert language_model.config.use_cache is False
    assert evidence == {
        "vision_parameter_tensors": 2,
        "vision_parameters": 6,
        "vision_frozen": True,
        "vision_source_devices": ["cpu"],
        "vision_training_devices": ["cpu"],
        "vision_storage_bytes": 24,
        "vision_cpu_resident": True,
        "vision_moved_to_cpu": False,
        "language_model_use_cache": False,
        "passed": True,
    }


def test_qwen_training_structure_rejects_wrong_component_layout() -> None:
    with pytest.raises(RuntimeError, match="component was not found"):
        configure_qwen_training_structure(types.SimpleNamespace(model=types.SimpleNamespace()))


def test_cuda_qualification_requires_measured_vision_offload_savings() -> None:
    qualifier = (ROOT / "scripts/cuda/qualify.py").read_text()
    production = (ROOT / "scripts/train/run_sft.py").read_text()
    runtime = (ROOT / "scripts/train/qwen_runtime.py").read_text()
    assert 'vision.to("cpu")' in runtime
    for source in (qualifier, production):
        assert "cuda_allocated_released_by_vision_offload_bytes" in source
        assert 'RuntimeError("frozen vision offload did not release CUDA memory")' in source
    assert 'enforce_cuda_peak(recipe["maximum_peak_vram_bytes"],journal_path,"sequence-envelope")' in qualifier
    assert 'enforce_cuda_peak(recipe["maximum_peak_vram_bytes"],journal_path,"optimizer-step"' in qualifier
    assert 'if current_peak>maximum: raise RuntimeError(f"peak VRAM {current_peak} exceeds {maximum}")' in production


def test_cuda_peak_is_enforced_at_intermediate_checkpoints(monkeypatch, tmp_path: Path) -> None:
    torch = pytest.importorskip("torch")
    monkeypatch.setattr(torch.cuda, "max_memory_allocated", lambda _device: 100)
    monkeypatch.setattr(torch.cuda, "max_memory_reserved", lambda _device: 120)
    journal = tmp_path / "journal.jsonl"
    assert enforce_cuda_peak(120, journal, "sequence-envelope") == {
        "peak_allocated_bytes": 100,
        "peak_reserved_bytes": 120,
    }
    with pytest.raises(RuntimeError, match="peak CUDA VRAM 120 exceeds frozen ceiling 119"):
        enforce_cuda_peak(119, journal, "optimizer-step", index=0)


def test_saved_adapter_reloads_and_merges_without_second_base_load(tmp_path: Path) -> None:
    pytest.importorskip("peft")
    pytest.importorskip("transformers")
    from peft import LoraConfig, get_peft_model
    from transformers import GPT2Config, GPT2LMHeadModel

    base = GPT2LMHeadModel(GPT2Config(n_layer=1,n_head=1,n_embd=8,vocab_size=32))
    trained = get_peft_model(
        base,
        LoraConfig(r=2,lora_alpha=4,target_modules=["c_attn"],bias="none",task_type="CAUSAL_LM"),
    )
    adapter_dir = tmp_path / "adapter"
    trained.save_pretrained(adapter_dir,safe_serialization=True)

    merged,evidence = reload_and_merge_saved_adapter(trained,adapter_dir)

    assert not any("lora_" in name for name,_ in merged.named_modules())
    assert evidence == {
        "adapter_unloaded_before_reload": True,
        "adapter_reloaded": True,
        "safe_merge": True,
        "second_base_model_load": False,
        "passed": True,
    }


def test_qwen_serving_cache_is_restored_after_training() -> None:
    language_model = types.SimpleNamespace(config=types.SimpleNamespace(use_cache=False))
    model = types.SimpleNamespace(model=types.SimpleNamespace(language_model=language_model))

    evidence = restore_qwen_serving_cache(model)

    assert language_model.config.use_cache is True
    assert evidence == {"language_model_use_cache": True, "passed": True}


def test_resolved_kernel_implementation_reports_decorator_target() -> None:
    def external_kernel():
        return None

    def decorate(implementation):
        def wrapper():
            return implementation()
        return wrapper

    identity = resolved_kernel_implementation(decorate(external_kernel))
    assert identity == {
        "wrapper_module": __name__,
        "wrapper_name": "wrapper",
        "implementation_module": __name__,
        "implementation_name": "external_kernel",
    }


def test_resolved_kernel_implementation_fails_without_dispatch_closure() -> None:
    def plain_function():
        return None

    with pytest.raises(RuntimeError, match="no resolved implementation"):
        resolved_kernel_implementation(plain_function)


def test_docker_context_excludes_models_and_measurement_archives() -> None:
    ignore = (ROOT / ".dockerignore").read_text().splitlines()
    assert ignore[0] == "**"
    assert "!pyproject.toml" in ignore and "!uv.lock" in ignore
    assert all("models" not in row and "measurement" not in row for row in ignore[1:])


def test_execution_card_never_claims_executed_evidence() -> None:
    card = json.loads((ROOT / "measurement/cuda/execution_card.json").read_text())
    assert card["status"] == "not_ready"
    assert card["gcloud_inspected_or_used"] is False
    assert card["execution"]["maximum_cost_usd"] <= 5
    assert card["provider_discovery"]["secret_values_inspected"] is False
    assert card["qualification_order"] == [PRIMARY_RECIPE, FALLBACK_RECIPE]
