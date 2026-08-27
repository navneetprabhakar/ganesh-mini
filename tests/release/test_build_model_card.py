import json
from pathlib import Path

import pytest

from scripts.release.adjudicate import adjudicate
from scripts.release.build_model_card import render_model_card, validate_inputs
from tests.release.test_adjudicate import release_inputs


def write(path: Path, value: dict) -> Path:
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def release_files(tmp_path: Path) -> tuple[dict, dict[str, Path]]:
    base, v01, quant, laptop, manifests = release_inputs(tmp_path)
    decision = adjudicate(base, v01, quant, laptop, manifests)
    assert decision["status"] == "release-eligible"
    files = {
        "decision_path": write(tmp_path / "decision.json", decision),
        "artifact_manifest_path": next(path for path in manifests if path.name == "release-artifacts.json"),
        "export_equivalence_path": next(path for path in manifests if path.name == "export-equivalence.json"),
        "qwen_comparison_path": write(tmp_path / "qwen.json", base),
        "ganesh_v01_comparison_path": write(tmp_path / "v01.json", v01),
        "quant_comparison_path": write(tmp_path / "quant.json", quant),
        "laptop_path": write(tmp_path / "laptop.json", laptop),
    }
    return decision, files


def test_model_card_is_derived_from_bound_release_evidence(tmp_path: Path) -> None:
    decision, files = release_files(tmp_path)
    values = validate_inputs(**files)
    card = render_model_card(*values)
    assert "# Ganesh Mini 1.0" in card
    assert "Qwen/Qwen3.5-2B" in card
    assert "Ganesh v0.1 remains ahead" in card
    assert decision["evidence_sha256"] in card
    assert "20.00%" not in card  # Fixture macro values are derived, never hard-coded.


def test_model_card_rejects_unbound_comparison(tmp_path: Path) -> None:
    _, files = release_files(tmp_path)
    value = json.loads(files["qwen_comparison_path"].read_text())
    value["report_sha256"] = "f" * 64
    files["qwen_comparison_path"].write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError, match="invalid report_sha256"):
        validate_inputs(**files)
