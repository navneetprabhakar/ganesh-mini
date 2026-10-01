#!/usr/bin/env python3
"""Merge a qualified adapter and produce sealed BF16, GGUF F16, and GGUF Q8 artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from scripts.model.gate0 import validate_local_files


QWEN_MODEL_ID = "Qwen/Qwen3.5-2B"
QWEN_REVISION = "15852e8c16360a2fea060d615a32b45270f8a8fc"
GGUF_TARGET_FLAGS = ("--no-mtp",)


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def sha256(path: Path) -> str:
    digest=hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda:handle.read(8*1024*1024),b""): digest.update(chunk)
    return digest.hexdigest()


def inventory(root: Path) -> list[dict[str,Any]]:
    return [{"path":str(path.relative_to(root)),"bytes":path.stat().st_size,"sha256":sha256(path)} for path in sorted(root.rglob("*")) if path.is_file()]


def load_sealed(path: Path, field: str, label: str) -> dict[str,Any]:
    value=json.loads(path.read_text()); claimed=value.pop(field,None)
    if claimed!=canonical_sha256(value): raise ValueError(f"invalid {label} seal")
    value[field]=claimed; return value


def validate_base_model(base_model: Path, inventory_path: Path, readiness_path: Path) -> dict[str,Any]:
    inventory_value=json.loads(inventory_path.read_text())
    readiness=load_sealed(readiness_path,"report_sha256","Gate 0 readiness")
    inventory_sha=canonical_sha256(inventory_value)
    if (
        readiness.get("status")!="ready"
        or readiness.get("failed_checks")!=[]
        or readiness.get("model_id")!=QWEN_MODEL_ID
        or readiness.get("revision")!=QWEN_REVISION
        or readiness.get("inventory_sha256")!=inventory_sha
        or inventory_value.get("model_id")!=QWEN_MODEL_ID
        or inventory_value.get("revision")!=QWEN_REVISION
    ):
        raise ValueError("base model readiness or inventory identity mismatch")
    checks=validate_local_files(base_model,inventory_value)
    failed=[row["path"] for row in checks if row.get("passed") is not True]
    if failed: raise ValueError(f"base model files do not match pinned inventory: {failed}")
    files=[{"path":row["path"],"bytes":(base_model/row["path"]).stat().st_size,"sha256":sha256(base_model/row["path"])} for row in inventory_value["files"]]
    return {
        "model_id":QWEN_MODEL_ID,"revision":QWEN_REVISION,
        "inventory_sha256":inventory_sha,"readiness_report_sha256":readiness["report_sha256"],
        "artifact_sha256":canonical_sha256(files),
    }


def validate_selected_run(path: Path, adapter: Path) -> dict[str,Any]:
    selected=load_sealed(path,"evidence_sha256","selected-run evidence")
    if (
        selected.get("schema_version")!="ganesh-mini-sft-run/v2"
        or selected.get("status")!="complete"
        or selected.get("identities",{}).get("model_revision")!=QWEN_REVISION
        or selected.get("save_reload",{}).get("passed") is not True
    ): raise ValueError("only a complete repaired-recipe selected run may be merged")
    observed_adapter={str(file.relative_to(adapter)):sha256(file) for file in sorted(adapter.rglob("*")) if file.is_file()}
    if observed_adapter!=selected.get("adapter_files"): raise ValueError("adapter files do not match selected-run evidence")
    return selected


def save_optional_processor(processor_class: Any, base_model: Path, merged: Path) -> bool:
    """Copy vision processor metadata only when its optional backends exist.

    The release serving contract is text-only. The tokenizer is mandatory and
    saved separately; missing Pillow/torchvision must not invalidate a merge.
    """
    try:
        processor_class.from_pretrained(base_model, local_files_only=True).save_pretrained(merged)
    except (ImportError, OSError, ValueError):
        return False
    return True


def build(args: argparse.Namespace) -> dict[str,Any]:
    selected=validate_selected_run(args.selected_run_evidence,args.adapter)
    base_identity=validate_base_model(args.base_model,args.base_inventory,args.gate0_readiness)
    llama_matrix=json.loads(args.llama_matrix.read_text())
    observed_revision=subprocess.run(["git","rev-parse","HEAD"],cwd=args.llama_cpp,check=True,capture_output=True,text=True).stdout.strip()
    if observed_revision!=llama_matrix["llama_cpp"]["revision"]: raise ValueError("llama.cpp revision mismatch")
    converter=args.llama_cpp/"convert_hf_to_gguf.py"; quantizer=args.llama_cpp/"build/bin/llama-quantize"; llama_cli=args.llama_cpp/"build/bin/llama-cli"; gate0=load_sealed(args.gate0_gguf_evidence,"evidence_sha256","Gate 0 GGUF evidence")
    if (
        gate0.get("passed") is not True or gate0.get("model_id")!=QWEN_MODEL_ID
        or gate0.get("revision")!=QWEN_REVISION or gate0.get("llama_cpp_revision")!=observed_revision
        or sha256(converter)!=gate0["converter_sha256"] or sha256(quantizer)!=gate0["quantizer_sha256"]
        or sha256(llama_cli)!=gate0["llama_cli_sha256"]
    ): raise ValueError("llama.cpp tool or Gate 0 GGUF identity mismatch")
    if args.output.exists(): raise FileExistsError("release output must be fresh")
    import torch
    from peft import PeftModel
    from transformers import AutoModelForImageTextToText,AutoProcessor,AutoTokenizer
    args.output.mkdir(parents=True); merged=args.output/"ganesh-mini-1.0-bf16-hf"; f16=args.output/"ganesh-mini-1.0-f16.gguf"; q8=args.output/"ganesh-mini-1.0-q8_0.gguf"
    base_license=args.base_model/"LICENSE"
    if not base_license.is_file(): raise FileNotFoundError("pinned base LICENSE is missing")
    base=AutoModelForImageTextToText.from_pretrained(args.base_model,local_files_only=True,dtype=torch.bfloat16,device_map="cpu"); model=PeftModel.from_pretrained(base,args.adapter).merge_and_unload(safe_merge=True); model.save_pretrained(merged,safe_serialization=True,max_shard_size="4GB"); AutoTokenizer.from_pretrained(args.base_model,local_files_only=True).save_pretrained(merged); shutil.copyfile(base_license,merged/"LICENSE")
    save_optional_processor(AutoProcessor,args.base_model,merged)
    # PEFT's merged inference checkpoint omits the untouched speculative MTP
    # head. The target GGUF must not advertise a 25th decoder block.
    subprocess.run([sys.executable,str(converter),str(merged),"--outfile",str(f16),"--outtype","f16",*GGUF_TARGET_FLAGS],check=True)
    subprocess.run([str(quantizer),str(f16),str(q8),"Q8_0"],check=True)
    merged_files=inventory(merged)
    artifacts={"merged_bf16_hf":{"path":str(merged),"sha256":canonical_sha256(merged_files),"files":merged_files},"gguf_f16":{"path":str(f16),"bytes":f16.stat().st_size,"sha256":sha256(f16)},"gguf_q8":{"path":str(q8),"bytes":q8.stat().st_size,"sha256":sha256(q8)}}
    report={"schema_version":"ganesh-mini-release-artifacts/v1","status":"built","model_name":"ganesh-mini-1.0","base_model":base_identity,"selected_run_evidence_sha256":selected["evidence_sha256"],"llama_cpp":{"revision":observed_revision,"converter_sha256":sha256(converter),"quantizer_sha256":sha256(quantizer),"llama_cli_sha256":sha256(llama_cli),"target_conversion_flags":list(GGUF_TARGET_FLAGS)},"artifacts":artifacts}; report["manifest_sha256"]=canonical_sha256(report); (args.output/"manifest.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n"); return report


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--base-model",type=Path,required=True); parser.add_argument("--base-inventory",type=Path,default=Path("configs/model/qwen3_5_2b.inventory.json")); parser.add_argument("--gate0-readiness",type=Path,default=Path("measurement/gate0/readiness.json")); parser.add_argument("--adapter",type=Path,required=True); parser.add_argument("--selected-run-evidence",type=Path,required=True); parser.add_argument("--llama-cpp",type=Path,default=Path("models/llama.cpp")); parser.add_argument("--llama-matrix",type=Path,default=Path("configs/model/gate0_apple_matrix.json")); parser.add_argument("--gate0-gguf-evidence",type=Path,default=Path("measurement/gate0/gguf.json")); parser.add_argument("--output",type=Path,required=True); args=parser.parse_args(); build(args); return 0


if __name__=="__main__": raise SystemExit(main())
