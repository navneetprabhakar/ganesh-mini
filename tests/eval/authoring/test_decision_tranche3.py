from scripts.eval.authoring.build_decision_tranche3 import (
    DEVELOPMENT_MANIFESTS,
    PRIOR_DECISION_MANIFESTS,
    ROOT,
    SEED_PATHS,
    SLUGS,
    build,
)
from scripts.eval.contracts import load_json, sha256_object, validate_task


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
