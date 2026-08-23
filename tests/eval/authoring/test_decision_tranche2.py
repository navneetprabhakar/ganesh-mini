import pytest

from scripts.eval.authoring.build_decision_tranche2 import ROOT, build
from scripts.eval.contracts import load_json, sha256_object, validate_task
from scripts.verify.sandbox import SANDBOX_CONTRACT


def test_decision_tranche2_contract_balance_hashes_and_separation() -> None:
    manifest, overlap = build()
    assert manifest["surface"] == "decision" and manifest["task_count"] == 60
    assert all(x == {"generation": 5, "repair": 5} for x in manifest["counts_by_lane"].values())
    assert overlap["seed_records_inspected"] == 1449
    assert overlap["private_development_prompts_inspected"] == 180
    assert overlap["comparison_prompts_inspected"] == 1629
    assert overlap["exact_prompt_overlaps"] == overlap["normalized_prompt_overlaps"] == []
    assert overlap["within_tranche_exact_overlaps"] == overlap["within_tranche_normalized_overlaps"] == []
    assert overlap["evaluation_manifest_sha256"] == manifest["manifest_sha256"]
    assert overlap["private_development_manifests"] == [f"manifests/evaluation/private/development-tranche{i}.json" for i in range(1, 7)]
    for entry in manifest["tasks"]:
        task = validate_task(load_json(ROOT / entry["path"]))
        assert sha256_object(task) == entry["sha256"]
        assert task["limits"]["timeout_seconds"] == (60 if task["language"] in {"go", "java", "rust"} else 30)
        prompt = task["prompt"]["text"]
        assert all(x in prompt for x in ("File contract:", "Required API:", "Behavior:", "Visible example:", "Return only the complete source file"))
        if task["task_type"] == "repair":
            assert "Buggy source to repair:" in prompt
            assert task["validation"]["known_bad"][0]["code"] in prompt


def test_executed_directionality_evidence_is_complete_and_bound() -> None:
    evidence_path = ROOT / "manifests/evaluation/private/decision-tranche2-directionality.json"
    if not evidence_path.exists():
        pytest.skip("directionality waits for the sealed cross-tranche overlap report")
    evidence = load_json(evidence_path)
    if evidence["executions"][0]["verifier"]["sandbox_contract_sha256"] != sha256_object(SANDBOX_CONTRACT):
        pytest.skip("archived ARM64 directionality is intentionally non-current")
    claimed = evidence.pop("evidence_sha256")
    assert sha256_object(evidence) == claimed
    assert evidence["status"] == "passed"
    assert evidence["execution_mode"] == "sequential"
    assert evidence["evaluation_manifest_sha256"] == "15cc33ac14830406a670aefc8e96420d7f3f20f756d41b8c4ce672d1a609bab9"
    assert evidence["cross_tranche_overlap_report"] == "manifests/evaluation/private/decision-tranches1-2-cross-overlap.json"
    assert evidence["cross_tranche_overlap_report_sha256"] == "2c9d3dd4c91b846f95adf437c79ae6d52543e030d5a35a6317b828ba42116cf3"
    assert SANDBOX_CONTRACT["backend"] == "docker"
    assert SANDBOX_CONTRACT["network"] == "none"
    assert SANDBOX_CONTRACT["pull"] == "never"
    assert evidence["sandbox_contract_sha256"] == sha256_object(SANDBOX_CONTRACT)
    assert evidence["task_count"] == 60
    assert evidence["execution_count"] == 120
    assert evidence["reference_passes"] == 60
    assert evidence["known_bad_rejections"] == 60
    assert evidence["failures"] == []
    assert all(
        "@sha256:" in row["verifier"]["image"]
        and row["verifier"]["sandbox_contract_sha256"] == evidence["sandbox_contract_sha256"]
        and not row["verifier"]["timed_out"]
        for row in evidence["executions"]
    )
