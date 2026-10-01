from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pytest

from scripts.data.admit_repair_delta import teacher_candidate_sha256
from scripts.data.build_capability_corpus_plan import CAPABILITIES, canonical_sha256
from scripts.data.build_repair_delta_queue import repair_cells
from scripts.data.build_v5_interface_replay_cohort import (
    BUDGET_CLARIFICATION_ADDENDUM_SHA256, CONTRACT_ID, PLAN_SHA256,
    REPLACEMENT_CELLS, UNRESERVED_CELLS,
    V4_CONTRACT_ID, V4_PLAN_SHA256,
    build,
)


ROOT = Path(__file__).resolve().parents[2]


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def source(identifier: str, lane: str, index: int, dataset: str = "fixture") -> dict:
    return {
        "id": identifier, "lane": lane, "task_type": "repair",
        "stimulus": f"fixture repair stimulus {identifier}",
        "source": {
            "dataset": dataset, "revision": "r1", "record_id": f"record-{index}",
            "source_record_sha256": hashlib.sha256(f"source-{identifier}".encode()).hexdigest(),
            "license": "MIT",
        },
    }


def make_inputs(tmp_path: Path) -> argparse.Namespace:
    cells = repair_cells()
    v4_queue: list[dict] = []
    teacher_by_lane: dict[str, list[dict]] = {lane: [] for lane in {cell["lane"] for cell in cells}}
    for role in ("primary", "reserve"):
        for index, cell in enumerate(cells):
            identifier = f"cap-v4-{cell['primary_capability']}-{cell['lane']}-repair-{role}"
            src = source(f"v4-source-{role}-{index}", cell["lane"], index + (0 if role == "primary" else 1000), "v4")
            queue_row = {
                "id": identifier, "role": role, "cell_id": cell["cell_id"],
                "lane": cell["lane"], "primary_capability": cell["primary_capability"],
                "primary_capability_definition": CAPABILITIES[cell["primary_capability"]],
                "assigned_cross_cutting_dimension": cell["assigned_cross_cutting_dimension"],
                "source_queue_id": src["id"], "source": src["source"],
                "source_affinity_evidence_sha256": "a" * 64,
                "source_separation_attestation_sha256": "b" * 64,
            }
            v4_queue.append(queue_row)
            if role == "primary":
                candidate = {
                    "id": identifier, "lane": cell["lane"], "task_type": "repair",
                    "source": src["source"], "verification_task": {"files": []},
                }
                proof = {
                    "candidate_id": identifier,
                    "teacher_candidate_sha256": teacher_candidate_sha256(candidate),
                    "queue_record_sha256": canonical_sha256(queue_row),
                    "teacher_run_evidence_sha256": hashlib.sha256(identifier.encode()).hexdigest(),
                }
                proof["evidence_sha256"] = canonical_sha256(proof)
                teacher_by_lane[cell["lane"]].append({"candidate": candidate, "repair_delta_proof": proof})
    v4_queue_path = tmp_path / "v4-queue.jsonl"; write_jsonl(v4_queue_path, v4_queue)
    v4_manifest = {
        "schema_version": "ganesh-mini-repair-delta-v4-queue-manifest/v1",
        "contract_id": V4_CONTRACT_ID, "plan_sha256": V4_PLAN_SHA256,
        "queue_sha256": hashlib.sha256(v4_queue_path.read_bytes()).hexdigest(), "assignments": 120,
    }
    v4_manifest["manifest_sha256"] = canonical_sha256(v4_manifest)
    v4_manifest_path = tmp_path / "v4-manifest.json"; write_json(v4_manifest_path, v4_manifest)
    candidate_paths: list[Path] = []; evidence_paths: list[Path] = []
    for lane in ("go", "java", "javascript", "typescript", "python", "rust"):
        candidate_path = tmp_path / f"teacher-{lane}.jsonl"; write_jsonl(candidate_path, teacher_by_lane[lane])
        ids = [row["candidate"]["id"] for row in teacher_by_lane[lane]]
        evidence = {
            "schema_version": "ganesh-mini-repair-delta-v4-teacher-batch/v1",
            "contract_id": V4_CONTRACT_ID, "plan_sha256": V4_PLAN_SHA256,
            "queue_manifest_sha256": v4_manifest["manifest_sha256"], "role": "primary",
            "lane": lane, "failures": [], "generated": 10, "requested_ids": ids,
            "candidate_output_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
            "evaluation_artifacts_read": 0,
        }
        evidence["evidence_sha256"] = canonical_sha256(evidence)
        evidence_path = tmp_path / f"teacher-{lane}-evidence.json"; write_json(evidence_path, evidence)
        candidate_paths.append(candidate_path); evidence_paths.append(evidence_path)

    source_rows: list[dict] = []; ontology_rows: list[dict] = []
    for index, cell in enumerate(cells):
        for alternate in range(2):
            src = source(f"fresh-{index}-{alternate}", cell["lane"], 10000 + index * 2 + alternate)
            source_rows.append(src)
            verdict = {
                "primary_capability": cell["primary_capability"], "decision": "accept",
                "capability_operation": "fixture operation", "defect_affordance": "fixture defect",
                "capability_operation_present": True, "identifiable_defect_affordance": True,
                "self_contained_standard_library_feasible": True, "code_repair_material": True,
                "forbidden_dependency_absent": True,
            }
            row = {
                "schema_version": "ganesh-mini-repair-source-ontology/v1",
                "source_queue_id": src["id"], "lane": src["lane"],
                "source_identity": {key: src["source"][key] for key in ("dataset", "revision", "record_id")},
                "source_record_sha256": src["source"]["source_record_sha256"],
                "separation_attestation_sha256": "c" * 64,
                "evaluation_artifacts_read": 0, "verdicts": [verdict],
            }
            row["evidence_sha256"] = canonical_sha256(row); ontology_rows.append(row)
    source_path = tmp_path / "sources.jsonl"; write_jsonl(source_path, source_rows)
    ontology_path = tmp_path / "ontology.jsonl"; write_jsonl(ontology_path, ontology_rows)
    summary = {
        "schema_version": "ganesh-mini-repair-source-ontology-aggregate/v1",
        "status": "coverage-complete", "combined_evidence_sha256": hashlib.sha256(ontology_path.read_bytes()).hexdigest(),
        "source_queue_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "unique_sources": 120, "evaluation_artifacts_read": 0,
    }
    summary["aggregate_sha256"] = canonical_sha256(summary)
    summary_path = tmp_path / "ontology-summary.json"; write_json(summary_path, summary)

    exclusions = []
    for name, idx in (("seed", 20000), ("v2", 20001), ("v3", 20002)):
        path = tmp_path / f"{name}.jsonl"; write_jsonl(path, [source(name, "go", idx, name)])
        exclusions.append(path)
    runtime = tmp_path / "runtime.json"; runtime.write_text("runtime", encoding="utf-8")
    preflight = tmp_path / "preflight.json"; preflight.write_text("preflight", encoding="utf-8")
    return argparse.Namespace(
        plan=ROOT / "docs/plans/GATE2_REPAIR_DELTA_V5_INTERFACE_REPLAY_PLAN_20260916.md",
        source_feasibility_addendum=(
            ROOT / "docs/plans/GATE2_V5_SOURCE_FEASIBILITY_ADDENDUM_20260916.md"
        ),
        budget_clarification_addendum=(
            ROOT / "docs/plans/GATE2_V5_BUDGET_CLARIFICATION_ADDENDUM_20260916.md"
        ),
        v4_queue=v4_queue_path, v4_queue_manifest=v4_manifest_path,
        v4_teacher_candidates=candidate_paths, v4_teacher_evidence=evidence_paths,
        source_queue=source_path, ontology_evidence=ontology_path, ontology_summary=summary_path,
        prior_corpus=exclusions[0], v2_artifact=[exclusions[1]], v3_queue=exclusions[2],
        runtime_config=runtime, preflight_config=preflight,
    )


def test_builds_exact_58_plus_2_ordered_cohort_and_59_unique_reserves(tmp_path: Path) -> None:
    args = make_inputs(tmp_path)
    ledger, carries, sources, cohort = build(args)
    assert PLAN_SHA256 == hashlib.sha256(args.plan.read_bytes()).hexdigest()
    assert carries["records"] == 58
    assert set(carries["excluded_replacement_cells"]) == set(REPLACEMENT_CELLS)
    assert sources["fresh_primary_sources"] == 2
    assert sources["prebound_reserve_sources"] == 59
    assert sources["unreserved_cells"] == list(UNRESERVED_CELLS)
    assert sources["unique_selected_source_identities"] == 61
    assert cohort["records"] == 60
    assert cohort["budget_clarification_addendum_sha256"] == BUDGET_CLARIFICATION_ADDENDUM_SHA256
    assert cohort["maximum_generated_reserves"] == 5
    assert [row["ordinal"] for row in cohort["rows"]] == list(range(60))
    assert {row["cell_id"] for row in cohort["rows"] if row["mode"] == "fresh-v5-teacher-primary"} == set(REPLACEMENT_CELLS)
    assert sum(row["mode"] == "immutable-v4-teacher-carry" for row in cohort["rows"]) == 58
    excluded = {(row["dataset"], row["revision"], row["record_id"]) for row in ledger["excluded_source_identities"]}
    selected = {tuple(row["source_identity"][key] for key in ("dataset", "revision", "record_id")) for row in sources["selections"]}
    assert excluded.isdisjoint(selected)
    assert len(selected) == 61
    assert all(row["v4_teacher_artifact"]["row_index"] >= 0 for row in carries["rows"])
    assert build(args) == (ledger, carries, sources, cohort)


def test_fails_closed_when_immutable_v4_proof_changes(tmp_path: Path) -> None:
    args = make_inputs(tmp_path)
    path = args.v4_teacher_candidates[0]
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    rows[0]["repair_delta_proof"]["teacher_run_evidence_sha256"] = "f" * 64
    write_jsonl(path, rows)
    evidence_path = args.v4_teacher_evidence[0]
    evidence = json.loads(evidence_path.read_text())
    evidence["candidate_output_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    evidence.pop("evidence_sha256"); evidence["evidence_sha256"] = canonical_sha256(evidence)
    write_json(evidence_path, evidence)
    with pytest.raises(ValueError, match="candidate, proof, and assignment do not bind"):
        build(args)


def test_fails_closed_when_fresh_matching_cannot_cover_a_cell(tmp_path: Path) -> None:
    args = make_inputs(tmp_path)
    sources = [json.loads(line) for line in args.source_queue.read_text().splitlines()]
    target_index = next(
        index for index, cell in enumerate(repair_cells())
        if cell["cell_id"] == REPLACEMENT_CELLS[0]
    )
    target_ids = {f"fresh-{target_index}-0", f"fresh-{target_index}-1"}
    # Remove every ontology edge for one cell while preserving sealed aggregate bindings.
    ontology = [json.loads(line) for line in args.ontology_evidence.read_text().splitlines()]
    ontology = [row for row in ontology if row["source_queue_id"] not in target_ids]
    write_jsonl(args.ontology_evidence, ontology)
    summary = json.loads(args.ontology_summary.read_text())
    summary["combined_evidence_sha256"] = hashlib.sha256(args.ontology_evidence.read_bytes()).hexdigest()
    summary["unique_sources"] = len(ontology)
    summary.pop("aggregate_sha256"); summary["aggregate_sha256"] = canonical_sha256(summary)
    write_json(args.ontology_summary, summary)
    with pytest.raises(ValueError, match="no fresh accepted source"):
        build(args)
