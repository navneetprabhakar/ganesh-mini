#!/usr/bin/env python3
"""Freeze the exact 120-cell Gate 3/4 training-entry lineage."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256


PLAN_SHA256 = "a1606049ce585ced662692ec8f31e29b35fc69a88df5c44339f8af64ac6849d0"
V2_ADMITTED_SHA256 = "602e40b1ef2590d6194dbc58bf7ed9baca976d156f19923a1fd41c5274045989"
V2_ADMISSION_FILE_SHA256 = "031fdf2c1f634b0419cd7fc219bde3ec6468e72db6cd85a5b0498ee1736fc682"
V2_ADMISSION_SEAL = "c576ef4f5b0f137edac829703eae6d7c4a63cae513544d36471f7ffcf81b7cb7"
V2_QUALIFICATION_FILE_SHA256 = "b12302218bf6f96a4212ed7a605b6ebce25dc80f0ef89656ded6448700630ffa"
V2_QUALIFICATION_SEAL = "293ebd4d38e4200a9de6bd45ba1a9ba4d0f9c0707ce632ba0be8241f41195139"
V9_CANDIDATES_SHA256 = "595b3b1c064390fbe7319cc99a0841c0beb2569c4f98607269a2ad272a82d1f7"
V9_QUALIFICATION_FILE_SHA256 = "0f0470a741137d6ec694053702853313d72ad266a99b92d6342d0c92854d7891"
V9_QUALIFICATION_SEAL = "cb0eafa84cbd76ff90c72456883c854d22356bb87da7a1ecf6a7bd4cf50ade0e"
V9_SEPARATION_FILE_SHA256 = "ab31406b3a717b91dac87c65488570df3871ef080444efb9598369e6efb2c177"
V9_SEPARATION_SEAL = "6939abd59610a771288f9232604f6d2c32c8ad74be1bc3398337ab22f8063647"
ASSIGNMENTS_SHA256 = "62ae376d4508683ee7a6e8c2e878d69ee4e7895d01413e7987ad9a0796d26e0d"
V5_COHORT_MANIFEST_FILE_SHA256 = "4753e9a3cc419ff78c2a0eb308b51f791dedc4901d3e407cc60ddebcf265fd2a"
V5_COHORT_MANIFEST_SEAL = "138c0dff1263278cae17bdab4c497f00fabec336f5ffded26daf0a30fae51e9d"
V7_TERMINAL_SHA256 = "3fff98cfbd30bc2167dfb9b9f3ee12257af90c060b7c757047508eb89ce93804"
V7_QUALIFICATION_FILE_SHA256 = "45b1130de322347d8b61ccfdbb0706ccdb4bf3c2f1e87180cdb580aece1cac05"
V7_QUALIFICATION_SEAL = "1bbdd82b8558542547f0476e8b753089a0c93e73221f4db4c6b6b9787dde3f06"
RIGHTS = ("prompt", "answer", "tests", "redistribution", "model_training")
LANES = ("go", "java", "javascript", "typescript", "python", "rust")
TASK_TYPES = ("generation", "repair")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sealed(path: Path, expected: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    claimed = body.pop("report_sha256", None)
    if claimed != expected or claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid frozen report seal")
    return value


def source_key(source: dict[str, Any]) -> str:
    required = ("dataset", "revision", "record_id", "source_record_sha256", "license")
    if any(not isinstance(source.get(key), str) or not source[key] for key in required):
        raise ValueError("selected row has incomplete source lineage")
    return "|".join(str(source[key]) for key in ("dataset", "revision", "record_id"))


def lineage_row(
    *, ordinal: int, origin: str, record: dict[str, Any], cell_id: str,
    capability: str, dimension: str, qualification: dict[str, Any], anchor: bool,
) -> dict[str, Any]:
    parts = cell_id.split("/")
    if len(parts) != 3 or parts != [capability, record.get("lane"), record.get("task_type")]:
        raise ValueError(f"{record.get('id')}: cell identity differs from record")
    rights = record.get("rights")
    if not isinstance(rights, dict) or any(rights.get(key) is not True for key in RIGHTS):
        raise ValueError(f"{record.get('id')}: incomplete training or publication rights")
    source = record.get("lineage") if origin == "v2-generation" else record.get("source")
    if not isinstance(source, dict):
        raise ValueError(f"{record.get('id')}: missing source lineage")
    row = {
        "schema_version": "ganesh-mini-training-entry-lineage-row/v1",
        "ordinal": ordinal,
        "origin": origin,
        "record_id": record["id"],
        "record_sha256": canonical_sha256(record),
        "cell_id": cell_id,
        "lane": record["lane"],
        "task_type": record["task_type"],
        "primary_capability": capability,
        "assigned_cross_cutting_dimension": dimension,
        "cell_anchor": anchor,
        "source_identity": source_key(source),
        "source": source,
        "rights": {key: rights[key] for key in RIGHTS},
        "upstream_qualification": qualification,
        "evaluation_artifacts_read": 0,
    }
    row["row_sha256"] = canonical_sha256(row)
    return row


def build(args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    expected_files = {
        args.plan: PLAN_SHA256,
        args.v2_admitted: V2_ADMITTED_SHA256,
        args.v2_admission: V2_ADMISSION_FILE_SHA256,
        args.v2_qualification: V2_QUALIFICATION_FILE_SHA256,
        args.v9_candidates: V9_CANDIDATES_SHA256,
        args.v9_qualification: V9_QUALIFICATION_FILE_SHA256,
        args.v9_separation: V9_SEPARATION_FILE_SHA256,
        args.assignments: ASSIGNMENTS_SHA256,
        args.v5_cohort_manifest: V5_COHORT_MANIFEST_FILE_SHA256,
        args.v7_terminal: V7_TERMINAL_SHA256,
        args.v7_qualification: V7_QUALIFICATION_FILE_SHA256,
    }
    for path, digest in expected_files.items():
        if file_sha256(path) != digest:
            raise ValueError(f"{path}: frozen file hash differs")

    v2_admission = sealed(args.v2_admission, V2_ADMISSION_SEAL)
    v2_qualification = sealed(args.v2_qualification, V2_QUALIFICATION_SEAL)
    v9_qualification = sealed(args.v9_qualification, V9_QUALIFICATION_SEAL)
    v9_separation = sealed(args.v9_separation, V9_SEPARATION_SEAL)
    v7_qualification = sealed(args.v7_qualification, V7_QUALIFICATION_SEAL)
    v5_cohort = json.loads(args.v5_cohort_manifest.read_text(encoding="utf-8"))
    v5_cohort_body = dict(v5_cohort)
    v5_cohort_claimed = v5_cohort_body.pop("manifest_sha256", None)
    v2_generation = v2_qualification.get("by_task_type", {}).get("generation")
    v9_comparison = v9_separation.get("comparison_manifest", {}).get("candidate_input")
    if (
        v2_qualification.get("status") != "qualification-failed"
        or v2_qualification.get("report_sha256") != V2_QUALIFICATION_SEAL
        or not isinstance(v2_generation, dict)
        or v2_generation.get("generated") != 120
        or v2_generation.get("admitted") != 114
        or v2_admission.get("report_sha256") != V2_ADMISSION_SEAL
        or v2_admission.get("outputs", {}).get("admitted", {}).get("sha256") != V2_ADMITTED_SHA256
        or v9_qualification.get("status") != "passed"
        or v9_qualification.get("final_admitted") != 60
        or v9_qualification.get("combined_coverage") != {"covered": 120, "required": 120}
        or v9_separation.get("status") != "passed"
        or v9_qualification.get("separation_report_sha256") != V9_SEPARATION_SEAL
        or v7_qualification.get("status") != "qualification-failed"
        or v7_qualification.get("admitted") != 58
        or v7_qualification.get("rejected") != 2
        or v9_comparison != {
            "bytes": args.v9_candidates.stat().st_size,
            "records": 60,
            "sha256": V9_CANDIDATES_SHA256,
        }
        or v5_cohort_claimed != V5_COHORT_MANIFEST_SEAL
        or v5_cohort_claimed != canonical_sha256(v5_cohort_body)
        or v5_cohort.get("records") != 60
        or v5_cohort.get("assignment_output", {}).get("sha256") != ASSIGNMENTS_SHA256
    ):
        raise ValueError("upstream Gate 2 decisions do not satisfy training entry")

    v2_rows = read_jsonl(args.v2_admitted)
    generation_by_cell: dict[str, list[dict[str, Any]]] = {}
    for value in v2_rows:
        record = value.get("record", {})
        qualification = value.get("qualification", {})
        if record.get("task_type") == "generation":
            generation_by_cell.setdefault(str(qualification.get("cell_id")), []).append(value)
    if len(generation_by_cell) != 60:
        raise ValueError("V2 admitted generation rows do not cover exactly 60 cells")

    rows: list[dict[str, Any]] = []
    for cell_id in sorted(generation_by_cell):
        selected = sorted(generation_by_cell[cell_id], key=lambda value: value["record"]["id"])
        for cell_ordinal, value in enumerate(selected):
            record = value["record"]
            qualification = value["qualification"]
            rows.append(lineage_row(
                ordinal=len(rows), origin="v2-generation", record=record, cell_id=cell_id,
                capability=qualification["primary_capability"],
                dimension=qualification["assigned_cross_cutting_dimension"],
                qualification={
                    "candidate_sha256": qualification["candidate_sha256"],
                    "queue_record_sha256": qualification["queue_record_sha256"],
                    "evidence_sha256s": qualification["evidence_sha256s"],
                    "v2_qualification_report_sha256": V2_QUALIFICATION_SEAL,
                },
                anchor=cell_ordinal == 0,
            ))

    assignments = {row["id"]: row for row in read_jsonl(args.assignments)}
    repairs = read_jsonl(args.v9_candidates)
    if len(repairs) != 60 or len(assignments) != 60:
        raise ValueError("V9 repair candidates or assignments do not contain exactly 60 rows")
    repair_ids = [record.get("id") for record in repairs]
    if repair_ids != v5_cohort.get("ordered_candidate_ids") or repair_ids != list(assignments):
        raise ValueError("V9 repair candidate order differs from the sealed assignment cohort")
    separation_by_id = {row.get("id"): row for row in v9_separation.get("records", [])}
    if len(separation_by_id) != 60 or any(
        separation_by_id.get(record["id"], {}).get("candidate_sha256") != canonical_sha256(record)
        for record in repairs
    ):
        raise ValueError("V9 candidates differ from the complete-cohort separation evidence")
    v7_terminal = read_jsonl(args.v7_terminal)
    v7_admitted = {
        row.get("candidate_id"): row for row in v7_terminal if row.get("status") == "admitted"
    }
    v7_rejected = {
        row.get("candidate_id") for row in v7_terminal if row.get("status") == "rejected"
    }
    corrected = {
        row.get("candidate_id"): row for row in v9_qualification.get("corrected_rows", [])
    }
    if (
        len(v7_terminal) != 60 or len(v7_admitted) != 58 or len(v7_rejected) != 2
        or set(corrected) != v7_rejected
        or any(
            canonical_sha256(v7_admitted[record["id"]]["envelope"]["candidate"])
            != canonical_sha256(record)
            for record in repairs if record["id"] in v7_admitted
        )
        or any(
            corrected[record["id"]].get("status") != "admitted"
            or corrected[record["id"]].get("candidate_sha256") != canonical_sha256(record)
            for record in repairs if record["id"] in corrected
        )
    ):
        raise ValueError("V9 repair rows do not reconcile to the exact V7 58+2 lineage")
    for record in repairs:
        assignment = assignments.get(record.get("id"))
        if not isinstance(assignment, dict):
            raise ValueError(f"{record.get('id')}: missing frozen repair assignment")
        rows.append(lineage_row(
            ordinal=len(rows), origin="v9-repair", record=record,
            cell_id=assignment["cell_id"], capability=assignment["primary_capability"],
            dimension=assignment["assigned_cross_cutting_dimension"],
            qualification={
                "candidate_sha256": canonical_sha256(record),
                "assignment_sha256": assignment["assignment_sha256"],
                "v9_qualification_report_sha256": V9_QUALIFICATION_SEAL,
                "v9_separation_report_sha256": V9_SEPARATION_SEAL,
            },
            anchor=True,
        ))

    cells = [row["cell_id"] for row in rows]
    ids = [row["record_id"] for row in rows]
    sources = [row["source_identity"] for row in rows]
    cell_counts = Counter(cells)
    anchors = [row for row in rows if row["cell_anchor"]]
    lane_task = Counter((row["lane"], row["task_type"]) for row in anchors)
    capabilities = Counter(row["primary_capability"] for row in anchors)
    dimensions = Counter(row["assigned_cross_cutting_dimension"] for row in anchors)
    if (
        len(rows) != 174 or len(set(cells)) != 120 or len(set(ids)) != 174
        or len(set(sources)) != 174 or len(anchors) != 120
        or set(lane_task) != {(lane, task) for lane in LANES for task in TASK_TYPES}
        or any(value != 10 for value in lane_task.values())
        or len(capabilities) != 10 or any(value != 12 for value in capabilities.values())
        or len(dimensions) != 5 or any(value != 24 for value in dimensions.values())
    ):
        raise ValueError("training-entry lineage does not satisfy the exact 120-cell matrix")

    payload = "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows).encode()
    manifest = {
        "schema_version": "ganesh-mini-training-entry-lineage-manifest/v1",
        "status": "passed",
        "plan_sha256": PLAN_SHA256,
        "builder": {
            "path": "scripts/data/freeze_training_entry_lineage.py",
            "sha256": file_sha256(Path(__file__)),
        },
        "records": 174,
        "cells": 120,
        "cell_anchors": 120,
        "unique_record_ids": 174,
        "unique_source_identities": 174,
        "generation_records": 114,
        "repair_records": 60,
        "lineage_jsonl_sha256": hashlib.sha256(payload).hexdigest(),
        "lineage_rows_sha256": canonical_sha256(rows),
        "upstream": {
            "v2_admitted": {"path": str(args.v2_admitted), "sha256": V2_ADMITTED_SHA256, "records": len(v2_rows)},
            "v2_admission": {"path": str(args.v2_admission), "sha256": V2_ADMISSION_FILE_SHA256, "report_sha256": V2_ADMISSION_SEAL},
            "v2_qualification": {"path": str(args.v2_qualification), "sha256": V2_QUALIFICATION_FILE_SHA256, "report_sha256": V2_QUALIFICATION_SEAL},
            "v9_candidates": {"path": str(args.v9_candidates), "sha256": V9_CANDIDATES_SHA256, "records": len(repairs)},
            "v9_qualification": {"path": str(args.v9_qualification), "sha256": V9_QUALIFICATION_FILE_SHA256, "report_sha256": V9_QUALIFICATION_SEAL},
            "v9_separation": {"path": str(args.v9_separation), "sha256": V9_SEPARATION_FILE_SHA256, "report_sha256": V9_SEPARATION_SEAL},
            "repair_assignments": {"path": str(args.assignments), "sha256": ASSIGNMENTS_SHA256, "records": len(assignments)},
            "v5_cohort_manifest": {"path": str(args.v5_cohort_manifest), "sha256": V5_COHORT_MANIFEST_FILE_SHA256, "manifest_sha256": V5_COHORT_MANIFEST_SEAL},
            "v7_terminal": {"path": str(args.v7_terminal), "sha256": V7_TERMINAL_SHA256, "records": len(v7_terminal), "admitted": len(v7_admitted)},
            "v7_qualification": {"path": str(args.v7_qualification), "sha256": V7_QUALIFICATION_FILE_SHA256, "report_sha256": V7_QUALIFICATION_SEAL},
        },
        "distribution": {
            "anchor_lane_task_type": {f"{lane}/{task}": lane_task[(lane, task)] for lane in LANES for task in TASK_TYPES},
            "anchor_primary_capability": dict(sorted(capabilities.items())),
            "anchor_cross_cutting_dimension": dict(sorted(dimensions.items())),
        },
        "cell_top_up": {cell: 6 - cell_counts[cell] for cell in sorted(cell_counts)},
        "construction_target": {
            "qualified_seed_records": 174,
            "additional_generation_records": 246,
            "additional_repair_records": 300,
            "additional_new_records": 546,
            "broad_replay_records": 180,
            "final_pilot_records": 900,
        },
        "evaluation_artifacts_read": 0,
        "training_executed": False,
        "gcloud_actions": 0,
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    return rows, manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (
        "plan", "v2-admitted", "v2-admission", "v2-qualification", "v9-candidates",
        "v9-qualification", "v9-separation", "assignments", "v5-cohort-manifest",
        "v7-terminal", "v7-qualification",
        "lineage-output", "manifest-output",
    ):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args(argv)
    rows, manifest = build(args)
    args.lineage_output.parent.mkdir(parents=True, exist_ok=True)
    args.lineage_output.write_text(
        "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )
    args.manifest_output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": manifest["status"], "records": 174, "manifest_sha256": manifest["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
