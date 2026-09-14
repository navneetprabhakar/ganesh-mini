import json
from pathlib import Path

from scripts.inference.build_gradient_conflict_probe_readonly_plan import REUSED_INPUTS, UPLOADED_INPUTS, build, canonical_sha256


def seal(path: Path, value: dict, field: str) -> None:
    value[field] = canonical_sha256(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


def test_readonly_plan_binds_uploaded_and_reused_generations(tmp_path: Path) -> None:
    objects = []
    for index, name in enumerate(UPLOADED_INPUTS):
        objects.append({"destination": f"gs://bucket/prefix/{name}", "generation_uri": f"gs://bucket/prefix/{name}#{index+1}", "sha256": f"{index+1:064x}", "size_bytes": index+1, "byte_identical": True})
    receipt_path = tmp_path / "receipt.json"
    seal(receipt_path, {"schema_version": "ganesh-mini-gradient-conflict-probe-gcloud-upload-receipt/v1", "status": "complete-exact-generation-roundtrip-verified", "objects": objects}, "receipt_sha256")
    prior_path = tmp_path / "prior.json"
    prior_inputs = {name: {"generation_uri": f"gs://bucket/{name}#1", "sha256": "a" * 64, "size_bytes": 1} for name in REUSED_INPUTS}
    seal(prior_path, {"status": "complete-ready-for-separate-proposal", "inputs": prior_inputs}, "report_sha256")
    plan = build(receipt_path, prior_path)
    assert plan["status"] == "pending-explicit-gcloud-readonly-approval"
    assert len(plan["inputs"]) == 10
    assert plan["inputs"]["controller"]["generation_uri"].endswith("startup-controller.sh#5")
    claimed = plan.pop("inspection_plan_sha256")
    assert claimed == canonical_sha256(plan)


def test_readonly_plan_supports_fresh_attempt_identity(tmp_path: Path) -> None:
    objects = []
    for index, name in enumerate(UPLOADED_INPUTS):
        objects.append({"destination": f"gs://bucket/prefix/{name}", "generation_uri": f"gs://bucket/prefix/{name}#{index+1}", "sha256": f"{index+1:064x}", "size_bytes": index+1, "byte_identical": True})
    receipt_path = tmp_path / "receipt.json"
    seal(receipt_path, {"schema_version": "ganesh-mini-gradient-conflict-probe-gcloud-upload-receipt/v1", "status": "complete-exact-generation-roundtrip-verified", "objects": objects}, "receipt_sha256")
    prior_path = tmp_path / "prior.json"
    prior_inputs = {name: {"generation_uri": f"gs://bucket/{name}#1", "sha256": "a" * 64, "size_bytes": 1} for name in REUSED_INPUTS}
    seal(prior_path, {"status": "complete-ready-for-separate-proposal", "inputs": prior_inputs}, "report_sha256")

    plan = build(receipt_path, prior_path, "20260914T003000Z")

    assert plan["planned_attempt_id"] == "20260914T003000Z"
    assert plan["planned_resource_names"]["instance"] == "ganesh-mini-g4-grad-20260914t003000z"
