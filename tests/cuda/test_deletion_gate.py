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
    resource=tmp_path/"resource.json"; resource.write_text(json.dumps({"name":"vm","id":"1","status":status}))
    for name,path in {"runtime-files.sha256":inventory,"provider/serial-port.log":serial,"provider/operations.json":operations,"provider/system-events.json":events,"provider/resource-terminated.json":resource}.items():
        rows.append({"object_uri":f"{prefix}/{name}","downloaded_sha256":sha(path),"verified":True})
    manifest={"schema_version":"ganesh-mini-gcs-backup-manifest/v1","status":"verified","project":"p","prefix":prefix,"object_count":len(rows),"objects":rows}; manifest["evidence_sha256"]=canonical_sha256(manifest)
    manifest_path=tmp_path/"manifest.json"; manifest_path.write_text(json.dumps(manifest))
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


def test_deletion_gate_records_explicit_provider_serial_unavailable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    argv,output=write_inputs(tmp_path,"runtime")
    manifest_path=Path(argv[argv.index("--backup-manifest")+1])
    manifest=json.loads(manifest_path.read_text()); prefix=manifest["prefix"]
    unavailable=tmp_path/"serial-unavailable.txt"; unavailable.write_text("provider returned resource not ready\n")
    row=next(row for row in manifest["objects"] if row["object_uri"].endswith("/provider/serial-port.log"))
    row["object_uri"]=f"{prefix}/provider/serial-port-unavailable.txt"; row["downloaded_sha256"]=sha(unavailable)
    manifest.pop("evidence_sha256"); manifest["evidence_sha256"]=canonical_sha256(manifest); manifest_path.write_text(json.dumps(manifest))
    index=argv.index("--serial-evidence"); argv[index:index+2]=["--serial-unavailable-evidence",str(unavailable)]
    monkeypatch.setattr("sys.argv",argv)
    assert main()==0
    assert json.loads(output.read_text())["provider_serial_status"]=="provider-unavailable-recorded"


def test_deletion_gate_accepts_gate1_phase_with_the_same_exact_backup_contract(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    argv, output = write_inputs(tmp_path, "gate1-baseline")
    monkeypatch.setattr("sys.argv", argv)
    assert main() == 0
    assert json.loads(output.read_text())["phase"] == "gate1-baseline"


def test_quarantine_deletion_gate_allows_teardown_but_forbids_admission_on_bad_inventory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    argv, output = write_inputs(tmp_path, "gate1-baseline")
    inventory = Path(argv[argv.index("--inventory") + 1])
    inventory.write_text(inventory.read_text().replace("startup.stdout.log", "wrong-name.log"))
    manifest_path = Path(argv[argv.index("--backup-manifest") + 1])
    manifest = json.loads(manifest_path.read_text())
    inventory_row = next(row for row in manifest["objects"] if row["object_uri"].endswith("/runtime-files.sha256"))
    inventory_row["downloaded_sha256"] = sha(inventory)
    manifest.pop("evidence_sha256")
    manifest["evidence_sha256"] = canonical_sha256(manifest)
    manifest_path.write_text(json.dumps(manifest))
    argv.extend(["--integrity-mode", "quarantine"])
    monkeypatch.setattr("sys.argv", argv)
    assert main() == 0
    evidence = json.loads(output.read_text())
    assert evidence["integrity_mode"] == "quarantine"
    assert evidence["admission_eligible"] is False
