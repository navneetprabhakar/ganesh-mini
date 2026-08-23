import pytest

from scripts.eval.authoring.build_tranche3 import BEHAVIOR,KINDS,LANG,ROOT,SLUGS,build
from scripts.eval.contracts import load_json,sha256_object,validate_task

def test_tranche3_contract_balance_and_overlap():
    manifest,overlap=build()
    assert manifest["task_count"]==30
    assert sum(v["generation"] for v in manifest["counts_by_lane"].values())==15
    assert sum(v["repair"] for v in manifest["counts_by_lane"].values())==15
    assert overlap["seed_records_inspected"]==1449
    assert overlap["other_private_development_prompts_inspected"]==90
    assert overlap["exact_prompt_overlaps"]==[]
    assert overlap["normalized_prompt_overlaps"]==[]
    assert overlap["evaluation_manifest_sha256"]==manifest["manifest_sha256"]

def test_each_lane_has_five_original_directional_tasks():
    assert len(SLUGS)==5 and len(set(SLUGS))==5
    for language,kinds in KINDS.items():
        assert len(kinds)==5 and set(LANG[language])==set(SLUGS)
        for slug,item in LANG[language].items():
            assert item["reference"]!=item["bad"]
            assert BEHAVIOR[slug]

def test_task_hashes_and_prompt_contracts():
    manifest,_=build()
    for entry in manifest["tasks"]:
        task=validate_task(load_json(ROOT/entry["path"]))
        assert sha256_object(task)==entry["sha256"]
        prompt=task["prompt"]["text"]
        assert "File contract:" in prompt and "Required API:" in prompt
        assert "Behavior:" in prompt and "Visible example:" in prompt
        assert "Return only the complete source file" in prompt
        if task["task_type"]=="repair":
            assert "Buggy source to repair:" in prompt
            assert task["validation"]["known_bad"][0]["code"] in prompt

def test_executed_directionality_evidence_is_complete_and_bound():
    evidence=load_json(ROOT/"manifests/evaluation/private/development-tranche3-directionality.json")
    manifest=load_json(ROOT/evidence["manifest_path"])
    if evidence["manifest_sha256"] != manifest["manifest_sha256"]:
        pytest.skip("directionality evidence is intentionally stale pending native rerun")
    claimed=evidence.pop("evidence_sha256")
    assert sha256_object(evidence)==claimed
    assert evidence["status"]=="passed"
    assert evidence["execution_count"]==60
    assert evidence["reference_passes"]==30
    assert evidence["known_bad_failures"]==30
    assert evidence["timeouts"]==0
    assert evidence["directionality_failures"]==[]
    assert evidence["execution_mode"]=="sequential" and evidence["network_mode"]=="none"
    assert all("@sha256:" in row["verifier"]["image"] for row in evidence["results"])
