#!/usr/bin/env python3
"""Merge a qualified adapter and produce sealed BF16, GGUF F16, and GGUF Q8 artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def sha256(path: Path) -> str:
    digest=hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda:handle.read(8*1024*1024),b""): digest.update(chunk)
    return digest.hexdigest()


def inventory(root: Path) -> list[dict[str,Any]]:
    return [{"path":str(path.relative_to(root)),"bytes":path.stat().st_size,"sha256":sha256(path)} for path in sorted(root.rglob("*")) if path.is_file()]


def load_sealed(path: Path) -> dict[str,Any]:
    value=json.loads(path.read_text()); claimed=value.pop("evidence_sha256",None)
    if claimed!=canonical_sha256(value): raise ValueError("invalid selected-run evidence seal")
    value["evidence_sha256"]=claimed; return value


def build(args: argparse.Namespace) -> dict[str,Any]:
    import torch
    from peft import PeftModel
    from transformers import AutoModelForImageTextToText,AutoProcessor,AutoTokenizer
    selected=load_sealed(args.selected_run_evidence)
    if selected.get("status")!="complete": raise ValueError("only a complete selected run may be merged")
    observed_adapter={str(path.relative_to(args.adapter)):sha256(path) for path in sorted(args.adapter.rglob("*")) if path.is_file()}
    if observed_adapter!=selected.get("adapter_files"): raise ValueError("adapter files do not match selected-run evidence")
    llama_matrix=json.loads(args.llama_matrix.read_text())
    observed_revision=subprocess.run(["git","rev-parse","HEAD"],cwd=args.llama_cpp,check=True,capture_output=True,text=True).stdout.strip()
    if observed_revision!=llama_matrix["llama_cpp"]["revision"]: raise ValueError("llama.cpp revision mismatch")
    converter=args.llama_cpp/"convert_hf_to_gguf.py"; quantizer=args.llama_cpp/"build/bin/llama-quantize"; gate0=json.loads(args.gate0_gguf_evidence.read_text())
    if sha256(converter)!=gate0["converter_sha256"] or sha256(quantizer)!=gate0["quantizer_sha256"]: raise ValueError("llama.cpp tool hash mismatch")
    if args.output.exists(): raise FileExistsError("release output must be fresh")
    args.output.mkdir(parents=True); merged=args.output/"ganesh-mini-1.0-bf16-hf"; f16=args.output/"ganesh-mini-1.0-f16.gguf"; q8=args.output/"ganesh-mini-1.0-q8_0.gguf"
    base=AutoModelForImageTextToText.from_pretrained(args.base_model,local_files_only=True,dtype=torch.bfloat16,device_map="cpu"); model=PeftModel.from_pretrained(base,args.adapter).merge_and_unload(safe_merge=True); model.save_pretrained(merged,safe_serialization=True,max_shard_size="4GB"); AutoTokenizer.from_pretrained(args.base_model,local_files_only=True).save_pretrained(merged)
    try: AutoProcessor.from_pretrained(args.base_model,local_files_only=True).save_pretrained(merged)
    except (ValueError,OSError): pass
    subprocess.run([sys.executable,str(converter),str(merged),"--outfile",str(f16),"--outtype","f16"],check=True)
    subprocess.run([str(quantizer),str(f16),str(q8),"Q8_0"],check=True)
    merged_files=inventory(merged)
    artifacts={"merged_bf16_hf":{"path":str(merged),"sha256":canonical_sha256(merged_files),"files":merged_files},"gguf_f16":{"path":str(f16),"bytes":f16.stat().st_size,"sha256":sha256(f16)},"gguf_q8":{"path":str(q8),"bytes":q8.stat().st_size,"sha256":sha256(q8)}}
    report={"schema_version":"ganesh-mini-release-artifacts/v1","status":"built","model_name":"ganesh-mini-1.0","selected_run_evidence_sha256":selected["evidence_sha256"],"llama_cpp":{"revision":observed_revision,"converter_sha256":sha256(converter),"quantizer_sha256":sha256(quantizer)},"artifacts":artifacts}; report["manifest_sha256"]=canonical_sha256(report); (args.output/"manifest.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n"); return report


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--base-model",type=Path,required=True); parser.add_argument("--adapter",type=Path,required=True); parser.add_argument("--selected-run-evidence",type=Path,required=True); parser.add_argument("--llama-cpp",type=Path,default=Path("models/llama.cpp")); parser.add_argument("--llama-matrix",type=Path,default=Path("configs/model/gate0_apple_matrix.json")); parser.add_argument("--gate0-gguf-evidence",type=Path,default=Path("measurement/gate0/gguf.json")); parser.add_argument("--output",type=Path,required=True); args=parser.parse_args(); build(args); return 0


if __name__=="__main__": raise SystemExit(main())
