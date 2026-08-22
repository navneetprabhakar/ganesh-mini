import hashlib
import json
from pathlib import Path

import pytest

from scripts.cuda.gcloud_backup_manifest import canonical_sha256
from scripts.cuda.verify_deletion_gate import main


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_inputs(tmp_path: Path, phase: str, status: str = "TERMINATED") -> tuple[list[str], Path]:
    prefix = f"gs://b/run/{phase}-terminal"
    inventory = tmp_path / "runtime-files.sha256"
    local = {"startup-exit-code.txt":b"0\n","startup.stdout.log":b"ok\n","startup.stderr.log":b"none\n"}
    if phase == "runtime": local["controller-exit-code.txt"] = b"0\n"
    inventory.write_text("".join(f"{hashlib.sha256(data).hexdigest()}  ./{name}\n" for name,data in local.items()))
    serial = tmp_path / "serial.log"; serial.write_text("serial\n")
    operations = tmp_path / "operations.json"; operations.write_text('{"items":[]}\n')
    events = tmp_path / "events.json"; events.write_text('{"events":[]}\n')
    rows = [{"object_uri":f"{prefix}/{name}","downloaded_sha256":hashlib.sha256(data).hexdigest(),"verified":True} for name,data in local.items()]
    for name,path in {"runtime-files.sha256":inventory,"provider/serial-port.log":serial,"provider/operations.json":operations,"provider/system-events.json":events}.items():
        rows.append({"object_uri":f"{prefix}/{name}","downloaded_sha256":sha(path),"verified":True})
    manifest={"schema_version":"ganesh-mini-gcs-backup-manifest/v1","status":"verified","project":"p","prefix":prefix,"object_count":len(rows),"objects":rows}; manifest["evidence_sha256"]=canonical_sha256(manifest)
    manifest_path=tmp_path/"manifest.json"; manifest_path.write_text(json.dumps(manifest))
    resource=tmp_path/"resource.json"; resource.write_text(json.dumps({"name":"vm","id":"1","status":status}))
    argv=["gate","--phase",phase,"--backup-manifest",str(manifest_path),"--resource-state",str(resource),"--inventory",str(inventory),"--serial-evidence",str(serial),"--operations-evidence",str(operations),"--system-events-evidence",str(events),"--expected-resource-name","vm","--expected-resource-id","1","--expected-prefix",prefix,"--output",str(tmp_path/"gate.json")]
    return argv,tmp_path/"gate.json"


def test_deletion_gate_requires_exact_inventory_provider_evidence_and_stopped_vm(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    argv,output=write_inputs(tmp_path,"runtime"); monkeypatch.setattr("sys.argv",argv)
    assert main()==0 and json.loads(output.read_text())["status"]=="passed"


def test_deletion_gate_rejects_running_vm(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    argv,_=write_inputs(tmp_path,"prebuild","RUNNING"); monkeypatch.setattr("sys.argv",argv)
    with pytest.raises(SystemExit,match="must be stopped"): main()


def test_deletion_gate_rejects_omitted_local_artifact(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    argv,_=write_inputs(tmp_path,"runtime"); inventory=Path(argv[argv.index("--inventory")+1]); inventory.write_text(inventory.read_text()+f"{'a'*64}  ./output/merged/model.safetensors\n"); monkeypatch.setattr("sys.argv",argv)
    with pytest.raises(SystemExit,match="inventory"): main()
