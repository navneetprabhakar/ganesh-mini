from scripts.inference.verify_gate1_runtime_bundle import ATTEMPT_ID, canonical_sha256, rehearse


def test_sealed_runtime_bundle_rehearses_exact_failed_attempt_id() -> None:
    evidence = rehearse()
    claimed = evidence.pop("evidence_sha256")
    assert claimed == canonical_sha256(evidence)
    assert evidence["status"] == "passed"
    assert evidence["attempt_id"] == ATTEMPT_ID
    assert len(evidence["container_names"]) == 7
    assert all(evidence["checks"].values())
