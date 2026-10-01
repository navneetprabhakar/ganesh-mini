#!/usr/bin/env python3
"""Extend the sealed cumulative capability-scale reserve-chain ledger."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.select_capability_scale_stage import read_jsonl, sealed


MAX_RESERVES = 165


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_queue(queue_path: Path, manifest_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = read_jsonl(queue_path)
    manifest = sealed(json.loads(manifest_path.read_text(encoding="utf-8")), "manifest_sha256", str(manifest_path))
    if manifest.get("queue_sha256") != _file_sha256(queue_path):
        raise ValueError("queue manifest does not bind queue bytes")
    if manifest.get("reserve_records") != MAX_RESERVES:
        raise ValueError("queue does not preserve the 165-reserve ceiling")
    ids = [row.get("id") for row in rows]
    requests = [row.get("request_sha256") for row in rows]
    sources = [row.get("source_queue_id") for row in rows]
    if any(not isinstance(value, str) or not value for value in ids + requests + sources):
        raise ValueError("queue identity fields are absent")
    if len(set(ids)) != len(ids) or len(set(requests)) != len(requests) or len(set(sources)) != len(sources):
        raise ValueError("queue candidate, request, or source identity is not unique")
    source_identities = []
    source_hashes = []
    for row in rows:
        source = row.get("source")
        if not isinstance(source, dict):
            raise ValueError("queue source lineage is absent")
        identity = tuple(source.get(key) for key in ("dataset", "revision", "record_id"))
        source_hash = source.get("source_record_sha256")
        if any(not isinstance(value, str) or not value for value in identity) or not isinstance(source_hash, str):
            raise ValueError("queue source lineage is incomplete")
        source_identities.append(identity); source_hashes.append(source_hash)
    if len(set(source_identities)) != len(rows) or len(set(source_hashes)) != len(rows):
        raise ValueError("queue source identity is not unique")
    for row in rows:
        body = copy.deepcopy(row)
        claimed = body.pop("request_sha256", None)
        if claimed != canonical_sha256(body) or row.get("evaluation_artifacts_read") != 0:
            raise ValueError(f"{row.get('id')}: invalid queue request seal")
    reserves = [row for row in rows if row.get("cohort") == "reserve"]
    first = [row for row in rows if row.get("cohort") == "first_pass"]
    per_cell = Counter(row.get("cell_id") for row in reserves)
    if len(reserves) != MAX_RESERVES or not per_cell or any(count not in (1, 2) for count in per_cell.values()):
        raise ValueError("reserve allocation must be 165 total and one or two per cell")
    if any(row.get("cell_id") not in per_cell for row in first):
        raise ValueError("a first-pass cell has no reserve allocation")
    return rows, manifest


def _load_selection(rows_path: Path, report_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = read_jsonl(rows_path)
    report = sealed(json.loads(report_path.read_text(encoding="utf-8")), "report_sha256", str(report_path))
    id_field = report.get("id_field", "candidate_id")
    seal_field = report.get("row_seal_field", "artifact_sha256")
    status_field = report.get("status_field", "status")
    if not all(isinstance(value, str) and value for value in (id_field, seal_field, status_field)):
        raise ValueError("stage selection field bindings are invalid")
    if (
        report.get("schema_version") != "ganesh-mini-capability-scale-stage-selection/v1"
        or report.get("selected_rows_sha256") != canonical_sha256(rows)
        or report.get("selected") != len(rows)
        or report.get("selected_ids") != [row.get(id_field) for row in rows]
        or report.get("selected_artifact_sha256s") != [row.get(seal_field) for row in rows]
        or report.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("stage selection report does not bind selected rows")
    for row in rows:
        sealed(row, seal_field, f"selection/{row.get(id_field)}")
    return rows, report


def extend_ledger(
    queue_path: Path,
    queue_manifest_path: Path,
    selections: list[tuple[Path, Path]],
    prior_ledger_path: Path | None = None,
) -> dict[str, Any]:
    queue, manifest = _load_queue(queue_path, queue_manifest_path)
    by_id = {row["id"]: row for row in queue}
    reserve_by_cell: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in queue:
        if row["cohort"] == "reserve":
            reserve_by_cell[row["cell_id"]].append(row)

    previous: list[dict[str, Any]] = []
    prior_sha: str | None = None
    if prior_ledger_path is not None:
        prior = sealed(json.loads(prior_ledger_path.read_text(encoding="utf-8")), "ledger_sha256", str(prior_ledger_path))
        if prior.get("queue_manifest_sha256") != manifest["manifest_sha256"]:
            raise ValueError("prior ledger belongs to another queue")
        previous = copy.deepcopy(prior.get("activations"))
        if not isinstance(previous, list):
            raise ValueError("prior ledger activations are absent")
        if (
            prior.get("activation_count") != len(previous)
            or prior.get("used_reserve_ids") != sorted(row.get("replacement_candidate_id") for row in previous)
            or prior.get("remaining_reserve_capacity") != MAX_RESERVES - len(previous)
            or prior.get("evaluation_artifacts_read") != 0
        ):
            raise ValueError("prior ledger summary differs from its activations")
        prior_sha = prior["ledger_sha256"]

    root_of: dict[str, str] = {}
    used_reserves: set[str] = set()
    failed_candidates: set[str] = set()
    for expected_ordinal, activation in enumerate(previous, start=1):
        sealed(activation, "activation_sha256", f"prior/{activation.get('replacement_candidate_id')}")
        root, failed, replacement = (
            activation.get("root_first_pass_id"), activation.get("failed_candidate_id"),
            activation.get("replacement_candidate_id"),
        )
        if root not in by_id or by_id[root]["cohort"] != "first_pass":
            raise ValueError("prior activation root is not first-pass")
        if failed not in by_id or replacement not in by_id or by_id[replacement]["cohort"] != "reserve":
            raise ValueError("prior activation references an unknown candidate")
        if by_id[failed]["cell_id"] != by_id[replacement]["cell_id"] or failed == replacement:
            raise ValueError("prior activation violates same-cell replacement")
        if (
            activation.get("ordinal") != expected_ordinal
            or activation.get("cell_id") != by_id[replacement]["cell_id"]
            or activation.get("replacement_request_sha256") != by_id[replacement]["request_sha256"]
            or activation.get("replacement_source_queue_id") != by_id[replacement]["source_queue_id"]
            or activation.get("evaluation_artifacts_read") != 0
        ):
            raise ValueError("prior activation queue binding differs")
        if failed in failed_candidates or replacement in used_reserves:
            raise ValueError("prior activation reuses a failure or reserve")
        if failed != root and root_of.get(failed) != root:
            raise ValueError("prior reserve chain is discontinuous")
        failed_candidates.add(failed); used_reserves.add(replacement); root_of[replacement] = root

    incoming: list[tuple[dict[str, Any], dict[str, Any]]] = []
    selection_bindings: list[dict[str, str]] = []
    seen_incoming: set[str] = set()
    for rows_path, report_path in selections:
        rows, report = _load_selection(rows_path, report_path)
        selection_bindings.append({"stage": report["stage"], "selection_report_sha256": report["report_sha256"]})
        for row in rows:
            id_field = report.get("id_field", "candidate_id")
            seal_field = report.get("row_seal_field", "artifact_sha256")
            status_field = report.get("status_field", "status")
            identifier = row[id_field]
            if identifier in seen_incoming or identifier in failed_candidates:
                raise ValueError(f"{identifier}: failure already activated")
            if identifier not in by_id:
                raise ValueError(f"{identifier}: failure is absent from the source queue")
            if row.get("cell_id") != by_id[identifier]["cell_id"]:
                raise ValueError(f"{identifier}: failure cell differs from queue")
            seen_incoming.add(identifier)
            normalized = copy.deepcopy(row)
            normalized["_ledger_candidate_id"] = identifier
            normalized["_ledger_artifact_sha256"] = row[seal_field]
            normalized["_ledger_status"] = row[status_field]
            incoming.append((normalized, report))

    activations = previous
    exhausted: list[dict[str, Any]] = []
    for failure, report in incoming:
        failed_id = failure["_ledger_candidate_id"]
        root = failed_id if by_id[failed_id]["cohort"] == "first_pass" else root_of.get(failed_id)
        if root is None:
            raise ValueError(f"{failed_id}: reserve failure is not part of an existing chain")
        cell = by_id[failed_id]["cell_id"]
        available = [row for row in reserve_by_cell[cell] if row["id"] not in used_reserves and row["id"] != failed_id]
        if not available:
            item = {
                "root_first_pass_id": root, "failed_candidate_id": failed_id, "cell_id": cell,
                "failed_stage": report["stage"], "failure_status": failure["_ledger_status"],
                "failure_artifact_sha256": failure["_ledger_artifact_sha256"],
                "selection_report_sha256": report["report_sha256"],
            }
            item["exhaustion_sha256"] = canonical_sha256(item)
            exhausted.append(item)
            continue
        reserve = available[0]
        activation = {
            "schema_version": "ganesh-mini-capability-scale-reserve-chain-activation/v1",
            "ordinal": len(activations) + 1,
            "root_first_pass_id": root,
            "failed_candidate_id": failed_id,
            "failed_stage": report["stage"],
            "failure_status": failure["_ledger_status"],
            "failure_artifact_sha256": failure["_ledger_artifact_sha256"],
            "selection_report_sha256": report["report_sha256"],
            "cell_id": cell,
            "replacement_candidate_id": reserve["id"],
            "replacement_request_sha256": reserve["request_sha256"],
            "replacement_source_queue_id": reserve["source_queue_id"],
            "evaluation_artifacts_read": 0,
        }
        activation["activation_sha256"] = canonical_sha256(activation)
        activations.append(activation)
        failed_candidates.add(failed_id); used_reserves.add(reserve["id"]); root_of[reserve["id"]] = root

    if len(used_reserves) > MAX_RESERVES:
        raise ValueError("global reserve ceiling exceeded")
    ledger: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-scale-reserve-chain-ledger/v1",
        "status": "capacity-exhausted" if exhausted else "active",
        "queue_manifest_sha256": manifest["manifest_sha256"],
        "queue_sha256": manifest["queue_sha256"],
        "prior_ledger_sha256": prior_sha,
        "selection_bindings": selection_bindings,
        "activations": activations,
        "activation_count": len(activations),
        "used_reserve_ids": sorted(used_reserves),
        "remaining_reserve_capacity": MAX_RESERVES - len(used_reserves),
        "capacity_exhaustions": exhausted,
        "evaluation_artifacts_read": 0,
    }
    ledger["ledger_sha256"] = canonical_sha256(ledger)
    return ledger


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--queue-manifest", type=Path, required=True)
    parser.add_argument("--selection", action="append", nargs=2, metavar=("ROWS", "REPORT"), required=True)
    parser.add_argument("--prior-ledger", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    ledger = extend_ledger(
        args.queue, args.queue_manifest,
        [(Path(rows), Path(report)) for rows, report in args.selection], args.prior_ledger,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(args.output)
    print(json.dumps({"status": ledger["status"], "activations": ledger["activation_count"], "ledger_sha256": ledger["ledger_sha256"]}, sort_keys=True))
    return 2 if ledger["status"] == "capacity-exhausted" else 0


if __name__ == "__main__":
    raise SystemExit(main())
