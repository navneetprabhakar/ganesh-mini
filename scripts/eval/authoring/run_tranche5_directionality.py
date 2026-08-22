#!/usr/bin/env python3
"""Execute tranche-5 directionality sequentially in bounded sandboxes."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Any
from scripts.eval.authoring.build_tranche5 import MANIFEST,ROOT
from scripts.eval.contracts import load_json,sha256_object,write_json
from scripts.verify.sandbox import verify

DEFAULT_OUTPUT=ROOT/"manifests/evaluation/private/development-tranche5-directionality.json"
RUNTIME_CONFIG=ROOT/"configs/eval/runtimes.json"

def passed(result:dict[str,Any])->bool:return not result["timed_out"] and bool(result["exit_codes"]) and all(code==0 for code in result["exit_codes"])
def execute(entry:dict[str,Any],artifact:str)->dict[str,Any]:
    task=load_json(ROOT/entry["path"]);selected=task["validation"]["reference"] if artifact=="reference" else task["validation"]["known_bad"][0];verifier=verify(task,selected["code"],RUNTIME_CONFIG)
    return {"task_id":task["task_id"],"language":task["language"],"artifact":artifact,"artifact_label":selected["label"],"artifact_sha256":selected["sha256"],"expected_pass":artifact=="reference","observed_pass":passed(verifier),"verifier":verifier}
def summarize(manifest:dict[str,Any],rows:list[dict[str,Any]])->dict[str,Any]:
    failures=[{"task_id":r["task_id"],"artifact":r["artifact"],"expected_pass":r["expected_pass"],"observed_pass":r["observed_pass"],"timed_out":r["verifier"]["timed_out"]}for r in rows if r["expected_pass"]!=r["observed_pass"]or r["verifier"]["timed_out"]]
    evidence={"schema_version":"ganesh-mini-directionality-evidence/v1","evaluation_manifest":str(MANIFEST.relative_to(ROOT)),"evaluation_manifest_sha256":manifest["manifest_sha256"],"runtime_config":str(RUNTIME_CONFIG.relative_to(ROOT)),"execution_mode":"sequential","task_count":manifest["task_count"],"execution_count":len(rows),"reference_passes":sum(r["artifact"]=="reference"and r["observed_pass"]for r in rows),"known_bad_rejections":sum(r["artifact"]=="known_bad"and not r["observed_pass"]for r in rows),"failures":failures,"status":"passed"if not failures else"failed","executions":rows};evidence["evidence_sha256"]=sha256_object(evidence);return evidence
def run(output:Path=DEFAULT_OUTPUT)->dict[str,Any]:
    manifest=load_json(MANIFEST);rows=[]
    for entry in manifest["tasks"]:rows.append(execute(entry,"reference"));rows.append(execute(entry,"known_bad"))
    evidence=summarize(manifest,rows);write_json(output,evidence);return evidence
def main()->int:
    parser=argparse.ArgumentParser();parser.add_argument("--output",type=Path,default=DEFAULT_OUTPUT);args=parser.parse_args();e=run(args.output);print(json.dumps({k:e[k]for k in("status","execution_count","reference_passes","known_bad_rejections","evidence_sha256")},sort_keys=True));return int(e["status"]!="passed")
if __name__=="__main__":raise SystemExit(main())
