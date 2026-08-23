#!/usr/bin/env python3
"""Freeze a small six-lane instruction/output-contract retention slice."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from scripts.eval.contracts import sha256_object,validate_task


LANES=("go","java","javascript","typescript","python","rust")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def build(root: Path) -> dict[str,Any]:
    by_lane=defaultdict(list)
    for path in sorted((root/"eval/private/development").glob("**/*.task.json")):
        task=validate_task(json.loads(path.read_text())); by_lane[task["language"]].append((path,task))
    tasks=[]
    for lane in LANES:
        if len(by_lane[lane])<2: raise ValueError(f"retention slice lacks {lane}")
        for path,task in by_lane[lane][:2]: tasks.append({"task_id":task["task_id"],"language":lane,"task_path":str(path.relative_to(root)),"task_sha256":sha256_object(task),"prompt_sha256":task["prompt"]["sha256"]})
    report={"schema_version":"ganesh-mini-retention-slice/v1","status":"frozen","purpose":"general coding instruction and raw-source output-contract retention; promotion diagnostic only","selection":"first two task IDs per lane from the already frozen private development surface","task_count":12,"tasks":tasks}; report["manifest_sha256"]=canonical_sha256(report); return report


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[2]); parser.add_argument("--output",type=Path,default=Path("manifests/evaluation/private/retention-slice.json")); args=parser.parse_args(); root=args.root.resolve(); output=args.output if args.output.is_absolute() else root/args.output; report=build(root); output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n"); return 0


if __name__=="__main__": raise SystemExit(main())
