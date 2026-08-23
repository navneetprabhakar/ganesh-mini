import copy
import json

import pytest

import scripts.eval.authoring.audit_global_decision_separation as audit
from scripts.eval.authoring.audit_global_decision_separation import (
    OUTPUT,
    ROOT,
    build,
    normalized,
)
from scripts.eval.contracts import load_json, sha256_bytes, sha256_object

EXPECTED_REPORT_SHA256 = "96ea9669e194c567f304c5462b2be9cc171555bba56ea10801186480bb347a06"


def current_directionality_available() -> bool:
    evidence = load_json(ROOT / "manifests/evaluation/private/decision-tranche1-directionality.json")
    runtime = load_json(ROOT / "configs/eval/runtimes.json")["runtimes"]
    first = evidence["executions"][0]
    expected = runtime[first["verifier"]["runtime_id"]]
    return first["verifier"]["image_id"] == expected["image_id"]


def test_normalization_is_nfkc_casefold_and_whitespace_collapsed() -> None:
    assert normalized("  Ａ\tStraße\n") == "a strasse"


def test_manifest_seal_tamper_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    original = audit.load_json

    def tampered(path):
        value = original(path)
        if path.name == "development-tranche1.json":
            value = copy.deepcopy(value)
            value["task_count"] = 29
        return value

    monkeypatch.setattr(audit, "load_json", tampered)
    with pytest.raises(RuntimeError, match="manifest seal mismatch"):
        audit.build()


def test_resealed_directionality_artifact_tamper_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    if not current_directionality_available():
        pytest.skip("archived ARM64 directionality is intentionally non-current")
    original = audit.load_json

    def tampered(path):
        value = original(path)
        if path.name == "decision-tranche3-directionality.json":
            value = copy.deepcopy(value)
            value["executions"][0]["artifact_sha256"] = "0" * 64
            value["evidence_sha256"] = sha256_object(
                {key: item for key, item in value.items() if key != "evidence_sha256"}
            )
        return value

    monkeypatch.setattr(audit, "load_json", tampered)
    with pytest.raises(RuntimeError, match="artifact seal mismatch"):
        audit.build()


def test_resealed_directionality_output_hash_tamper_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    if not current_directionality_available():
        pytest.skip("archived ARM64 directionality is intentionally non-current")
    original = audit.load_json

    def tampered(path):
        value = original(path)
        if path.name == "decision-tranche4-directionality.json":
            value = copy.deepcopy(value)
            value["executions"][0]["verifier"]["stdout_sha256"] = "0" * 64
            value["evidence_sha256"] = sha256_object(
                {key: item for key, item in value.items() if key != "evidence_sha256"}
            )
        return value

    monkeypatch.setattr(audit, "load_json", tampered)
    with pytest.raises(RuntimeError, match="stdout seal mismatch"):
        audit.build()


def test_global_decision_separation_is_complete_and_sealed() -> None:
    if not current_directionality_available():
        with pytest.raises(RuntimeError, match="verifier image mismatch"):
            build()
        return
    report = build()
    assert report["status"] == "passed"
    assert report["counts"] == {
        "seed_records": 1449,
        "development_tasks": 180,
        "decision_tasks": 360,
        "comparison_prompts": 1629,
    }
    assert len(report["seed_inputs"]) == 2
    assert len(report["development_manifests"]) == 6
    assert len(report["decision_manifests"]) == 6
    assert len(report["decision_evidence"]) == 6
    assert all(len(item["tasks"]) == 30 for item in report["development_manifests"])
    assert all(len(item["tasks"]) == 60 for item in report["decision_manifests"])
    assert all(
        not report[field]
        for field in (
            "exact_decision_vs_seed_development_overlaps",
            "normalized_decision_vs_seed_development_overlaps",
            "exact_decision_prompt_overlaps",
            "normalized_decision_prompt_overlaps",
            "duplicate_ids",
            "duplicate_seed_development_exact_prompts",
            "duplicate_seed_development_normalized_prompts",
        )
    )
    for seed in report["seed_inputs"]:
        assert sha256_bytes((ROOT / seed["path"]).read_bytes()) == seed["sha256"]
    stored = load_json(OUTPUT)
    claimed = stored.pop("report_sha256")
    assert (
        sha256_object(stored)
        == claimed
        == report["report_sha256"]
        == EXPECTED_REPORT_SHA256
    )
    json.dumps(report, allow_nan=False)
