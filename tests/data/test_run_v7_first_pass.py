from scripts.data.run_v7_first_pass import _thresholds


def _rows(status="structurally-valid"):
    lanes = ("go", "java", "javascript", "typescript", "python", "rust")
    capabilities = tuple(f"cap-{i}" for i in range(10))
    dimensions = tuple(f"dim-{i}" for i in range(5))
    return [{
        "status": status, "lane": lanes[i % 6], "primary_capability": capabilities[i % 10],
        "assigned_cross_cutting_dimension": dimensions[i % 5], "evaluation_artifacts_read": 0,
    } for i in range(60)]


def test_thresholds_allow_direct_final_stage_for_clean_60() -> None:
    result = _thresholds(_rows())
    assert result["direct_final_stage_eligible"] is True
    assert result["structural_reauthoring_eligible"] is False


def test_thresholds_fail_closed_on_unresolved() -> None:
    rows = _rows(); rows[0]["status"] = "invocation-failed"
    result = _thresholds(rows)
    assert result["direct_final_stage_eligible"] is False
    assert result["structural_reauthoring_eligible"] is False
