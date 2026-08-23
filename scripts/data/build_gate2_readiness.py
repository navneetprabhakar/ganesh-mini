#!/usr/bin/env python3
"""Build the fail-closed Gate 2 seed readiness report."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_seal(value: dict[str,Any], field: str) -> bool:
    claimed=value.get(field); unsigned=dict(value); unsigned.pop(field,None); return claimed==canonical_sha256(unsigned)


def build(root: Path, manifest_path: Path) -> dict[str,Any]:
    manifest=json.loads(manifest_path.read_text()); checks=[]
    checks.append({"name":"seed_manifest_seal","passed":verify_seal(manifest,"manifest_sha256")})
    outputs=manifest.get("outputs",{})
    for split in ("train","validation"):
        item=outputs.get(split,{}); path=root/item.get("path",""); checks.append({"name":f"{split}_identity","passed":path.is_file() and file_sha256(path)==item.get("sha256") and len(path.read_text().splitlines())==item.get("records")})
    overlap=manifest.get("evaluation_overlap",{}); separation=overlap.get("global_separation") or {}; separation_path=root/separation.get("path","")
    separation_ok=separation_path.is_file() and file_sha256(separation_path)==separation.get("sha256") and overlap.get("status")=="passed" and overlap.get("normalized_prompt_overlaps")==[] and len(overlap.get("inputs",[]))==540
    checks.append({"name":"evaluation_overlap","passed":separation_ok,"comparison_tasks":len(overlap.get("inputs",[]))})
    compatibility=manifest.get("compatibility",{}).get("current_language_toolchain_execution"); compatibility_path=root/(compatibility or {}).get("path","") if isinstance(compatibility,dict) else root/"missing"
    compatibility_ok=isinstance(compatibility,dict) and compatibility.get("status")=="passed" and compatibility.get("records")==1449 and compatibility_path.is_file() and file_sha256(compatibility_path)==compatibility.get("sha256")
    checks.append({"name":"current_toolchain_compatibility","passed":compatibility_ok,"scope":compatibility.get("scope") if isinstance(compatibility,dict) else None})
    ready=all(row["passed"] for row in checks)
    report={"schema_version":"ganesh-mini-readiness/v1","gate":2,"status":"ready" if ready else "not_ready","model_id":"Qwen/Qwen3.5-2B","revision":"15852e8c16360a2fea060d615a32b45270f8a8fc","seed_manifest_sha256":file_sha256(manifest_path),"seed_manifest_seal":manifest.get("manifest_sha256"),"train_sha256":outputs.get("train",{}).get("sha256"),"validation_sha256":outputs.get("validation",{}).get("sha256"),"compatibility_passed":compatibility_ok,"compatibility_scope":compatibility.get("scope") if isinstance(compatibility,dict) else None,"evaluation_overlap_passed":separation_ok,"checks":checks,"failed_checks":[row["name"] for row in checks if not row["passed"]]}; report["report_sha256"]=canonical_sha256(report); return report


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[2]); parser.add_argument("--manifest",type=Path,default=Path("manifests/datasets/ganesh_v01_seed.json")); parser.add_argument("--output",type=Path,default=Path("measurement/gate2/readiness.json")); args=parser.parse_args(); report=build(args.root.resolve(),args.manifest); args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n"); return 0 if report["status"]=="ready" else 2


if __name__=="__main__": raise SystemExit(main())
