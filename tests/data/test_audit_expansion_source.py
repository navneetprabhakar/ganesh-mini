from __future__ import annotations

import json

import pytest

from scripts.data.audit_expansion_source import audit


def test_audit_counts_target_rows_but_does_not_admit_them(tmp_path) -> None:
    source = tmp_path / "source.json"
    source.write_text(json.dumps([
        {"instruction": "p", "output": "a", "language": "Go", "source": "McEval-Instruct"},
        {"instruction": "p2", "output": "a2", "language": "Rust", "source": "McEval-Instruct"},
    ]))
    report = audit(source, "abc")
    assert report["target_language_records"]["go"] == 1
    assert report["target_records_with_independent_behavioral_tests"] == 0
    assert report["admission_status"] == "candidate-queue-only"


def test_audit_rejects_schema_drift(tmp_path) -> None:
    source = tmp_path / "source.json"
    source.write_text(json.dumps([{"instruction": "p", "output": "a", "language": "Go"}]))
    with pytest.raises(ValueError, match="unexpected schema"):
        audit(source, "abc")
