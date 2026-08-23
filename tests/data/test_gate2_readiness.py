from pathlib import Path

from scripts.data.build_gate2_readiness import build, verify_seal


ROOT=Path(__file__).resolve().parents[2]


def test_gate2_is_bound_to_overlap_compatibility_and_seed_bytes() -> None:
    report=build(ROOT,ROOT/"manifests/datasets/ganesh_v01_seed.json")
    assert report["status"]=="ready"
    assert report["evaluation_overlap_passed"] and report["compatibility_passed"]
    assert verify_seal(report,"report_sha256")
