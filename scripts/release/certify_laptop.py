#!/usr/bin/env python3
"""Certify final GGUF artifacts against frozen 8 GB and 16 GB RSS envelopes."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any


GIB=1024**3
ROOT=Path(__file__).resolve().parents[2]
PROMPTS=(
    "Return only a Go function Add(a, b int) int that returns the sum.",
    "Return only a Java class Solution with static int add(int a,int b).",
    "Return only a JavaScript function add(a,b) that returns the sum.",
    "Return only a TypeScript function add(a:number,b:number):number.",
    "Return only a Python function add(a, b) that returns the sum.",
    "Return only a Rust function fn add(a: i32, b: i32) -> i32.",
)


def sha256(path: Path) -> str:
    digest=hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda:handle.read(8*1024*1024),b""): digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def load_sealed(path: Path, field: str) -> dict[str,Any]:
    value=json.loads(path.read_text(encoding="utf-8")); unsigned=dict(value); claimed=unsigned.pop(field,None)
    if claimed!=canonical_sha256(unsigned): raise ValueError(f"invalid {field}: {path}")
    return value


def validate_release_inputs(manifest_path: Path, llama_cpp: Path, cli: Path, q8: Path, f16: Path) -> tuple[dict[str,Any],str]:
    manifest=load_sealed(manifest_path,"manifest_sha256")
    if manifest.get("schema_version")!="ganesh-mini-release-artifacts/v1" or manifest.get("status")!="built" or manifest.get("model_name")!="ganesh-mini-1.0": raise ValueError("invalid release artifact manifest")
    llama=manifest.get("llama_cpp",{}); revision=subprocess.run(["git","rev-parse","HEAD"],cwd=llama_cpp,check=True,capture_output=True,text=True).stdout.strip()
    if revision!=llama.get("revision") or sha256(cli)!=llama.get("llama_cli_sha256"): raise ValueError("laptop runtime does not match the artifact build's pinned llama.cpp")
    for key,path in (("gguf_q8",q8),("gguf_f16",f16)):
        row=manifest.get("artifacts",{}).get(key,{})
        if not path.is_file() or path.stat().st_size!=row.get("bytes") or sha256(path)!=row.get("sha256"): raise ValueError(f"{key} does not match the release artifact manifest")
    return manifest,revision


def peak_rss(stderr: str, system: str) -> int | None:
    if system=="Darwin":
        match=re.search(r"^\s*(\d+)\s+maximum resident set size\s*$",stderr,re.MULTILINE)
        return int(match.group(1)) if match else None
    match=re.search(r"Maximum resident set size \(kbytes\):\s*(\d+)",stderr)
    return int(match.group(1))*1024 if match else None


def profile_ok(method: str, profile_bytes: int) -> tuple[bool,dict[str,Any]]:
    if method=="cgroup_v2":
        available=platform.system()=="Linux" and shutil.which("systemd-run") is not None and subprocess.run(["systemd-run","--version"],capture_output=True).returncode==0
        return available,{"method":method,"enforced_limit_bytes":profile_bytes,"launcher":"systemd-run --user --scope -p MemoryMax"}
    physical=int(subprocess.run(["sysctl","-n","hw.memsize"],check=True,capture_output=True,text=True).stdout) if platform.system()=="Darwin" else None
    return physical is not None and profile_bytes<=physical<=profile_bytes+512*1024**2,{"method":method,"observed_physical_memory_bytes":physical}


def run_profile(name: str, model: Path, limit: int, cli: Path, timeout: int, method: str) -> dict[str,Any]:
    system=platform.system(); profile_bytes=8*GIB if name=="q8" else 16*GIB; qualified,profile=profile_ok(method,profile_bytes); runs=[]; maximum=0
    time_prefix=["/usr/bin/time","-l"] if system=="Darwin" else ["/usr/bin/time","-v"]
    for prompt in PROMPTS:
        command=time_prefix+[str(cli),"-m",str(model),"-p",prompt,"-n","96","-c","8192","--temp","0","--seed","0","-ngl","999","--no-display-prompt","--no-warmup","-cnv","-st","--chat-template-kwargs",'{"enable_thinking":false}',"--reasoning","off"]
        if method=="cgroup_v2": command=["systemd-run","--user","--scope","--quiet","--wait","--pipe",f"-pMemoryMax={profile_bytes}"]+command
        started=time.monotonic()
        try:
            result=subprocess.run(command,text=True,capture_output=True,timeout=timeout,check=False); timed_out=False
        except subprocess.TimeoutExpired as exc:
            result=type("Result",(),{"returncode":None,"stdout":exc.stdout or "","stderr":exc.stderr or ""})(); timed_out=True
        rss=peak_rss(result.stderr,system); maximum=max(maximum,rss or 0); runs.append({"prompt_sha256":hashlib.sha256(prompt.encode()).hexdigest(),"command":command,"returncode":result.returncode,"timed_out":timed_out,"wall_seconds":time.monotonic()-started,"peak_rss_bytes":rss,"stdout":result.stdout,"stderr":result.stderr})
    passed=qualified and all(row["returncode"]==0 and not row["timed_out"] and row["peak_rss_bytes"] is not None for row in runs) and maximum<=limit
    return {"passed":passed,"profile":profile,"artifact":{"path":str(model),"bytes":model.stat().st_size,"sha256":sha256(model)},"context_length":8192,"peak_rss_bytes":maximum,"maximum_peak_rss_bytes":limit,"runs":runs}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--artifact-manifest",type=Path,required=True); parser.add_argument("--llama-cpp",type=Path,default=Path("models/llama.cpp")); parser.add_argument("--llama-cli",type=Path,required=True); parser.add_argument("--q8",type=Path,required=True); parser.add_argument("--f16",type=Path,required=True); parser.add_argument("--profile-method",choices=("actual_machine","cgroup_v2"),required=True); parser.add_argument("--timeout-seconds",type=int,default=300); parser.add_argument("--output",type=Path,required=True); args=parser.parse_args()
    manifest,revision=validate_release_inputs(args.artifact_manifest,args.llama_cpp,args.llama_cli,args.q8,args.f16)
    value={"schema_version":"ganesh-mini-laptop-certification/v1","artifact_manifest_sha256":manifest["manifest_sha256"],"llama_cpp_revision":revision,"llama_cli_sha256":sha256(args.llama_cli),"host":{"system":platform.system(),"release":platform.release(),"machine":platform.machine()},"profiles":{"q8":run_profile("q8",args.q8,7*GIB,args.llama_cli,args.timeout_seconds,args.profile_method),"f16":run_profile("f16",args.f16,14*GIB,args.llama_cli,args.timeout_seconds,args.profile_method)}}; value["status"]="passed" if all(item["passed"] for item in value["profiles"].values()) else "failed"; value["evidence_sha256"]=canonical_sha256(value); args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(value,indent=2,sort_keys=True)+"\n"); return 0 if value["status"]=="passed" else 2


if __name__=="__main__": raise SystemExit(main())
