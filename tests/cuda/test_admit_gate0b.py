from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.cuda.admit_gate0b import build, canonical_sha256, load_sealed


ROOT = Path(__file__).resolve().parents[2]


def test_repository_gate0b_evidence_admits_exact_passed_run() -> None:
    evidence = build(ROOT)
    claimed = evidence.pop("evidence_sha256")
    assert claimed == canonical_sha256(evidence)
    assert evidence["passed"] is True
    assert evidence["model_id"] == "Qwen/Qwen3.5-2B"
    assert evidence["revision"] == "15852e8c16360a2fea060d615a32b45270f8a8fc"
    assert evidence["recipe_id"] == "bf16-lora-primary-v1"
    assert evidence["records_completed"] == evidence["optimizer_steps"] == 16
    assert evidence["exact_resources_absent"] is True


def test_rejects_resealed_result_without_passed_qualification() -> None:
    def forged(path: Path, field: str):
        value = load_sealed(path, field)
        if path.name == "run-result.json":
            value["qualification"]["status"] = "failed"
            value[field] = canonical_sha256({key: row for key, row in value.items() if key != field})
        return value

    with patch("scripts.cuda.admit_gate0b.load_sealed", side_effect=forged):
        with pytest.raises(ValueError, match="qualification envelope"):
            build(ROOT)
