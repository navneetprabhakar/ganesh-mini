#!/usr/bin/env python3
"""Fail-closed CUDA LoRA qualification for the pinned Qwen3.5 checkpoint."""
from __future__ import annotations

import argparse, gc, hashlib, importlib.metadata, json, os, platform, resource, subprocess, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PACKAGE_IMPORTS = {"torch":"torch","transformers":"transformers","peft":"peft","ms-swift":"swift","bitsandbytes":"bitsandbytes","flash-linear-attention":"fla","causal-conv1d":"causal_conv1d","accelerate":"accelerate","qwen-vl-utils":"qwen_vl_utils","triton":"triton"}
PRIMARY_RECIPE = "bf16-lora-primary-v1"
FALLBACK_RECIPE = "nf4-qlora-fallback-v1"

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
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def load_and_validate_config(path: Path, root: Path) -> dict[str, Any]:
    config = json.loads(path.read_text(encoding="utf-8"))
    if config.get("schema_version") != "ganesh-mini-cuda-gate0/v2": raise ValueError("unsupported CUDA qualification schema")
    contract_path = root / config["model"]["contract_path"]
    if file_sha256(contract_path) != config["model"]["contract_sha256"]: raise ValueError("model contract hash mismatch")
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    if (contract.get("model_id"), contract.get("revision")) != (config["model"]["model_id"], config["model"]["revision"]):
        raise ValueError("model identity does not match the pinned contract")
    if config.get("qualification_order") != [PRIMARY_RECIPE, FALLBACK_RECIPE]: raise ValueError("BF16 primary and NF4 fallback order changed")
    common = {"sequence_length":4096,"micro_batch_size":1,"gradient_checkpointing":True,"record_count":16,"rank":32,"alpha":64,"dropout":0.05,"learning_rate":0.00001,"response_only":True,"network_during_execution":False}
    primary = {"role":"primary","minimum_vram_bytes":25769803776,"base_dtype":"bfloat16","quantization":None,**common}
    fallback = {"role":"fallback","minimum_vram_bytes":17179869184,"base_dtype":"bfloat16","quantization":{"bits":4,"type":"nf4","double_quantization":True,"compute_dtype":"bfloat16"},**common}
    if config["recipes"].get(PRIMARY_RECIPE) != primary: raise ValueError("BF16 LoRA primary recipe changed without a schema revision")
    if config["recipes"].get(FALLBACK_RECIPE) != fallback: raise ValueError("NF4 QLoRA fallback recipe changed without a schema revision")
    budget = config["budget"]
    if budget["maximum_usd"] > 5 or budget["maximum_wall_seconds"] > 1800 or budget["maximum_gpu_count"] != 1: raise ValueError("qualification exceeds the authorized bound")
    return config

def package_identity(expected: dict[str,str]) -> dict[str,Any]:
    observed, imports = {}, {}
    for distribution, module in PACKAGE_IMPORTS.items():
        observed[distribution] = importlib.metadata.version(distribution); __import__(module); imports[module] = True
    return {"expected":expected,"observed":observed,"imports":imports,"passed":observed == expected}

def gpu_identity(config: dict[str,Any], recipe: dict[str,Any]) -> dict[str,Any]:
    import torch
    if platform.system() != "Linux" or not torch.cuda.is_available() or torch.cuda.device_count() != 1: raise RuntimeError("qualification requires exactly one Linux CUDA GPU")
    props = torch.cuda.get_device_properties(0); capability = list(torch.cuda.get_device_capability(0)); minimum = config["hardware"]["minimum_compute_capability"]
    passed = capability >= minimum and props.total_memory >= recipe["minimum_vram_bytes"] and torch.cuda.is_bf16_supported()
    if not passed: raise RuntimeError(f"GPU does not meet recipe floor: observed_vram={props.total_memory}, required_vram={recipe['minimum_vram_bytes']}, capability={capability}, bf16={torch.cuda.is_bf16_supported()}")
    smi = subprocess.run(["nvidia-smi","--query-gpu=name,uuid,driver_version,memory.total","--format=csv,noheader,nounits"],check=True,capture_output=True,text=True,timeout=10).stdout.strip()
    return {"name":props.name,"compute_capability":capability,"total_memory_bytes":props.total_memory,"required_memory_bytes":recipe["minimum_vram_bytes"],"bfloat16_supported":torch.cuda.is_bf16_supported(),"torch_cuda":torch.version.cuda,"cudnn":torch.backends.cudnn.version(),"nvidia_smi_csv":smi,"passed":passed}

def kernel_identity() -> dict[str,Any]:
    from transformers.models.qwen3_5 import modeling_qwen3_5
    symbols = {"causal_conv1d_fn":modeling_qwen3_5.causal_conv1d_fn is not None,"causal_conv1d_update":modeling_qwen3_5.causal_conv1d_update is not None,"chunk_gated_delta_rule":modeling_qwen3_5.chunk_gated_delta_rule is not None,"fused_recurrent_gated_delta_rule":modeling_qwen3_5.fused_recurrent_gated_delta_rule is not None,"fast_path":bool(modeling_qwen3_5.is_fast_path_available)}
    if not all(symbols.values()): raise RuntimeError(f"Qwen3.5 CUDA fast path is incomplete: {symbols}")
    return {"symbols":symbols,"passed":True}

def swift_identity(model_dir: Path) -> dict[str,Any]:
    from swift.model import get_model_info_meta
    info, meta = get_model_info_meta(str(model_dir)); model_type = getattr(info,"model_type",None); template = getattr(meta,"template",None); passed = model_type == "qwen3_5" and template == "qwen3_5"
    if not passed: raise RuntimeError(f"ms-swift did not resolve pinned checkpoint as qwen3_5: {model_type=}, {template=}")
    return {"model_type":model_type,"template":template,"passed":passed}

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
    encoded = tokenizer.apply_chat_template(messages,tokenize=True,add_generation_prompt=False,return_dict=True,return_tensors="pt",return_assistant_tokens_mask=True,truncation=True,max_length=max_length)
    mask = encoded.pop("assistant_masks",encoded.pop("assistant_tokens_mask",None))
    if mask is None: raise RuntimeError("upstream tokenizer did not produce assistant response masks")
    labels = encoded["input_ids"].clone(); labels[mask.to(dtype=labels.dtype) == 0] = -100
    if not (labels != -100).any(): raise RuntimeError("assistant response mask selected zero tokens")
    encoded["labels"] = labels
    return {key:value.to(device) for key,value in encoded.items()}

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
    if not torch.isfinite(output.loss): raise RuntimeError("non-finite loss in 4,096-token synthetic envelope probe")
    output.loss.backward(); model.zero_grad(set_to_none=True)
    return {"kind":"synthetic-active-token-shape-probe","sequence_length":length,"active_tokens":length,"micro_batch_size":1,"optimizer_step":False,"quality_training_record":False,"loss_finite":True,"passed":True}

def run_training_smoke(config: dict[str,Any], recipe_id: str, model_dir: Path, records_path: Path, adapter_dir: Path) -> dict[str,Any]:
    import torch
    from peft import LoraConfig, PeftModel, get_peft_model, prepare_model_for_kbit_training
    from transformers import AutoModelForImageTextToText, AutoTokenizer
    recipe = config["recipes"][recipe_id]; tokenizer = AutoTokenizer.from_pretrained(model_dir,local_files_only=True); model = load_model(model_dir,recipe_id)
    if hasattr(model,"visual"):
        for parameter in model.visual.parameters(): parameter.requires_grad = False
    quantized = [name for name,value in model.named_parameters() if value.__class__.__name__ == "Params4bit"]
    if recipe_id == FALLBACK_RECIPE:
        import bitsandbytes as bnb
        if not quantized: raise RuntimeError("bitsandbytes NF4 parameters were not observed")
        linear_type = bnb.nn.Linear4bit; model = prepare_model_for_kbit_training(model,use_gradient_checkpointing=True)
    else:
        if quantized: raise RuntimeError("BF16 primary unexpectedly contains quantized parameters")
        linear_type = torch.nn.Linear; model.gradient_checkpointing_enable(); model.enable_input_require_grads()
    model.config.use_cache = False
    targets = [name for name,module in model.named_modules() if isinstance(module,linear_type) and name.startswith("model.language_model.") and not name.endswith("lm_head")]
    if not targets: raise RuntimeError("no eligible language-model linear modules found")
    model = get_peft_model(model,LoraConfig(r=recipe["rank"],lora_alpha=recipe["alpha"],lora_dropout=recipe["dropout"],target_modules=targets,bias="none",task_type="CAUSAL_LM"))
    trainable = {name for name,parameter in model.named_parameters() if parameter.requires_grad}
    if not trainable or any("visual" in name or "lm_head" in name for name in trainable): raise RuntimeError("adapter targeting escaped the language model or produced no trainable parameters")
    records = select_records(records_path,tokenizer,recipe["record_count"],recipe["sequence_length"]); optimizer = torch.optim.AdamW((value for value in model.parameters() if value.requires_grad),lr=recipe["learning_rate"])
    torch.cuda.reset_peak_memory_stats(0); envelope = sequence_envelope_probe(model,tokenizer,recipe["sequence_length"])
    losses, gradients, active_tokens, response_tokens = [], set(), 0, 0
    torch.cuda.synchronize(); training_started = time.monotonic(); model.train()
    for item in records:
        batch = response_only_batch(tokenizer,item["row"]["messages"],recipe["sequence_length"],"cuda:0"); optimizer.zero_grad(set_to_none=True); output = model(**batch)
        if not torch.isfinite(output.loss): raise RuntimeError(f"non-finite loss for {item['row']['id']}")
        output.loss.backward(); gradients.update(name for name,parameter in model.named_parameters() if parameter.requires_grad and parameter.grad is not None and torch.count_nonzero(parameter.grad).item() > 0); optimizer.step()
        active_tokens += int(batch["attention_mask"].sum().item()); response_tokens += int((batch["labels"] != -100).sum().item()); losses.append(float(output.loss.detach().cpu()))
    torch.cuda.synchronize(); training_seconds = time.monotonic()-training_started; missing = sorted(trainable-gradients)
    if missing: raise RuntimeError(f"{len(missing)} trainable adapter parameters never received non-zero gradients")
    memory = {"peak_allocated_bytes":torch.cuda.max_memory_allocated(0),"peak_reserved_bytes":torch.cuda.max_memory_reserved(0)}
    adapter_dir.mkdir(parents=True,exist_ok=True); model.save_pretrained(adapter_dir,safe_serialization=True); tokenizer.save_pretrained(adapter_dir); hashes = {path.name:file_sha256(path) for path in sorted(adapter_dir.iterdir()) if path.is_file()}
    del optimizer, model; gc.collect(); torch.cuda.empty_cache()
    base = AutoModelForImageTextToText.from_pretrained(model_dir,local_files_only=True,dtype=torch.bfloat16,device_map={"":0}); reloaded = PeftModel.from_pretrained(base,adapter_dir,is_trainable=False); merged = reloaded.merge_and_unload(safe_merge=True); merged.eval(); probe = tokenizer("def add(a, b):",return_tensors="pt").to("cuda:0")
    with torch.inference_mode(): merge_finite = bool(torch.isfinite(merged(**probe).logits).all().item())
    if not merge_finite: raise RuntimeError("merged checkpoint produced non-finite logits")
    return {"recipe_id":recipe_id,"records":[{"id":item["row"]["id"],"tokens":item["tokens"],"rendered_prompt_sha256":hashlib.sha256(item["rendered"].encode()).hexdigest()} for item in records],"response_only":True,"optimizer_steps":len(records),"losses":losses,"sequence_envelope":envelope,"gradient_checkpointing":True,"quantized_parameter_count":len(quantized),"target_module_count":len(targets),"target_modules":targets,"trainable_parameter_names":sorted(trainable),"gradient_parameter_names":sorted(gradients),"training_seconds":training_seconds,"active_tokens":active_tokens,"response_tokens":response_tokens,"active_tokens_per_second":active_tokens/training_seconds,"response_tokens_per_second":response_tokens/training_seconds,"cuda_memory":memory,"adapter_file_sha256":hashes,"adapter_reloaded":True,"merge_logits_finite":merge_finite,"passed":True}

def inference_smoke(model_dir: Path, recipe_id: str) -> dict[str,Any]:
    import torch
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_dir,local_files_only=True); model = load_model(model_dir,recipe_id); model.eval(); messages = [{"role":"user","content":"Return only a Python function add(a, b) that returns the sum."}]; rendered = tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False); inputs = tokenizer(rendered,return_tensors="pt").to("cuda:0")
    with torch.inference_mode(): generated = model.generate(**inputs,do_sample=False,max_new_tokens=32,pad_token_id=tokenizer.eos_token_id)
    new_ids = generated[0,inputs.input_ids.shape[1]:]; raw = tokenizer.decode(new_ids,skip_special_tokens=False); clean = tokenizer.decode(new_ids,skip_special_tokens=True); passed = bool(clean.strip()) and rendered.endswith("<think>\n\n</think>\n\n")
    if not passed: raise RuntimeError("text-only non-thinking inference contract failed")
    del model; gc.collect(); torch.cuda.empty_cache()
    return {"messages":messages,"rendered_prompt":rendered,"rendered_prompt_sha256":hashlib.sha256(rendered.encode()).hexdigest(),"raw_output":raw,"extracted_output":clean,"input_tokens":int(inputs.input_ids.shape[1]),"output_tokens":int(new_ids.shape[0]),"passed":passed}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); root = Path(__file__).resolve().parents[2]
    parser.add_argument("--config",type=Path,default=root/"configs/cuda/qwen3_5_2b_gate0.json"); parser.add_argument("--recipe",choices=[PRIMARY_RECIPE,FALLBACK_RECIPE],default=PRIMARY_RECIPE); parser.add_argument("--model-dir",type=Path,required=True); parser.add_argument("--records",type=Path,default=root/"data/seed/ganesh_v01/train.jsonl"); parser.add_argument("--adapter-dir",type=Path,default=root/"outputs/cuda/gate0-adapter"); parser.add_argument("--output",type=Path,default=root/"measurement/cuda/qualification.json"); args = parser.parse_args()
    os.environ.setdefault("TOKENIZERS_PARALLELISM","false"); os.environ.setdefault("HF_HUB_OFFLINE","1"); os.environ.setdefault("TRANSFORMERS_OFFLINE","1"); started = time.monotonic(); evidence: dict[str,Any] = {"schema_version":"ganesh-mini-cuda-qualification/v2","status":"failed","recipe_id":args.recipe,"recorded_at":datetime.now(timezone.utc).isoformat(),"host":{"platform":platform.platform(),"machine":platform.machine(),"python":platform.python_version()}}
    try:
        config = load_and_validate_config(args.config,root); recipe = config["recipes"][args.recipe]
        evidence.update({"model_id":config["model"]["model_id"],"revision":config["model"]["revision"],"config_sha256":file_sha256(args.config),"model_inventory":{path.name:file_sha256(path) for path in sorted(args.model_dir.iterdir()) if path.is_file()},"packages":package_identity(config["packages"]),"gpu":gpu_identity(config,recipe),"kernels":kernel_identity(),"ms_swift":swift_identity(args.model_dir),"inference":inference_smoke(args.model_dir,args.recipe),"training":run_training_smoke(config,args.recipe,args.model_dir,args.records,args.adapter_dir),"status":"passed"})
    except Exception as exc: evidence.update({"error_type":type(exc).__name__,"error":str(exc)})
    evidence["wall_seconds"] = time.monotonic()-started; evidence["peak_rss_bytes"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024; write_evidence(evidence,args.output)
    return 0 if evidence["status"] == "passed" else 2

if __name__ == "__main__": raise SystemExit(main())
