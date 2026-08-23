import pytest

from scripts.eval.authoring.build_decision_tranche3 import (
    DEVELOPMENT_MANIFESTS,
    PRIOR_DECISION_MANIFESTS,
    ROOT,
    SEED_PATHS,
    SLUGS,
    build,
)
from scripts.eval.contracts import load_json, sha256_object, validate_task
from scripts.verify.sandbox import SANDBOX_CONTRACT


def test_decision_tranche3_contract_balance_hashes_and_separation() -> None:
    manifest, overlap = build()
    assert manifest["surface"] == "decision"
    assert manifest["task_count"] == 60
    assert all(x == {"generation": 5, "repair": 5} for x in manifest["counts_by_lane"].values())
    assert overlap["comparison_inputs"] == {
        "seed_jsonl": list(SEED_PATHS),
        "private_development_manifests": list(DEVELOPMENT_MANIFESTS),
        "prior_decision_manifests": list(PRIOR_DECISION_MANIFESTS),
    }
    assert overlap["seed_records_inspected"] == 1449
    assert overlap["private_development_prompts_inspected"] == 180
    assert overlap["prior_decision_prompts_inspected"] == 120
    assert overlap["comparison_prompts_inspected"] == 1749
    assert overlap["exact_prompt_overlaps"] == overlap["normalized_prompt_overlaps"] == []
    assert overlap["within_tranche_exact_overlaps"] == overlap["within_tranche_normalized_overlaps"] == []
    assert overlap["evaluation_manifest_sha256"] == manifest["manifest_sha256"]
    assert len({entry["task_id"] for entry in manifest["tasks"]}) == 60
    assert all(any(slug in entry["task_id"] for slug in SLUGS) for entry in manifest["tasks"])
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
    evidence_path = ROOT / "manifests/evaluation/private/decision-tranche3-directionality.json"
    if not evidence_path.exists():
        pytest.skip("directionality has not been executed")
    evidence = load_json(evidence_path)
    if evidence["executions"][0]["verifier"]["sandbox_contract_sha256"] != sha256_object(SANDBOX_CONTRACT):
        pytest.skip("archived ARM64 directionality is intentionally non-current")
    claimed = evidence.pop("evidence_sha256")
    assert sha256_object(evidence) == claimed
    assert evidence["status"] == "passed"
    assert evidence["execution_mode"] == "sequential"
    assert evidence["evaluation_manifest_sha256"] == "26f982c437000012d2eae1f4a3d77260b9f3798931dc938941e29c91f2e3a3d9"
    assert evidence["overlap_report"] == "manifests/evaluation/private/decision-tranche3-overlap.json"
    assert evidence["overlap_report_sha256"] == "dae97584f926381995f06232381425239fa35e1e0d83ce6b5404b93e0bba15d4"
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
