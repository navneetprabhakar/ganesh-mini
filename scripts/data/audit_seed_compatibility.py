#!/usr/bin/env python3
"""Run bounded current-toolchain syntax/compile checks over the authorized seed."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import resource
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.inference.extract import extract_code


COMMANDS = {
    "python": lambda name: ["python3", "-m", "py_compile", name],
    "javascript": lambda name: ["node", "--check", name],
    "typescript": lambda name: ["tsc", "--pretty", "false", "--noEmit", "--skipLibCheck", "--target", "ES2022", "--module", "commonjs", name],
    "go": lambda name: ["gofmt", "-w", name],
    "java": lambda name: ["javac", "-proc:none", "-Xlint:none", name],
    "rust": lambda name: ["rustc", "--crate-type", "lib", "--emit", "metadata", name],
}
EXTENSIONS={"python":"py","javascript":"js","typescript":"ts","go":"go","java":"java","rust":"rs"}


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def limits() -> None:
    requested_limits=[(resource.RLIMIT_CPU,10),(resource.RLIMIT_FSIZE,16*1024**2)]
    if sys.platform != "darwin": requested_limits += [(resource.RLIMIT_AS,2*1024**3),(resource.RLIMIT_NPROC,64)]
    for kind,requested in requested_limits:
        _,hard=resource.getrlimit(kind); limit=requested if hard==resource.RLIM_INFINITY else min(requested,hard); resource.setrlimit(kind,(limit,limit))


def filename(lane: str, code: str) -> str:
    if lane=="java":
        match=re.search(r"\bpublic\s+(?:final\s+)?(?:class|interface|enum|record)\s+([A-Za-z_$][\w$]*)",code)
        return f"{match.group(1) if match else 'Solution'}.java"
    return f"solution.{EXTENSIONS[lane]}"


def tool_identity(tool: str) -> dict[str,str]:
    executable=COMMANDS[tool]("x."+EXTENSIONS[tool])[0]
    flag="--version" if executable not in {"go","gofmt"} else "version"
    command=[executable,flag] if executable!="gofmt" else ["gofmt","--help"]
    result=subprocess.run(command,capture_output=True,text=True,timeout=10)
    return {"executable":executable,"identity":(result.stdout or result.stderr).splitlines()[0][:500]}


def audit(paths: list[Path], output: Path) -> dict[str,Any]:
    rows=[]; counts=Counter()
    with tempfile.TemporaryDirectory(prefix="ganesh-seed-compat-") as directory:
        root=Path(directory)
        for source in paths:
            for line_number,line in enumerate(source.read_text(encoding="utf-8").splitlines(),1):
                record=json.loads(line); lane=record["lane"]; code,extraction=extract_code(record["messages"][-1]["content"],lane); name=filename(lane,code); work=root/record["id"]; work.mkdir(); candidate=work/name; candidate.write_text(code,encoding="utf-8")
                started=datetime.now(timezone.utc).isoformat()
                try:
                    result=subprocess.run(COMMANDS[lane](name),cwd=work,capture_output=True,text=True,timeout=20,env={**os.environ,"NO_PROXY":"*","no_proxy":"*"},preexec_fn=limits)
                    passed=result.returncode==0; exit_code=result.returncode; stderr=result.stderr[-4000:]; timed_out=False
                except subprocess.TimeoutExpired as exc:
                    passed=False; exit_code=None; stderr=str(exc)[-4000:]; timed_out=True
                rows.append({"id":record["id"],"lane":lane,"source":str(source),"source_line":line_number,"code_sha256":hashlib.sha256(code.encode()).hexdigest(),"extraction_strategy":extraction["strategy"],"command":COMMANDS[lane](name),"started_at":started,"exit_code":exit_code,"timed_out":timed_out,"stderr":stderr,"passed":passed}); counts[(lane,"passed" if passed else "failed")]+=1
    report={"schema_version":"ganesh-mini-seed-compatibility/v1","status":"passed" if all(row["passed"] for row in rows) else "failed","scope":"current-toolchain-syntax-compile-only-no-behavioral-harness","network_execution":False,"toolchains":{lane:tool_identity(lane) for lane in COMMANDS},"counts":{lane:{"passed":counts[(lane,"passed")],"failed":counts[(lane,"failed")]} for lane in COMMANDS},"records":rows,"recorded_at":datetime.now(timezone.utc).isoformat()}; report["evidence_sha256"]=canonical_sha256(report); output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n"); return report


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--input",type=Path,action="append",required=True); parser.add_argument("--output",type=Path,required=True); args=parser.parse_args(); report=audit(args.input,args.output); print(json.dumps({"status":report["status"],"counts":report["counts"]},sort_keys=True)); return 0 if report["status"]=="passed" else 2


if __name__=="__main__": raise SystemExit(main())
