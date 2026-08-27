#!/usr/bin/env python3
"""Freeze the pre-existing development tranche 1 as the Gate 3 canary.

The selection rule is structural and predates all candidate results: take all
five tasks per lane from tranche 1.  No result files are read, and the canary
remains development evidence rather than training data or a release surface.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


LANES=("go","java","javascript","typescript","python","rust")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def build(root: Path, output: Path) -> dict[str,Any]:
    tranche=root/"eval/private/development/tranche1"
    entries=[]; lanes=Counter(); kinds=Counter()
    for path in sorted(tranche.glob("*.task.json")):
        task=json.loads(path.read_text())
        if task.get("surface")!="development" or task.get("language") not in LANES:
            raise ValueError(f"non-development task escaped canary: {path}")
        entries.append({"task_id":task["task_id"],"language":task["language"],"task_type":task["task_type"],"path":str(path.relative_to(root)),"task_file_sha256":sha256(path),"prompt_sha256":task["prompt"]["sha256"]})
        lanes[task["language"]]+=1; kinds[task["task_type"]]+=1
    if len(entries)!=30 or lanes!=Counter({lane:5 for lane in LANES}) or set(kinds)!={"generation","repair"}:
        raise ValueError("canary must contain the complete five-per-lane tranche 1 surface")
    manifest={"schema_version":"ganesh-mini-gate3-canary/v1","status":"frozen","surface":"development","selection_rule":"all tasks from pre-existing development tranche 1; structural selection without reading model results","checkpoint_triage_allowed":True,"promotion_selection_allowed":False,"training_admission_allowed":False,"records":len(entries),"lanes":dict(lanes),"task_types":dict(kinds),"tasks":entries}
    manifest["manifest_sha256"]=canonical_sha256(manifest)
    output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    return manifest


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[2]); parser.add_argument("--output",type=Path,default=Path("eval/private/development/gate3_canary_manifest.json")); args=parser.parse_args(); root=args.root.resolve(); output=args.output if args.output.is_absolute() else root/args.output; result=build(root,output); print(json.dumps({"status":result["status"],"records":result["records"],"manifest_sha256":result["manifest_sha256"]},sort_keys=True)); return 0


if __name__=="__main__": raise SystemExit(main())
