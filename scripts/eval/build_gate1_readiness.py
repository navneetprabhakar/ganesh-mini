#!/usr/bin/env python3
"""Build a fail-closed Gate 1 readiness report from frozen evaluation evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.eval.contracts import load_json, sha256_object, validate_result, validate_task
from scripts.inference.run_evaluation import implementation_identity


MODEL_ID="Qwen/Qwen3.5-2B"
REVISION="15852e8c16360a2fea060d615a32b45270f8a8fc"


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":"),ensure_ascii=False,allow_nan=False).encode()).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sealed(path: Path, field: str) -> dict[str,Any]:
    value=json.loads(path.read_text()); unsigned=dict(value); claimed=unsigned.pop(field,None)
    if claimed!=canonical_sha256(unsigned): raise ValueError(f"invalid {field}: {path}")
    return value


def check(name: str, passed: bool, **evidence: Any) -> dict[str,Any]:
    return {"name":name,"passed":bool(passed),"evidence":evidence}


def validate_baseline_tasks(root: Path, baseline: dict[str,Any] | None) -> tuple[bool,dict[str,Any]]:
    if baseline is None: return False,{"reason":"baseline_missing"}
    try:
        config_path=root/"configs/inference/qwen_base_development.json"
        config=load_json(config_path); expected_config_sha=sha256_object(config)
        if baseline.get("schema_version")!="ganesh-mini-inference-run/v2" or baseline.get("config_sha256")!=expected_config_sha:
            raise ValueError("baseline schema or frozen config identity mismatch")
        expected_implementation=implementation_identity()
        runtime=baseline.get("runtime",{})
        if runtime.get("implementation")!=expected_implementation: raise ValueError("baseline implementation identity mismatch")
        expected_tasks={}
        for path in sorted(root.glob("eval/private/development/**/*.task.json")):
            task=validate_task(load_json(path)); expected_tasks[task["task_id"]]=(task,sha256_object(task))
        if len(expected_tasks)!=180: raise ValueError(f"expected 180 unique development tasks, found {len(expected_tasks)}")
        rows=baseline.get("tasks",[])
        if len(rows)!=180 or {row.get("task_id") for row in rows}!=set(expected_tasks): raise ValueError("baseline task rows do not exactly cover the frozen development surface")
        passed=sum(row.get("passed") is True for row in rows); failed=sum(row.get("passed") is False for row in rows); accounting=baseline.get("task_accounting",{})
        if accounting.get("passed")!=passed or accounting.get("failed")!=failed or passed+failed!=180: raise ValueError("baseline aggregate pass accounting mismatch")
        seen_paths=set()
        for row in rows:
            relative=row.get("evidence_path")
            if not isinstance(relative,str): raise ValueError("baseline task evidence path is missing")
            path=(root/relative).resolve(); path.relative_to(root.resolve())
            if path in seen_paths: raise ValueError("duplicate baseline task evidence path")
            seen_paths.add(path)
            evidence=sealed(path,"evidence_sha256")
            if row.get("evidence_sha256")!=evidence["evidence_sha256"]: raise ValueError("baseline row/task evidence seal mismatch")
            task,task_sha=expected_tasks[row["task_id"]]
            if evidence.get("schema_version")!="ganesh-mini-task-evidence/v2" or evidence.get("classification")!="private_development_baseline" or evidence.get("run_id")!=baseline.get("run_id"): raise ValueError("baseline task evidence classification mismatch")
            if evidence.get("model")!=baseline.get("model") or evidence.get("runtime")!=runtime: raise ValueError("baseline task model or runtime mismatch")
            binding=evidence.get("task",{})
            if binding.get("task_id")!=task["task_id"] or binding.get("surface")!="development" or binding.get("task_sha256")!=task_sha or binding.get("config_sha256")!=expected_config_sha: raise ValueError("baseline task binding mismatch")
            result=validate_result(evidence.get("verification",{}).get("result"))
            inference_task=dict(task); inference_task["rendered_prompt"]={"text":evidence["prompt"]["rendered"],"sha256":evidence["prompt"]["rendered_sha256"]}
            if result["task_id"]!=task["task_id"] or result["surface"]!="development" or result["task_sha256"]!=sha256_object(inference_task) or result["prompt_sha256"]!=task["prompt"]["sha256"] or result["rendered_prompt_sha256"]!=evidence["prompt"]["rendered_sha256"]: raise ValueError("baseline result task mismatch")
            if result["passed"] is not row.get("passed") or result["result_sha256"]!=evidence.get("verification",{}).get("result_sha256"): raise ValueError("baseline result accounting mismatch")
            result_model=result["model"]
            if result_model!={key:baseline["model"][key] for key in ("model_id","revision","artifact_sha256","serving_contract_sha256")}: raise ValueError("baseline result model mismatch")
        return True,{"validated_task_evidence":len(rows),"config_sha256":expected_config_sha,"implementation":expected_implementation}
    except (OSError,ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
        return False,{"reason":str(exc)}


def training_isolation(root: Path, manifest_path: Path | None) -> tuple[bool, dict[str, Any]]:
    if manifest_path is not None:
        try:
            manifest=sealed(manifest_path,"manifest_sha256")
            files=manifest.get("files",[])
            passed=(manifest.get("schema_version")=="ganesh-mini-training-workspace/v1" and manifest.get("status")=="sealed" and "eval" in manifest.get("forbidden_roots",[]) and bool(files) and all("eval" not in Path(row["path"]).parts for row in files))
            return passed,{"training_workspace_manifest":str(manifest_path),"training_workspace_manifest_sha256":manifest.get("manifest_sha256"),"training_file_count":len(files)}
        except (OSError,ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
            return False,{"reason":str(exc)}
    try:
        from scripts.train.package_workspace import collect
        files=collect(root)
        return bool(files) and all("eval" not in path.relative_to(root).parts for path in files),{"packager_sha256":file_sha256(root/"scripts/train/package_workspace.py"),"training_file_count":len(files)}
    except (OSError,ValueError,ImportError) as exc:
        return False,{"reason":str(exc)}


def build(root: Path, baseline_path: Path, training_manifest_path: Path | None = None) -> dict[str,Any]:
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
    task_evidence_ok,task_evidence=validate_baseline_tasks(root,baseline)
    baseline_ok=(baseline is not None and baseline.get("classification")=="private_development_baseline" and baseline.get("model",{}).get("model_id")==MODEL_ID and baseline.get("model",{}).get("revision")==REVISION and accounting.get("expected")==accounting.get("completed")==180 and accounting.get("pending")==0 and len(baseline.get("tasks",[]))==180 and all(row.get("status")=="complete" and isinstance(row.get("passed"),bool) and isinstance(row.get("evidence_sha256"),str) for row in baseline.get("tasks",[])) and task_evidence_ok)
    isolation_ok,isolation_evidence=training_isolation(root,training_manifest_path)
    checks=[
        check("private_evaluation_contract",private_ok,path=str(global_path.relative_to(root)),sha256=file_sha256(global_path),seal=global_report.get("report_sha256")),
        check("public_diagnostic_admission",public_ok,path=str(public_path.relative_to(root)),sha256=file_sha256(public_path),status=public.get("status"),imported_tasks=public.get("counts",{}).get("imported_tasks")),
        check("exact_base_development_baseline",baseline_ok,path=str(baseline_path.relative_to(root)) if baseline_path.is_relative_to(root) else str(baseline_path),sha256=file_sha256(baseline_path) if baseline_path.is_file() else None,run_sha256=(baseline or {}).get("run_sha256"),task_evidence=task_evidence),
        check("decision_prompts_not_opened_for_model_selection",isolation_ok,proof="training workspace allowlist excludes eval/; final decision config requires a sealed opened-once declaration",**isolation_evidence),
    ]
    ready=all(row["passed"] for row in checks)
    report={"schema_version":"ganesh-mini-readiness/v1","gate":1,"status":"ready" if ready else "not_ready","model_id":MODEL_ID,"revision":REVISION,"evaluation_contract_frozen":private_ok and public_ok,"base_baseline_complete":baseline_ok,"decision_prompts_exposed":False,"checks":checks,"failed_checks":[row["name"] for row in checks if not row["passed"]]}
    report["evidence_sha256"]=canonical_sha256(report); return report


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[2]); parser.add_argument("--baseline",type=Path,default=Path("measurement/inference/development/qwen3.5-2b-base-v1/run.json")); parser.add_argument("--training-workspace-manifest",type=Path); parser.add_argument("--output",type=Path,default=Path("measurement/gate1/readiness.json")); args=parser.parse_args(); root=args.root.resolve(); resolve=lambda path:path if path.is_absolute() else root/path; report=build(root,resolve(args.baseline),resolve(args.training_workspace_manifest) if args.training_workspace_manifest else None); output=resolve(args.output); output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n"); return 0 if report["status"]=="ready" else 2


if __name__=="__main__": raise SystemExit(main())
