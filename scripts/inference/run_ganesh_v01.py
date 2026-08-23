#!/usr/bin/env python3
"""Run the exact Ganesh v0.1 lane-routed reference on a frozen evaluation config."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from pathlib import Path
from typing import Any

from scripts.eval.contracts import sha256_object
from scripts.inference.run_evaluation import TransformersBatchBackend,execute


def sha256(path: Path) -> str:
    digest=hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda:handle.read(8*1024*1024),b""): digest.update(chunk)
    return digest.hexdigest()


class GaneshV01Backend(TransformersBatchBackend):
    def __init__(self, base_dir: Path, provision_dir: Path, contract: dict[str,Any]) -> None:
        import torch
        from peft import PeftModel
        from transformers import AutoModelForImageTextToText,AutoTokenizer
        started=time.perf_counter(); self.torch=torch; self.device="cuda" if torch.cuda.is_available() else "cpu"; self.dtype=torch.bfloat16
        if self.device!="cuda": raise RuntimeError("Ganesh v0.1 12B reference requires CUDA")
        self.tokenizer=AutoTokenizer.from_pretrained(base_dir,local_files_only=True); self.tokenizer.padding_side="left"
        if self.tokenizer.pad_token_id is None: self.tokenizer.pad_token_id=self.tokenizer.eos_token_id
        base=AutoModelForImageTextToText.from_pretrained(base_dir,local_files_only=True,dtype=torch.bfloat16,device_map={"":0})
        self.model=PeftModel.from_pretrained(base,provision_dir/"adapters/go",adapter_name="go",is_trainable=False)
        for lane in ("java","javascript","typescript","python"): self.model.load_adapter(provision_dir/f"adapters/{lane}",adapter_name=lane,is_trainable=False)
        self.model.eval(); self._disabled=False; self.eos_token_id=int(self.tokenizer.eos_token_id); self.load_ms=round((time.perf_counter()-started)*1000)
        self.identity={"backend":"transformers-peft-lane-routed","python":platform.python_version(),"torch":torch.__version__,"device":self.device,"dtype":str(next(self.model.parameters()).dtype),"routing":contract["routing"]}

    def activate(self, lane: str) -> None:
        if lane=="rust":
            if not self._disabled: self.model.disable_adapter_layers(); self._disabled=True
        else:
            if self._disabled: self.model.enable_adapter_layers(); self._disabled=False
            self.model.set_adapter(lane)


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--config",type=Path,required=True); parser.add_argument("--contract",type=Path,default=Path("configs/model/ganesh_v01.contract.json")); parser.add_argument("--base-dir",type=Path,required=True); parser.add_argument("--provision-dir",type=Path,default=Path("artifacts/reference/ganesh-v0.1")); args=parser.parse_args()
    contract=json.loads(args.contract.read_text()); provision=json.loads((args.provision_dir/"manifest.json").read_text()); claimed=provision.pop("manifest_sha256",None)
    if claimed!=hashlib.sha256(json.dumps(provision,sort_keys=True,separators=(",", ":")).encode()).hexdigest() or provision.get("source_revision")!=contract["source_revision"]: raise ValueError("Ganesh v0.1 provision identity mismatch")
    base_manifest=json.loads((args.provision_dir/"base_model_manifest.json").read_text())
    for item in base_manifest["files"]:
        path=args.base_dir/item["path"]
        if not path.is_file() or path.stat().st_size!=item["bytes"] or sha256(path)!=item["sha256"]: raise ValueError(f"Ganesh v0.1 base file mismatch: {item['path']}")
    weights=args.base_dir/"model.safetensors"
    adapter_bytes=sum(path.stat().st_size for path in args.provision_dir.glob("adapters/**/*") if path.is_file()); artifact_size=sum(item["bytes"] for item in base_manifest["files"])+adapter_bytes
    artifact_sha=sha256_object({"base_weights_sha256":contract["base_model"]["weights_sha256"],"provision_manifest_sha256":claimed})
    identity={"model_id":"ganesh-v0.1","revision":contract["source_revision"],"artifact_sha256":artifact_sha,"serving_contract_sha256":sha256_object(contract["serving_contract"]),"base_model_id":contract["base_model"]["model_id"],"base_revision":contract["base_model"]["revision"]}
    backend=GaneshV01Backend(args.base_dir,args.provision_dir,contract); result=execute(args.config.resolve(),backend,identity,artifact_size); print(json.dumps(result["task_accounting"],sort_keys=True)); return 0 if result["task_accounting"]["pending"]==0 else 2


if __name__=="__main__": raise SystemExit(main())
