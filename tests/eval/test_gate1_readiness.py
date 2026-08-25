import json
from pathlib import Path
from unittest.mock import patch

from scripts.eval.build_gate1_readiness import build, canonical_sha256


ROOT=Path(__file__).resolve().parents[2]


def test_repository_gate1_is_open_on_admitted_exact_base_baseline() -> None:
    report=build(ROOT,ROOT/"measurement/inference/development/qwen3.5-2b-base-v1/run.json")
    assert report["status"]=="ready"
    assert report["failed_checks"]==[]
    assert report["base_baseline_complete"] is True
    assert report["checks"][2]["evidence"]["task_evidence"]["validated_task_evidence"]==180
    unsigned=dict(report); claimed=unsigned.pop("evidence_sha256")
    assert canonical_sha256(unsigned)==claimed


@patch("scripts.eval.build_gate1_readiness.validate_baseline_tasks",return_value=(True,{"validated_task_evidence":180}))
def test_complete_baseline_opens_gate(_validated, tmp_path: Path) -> None:
    tasks=[{"task_id":f"task-{index}","status":"complete","passed":False,"evidence_sha256":"a"*64} for index in range(180)]
    run={"classification":"private_development_baseline","model":{"model_id":"Qwen/Qwen3.5-2B","revision":"15852e8c16360a2fea060d615a32b45270f8a8fc"},"task_accounting":{"expected":180,"completed":180,"passed":0,"failed":180,"pending":0},"tasks":tasks}
    run["run_sha256"]=canonical_sha256(run); path=tmp_path/"run.json"; path.write_text(json.dumps(run))
    report=build(ROOT,path)
    assert report["status"]=="ready"


def test_aggregate_baseline_without_task_evidence_stays_closed(tmp_path: Path) -> None:
    tasks=[{"task_id":f"task-{index}","status":"complete","passed":False,"evidence_path":f"tasks/task-{index}.json","evidence_sha256":"a"*64} for index in range(180)]
    run={"schema_version":"ganesh-mini-inference-run/v2","run_id":"untrusted-aggregate","classification":"private_development_baseline","config_sha256":"b"*64,"model":{"model_id":"Qwen/Qwen3.5-2B","revision":"15852e8c16360a2fea060d615a32b45270f8a8fc"},"runtime":{},"task_accounting":{"expected":180,"completed":180,"passed":0,"failed":180,"pending":0},"tasks":tasks}
    run["run_sha256"]=canonical_sha256(run); path=tmp_path/"run.json"; path.write_text(json.dumps(run))
    report=build(ROOT,path)
    assert report["status"]=="not_ready"
    assert report["failed_checks"]==["exact_base_development_baseline"]
    assert report["checks"][2]["evidence"]["task_evidence"]["reason"]=="baseline schema or frozen config identity mismatch"
