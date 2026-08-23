import hashlib
import json
import subprocess
from pathlib import Path

from scripts.model.provision_ganesh_v01 import provision


def test_provision_uses_only_pinned_git_objects(tmp_path: Path) -> None:
    source=tmp_path/"source"; source.mkdir(); subprocess.run(["git","init","-q"],cwd=source,check=True)
    adapters={}
    for lane in ("go","java","javascript","typescript","python"):
        directory=source/"outputs/hf_release/ganesh-v1/adapters"/lane; directory.mkdir(parents=True)
        config=f'{{"lane":"{lane}"}}\n'.encode(); weights=f"weights-{lane}".encode(); (directory/"adapter_config.json").write_bytes(config); (directory/"adapter_model.safetensors").write_bytes(weights)
        adapters[lane]={"config_sha256":hashlib.sha256(config).hexdigest(),"weights_sha256":hashlib.sha256(weights).hexdigest()}
    release=b'{"release":"test"}\n'; release_path=source/"outputs/hf_release/ganesh-v1/release_manifest.json"; release_path.write_bytes(release)
    subprocess.run(["git","add","."],cwd=source,check=True); subprocess.run(["git","-c","user.name=Test","-c","user.email=test@example.com","commit","-qm","fixture"],cwd=source,check=True); revision=subprocess.run(["git","rev-parse","HEAD"],cwd=source,check=True,capture_output=True,text=True).stdout.strip()
    contract={"reference_name":"ganesh-v0.1","source_revision":revision,"release_manifest_path":"outputs/hf_release/ganesh-v1/release_manifest.json","release_manifest_sha256":hashlib.sha256(release).hexdigest(),"routing":{"rust":"base_unadapted"},"adapters":adapters}; contract_path=tmp_path/"contract.json"; contract_path.write_text(json.dumps(contract))
    output=tmp_path/"output"; manifest=provision(source,contract_path,output)
    assert manifest["status"]=="provisioned" and len(manifest["files"])==11
    assert (output/"adapters/python/adapter_model.safetensors").read_bytes()==b"weights-python"
