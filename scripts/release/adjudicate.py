#!/usr/bin/env python3
"""Apply the frozen Ganesh Mini 1.0 release gates without inventing evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


LANES=("go","java","javascript","typescript","python","rust")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str,Any]:
    return json.loads(path.read_text())


def total_passes(cohort: dict[str,Any]) -> int:
    return sum(cohort["lanes"][lane]["passed"] for lane in LANES)


def check(name: str, passed: bool, **evidence: Any) -> dict[str,Any]:
    return {"name":name,"passed":bool(passed),"evidence":evidence}


def adjudicate(base_comparison: dict[str,Any], quant_comparison: dict[str,Any], laptop: dict[str,Any], manifests: list[Path]) -> dict[str,Any]:
    delta=base_comparison["five_family_macro_delta"]["decimal"]; paired=base_comparison["paired"]; cluster=paired["cluster_aware"]
    lane_deltas={lane:base_comparison["candidate"]["lanes"][lane]["passed"]-base_comparison["base"]["lanes"][lane]["passed"] for lane in LANES}
    merged=total_passes(quant_comparison["base"]); q8=total_passes(quant_comparison["candidate"]); retention=q8/merged if merged else 1.0
    manifest_evidence=[]
    for path in manifests:
        try:
            value=load(path); seal=next((value[key] for key in ("manifest_sha256","report_sha256","evidence_sha256","run_sha256") if key in value),None)
            sealed_ok=isinstance(seal,str) and len(seal)==64 and canonical_sha256({key:item for key,item in value.items() if item!=seal or key not in ("manifest_sha256","report_sha256","evidence_sha256","run_sha256")})==seal
        except (OSError,json.JSONDecodeError):
            seal=None; sealed_ok=False
        manifest_evidence.append({"path":str(path),"sha256":file_sha256(path) if path.is_file() else None,"seal":seal,"passed":sealed_ok})
    profiles=laptop.get("profiles",{})
    checks=[
        check("positive_five_family_macro",delta>0,delta=delta),
        check("cluster_supported_improvement",cluster["bootstrap_ci"]["lower"]>0 and cluster["two_sided_permutation_p"]<=0.05,cluster_aware=cluster),
        check("no_lane_regresses_more_than_two",all(value>=-2 for value in lane_deltas.values()),lane_pass_deltas=lane_deltas),
        check("q8_retains_98_percent",retention>=0.98,merged_solved=merged,q8_solved=q8,retention=retention),
        check("q8_8gb_profile",profiles.get("q8",{}).get("passed") is True and profiles.get("q8",{}).get("peak_rss_bytes",8*1024**3)<=7*1024**3,profile=profiles.get("q8")),
        check("f16_16gb_profile",profiles.get("f16",{}).get("passed") is True and profiles.get("f16",{}).get("peak_rss_bytes",16*1024**3)<=14*1024**3,profile=profiles.get("f16")),
        check("required_manifests_complete",bool(manifest_evidence) and all(row["passed"] for row in manifest_evidence),manifests=manifest_evidence),
    ]
    eligible=all(row["passed"] for row in checks); report={"schema_version":"ganesh-mini-release-decision/v1","model_name":"ganesh-mini-1.0","status":"release-eligible" if eligible else "release-blocked","checks":checks,"failed_checks":[row["name"] for row in checks if not row["passed"]]}; report["evidence_sha256"]=canonical_sha256(report); return report


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--base-comparison",type=Path,required=True); parser.add_argument("--quant-comparison",type=Path,required=True); parser.add_argument("--laptop-certification",type=Path,required=True); parser.add_argument("--manifest",type=Path,action="append",required=True); parser.add_argument("--output",type=Path,required=True); args=parser.parse_args(); report=adjudicate(load(args.base_comparison),load(args.quant_comparison),load(args.laptop_certification),args.manifest); args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n"); return 0 if report["status"]=="release-eligible" else 2


if __name__=="__main__": raise SystemExit(main())
