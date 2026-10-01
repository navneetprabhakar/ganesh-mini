import argparse
import json

import pytest

from scripts.data.assess_capability_go_requalification import assess
from scripts.data.build_capability_corpus_plan import canonical_sha256


def _seal(value, field):
    value[field] = canonical_sha256(value)
    return value


def _write_json(path, value):
    path.write_text(json.dumps(value) + "\n", encoding="utf-8")


def _write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def _fixture(tmp_path, changed=None):
    changed = changed or {}
    parent = []
    for index in range(534):
        lane = "go" if index < 89 else "java"
        status = ("admitted" if index < 51 else "rejected" if index < 55 else "unresolved") if lane == "go" else "admitted"
        parent.append(_seal({
            "candidate_id": f"candidate-{index}", "lane": lane, "status": status,
            "input_sha256": f"input-{index}", "evaluation_artifacts_read": 0,
        }, "artifact_sha256"))
    new = []
    for index, old in enumerate(parent[:89]):
        row = {key: value for key, value in old.items() if key != "artifact_sha256"}
        row["status"] = changed.get(index, "admitted" if index < 51 or index >= 55 else "rejected")
        new.append(_seal(row, "artifact_sha256"))
    ids = [row["candidate_id"] for row in new]
    parent_report = _seal({
        "requested": 534, "terminal_rows_sha256": canonical_sha256(parent),
        "evaluation_artifacts_read": 0,
    }, "report_sha256")
    go_report = _seal({
        "requested": 89, "terminal_rows_sha256": canonical_sha256(new),
        "ordered_candidate_ids": ids,
        "terminal_artifact_sha256s": [row["artifact_sha256"] for row in new],
        "evaluation_artifacts_read": 0,
    }, "report_sha256")
    manifest = _seal({
        "status": "ready", "selected": 89, "workers": 1,
        "candidate_or_runtime_mutation": False, "evaluation_artifacts_read": 0,
        "parent_report_sha256s": {"matrix": parent_report["report_sha256"]},
        "ordered_candidate_ids": ids,
        "original_input_sha256s": [row["input_sha256"] for row in parent[:89]],
        "original_artifact_sha256s": [row["artifact_sha256"] for row in parent[:89]],
        "original_statuses": [row["status"] for row in parent[:89]],
    }, "manifest_sha256")
    paths = {name: tmp_path / name for name in (
        "input_manifest", "parent_report", "parent_artifacts", "go_report", "go_artifacts",
    )}
    for name, value in (("input_manifest", manifest), ("parent_report", parent_report), ("go_report", go_report)):
        _write_json(paths[name], value)
    _write_jsonl(paths["parent_artifacts"], parent)
    _write_jsonl(paths["go_artifacts"], new)
    return argparse.Namespace(**paths, output_dir=tmp_path / "output")


def test_accepts_uniform_complete_go_cohort(tmp_path):
    args = _fixture(tmp_path)
    report = assess(args)
    assert report["status"] == "accepted"
    assert report["go_counts"] == {"admitted": 85, "rejected": 4}
    combined = json.loads((args.output_dir / "matrix-report.json").read_text(encoding="utf-8"))
    assert combined["counts"] == {"admitted": 530, "rejected": 4}
    assert combined["terminal_rows_sha256"] == canonical_sha256([
        json.loads(line) for line in (args.output_dir / "terminal-artifacts.jsonl").read_text(encoding="utf-8").splitlines()
    ])


@pytest.mark.parametrize("changed,field", [
    ({0: "rejected"}, "regressed_original_admission_ids"),
    ({55: "unresolved"}, "unresolved_candidate_ids"),
])
def test_fails_closed_without_writing_combined_matrix(tmp_path, changed, field):
    args = _fixture(tmp_path, changed)
    report = assess(args)
    assert report["status"] == "failed"
    assert report[field]
    assert not (args.output_dir / "matrix-report.json").exists()


def test_rejects_changed_input_sha(tmp_path):
    args = _fixture(tmp_path)
    rows = [json.loads(line) for line in args.go_artifacts.read_text(encoding="utf-8").splitlines()]
    rows[0]["input_sha256"] = "changed"
    rows[0].pop("artifact_sha256")
    _seal(rows[0], "artifact_sha256")
    _write_jsonl(args.go_artifacts, rows)
    report = json.loads(args.go_report.read_text(encoding="utf-8"))
    report["terminal_rows_sha256"] = canonical_sha256(rows)
    report["terminal_artifact_sha256s"][0] = rows[0]["artifact_sha256"]
    report.pop("report_sha256")
    _write_json(args.go_report, _seal(report, "report_sha256"))
    with pytest.raises(ValueError, match="input or ordered artifact bindings drifted"):
        assess(args)
