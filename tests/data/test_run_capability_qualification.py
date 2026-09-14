import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.run_capability_qualification import run_batch, verify_completed


def write_complete(output: Path, evidence: Path, identifiers: list[str]) -> None:
    payload = b"".join(
        json.dumps({"id": identifier}, sort_keys=True, separators=(",", ":")).encode() + b"\n"
        for identifier in identifiers
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    evidence.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(payload)
    record = {
        "candidate_output_sha256": hashlib.sha256(payload).hexdigest(),
        "generated": len(identifiers),
        "failures": [],
        "selection": {"requested_ids": identifiers, "evaluation_surfaces_read": 0},
    }
    record["evidence_sha256"] = canonical_sha256(record)
    evidence.write_text(json.dumps(record), encoding="utf-8")


def test_verify_completed_accepts_exact_sealed_batch(tmp_path: Path) -> None:
    output, evidence = tmp_path / "batch.jsonl", tmp_path / "evidence.json"
    write_complete(output, evidence, ["a", "b"])
    assert verify_completed(output, evidence, ["a", "b"])["generated"] == 2


def test_verify_completed_rejects_partial_or_wrong_ids(tmp_path: Path) -> None:
    output, evidence = tmp_path / "batch.jsonl", tmp_path / "evidence.json"
    output.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="partial"):
        verify_completed(output, evidence, ["a"])
    evidence.unlink(missing_ok=True)
    output.unlink()
    write_complete(output, evidence, ["a"])
    with pytest.raises(ValueError, match="sealed contract"):
        verify_completed(output, evidence, ["b"])


def test_run_batch_reuses_valid_artifacts_without_subprocess(tmp_path: Path) -> None:
    output, evidence = tmp_path / "batch.jsonl", tmp_path / "evidence.json"
    write_complete(output, evidence, ["a"])
    with patch("scripts.data.run_capability_qualification.subprocess.run") as invoked:
        result = run_batch(["never"], output, evidence, ["a"])
    invoked.assert_not_called()
    assert result["status"] == "reused"
