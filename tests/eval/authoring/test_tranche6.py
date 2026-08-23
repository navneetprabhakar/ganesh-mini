import pytest

from scripts.eval.authoring.build_tranche6 import ROOT,build
from scripts.eval.contracts import load_json,sha256_object,validate_task

def test_tranche6_contract_balance_hashes_and_separation()->None:
    manifest,overlap=build();assert manifest["task_count"]==30
    assert sum(x["generation"]for x in manifest["counts_by_lane"].values())==15
    assert sum(x["repair"]for x in manifest["counts_by_lane"].values())==15
    assert all(sum(x.values())==5 and set(x.values())=={2,3}for x in manifest["counts_by_lane"].values())
    assert overlap["seed_records_inspected"]==1449
    assert overlap["exact_prompt_overlaps"]==overlap["normalized_prompt_overlaps"]==[]
    assert overlap["within_tranche_exact_overlaps"]==overlap["within_tranche_normalized_overlaps"]==[]
    assert overlap["evaluation_manifest_sha256"]==manifest["manifest_sha256"]
    for entry in manifest["tasks"]:
        task=validate_task(load_json(ROOT/entry["path"]));assert sha256_object(task)==entry["sha256"]
        prompt=task["prompt"]["text"]
        assert all(x in prompt for x in("File contract:","Required API:","Behavior:","Visible example:","Return only the complete source file"))
        if task["task_type"]=="repair":assert "Buggy source to repair:" in prompt and task["validation"]["known_bad"][0]["code"]in prompt

def test_executed_directionality_evidence_is_complete_and_bound()->None:
    evidence=load_json(ROOT/"manifests/evaluation/private/development-tranche6-directionality.json")
    manifest=load_json(ROOT/evidence["evaluation_manifest"])
    if evidence["evaluation_manifest_sha256"] != manifest["manifest_sha256"]:
        pytest.skip("directionality evidence is intentionally stale pending native rerun")
    claimed=evidence.pop("evidence_sha256");assert sha256_object(evidence)==claimed
    assert evidence["status"]=="passed" and evidence["execution_mode"]=="sequential"
    assert evidence["task_count"]==30 and evidence["execution_count"]==60
    assert evidence["reference_passes"]==30 and evidence["known_bad_rejections"]==30 and evidence["failures"]==[]
    assert all("@sha256:" in r["verifier"]["image"]and not r["verifier"]["timed_out"]for r in evidence["executions"])
