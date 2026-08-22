#!/usr/bin/env python3
"""Execute tranche-3 reference/bad evidence sequentially."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Any
from scripts.eval.authoring.build_tranche3 import MANIFEST,ROOT
from scripts.eval.contracts import load_json,sha256_object,write_json
from scripts.verify.sandbox import verify

DEFAULT_OUTPUT=ROOT/"manifests/evaluation/private/development-tranche3-directionality.json"
RUNTIME_CONFIG=ROOT/"configs/eval/runtimes.json"
def passed(r:dict[str,Any])->bool:return not r["timed_out"] and bool(r["exit_codes"]) and all(c==0 for c in r["exit_codes"])
def execute(entry:dict[str,Any],artifact:str)->dict[str,Any]:
    task=load_json(ROOT/entry["path"]);selected=task["validation"]["reference"] if artifact=="reference" else task["validation"]["known_bad"][0];result=verify(task,selected["code"],RUNTIME_CONFIG)
    return {"task_id":task["task_id"],"language":task["language"],"artifact":artifact,"artifact_label":selected["label"],"artifact_sha256":selected["sha256"],"expected_pass":artifact=="reference","observed_pass":passed(result),"verifier":result}
def run(output:Path=DEFAULT_OUTPUT)->dict[str,Any]:
    manifest=load_json(MANIFEST);rows=[]
    for entry in manifest["tasks"]:
        for artifact in ("reference","known_bad"): rows.append(execute(entry,artifact))
    failures=[{"task_id":r["task_id"],"artifact":r["artifact"],"expected":r["expected_pass"],"observed":r["observed_pass"]} for r in rows if r["expected_pass"]!=r["observed_pass"]]
    evidence={"schema_version":"ganesh-mini-directionality/v1","manifest_path":str(MANIFEST.relative_to(ROOT)),"manifest_sha256":manifest["manifest_sha256"],"execution_mode":"sequential","network_mode":"none","execution_count":len(rows),"reference_passes":sum(r["artifact"]=="reference" and r["observed_pass"] for r in rows),"known_bad_failures":sum(r["artifact"]=="known_bad" and not r["observed_pass"] for r in rows),"timeouts":sum(r["verifier"]["timed_out"] for r in rows),"directionality_failures":failures,"status":"passed" if not failures else "failed","results":rows}
    evidence["evidence_sha256"]=sha256_object(evidence);write_json(output,evidence);return evidence
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,default=DEFAULT_OUTPUT);a=p.parse_args();e=run(a.output);print(json.dumps({k:e[k] for k in ("status","execution_count","reference_passes","known_bad_failures","timeouts","evidence_sha256")},sort_keys=True));raise SystemExit(0 if e["status"]=="passed" else 1)
