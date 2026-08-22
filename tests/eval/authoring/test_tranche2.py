from scripts.eval.authoring.build_tranche2 import ROOT, SLUGS, build
from scripts.eval.contracts import load_json, sha256_object, validate_task

def test_tranche2_contract_balance_hashes_and_overlap() -> None:
    manifest,overlap=build()
    assert manifest["task_count"]==30
    assert sum(x["generation"] for x in manifest["counts_by_lane"].values())==15
    assert sum(x["repair"] for x in manifest["counts_by_lane"].values())==15
    assert all(sum(x.values())==5 and set(x.values())=={2,3} for x in manifest["counts_by_lane"].values())
    assert overlap["seed_records_inspected"]==1449
    assert overlap["exact_prompt_overlaps"]==[] and overlap["normalized_prompt_overlaps"]==[]
    assert overlap["evaluation_manifest_sha256"]==manifest["manifest_sha256"]
    for entry in manifest["tasks"]:
        task=validate_task(load_json(ROOT/entry["path"]));assert sha256_object(task)==entry["sha256"]
        prompt=task["prompt"]["text"]
        assert all(marker in prompt for marker in ("File contract:","Required API:","Behavior:","Visible example:","Return only the complete source file"))
        if task["task_type"]=="repair":
            assert "Buggy source to repair:" in prompt and task["validation"]["known_bad"][0]["code"] in prompt
    assert all(any(entry["task_id"].endswith(slug) for entry in manifest["tasks"]) for slug in SLUGS)

def test_executed_directionality_evidence_is_complete_and_bound() -> None:
    evidence=load_json(ROOT/"manifests/evaluation/private/development-tranche2-directionality.json")
    claimed=evidence.pop("evidence_sha256");assert sha256_object(evidence)==claimed
    assert evidence["status"]=="passed" and evidence["execution_mode"] in {"sequential","sequential-with-targeted-retry"}
    if evidence["execution_mode"]=="sequential-with-targeted-retry":
        assert evidence["prior_evidence_sha256"] and evidence["retry_execution_count"]>=1
    assert evidence["task_count"]==30 and evidence["execution_count"]==60
    assert evidence["reference_passes"]==30 and evidence["known_bad_rejections"]==30 and evidence["failures"]==[]
    assert evidence["evaluation_manifest_sha256"]==load_json(ROOT/evidence["evaluation_manifest"])["manifest_sha256"]
    assert all("@sha256:" in row["verifier"]["image"] and not row["verifier"]["timed_out"] for row in evidence["executions"])
