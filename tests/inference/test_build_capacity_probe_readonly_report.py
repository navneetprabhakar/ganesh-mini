from scripts.inference.build_capacity_probe_readonly_report import build, canonical_sha256


def test_builds_complete_non_executable_report() -> None:
    report = build()
    claimed = report.pop("report_sha256")
    assert claimed == canonical_sha256(report)
    assert report["status"] == "complete-ready-for-separate-proposal"
    assert report["conclusion"]["prerequisites_passed"] is True
    assert report["conclusion"]["execution_authorized"] is False
    assert report["provider"]["capacity_claimed"] is False
    assert len(report["inputs"]) == 10
    assert all(row["metadata_match"] for row in report["inputs"].values())
