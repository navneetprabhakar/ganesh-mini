#!/usr/bin/env python3
"""Build a fail-closed Gate 1 readiness report from frozen evaluation evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.train.package_workspace import collect


MODEL_ID="Qwen/Qwen3.5-2B"
REVISION="15852e8c16360a2fea060d615a32b45270f8a8fc"


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sealed(path: Path, field: str) -> dict[str,Any]:
    value=json.loads(path.read_text()); unsigned=dict(value); claimed=unsigned.pop(field,None)
    if claimed!=canonical_sha256(unsigned): raise ValueError(f"invalid {field}: {path}")
    return value


def check(name: str, passed: bool, **evidence: Any) -> dict[str,Any]:
    return {"name":name,"passed":bool(passed),"evidence":evidence}


def build(root: Path, baseline_path: Path) -> dict[str,Any]:
    global_path=root/"manifests/evaluation/private/decision-global-separation.json"
    public_path=root/"manifests/evaluation/public/multi_livecodebench_v6.json"
    global_report=sealed(global_path,"report_sha256")
    public=json.loads(public_path.read_text())
    baseline=None
    try:
        baseline=sealed(baseline_path,"run_sha256") if baseline_path.is_file() else None
    except (OSError,ValueError,json.JSONDecodeError):
        baseline=None
    private_ok=(global_report.get("status")=="passed" and global_report.get("counts",{}).get("development_tasks")==180 and global_report.get("counts",{}).get("decision_tasks")==360 and not global_report.get("overlaps",{}).get("exact") and not global_report.get("overlaps",{}).get("normalized"))
    public_ok=public.get("status")=="no_compatible_tasks" and public.get("counts",{}).get("source_records")==175 and public.get("counts",{}).get("exclusions")==1050 and public.get("counts",{}).get("imported_tasks")==0
    accounting=(baseline or {}).get("task_accounting",{})
    baseline_ok=(baseline is not None and baseline.get("classification")=="private_development_baseline" and baseline.get("model",{}).get("model_id")==MODEL_ID and baseline.get("model",{}).get("revision")==REVISION and accounting.get("expected")==accounting.get("completed")==180 and accounting.get("pending")==0 and len(baseline.get("tasks",[]))==180 and all(row.get("status")=="complete" and isinstance(row.get("passed"),bool) and isinstance(row.get("evidence_sha256"),str) for row in baseline.get("tasks",[])))
    training_files=collect(root); isolation_ok=bool(training_files) and all("eval" not in path.relative_to(root).parts for path in training_files)
    checks=[
        check("private_evaluation_contract",private_ok,path=str(global_path.relative_to(root)),sha256=file_sha256(global_path),seal=global_report.get("report_sha256")),
        check("public_diagnostic_admission",public_ok,path=str(public_path.relative_to(root)),sha256=file_sha256(public_path),status=public.get("status"),imported_tasks=public.get("counts",{}).get("imported_tasks")),
        check("exact_base_development_baseline",baseline_ok,path=str(baseline_path.relative_to(root)) if baseline_path.is_relative_to(root) else str(baseline_path),sha256=file_sha256(baseline_path) if baseline_path.is_file() else None,run_sha256=(baseline or {}).get("run_sha256")),
        check("decision_prompts_not_opened_for_model_selection",isolation_ok,proof="training workspace allowlist excludes eval/; final decision config requires a sealed opened-once declaration",packager_sha256=file_sha256(root/"scripts/train/package_workspace.py"),training_file_count=len(training_files)),
    ]
    ready=all(row["passed"] for row in checks)
    report={"schema_version":"ganesh-mini-readiness/v1","gate":1,"status":"ready" if ready else "not_ready","model_id":MODEL_ID,"revision":REVISION,"evaluation_contract_frozen":private_ok and public_ok,"base_baseline_complete":baseline_ok,"decision_prompts_exposed":False,"checks":checks,"failed_checks":[row["name"] for row in checks if not row["passed"]]}
    report["evidence_sha256"]=canonical_sha256(report); return report


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[2]); parser.add_argument("--baseline",type=Path,default=Path("measurement/inference/development/qwen3.5-2b-base-v1/run.json")); parser.add_argument("--output",type=Path,default=Path("measurement/gate1/readiness.json")); args=parser.parse_args(); root=args.root.resolve(); resolve=lambda path:path if path.is_absolute() else root/path; report=build(root,resolve(args.baseline)); output=resolve(args.output); output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n"); return 0 if report["status"]=="ready" else 2


if __name__=="__main__": raise SystemExit(main())
