from scripts.release.verify_export_equivalence import LANES, canonical_sha256, verify


def sealed(value: dict, field: str) -> dict:
    value = dict(value)
    value[field] = canonical_sha256(value)
    return value


def cohort(artifact_sha256: str, *, flip: str | None = None) -> tuple[dict, list[dict]]:
    results = []
    for lane in LANES:
        results.append({
            "task_id": f"export-{lane}",
            "language": lane,
            "passed": lane != flip,
            "_source_task_sha256": lane[0] * 64,
            "rendered_prompt_sha256": lane[-1] * 64,
            "result_sha256": artifact_sha256,
        })
    run = {
        "run_sha256": artifact_sha256[::-1],
        "model": {"model_id": "ganesh-mini-1.0", "artifact_sha256": artifact_sha256},
    }
    return run, results


def fixture() -> tuple[dict, dict]:
    hashes = {"merged_bf16_hf": "a" * 64, "gguf_f16": "b" * 64, "gguf_q8": "c" * 64}
    manifest = sealed({
        "schema_version": "ganesh-mini-release-artifacts/v1",
        "status": "built",
        "artifacts": {name: {"sha256": digest} for name, digest in hashes.items()},
    }, "manifest_sha256")
    cohorts = {name: cohort(digest) for name, digest in hashes.items()}
    return manifest, cohorts


def test_export_equivalence_requires_matching_six_lane_pass_vectors() -> None:
    manifest, cohorts = fixture()
    report = verify(manifest, cohorts)
    assert report["status"] == "passed"
    assert report["pass_vector_equivalence"] == {"gguf_f16": True, "gguf_q8": True}


def test_export_equivalence_records_quantized_behavior_drift() -> None:
    manifest, cohorts = fixture()
    cohorts["gguf_q8"] = cohort("c" * 64, flip="rust")
    report = verify(manifest, cohorts)
    assert report["status"] == "failed"
    assert report["pass_vector_equivalence"]["gguf_q8"] is False


def test_export_equivalence_rejects_prompt_template_drift() -> None:
    manifest, cohorts = fixture()
    run, results = cohorts["gguf_f16"]
    results[0]["rendered_prompt_sha256"] = "d" * 64
    cohorts["gguf_f16"] = run, results
    import pytest

    with pytest.raises(ValueError, match="rendered prompts"):
        verify(manifest, cohorts)
