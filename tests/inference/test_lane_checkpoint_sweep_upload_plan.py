import json
from pathlib import Path

from scripts.inference.build_lane_checkpoint_sweep_upload_plan import OBJECTS, build, canonical_sha256, file_sha256


ROOT = Path(__file__).resolve().parents[2]


def test_upload_plan_binds_all_inputs_and_forbids_compute() -> None:
    source_commit = "8ddeae14304d195a2f83e4df8e2c691055edb712"
    plan = build(ROOT, source_commit)

    assert plan["status"] == "pending-explicit-gcloud-upload-approval"
    assert plan["object_count"] == 6
    assert plan["maximum_new_bytes"] == sum(row["size_bytes"] for row in plan["objects"])
    assert "inspect, create, start, stop, mutate, or delete compute and network resources" in plan["forbidden_operations"]
    assert plan["upload_plan_sha256"] == canonical_sha256({
        key: value for key, value in plan.items() if key != "upload_plan_sha256"
    })
    for row, (relative, name) in zip(plan["objects"], OBJECTS, strict=True):
        source = ROOT / relative
        assert row["size_bytes"] == source.stat().st_size
        assert row["sha256"] == file_sha256(source)
        assert row["destination"].endswith(f"/{name}")
        assert "/input/8ddeae14/" in row["destination"]


def test_sealed_repository_plan_matches_builder() -> None:
    path = ROOT / "measurement/gate4/lane-stratified-probe-checkpoint-sweep-20260910/gcloud-upload-plan.json"
    plan = json.loads(path.read_text())

    assert plan == build(ROOT, plan["source_commit"])
