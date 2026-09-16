from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

import scripts.data.summarize_repair_delta_qualification as subject
from scripts.data.build_capability_corpus_plan import canonical_sha256


CAPABILITIES = tuple(f"cap-{index}" for index in range(10))
DIMENSIONS = tuple(f"dimension-{index}" for index in range(5))


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows))


def seal(value: dict, field: str = "report_sha256") -> dict:
    value[field] = canonical_sha256(value)
    return value


def admission(
    path: Path, envelopes: Path, rejected_ids: set[str], unresolved_ids: set[str] | None = None,
) -> Path:
    unresolved_ids = unresolved_ids or set()
    rows = [json.loads(line) for line in envelopes.read_text().splitlines()]
    admitted_rows = []
    rejected_rows = []
    for row in rows:
        candidate = row["candidate"]
        qualification = row.get("assignment", row.get("qualification"))
        if candidate["id"] in rejected_ids:
            rejected_rows.append({"id": candidate["id"], "reason": "measured reject"})
        else:
            if row.get("schema_version") == "ganesh-mini-repair-delta-envelope/v1":
                admitted_rows.append({
                    "schema_version": "ganesh-mini-repair-delta-admitted/v1",
                    "id": candidate["id"], "cell_id": qualification["cell_id"],
                    "lane": candidate["lane"],
                    "primary_capability": qualification["primary_capability"],
                    "assigned_cross_cutting_dimension": qualification[
                        "assigned_cross_cutting_dimension"
                    ],
                    "candidate": candidate, "evidence_sha256s": {},
                    "proof_consistency_sha256": "a" * 64,
                })
            else:
                admitted_rows.append({
                    "record": {"id": candidate["id"]},
                    "qualification": {
                        "queue_id": candidate["id"], "cell_id": qualification["cell_id"],
                        "lane": candidate["lane"],
                        "primary_capability": qualification["primary_capability"],
                        "assigned_cross_cutting_dimension": qualification.get(
                            "assigned_cross_cutting_dimension"
                        ),
                    },
                })
    admitted_path = path.with_suffix(".admitted.jsonl")
    rejected_path = path.with_suffix(".rejected.json")
    unresolved_rows = [
        {"id": identifier, "cell_id": "recorded-by-assembly",
         "terminal_stage": "executable", "reason": "timeout"}
        for identifier in sorted(unresolved_ids)
    ]
    # Move explicit unresolved IDs out of either admitted or rejected fixtures.
    admitted_rows = [row for row in admitted_rows if row.get("id", row.get("record", {}).get("id")) not in unresolved_ids]
    rejected_rows = [row for row in rejected_rows if row["id"] not in unresolved_ids]
    unresolved_path = path.with_suffix(".unresolved.json")
    write_jsonl(admitted_path, admitted_rows)
    rejected_path.write_text(json.dumps(rejected_rows) + "\n")
    unresolved_path.write_text(json.dumps(unresolved_rows) + "\n")
    is_v3 = bool(rows) and rows[0].get("schema_version") == "ganesh-mini-repair-delta-envelope/v1"
    report = {
        "schema_version": (
            "ganesh-mini-repair-delta-admission-report/v1" if is_v3
            else "ganesh-mini-capability-qualification-admission/v1"
        ),
        "status": ("admission-complete" if not rejected_rows else "failed") if is_v3 else (
            "passed" if not rejected_rows else "failed"
        ),
        "input": {
            "path": str(envelopes), "sha256": subject.file_sha256(envelopes),
            "bytes": envelopes.stat().st_size,
        },
        "accepted": len(admitted_rows), "rejected": len(rejected_rows),
        "outputs": {
            "admitted": {
                "path": str(admitted_path), "sha256": subject.file_sha256(admitted_path),
                "bytes": admitted_path.stat().st_size,
            },
            "rejected": {
                "path": str(rejected_path), "sha256": subject.file_sha256(rejected_path),
                "bytes": rejected_path.stat().st_size,
            },
        },
    }
    if is_v3:
        report.update({
            "contract_id": subject.CONTRACT_ID, "unresolved": len(unresolved_rows),
            "runtime_config_sha256": "1" * 64, "admission_config_sha256": "2" * 64,
            "sandbox_contract_sha256": "3" * 64, "separation_contract_sha256": "4" * 64,
            "counts_by_lane": dict(sorted(__import__("collections").Counter(
                row["lane"] for row in admitted_rows
            ).items())), "evaluation_artifacts_read": 0,
        })
        report["outputs"]["unresolved"] = {
            "path": str(unresolved_path), "sha256": subject.file_sha256(unresolved_path),
            "bytes": unresolved_path.stat().st_size,
        }
    else:
        report["mode"] = "final"
    path.write_text(json.dumps(seal(report)))
    return path


def setup_contract(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Path | list[dict]]:
    plan = tmp_path / "plan.md"
    plan.write_text("frozen repair delta plan\n")
    monkeypatch.setattr(subject, "PLAN_SHA256", subject.file_sha256(plan))

    queue_rows = []
    cells = []
    ordinal = 0
    for capability in CAPABILITIES:
        for lane in subject.LANES:
            dimension = DIMENSIONS[ordinal % len(DIMENSIONS)]
            cell = f"{capability}/{lane}/repair"
            cells.append(cell)
            for cohort in (subject.FIRST_PASS, subject.RESERVE):
                role = "primary" if cohort == subject.FIRST_PASS else "reserve"
                queue_rows.append({
                    "id": f"v3-{cohort}-{ordinal}", "role": role,
                    "generation_eligible": role == "primary", "cell_id": cell,
                    "primary_capability": capability, "lane": lane, "task_type": "repair",
                    "assigned_cross_cutting_dimension": dimension,
                    "source": {
                        "dataset": "source-a" if ordinal % 2 else "source-b",
                        "revision": "rev", "record_id": f"{cohort}-{ordinal}",
                    },
                })
            ordinal += 1
    queue = tmp_path / "queue.jsonl"
    write_jsonl(queue, queue_rows)
    manifest = tmp_path / "queue-manifest.json"
    manifest_value = {
        "schema_version": subject.QUEUE_SCHEMA, "plan_sha256": subject.PLAN_SHA256,
        "status": "sealed-primary-generation-eligible", "seed": subject.QUEUE_SEED,
        "queue_sha256": subject.file_sha256(queue),
        "assignments": 120, "primary_assignments": 60, "cell_bound_reserves": 60,
        "initial_generation_eligible": 60, "maximum_reserve_generation_eligible": 6,
        "absolute_candidate_budget": 66, "unique_source_identities": 120,
        "dataset_counts": {"primary": {"source-a": 30, "source-b": 30},
                           "reserve": {"source-a": 30, "source-b": 30}},
        "evaluation_artifacts_read": 0,
    }
    manifest.write_text(json.dumps(seal(manifest_value, "manifest_sha256")))

    v2_envelopes = tmp_path / "v2-envelopes.jsonl"
    v2_rows = []
    for index, cell in enumerate(cells):
        capability, lane, _ = cell.split("/")
        for copy in range(2):
            identifier = f"v2-generation-{index}-{copy}"
            nested = {
                "teacher": {"kind": "teacher"},
                "test_author": {"kind": "test_author"},
                "semantic_review": {"kind": "semantic_review", "verdict": "pass"},
                "separation": {"kind": "separation"},
                "lineage": {"kind": "lineage"},
            }
            for item in nested.values():
                item["evidence_sha256"] = canonical_sha256(item)
            v2_rows.append({
                "candidate": {"id": identifier, "lane": lane, "task_type": "generation"},
                "qualification": {
                    "queue_id": identifier, "cell_id": f"{capability}/{lane}/generation",
                    "primary_capability": capability,
                    "evidence": nested,
                },
            })
    write_jsonl(v2_envelopes, v2_rows)
    v2_rejected = {f"v2-generation-{index}-1" for index in range(6)}
    v2_admission = admission(tmp_path / "v2-admission.json", v2_envelopes, v2_rejected)
    v2_admission_value = json.loads(v2_admission.read_text())
    monkeypatch.setattr(subject, "V2_ADMISSION_SHA256", v2_admission_value["report_sha256"])
    v2_summary = tmp_path / "v2-summary.json"
    v2_summary_value = seal({"schema_version": "v2-summary", "status": "qualification-failed"})
    v2_summary.write_text(json.dumps(v2_summary_value))
    monkeypatch.setattr(subject, "V2_SUMMARY_SHA256", v2_summary_value["report_sha256"])
    return {
        "plan": plan, "queue": queue, "manifest": manifest,
        "queue_rows": [dict(row, cohort=(
            subject.FIRST_PASS if row["role"] == "primary" else subject.RESERVE
        )) for row in queue_rows],
        "v2_envelopes": v2_envelopes, "v2_admission": v2_admission, "v2_summary": v2_summary,
    }


def cohort_envelopes(tmp_path: Path, queue_rows: list[dict], cohort: str) -> Path:
    path = tmp_path / f"{cohort}-envelopes.jsonl"
    rows = []
    for row in queue_rows:
        if row["cohort"] != cohort:
            continue
        rows.append({
            "schema_version": "ganesh-mini-repair-delta-envelope/v1",
            "candidate": {
                "id": row["id"], "lane": row["lane"], "task_type": "repair",
                "qualification_assignment": {
                    "cell_id": row["cell_id"], "primary_capability": row["primary_capability"],
                    "assigned_cross_cutting_dimension": row["assigned_cross_cutting_dimension"],
                },
            },
            "assignment": {
                "contract_id": subject.CONTRACT_ID, "cell_id": row["cell_id"],
                "primary_capability": row["primary_capability"],
                "assigned_cross_cutting_dimension": row["assigned_cross_cutting_dimension"],
            },
        })
    write_jsonl(path, rows)
    return path


def call(paths: dict, **extra):
    return subject.summarize(
        plan_path=paths["plan"], queue_path=paths["queue"],
        queue_manifest_path=paths["manifest"], v2_summary_path=paths["v2_summary"],
        v2_admission_path=paths["v2_admission"], v2_envelopes_path=paths["v2_envelopes"],
        **extra,
    )


def test_six_reserves_close_all_cells_after_passing_first_pass(tmp_path: Path, monkeypatch) -> None:
    paths = setup_contract(tmp_path, monkeypatch)
    first = cohort_envelopes(tmp_path, paths["queue_rows"], subject.FIRST_PASS)
    # One reject per lane, spread across capabilities and no more than two per dimension.
    first_ids = [row["id"] for row in paths["queue_rows"] if row["cohort"] == subject.FIRST_PASS]
    rejected = {first_ids[index] for index in (0, 11, 22, 33, 44, 55)}
    first_report = admission(tmp_path / "first-report.json", first, rejected)
    rejected_cells = {
        row["cell_id"] for row in paths["queue_rows"]
        if row["cohort"] == subject.FIRST_PASS and row["id"] in rejected
    }
    reserve_rows = [
        row for row in paths["queue_rows"]
        if row["cohort"] == subject.RESERVE and row["cell_id"] in rejected_cells
    ]
    reserve = cohort_envelopes(tmp_path, reserve_rows, subject.RESERVE)
    reserve_report = admission(tmp_path / "reserve-report.json", reserve, set())

    report = call(
        paths, first_envelopes_path=first, first_admission_path=first_report,
        reserve_envelopes_path=reserve, reserve_admission_path=reserve_report,
    )

    assert report["status"] == "qualification-passed-via-v3-repair-delta"
    assert report["generation_equivalence"]["semantic_passed"] == 120
    assert report["generation_equivalence"]["admitted"] == 114
    assert report["first_pass"]["admitted"] == 54
    assert report["reserves"]["generated"] == 6
    assert report["final"]["repair_cells_covered"] == 60
    assert report["final"]["combined_cells_covered"] == 120
    body = dict(report)
    assert body.pop("report_sha256") == canonical_sha256(body)


def test_partial_first_pass_is_in_progress_and_reserves_are_not_eligible(tmp_path: Path, monkeypatch) -> None:
    paths = setup_contract(tmp_path, monkeypatch)
    selected = [row for row in paths["queue_rows"] if row["cohort"] == subject.FIRST_PASS][:20]
    first = cohort_envelopes(tmp_path, selected, subject.FIRST_PASS)
    first_report = admission(tmp_path / "first-report.json", first, set())

    report = call(paths, first_envelopes_path=first, first_admission_path=first_report)

    assert report["status"] == "qualification-in-progress"
    assert report["first_pass"]["thresholds"]["complete_60"] is False
    assert report["reserves"]["eligible_cells"] == []


def test_unresolved_first_pass_is_not_rejected_or_terminally_dispositioned(tmp_path: Path, monkeypatch) -> None:
    paths = setup_contract(tmp_path, monkeypatch)
    first = cohort_envelopes(tmp_path, paths["queue_rows"], subject.FIRST_PASS)
    unresolved_id = next(
        row["id"] for row in paths["queue_rows"] if row["cohort"] == subject.FIRST_PASS
    )
    first_report = admission(
        tmp_path / "first-report.json", first, set(), unresolved_ids={unresolved_id},
    )

    report = call(paths, first_envelopes_path=first, first_admission_path=first_report)

    assert report["status"] == "qualification-in-progress"
    assert report["first_pass"]["generated"] == 60
    assert report["first_pass"]["dispositioned"] == 59
    assert report["first_pass"]["rejected"] == 0
    assert report["first_pass"]["unresolved"] == 1
    assert report["first_pass"]["thresholds"]["complete_60"] is False
    assert report["reserves"]["eligible_cells"] == []


def test_failed_first_pass_forbids_reserve_generation(tmp_path: Path, monkeypatch) -> None:
    paths = setup_contract(tmp_path, monkeypatch)
    first = cohort_envelopes(tmp_path, paths["queue_rows"], subject.FIRST_PASS)
    first_ids = [row["id"] for row in paths["queue_rows"] if row["cohort"] == subject.FIRST_PASS]
    first_report = admission(tmp_path / "first-report.json", first, set(first_ids[:7]))
    reserve_row = next(row for row in paths["queue_rows"] if row["cohort"] == subject.RESERVE)
    reserve = cohort_envelopes(tmp_path, [reserve_row], subject.RESERVE)
    reserve_report = admission(tmp_path / "reserve-report.json", reserve, set())

    with pytest.raises(ValueError, match="before every first-pass threshold"):
        call(
            paths, first_envelopes_path=first, first_admission_path=first_report,
            reserve_envelopes_path=reserve, reserve_admission_path=reserve_report,
        )


def test_v2_semantic_or_admission_equivalence_failure_is_terminal(tmp_path: Path, monkeypatch) -> None:
    paths = setup_contract(tmp_path, monkeypatch)
    rows = [json.loads(line) for line in paths["v2_envelopes"].read_text().splitlines()]
    semantic = rows[0]["qualification"]["evidence"]["semantic_review"]
    semantic["verdict"] = "reject"
    semantic.pop("evidence_sha256")
    semantic["evidence_sha256"] = canonical_sha256(semantic)
    write_jsonl(paths["v2_envelopes"], rows)
    # Reseal admission around the modified input while preserving the frozen report identity override.
    paths["v2_admission"] = admission(
        tmp_path / "v2-admission-modified.json", paths["v2_envelopes"],
        {f"v2-generation-{index}-1" for index in range(6)},
    )
    monkeypatch.setattr(
        subject, "V2_ADMISSION_SHA256",
        json.loads(paths["v2_admission"].read_text())["report_sha256"],
    )

    report = call(paths)

    assert report["status"] == "qualification-failed"
    assert report["generation_equivalence"]["passed"] is False


def test_queue_manifest_and_admission_hashes_fail_closed(tmp_path: Path, monkeypatch) -> None:
    paths = setup_contract(tmp_path, monkeypatch)
    manifest = json.loads(paths["manifest"].read_text())
    manifest["queue_sha256"] = "0" * 64
    paths["manifest"].write_text(json.dumps(seal({k: v for k, v in manifest.items() if k != "manifest_sha256"}, "manifest_sha256")))

    with pytest.raises(ValueError, match="queue differs"):
        call(paths)


def test_more_than_six_reserves_fails_closed(tmp_path: Path, monkeypatch) -> None:
    paths = setup_contract(tmp_path, monkeypatch)
    first = cohort_envelopes(tmp_path, paths["queue_rows"], subject.FIRST_PASS)
    first_ids = [row["id"] for row in paths["queue_rows"] if row["cohort"] == subject.FIRST_PASS]
    first_report = admission(tmp_path / "first-report.json", first, set(first_ids[:7]))
    reserve_rows = [row for row in paths["queue_rows"] if row["cohort"] == subject.RESERVE][:7]
    reserve = cohort_envelopes(tmp_path, reserve_rows, subject.RESERVE)
    reserve_report = admission(tmp_path / "reserve-report.json", reserve, set())

    with pytest.raises(ValueError, match="exceed six"):
        call(
            paths, first_envelopes_path=first, first_admission_path=first_report,
            reserve_envelopes_path=reserve, reserve_admission_path=reserve_report,
        )
