#!/usr/bin/env python3
"""Apply the frozen Gate 3 pilot promotion rule."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.eval.score import load_results


FAMILIES=("go","java","javascript_typescript","python","rust")
LANES=("go","java","javascript","typescript","python","rust")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def load_sealed(path: Path, field: str) -> dict[str,Any]:
    value=json.loads(path.read_text()); claimed=value.pop(field,None)
    if claimed!=canonical_sha256(value): raise ValueError(f"invalid evidence seal: {path}")
    value[field]=claimed; return value


def adjudicate(comparison: dict[str,Any], base: list[dict[str,Any]], candidate: list[dict[str,Any]], retention: dict[str,Any], sft: dict[str,Any]) -> dict[str,Any]:
    improved=[family for family in FAMILIES if comparison["candidate"]["families"][family]["decimal"]>comparison["base"]["families"][family]["decimal"]]
    lane_deltas={lane:comparison["candidate"]["lanes"][lane]["passed"]-comparison["base"]["lanes"][lane]["passed"] for lane in LANES}
    base_quality=comparison["base"]["quality_failures"]; candidate_quality=comparison["candidate"]["quality_failures"]
    ids={row["task_id"] for row in retention["tasks"]}; base_by={row["task_id"]:row for row in base}; candidate_by={row["task_id"]:row for row in candidate}
    if not ids<=set(base_by) or not ids<=set(candidate_by): raise ValueError("retention slice is absent from development results")
    retention_wins=sum(candidate_by[item]["passed"] and not base_by[item]["passed"] for item in ids); retention_losses=sum(base_by[item]["passed"] and not candidate_by[item]["passed"] for item in ids)
    checks=[
        {"name":"four_of_five_families_improve","passed":len(improved)>=4,"evidence":{"improved":improved}},
        {"name":"no_lane_regression","passed":all(delta>=0 for delta in lane_deltas.values()),"evidence":{"lane_deltas":lane_deltas}},
        {"name":"quality_failures_do_not_increase","passed":all(candidate_quality[key]<=base_quality[key] for key in base_quality),"evidence":{"base":base_quality,"candidate":candidate_quality}},
        {"name":"retention_slice","passed":retention_losses<=1 and retention_wins-retention_losses>=-1,"evidence":{"wins":retention_wins,"losses":retention_losses,"tasks":len(ids)}},
        {"name":"sft_complete_and_reload_reproduced","passed":sft.get("status")=="complete" and sft.get("save_reload",{}).get("passed") is True,"evidence":{"run_evidence_sha256":sft.get("evidence_sha256"),"save_reload":sft.get("save_reload")}},
    ]
    passed=all(row["passed"] for row in checks); report={"schema_version":"ganesh-mini-pilot-promotion/v1","status":"promote" if passed else "reject","checks":checks,"failed_checks":[row["name"] for row in checks if not row["passed"]],"decision":"promote_directly_or_admit_one_frozen_pass_a_expansion" if passed else "change_data_or_mechanism_before_scaling"}; report["evidence_sha256"]=canonical_sha256(report); return report


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--comparison",type=Path,required=True); parser.add_argument("--base-results",type=Path,required=True); parser.add_argument("--candidate-results",type=Path,required=True); parser.add_argument("--retention-manifest",type=Path,default=Path("manifests/evaluation/private/retention-slice.json")); parser.add_argument("--sft-evidence",type=Path,required=True); parser.add_argument("--output",type=Path,required=True); args=parser.parse_args(); report=adjudicate(json.loads(args.comparison.read_text()),load_results(args.base_results),load_results(args.candidate_results),load_sealed(args.retention_manifest,"manifest_sha256"),load_sealed(args.sft_evidence,"evidence_sha256")); args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n"); return 0 if report["status"]=="promote" else 2


if __name__=="__main__": raise SystemExit(main())
