#!/usr/bin/env python3
"""Fail-closed CUDA LoRA qualification for the pinned Qwen3.5 checkpoint."""
from __future__ import annotations

import argparse, gc, hashlib, importlib, importlib.metadata, inspect, json, os, platform, resource, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.train.qwen_runtime import (
    configure_qwen_training_structure,
    unload_and_reload_saved_adapter,
    restore_qwen_serving_cache,
)
from scripts.train.response_only import ResponseOnlyError, build_response_only_encoding

PACKAGE_IMPORTS = {"torch":"torch","torchvision":"torchvision","transformers":"transformers","peft":"peft","ms-swift":"swift","bitsandbytes":"bitsandbytes","flash-linear-attention":"fla","causal-conv1d":"causal_conv1d","accelerate":"accelerate","qwen-vl-utils":"qwen_vl_utils","triton":"triton"}
PRIMARY_RECIPE = "bf16-lora-primary-v1"
FALLBACK_RECIPE = "nf4-qlora-fallback-v1"

class PeakVramExceeded(RuntimeError):
    def __init__(self, observed: int, maximum: int) -> None:
        self.observed = observed
        self.maximum = maximum
        super().__init__(f"peak CUDA VRAM {observed} exceeds frozen ceiling {maximum}")

def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""): digest.update(chunk)
    return digest.hexdigest()

def write_evidence(value: dict[str, Any], path: Path) -> None:
    unsigned = dict(value); unsigned.pop("evidence_sha256", None)
    value["evidence_sha256"] = canonical_sha256(unsigned)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        handle.write(json.dumps(value, indent=2, sort_keys=True) + "\n")
        handle.flush(); os.fsync(handle.fileno())
    temporary.replace(path)

def append_journal(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {"recorded_at": datetime.now(timezone.utc).isoformat(), **event}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
        handle.flush(); os.fsync(handle.fileno())

def load_and_validate_config(path: Path, root: Path) -> dict[str, Any]:
    config = json.loads(path.read_text(encoding="utf-8"))
    if config.get("schema_version") != "ganesh-mini-cuda-gate0/v3": raise ValueError("unsupported CUDA qualification schema")
    contract_path = root / config["model"]["contract_path"]
    if file_sha256(contract_path) != config["model"]["contract_sha256"]: raise ValueError("model contract hash mismatch")
    if file_sha256(root / "uv.lock") != config["container"]["uv_lock_sha256"]: raise ValueError("CUDA environment lock hash mismatch")
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    if (contract.get("model_id"), contract.get("revision")) != (config["model"]["model_id"], config["model"]["revision"]):
        raise ValueError("model identity does not match the pinned contract")
    if config.get("qualification_order") != [PRIMARY_RECIPE, FALLBACK_RECIPE]: raise ValueError("BF16 primary and NF4 fallback order changed")
    common = {"sequence_length":4096,"micro_batch_size":1,"gradient_checkpointing":True,"record_count":16,"rank":32,"alpha":64,"dropout":0.05,"learning_rate":0.00001,"response_only":True,"network_during_execution":False,"maximum_peak_vram_bytes":21*1024**3}
    primary = {"role":"primary","minimum_vram_bytes":22*1024**3,"base_dtype":"bfloat16","quantization":None,**common}
    fallback = {"role":"fallback","minimum_vram_bytes":17179869184,"base_dtype":"bfloat16","quantization":{"bits":4,"type":"nf4","double_quantization":True,"compute_dtype":"bfloat16"},**common}
    if config["recipes"].get(PRIMARY_RECIPE) != primary: raise ValueError("BF16 LoRA primary recipe changed without a schema revision")
    if config["recipes"].get(FALLBACK_RECIPE) != fallback: raise ValueError("NF4 QLoRA fallback recipe changed without a schema revision")
    budget = config["budget"]
    if budget["maximum_usd"] > 1 or budget["maximum_wall_seconds"] > 3600 or budget["maximum_gpu_count"] != 1: raise ValueError("qualification exceeds the authorized bound")
    return config

def package_identity(expected: dict[str,str]) -> dict[str,Any]:
    observed, imports = {}, {}
    for distribution, module in PACKAGE_IMPORTS.items():
        try:
            observed[distribution] = importlib.metadata.version(distribution)
            __import__(module)
            imports[module] = True
        except Exception as exc:
            raise RuntimeError(
                f"required package import failed: distribution={distribution} module={module} "
                f"error_type={type(exc).__name__} error={exc}"
            ) from exc
    passed = observed == expected
    if not passed: raise RuntimeError(f"pinned package identity mismatch: expected={expected}, observed={observed}")
    return {"expected":expected,"observed":observed,"imports":imports,"passed":passed}

def gpu_identity(config: dict[str,Any], recipe: dict[str,Any]) -> dict[str,Any]:
    import torch
    if platform.system() != "Linux" or not torch.cuda.is_available() or torch.cuda.device_count() != 1: raise RuntimeError("qualification requires exactly one Linux CUDA GPU")
    props = torch.cuda.get_device_properties(0); capability = list(torch.cuda.get_device_capability(0)); minimum = config["hardware"]["minimum_compute_capability"]
    passed = capability >= minimum and props.total_memory >= recipe["minimum_vram_bytes"] and torch.cuda.is_bf16_supported()
    if not passed: raise RuntimeError(f"GPU does not meet recipe floor: observed_vram={props.total_memory}, required_vram={recipe['minimum_vram_bytes']}, capability={capability}, bf16={torch.cuda.is_bf16_supported()}")
    smi = subprocess.run(["nvidia-smi","--query-gpu=name,uuid,driver_version,memory.total","--format=csv,noheader,nounits"],check=True,capture_output=True,text=True,timeout=10).stdout.strip()
    return {"name":props.name,"compute_capability":capability,"total_memory_bytes":props.total_memory,"required_memory_bytes":recipe["minimum_vram_bytes"],"bfloat16_supported":torch.cuda.is_bf16_supported(),"torch_cuda":torch.version.cuda,"cudnn":torch.backends.cudnn.version(),"nvidia_smi_csv":smi,"passed":passed}

def triton_identity() -> dict[str,Any]:
    import triton
    try:
        target = triton.runtime.driver.active.get_current_target()
    except Exception as exc:
        raise RuntimeError(
            f"Triton CUDA backend initialization failed: error_type={type(exc).__name__} error={exc}"
        ) from exc
    if target.backend != "cuda":
        raise RuntimeError(f"Triton selected a non-CUDA backend: {target.backend}")
    return {"version":triton.__version__,"backend":target.backend,"architecture":str(target.arch),"cache_dir":os.environ.get("TRITON_CACHE_DIR"),"passed":True}

def install_fla_recurrent_compatibility() -> dict[str,Any]:
    """Expose FLA 0.5's fused recurrent kernel under Transformers' expected name."""
    model_module = "transformers.models.qwen3_5.modeling_qwen3_5"
    if model_module in sys.modules:
        raise RuntimeError("FLA recurrent compatibility must be installed before Qwen3.5 model import")
    module = importlib.import_module("fla.ops.gated_delta_rule")
    requested_name = "recurrent_gated_delta_rule"
    source_name = "fused_recurrent_gated_delta_rule"
    implementation = getattr(module, requested_name, None)
    installed_alias = implementation is None
    if installed_alias:
        implementation = getattr(module, source_name, None)
        if not callable(implementation):
            raise RuntimeError(f"FLA exposes neither {requested_name} nor callable {source_name}")
        setattr(module, requested_name, implementation)
    if not callable(implementation):
        raise RuntimeError(f"FLA {requested_name} is not callable")
    implementation_module = implementation.__module__
    passed = implementation_module == "fla" or implementation_module.startswith("fla.")
    if not passed:
        raise RuntimeError(f"FLA recurrent implementation resolved outside fla: {implementation_module}")
    return {
        "requested_symbol":"fla.ops.gated_delta_rule.recurrent_gated_delta_rule",
        "resolved_symbol":f"{implementation_module}.{implementation.__name__}",
        "installed_alias":installed_alias,
        "passed":passed,
    }

def resolved_kernel_implementation(function: Any) -> dict[str,Any]:
    implementation = inspect.getclosurevars(function).nonlocals.get("implementation")
    if not callable(implementation):
        raise RuntimeError(f"kernel wrapper has no resolved implementation: {function.__module__}.{function.__name__}")
    return {
        "wrapper_module": function.__module__,
        "wrapper_name": function.__name__,
        "implementation_module": implementation.__module__,
        "implementation_name": implementation.__name__,
    }

def kernel_identity() -> dict[str,Any]:
    import triton
    from fla.utils import _device as fla_device
    from transformers.models.qwen3_5 import modeling_qwen3_5
    triton_backend = triton.runtime.driver.active.get_current_target().backend
    backend = {
        "triton": triton_backend,
        "fla": fla_device.device_platform,
        "fla_is_nvidia": bool(fla_device.IS_NVIDIA),
    }
    if backend != {"triton":"cuda","fla":"cuda","fla_is_nvidia":True}:
        raise RuntimeError(f"CUDA kernel backend mismatch: {backend}")
    expected = {
        "causal_conv1d_fn": (modeling_qwen3_5.causal_conv1d_fn, "causal_conv1d"),
        "causal_conv1d_update": (modeling_qwen3_5.causal_conv1d_update, "causal_conv1d"),
        "chunk_gated_delta_rule": (modeling_qwen3_5.torch_chunk_gated_delta_rule, "fla"),
        "recurrent_gated_delta_rule": (modeling_qwen3_5.torch_recurrent_gated_delta_rule, "fla"),
    }
    implementations = {}
    for name, (function, package) in expected.items():
        identity = resolved_kernel_implementation(function)
        module = identity["implementation_module"]
        identity["expected_package"] = package
        identity["passed"] = module == package or module.startswith(package + ".")
        implementations[name] = identity
    if not all(identity["passed"] for identity in implementations.values()):
        raise RuntimeError(f"Qwen3.5 CUDA fast path did not resolve external kernels: {implementations}")
    return {"backend":backend,"implementations":implementations,"passed":True}

def swift_identity(model_dir: Path) -> dict[str,Any]:
    from swift.model import get_model_info_meta
    from swift.template import get_template_meta

    requested_model_type = "qwen3_5"
    requested_template = "qwen3_5"
    info, meta = get_model_info_meta(
        str(model_dir), model_type=requested_model_type, download_model=False
    )
    template_meta = get_template_meta(info, meta, template_type=requested_template)
    model_type = getattr(info,"model_type",None)
    resolved_template = getattr(template_meta,"template_type",None)
    passed = model_type == requested_model_type and resolved_template == requested_template
    if not passed:
        raise RuntimeError(
            "ms-swift did not resolve the explicit Qwen3.5 identity: "
            f"{model_type=}, {resolved_template=}"
        )
    return {
        "requested_model_type":requested_model_type,
        "requested_template":requested_template,
        "selection":"explicit",
        "model_type":model_type,
        "model_meta_template":getattr(meta,"template",None),
        "candidate_templates":list(getattr(meta,"candidate_templates",[])),
        "resolved_template":resolved_template,
        "passed":passed,
    }

def select_records(path: Path, tokenizer: Any, count: int, max_length: int) -> list[dict[str,Any]]:
    candidates = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line); rendered = tokenizer.apply_chat_template(row["messages"],tokenize=False,add_generation_prompt=False); tokens = len(tokenizer(rendered,add_special_tokens=False).input_ids)
            if tokens <= max_length: candidates.append((tokens,row["id"],row,rendered))
    candidates.sort(key=lambda value:(value[0],value[1]))
    if len(candidates) < count: raise ValueError(f"only {len(candidates)} records fit max_length={max_length}")
    indices = [round(index * (len(candidates)-1) / (count-1)) for index in range(count)]
    return [{"tokens":candidates[index][0],"row":candidates[index][2],"rendered":candidates[index][3]} for index in indices]

def response_only_batch(tokenizer: Any, messages: list[dict[str,str]], max_length: int, device: str) -> dict[str,Any]:
    try:
        response = build_response_only_encoding(
            tokenizer, messages, max_length=max_length, return_tensors="pt"
        )
    except ResponseOnlyError as exc:
        raise RuntimeError(str(exc)) from exc
    return {key:value.to(device) for key,value in response.encoding.items()}

def load_model(model_dir: Path, recipe_id: str):
    import torch
    from transformers import AutoModelForImageTextToText, BitsAndBytesConfig
    kwargs: dict[str,Any] = {"local_files_only":True,"dtype":torch.bfloat16,"device_map":{"":0}}
    if recipe_id == FALLBACK_RECIPE: kwargs["quantization_config"] = BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type="nf4",bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.bfloat16)
    return AutoModelForImageTextToText.from_pretrained(model_dir,**kwargs)

def sequence_envelope_probe(model: Any, tokenizer: Any, length: int) -> dict[str,Any]:
    """Backward-only synthetic shape probe; no optimizer step or quality claim."""
    import torch
    if tokenizer.eos_token_id is None: raise RuntimeError("tokenizer has no EOS token for deterministic envelope probe")
    input_ids = torch.full((1,length),tokenizer.eos_token_id,dtype=torch.long,device="cuda:0"); labels = input_ids.clone(); labels[:,:64] = -100; attention_mask = torch.ones_like(input_ids)
    model.zero_grad(set_to_none=True); output = model(input_ids=input_ids,attention_mask=attention_mask,labels=labels)
    if not torch.isfinite(output.loss) or output.loss.detach().item() <= 0: raise RuntimeError("non-finite or non-positive loss in 4,096-token synthetic envelope probe")
    output.loss.backward(); model.zero_grad(set_to_none=True)
    return {"kind":"synthetic-active-token-shape-probe","sequence_length":length,"input_tokens":length,"supervised_tokens":length-64,"masked_prompt_tokens":64,"micro_batch_size":1,"optimizer_step":False,"quality_training_record":False,"loss_finite":True,"loss_positive":bool(output.loss.detach().item()>0),"passed":True}

def enforce_cuda_peak(maximum: int, journal_path: Path | None, phase: str, **fields: Any) -> dict[str,int]:
    import torch
    memory = {
        "peak_allocated_bytes":torch.cuda.max_memory_allocated(0),
        "peak_reserved_bytes":torch.cuda.max_memory_reserved(0),
    }
    observed = max(memory.values())
    if journal_path:
        append_journal(journal_path,{"phase":"cuda-peak","checkpoint":phase,"observed_peak_bytes":observed,"maximum_peak_vram_bytes":maximum,**memory,**fields})
    if observed > maximum:
        raise PeakVramExceeded(observed,maximum)
    return memory

def run_training_smoke(config: dict[str,Any], recipe_id: str, model_dir: Path, records_path: Path, adapter_dir: Path, model: Any, tokenizer: Any, model_load_peak: dict[str,int], journal_path: Path | None = None) -> dict[str,Any]:
    import torch
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    recipe = config["recipes"][recipe_id]
    vision_offload_before = torch.cuda.memory_allocated(0)
    training_structure = configure_qwen_training_structure(model)
    gc.collect(); torch.cuda.empty_cache()
    vision_offload_after = torch.cuda.memory_allocated(0)
    training_structure["cuda_allocated_before_vision_offload_bytes"] = vision_offload_before
    training_structure["cuda_allocated_after_vision_offload_bytes"] = vision_offload_after
    training_structure["cuda_allocated_released_by_vision_offload_bytes"] = vision_offload_before - vision_offload_after
    if not training_structure["vision_moved_to_cpu"] or vision_offload_after >= vision_offload_before:
        raise RuntimeError("frozen vision offload did not release CUDA memory")
    if journal_path: append_journal(journal_path,{"phase":"training-structure","state":"completed",**training_structure})
    quantized = [name for name,value in model.named_parameters() if value.__class__.__name__ == "Params4bit"]
    if recipe_id == FALLBACK_RECIPE:
        import bitsandbytes as bnb
        if not quantized: raise RuntimeError("bitsandbytes NF4 parameters were not observed")
        linear_type = bnb.nn.Linear4bit; model = prepare_model_for_kbit_training(model,use_gradient_checkpointing=True)
    else:
        if quantized: raise RuntimeError("BF16 primary unexpectedly contains quantized parameters")
        linear_type = torch.nn.Linear; model.gradient_checkpointing_enable(); model.enable_input_require_grads()
    if not model.is_gradient_checkpointing:
        raise RuntimeError("gradient checkpointing did not activate on the Qwen3.5 language model")
    targets = [name for name,module in model.named_modules() if isinstance(module,linear_type) and name.startswith("model.language_model.") and not name.endswith("lm_head")]
    if not targets: raise RuntimeError("no eligible language-model linear modules found")
    model = get_peft_model(model,LoraConfig(r=recipe["rank"],lora_alpha=recipe["alpha"],lora_dropout=recipe["dropout"],target_modules=targets,bias="none",task_type="CAUSAL_LM"))
    trainable = {name for name,parameter in model.named_parameters() if parameter.requires_grad}
    if not trainable or any("visual" in name or "lm_head" in name for name in trainable): raise RuntimeError("adapter targeting escaped the language model or produced no trainable parameters")
    records = select_records(records_path,tokenizer,recipe["record_count"],recipe["sequence_length"]); optimizer = torch.optim.AdamW((value for value in model.parameters() if value.requires_grad),lr=recipe["learning_rate"])
    torch.cuda.reset_peak_memory_stats(0); envelope = sequence_envelope_probe(model,tokenizer,recipe["sequence_length"])
    envelope["cuda_memory"] = enforce_cuda_peak(recipe["maximum_peak_vram_bytes"],journal_path,"sequence-envelope")
    losses, gradients, active_tokens, response_tokens = [], set(), 0, 0
    torch.cuda.synchronize(); training_started = time.monotonic(); model.train()
    for index, item in enumerate(records):
        if journal_path: append_journal(journal_path,{"phase":"training-record","state":"started","index":index,"record_id":item["row"]["id"]})
        batch = response_only_batch(tokenizer,item["row"]["messages"],recipe["sequence_length"],"cuda:0"); optimizer.zero_grad(set_to_none=True); output = model(**batch)
        if not torch.isfinite(output.loss) or output.loss.detach().item() <= 0: raise RuntimeError(f"non-finite or non-positive loss for {item['row']['id']}")
        output.loss.backward(); gradients.update(name for name,parameter in model.named_parameters() if parameter.requires_grad and parameter.grad is not None and torch.count_nonzero(parameter.grad).item() > 0); optimizer.step()
        enforce_cuda_peak(recipe["maximum_peak_vram_bytes"],journal_path,"optimizer-step",index=index,record_id=item["row"]["id"])
        active_tokens += int(batch["attention_mask"].sum().item()); response_tokens += int((batch["labels"] != -100).sum().item()); losses.append(float(output.loss.detach().cpu()))
        if journal_path: append_journal(journal_path,{"phase":"training-record","state":"completed","index":index,"record_id":item["row"]["id"],"loss":losses[-1]})
    torch.cuda.synchronize(); training_seconds = time.monotonic()-training_started; missing = sorted(trainable-gradients)
    if missing: raise RuntimeError(f"{len(missing)} trainable adapter parameters never received non-zero gradients")
    memory = {"training_peak_allocated_bytes":torch.cuda.max_memory_allocated(0),"training_peak_reserved_bytes":torch.cuda.max_memory_reserved(0)}
    model.eval(); probe = tokenizer("def add(a, b):",return_tensors="pt").to("cuda:0")
    with torch.inference_mode(): trained_logits = model(**probe).logits[:,-1,:].float().cpu()
    if journal_path: append_journal(journal_path,{"phase":"adapter-save","state":"started"})
    adapter_dir.mkdir(parents=True,exist_ok=False); model.save_pretrained(adapter_dir,safe_serialization=True); tokenizer.save_pretrained(adapter_dir); hashes = {path.name:file_sha256(path) for path in sorted(adapter_dir.iterdir()) if path.is_file()}
    if journal_path: append_journal(journal_path,{"phase":"adapter-save","state":"completed","file_sha256":hashes})
    del optimizer; model.zero_grad(set_to_none=True); gc.collect(); torch.cuda.empty_cache()
    if journal_path: append_journal(journal_path,{"phase":"adapter-reload-merge","state":"started"})
    reloaded, reload_merge = unload_and_reload_saved_adapter(model,adapter_dir); reloaded.eval()
    with torch.inference_mode(): reloaded_logits = reloaded(**probe).logits[:,-1,:].float().cpu()
    reload_max_abs = float((trained_logits-reloaded_logits).abs().max())
    if reload_max_abs > 0.01: raise RuntimeError("saved/reloaded adapter logits do not reproduce the trained adapter")
    merged = reloaded.merge_and_unload(safe_merge=True)
    if any("lora_" in name for name,_ in merged.named_modules()): raise RuntimeError("LoRA modules remained after safe merge")
    reload_merge["safe_merge"] = True
    serving_structure = restore_qwen_serving_cache(merged); merged.eval()
    with torch.inference_mode(): merged_logits = merged(**probe).logits[:,-1,:].float().cpu()
    merge_finite = bool(torch.isfinite(merged_logits).all().item()); merge_max_abs = float((trained_logits-merged_logits).abs().max())
    merge_close = bool(torch.allclose(trained_logits,merged_logits,atol=0.25,rtol=0.02))
    if not merge_finite or not merge_close: raise RuntimeError("merged checkpoint logits are non-finite or outside the frozen BF16 equivalence tolerance")
    merged_dir = adapter_dir.parent / f"merged-{recipe_id}"
    merged_dir.mkdir(parents=False,exist_ok=False); merged.save_pretrained(merged_dir,safe_serialization=True); tokenizer.save_pretrained(merged_dir)
    merged_hashes = {path.name:file_sha256(path) for path in sorted(merged_dir.iterdir()) if path.is_file()}
    memory.update({"full_smoke_peak_allocated_bytes":torch.cuda.max_memory_allocated(0),"full_smoke_peak_reserved_bytes":torch.cuda.max_memory_reserved(0)})
    observed_peak = max((*model_load_peak.values(),*memory.values()))
    if observed_peak > recipe["maximum_peak_vram_bytes"]:
        raise PeakVramExceeded(observed_peak,recipe["maximum_peak_vram_bytes"])
    if journal_path: append_journal(journal_path,{"phase":"adapter-reload-merge","state":"completed","file_sha256":merged_hashes,"reload_max_abs_logit_difference":reload_max_abs,"merge_max_abs_logit_difference":merge_max_abs,"logits_finite":True})
    equivalence = {"probe":"def add(a, b):","reload_atol":0.01,"reload_max_abs_logit_difference":reload_max_abs,"merge_atol":0.25,"merge_rtol":0.02,"merge_max_abs_logit_difference":merge_max_abs,"passed":True}
    return {"recipe_id":recipe_id,"records":[{"id":item["row"]["id"],"tokens":item["tokens"],"rendered_prompt_sha256":hashlib.sha256(item["rendered"].encode()).hexdigest()} for item in records],"response_only":True,"model_load_reused_after_inference":True,"optimizer_steps":len(records),"losses":losses,"losses_finite_and_positive":True,"sequence_envelope":envelope,"training_structure":training_structure,"serving_structure":serving_structure,"gradient_checkpointing":True,"quantized_parameter_count":len(quantized),"target_module_count":len(targets),"target_modules":targets,"trainable_parameter_names":sorted(trainable),"gradient_parameter_names":sorted(gradients),"training_seconds":training_seconds,"active_tokens":active_tokens,"response_tokens":response_tokens,"active_tokens_per_second":active_tokens/training_seconds,"response_tokens_per_second":response_tokens/training_seconds,"cuda_memory":{"model_load":model_load_peak,"training":memory,"observed_peak_bytes":observed_peak,"maximum_peak_vram_bytes":recipe["maximum_peak_vram_bytes"],"passed":True},"adapter_file_sha256":hashes,"reload_merge":reload_merge,"serialization_equivalence":equivalence,"merged_checkpoint_file_sha256":merged_hashes,"merge_logits_finite":merge_finite,"passed":True}

def inference_smoke(model: Any, tokenizer: Any) -> dict[str,Any]:
    import torch
    model.eval(); messages = [{"role":"user","content":"Return only a Python function add(a, b) that returns the sum."}]; rendered = tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False); inputs = tokenizer(rendered,return_tensors="pt").to("cuda:0")
    with torch.inference_mode(): generated = model.generate(**inputs,do_sample=False,max_new_tokens=32,pad_token_id=tokenizer.eos_token_id)
    new_ids = generated[0,inputs.input_ids.shape[1]:]; raw = tokenizer.decode(new_ids,skip_special_tokens=False); clean = tokenizer.decode(new_ids,skip_special_tokens=True); passed = bool(clean.strip()) and rendered.endswith("<think>\n\n</think>\n\n")
    if not passed: raise RuntimeError("text-only non-thinking inference contract failed")
    return {"messages":messages,"rendered_prompt":rendered,"rendered_prompt_sha256":hashlib.sha256(rendered.encode()).hexdigest(),"raw_output":raw,"extracted_output":clean,"input_tokens":int(inputs.input_ids.shape[1]),"output_tokens":int(new_ids.shape[0]),"model_load_shared_with_training":True,"passed":passed}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); root = Path(__file__).resolve().parents[2]
    parser.add_argument("--config",type=Path,default=root/"configs/cuda/qwen3_5_2b_gate0.json"); parser.add_argument("--recipe",choices=[PRIMARY_RECIPE,FALLBACK_RECIPE],default=PRIMARY_RECIPE); parser.add_argument("--model-dir",type=Path,required=True); parser.add_argument("--records",type=Path,default=root/"data/seed/ganesh_v01/train.jsonl"); parser.add_argument("--adapter-dir",type=Path,default=root/"outputs/cuda/gate0-adapter"); parser.add_argument("--output",type=Path,default=root/"measurement/cuda/qualification.json"); args = parser.parse_args(); journal_path = args.output.with_suffix(".journal.jsonl")
    os.environ.setdefault("TOKENIZERS_PARALLELISM","false"); os.environ.setdefault("HF_HUB_OFFLINE","1"); os.environ.setdefault("TRANSFORMERS_OFFLINE","1"); started = time.monotonic(); evidence: dict[str,Any] = {"schema_version":"ganesh-mini-cuda-qualification/v2","status":"failed","recipe_id":args.recipe,"attempt_id":os.environ.get("GANESH_ATTEMPT_ID"),"resume_policy":"fresh-attempt-only","recorded_at":datetime.now(timezone.utc).isoformat(),"host":{"platform":platform.platform(),"machine":platform.machine(),"python":platform.python_version()}}
    try:
        append_journal(journal_path,{"phase":"qualification","state":"started","recipe_id":args.recipe})
        config = load_and_validate_config(args.config,root); recipe = config["recipes"][args.recipe]
        append_journal(journal_path,{"phase":"identity","state":"started"})
        evidence.update({"model_id":config["model"]["model_id"],"revision":config["model"]["revision"],"config_sha256":file_sha256(args.config),"model_inventory":{path.name:file_sha256(path) for path in sorted(args.model_dir.iterdir()) if path.is_file()}})
        for component, check in (("gpu",lambda:gpu_identity(config,recipe)),("triton",triton_identity),("fla_recurrent_compatibility",install_fla_recurrent_compatibility),("packages",lambda:package_identity(config["packages"])),("kernels",kernel_identity),("ms_swift",lambda:swift_identity(args.model_dir))):
            append_journal(journal_path,{"phase":"identity-component","component":component,"state":"started"})
            evidence[component] = check()
            append_journal(journal_path,{"phase":"identity-component","component":component,"state":"completed"})
        append_journal(journal_path,{"phase":"identity","state":"completed"})
        from transformers import AutoTokenizer
        import torch
        tokenizer = AutoTokenizer.from_pretrained(args.model_dir,local_files_only=True)
        torch.cuda.reset_peak_memory_stats(0)
        model = load_model(args.model_dir,args.recipe)
        model_load_peak = {"peak_allocated_bytes":torch.cuda.max_memory_allocated(0),"peak_reserved_bytes":torch.cuda.max_memory_reserved(0)}
        append_journal(journal_path,{"phase":"inference","state":"started"}); evidence["inference"] = inference_smoke(model,tokenizer); append_journal(journal_path,{"phase":"inference","state":"completed"})
        append_journal(journal_path,{"phase":"training","state":"started"}); evidence["training"] = run_training_smoke(config,args.recipe,args.model_dir,args.records,args.adapter_dir,model,tokenizer,model_load_peak,journal_path); append_journal(journal_path,{"phase":"training","state":"completed"})
        evidence["status"] = "passed"; append_journal(journal_path,{"phase":"qualification","state":"completed","status":"passed"})
    except Exception as exc:
        evidence.update({"error_type":type(exc).__name__,"error":str(exc)}); append_journal(journal_path,{"phase":"qualification","state":"completed","status":"failed","error_type":type(exc).__name__,"error":str(exc)})
        if isinstance(exc,PeakVramExceeded): evidence["peak_vram_failure"] = {"observed_peak_bytes":exc.observed,"maximum_peak_vram_bytes":exc.maximum}
    evidence["wall_seconds"] = time.monotonic()-started; evidence["peak_rss_bytes"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024; write_evidence(evidence,args.output)
    return 0 if evidence["status"] == "passed" else 2

if __name__ == "__main__": raise SystemExit(main())
