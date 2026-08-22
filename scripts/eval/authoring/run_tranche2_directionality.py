#!/usr/bin/env python3
"""Execute tranche-2 directionality sequentially and preserve evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.eval.authoring.build_tranche2 import MANIFEST, ROOT
from scripts.eval.contracts import load_json, sha256_object, write_json
from scripts.verify.sandbox import verify

DEFAULT_OUTPUT = ROOT / "manifests/evaluation/private/development-tranche2-directionality.json"
RUNTIME_CONFIG = ROOT / "configs/eval/runtimes.json"

def passed(result: dict[str,Any])->bool:
    return not result["timed_out"] and bool(result["exit_codes"]) and all(code==0 for code in result["exit_codes"])

def execute(entry: dict[str,Any], artifact: str)->dict[str,Any]:
    task=load_json(ROOT/entry["path"])
    selected=task["validation"]["reference"] if artifact=="reference" else task["validation"]["known_bad"][0]
    verifier=verify(task,selected["code"],RUNTIME_CONFIG)
    return {"task_id":task["task_id"],"language":task["language"],"artifact":artifact,"artifact_label":selected["label"],"artifact_sha256":selected["sha256"],"expected_pass":artifact=="reference","observed_pass":passed(verifier),"verifier":verifier}

def run(output:Path=DEFAULT_OUTPUT,retry_failures:bool=False)->dict[str,Any]:
    manifest=load_json(MANIFEST);prior_hash=None;retry_count=0
    if retry_failures:
        prior=load_json(output);prior_hash=prior["evidence_sha256"];rows=[]
        prior_rows={(r["task_id"],r["artifact"]):r for r in prior["executions"]}
        for entry in manifest["tasks"]:
            task=load_json(ROOT/entry["path"])
            for artifact in ("reference","known_bad"):
                selected=task["validation"]["reference"] if artifact=="reference" else task["validation"]["known_bad"][0]
                old=prior_rows.get((task["task_id"],artifact))
                if old is None or old["artifact_sha256"]!=selected["sha256"] or old["expected_pass"]!=old["observed_pass"]:
                    rows.append(execute(entry,artifact));retry_count+=1
                else: rows.append(old)
    else:
        rows=[]
        for entry in manifest["tasks"]:
            rows.append(execute(entry,"reference"));rows.append(execute(entry,"known_bad"))
    failures=[{"task_id":r["task_id"],"artifact":r["artifact"],"expected_pass":r["expected_pass"],"observed_pass":r["observed_pass"]} for r in rows if r["expected_pass"]!=r["observed_pass"]]
    evidence={"schema_version":"ganesh-mini-directionality-evidence/v1","evaluation_manifest":str(MANIFEST.relative_to(ROOT)),"evaluation_manifest_sha256":manifest["manifest_sha256"],"runtime_config":str(RUNTIME_CONFIG.relative_to(ROOT)),"execution_mode":"sequential" if not retry_failures else "sequential-with-targeted-retry","prior_evidence_sha256":prior_hash,"retry_execution_count":retry_count,"task_count":manifest["task_count"],"execution_count":len(rows),"reference_passes":sum(r["artifact"]=="reference" and r["observed_pass"] for r in rows),"known_bad_rejections":sum(r["artifact"]=="known_bad" and not r["observed_pass"] for r in rows),"failures":failures,"status":"passed" if not failures else "failed","executions":rows}
    evidence["evidence_sha256"]=sha256_object(evidence);write_json(output,evidence);return evidence

if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--retry-failures",action="store_true");args=parser.parse_args()
    e=run(retry_failures=args.retry_failures);print(json.dumps({k:e[k] for k in ("status","execution_count","retry_execution_count","reference_passes","known_bad_rejections","evidence_sha256")},sort_keys=True));raise SystemExit(e["status"]!="passed")
