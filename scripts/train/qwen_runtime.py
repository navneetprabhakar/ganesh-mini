"""Fail-closed Qwen3.5 structure and PEFT lifecycle helpers."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any


CUDA_ALLOCATOR_CONFIG = "expandable_segments:True"
LIGER_KERNEL_VERSION = "0.8.2"


def configure_cuda_allocator(expected: str) -> dict[str,Any]:
    if expected != CUDA_ALLOCATOR_CONFIG:
        raise RuntimeError(f"unsupported CUDA allocator contract: {expected!r}")
    observed = os.environ.get("PYTORCH_CUDA_ALLOC_CONF")
    torch_module = sys.modules.get("torch")
    cuda_initialized = bool(
        torch_module is not None
        and hasattr(torch_module,"cuda")
        and torch_module.cuda.is_initialized()
    )
    if cuda_initialized and observed != expected:
        raise RuntimeError("CUDA allocator was initialized before the frozen allocator contract")
    if observed is None:
        os.environ["PYTORCH_CUDA_ALLOC_CONF"] = expected
        observed = expected
    if observed != expected:
        raise RuntimeError(f"CUDA allocator contract mismatch: expected={expected!r} observed={observed!r}")
    return {
        "environment_variable":"PYTORCH_CUDA_ALLOC_CONF",
        "value":observed,
        "cuda_initialized_before_validation":cuda_initialized,
        "passed":True,
    }


def configure_fused_training_loss(model: Any, expected_version: str) -> dict[str,Any]:
    """Patch only Qwen3.5 fused linear CE; keep all other kernels unchanged."""
    from importlib.metadata import version

    if expected_version != LIGER_KERNEL_VERSION:
        raise RuntimeError(f"unsupported Liger Kernel contract: {expected_version!r}")
    observed_version = version("liger-kernel")
    if observed_version != expected_version:
        raise RuntimeError(
            f"Liger Kernel version mismatch: expected={expected_version!r} observed={observed_version!r}"
        )
    from liger_kernel.transformers import apply_liger_kernel_to_qwen3_5

    apply_liger_kernel_to_qwen3_5(
        rope=False,
        cross_entropy=False,
        fused_linear_cross_entropy=True,
        rms_norm=False,
        swiglu=False,
        model=model,
    )
    forward = getattr(model.forward,"__func__",model.forward)
    forward_module = getattr(forward,"__module__",None)
    forward_name = getattr(forward,"__name__",None)
    passed = (
        forward_module == "liger_kernel.transformers.model.qwen3_5"
        and forward_name == "lce_forward_for_multimodal"
    )
    if not passed:
        raise RuntimeError(
            "Qwen3.5 fused linear cross entropy did not bind the expected multimodal forward: "
            f"{forward_module=}, {forward_name=}"
        )
    return {
        "provider":"liger-kernel",
        "version":observed_version,
        "forward_module":forward_module,
        "forward_name":forward_name,
        "fused_linear_cross_entropy":True,
        "materialize_training_logits":False,
        "other_liger_kernels_enabled":False,
        "passed":True,
    }


def configure_qwen_training_structure(model: Any) -> dict[str,Any]:
    inner = getattr(model,"model",None)
    vision = getattr(inner,"visual",None)
    language_model = getattr(inner,"language_model",None)
    if vision is None or language_model is None:
        raise RuntimeError("Qwen3.5 vision or language-model component was not found at model.model")
    vision_parameters = list(vision.parameters())
    if not vision_parameters:
        raise RuntimeError("Qwen3.5 vision tower exposes no parameters to freeze")
    for parameter in vision_parameters:
        parameter.requires_grad = False
    vision_source_devices = sorted({parameter.device.type for parameter in vision_parameters})
    vision_storage_bytes = sum(parameter.numel() * parameter.element_size() for parameter in vision_parameters)
    vision.to("cpu")
    vision_training_devices = sorted({parameter.device.type for parameter in vision_parameters})
    language_config = getattr(language_model,"config",None)
    if language_config is None or not hasattr(language_config,"use_cache"):
        raise RuntimeError("Qwen3.5 language-model cache configuration is unavailable")
    language_config.use_cache = False
    if (
        any(parameter.requires_grad for parameter in vision_parameters)
        or vision_training_devices != ["cpu"]
        or language_config.use_cache is not False
    ):
        raise RuntimeError("Qwen3.5 training structure did not freeze/offload vision and disable language cache")
    return {
        "vision_parameter_tensors":len(vision_parameters),
        "vision_parameters":sum(parameter.numel() for parameter in vision_parameters),
        "vision_frozen":True,
        "vision_source_devices":vision_source_devices,
        "vision_training_devices":vision_training_devices,
        "vision_storage_bytes":vision_storage_bytes,
        "vision_cpu_resident":True,
        "vision_moved_to_cpu":vision_source_devices != ["cpu"],
        "language_model_use_cache":False,
        "passed":True,
    }


def unload_and_reload_saved_adapter(model: Any, adapter_dir: Path) -> tuple[Any,dict[str,Any]]:
    from peft import PeftModel

    unload = getattr(model,"unload",None)
    if not callable(unload):
        raise RuntimeError("trained PEFT model cannot unload its in-memory adapter")
    base = unload()
    del model
    if any("lora_" in name for name,_ in base.named_modules()):
        raise RuntimeError("LoRA modules remained after unloading the in-memory adapter")
    reloaded = PeftModel.from_pretrained(base,adapter_dir,is_trainable=False)
    if not any("lora_" in name for name,_ in reloaded.named_modules()):
        raise RuntimeError("saved LoRA adapter did not reload into the base model")
    return reloaded,{
        "adapter_unloaded_before_reload":True,
        "adapter_reloaded":True,
        "second_base_model_load":False,
        "passed":True,
    }


def reload_and_merge_saved_adapter(model: Any, adapter_dir: Path) -> tuple[Any,dict[str,Any]]:
    reloaded,evidence = unload_and_reload_saved_adapter(model,adapter_dir)
    merged = reloaded.merge_and_unload(safe_merge=True)
    if any("lora_" in name for name,_ in merged.named_modules()):
        raise RuntimeError("LoRA modules remained after safe merge")
    return merged,{**evidence,"safe_merge":True}


def restore_qwen_serving_cache(model: Any) -> dict[str,Any]:
    language_model = getattr(getattr(model,"model",None),"language_model",None)
    language_config = getattr(language_model,"config",None)
    if language_config is None or not hasattr(language_config,"use_cache"):
        raise RuntimeError("merged Qwen3.5 language-model cache configuration is unavailable")
    language_config.use_cache = True
    if language_config.use_cache is not True:
        raise RuntimeError("merged Qwen3.5 serving cache was not restored")
    return {"language_model_use_cache":True,"passed":True}
