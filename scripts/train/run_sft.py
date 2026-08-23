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
import resource
import time
from decimal import Decimal
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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


def seed_everything(seed: int) -> None:
    import torch
    random.seed(seed); torch.manual_seed(seed); torch.cuda.manual_seed_all(seed); torch.use_deterministic_algorithms(True,warn_only=True)


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


def save_checkpoint(output: Path, model: Any, optimizer: Any, scheduler: Any, state: dict[str,Any], identities: dict[str,str]) -> dict[str,Any]:
    import torch
    checkpoint=output/"checkpoints"/f"tokens-{state['seen_tokens']:012d}"; checkpoint.mkdir(parents=True,exist_ok=False); model.save_pretrained(checkpoint/"adapter",safe_serialization=True); torch.save({"optimizer":optimizer.state_dict(),"scheduler":scheduler.state_dict(),"torch_rng":torch.get_rng_state(),"cuda_rng":torch.cuda.get_rng_state_all(),"state":state},checkpoint/"trainer-state.pt")
    files=[{"path":str(path.relative_to(checkpoint)),"size":path.stat().st_size,"sha256":file_sha256(path)} for path in sorted(checkpoint.rglob("*")) if path.is_file()]; manifest={"schema_version":"ganesh-mini-checkpoint/v1","status":"complete","identities":identities,"state":state,"files":files}; manifest["manifest_sha256"]=canonical_sha256(manifest); atomic_json(checkpoint/"manifest.json",manifest); append_jsonl(output/"checkpoints.jsonl",{"path":str(checkpoint),"manifest_sha256":manifest["manifest_sha256"],"seen_tokens":state["seen_tokens"]}); return manifest


def run(args: argparse.Namespace) -> dict[str,Any]:
    import torch
    from peft import LoraConfig,PeftModel,get_peft_model,prepare_model_for_kbit_training
    from transformers import AutoModelForImageTextToText,BitsAndBytesConfig,get_cosine_schedule_with_warmup
    if not torch.cuda.is_available() or torch.cuda.device_count()!=1: raise RuntimeError("SFT requires exactly one CUDA GPU")
    card=load_sealed(args.card,"card_sha256")
    if card.get("status")!="ready" or card.get("failed_checks"): raise RuntimeError("training execution card is not ready")
    config=json.loads(args.config.read_text()); config_sha=file_sha256(args.config)
    if card["inputs"]["config_sha256"]!=config_sha: raise RuntimeError("card/config identity mismatch")
    prepared_manifest=load_sealed(args.prepared_manifest,"manifest_sha256")
    if card["inputs"]["prepared_manifest_sha256"]!=prepared_manifest["manifest_sha256"]: raise RuntimeError("card/prepared manifest mismatch")
    rows=load_rows(args.prepared_data); validation_rows=load_rows(args.validation_data); recipe=card["selected_recipe"]; lr=args.learning_rate
    if lr not in recipe["learning_rate_candidates"]: raise RuntimeError("learning rate escaped predeclared candidates")
    if args.phase=="lr-candidate" and args.maximum_seen_tokens!=recipe["lr_selection_budget_seen_tokens_per_candidate"]: raise RuntimeError("LR candidate budget changed")
    if args.phase=="main":
        selection=load_sealed(args.lr_selection_evidence,"evidence_sha256") if args.lr_selection_evidence else None
        if not selection or selection.get("selected_learning_rate")!=lr or selection.get("rule")!=recipe["lr_selection_rule"]: raise RuntimeError("main SFT requires sealed LR selection evidence")
        if args.maximum_seen_tokens!=config["control"]["maximum_seen_tokens"]: raise RuntimeError("main SFT token budget changed")
    hourly=Decimal(str(args.hourly_cost_usd)); prior=Decimal(str(args.prior_cost_usd)); ceiling=Decimal(str(args.cost_ceiling_usd))
    if hourly<=0 or prior<0 or ceiling<=prior or ceiling>Decimal(str(config["control"]["maximum_cost_usd"])): raise RuntimeError("invalid or escaped cost envelope")
    cost_wall_seconds=float((ceiling-prior)/hourly*Decimal(3600))
    if cost_wall_seconds<=120: raise RuntimeError("cost envelope leaves no safe training and checkpoint reserve")
    wall_limit=min(float(config["control"]["maximum_wall_seconds"]),cost_wall_seconds-60)
    if file_sha256(args.prepared_data)!=prepared_manifest["prepared_train_sha256"] or file_sha256(args.validation_data)!=prepared_manifest["prepared_validation_sha256"]: raise RuntimeError("prepared data identity mismatch")
    identities={"card_sha256":card["card_sha256"],"config_sha256":config_sha,"prepared_manifest_sha256":prepared_manifest["manifest_sha256"],"prepared_data_sha256":file_sha256(args.prepared_data),"validation_data_sha256":file_sha256(args.validation_data),"model_revision":card["model"]["revision"],"recipe_sha256":canonical_sha256(recipe),"learning_rate":str(lr),"phase":args.phase}
    seed_everything(recipe["random_seed"]); kwargs={"local_files_only":True,"dtype":torch.bfloat16,"device_map":{"":0}}
    if recipe["base_loading"]=="qlora": kwargs["quantization_config"]=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type="nf4",bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.bfloat16)
    torch.cuda.reset_peak_memory_stats(0); model=AutoModelForImageTextToText.from_pretrained(args.model_dir,**kwargs)
    if hasattr(model,"visual"):
        for parameter in model.visual.parameters(): parameter.requires_grad=False
    if recipe["base_loading"]=="qlora": model=prepare_model_for_kbit_training(model,use_gradient_checkpointing=True); linear_type=__import__("bitsandbytes").nn.Linear4bit
    else: model.gradient_checkpointing_enable(); model.enable_input_require_grads(); linear_type=torch.nn.Linear
    model.config.use_cache=False; targets=[name for name,module in model.named_modules() if isinstance(module,linear_type) and name.startswith("model.language_model.") and not name.endswith("lm_head")]
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
    model.train()
    optimizer=torch.optim.AdamW((parameter for parameter in model.parameters() if parameter.requires_grad),lr=lr,betas=tuple(recipe["optimizer_betas"]),eps=recipe["optimizer_epsilon"],weight_decay=recipe["weight_decay"])
    end_row=planned_end(rows,args.maximum_seen_tokens,recipe["gradient_accumulation_steps"]); total_micro_steps=end_row; total_optimizer_steps=math.ceil(total_micro_steps/recipe["gradient_accumulation_steps"]); scheduler=get_cosine_schedule_with_warmup(optimizer,math.ceil(total_optimizer_steps*recipe["warmup_ratio"]),total_optimizer_steps)
    state={"next_row":0,"seen_tokens":0,"response_tokens":0,"optimizer_steps":0,"micro_steps":0,"last_optimizer_micro_step":0,"losses":[],"started_at":datetime.now(timezone.utc).isoformat()}; output=args.output; output.mkdir(parents=True,exist_ok=True)
    if resume_manifest:
        saved=torch.load(args.resume_checkpoint/"trainer-state.pt",map_location="cpu",weights_only=False); state=saved["state"]
        if state!=resume_manifest["state"]: raise RuntimeError("resume state disagrees with manifest")
        optimizer.load_state_dict(saved["optimizer"]); scheduler.load_state_dict(saved["scheduler"]); torch.set_rng_state(saved["torch_rng"]); torch.cuda.set_rng_state_all(saved["cuda_rng"])
    checkpoint_interval=min(config["control"]["checkpoint_every_tokens"],max(1,sum(sum(row["attention_mask"]) for row in rows)//6)); next_checkpoint=(state["seen_tokens"]//checkpoint_interval+1)*checkpoint_interval; started=time.monotonic(); optimizer.zero_grad(set_to_none=True); spikes=0; last_loss=None
    for index,row in enumerate(rows[state["next_row"]:end_row],state["next_row"]):
        if time.monotonic()-started>=wall_limit and state["last_optimizer_micro_step"]==state["micro_steps"]: break
        batch=collate(row,"cuda:0"); result=model(**batch); loss=result.loss/recipe["gradient_accumulation_steps"]
        if not torch.isfinite(loss): raise RuntimeError("non-finite loss")
        loss.backward(); raw_loss=float(result.loss.detach().cpu()); spikes=spikes+1 if last_loss is not None and raw_loss>last_loss*3 else 0; last_loss=raw_loss
        if spikes>=3: raise RuntimeError("three consecutive loss spikes")
        state.update({"next_row":index+1,"seen_tokens":state["seen_tokens"]+int(batch["attention_mask"].sum()),"response_tokens":state["response_tokens"]+int((batch["labels"]!=-100).sum()),"micro_steps":state["micro_steps"]+1}); state["losses"]=(state["losses"]+[raw_loss])[-100:]
        if state["micro_steps"]%recipe["gradient_accumulation_steps"]==0 or index==len(rows)-1:
            torch.nn.utils.clip_grad_norm_(model.parameters(),recipe["max_gradient_norm"]); optimizer.step(); scheduler.step(); optimizer.zero_grad(set_to_none=True); state["optimizer_steps"]+=1; state["last_optimizer_micro_step"]=state["micro_steps"]; append_jsonl(output/"telemetry.jsonl",{"recorded_at":datetime.now(timezone.utc).isoformat(),"seen_tokens":state["seen_tokens"],"response_tokens":state["response_tokens"],"optimizer_steps":state["optimizer_steps"],"loss":raw_loss,"learning_rate":scheduler.get_last_lr()[0],"peak_allocated_bytes":torch.cuda.max_memory_allocated(0),"peak_reserved_bytes":torch.cuda.max_memory_reserved(0)})
        if state["seen_tokens"]>=next_checkpoint and state["last_optimizer_micro_step"]==state["micro_steps"]: save_checkpoint(output,model,optimizer,scheduler,state,identities); next_checkpoint+=checkpoint_interval
    maximum=int(recipe.get("maximum_peak_vram_gb",23)*1024**3)
    model.eval(); validation_loss_by_lane={lane:[] for lane in ("go","java","javascript","typescript","python","rust")}
    with torch.inference_mode():
        for row in validation_rows:
            validation_loss_by_lane[row["lane"]].append(float(model(**collate(row,"cuda:0")).loss.detach().cpu()))
    validation={lane:sum(values)/len(values) for lane,values in validation_loss_by_lane.items() if values}; validation["macro_mean"]=sum(validation.values())/len(validation)
    probe=collate(validation_rows[0],"cuda:0")
    with torch.inference_mode(): original_logits=model(**probe).logits[:,-1,:].float().cpu()
    final=output/"adapter-final"; model.save_pretrained(final,safe_serialization=True); files={str(path.relative_to(final)):file_sha256(path) for path in sorted(final.rglob("*")) if path.is_file()}
    del model; gc.collect(); torch.cuda.empty_cache(); reloaded_base=AutoModelForImageTextToText.from_pretrained(args.model_dir,**kwargs); reloaded=PeftModel.from_pretrained(reloaded_base,final,is_trainable=False).eval()
    with torch.inference_mode(): reloaded_logits=reloaded(**probe).logits[:,-1,:].float().cpu()
    reload_max_abs=float((original_logits-reloaded_logits).abs().max()); save_reload={"passed":reload_max_abs<=0.01,"probe_source_id":validation_rows[0].get("source_id"),"maximum_absolute_logit_difference":reload_max_abs,"tolerance":0.01}
    if not save_reload["passed"]: raise RuntimeError("saved/reloaded adapter logits do not reproduce")
    peak=max(torch.cuda.max_memory_allocated(0),torch.cuda.max_memory_reserved(0))
    if peak>maximum: raise RuntimeError(f"peak VRAM {peak} exceeds {maximum}")
    state["completed_at"]=datetime.now(timezone.utc).isoformat(); state["wall_seconds"]=time.monotonic()-started
    completed=state["next_row"]==end_row and state["last_optimizer_micro_step"]==state["micro_steps"]
    evidence={"schema_version":"ganesh-mini-sft-run/v1","status":"complete" if completed else "bounded-stop","identities":identities,"planned_end_row":end_row,"validation_loss_diagnostic":validation,"save_reload":save_reload,"state":state,"cost":{"hourly_usd":str(hourly),"prior_usd":str(prior),"ceiling_usd":str(ceiling),"cost_bounded_wall_seconds":cost_wall_seconds,"projected_final_usd":str(prior+hourly*Decimal(str(state["wall_seconds"]))/Decimal(3600))},"cuda":{"name":torch.cuda.get_device_name(0),"peak_vram_bytes":peak,"maximum_peak_vram_bytes":maximum},"adapter_files":files,"peak_rss_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024}; evidence["evidence_sha256"]=canonical_sha256(evidence); atomic_json(output/"run-evidence.json",evidence); del reloaded,reloaded_base,optimizer; gc.collect(); torch.cuda.empty_cache(); return evidence


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--phase",choices=("lr-candidate","main"),required=True); parser.add_argument("--card",type=Path,required=True); parser.add_argument("--config",type=Path,default=Path("configs/train/seed_pilot.json")); parser.add_argument("--prepared-manifest",type=Path,default=Path("artifacts/train/seed-pilot/prepared-dataset-manifest.json")); parser.add_argument("--prepared-data",type=Path,default=Path("artifacts/train/seed-pilot/prepared-train.jsonl")); parser.add_argument("--validation-data",type=Path,default=Path("artifacts/train/seed-pilot/prepared-validation.jsonl")); parser.add_argument("--model-dir",type=Path,required=True); parser.add_argument("--output",type=Path,required=True); parser.add_argument("--learning-rate",type=float,required=True); parser.add_argument("--maximum-seen-tokens",type=int,required=True); parser.add_argument("--hourly-cost-usd",type=float,required=True); parser.add_argument("--prior-cost-usd",type=float,required=True); parser.add_argument("--cost-ceiling-usd",type=float,required=True); parser.add_argument("--lr-selection-evidence",type=Path); parser.add_argument("--resume-checkpoint",type=Path); args=parser.parse_args(); evidence=run(args); print(json.dumps({"status":evidence["status"],"seen_tokens":evidence["state"]["seen_tokens"],"evidence_sha256":evidence["evidence_sha256"]},sort_keys=True)); return 0 if evidence["status"]=="complete" else 2


if __name__=="__main__": raise SystemExit(main())
