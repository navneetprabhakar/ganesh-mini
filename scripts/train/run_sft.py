#!/usr/bin/env python3
"""Deterministic, resumable response-only LoRA SFT execution engine."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
import os
import random
import re
import resource
import statistics
import time
from decimal import Decimal
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.train.gradient_conflict import (
    assign_gradients,
    collect_lane_gradients,
    deterministic_pcgrad,
    measure_gradient_conflicts,
    rotated_lane_order,
    split_optimizer_groups,
)
from scripts.train.qwen_runtime import configure_cuda_allocator, configure_fused_training_loss, configure_qwen_training_structure, unload_and_reload_saved_adapter


EXPANSION_CARD_SCHEMAS = {
    "ganesh-mini-expansion-pilot-config/v1": "ganesh-mini-expansion-pilot-card/v1",
    "ganesh-mini-expansion-pilot-config/v2": "ganesh-mini-expansion-pilot-card/v2",
    "ganesh-mini-expansion-pilot-config/v3": "ganesh-mini-expansion-pilot-card/v3",
    "ganesh-mini-expansion-pilot-config/v4": "ganesh-mini-expansion-pilot-card/v4",
}


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def file_sha256(path: Path) -> str:
    digest=hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda:handle.read(8*1024*1024),b""): digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: dict[str,Any]) -> None:
    path.parent.mkdir(parents=True,exist_ok=True); temporary=path.with_name(f".{path.name}.{os.getpid()}.tmp"); temporary.write_text(json.dumps(value,indent=2,sort_keys=True)+"\n"); os.replace(temporary,path)


def append_jsonl(path: Path, value: dict[str,Any]) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("a",encoding="utf-8") as handle: handle.write(json.dumps(value,sort_keys=True,separators=(",", ":"))+"\n"); handle.flush(); os.fsync(handle.fileno())


def load_sealed(path: Path, field: str) -> dict[str,Any]:
    value=json.loads(path.read_text()); claimed=value.pop(field,None)
    if claimed!=canonical_sha256(value): raise ValueError(f"invalid {field}: {path}")
    value[field]=claimed; return value


def validate_gradient_conflict_audit(audit: dict[str,Any], identities: dict[str,str]) -> None:
    claimed=audit.get("audit_sha256")
    payload={key:value for key,value in audit.items() if key!="audit_sha256"}
    if (
        audit.get("schema_version")!="ganesh-mini-gradient-conflict-audit/v1"
        or audit.get("status")!="complete"
        or audit.get("identities")!=identities
        or claimed!=canonical_sha256(payload)
        or not isinstance(audit.get("decision",{}).get("stage_2_allowed"),bool)
    ):
        raise RuntimeError("invalid or mismatched gradient-conflict audit")


def seed_everything(seed: int) -> None:
    import torch
    random.seed(seed); torch.manual_seed(seed); torch.cuda.manual_seed_all(seed); torch.use_deterministic_algorithms(True,warn_only=True)


def initialize_cuda_measurement(torch_module: Any) -> Any:
    """Select and initialize the sole CUDA device before resetting its counters."""
    device=torch_module.device("cuda:0")
    torch_module.cuda.set_device(device)
    torch_module.cuda.init()
    torch_module.cuda.reset_peak_memory_stats()
    return device


def load_rows(path: Path) -> list[dict[str,Any]]:
    rows=[json.loads(line) for line in path.read_text().splitlines() if line]
    if not rows or any(len(row["input_ids"])!=len(row["labels"]) or row["labels"][:row["prompt_token_count"]]!=[-100]*row["prompt_token_count"] for row in rows): raise ValueError("invalid prepared response-only data")
    return rows


def collate(row: dict[str,Any], device: str) -> dict[str,Any]:
    import torch
    return {key:torch.tensor([row[key]],dtype=torch.long,device=device) for key in ("input_ids","attention_mask","labels")}


def planned_end(rows: list[dict[str,Any]], maximum_seen_tokens: int, accumulation: int) -> int:
    seen=0; end=0
    for end,row in enumerate(rows,1):
        seen+=sum(row["attention_mask"])
        if seen>=maximum_seen_tokens: break
    if end < len(rows) and end % accumulation:
        end=min(len(rows),end+(accumulation-end%accumulation))
    return end


def bounded_training_wall(maximum_wall_seconds: float, cost_wall_seconds: float, finalization_reserve_seconds: float = 600) -> float:
    if maximum_wall_seconds <= finalization_reserve_seconds+60 or cost_wall_seconds <= finalization_reserve_seconds+60:
        raise RuntimeError("wall or cost envelope leaves insufficient training and finalization time")
    return min(maximum_wall_seconds,cost_wall_seconds)-finalization_reserve_seconds


def five_family_validation(lane_losses: dict[str,list[float]]) -> dict[str,float]:
    required={"go","java","javascript","typescript","python","rust"}
    if set(lane_losses)!=required or any(not values for values in lane_losses.values()):
        raise RuntimeError("validation data does not cover every frozen lane")
    result={lane:sum(values)/len(values) for lane,values in lane_losses.items()}
    javascript_family=(result["javascript"]+result["typescript"])/2
    result["javascript_typescript_family_mean"]=javascript_family
    result["five_family_macro_mean"]=(result["go"]+result["java"]+javascript_family+result["python"]+result["rust"])/5
    return result


def summarize_validation(lane_rows: dict[str,list[dict[str,float]]]) -> dict[str,Any]:
    """Report comparable record-mean and supervised-token-mean diagnostics."""
    record_means=five_family_validation({lane:[row["loss"] for row in rows] for lane,rows in lane_rows.items()})
    token_means={lane:sum(row["loss"]*row["response_tokens"] for row in rows)/sum(row["response_tokens"] for row in rows) for lane,rows in lane_rows.items()}
    token_summary=five_family_validation({lane:[value] for lane,value in token_means.items()})
    return {"record_mean":record_means,"supervised_token_mean":token_summary,"records_by_lane":{lane:len(rows) for lane,rows in lane_rows.items()},"response_tokens_by_lane":{lane:int(sum(row["response_tokens"] for row in rows)) for lane,rows in lane_rows.items()}}


def select_lora_targets(named_modules: Any, linear_type: type, recipe: dict[str,Any]) -> list[str]:
    """Select exact, layer-bounded Qwen attention projections for LoRA."""
    policy=recipe.get("target_policy",{"scope":"all-language-model-linears"})
    if policy["scope"]=="all-language-model-linears":
        return [name for name,module in named_modules if isinstance(module,linear_type) and name.startswith("model.language_model.") and not name.endswith("lm_head")]
    supported={"last-n-attention-projections","all-attention-plus-last-n-mlp"}
    if policy["scope"] not in supported:
        raise RuntimeError("unsupported LoRA target policy")
    layer_count=policy.get("layer_count")
    layer_total=policy.get("model_layer_count")
    full=set(policy.get("full_attention_projections",[])); linear=set(policy.get("linear_attention_projections",[]))
    if not isinstance(layer_count,int) or not isinstance(layer_total,int) or not 0<layer_count<=layer_total or not full or not linear:
        raise RuntimeError("invalid layer-bounded LoRA target policy")
    first_layer=layer_total-layer_count; selected=[]
    mlp=set(policy.get("mlp_projections",[]))
    if policy["scope"]=="last-n-attention-projections" and mlp:
        raise RuntimeError("attention-only LoRA target policy cannot declare MLP projections")
    if policy["scope"]=="all-attention-plus-last-n-mlp" and not mlp:
        raise RuntimeError("capacity-expanded LoRA target policy requires MLP projections")
    pattern=re.compile(r"^model\.language_model\.layers\.(\d+)\.(self_attn|linear_attn|mlp)\.([^.]+)$")
    for name,module in named_modules:
        match=pattern.fullmatch(name)
        if not match or not isinstance(module,linear_type):
            continue
        layer=int(match.group(1)); block=match.group(2); projection=match.group(3)
        if block=="mlp":
            if policy["scope"]=="all-attention-plus-last-n-mlp" and layer>=first_layer and projection in mlp: selected.append(name)
            continue
        if policy["scope"]=="last-n-attention-projections" and layer<first_layer:
            continue
        allowed=full if block=="self_attn" else linear
        if projection in allowed: selected.append(name)
    attention_layers={int(pattern.fullmatch(name).group(1)) for name in selected if ".self_attn." in name or ".linear_attn." in name}
    expected_attention_layers=set(range(first_layer,layer_total)) if policy["scope"]=="last-n-attention-projections" else set(range(layer_total))
    if attention_layers != expected_attention_layers:
        raise RuntimeError("LoRA target policy did not cover every declared attention layer")
    if policy["scope"]=="all-attention-plus-last-n-mlp":
        mlp_layers={int(pattern.fullmatch(name).group(1)) for name in selected if ".mlp." in name}
        if mlp_layers != set(range(first_layer,layer_total)):
            raise RuntimeError("LoRA target policy did not cover every declared final-layer MLP")
    return selected


class RollingLossGuard:
    """Robust optimizer-group anomaly detector; raw record losses never trip it."""

    def __init__(self, contract: dict[str,Any], history: list[float] | None = None, streak: int = 0) -> None:
        self.contract=contract; self.history=list(history or []); self.streak=streak

    def observe(self, value: float) -> dict[str,Any]:
        window=self.history[-self.contract["rolling_window_optimizer_steps"]:]
        ready=len(self.history)>=self.contract["warmup_optimizer_steps"] and len(window)>=self.contract["minimum_history_optimizer_steps"]
        median=statistics.median(window) if window else None
        mad=statistics.median(abs(item-median) for item in window) if window else None
        scale=1.4826*max(mad or 0.0,self.contract["mad_floor"])
        ratio=value/max(median or 0.0,self.contract["mad_floor"]) if median is not None else None
        robust_z=(value-median)/scale if median is not None else None
        spike=bool(ready and ratio>=self.contract["minimum_median_ratio"] and robust_z>=self.contract["robust_z_threshold"])
        self.streak=self.streak+1 if spike else 0
        triggered=self.streak>=self.contract["consecutive_optimizer_groups"]
        # Keep anomalous groups out of the reference window; otherwise the
        # first spike raises the median enough to hide a genuinely consecutive
        # run. A normal group resets the streak and becomes new baseline data.
        if not spike: self.history.append(value)
        return {"ready":ready,"median":median,"mad":mad,"median_ratio":ratio,"robust_z":robust_z,"spike":spike,"streak":self.streak,"triggered":triggered}


def save_checkpoint(output: Path, model: Any, optimizer: Any, scheduler: Any, state: dict[str,Any], identities: dict[str,str]) -> dict[str,Any]:
    import torch
    checkpoint=output/"checkpoints"/f"tokens-{state['seen_tokens']:012d}"; checkpoint.mkdir(parents=True,exist_ok=False); model.save_pretrained(checkpoint/"adapter",safe_serialization=True); torch.save({"optimizer":optimizer.state_dict(),"scheduler":scheduler.state_dict(),"torch_rng":torch.get_rng_state(),"cuda_rng":torch.cuda.get_rng_state_all(),"state":state},checkpoint/"trainer-state.pt")
    files=[{"path":str(path.relative_to(checkpoint)),"size":path.stat().st_size,"sha256":file_sha256(path)} for path in sorted(checkpoint.rglob("*")) if path.is_file()]; manifest={"schema_version":"ganesh-mini-checkpoint/v1","status":"complete","identities":identities,"state":state,"files":files}; manifest["manifest_sha256"]=canonical_sha256(manifest); atomic_json(checkpoint/"manifest.json",manifest); append_jsonl(output/"checkpoints.jsonl",{"path":str(checkpoint),"manifest_sha256":manifest["manifest_sha256"],"seen_tokens":state["seen_tokens"]}); return manifest


def run(args: argparse.Namespace) -> dict[str,Any]:
    card=load_sealed(args.card,"card_sha256")
    if card.get("status")!="ready" or card.get("failed_checks"): raise RuntimeError("training execution card is not ready")
    config=json.loads(args.config.read_text()); config_sha=file_sha256(args.config)
    expansion=config.get("schema_version") in EXPANSION_CARD_SCHEMAS
    if config.get("schema_version") not in {"ganesh-mini-train-config/v4","ganesh-mini-train-config/v5",*EXPANSION_CARD_SCHEMAS}: raise RuntimeError("unsupported training config schema")
    expected_expansion_card=EXPANSION_CARD_SCHEMAS.get(config.get("schema_version"))
    if expansion and card.get("schema_version")!=expected_expansion_card: raise RuntimeError("expansion card/config contract mismatch")
    if card["inputs"]["config_sha256"]!=config_sha: raise RuntimeError("card/config identity mismatch")
    prepared_manifest=load_sealed(args.prepared_manifest,"manifest_sha256")
    if card["inputs"]["prepared_manifest_sha256"]!=prepared_manifest["manifest_sha256"]: raise RuntimeError("card/prepared manifest mismatch")
    rows=load_rows(args.prepared_data); validation_rows=load_rows(args.validation_data); recipe=card["selected_recipe"]; lr=args.learning_rate
    allocator=configure_cuda_allocator(recipe.get("cuda_allocator_config"))
    import torch
    from peft import LoraConfig,PeftModel,get_peft_model,prepare_model_for_kbit_training
    from transformers import AutoModelForImageTextToText,BitsAndBytesConfig,get_cosine_schedule_with_warmup
    if not torch.cuda.is_available() or torch.cuda.device_count()!=1: raise RuntimeError("SFT requires exactly one CUDA GPU")
    permitted_lrs=[recipe["learning_rate"]] if expansion else recipe["learning_rate_candidates"]
    if lr not in permitted_lrs: raise RuntimeError("learning rate escaped predeclared candidates")
    if expansion and (args.phase!="expansion-pilot" or args.maximum_seen_tokens!=config["control"]["maximum_seen_tokens"]): raise RuntimeError("expansion pilot phase or token budget changed")
    if args.phase=="lr-candidate" and args.maximum_seen_tokens!=recipe["lr_selection_budget_seen_tokens_per_candidate"]: raise RuntimeError("LR candidate budget changed")
    if args.phase=="main":
        selection=load_sealed(args.lr_selection_evidence,"evidence_sha256") if args.lr_selection_evidence else None
        if not selection or selection.get("selected_learning_rate")!=lr or selection.get("rule")!=recipe["lr_selection_rule"]: raise RuntimeError("main SFT requires sealed LR selection evidence")
        if args.maximum_seen_tokens!=config["control"]["maximum_seen_tokens"]: raise RuntimeError("main SFT token budget changed")
    hourly=Decimal(str(args.hourly_cost_usd)); prior=Decimal(str(args.prior_cost_usd)); ceiling=Decimal(str(args.cost_ceiling_usd))
    if expansion:
        provider=card.get("provider_execution") or {}
        cost_ok=(hourly,prior,ceiling)==(Decimal(str(provider.get("hourly_cost_usd",0))),Decimal(str(provider.get("prior_cost_usd",-1))),Decimal(str(provider.get("cost_ceiling_usd",0))))
    else:
        cost_ok=ceiling<=Decimal(str(config["control"]["maximum_cost_usd"]))
    if hourly<=0 or prior<0 or ceiling<=prior or not cost_ok: raise RuntimeError("invalid or escaped cost envelope")
    cost_wall_seconds=float((ceiling-prior)/hourly*Decimal(3600))
    finalization_reserve_seconds=float(config["control"].get("finalization_reserve_seconds",600))
    wall_limit=bounded_training_wall(float(config["control"]["maximum_wall_seconds"]),cost_wall_seconds,finalization_reserve_seconds)
    prepared_train_sha=prepared_manifest.get("prepared_train_sha256") or prepared_manifest.get("prepared_train",{}).get("sha256")
    prepared_validation_sha=prepared_manifest.get("prepared_validation_sha256") or prepared_manifest.get("prepared_validation",{}).get("sha256")
    if file_sha256(args.prepared_data)!=prepared_train_sha or file_sha256(args.validation_data)!=prepared_validation_sha: raise RuntimeError("prepared data identity mismatch")
    identities={"card_sha256":card["card_sha256"],"config_sha256":config_sha,"prepared_manifest_sha256":prepared_manifest["manifest_sha256"],"prepared_data_sha256":file_sha256(args.prepared_data),"validation_data_sha256":file_sha256(args.validation_data),"model_revision":card["model"]["revision"],"recipe_sha256":canonical_sha256(recipe),"learning_rate":str(lr),"phase":args.phase}
    seed_everything(recipe["random_seed"]); kwargs={"local_files_only":True,"dtype":torch.bfloat16,"device_map":{"":0}}
    if recipe["base_loading"]=="qlora": kwargs["quantization_config"]=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type="nf4",bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.bfloat16)
    initialize_cuda_measurement(torch); model=AutoModelForImageTextToText.from_pretrained(args.model_dir,**kwargs)
    vision_offload_before=torch.cuda.memory_allocated(0); training_structure=configure_qwen_training_structure(model)
    gc.collect(); torch.cuda.empty_cache()
    vision_offload_after=torch.cuda.memory_allocated(0); training_structure.update({"cuda_allocated_before_vision_offload_bytes":vision_offload_before,"cuda_allocated_after_vision_offload_bytes":vision_offload_after,"cuda_allocated_released_by_vision_offload_bytes":vision_offload_before-vision_offload_after})
    if not training_structure["vision_moved_to_cpu"] or vision_offload_after>=vision_offload_before: raise RuntimeError("frozen vision offload did not release CUDA memory")
    if recipe["base_loading"]=="qlora": model=prepare_model_for_kbit_training(model,use_gradient_checkpointing=True); linear_type=__import__("bitsandbytes").nn.Linear4bit
    else: model.gradient_checkpointing_enable(); model.enable_input_require_grads(); linear_type=torch.nn.Linear
    if not model.is_gradient_checkpointing: raise RuntimeError("gradient checkpointing did not activate on the Qwen3.5 language model")
    fused_training_loss=configure_fused_training_loss(model,recipe["fused_linear_cross_entropy"]["version"])
    def validation_diagnostic(current_model: Any) -> dict[str,Any]:
        current_model.eval(); lane_rows={lane:[] for lane in ("go","java","javascript","typescript","python","rust")}
        with torch.inference_mode():
            for row in validation_rows:
                validation_result=current_model(**collate(row,"cuda:0"),skip_logits=True)
                if validation_result.logits is not None: raise RuntimeError("fused training loss materialized validation logits")
                lane_rows[row["lane"]].append({"loss":float(validation_result.loss.detach().cpu()),"response_tokens":float(sum(label!=-100 for label in row["labels"]))})
        return summarize_validation(lane_rows)
    base_validation=validation_diagnostic(model)
    targets=select_lora_targets(model.named_modules(),linear_type,recipe)
    if not targets: raise RuntimeError("no eligible Qwen3.5 language-model LoRA targets found")
    resume_manifest=None
    if args.resume_checkpoint:
        resume_manifest=load_sealed(args.resume_checkpoint/"manifest.json","manifest_sha256")
        if resume_manifest.get("identities")!=identities: raise RuntimeError("resume checkpoint identity mismatch")
        for item in resume_manifest.get("files",[]):
            path=args.resume_checkpoint/item["path"]
            if not path.is_file() or path.stat().st_size!=item["size"] or file_sha256(path)!=item["sha256"]: raise RuntimeError("resume checkpoint file mismatch")
        model=PeftModel.from_pretrained(model,args.resume_checkpoint/"adapter",is_trainable=True)
    else:
        model=get_peft_model(model,LoraConfig(r=recipe["lora_rank"],lora_alpha=recipe["lora_alpha"],lora_dropout=recipe["lora_dropout"],target_modules=targets,bias="none",task_type="CAUSAL_LM"))
    trainable_names=[name for name,parameter in model.named_parameters() if parameter.requires_grad]
    trainable_parameters=[parameter for parameter in model.parameters() if parameter.requires_grad]
    if not trainable_names or any("visual" in name or "lm_head" in name for name in trainable_names): raise RuntimeError("SFT adapter targeting escaped the Qwen3.5 language model")
    model.train()
    optimizer=torch.optim.AdamW(trainable_parameters,lr=lr,betas=tuple(recipe["optimizer_betas"]),eps=recipe["optimizer_epsilon"],weight_decay=recipe["weight_decay"])
    end_row=planned_end(rows,args.maximum_seen_tokens,recipe["gradient_accumulation_steps"]); total_micro_steps=end_row; total_optimizer_steps=math.ceil(total_micro_steps/recipe["gradient_accumulation_steps"]); scheduler=get_cosine_schedule_with_warmup(optimizer,math.ceil(total_optimizer_steps*recipe["warmup_ratio"]),total_optimizer_steps)
    state={"next_row":0,"seen_tokens":0,"response_tokens":0,"optimizer_steps":0,"micro_steps":0,"last_optimizer_micro_step":0,"losses":[],"anomaly_detector":{"history":[],"streak":0},"started_at":datetime.now(timezone.utc).isoformat()}; output=args.output; output.mkdir(parents=True,exist_ok=True)
    if resume_manifest:
        saved=torch.load(args.resume_checkpoint/"trainer-state.pt",map_location="cpu",weights_only=False); state=saved["state"]
        if state!=resume_manifest["state"]: raise RuntimeError("resume state disagrees with manifest")
        optimizer.load_state_dict(saved["optimizer"]); scheduler.load_state_dict(saved["scheduler"]); torch.set_rng_state(saved["torch_rng"]); torch.cuda.set_rng_state_all(saved["cuda_rng"])
    maximum=int(recipe.get("maximum_peak_vram_gb",23)*1024**3)
    anomaly_contract=recipe.get("loss_anomaly_detector")
    if config["schema_version"] in {"ganesh-mini-train-config/v5",*EXPANSION_CARD_SCHEMAS} and not anomaly_contract: raise RuntimeError("current recipe requires optimizer-group anomaly detection")
    detector=RollingLossGuard(anomaly_contract,state.get("anomaly_detector",{}).get("history",[]),state.get("anomaly_detector",{}).get("streak",0)) if anomaly_contract else None
    configured_checkpoint=config["control"].get("checkpoint_every_tokens") or min(config["control"]["checkpoint_tokens"])
    checkpoint_interval=min(configured_checkpoint,max(1,sum(sum(row["attention_mask"]) for row in rows)//6)); next_checkpoint=(state["seen_tokens"]//checkpoint_interval+1)*checkpoint_interval; started=time.monotonic(); optimizer.zero_grad(set_to_none=True); group_raw_losses=[]; group_weighted_loss=0.0; group_weight=0.0
    conflict_contract=recipe.get("gradient_conflict")
    audit_only_stop=False
    conflict_groups=None
    if conflict_contract:
        lane_weights=conflict_contract["stage_2"]["lane_weights"]
        conflict_groups=split_optimizer_groups(rows[:end_row],recipe["gradient_accumulation_steps"],lane_weights)
        audit=state.get("gradient_conflict_audit")
        if audit is None:
            stage_1=conflict_contract["stage_1"]
            measured=measure_gradient_conflicts(
                model,conflict_groups,stage_1["selected_optimizer_groups"],trainable_parameters,lane_weights,collate,torch,
                negative_cosine_threshold=stage_1["negative_cosine_threshold"],
                minimum_negative_groups=stage_1["minimum_groups_with_negative_pair"],
                minimum_javascript_typescript_groups=stage_1["minimum_javascript_or_typescript_groups"],
            )
            audit={"schema_version":"ganesh-mini-gradient-conflict-audit/v1","status":"complete","identities":identities,**measured}
            audit["audit_sha256"]=canonical_sha256(audit)
            validate_gradient_conflict_audit(audit,identities)
            atomic_json(output/"gradient-conflict-audit.json",audit)
            state["gradient_conflict_audit"]=audit
        else:
            validate_gradient_conflict_audit(audit,identities)
        audit_only_stop=not audit["decision"]["stage_2_allowed"]

    if conflict_contract and not audit_only_stop:
        assert conflict_groups is not None
        accumulation=recipe["gradient_accumulation_steps"]
        if state["next_row"]%accumulation or state["micro_steps"]%accumulation:
            raise RuntimeError("gradient-conflict resume is not on an optimizer-group boundary")
        for group_index in range(state["next_row"]//accumulation,len(conflict_groups)):
            if time.monotonic()-started>=wall_limit: break
            group=conflict_groups[group_index]
            lane_gradients,lane_losses=collect_lane_gradients(model,group,trainable_parameters,lane_weights,collate,torch)
            aggregate,projection=deterministic_pcgrad(
                lane_gradients,lane_weights,
                rotated_lane_order(list(lane_weights),conflict_contract["stage_2"]["projection_seed"],group_index),
            )
            assign_gradients(trainable_parameters,aggregate)
            group_raw_losses=[value for lane in lane_weights for value in (
                lane_losses[lane]["raw_loss_min"],lane_losses[lane]["raw_loss_max"]
            )]
            raw_record_count=sum(lane_losses[lane]["records"] for lane in lane_weights)
            raw_record_mean=sum(lane_losses[lane]["raw_loss_mean"]*lane_losses[lane]["records"] for lane in lane_weights)/raw_record_count
            group_weighted_loss=sum(lane_losses[lane]["raw_loss_mean"]*lane_weights[lane] for lane in lane_weights)
            gradient_norm=float(torch.nn.utils.clip_grad_norm_(trainable_parameters,recipe["max_gradient_norm"]))
            guard=detector.observe(group_weighted_loss) if detector else {"ready":False,"triggered":False}
            state.update({
                "next_row":min((group_index+1)*accumulation,end_row),
                "seen_tokens":state["seen_tokens"]+sum(sum(row["attention_mask"]) for row in group),
                "response_tokens":state["response_tokens"]+sum(sum(label!=-100 for label in row["labels"]) for row in group),
                "micro_steps":state["micro_steps"]+len(group),
            })
            state["losses"]=(state["losses"]+[lane_losses[lane]["raw_loss_mean"] for lane in lane_weights])[-100:]
            telemetry={"recorded_at":datetime.now(timezone.utc).isoformat(),"seen_tokens":state["seen_tokens"],"response_tokens":state["response_tokens"],"optimizer_steps":state["optimizer_steps"]+1,"weighted_group_loss":group_weighted_loss,"group_objective_weight":sum(lane_weights.values()),"raw_record_loss_min":min(group_raw_losses),"raw_record_loss_mean":raw_record_mean,"raw_record_loss_max":max(group_raw_losses),"gradient_norm_before_clip":gradient_norm,"loss_anomaly":guard,"learning_rate":scheduler.get_last_lr()[0],"peak_allocated_bytes":torch.cuda.max_memory_allocated(0),"peak_reserved_bytes":torch.cuda.max_memory_reserved(0),"gradient_conflict":{"optimizer_group":group_index,"lane_losses":lane_losses,**projection}}
            append_jsonl(output/"telemetry.jsonl",telemetry)
            if guard["triggered"]:
                optimizer.zero_grad(set_to_none=True); raise RuntimeError("robust optimizer-group loss anomaly")
            optimizer.step(); scheduler.step(); optimizer.zero_grad(set_to_none=True); state["optimizer_steps"]+=1; state["last_optimizer_micro_step"]=state["micro_steps"]
            if detector: state["anomaly_detector"]={"history":detector.history,"streak":detector.streak}
            current_peak=max(torch.cuda.max_memory_allocated(0),torch.cuda.max_memory_reserved(0))
            if current_peak>maximum: raise RuntimeError(f"peak VRAM {current_peak} exceeds {maximum}")
            if state["seen_tokens"]>=next_checkpoint: save_checkpoint(output,model,optimizer,scheduler,state,identities); next_checkpoint+=checkpoint_interval
    elif not conflict_contract:
        for index,row in enumerate(rows[state["next_row"]:end_row],state["next_row"]):
            if time.monotonic()-started>=wall_limit and state["last_optimizer_micro_step"]==state["micro_steps"]: break
            batch=collate(row,"cuda:0"); result=model(**batch,skip_logits=True)
            if result.logits is not None: raise RuntimeError("fused training loss materialized record logits")
            objective_weight=float(row.get("objective_weight",1/recipe["gradient_accumulation_steps"]))
            if not math.isfinite(objective_weight) or objective_weight<=0: raise RuntimeError("invalid training objective weight")
            loss=result.loss*objective_weight
            if not torch.isfinite(loss): raise RuntimeError("non-finite loss")
            loss.backward(); raw_loss=float(result.loss.detach().cpu()); group_raw_losses.append(raw_loss); group_weighted_loss+=raw_loss*objective_weight; group_weight+=objective_weight
            current_peak=max(torch.cuda.max_memory_allocated(0),torch.cuda.max_memory_reserved(0))
            if current_peak>maximum: raise RuntimeError(f"peak VRAM {current_peak} exceeds {maximum}")
            state.update({"next_row":index+1,"seen_tokens":state["seen_tokens"]+int(batch["attention_mask"].sum()),"response_tokens":state["response_tokens"]+int((batch["labels"]!=-100).sum()),"micro_steps":state["micro_steps"]+1}); state["losses"]=(state["losses"]+[raw_loss])[-100:]
            if state["micro_steps"]%recipe["gradient_accumulation_steps"]==0 or index==end_row-1:
                gradient_norm=float(torch.nn.utils.clip_grad_norm_(model.parameters(),recipe["max_gradient_norm"]))
                guard=detector.observe(group_weighted_loss) if detector else {"ready":False,"triggered":False}
                telemetry={"recorded_at":datetime.now(timezone.utc).isoformat(),"seen_tokens":state["seen_tokens"],"response_tokens":state["response_tokens"],"optimizer_steps":state["optimizer_steps"]+1,"weighted_group_loss":group_weighted_loss,"group_objective_weight":group_weight,"raw_record_loss_min":min(group_raw_losses),"raw_record_loss_mean":sum(group_raw_losses)/len(group_raw_losses),"raw_record_loss_max":max(group_raw_losses),"gradient_norm_before_clip":gradient_norm,"loss_anomaly":guard,"learning_rate":scheduler.get_last_lr()[0],"peak_allocated_bytes":torch.cuda.max_memory_allocated(0),"peak_reserved_bytes":torch.cuda.max_memory_reserved(0)}
                append_jsonl(output/"telemetry.jsonl",telemetry)
                if guard["triggered"]:
                    optimizer.zero_grad(set_to_none=True); raise RuntimeError("robust optimizer-group loss anomaly")
                optimizer.step(); scheduler.step(); optimizer.zero_grad(set_to_none=True); state["optimizer_steps"]+=1; state["last_optimizer_micro_step"]=state["micro_steps"]
                if detector: state["anomaly_detector"]={"history":detector.history,"streak":detector.streak}
                group_raw_losses=[]; group_weighted_loss=0.0; group_weight=0.0
            if state["seen_tokens"]>=next_checkpoint and state["last_optimizer_micro_step"]==state["micro_steps"]: save_checkpoint(output,model,optimizer,scheduler,state,identities); next_checkpoint+=checkpoint_interval
    completed_training=state["next_row"]==end_row and state["last_optimizer_micro_step"]==state["micro_steps"]
    if not completed_training and not audit_only_stop:
        terminal_checkpoint=output/"checkpoints"/f"tokens-{state['seen_tokens']:012d}"
        if not terminal_checkpoint.exists(): save_checkpoint(output,model,optimizer,scheduler,state,identities)
    validation=validation_diagnostic(model)
    probe=collate(validation_rows[0],"cuda:0")
    with torch.inference_mode(): original_logits=model(**probe).logits[:,-1,:].float().cpu()
    final=output/"adapter-final"; model.save_pretrained(final,safe_serialization=True); files={str(path.relative_to(final)):file_sha256(path) for path in sorted(final.rglob("*")) if path.is_file()}
    model.zero_grad(set_to_none=True); del optimizer,scheduler; gc.collect(); torch.cuda.empty_cache(); reloaded,reload_lifecycle=unload_and_reload_saved_adapter(model,final); reloaded.eval()
    with torch.inference_mode(): reloaded_logits=reloaded(**probe).logits[:,-1,:].float().cpu()
    reload_max_abs=float((original_logits-reloaded_logits).abs().max()); save_reload={"passed":reload_max_abs<=0.01,"probe_source_id":validation_rows[0].get("source_id"),"maximum_absolute_logit_difference":reload_max_abs,"tolerance":0.01}
    if not save_reload["passed"]: raise RuntimeError("saved/reloaded adapter logits do not reproduce")
    peak=max(torch.cuda.max_memory_allocated(0),torch.cuda.max_memory_reserved(0))
    if peak>maximum: raise RuntimeError(f"peak VRAM {peak} exceeds {maximum}")
    state["completed_at"]=datetime.now(timezone.utc).isoformat(); state["wall_seconds"]=time.monotonic()-started
    run_status="gradient-audit-stop" if audit_only_stop else "complete" if completed_training else "bounded-stop"
    evidence={"schema_version":"ganesh-mini-sft-run/v2" if config["schema_version"].endswith("v5") or expansion else "ganesh-mini-sft-run/v1","status":run_status,"identities":identities,"planned_end_row":end_row,"cuda_allocator":allocator,"training_structure":training_structure,"fused_training_loss":fused_training_loss,"lora_target_policy":recipe.get("target_policy",{"scope":"all-language-model-linears"}),"trainable_parameter_names":trainable_names,"base_validation_loss_diagnostic":base_validation,"validation_loss_diagnostic":validation,"save_reload":{**save_reload,"lifecycle":reload_lifecycle},"state":state,"cost":{"hourly_usd":str(hourly),"prior_usd":str(prior),"ceiling_usd":str(ceiling),"cost_bounded_wall_seconds":cost_wall_seconds,"training_wall_limit_seconds":wall_limit,"finalization_reserve_seconds":finalization_reserve_seconds,"projected_final_usd":str(prior+hourly*Decimal(str(state["wall_seconds"]))/Decimal(3600))},"cuda":{"name":torch.cuda.get_device_name(0),"peak_vram_bytes":peak,"maximum_peak_vram_bytes":maximum},"adapter_files":files,"peak_rss_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024}; evidence["evidence_sha256"]=canonical_sha256(evidence); atomic_json(output/"run-evidence.json",evidence); del reloaded; gc.collect(); torch.cuda.empty_cache(); return evidence


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--phase",choices=("lr-candidate","main","expansion-pilot"),required=True); parser.add_argument("--card",type=Path,required=True); parser.add_argument("--config",type=Path,default=Path("configs/train/seed_pilot.json")); parser.add_argument("--prepared-manifest",type=Path,default=Path("artifacts/train/seed-pilot/prepared-dataset-manifest.json")); parser.add_argument("--prepared-data",type=Path,default=Path("artifacts/train/seed-pilot/prepared-train.jsonl")); parser.add_argument("--validation-data",type=Path,default=Path("artifacts/train/seed-pilot/prepared-validation.jsonl")); parser.add_argument("--model-dir",type=Path,required=True); parser.add_argument("--output",type=Path,required=True); parser.add_argument("--learning-rate",type=float,required=True); parser.add_argument("--maximum-seen-tokens",type=int,required=True); parser.add_argument("--hourly-cost-usd",type=float,required=True); parser.add_argument("--prior-cost-usd",type=float,required=True); parser.add_argument("--cost-ceiling-usd",type=float,required=True); parser.add_argument("--lr-selection-evidence",type=Path); parser.add_argument("--resume-checkpoint",type=Path); args=parser.parse_args(); evidence=run(args); print(json.dumps({"status":evidence["status"],"seen_tokens":evidence["state"]["seen_tokens"],"evidence_sha256":evidence["evidence_sha256"]},sort_keys=True)); return 0 if evidence["status"]=="complete" else 2


if __name__=="__main__": raise SystemExit(main())
