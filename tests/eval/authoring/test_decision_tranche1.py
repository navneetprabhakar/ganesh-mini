import pytest

from scripts.eval.authoring.build_decision_tranche1 import (
    BEHAVIOR,
    CASES,
    DEVELOPMENT_MANIFESTS,
    ROOT,
    SEED_PATHS,
    SLUGS,
    build,
)
from scripts.eval.contracts import load_json, sha256_object, validate_task
from scripts.verify.sandbox import SANDBOX_CONTRACT


def test_decision_tranche1_contract_balance_hashes_and_explicit_separation() -> None:
    manifest, overlap = build()
    assert manifest["surface"] == "decision"
    assert manifest["status"] == "authored-unexecuted"
    assert manifest["task_count"] == 60
    assert all(counts == {"generation": 5, "repair": 5} for counts in manifest["counts_by_lane"].values())
    assert sum(counts["generation"] for counts in manifest["counts_by_lane"].values()) == 30
    assert sum(counts["repair"] for counts in manifest["counts_by_lane"].values()) == 30
    assert overlap["comparison_inputs"] == {
        "seed_jsonl": list(SEED_PATHS),
        "private_development_manifests": list(DEVELOPMENT_MANIFESTS),
    }
    assert overlap["seed_records_inspected"] == 1449
    assert overlap["private_development_prompts_inspected"] == 180
    assert overlap["comparison_prompts_inspected"] == 1629
    assert overlap["exact_prompt_overlaps"] == overlap["normalized_prompt_overlaps"] == []
    assert overlap["within_tranche_exact_overlaps"] == overlap["within_tranche_normalized_overlaps"] == []
    assert overlap["evaluation_manifest_sha256"] == manifest["manifest_sha256"]
    assert len({entry["task_id"] for entry in manifest["tasks"]}) == 60
    assert all(sum(entry["language"] == lane for entry in manifest["tasks"]) == 10 for lane in manifest["counts_by_lane"])
    assert all(len(cases) >= 6 for cases in CASES.values())
    assert "9223372036854775807" in BEHAVIOR["api-token-validation"]
    assert "2147483647" in BEHAVIOR["circuit-trace"]
    assert "-9223372036854775808..9223372036854775807" in BEHAVIOR["bounded-window-rollup"]
    assert "Values may contain =" in BEHAVIOR["tag-patch"]
    assert "9223372036854775807" in BEHAVIOR["version-compaction"]
    assert all(any(slug in entry["task_id"] for slug in SLUGS) for entry in manifest["tasks"])
    for entry in manifest["tasks"]:
        task = validate_task(load_json(ROOT / entry["path"]))
        assert sha256_object(task) == entry["sha256"]
        assert task["prompt"]["sha256"] == entry["prompt_sha256"]
        assert task["limits"]["timeout_seconds"] == (60 if task["language"] in {"go", "java", "rust"} else 30)
        prompt = task["prompt"]["text"]
        assert all(marker in prompt for marker in ("File contract:", "Required API:", "Behavior:", "Visible example:", "Return only the complete source file"))
        if task["task_type"] == "repair":
            assert "Buggy source to repair:" in prompt
            assert task["validation"]["known_bad"][0]["code"] in prompt


def test_executed_directionality_evidence_is_complete_and_bound() -> None:
    evidence_path = ROOT / "manifests/evaluation/private/decision-tranche1-directionality.json"
    if not evidence_path.exists():
        pytest.skip("directionality waits for regenerated cross-tranche overlap seal")
    evidence = load_json(evidence_path)
    if evidence["executions"][0]["verifier"]["sandbox_contract_sha256"] != sha256_object(SANDBOX_CONTRACT):
        pytest.skip("archived ARM64 directionality is intentionally non-current")
    claimed = evidence.pop("evidence_sha256")
    assert sha256_object(evidence) == claimed
    assert evidence["status"] == "passed"
    assert evidence["execution_mode"] == "sequential"
    assert evidence["evaluation_manifest_sha256"] == "4202928ddd2168fed9bb331c027244cce538a1c14f71b3fa7cf842f7698ca110"
    assert evidence["cross_tranche_overlap_report"] == "manifests/evaluation/private/decision-tranches1-2-cross-overlap.json"
    assert evidence["cross_tranche_overlap_report_sha256"] == "2c9d3dd4c91b846f95adf437c79ae6d52543e030d5a35a6317b828ba42116cf3"
    assert evidence["task_count"] == 60
    assert evidence["execution_count"] == 120
    assert evidence["reference_passes"] == 60
    assert evidence["known_bad_rejections"] == 60
    assert evidence["failures"] == []
    assert all("@sha256:" in row["verifier"]["image"] and not row["verifier"]["timed_out"] for row in evidence["executions"])
