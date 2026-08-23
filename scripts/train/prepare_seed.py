#!/usr/bin/env python3
"""Tokenize and deterministically balance the full authorized seed for SFT."""

from __future__ import annotations

import argparse
import hashlib
import json
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
    targets=config["data"]["family_token_targets"]; maximum_epochs=config["recipes"]["primary"]["maximum_effective_epochs"]; total_target=int(min(maximum_epochs*base_tokens[lane]/targets[lane] for lane in LANES)*0.985); rng=random.Random(config.get("seed",3502)); selected=[]; sampled=Counter()
    for lane in LANES:
        candidates=list(by_lane[lane]); rng.shuffle(candidates); goal=round(total_target*targets[lane]); index=0
        while sampled[lane]<goal:
            item=candidates[index%len(candidates)]; response_tokens=len(item["labels"])-item["prompt_token_count"]
            if sampled[lane] and abs(goal-sampled[lane]) <= abs(goal-(sampled[lane]+response_tokens)): break
            copy=dict(item); copy["id"]=f"{item['source_id']}#sample-{index+1}"; selected.append(copy); sampled[lane]+=response_tokens; index+=1
    rng.shuffle(selected); _write_jsonl(output,selected)
    validation_rows=_encode_rows(tokenizer,root/config["data"]["validation_path"],maximum_length); _write_jsonl(validation_output,validation_rows)
    template=root/"models/qwen3.5-2b-15852e8/chat_template.jinja"; effective={lane:sampled[lane]/base_tokens[lane] for lane in LANES}; shares={lane:sampled[lane]/sum(sampled.values()) for lane in LANES}; tolerance=config["data"]["maximum_absolute_share_error"]
    manifest={"schema_version":"ganesh-mini-prepared-seed/v1","passed":all(abs(shares[lane]-targets[lane])<=tolerance and 0<effective[lane]<=maximum_epochs for lane in LANES),"model_id":config["model"]["model_id"],"revision":config["model"]["revision"],"train_sha256":config["data"]["train_sha256"],"validation_sha256":config["data"]["validation_sha256"],"rendering":{"chat_template_source":"chat_template.jinja","chat_template_sha256":sha256(template),"upstream_tokenizer_applied":True,"add_generation_prompt":False,"response_only_labels_verified":True,"response_boundary_method":"tokenizer-generation-prefix-differential-v1","prompt_label_id":-100,"vision_token_count":0},"prepared_train_path":str(output.relative_to(root)),"prepared_train_sha256":sha256(output),"prepared_train_records":len(selected),"prepared_train_input_tokens":sum(sum(row["attention_mask"]) for row in selected),"prepared_validation_path":str(validation_output.relative_to(root)),"prepared_validation_sha256":sha256(validation_output),"prepared_validation_records":len(validation_rows),"sampled_response_tokens_by_lane":dict(sampled),"response_token_shares":shares,"source_response_tokens_by_lane":dict(base_tokens),"effective_epochs_by_lane":effective,"seed":config.get("seed",3502)}; manifest["manifest_sha256"]=canonical_sha256(manifest); manifest_path.parent.mkdir(parents=True,exist_ok=True); manifest_path.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n"); return manifest


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--config",type=Path,default=Path("configs/train/seed_pilot.json")); parser.add_argument("--output",type=Path,default=Path("artifacts/train/seed-pilot/prepared-train.jsonl")); parser.add_argument("--validation-output",type=Path,default=Path("artifacts/train/seed-pilot/prepared-validation.jsonl")); parser.add_argument("--manifest",type=Path,default=Path("artifacts/train/seed-pilot/prepared-dataset-manifest.json")); args=parser.parse_args(); root=Path(__file__).resolve().parents[2]; resolve=lambda path:path if path.is_absolute() else root/path; report=prepare(resolve(args.config),root,resolve(args.output),resolve(args.validation_output),resolve(args.manifest)); print(json.dumps({"passed":report["passed"],"records":report["prepared_train_records"],"shares":report["response_token_shares"]},sort_keys=True)); return 0 if report["passed"] else 2


if __name__=="__main__": raise SystemExit(main())
