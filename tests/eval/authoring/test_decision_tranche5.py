import pytest

from scripts.eval.authoring.build_decision_tranche5 import (
    DEVELOPMENT_MANIFESTS,
    EXPECTED_TRANCHE4_SHA256,
    PRIOR_DECISION_MANIFESTS,
    ROOT,
    SEED_PATHS,
    SLUGS,
    build,
)
from scripts.eval.contracts import load_json, sha256_object, validate_task
from scripts.verify.sandbox import SANDBOX_CONTRACT


def test_decision_tranche5_contract_balance_hashes_and_separation() -> None:
    tranche4 = load_json(ROOT / PRIOR_DECISION_MANIFESTS[-1])
    assert tranche4["manifest_sha256"] == EXPECTED_TRANCHE4_SHA256
    manifest, overlap = build()
    assert manifest["surface"] == "decision"
    assert manifest["status"] == "authored-unexecuted"
    assert manifest["task_count"] == 60
    assert all(counts == {"generation": 5, "repair": 5} for counts in manifest["counts_by_lane"].values())
    assert overlap["comparison_inputs"] == {
        "seed_jsonl": list(SEED_PATHS),
        "private_development_manifests": list(DEVELOPMENT_MANIFESTS),
        "prior_decision_manifests": list(PRIOR_DECISION_MANIFESTS),
    }
    assert overlap["seed_records_inspected"] == 1449
    assert overlap["private_development_prompts_inspected"] == 180
    assert overlap["prior_decision_prompts_inspected"] == 240
    assert overlap["comparison_prompts_inspected"] == 1869
    assert overlap["evaluation_prompts_inspected"] == 60
    assert overlap["exact_prompt_overlaps"] == overlap["normalized_prompt_overlaps"] == []
    assert overlap["within_tranche_exact_overlaps"] == overlap["within_tranche_normalized_overlaps"] == []
    assert overlap["evaluation_manifest_sha256"] == manifest["manifest_sha256"]
    assert sha256_object({key: value for key, value in overlap.items() if key != "report_sha256"}) == overlap["report_sha256"]
    assert len({entry["task_id"] for entry in manifest["tasks"]}) == 60
    assert all(any(slug in entry["task_id"] for slug in SLUGS) for entry in manifest["tasks"])
    for entry in manifest["tasks"]:
        task = validate_task(load_json(ROOT / entry["path"]))
        assert sha256_object(task) == entry["sha256"]
        assert task["limits"] == {
            "timeout_seconds": 60 if task["language"] in {"go", "java", "rust"} else 30,
            "memory_mb": 512,
            "cpus": 1,
            "pids": 64,
            "output_bytes": 65536,
        }
        prompt = task["prompt"]["text"]
        assert all(label in prompt for label in ("File contract:", "Required API:", "Behavior:", "Visible example:", "Return only the complete source file"))
        assert task["prompt"]["sha256"] == task["rendered_prompt"]["sha256"]
        if task["task_type"] == "repair":
            assert "Buggy source to repair:" in prompt
            assert task["validation"]["known_bad"][0]["code"] in prompt


def test_executed_directionality_evidence_is_complete_and_bound() -> None:
    evidence_path = ROOT / "manifests/evaluation/private/decision-tranche5-directionality.json"
    if not evidence_path.exists():
        pytest.skip("directionality has not been executed")
    evidence = load_json(evidence_path)
    if evidence["executions"][0]["verifier"]["sandbox_contract_sha256"] != sha256_object(SANDBOX_CONTRACT):
        pytest.skip("archived ARM64 directionality is intentionally non-current")
    claimed = evidence.pop("evidence_sha256")
    assert claimed == "cd7cafdec42d97173e877fa74530c5daef3d4c1edded9df1b71de9dd453ecdb1"
    assert sha256_object(evidence) == claimed
    assert evidence["status"] == "passed"
    assert evidence["execution_mode"] == "sequential"
    assert evidence["evaluation_manifest_sha256"] == "ee52d232e2d44411a398ad680def61ffffd54722d8a8fc400ffdd2143d4240e3"
    assert evidence["overlap_report"] == "manifests/evaluation/private/decision-tranche5-overlap.json"
    assert evidence["overlap_report_sha256"] == "251cee5751463ffa76159823b3ec939a6edbd66e328336ca65e7169022186de5"
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
