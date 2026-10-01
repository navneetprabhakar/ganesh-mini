from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts.eval.adjudicate_gate3_capability_canary import adjudicate as select_canary
from scripts.eval.adjudicate_gate3_capability_development import adjudicate
from scripts.eval.contracts import ContractError, sha256_object
from tests.eval.test_adjudicate_gate3_capability_canary import (
    BASE, CANARY, WORKSPACE, _fixture, _flip_pass, _sealed,
)


ROOT = Path(__file__).resolve().parents[2]
BASE_ADMISSION = ROOT / "measurement/gate1/baseline_admission.json"
BASE_RUN = ROOT / "measurement/inference/development/qwen3.5-2b-base-v1/run.json"


def _full_fixture(tmp_path: Path) -> tuple[Path, Path, Path]:
    fixture = _fixture(tmp_path)
    selection = select_canary(CANARY, WORKSPACE, BASE, fixture[0], fixture[1], fixture[2], fixture[3])
    selection_path = tmp_path / "selection.json"
    selection_path.write_text(json.dumps(selection))
    candidate_dir = tmp_path / "development"
    candidate_dir.mkdir()
    selected = selection["selected_candidate"]["model"]
    for base_path in BASE.glob("dev-*.json"):
        envelope = copy.deepcopy(json.loads(base_path.read_text()))
        result = envelope["verification"]["result"]
        result["model"] = copy.deepcopy(selected)
        envelope["model"].update(selected)
        result.pop("result_sha256")
        result["result_sha256"] = sha256_object(result)
        envelope.pop("evidence_sha256")
        _sealed(candidate_dir / base_path.name, envelope, "evidence_sha256")
    return selection_path, fixture[0], candidate_dir


def _adjudicate(value: tuple[Path, Path, Path], *, base_admission: Path = BASE_ADMISSION) -> dict:
    return adjudicate(value[0], WORKSPACE, ROOT, value[1], base_admission, BASE_RUN, BASE, value[2])


def test_full_development_fails_quality_with_no_gain(tmp_path: Path) -> None:
    value = _full_fixture(tmp_path)
    report = _adjudicate(value)
    assert report["status"] == "quality-criteria-failed"
    assert report["failed_checks"] == ["minimum_four_improved_product_families"]
    assert report["gate3_sealed"] is False
    assert report["task_count"] == 180
    assert report["gate1_baseline_admission_sha256"]


def test_four_families_without_regression_satisfy_frozen_quality(tmp_path: Path) -> None:
    value = _full_fixture(tmp_path)
    candidate_dir = value[2]
    for lane in ("go", "java", "javascript", "python"):
        failed = next(path for path in sorted(candidate_dir.glob(f"dev-*-{lane}-*.json"))
                      if json.loads(path.read_text())["verification"]["result"]["passed"] is False)
        _flip_pass(failed)
    report = _adjudicate(value)
    assert report["status"] == "quality-criteria-passed"
    assert report["families_improved"] == ["go", "java", "javascript_typescript", "python"]
    assert report["lane_regressions"] == []
    assert report["gate3_sealed"] is False


def test_rejects_missing_task_and_invalid_gate1_binding(tmp_path: Path) -> None:
    value = _full_fixture(tmp_path)
    next(value[2].glob("dev-*.json")).unlink()
    with pytest.raises(ContractError, match="exactly 180"):
        _adjudicate(value)
    other = tmp_path / "other"
    other.mkdir()
    value = _full_fixture(other)
    fake = tmp_path / "fake-admission.json"
    admission = json.loads(BASE_ADMISSION.read_text())
    admission.pop("evidence_sha256")
    admission["baseline_run_sha256"] = "0" * 64
    _sealed(fake, admission, "evidence_sha256")
    with pytest.raises(ContractError, match="Gate 1"):
        _adjudicate(value, base_admission=fake)
