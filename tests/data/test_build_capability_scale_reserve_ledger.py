import copy
import hashlib
import json
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_capability_scale_reserve_ledger import extend_ledger


def _queue(tmp_path: Path, *, duplicate_source: bool = False) -> tuple[Path, Path, list[dict]]:
    rows = []
    for index in range(120):
        cell = f"cap-{index}/python/generation"
        count = 2 if index < 45 else 1
        for cohort, ordinal in [("first_pass", 0)] + [("reserve", value) for value in range(1, count + 1)]:
            identifier = f"c{index}-{cohort}-{ordinal}"
            row = {
                "schema_version": "request/v1", "id": identifier, "cell_id": cell,
                "cohort": cohort, "source_queue_id": "duplicate" if duplicate_source and len(rows) == 1 else f"source-{identifier}",
                "source": {
                    "dataset": "fixture", "revision": "r1", "record_id": f"record-{identifier}",
                    "source_record_sha256": canonical_sha256({"source": identifier}),
                },
                "evaluation_artifacts_read": 0,
            }
            if duplicate_source and len(rows) == 1:
                row["source_queue_id"] = rows[0]["source_queue_id"]
            row["request_sha256"] = canonical_sha256(row)
            rows.append(row)
    path = tmp_path / "queue.jsonl"
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    manifest = {
        "schema_version": "queue-manifest/v1", "queue_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "reserve_records": 165, "evaluation_artifacts_read": 0,
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return path, manifest_path, rows


def _selection(tmp_path: Path, name: str, candidate: dict, stage: str, status: str) -> tuple[Path, Path]:
    row = {
        "candidate_id": candidate["id"], "cell_id": candidate["cell_id"], "status": status,
        "evaluation_artifacts_read": 0,
    }
    row["artifact_sha256"] = canonical_sha256(row)
    rows_path = tmp_path / f"{name}.jsonl"
    rows_path.write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    report = {
        "schema_version": "ganesh-mini-capability-scale-stage-selection/v1", "stage": stage,
        "selected": 1, "selected_ids": [row["candidate_id"]],
        "selected_artifact_sha256s": [row["artifact_sha256"]],
        "selected_rows_sha256": canonical_sha256([row]), "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    report_path = tmp_path / f"{name}.report.json"
    report_path.write_text(json.dumps(report), encoding="utf-8")
    return rows_path, report_path


def _write_ledger(path: Path, ledger: dict) -> None:
    path.write_text(json.dumps(ledger), encoding="utf-8")


def test_cumulative_chain_uses_next_same_cell_reserve_then_seals_exhaustion(tmp_path: Path) -> None:
    queue, manifest, rows = _queue(tmp_path)
    first = next(row for row in rows if row["id"] == "c0-first_pass-0")
    one = _selection(tmp_path, "teacher-failure", first, "teacher", "response-rejected")
    ledger1 = extend_ledger(queue, manifest, [one])
    assert ledger1["status"] == "active"
    assert ledger1["activations"][0]["replacement_candidate_id"] == "c0-reserve-1"
    assert ledger1["remaining_reserve_capacity"] == 164

    prior1 = tmp_path / "ledger1.json"; _write_ledger(prior1, ledger1)
    reserve1 = next(row for row in rows if row["id"] == "c0-reserve-1")
    two = _selection(tmp_path, "matrix-failure", reserve1, "matrix", "rejected")
    ledger2 = extend_ledger(queue, manifest, [two], prior1)
    assert ledger2["activations"][-1]["root_first_pass_id"] == first["id"]
    assert ledger2["activations"][-1]["replacement_candidate_id"] == "c0-reserve-2"
    assert len({row["replacement_candidate_id"] for row in ledger2["activations"]}) == 2

    prior2 = tmp_path / "ledger2.json"; _write_ledger(prior2, ledger2)
    reserve2 = next(row for row in rows if row["id"] == "c0-reserve-2")
    three = _selection(tmp_path, "delta-failure", reserve2, "delta", "semantic-rejected")
    ledger3 = extend_ledger(queue, manifest, [three], prior2)
    assert ledger3["status"] == "capacity-exhausted"
    assert ledger3["activation_count"] == 2
    assert ledger3["capacity_exhaustions"][0]["root_first_pass_id"] == first["id"]
    body = copy.deepcopy(ledger3)
    assert body.pop("ledger_sha256") == canonical_sha256(body)


def test_ledger_handles_failures_from_multiple_stages_in_one_extension(tmp_path: Path) -> None:
    queue, manifest, rows = _queue(tmp_path)
    first0 = next(row for row in rows if row["id"] == "c0-first_pass-0")
    first1 = next(row for row in rows if row["id"] == "c1-first_pass-0")
    selections = [
        _selection(tmp_path, "semantic", first0, "semantic", "rejected"),
        _selection(tmp_path, "test", first1, "test-author", "response-contract-rejected"),
    ]
    ledger = extend_ledger(queue, manifest, selections)
    assert [row["failed_stage"] for row in ledger["activations"]] == ["semantic", "test-author"]
    assert len({row["replacement_source_queue_id"] for row in ledger["activations"]}) == 2


def test_ledger_rejects_duplicate_failure_or_unrelated_reserve_chain(tmp_path: Path) -> None:
    queue, manifest, rows = _queue(tmp_path)
    first = next(row for row in rows if row["id"] == "c0-first_pass-0")
    selection = _selection(tmp_path, "failure", first, "teacher", "failed")
    with pytest.raises(ValueError, match="already activated"):
        extend_ledger(queue, manifest, [selection, selection])

    unrelated = next(row for row in rows if row["id"] == "c2-reserve-1")
    reserve_failure = _selection(tmp_path, "orphan", unrelated, "delta", "rejected")
    with pytest.raises(ValueError, match="not part of an existing chain"):
        extend_ledger(queue, manifest, [reserve_failure])


def test_ledger_rejects_nonunique_queue_source_identity(tmp_path: Path) -> None:
    queue, manifest, _ = _queue(tmp_path, duplicate_source=True)
    with pytest.raises(ValueError, match="identity is not unique"):
        extend_ledger(queue, manifest, [])
