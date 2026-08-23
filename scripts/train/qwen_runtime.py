"""Fail-closed Qwen3.5 structure and PEFT lifecycle helpers."""
from __future__ import annotations

from pathlib import Path
from typing import Any


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
    language_config = getattr(language_model,"config",None)
    if language_config is None or not hasattr(language_config,"use_cache"):
        raise RuntimeError("Qwen3.5 language-model cache configuration is unavailable")
    language_config.use_cache = False
    if any(parameter.requires_grad for parameter in vision_parameters) or language_config.use_cache is not False:
        raise RuntimeError("Qwen3.5 training structure did not freeze vision and disable language cache")
    return {
        "vision_parameter_tensors":len(vision_parameters),
        "vision_parameters":sum(parameter.numel() for parameter in vision_parameters),
        "vision_frozen":True,
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
