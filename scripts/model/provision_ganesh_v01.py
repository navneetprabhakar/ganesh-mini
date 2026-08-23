#!/usr/bin/env python3
"""Materialize the exact Ganesh v0.1 release adapters from pinned Git objects."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_blob(repository: Path, revision: str, path: str) -> bytes:
    return subprocess.run(["git","show",f"{revision}:{path}"],cwd=repository,check=True,stdout=subprocess.PIPE).stdout


def provision(repository: Path, contract_path: Path, output: Path) -> dict[str,Any]:
    contract=json.loads(contract_path.read_text()); revision=contract["source_revision"]
    observed=subprocess.run(["git","rev-parse",revision],cwd=repository,check=True,capture_output=True,text=True).stdout.strip()
    if observed!=revision: raise ValueError("source revision is not exact")
    release=git_blob(repository,revision,contract["release_manifest_path"])
    if sha256_bytes(release)!=contract["release_manifest_sha256"]: raise ValueError("release manifest hash mismatch")
    temporary=output.with_name(f".{output.name}.{os.getpid()}.tmp")
    if output.exists() or temporary.exists(): raise FileExistsError("provision destination must be fresh")
    temporary.mkdir(parents=True); files=[]
    try:
        (temporary/"release_manifest.json").write_bytes(release)
        files.append({"path":"release_manifest.json","size":len(release),"sha256":sha256_bytes(release)})
        if contract.get("base_model_manifest_path"):
            base_manifest=git_blob(repository,revision,contract["base_model_manifest_path"])
            if sha256_bytes(base_manifest)!=contract["base_model_manifest_sha256"]: raise ValueError("base model manifest hash mismatch")
            (temporary/"base_model_manifest.json").write_bytes(base_manifest); files.append({"path":"base_model_manifest.json","size":len(base_manifest),"sha256":sha256_bytes(base_manifest),"source_path":contract["base_model_manifest_path"]})
        for lane,expected in contract["adapters"].items():
            lane_dir=temporary/"adapters"/lane; lane_dir.mkdir(parents=True)
            for filename,key in (("adapter_config.json","config_sha256"),("adapter_model.safetensors","weights_sha256")):
                source=f"outputs/hf_release/ganesh-v1/adapters/{lane}/{filename}"; content=git_blob(repository,revision,source)
                if sha256_bytes(content)!=expected[key]: raise ValueError(f"{lane}/{filename} hash mismatch")
                target=lane_dir/filename; target.write_bytes(content); files.append({"path":str(target.relative_to(temporary)),"size":len(content),"sha256":sha256_bytes(content),"source_path":source})
        manifest={"schema_version":"ganesh-mini-reference-provision/v1","status":"provisioned","reference_name":contract["reference_name"],"source_revision":revision,"contract_sha256":sha256_bytes(contract_path.read_bytes()),"routing":contract["routing"],"files":files}; manifest["manifest_sha256"]=canonical_sha256(manifest); (temporary/"manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n"); os.replace(temporary,output); return manifest
    except BaseException:
        for path in sorted(temporary.rglob("*"),reverse=True):
            if path.is_file(): path.unlink()
            elif path.is_dir(): path.rmdir()
        if temporary.exists(): temporary.rmdir()
        raise


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--source-repository",type=Path,required=True); parser.add_argument("--contract",type=Path,default=Path("configs/model/ganesh_v01.contract.json")); parser.add_argument("--output",type=Path,default=Path("artifacts/reference/ganesh-v0.1")); args=parser.parse_args(); provision(args.source_repository.resolve(),args.contract.resolve(),args.output.resolve()); return 0


if __name__=="__main__": raise SystemExit(main())
