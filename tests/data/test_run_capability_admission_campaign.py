from __future__ import annotations

import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.generate_capability_qualification import LANES
from scripts.data.run_capability_admission_campaign import (
    ASSEMBLY_SCHEMA,
    discover_batches,
    input_bindings,
    run_campaign,
)


def teacher_dirs(tmp_path: Path) -> tuple[Path, Path]:
    candidates = tmp_path / "candidates"
    evidence = tmp_path / "evidence"
    candidates.mkdir(); evidence.mkdir()
    for lane in LANES:
        for index in range(4):
            stem = f"{lane}-{index:03d}"
            (candidates / f"{stem}.candidates.jsonl").write_text("", encoding="utf-8")
            (evidence / f"{stem}.evidence.json").write_text("{}\n", encoding="utf-8")
    return candidates, evidence


def inputs(tmp_path: Path) -> dict[str, Path]:
    values = {}
    for name in ("plan", "queue", "queue_manifest", "semantic", "separation", "config", "runtime"):
        path = tmp_path / f"{name}.json"
        path.write_text("{}\n", encoding="utf-8")
        values[name] = path
    return values


def plan() -> dict:
    cells = [{"cell_id": f"cell-{index}"} for index in range(120)]
    value = {
        "schema_version": "ganesh-mini-capability-stratified-corpus-plan/v1",
        "matrix": {"cells": 120, "cell_contracts": cells},
        "qualification": {"drafts": 240, "minimum_admitted": 120, "minimum_admitted_per_cell": 1},
    }
    value["plan_sha256"] = canonical_sha256(value)
    return value


def sealed_assembly(path: Path, report_path: Path, envelopes: list[dict] | None = None) -> tuple[list[dict], dict]:
    envelopes = envelopes or [{"id": "fixture-envelope"}]
    path.write_text("".join(json.dumps(row) + "\n" for row in envelopes), encoding="utf-8")
    report = {
        "schema_version": ASSEMBLY_SCHEMA, "status": "ready-for-executable-admission",
        "records": len(envelopes),
    }
    report["report_sha256"] = canonical_sha256(report)
    report_path.write_text(json.dumps(report) + "\n", encoding="utf-8")
    return envelopes, report


def campaign_kwargs(tmp_path: Path) -> dict:
    candidates, evidence = teacher_dirs(tmp_path)
    value = inputs(tmp_path)
    return {
        "plan_path": value["plan"], "queue_path": value["queue"],
        "queue_manifest_path": value["queue_manifest"],
        "candidate_dir": candidates, "evidence_dir": evidence,
        "semantic_path": value["semantic"], "separation_path": value["separation"],
        "config_path": value["config"], "runtime_config_path": value["runtime"],
        "output_root": tmp_path / "output", "record_workers": 4, "verifier_workers": 2,
    }


def test_discovers_exact_24_lane_batches_and_rejects_extras(tmp_path: Path) -> None:
    candidates, evidence = teacher_dirs(tmp_path)
    candidate_paths, evidence_paths = discover_batches(candidates, evidence)
    assert len(candidate_paths) == len(evidence_paths) == 24
    assert candidate_paths[0].name == "go-000.candidates.jsonl"
    (candidates / "extra.candidates.jsonl").write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="exactly the 24"):
        discover_batches(candidates, evidence)


def test_optional_correction_report_binds_report_and_corrected_artifact(tmp_path: Path) -> None:
    candidates, evidence = teacher_dirs(tmp_path)
    candidate_paths, evidence_paths = discover_batches(candidates, evidence)
    value = inputs(tmp_path)
    corrected = tmp_path / "corrected.jsonl"
    corrected.write_text("{}\n", encoding="utf-8")
    correction_report = tmp_path / "correction.json"
    correction_report.write_text(json.dumps({"output": {"path": str(corrected)}}), encoding="utf-8")
    bindings = input_bindings(
        plan_path=value["plan"], queue_path=value["queue"],
        queue_manifest_path=value["queue_manifest"], candidate_paths=candidate_paths,
        evidence_paths=evidence_paths, semantic_path=value["semantic"],
        separation_path=value["separation"], config_path=value["config"],
        runtime_config_path=value["runtime"], record_workers=4, verifier_workers=2,
        correction_report_path=correction_report,
    )
    assert bindings["correction"]["report"]["sha256"]
    assert bindings["correction"]["corrected_candidates"]["sha256"] == hashlib.sha256(corrected.read_bytes()).hexdigest()


def test_runs_final_campaign_and_exact_completed_campaign_is_resumable(tmp_path: Path) -> None:
    kwargs = campaign_kwargs(tmp_path)
    queue = {}
    envelopes = []
    admitted = [
        {"qualification": {"cell_id": f"cell-{index}"}, "record": {"id": f"id-{index}"}}
        for index in range(120)
    ]
    rejected = []
    for index in range(120):
        for ordinal in range(2):
            identifier = f"q-{index}-{ordinal}"
            source = {"dataset": "fixture", "revision": "abc", "record_id": identifier}
            row = {
                "id": identifier, "cell_id": f"cell-{index}", "primary_capability": f"cap-{index}",
                "assigned_cross_cutting_dimension": "malformed_input", "source_queue_id": f"source-{identifier}",
                "lane": "python", "task_type": "generation", "source": source,
            }
            queue[identifier] = row
            envelopes.append({
                "schema_version": "ganesh-mini-capability-qualification-envelope/v1",
                "candidate": {"id": identifier, "lane": "python", "task_type": "generation", "source": source},
                "qualification": {
                    "queue_id": identifier, "cell_id": row["cell_id"], "primary_capability": row["primary_capability"],
                    "assigned_cross_cutting_dimension": row["assigned_cross_cutting_dimension"],
                    "source_queue_id": row["source_queue_id"],
                },
            })
            if ordinal == 1:
                rejected.append({"line": len(envelopes), "id": identifier, "reason": "not admitted"})

    def assembly(**values):
        return sealed_assembly(values["output_path"], values["report_path"], envelopes)

    with (
        patch("scripts.data.run_capability_admission_campaign.load_sealed", return_value=plan()),
        patch("scripts.data.run_capability_admission_campaign.load_teacher_queue", return_value=(list(queue.values()), {"manifest_sha256": "m"})),
        patch("scripts.data.run_capability_admission_campaign.load_admission_queue", return_value=queue),
        patch("scripts.data.run_capability_admission_campaign.load_report", side_effect=[{"report_sha256": "s"}, {"report_sha256": "x"}]),
        patch("scripts.data.run_capability_admission_campaign._load_or_build_assembly", side_effect=assembly),
        patch("scripts.data.run_capability_admission_campaign.admit_qualification", return_value=(admitted, rejected)) as admit,
    ):
        report = run_campaign(**kwargs)
    assert report["status"] == "qualification-passed"
    assert report["resumption"] == {"assembly_reused": False, "admission_reused": False}
    assert admit.call_args.kwargs["record_workers"] == 4
    assert admit.call_args.kwargs["verifier_workers"] == 2
    for name in ("admission-envelopes.jsonl", "admitted.jsonl", "rejected.json", "admission-report.json", "campaign-report.json"):
        assert (kwargs["output_root"] / name).is_file()

    # A sealed completed campaign returns before loading inputs or invoking a verifier.
    with patch("scripts.data.run_capability_admission_campaign.load_sealed", side_effect=AssertionError("must not rerun")):
        resumed = run_campaign(**kwargs)
    assert resumed["report_sha256"] == report["report_sha256"]


def test_valid_negative_admission_is_reported_as_gate_failure_not_execution_error(tmp_path: Path) -> None:
    kwargs = campaign_kwargs(tmp_path)

    def assembly(**values):
        return sealed_assembly(values["output_path"], values["report_path"])

    with (
        patch("scripts.data.run_capability_admission_campaign.load_sealed", return_value=plan()),
        patch("scripts.data.run_capability_admission_campaign.load_teacher_queue", return_value=([{"id": "q"}], {"manifest_sha256": "m"})),
        patch("scripts.data.run_capability_admission_campaign.load_admission_queue", return_value={"q": {}}),
        patch("scripts.data.run_capability_admission_campaign.load_report", side_effect=[{"report_sha256": "s"}, {"report_sha256": "x"}]),
        patch("scripts.data.run_capability_admission_campaign._load_or_build_assembly", side_effect=assembly),
        patch("scripts.data.run_capability_admission_campaign.admit_qualification", return_value=([], [{"line": 1, "id": "q", "reason": "failed"}])),
    ):
        report = run_campaign(**kwargs)
    assert report["status"] == "qualification-failed"
    assert report["outputs"]["rejected"]["bytes"] > 0


def test_rejects_unbounded_parallelism_before_admission(tmp_path: Path) -> None:
    kwargs = campaign_kwargs(tmp_path)
    kwargs["record_workers"] = 8
    kwargs["verifier_workers"] = 4
    with pytest.raises(ValueError, match="bounds exceeded"):
        run_campaign(**kwargs)
