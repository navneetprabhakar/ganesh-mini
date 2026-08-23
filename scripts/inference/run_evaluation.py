#!/usr/bin/env python3
"""Batched model generation with concurrent network-off CPU verification."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import resource
import sys
import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

from scripts.eval.contracts import load_json, sha256_bytes, sha256_object, sha256_text, validate_result, validate_task
from scripts.eval.run_task import build_result
from scripts.inference.extract import EXTRACTOR_ID, extract_code
from scripts.inference.run_base import directory_artifact_sha256
from scripts.verify.sandbox import verify


ROOT = Path(__file__).resolve().parents[2]
CLASSIFICATIONS = {
    "private_development_baseline": "development",
    "private_candidate_development": "development",
    "public_diagnostic": "diagnostic",
    "private_decision_final": "decision",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def sealed(value: dict[str, Any], field: str) -> dict[str, Any]:
    result = dict(value); result[field] = sha256_object(result); return result


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def implementation_identity() -> dict[str, str]:
    return {name: file_sha256(ROOT / path) for name, path in {
        "runner_sha256": "scripts/inference/run_evaluation.py",
        "extractor_sha256": "scripts/inference/extract.py",
        "result_builder_sha256": "scripts/eval/run_task.py",
        "verifier_sha256": "scripts/verify/sandbox.py",
        "runtimes_config_sha256": "configs/eval/runtimes.json",
        "qwen_cuda_compatibility_sha256": "scripts/cuda/qualify.py",
    }.items()}


def peak_rss_bytes() -> int:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value if sys.platform == "darwin" else value * 1024)


class BatchBackend(Protocol):
    load_ms: int
    identity: dict[str, Any]
    eos_token_id: int

    def render(self, prompt: str) -> tuple[str, list[int]]: ...
    def generate_batch(self, input_ids: list[list[int]], max_new_tokens: int, use_cache: bool) -> list[tuple[list[int], str, int]]: ...


class TransformersBatchBackend:
    def __init__(self, model_dir: Path, auto_model_class: str, adapter_dir: Path | None = None) -> None:
        from scripts.cuda.qualify import install_fla_recurrent_compatibility, kernel_identity
        recurrent_compatibility=install_fla_recurrent_compatibility()
        import torch
        from transformers import AutoModelForCausalLM, AutoModelForImageTextToText, AutoTokenizer
        started = time.perf_counter(); self.torch = torch
        self.device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        self.dtype = torch.bfloat16 if self.device in {"cuda", "mps"} else torch.float32
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
        self.tokenizer.padding_side = "left"
        if self.tokenizer.pad_token_id is None: self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        model_class = AutoModelForImageTextToText if auto_model_class == "image-text-to-text" else AutoModelForCausalLM
        self.model = model_class.from_pretrained(model_dir, local_files_only=True, dtype=self.dtype).to(self.device)
        if adapter_dir is not None:
            from peft import PeftModel
            self.model=PeftModel.from_pretrained(self.model,adapter_dir,is_trainable=False)
        self.model.eval()
        kernels=kernel_identity() if self.device=="cuda" else None
        self.eos_token_id = int(self.tokenizer.eos_token_id); self.load_ms = round((time.perf_counter()-started)*1000)
        adapter_identity=str(adapter_dir.relative_to(ROOT)) if adapter_dir is not None and adapter_dir.is_relative_to(ROOT) else str(adapter_dir) if adapter_dir is not None else None
        self.identity = {"backend":"transformers-peft-batched" if adapter_dir else "transformers-batched","python":platform.python_version(),"torch":torch.__version__,"device":self.device,"dtype":str(next(self.model.parameters()).dtype),"adapter_dir":adapter_identity,"fla_recurrent_compatibility":recurrent_compatibility,"cuda_kernel_identity":kernels}

    def render(self, prompt: str) -> tuple[str, list[int]]:
        rendered = self.tokenizer.apply_chat_template([{"role":"user","content":prompt}],tokenize=False,add_generation_prompt=True,enable_thinking=False)
        return rendered,self.tokenizer(rendered,add_special_tokens=False).input_ids

    def generate_batch(self, input_ids: list[list[int]], max_new_tokens: int, use_cache: bool) -> list[tuple[list[int],str,int]]:
        torch = self.torch; width=max(map(len,input_ids)); pad=self.tokenizer.pad_token_id
        rows=[[pad]*(width-len(row))+row for row in input_ids]; masks=[[0]*(width-len(row))+[1]*len(row) for row in input_ids]
        ids=torch.tensor(rows,dtype=torch.long,device=self.device); attention=torch.tensor(masks,dtype=torch.long,device=self.device)
        started=time.perf_counter()
        with torch.inference_mode():
            generated=self.model.generate(input_ids=ids,attention_mask=attention,do_sample=False,max_new_tokens=max_new_tokens,use_cache=use_cache,pad_token_id=pad,eos_token_id=self.eos_token_id)
        elapsed=round((time.perf_counter()-started)*1000)
        return [(tokens:=generated[index,width:].detach().cpu().tolist(),self.tokenizer.decode(tokens,skip_special_tokens=False),elapsed) for index in range(len(rows))]


def validate_config(config: dict[str, Any]) -> None:
    if config.get("schema_version") != "ganesh-mini-production-inference/v1": raise ValueError("unsupported production inference schema")
    expected_surface = CLASSIFICATIONS.get(config.get("classification"))
    if expected_surface is None or config.get("allowed_surface") != expected_surface: raise ValueError("classification/surface mismatch")
    if expected_surface == "decision":
        opening = config.get("decision_opening")
        if not isinstance(opening, dict) or opening.get("status") != "opened-once" or not isinstance(opening.get("candidate_set_sha256"), str):
            raise ValueError("decision tasks require one sealed final opening")
    if config.get("serving") != {"modality":"text-only","enable_thinking":False,"context_length":8192,"add_generation_prompt":True}: raise ValueError("serving contract changed")
    generation=config.get("generation",{}); execution=config.get("execution",{})
    if generation.get("do_sample") is not False or not 1 <= generation.get("max_new_tokens",0) <= 4096: raise ValueError("generation must be bounded greedy decoding")
    if not 1 <= execution.get("batch_size",0) <= 64 or not 1 <= execution.get("verifier_workers",0) <= 64: raise ValueError("invalid execution concurrency")
    if not isinstance(execution.get("length_bucket_width"),int) or not 1 <= execution["length_bucket_width"] <= 8192: raise ValueError("invalid length bucket width")
    if execution.get("required_device") not in {"cuda","mps","cpu"}: raise ValueError("invalid required execution device")
    if config.get("extractor_id") != EXTRACTOR_ID: raise ValueError("unknown extractor")
    if config.get("classification")=="private_candidate_development" and not isinstance(config.get("adapter"),dict): raise ValueError("candidate development requires a sealed adapter binding")
    if config.get("classification")=="private_development_baseline" and config.get("adapter") is not None: raise ValueError("base baseline cannot load an adapter")


def validate_batch_outputs(outputs: list[tuple[list[int],str,int]], batch_size: int) -> None:
    if len(outputs)!=batch_size: raise RuntimeError(f"generation backend returned {len(outputs)} outputs for batch size {batch_size}")


def model_identity(config: dict[str, Any]) -> tuple[dict[str, Any], int]:
    contract=load_json(ROOT/config["model_contract"]); inventory=load_json(ROOT/config["model_inventory"])
    artifact=directory_artifact_sha256(ROOT/config["model_dir"],inventory)
    size=sum(int(row["size"]) for row in inventory["files"])
    identity={"model_id":contract["model_id"],"revision":contract["revision"],"artifact_sha256":artifact,"serving_contract_sha256":sha256_object(contract["serving_contract"]),"inventory_sha256":sha256_object(inventory)}
    adapter=config.get("adapter")
    if adapter is not None:
        run=load_sealed(ROOT/adapter["run_evidence"],"evidence_sha256")
        if run is None or run.get("status")!="complete": raise ValueError("candidate adapter run is incomplete")
        adapter_dir=ROOT/adapter["dir"]; observed={str(path.relative_to(adapter_dir)):file_sha256(path) for path in sorted(adapter_dir.rglob("*")) if path.is_file()}
        if observed!=run.get("adapter_files"): raise ValueError("candidate adapter files mismatch sealed run")
        identity={"model_id":adapter["served_model_id"],"revision":contract["revision"],"artifact_sha256":sha256_object({"base":artifact,"adapter":observed,"run_evidence_sha256":run["evidence_sha256"]}),"serving_contract_sha256":sha256_object(contract["serving_contract"]),"base_artifact_sha256":artifact,"training_run_evidence_sha256":run["evidence_sha256"]}; size+=sum(path.stat().st_size for path in adapter_dir.rglob("*") if path.is_file())
    return identity,size


def load_sealed(path: Path, field: str) -> dict[str, Any] | None:
    if not path.is_file(): return None
    value=load_json(path); claimed=value.pop(field,None)
    if claimed != sha256_object(value): raise ValueError(f"invalid evidence seal: {path}")
    value[field]=claimed; return value


def validate_resumed_task(evidence: dict[str,Any], task: dict[str,Any], config: dict[str,Any], config_sha: str, model: dict[str,Any], backend: BatchBackend, implementation: dict[str,str]) -> None:
    if evidence.get("classification")!=config["classification"] or evidence.get("run_id")!=config["run_id"]: raise ValueError("resumed task classification/run mismatch")
    bound=evidence.get("task",{})
    if bound.get("task_id")!=task["task_id"] or bound.get("task_sha256")!=sha256_object(task) or bound.get("config_sha256")!=config_sha: raise ValueError("resumed task identity mismatch")
    if evidence.get("model")!=model: raise ValueError("resumed task model mismatch")
    runtime=evidence.get("runtime",{}); observed_implementation=runtime.get("implementation")
    if observed_implementation!=implementation: raise ValueError("resumed task implementation mismatch")
    if {key:value for key,value in runtime.items() if key!="implementation"}!=backend.identity: raise ValueError("resumed task runtime mismatch")
    validate_result(evidence["verification"]["result"])


def validate_resumed_generation(generated: dict[str,Any], task: dict[str,Any], config_sha: str, model: dict[str,Any], backend: BatchBackend, implementation: dict[str,str]) -> None:
    if generated.get("task_id")!=task["task_id"] or generated.get("task_sha256")!=sha256_object(task) or generated.get("config_sha256")!=config_sha: raise ValueError("resumed generation identity mismatch")
    if generated.get("model")!=model: raise ValueError("resumed generation model mismatch")
    if generated.get("runtime")!=backend.identity: raise ValueError("resumed generation runtime mismatch")
    if generated.get("implementation")!=implementation: raise ValueError("resumed generation implementation mismatch")


def run_manifest(config: dict[str,Any], config_sha: str, model: dict[str,Any], backend: BatchBackend, tasks: list[tuple[Path,dict[str,Any]]], completed: dict[str,dict[str,Any]], final_dir: Path) -> dict[str,Any]:
    rows=[]
    for _,task in tasks:
        evidence=completed.get(task["task_id"]); path=final_dir/f"{task['task_id']}.json"
        rows.append({"task_id":task["task_id"],"status":"complete" if evidence else "pending","passed":evidence["verification"]["result"]["passed"] if evidence else None,"evidence_path":str(path.relative_to(ROOT)) if evidence else None,"evidence_sha256":evidence.get("evidence_sha256") if evidence else None})
    return sealed({"schema_version":"ganesh-mini-inference-run/v2","run_id":config["run_id"],"classification":config["classification"],"config_sha256":config_sha,"model":model,"runtime":{**backend.identity,"implementation":implementation_identity()},"task_accounting":{"expected":len(rows),"completed":len(completed),"passed":sum(row["passed"] is True for row in rows),"failed":sum(row["passed"] is False for row in rows),"pending":len(rows)-len(completed)},"tasks":rows,"updated_at":utc_now()},"run_sha256")


def generation_evidence(task_path: Path, task: dict[str,Any], config: dict[str,Any], config_sha: str, model: dict[str,Any], artifact_size: int, backend: BatchBackend, rendered: str, ids: list[int], output: tuple[list[int],str,int]) -> dict[str,Any]:
    output_ids,raw,generation_ms=output; completed=datetime.now(timezone.utc); started=completed.timestamp()-generation_ms/1000; stopped=bool(output_ids and output_ids[-1]==backend.eos_token_id)
    value={"schema_version":"ganesh-mini-generation-evidence/v1","task_id":task["task_id"],"task_path":str(task_path.relative_to(ROOT)),"task_sha256":sha256_object(task),"config_sha256":config_sha,"model":model,"runtime":backend.identity,"prompt":{"rendered":rendered,"rendered_sha256":sha256_text(rendered),"input_token_ids":ids,"input_token_ids_sha256":sha256_bytes(canonical_bytes(ids))},"generation":{"raw_output":raw,"raw_output_sha256":sha256_text(raw),"output_token_ids":output_ids,"output_token_ids_sha256":sha256_bytes(canonical_bytes(output_ids)),"stopped_at_eos":stopped,"generation_ms":generation_ms,"started_at":datetime.fromtimestamp(started,timezone.utc).isoformat(),"completed_at":completed.isoformat()},"parameters":{**config["serving"],**config["generation"],"input_tokens":len(ids),"output_tokens":len(output_ids),"stopped_at_eos":stopped,"artifact_size_bytes":artifact_size},"recorded_at":completed.isoformat(),"implementation":implementation_identity()}
    return sealed(value,"generation_sha256")


def verify_generated(generated: dict[str,Any], task: dict[str,Any], config: dict[str,Any], model: dict[str,Any], backend: BatchBackend, runtimes: Path) -> dict[str,Any]:
    started=time.perf_counter(); extraction_started=time.perf_counter(); code,extraction=extract_code(generated["generation"]["raw_output"],task["language"]); extraction_ms=round((time.perf_counter()-extraction_started)*1000)
    inference_task=dict(task); inference_task["rendered_prompt"]={"text":generated["prompt"]["rendered"],"sha256":generated["prompt"]["rendered_sha256"]}; validate_task(inference_task)
    verifier_started=time.perf_counter(); verification=verify(inference_task,code,runtimes); verifier_ms=round((time.perf_counter()-verifier_started)*1000); completed=utc_now()
    inference={"parameters":generated["parameters"],"started_at":generated["generation"]["started_at"],"completed_at":completed}
    result=build_result(inference_task,generated["generation"]["raw_output"],code,EXTRACTOR_ID,{key:model[key] for key in ("model_id","revision","artifact_sha256","serving_contract_sha256")},inference,verification)
    value={"schema_version":"ganesh-mini-task-evidence/v2","classification":config["classification"],"run_id":config["run_id"],"task":{"task_id":task["task_id"],"surface":task["surface"],"language":task["language"],"task_sha256":sha256_object(task),"config_sha256":generated["config_sha256"]},"model":model,"runtime":{**backend.identity,"implementation":implementation_identity()},"prompt":generated["prompt"],"generation":generated["generation"],"generation_sha256":generated["generation_sha256"],"extraction":{**extraction,"extracted_code":code,"extracted_code_sha256":sha256_text(code)},"verification":{"result":result,"result_sha256":result["result_sha256"]},"timings_ms":{"model_load_once":backend.load_ms,"generation_batch":generated["generation"]["generation_ms"],"extraction":extraction_ms,"verifier":verifier_ms,"post_generation_total":round((time.perf_counter()-started)*1000)},"memory":{"process_peak_rss_bytes":peak_rss_bytes()},"recorded_at":completed}
    return sealed(value,"evidence_sha256")


def execute(config_path: Path, backend: BatchBackend | None = None, model_override: dict[str,Any] | None = None, artifact_size_override: int | None = None) -> dict[str,Any]:
    config=load_json(config_path); validate_config(config); config_sha=sha256_object(config)
    if model_override is None: model,artifact_size=model_identity(config)
    else:
        if artifact_size_override is None or artifact_size_override<=0: raise ValueError("model identity override requires positive artifact size")
        model,artifact_size=model_override,artifact_size_override
    paths=sorted({path for glob in config["task_globs"] for path in ROOT.glob(glob)})
    if len(paths)!=config["expected_task_count"]: raise ValueError(f"expected {config['expected_task_count']} tasks, found {len(paths)}")
    tasks=[(path,validate_task(load_json(path))) for path in paths]
    if any(task["surface"]!=config["allowed_surface"] for _,task in tasks): raise ValueError("task surface escaped config")
    task_ids=[task["task_id"] for _,task in tasks]
    if len(task_ids)!=len(set(task_ids)): raise ValueError("duplicate task IDs in selected evaluation surface")
    backend=backend or TransformersBatchBackend(ROOT/config["model_dir"],config["auto_model_class"],ROOT/config["adapter"]["dir"] if config.get("adapter") else None); output=ROOT/config["output_dir"]; generated_dir=output/"generated"; final_dir=output/"tasks"
    if backend.identity.get("device")!=config["execution"]["required_device"]: raise RuntimeError(f"evaluation requires {config['execution']['required_device']}, observed {backend.identity.get('device')}")
    implementation=implementation_identity()
    completed: dict[str,dict[str,Any]]={}; pending=[]
    for path,task in tasks:
        final=load_sealed(final_dir/f"{task['task_id']}.json","evidence_sha256")
        if final is not None:
            validate_resumed_task(final,task,config,config_sha,model,backend,implementation); completed[task["task_id"]]=final
        else: pending.append((path,task))
    generated_pending=[]; rendered=[]
    for path,task in pending:
        prior=load_sealed(generated_dir/f"{task['task_id']}.json","generation_sha256")
        if prior is not None:
            validate_resumed_generation(prior,task,config_sha,model,backend,implementation); generated_pending.append((path,task,prior))
        else:
            rendered.append((path,task,*backend.render(task["prompt"]["text"])))
    rendered.sort(key=lambda row:(row[1]["language"],len(row[3])//config["execution"]["length_bucket_width"],len(row[3]),row[1]["task_id"]))
    futures: dict[Future[dict[str,Any]],tuple[Path,dict[str,Any]]] = {}
    with ThreadPoolExecutor(max_workers=config["execution"]["verifier_workers"]) as pool:
        def persist_ready(ready: list[Future[dict[str,Any]]]) -> None:
            if not ready: return
            for future in ready:
                _,task=futures.pop(future); evidence=future.result(); atomic_json(final_dir/f"{task['task_id']}.json",evidence); completed[task["task_id"]]=evidence
            atomic_json(output/"run.json",run_manifest(config,config_sha,model,backend,tasks,completed,final_dir))
        for path,task,generation in generated_pending:
            futures[pool.submit(verify_generated,generation,task,config,model,backend,ROOT/config["runtimes"])]=(path,task)
        size=config["execution"]["batch_size"]
        for lane in sorted({row[1]["language"] for row in rendered}):
            lane_rows=[row for row in rendered if row[1]["language"]==lane]
            if hasattr(backend,"activate"): backend.activate(lane)
            for offset in range(0,len(lane_rows),size):
                batch=lane_rows[offset:offset+size]
                if any(len(row[3])+config["generation"]["max_new_tokens"]>8192 for row in batch): raise ValueError("prompt plus generation exceeds context")
                outputs=backend.generate_batch([row[3] for row in batch],config["generation"]["max_new_tokens"],config["generation"]["use_cache"])
                validate_batch_outputs(outputs,len(batch))
                for (path,task,text,ids),generated_output in zip(batch,outputs):
                    generation=generation_evidence(path,task,config,config_sha,model,artifact_size,backend,text,ids,generated_output); atomic_json(generated_dir/f"{task['task_id']}.json",generation)
                    futures[pool.submit(verify_generated,generation,task,config,model,backend,ROOT/config["runtimes"])]=(path,task)
                persist_ready([future for future in tuple(futures) if future.done()])
        while futures:
            persist_ready([next(as_completed(tuple(futures)))])
    manifest=run_manifest(config,config_sha,model,backend,tasks,completed,final_dir); atomic_json(output/"run.json",manifest); return manifest


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--config",type=Path,required=True); args=parser.parse_args(); result=execute(args.config.resolve()); print(json.dumps(result["task_accounting"],sort_keys=True)); return 0 if result["task_accounting"]["pending"]==0 else 2


if __name__ == "__main__": raise SystemExit(main())
