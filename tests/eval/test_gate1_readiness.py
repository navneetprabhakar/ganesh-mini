import json
from pathlib import Path

from scripts.eval.build_gate1_readiness import build, canonical_sha256


ROOT=Path(__file__).resolve().parents[2]


def test_repository_gate1_fails_only_on_unexecuted_base_baseline() -> None:
    report=build(ROOT,ROOT/"measurement/inference/development/qwen3.5-2b-base-v1/run.json")
    assert report["status"]=="not_ready"
    assert report["failed_checks"]==["exact_base_development_baseline"]
    unsigned=dict(report); claimed=unsigned.pop("evidence_sha256")
    assert canonical_sha256(unsigned)==claimed


def test_complete_baseline_opens_gate(tmp_path: Path) -> None:
    tasks=[{"task_id":f"task-{index}","status":"complete","passed":False,"evidence_sha256":"a"*64} for index in range(180)]
    run={"classification":"private_development_baseline","model":{"model_id":"Qwen/Qwen3.5-2B","revision":"15852e8c16360a2fea060d615a32b45270f8a8fc"},"task_accounting":{"expected":180,"completed":180,"passed":0,"failed":180,"pending":0},"tasks":tasks}
    run["run_sha256"]=canonical_sha256(run); path=tmp_path/"run.json"; path.write_text(json.dumps(run))
    report=build(ROOT,path)
    assert report["status"]=="ready"
