import copy
import json
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.select_capability_scale_stage import select_stage


def _write_stage(tmp_path: Path) -> tuple[Path, Path]:
    rows = []
    for identifier, status in (("a", "passed"), ("b", "rejected"), ("c", "response-rejected")):
        row = {
            "candidate_id": identifier, "cell_id": f"cell/{identifier}", "status": status,
            "evaluation_artifacts_read": 0,
        }
        row["artifact_sha256"] = canonical_sha256(row)
        rows.append(row)
    rows_path = tmp_path / "terminal.jsonl"
    rows_path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    report = {
        "schema_version": "test-report/v1", "status": "complete", "requested": 3,
        "terminal_rows_sha256": canonical_sha256(rows),
        "terminal_artifact_sha256s": [row["artifact_sha256"] for row in rows],
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    report_path = tmp_path / "report.json"
    report_path.write_text(json.dumps(report), encoding="utf-8")
    return rows_path, report_path


def test_selector_binds_parent_and_exact_selected_outputs(tmp_path: Path) -> None:
    rows_path, report_path = _write_stage(tmp_path)
    rows, report = select_stage(
        rows_path, report_path, {"rejected", "response-rejected"},
        stage="teacher", rows_hash_field="terminal_rows_sha256",
    )
    assert [row["candidate_id"] for row in rows] == ["b", "c"]
    assert report["selected_ids"] == ["b", "c"]
    assert report["selected_artifact_sha256s"] == [row["artifact_sha256"] for row in rows]
    assert report["selected_rows_sha256"] == canonical_sha256(rows)
    body = copy.deepcopy(report)
    assert body.pop("report_sha256") == canonical_sha256(body)


def test_selector_rejects_tampered_terminal_row_even_if_report_hash_is_resealed(tmp_path: Path) -> None:
    rows_path, report_path = _write_stage(tmp_path)
    rows = [json.loads(line) for line in rows_path.read_text().splitlines()]
    rows[1]["status"] = "passed"
    rows_path.write_text("".join(json.dumps(row) + "\n" for row in rows))
    report = json.loads(report_path.read_text())
    report.pop("report_sha256")
    report["terminal_rows_sha256"] = canonical_sha256(rows)
    report["report_sha256"] = canonical_sha256(report)
    report_path.write_text(json.dumps(report))
    with pytest.raises(ValueError, match="invalid artifact_sha256"):
        select_stage(rows_path, report_path, {"rejected"}, stage="semantic", rows_hash_field="terminal_rows_sha256")


def test_selector_requires_complete_parent_binding(tmp_path: Path) -> None:
    rows_path, report_path = _write_stage(tmp_path)
    rows = rows_path.read_text().splitlines()
    rows_path.write_text("\n".join(rows[:-1]) + "\n")
    with pytest.raises(ValueError, match="does not bind all terminal"):
        select_stage(rows_path, report_path, {"rejected"}, stage="delta", rows_hash_field="terminal_rows_sha256")
