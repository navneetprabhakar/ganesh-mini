import hashlib
import json
from pathlib import Path

import pytest

from scripts.inference.build_lane_stratified_probe_upload_plan import OBJECTS, build, canonical_sha256


def test_upload_plan_binds_exactly_four_local_objects(tmp_path: Path) -> None:
    for index, (relative, _) in enumerate(OBJECTS):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(f"object-{index}".encode())
    plan = build(tmp_path, "a" * 40)
    assert plan["status"] == "pending-explicit-gcloud-upload-approval"
    assert plan["object_count"] == 4
    assert plan["maximum_new_bytes"] == sum(len(f"object-{index}") for index in range(4))
    assert all(row["destination"].startswith("gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/lane-stratified-probe-v3/input/aaaaaaaa/") for row in plan["objects"])
    assert all(row["sha256"] == hashlib.sha256((tmp_path / row["source"]).read_bytes()).hexdigest() for row in plan["objects"])
    claimed = plan.pop("upload_plan_sha256")
    assert claimed == canonical_sha256(plan)


def test_upload_plan_rejects_missing_inputs_or_unsealed_commit(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="full lowercase Git SHA"):
        build(tmp_path, "HEAD")
    with pytest.raises(ValueError, match="upload input is missing"):
        build(tmp_path, "b" * 40)


def test_repository_upload_inputs_match_declared_workspace_hashes() -> None:
    root = Path(__file__).resolve().parents[2]
    plan = build(root, "c" * 40)
    by_source = {row["source"]: row for row in plan["objects"]}
    train_manifest = json.loads((root / "artifacts/train/workspaces/expansion-lane-stratified-probe-v3.manifest.json").read_text())
    eval_manifest = json.loads((root / "artifacts/eval/workspaces/development-v7.manifest.json").read_text())
    assert by_source["artifacts/train/workspaces/expansion-lane-stratified-probe-v3.tar.gz"]["sha256"] == train_manifest["archive_sha256"]
    assert by_source["artifacts/eval/workspaces/development-v7.tar.gz"]["sha256"] == eval_manifest["archive"]["sha256"]
