#!/usr/bin/env python3
"""Select and generate one bounded replacement for each sealed empty Gate 2 cell."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.admit_expansion import canonical_json, read_jsonl  # noqa: E402
from scripts.data.build_capability_corpus_plan import canonical_sha256, load_sealed  # noqa: E402
from scripts.data.build_capability_qualification_queue import source_key  # noqa: E402
from scripts.data.generate_capability_qualification import (  # noqa: E402
    generate_batch, load_queue, qualification_metadata, verify_codex_version,
)


SEED = 3503
MANIFEST_SCHEMA = "ganesh-mini-capability-replacement-queue-manifest/v1"
ADMISSION_SCHEMA = "ganesh-mini-capability-qualification-admission/v1"
CORRECTION_SCHEMA = "ganesh-mini-capability-qualification-correction-report/v1"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def empty_cells(queue: list[dict[str, Any]], semantic: dict[str, Any]) -> list[str]:
    if (
        semantic.get("schema_version") != "ganesh-mini-capability-semantic-review-report/v1"
        or semantic.get("status") != "complete"
        or semantic.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("semantic disposition report is incomplete or not isolated")
    queue_by_id = {row["id"]: row for row in queue}
    records = semantic.get("records")
    if not isinstance(records, list) or {row.get("id") for row in records if isinstance(row, dict)} != set(queue_by_id):
        raise ValueError("semantic disposition does not cover all 240 originals exactly")
    seen: set[str] = set()
    passes: Counter[str] = Counter()
    for record in records:
        identifier = record.get("id")
        if identifier in seen:
            raise ValueError("semantic disposition contains duplicate originals")
        seen.add(identifier)
        queue_row = queue_by_id[identifier]
        if (
            record.get("primary_capability") != queue_row["primary_capability"]
            or record.get("assigned_cross_cutting_dimension") != queue_row["assigned_cross_cutting_dimension"]
            or record.get("verdict") not in {"pass", "reject"}
        ):
            raise ValueError(f"{identifier}: semantic disposition binding is invalid")
        if record["verdict"] == "pass":
            passes[queue_row["cell_id"]] += 1
    cells = sorted({row["cell_id"] for row in queue})
    return [cell for cell in cells if passes[cell] == 0]


def _bound_file(binding: Any, where: str) -> Path:
    if not isinstance(binding, dict) or not isinstance(binding.get("path"), str):
        raise ValueError(f"{where}: artifact binding is absent")
    path = Path(binding["path"])
    data = path.read_bytes()
    if binding.get("sha256") != hashlib.sha256(data).hexdigest() or (
        "bytes" in binding and binding.get("bytes") != len(data)
    ):
        raise ValueError(f"{where}: artifact binding changed")
    return path


def actual_empty_cells(
    plan: dict[str, Any], queue: list[dict[str, Any]],
    admission_report_path: Path, correction_report_path: Path,
) -> tuple[list[str], dict[str, Any], dict[str, Any]]:
    """Authorize replacements only from post-correction executable disposition."""
    admission = load_sealed(admission_report_path, "report_sha256")
    correction = load_sealed(correction_report_path, "report_sha256")
    if (
        admission.get("schema_version") != ADMISSION_SCHEMA
        or admission.get("mode") != "final"
        or admission.get("status") != "failed"
        or admission.get("plan_sha256") != plan.get("plan_sha256")
        or admission.get("queue_disposition", {}).get("all_originals_dispositioned") is not True
        or admission.get("queue_disposition", {}).get("sealed_originals") != plan["qualification"]["drafts"]
        or admission.get("queue_disposition", {}).get("bounded_replacements") != 0
        or admission.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("corrected final admission is not a complete pre-replacement disposition")
    requested = correction.get("requested_corrections")
    completed = correction.get("completed_corrections")
    if (
        correction.get("schema_version") != CORRECTION_SCHEMA
        or correction.get("status") != "corrected-not-reviewed-not-admitted"
        or correction.get("evaluation_artifacts_read") != 0
        or correction.get("failure") is not None
        or type(requested) is not int or requested < 1 or completed != requested
    ):
        raise ValueError("single correction path is absent, incomplete, or unsealed")
    corrected_output = _bound_file(correction.get("output"), "correction output")
    if correction.get("output_sha256") != file_sha256(corrected_output):
        raise ValueError("correction output seal mismatch")

    input_binding = admission.get("input")
    if not isinstance(input_binding, dict) or not isinstance(input_binding.get("path"), str):
        raise ValueError("admission input envelope binding is absent")
    envelope_path = Path(input_binding["path"])
    if input_binding.get("sha256") != file_sha256(envelope_path):
        raise ValueError("admission envelope input changed")
    envelopes = read_jsonl(envelope_path)
    queue_ids = {row["id"] for row in queue}
    if len(envelopes) != len(queue_ids) or {
        row.get("qualification", {}).get("queue_id") for row in envelopes
    } != queue_ids:
        raise ValueError("corrected admission input does not contain all originals exactly once")
    correction_ids = {
        row.get("id") for row in correction.get("corrections", []) if isinstance(row, dict)
    }
    corrected_envelope_ids = {
        row["qualification"]["queue_id"] for row in envelopes
        if row.get("qualification", {}).get("correction_passes") == 1
    }
    if (
        len(correction_ids) != requested or correction_ids != corrected_envelope_ids
        or any(row.get("qualification", {}).get("correction_passes") not in (0, 1) for row in envelopes)
    ):
        raise ValueError("final admission does not bind every exhausted single correction")

    admitted_path = _bound_file(admission.get("outputs", {}).get("admitted"), "admitted output")
    rejected_path = _bound_file(admission.get("outputs", {}).get("rejected"), "rejected output")
    admitted = read_jsonl(admitted_path)
    rejected = json.loads(rejected_path.read_text(encoding="utf-8"))
    admitted_ids = {
        row.get("record", {}).get("id") for row in admitted if isinstance(row, dict)
    }
    rejected_ids = {
        row.get("id") for row in rejected if isinstance(row, dict)
    } if isinstance(rejected, list) else set()
    if (
        not isinstance(rejected, list)
        or admission.get("accepted") != len(admitted)
        or admission.get("rejected") != len(rejected)
        or len(admitted) + len(rejected) != len(queue)
        or admitted_ids & rejected_ids
        or admitted_ids | rejected_ids != queue_ids
        or any(
            row.get("evidence", {}).get("reference", {}).get("timed_out") is True
            for row in rejected if isinstance(row, dict)
        )
    ):
        raise ValueError("corrected admission dispositions do not reconcile or contain unresolved reference timeouts")
    admitted_cells = {row.get("qualification", {}).get("cell_id") for row in admitted}
    all_cells = {row["cell_id"] for row in plan["matrix"]["cell_contracts"]}
    missing = sorted(all_cells - admitted_cells)
    if not missing or admission.get("missing_cells") != missing:
        raise ValueError("reported missing cells differ from admitted executable evidence")
    return missing, admission, correction


def build_replacement_queue(
    queue: list[dict[str, Any]], semantic: dict[str, Any], source_rows: list[dict[str, Any]],
    prior_rows: list[dict[str, Any]], semantic_report_sha256: str,
) -> list[dict[str, Any]]:
    empties = empty_cells(queue, semantic)
    if not empties:
        raise ValueError("sealed disposition has no empty cells eligible for replacement")
    queue_by_cell: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in queue:
        queue_by_cell[row["cell_id"]].append(row)
    excluded = {source_key(row) for row in prior_rows} | {source_key(row) for row in queue}
    used: set[str] = set()
    replacements: list[dict[str, Any]] = []
    for cell_id in empties:
        originals = queue_by_cell[cell_id]
        if len(originals) != 2:
            raise ValueError(f"{cell_id}: empty cell does not have exactly two originals")
        template = originals[0]
        eligible = [
            row for row in source_rows
            if row.get("lane") == template["lane"] and row.get("task_type") == template["task_type"]
            and source_key(row) not in excluded and source_key(row) not in used
        ]
        eligible.sort(key=lambda row: hashlib.sha256(
            f"{SEED}\0{cell_id}\0{row.get('id')}\0{source_key(row)}".encode(),
        ).hexdigest())
        if not eligible:
            raise ValueError(f"{cell_id}: no collision-free replacement source remains")
        source_row = eligible[0]
        used.add(source_key(source_row))
        identifier = f"cap-v2-replacement-{template['primary_capability']}-{template['lane']}-{template['task_type']}-01"
        replacements.append({
            "schema_version": "ganesh-mini-capability-qualification-draft/v1",
            "id": identifier, "cell_id": cell_id,
            "primary_capability": template["primary_capability"],
            "primary_capability_definition": template["primary_capability_definition"],
            "assigned_cross_cutting_dimension": template["assigned_cross_cutting_dimension"],
            "lane": template["lane"], "task_type": template["task_type"],
            "source_queue_id": source_row["id"], "source": source_row["source"],
            "stimulus": source_row["stimulus"],
            "replacement_for_cell_id": cell_id, "replacement_attempt": 1,
            "original_queue_ids": sorted(row["id"] for row in originals),
            "disposition_report_sha256": semantic_report_sha256,
        })
    if len({row["cell_id"] for row in replacements}) != len(replacements):
        raise ValueError("more than one replacement was assigned to an empty cell")
    return replacements


def build_replacement_queue_for_cells(
    queue: list[dict[str, Any]], authorized_empty_cells: list[str],
    source_rows: list[dict[str, Any]], prior_rows: list[dict[str, Any]],
    disposition_report_sha256: str,
) -> list[dict[str, Any]]:
    queue_by_cell: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in queue:
        queue_by_cell[row["cell_id"]].append(row)
    unknown = set(authorized_empty_cells) - set(queue_by_cell)
    if unknown or len(authorized_empty_cells) != len(set(authorized_empty_cells)):
        raise ValueError("authorized executable empty-cell set is invalid")
    # Reuse the deterministic selector without treating semantic review as authority.
    synthetic = {
        "schema_version": "ganesh-mini-capability-semantic-review-report/v1",
        "status": "complete", "evaluation_artifacts_read": 0,
        "records": [{
            "id": row["id"], "primary_capability": row["primary_capability"],
            "assigned_cross_cutting_dimension": row["assigned_cross_cutting_dimension"],
            "verdict": "reject" if row["cell_id"] in authorized_empty_cells else "pass",
        } for row in queue],
    }
    return build_replacement_queue(
        queue, synthetic, source_rows, prior_rows, disposition_report_sha256,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--queue-manifest", type=Path, required=True)
    parser.add_argument("--semantic-report", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--corrected-admission-report", type=Path, required=True)
    parser.add_argument("--correction-report", type=Path, required=True)
    parser.add_argument("--source-queue", type=Path, required=True)
    parser.add_argument("--prior-corpus", type=Path, required=True)
    parser.add_argument("--teacher-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--queue-output", type=Path, required=True)
    parser.add_argument("--candidate-dir", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--teacher-workers", type=int, default=2)
    parser.add_argument("--codex-bin", default="codex")
    args = parser.parse_args()
    queue, queue_manifest = load_queue(args.queue, args.queue_manifest)
    semantic = load_sealed(args.semantic_report, "report_sha256")
    # Semantic empties are retained as a diagnostic cross-check only. They do
    # not authorize replacement generation.
    semantic_empty_cells = empty_cells(queue, semantic)
    plan = load_sealed(args.plan, "plan_sha256")
    authorized_empty_cells, admission, correction = actual_empty_cells(
        plan, queue, args.corrected_admission_report, args.correction_report,
    )
    replacements = build_replacement_queue_for_cells(
        queue, authorized_empty_cells, read_jsonl(args.source_queue), read_jsonl(args.prior_corpus),
        admission["report_sha256"],
    )
    args.queue_output.parent.mkdir(parents=True, exist_ok=True)
    args.queue_output.write_bytes(b"".join(canonical_json(row) + b"\n" for row in replacements))
    config = json.loads(args.teacher_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    generated: list[dict[str, Any]] = []
    batches: list[dict[str, Any]] = []
    for lane in sorted({row["lane"] for row in replacements}):
        rows = [row for row in replacements if row["lane"] == lane]
        candidates, runs, failures = generate_batch(rows, config, args.codex_bin, args.teacher_workers)
        if failures or len(candidates) != len(rows):
            raise RuntimeError(f"replacement teacher failed for {lane}: {failures}")
        output = args.candidate_dir / f"replacement-{lane}-000.candidates.jsonl"
        evidence_path = args.evidence_dir / f"replacement-{lane}-000.evidence.json"
        output.parent.mkdir(parents=True, exist_ok=True); evidence_path.parent.mkdir(parents=True, exist_ok=True)
        payload = b"".join(canonical_json(row) + b"\n" for row in candidates)
        output.write_bytes(payload)
        evidence: dict[str, Any] = {
            "schema_version": "ganesh-mini-capability-qualification-teacher-run/v1",
            "teacher": config, "cli_identity": cli_identity,
            "queue": {"sha256": file_sha256(args.queue), "manifest_sha256": queue_manifest["manifest_sha256"]},
            "selection": {
                "lane": lane, "batch_index": 0, "batch_size": len(rows),
                "requested_ids": [row["id"] for row in rows],
                "queue_row_sha256s": [canonical_sha256(row) for row in rows],
                "evaluation_surfaces_read": 0, "replacement_attempt": 1,
            },
            "execution": {"teacher_workers": min(args.teacher_workers, len(rows))},
            "generated": len(candidates), "candidate_output_sha256": hashlib.sha256(payload).hexdigest(),
            "failures": [], "runs": runs,
        }
        evidence["evidence_sha256"] = canonical_sha256(evidence)
        evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        generated.extend(candidates)
        batches.append({"lane": lane, "candidates": str(output), "evidence": str(evidence_path), "records": len(rows)})
    manifest: dict[str, Any] = {
        "schema_version": MANIFEST_SCHEMA, "status": "replacement-generation-complete-not-reviewed-not-admitted",
        "plan_sha256": queue_manifest["plan_sha256"], "queue_manifest_sha256": queue_manifest["manifest_sha256"],
        "semantic_report_sha256": semantic["report_sha256"],
        "corrected_admission_report_sha256": admission["report_sha256"],
        "correction_report_sha256": correction["report_sha256"],
        "semantic_provisional_empty_cells": semantic_empty_cells,
        "replacement_attempt": 1,
        "empty_cells": [row["cell_id"] for row in replacements], "records": len(replacements),
        "queue_output": {"path": str(args.queue_output), "sha256": file_sha256(args.queue_output)},
        "candidate_ids": [row["id"] for row in replacements], "batches": batches,
        "inputs": {
            "source_queue_sha256": file_sha256(args.source_queue),
            "prior_corpus_sha256": file_sha256(args.prior_corpus),
        },
        "evaluation_artifacts_read": 0,
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": manifest["status"], "records": len(replacements)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
