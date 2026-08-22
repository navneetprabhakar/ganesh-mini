from scripts.eval.authoring.build_tranche1 import ROOT, build
from scripts.eval.contracts import load_json, sha256_object, validate_task


def test_tranche1_contract_balance_hashes_and_seed_separation() -> None:
    manifest, overlap = build()
    assert manifest["task_count"] == 30
    assert sum(x["generation"] for x in manifest["counts_by_lane"].values()) == 15
    assert sum(x["repair"] for x in manifest["counts_by_lane"].values()) == 15
    assert all(sum(x.values()) == 5 and set(x.values()) == {2, 3} for x in manifest["counts_by_lane"].values())
    assert overlap["seed_records_inspected"] == 1449
    assert overlap["exact_prompt_overlaps"] == []
    assert overlap["normalized_prompt_overlaps"] == []
    assert overlap["evaluation_manifest_sha256"] == manifest["manifest_sha256"]
    for entry in manifest["tasks"]:
        task = validate_task(load_json(ROOT / entry["path"]))
        assert sha256_object(task) == entry["sha256"]
        assert task["surface"] == "development"
        assert task["validation"]["known_bad"]
        prompt = task["prompt"]["text"]
        assert "File contract:" in prompt
        assert "Required API:" in prompt
        assert "Visible example:" in prompt
        assert "Return only the complete source file" in prompt
        if task["task_type"] == "repair":
            assert "Buggy source to repair:" in prompt
            assert task["validation"]["known_bad"][0]["code"] in prompt


def test_executed_directionality_evidence_is_complete_and_bound() -> None:
    evidence = load_json(ROOT / "manifests/evaluation/private/development-tranche1-directionality.json")
    claimed = evidence.pop("evidence_sha256")
    assert sha256_object(evidence) == claimed
    assert evidence["status"] == "passed"
    assert evidence["task_count"] == 30
    assert evidence["execution_count"] == 60
    assert evidence["reference_passes"] == 30
    assert evidence["known_bad_rejections"] == 30
    assert evidence["failures"] == []
    assert evidence["evaluation_manifest_sha256"] == load_json(
        ROOT / evidence["evaluation_manifest"]
    )["manifest_sha256"]
    assert all("@sha256:" in row["verifier"]["image"] for row in evidence["executions"])
    assert all(not row["verifier"]["timed_out"] for row in evidence["executions"])
