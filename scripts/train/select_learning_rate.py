#!/usr/bin/env python3
"""Apply the frozen two-point learning-rate selection rule."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.eval.score import load_results


RULE="select_0.0002_only_if_development_macro_improves_by_at_least_one_task_equivalent_with_no_lane_regression_else_0.0001"
LANES=("go","java","javascript","typescript","python","rust")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def collection_sha256(results: list[dict[str,Any]]) -> str:
    return canonical_sha256([result["result_sha256"] for result in sorted(results,key=lambda row:row["task_id"])])


def load_run(path: Path) -> dict[str,Any]:
    value=json.loads(path.read_text()); claimed=value.pop("evidence_sha256",None)
    if claimed!=canonical_sha256(value): raise ValueError(f"invalid run evidence seal: {path}")
    value["evidence_sha256"]=claimed; return value


def select(low: list[dict[str,Any]], high: list[dict[str,Any]], low_run: dict[str,Any], high_run: dict[str,Any]) -> dict[str,Any]:
    low_by={row["task_id"]:row for row in low}; high_by={row["task_id"]:row for row in high}
    if set(low_by)!=set(high_by) or len(low_by)!=180: raise ValueError("LR candidates must cover the same 180 development tasks")
    for run,lr in ((low_run,0.0001),(high_run,0.0002)):
        if run.get("status")!="complete" or run.get("identities",{}).get("phase")!="lr-candidate" or run.get("identities",{}).get("learning_rate")!=str(lr) or run.get("state",{}).get("seen_tokens",0)<400000: raise ValueError("LR selection requires two complete, bounded candidate runs")
    low_lane={lane:sum(row["passed"] for row in low if row["language"]==lane) for lane in LANES}; high_lane={lane:sum(row["passed"] for row in high if row["language"]==lane) for lane in LANES}; low_total=sum(low_lane.values()); high_total=sum(high_lane.values()); choose_high=high_total>=low_total+1 and all(high_lane[lane]>=low_lane[lane] for lane in LANES)
    evidence={"schema_version":"ganesh-mini-lr-selection/v1","status":"selected","rule":RULE,"candidates":{"0.0001":{"run_evidence_sha256":low_run["evidence_sha256"],"result_collection_sha256":collection_sha256(low),"passed":low_total,"lanes":low_lane},"0.0002":{"run_evidence_sha256":high_run["evidence_sha256"],"result_collection_sha256":collection_sha256(high),"passed":high_total,"lanes":high_lane}},"selected_learning_rate":0.0002 if choose_high else 0.0001,"decision":"higher_lr_improved_without_lane_regression" if choose_high else "conservative_lower_lr_default"}; evidence["evidence_sha256"]=canonical_sha256(evidence); return evidence


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--lr-1e-4-results",type=Path,required=True); parser.add_argument("--lr-2e-4-results",type=Path,required=True); parser.add_argument("--lr-1e-4-run",type=Path,required=True); parser.add_argument("--lr-2e-4-run",type=Path,required=True); parser.add_argument("--output",type=Path,required=True); args=parser.parse_args(); evidence=select(load_results(args.lr_1e_4_results),load_results(args.lr_2e_4_results),load_run(args.lr_1e_4_run),load_run(args.lr_2e_4_run)); args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(evidence,indent=2,sort_keys=True)+"\n"); return 0


if __name__=="__main__": raise SystemExit(main())
