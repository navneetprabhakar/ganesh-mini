#!/usr/bin/env python3
"""Tokenize the authorized seed and materialize its training objective.

Version 1 physically sampled rows to balance response-token volume.  Version 2
keeps every authorized source row exactly once and attaches an explicit loss
weight.  The weights make the epoch-average optimization objective match the
five-family target without pretending that duplicated records add diversity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any

from scripts.train.response_only import build_response_only_encoding


LANES=("go","java","javascript","typescript","python","rust")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def _encode_rows(tokenizer: Any, source: Path, maximum_length: int) -> list[dict[str, Any]]:
    rows=[]
    for line in source.read_text(encoding="utf-8").splitlines():
        row=json.loads(line); encoded=build_response_only_encoding(tokenizer,row["messages"],max_length=maximum_length)
        rows.append({"source_id":row["id"],"id":row["id"],"lane":row["lane"],"input_ids":encoded.encoding["input_ids"],"labels":encoded.encoding["labels"],"attention_mask":encoded.encoding.get("attention_mask",[1]*len(encoded.encoding["input_ids"])),"prompt_token_count":encoded.prompt_token_count,"rendered_prompt_sha256":hashlib.sha256(encoded.rendered.encode()).hexdigest()})
    return rows


def attach_objective_weights(rows: list[dict[str, Any]], targets: dict[str, float], accumulation: int) -> tuple[list[dict[str, Any]], dict[str, float]]:
    """Weight token-mean record losses into an exact family-token objective.

    Transformers returns a mean over supervised tokens for each record.  For
    family ``f``, multiplying a record by ``target[f] * record_tokens /
    family_tokens`` reconstructs that family's token mean.  Multiplying by the
    number of optimizer groups keeps the average per-group loss near the usual
    unit scale without changing the epoch objective.
    """
    if not rows or accumulation <= 0:
        raise ValueError("non-empty rows and positive accumulation are required")
    source_ids=[row["source_id"] for row in rows]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("objective weighting requires unique source rows")
    family_tokens=Counter()
    for row in rows:
        family_tokens[row["lane"]] += len(row["labels"]) - row["prompt_token_count"]
    if set(family_tokens) != set(LANES) or set(targets) != set(LANES):
        raise ValueError("objective weighting requires all frozen lanes")
    optimizer_groups=math.ceil(len(rows)/accumulation)
    weighted=[]
    totals=Counter()
    for row in rows:
        response_tokens=len(row["labels"])-row["prompt_token_count"]
        objective_weight=targets[row["lane"]]*response_tokens/family_tokens[row["lane"]]*optimizer_groups
        item=dict(row)
        item["response_token_count"]=response_tokens
        item["objective_weight"]=objective_weight
        weighted.append(item)
        totals[row["lane"]]+=objective_weight
    normalized={lane:totals[lane]/sum(totals.values()) for lane in LANES}
    return weighted,normalized


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text("".join(json.dumps(row,sort_keys=True,separators=(",", ":"))+"\n" for row in rows),encoding="utf-8")


def prepare(config_path: Path, root: Path, output: Path, validation_output: Path, manifest_path: Path) -> dict[str,Any]:
    from transformers import AutoTokenizer
    config=json.loads(config_path.read_text()); tokenizer=AutoTokenizer.from_pretrained(root/"models/qwen3.5-2b-15852e8",local_files_only=True); by_lane=defaultdict(list); base_tokens=Counter()
    maximum_length=config["recipes"]["primary"]["sequence_length"]
    source=root/config["data"]["train_path"]
    for item in _encode_rows(tokenizer,source,maximum_length):
        by_lane[item["lane"]].append(item); base_tokens[item["lane"]]+=len(item["labels"])-item["prompt_token_count"]
    targets=config["data"]["family_token_targets"]; maximum_epochs=config["recipes"]["primary"]["maximum_effective_epochs"]; rng=random.Random(config.get("seed",3502))
    objective=config["data"].get("objective",{"method":"duplicated-response-token-schedule-v1"})
    if objective["method"]=="unique-row-token-weighted-five-family-v2":
        selected=[item for lane in LANES for item in by_lane[lane]]
        rng.shuffle(selected)
        selected,objective_shares=attach_objective_weights(selected,targets,config["recipes"]["primary"]["gradient_accumulation_steps"])
    elif objective["method"]=="duplicated-response-token-schedule-v1":
        total_target=int(min(maximum_epochs*base_tokens[lane]/targets[lane] for lane in LANES)*0.985); selected=[]; sampled=Counter()
        for lane in LANES:
            candidates=list(by_lane[lane]); rng.shuffle(candidates); goal=round(total_target*targets[lane]); index=0
            while sampled[lane]<goal:
                item=candidates[index%len(candidates)]; response_tokens=len(item["labels"])-item["prompt_token_count"]
                if sampled[lane] and abs(goal-sampled[lane]) <= abs(goal-(sampled[lane]+response_tokens)): break
                copy=dict(item); copy["id"]=f"{item['source_id']}#sample-{index+1}"; selected.append(copy); sampled[lane]+=response_tokens; index+=1
        rng.shuffle(selected); objective_shares={lane:sampled[lane]/sum(sampled.values()) for lane in LANES}
    else:
        raise ValueError(f"unsupported data objective: {objective['method']}")
    sampled=Counter({lane:sum(len(item["labels"])-item["prompt_token_count"] for item in selected if item["lane"]==lane) for lane in LANES})
    _write_jsonl(output,selected)
    validation_rows=_encode_rows(tokenizer,root/config["data"]["validation_path"],maximum_length); _write_jsonl(validation_output,validation_rows)
    template=root/"models/qwen3.5-2b-15852e8/chat_template.jinja"; effective={lane:sampled[lane]/base_tokens[lane] for lane in LANES}; shares={lane:sampled[lane]/sum(sampled.values()) for lane in LANES}; tolerance=config["data"]["maximum_absolute_share_error"]
    unique_ok=len(selected)==sum(len(values) for values in by_lane.values())==len({item["source_id"] for item in selected}) if objective["method"]=="unique-row-token-weighted-five-family-v2" else True
    balance_ok=all(abs(objective_shares[lane]-targets[lane])<=tolerance for lane in LANES)
    manifest={"schema_version":"ganesh-mini-prepared-seed/v2" if objective["method"].endswith("v2") else "ganesh-mini-prepared-seed/v1","passed":unique_ok and balance_ok and all(0<effective[lane]<=maximum_epochs for lane in LANES),"model_id":config["model"]["model_id"],"revision":config["model"]["revision"],"train_sha256":config["data"]["train_sha256"],"validation_sha256":config["data"]["validation_sha256"],"rendering":{"chat_template_source":"chat_template.jinja","chat_template_sha256":sha256(template),"upstream_tokenizer_applied":True,"add_generation_prompt":False,"response_only_labels_verified":True,"response_boundary_method":"tokenizer-generation-prefix-differential-v1","prompt_label_id":-100,"vision_token_count":0},"objective":{"method":objective["method"],"unique_source_rows":unique_ok,"loss_input":"per-record-supervised-token-mean","family_targets":targets,"realized_normalized_weight_by_lane":objective_shares,"optimizer_group_scale":math.ceil(len(selected)/config["recipes"]["primary"]["gradient_accumulation_steps"]) if objective["method"].endswith("v2") else None},"prepared_train_path":str(output.relative_to(root)),"prepared_train_sha256":sha256(output),"prepared_train_records":len(selected),"prepared_train_input_tokens":sum(sum(row["attention_mask"]) for row in selected),"prepared_validation_path":str(validation_output.relative_to(root)),"prepared_validation_sha256":sha256(validation_output),"prepared_validation_records":len(validation_rows),"sampled_response_tokens_by_lane":dict(sampled),"response_token_shares":shares,"source_response_tokens_by_lane":dict(base_tokens),"effective_epochs_by_lane":effective,"seed":config.get("seed",3502)}
    if not objective["method"].endswith("v2"): manifest.pop("objective")
    manifest["manifest_sha256"]=canonical_sha256(manifest); manifest_path.parent.mkdir(parents=True,exist_ok=True); manifest_path.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n"); return manifest


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--config",type=Path,default=Path("configs/train/seed_pilot.json")); parser.add_argument("--output",type=Path,default=Path("artifacts/train/seed-pilot/prepared-train.jsonl")); parser.add_argument("--validation-output",type=Path,default=Path("artifacts/train/seed-pilot/prepared-validation.jsonl")); parser.add_argument("--manifest",type=Path,default=Path("artifacts/train/seed-pilot/prepared-dataset-manifest.json")); args=parser.parse_args(); root=Path(__file__).resolve().parents[2]; resolve=lambda path:path if path.is_absolute() else root/path; report=prepare(resolve(args.config),root,resolve(args.output),resolve(args.validation_output),resolve(args.manifest)); print(json.dumps({"passed":report["passed"],"records":report["prepared_train_records"],"raw_response_token_shares":report["response_token_shares"],"objective_shares":report.get("objective",{}).get("realized_normalized_weight_by_lane",report["response_token_shares"])},sort_keys=True)); return 0 if report["passed"] else 2


if __name__=="__main__": raise SystemExit(main())
