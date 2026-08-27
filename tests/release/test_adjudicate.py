import json
from pathlib import Path

from scripts.release.adjudicate import QWEN_REVISION, adjudicate, canonical_sha256


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
MINI = {"model_id": "ganesh-mini-1.0-candidate", "revision": QWEN_REVISION, "artifact_sha256": "2" * 64}


def cohort(passed: int) -> dict:
    return {
        "task_count": 360,
        "lanes": {lane: {"passed": passed, "denominator": 60} for lane in LANES},
    }


def comparison(base_model: dict, candidate_model: dict, base_passed: int, candidate_passed: int, delta: float) -> dict:
    wins = max(0, (candidate_passed - base_passed) * len(LANES))
    losses = max(0, (base_passed - candidate_passed) * len(LANES))
    value = {
        "schema_version": "1.0",
        "base_model": base_model,
        "candidate_model": candidate_model,
        "evidence": {
            "base_result_set_sha256": "4" * 64,
            "candidate_result_set_sha256": "5" * 64,
            "source_task_set_sha256": "6" * 64,
        },
        "base": cohort(base_passed),
        "candidate": cohort(candidate_passed),
        "paired": {
            "aggregate": {"wins": wins, "losses": losses, "ties": 360 - wins - losses, "denominator": 360},
            "lanes": {lane: {"wins": 1, "losses": 0, "ties": 59, "denominator": 60} for lane in LANES},
            "cluster_aware": {"bootstrap_ci": {"lower": 0.01}, "two_sided_permutation_p": 0.01},
        },
        "five_family_macro_delta": {"decimal": delta},
    }
    value["report_sha256"] = canonical_sha256(value)
    return value


def sealed(value: dict, field: str) -> dict:
    value = dict(value)
    value[field] = canonical_sha256(value)
    return value


def release_inputs(tmp_path: Path) -> tuple[dict, dict, dict, dict, list[Path]]:
    base = comparison(
        {"model_id": "Qwen/Qwen3.5-2B", "revision": QWEN_REVISION, "artifact_sha256": "1" * 64},
        MINI,
        5,
        6,
        0.1,
    )
    v01 = comparison(
        {"model_id": "ganesh-v0.1", "revision": "9" * 40, "artifact_sha256": "3" * 64},
        MINI,
        7,
        6,
        -0.02,
    )
    q8_sha, f16_sha, merged_sha = "a" * 64, "b" * 64, "c" * 64
    quant = comparison(
        {"model_id": "ganesh-mini-1.0-bf16", "revision": QWEN_REVISION, "artifact_sha256": merged_sha},
        {"model_id": "ganesh-mini-1.0-q8_0", "revision": QWEN_REVISION, "artifact_sha256": q8_sha},
        10,
        10,
        0.0,
    )
    laptop = sealed({
        "schema_version": "ganesh-mini-laptop-certification/v1",
        "status": "passed",
        "profiles": {
            "q8": {"passed": True, "peak_rss_bytes": 6 * 1024**3, "artifact": {"sha256": q8_sha}},
            "f16": {"passed": True, "peak_rss_bytes": 13 * 1024**3, "artifact": {"sha256": f16_sha}},
        },
    }, "evidence_sha256")
    seed = sealed({
        "schema_version": "ganesh-mini-seed-manifest/v1",
        "source_revision": "8" * 40,
        "total_records": 1449,
    }, "manifest_sha256")
    seed_path = tmp_path / "seed.json"
    seed_path.write_text(json.dumps(seed), encoding="utf-8")
    import hashlib

    seed_file_sha = hashlib.sha256(seed_path.read_bytes()).hexdigest()
    readiness = sealed({
        "schema_version": "ganesh-mini-readiness/v1",
        "status": "ready",
        "model_id": "Qwen/Qwen3.5-2B",
        "revision": QWEN_REVISION,
        "seed_manifest_seal": seed["manifest_sha256"],
        "seed_manifest_sha256": seed_file_sha,
    }, "report_sha256")
    readiness_path = tmp_path / "readiness.json"
    readiness_path.write_text(json.dumps(readiness), encoding="utf-8")
    card = sealed({
        "schema_version": "ganesh-mini-training-execution-card/v1",
        "status": "ready",
        "output_model_name": "ganesh-mini-1.0",
        "inputs": {"seed_manifest_sha256": seed_file_sha},
    }, "card_sha256")
    card_path = tmp_path / "card.json"
    card_path.write_text(json.dumps(card), encoding="utf-8")
    training = sealed({
        "schema_version": "ganesh-mini-sft-run/v1",
        "status": "complete",
        "identities": {"model_revision": QWEN_REVISION, "card_sha256": card["card_sha256"]},
    }, "evidence_sha256")
    training_path = tmp_path / "training.json"
    training_path.write_text(json.dumps(training), encoding="utf-8")
    artifact_manifest = sealed({
        "schema_version": "ganesh-mini-release-artifacts/v1",
        "status": "built",
        "model_name": "ganesh-mini-1.0",
        "selected_run_evidence_sha256": training["evidence_sha256"],
        "artifacts": {"merged_bf16_hf": {"sha256": merged_sha}, "gguf_q8": {"sha256": q8_sha}, "gguf_f16": {"sha256": f16_sha}},
    }, "manifest_sha256")
    path = tmp_path / "release-artifacts.json"
    path.write_text(json.dumps(artifact_manifest), encoding="utf-8")
    export = sealed({
        "schema_version": "ganesh-mini-export-equivalence/v1",
        "status": "passed",
        "task_count": 6,
        "artifact_manifest_sha256": artifact_manifest["manifest_sha256"],
    }, "evidence_sha256")
    export_path = tmp_path / "export-equivalence.json"
    export_path.write_text(json.dumps(export), encoding="utf-8")
    return base, v01, quant, laptop, [seed_path, readiness_path, card_path, training_path, path, export_path]


def test_release_gates_fail_closed_and_pass_complete_evidence(tmp_path: Path) -> None:
    inputs = release_inputs(tmp_path)
    report = adjudicate(*inputs)
    assert report["status"] == "release-eligible"
    assert report["reference_comparison"]["ganesh_v01_stronger_absolute_correctness"] is True
    unsigned = dict(report)
    claimed = unsigned.pop("evidence_sha256")
    assert canonical_sha256(unsigned) == claimed


def test_tampered_comparison_blocks_release(tmp_path: Path) -> None:
    base, v01, quant, laptop, manifests = release_inputs(tmp_path)
    base["five_family_macro_delta"]["decimal"] = 0.2
    report = adjudicate(base, v01, quant, laptop, manifests)
    assert report["status"] == "release-blocked"
    assert "sealed_complete_decision_comparisons" in report["failed_checks"]


def test_missing_ganesh_v01_execution_blocks_release(tmp_path: Path) -> None:
    base, _, quant, laptop, manifests = release_inputs(tmp_path)
    report = adjudicate(base, {}, quant, laptop, manifests)
    assert report["status"] == "release-blocked"
    assert "ganesh_v01_reference_executed" in report["failed_checks"]


def test_missing_training_lineage_manifest_blocks_release(tmp_path: Path) -> None:
    base, v01, quant, laptop, manifests = release_inputs(tmp_path)
    manifests = [path for path in manifests if path.name != "training.json"]
    report = adjudicate(base, v01, quant, laptop, manifests)
    assert report["status"] == "release-blocked"
    assert "required_manifests_complete" in report["failed_checks"]


def test_artifact_must_bind_selected_training_run(tmp_path: Path) -> None:
    base, v01, quant, laptop, manifests = release_inputs(tmp_path)
    artifact_path = next(path for path in manifests if path.name == "release-artifacts.json")
    artifact = json.loads(artifact_path.read_text())
    artifact["selected_run_evidence_sha256"] = "f" * 64
    artifact.pop("manifest_sha256")
    artifact["manifest_sha256"] = canonical_sha256(artifact)
    artifact_path.write_text(json.dumps(artifact), encoding="utf-8")
    report = adjudicate(base, v01, quant, laptop, manifests)
    assert report["status"] == "release-blocked"
    assert "required_manifests_complete" in report["failed_checks"]
