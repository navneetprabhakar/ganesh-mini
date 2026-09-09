from pathlib import Path

import pytest

from scripts.inference.build_capacity_probe_upload_plan import OBJECTS, build, canonical_sha256


def fixture(tmp_path: Path) -> Path:
    for index, (relative, _) in enumerate(OBJECTS):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(f"object-{index}".encode())
    return tmp_path


def test_plan_is_exactly_upload_only(tmp_path: Path) -> None:
    plan = build(fixture(tmp_path), "a" * 40)
    assert plan["object_count"] == 4
    assert plan["maximum_new_bytes"] == sum(row["size_bytes"] for row in plan["objects"])
    assert all(row["destination"].endswith((".tar.gz", ".json")) for row in plan["objects"])
    assert any("create-only" in operation for operation in plan["allowed_operations"])
    assert any("compute" in operation for operation in plan["forbidden_operations"])
    unsigned = {key: value for key, value in plan.items() if key != "upload_plan_sha256"}
    assert plan["upload_plan_sha256"] == canonical_sha256(unsigned)


def test_plan_rejects_missing_input(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="missing"):
        build(tmp_path, "a" * 40)
