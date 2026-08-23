import json
from pathlib import Path

import pytest

from scripts.cuda.verify_absence_proof import canonical_sha256, main


def make_scope(tmp_path: Path, nonempty: bool = False) -> Path:
    resources = [
        {"kind": "instance", "name": "vm", "id": "1"},
        {"kind": "disk", "name": "disk", "id": "2"},
        {"kind": "network", "name": "net", "id": "3"},
        {"kind": "subnet", "name": "subnet", "id": "4"},
    ]
    queries = []
    for kind in ("instance", "disk", "network", "subnet"):
        path = tmp_path / f"{kind}.json"
        path.write_text(json.dumps([{"name": "unexpected"}] if nonempty and kind == "disk" else []))
        location = ["--location=us-central1-a"] if kind in {"instance", "disk"} else ["--location=us-central1"] if kind == "subnet" else []
        queries.append({"kind": kind, "path": str(path), "command": ["gcloud", kind, "list", "--project=p", *location]})
    scope = {"schema_version": "ganesh-mini-gcloud-absence-scope/v1", "project": "p", "region": "us-central1", "zone": "us-central1-a", "run_id": "run", "expected_resources": resources, "queries": queries}
    path = tmp_path / "scope.json"; path.write_text(json.dumps(scope)); return path


def test_absence_proof_binds_scope_queries_and_hashes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    output = tmp_path / "proof.json"
    monkeypatch.setattr("sys.argv", ["proof", "--scope", str(make_scope(tmp_path)), "--output", str(output)])
    assert main() == 0
    proof = json.loads(output.read_text()); claimed = proof.pop("evidence_sha256")
    assert canonical_sha256(proof) == claimed
    assert proof["status"] == "passed" and len(proof["queries"]) == 4


def test_absence_proof_rejects_nonempty_query(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["proof", "--scope", str(make_scope(tmp_path, True)), "--output", str(tmp_path / "proof.json")])
    with pytest.raises(SystemExit, match="not empty"):
        main()
