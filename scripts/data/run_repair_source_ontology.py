#!/usr/bin/env python3
"""Classify repair sources once against the complete v3 capability ontology."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.build_capability_corpus_plan import CAPABILITIES, canonical_sha256  # noqa: E402
from scripts.data.build_repair_delta_queue import (  # noqa: E402
    AFFINITY_FIELDS, PLAN_SHA256, canonical_json, ontology_affinity_prompt, source_key,
)
from scripts.data.generate_expansion_qualification import (  # noqa: E402
    CodexInvocationFailure, invoke_codex, verify_codex_version,
)
from scripts.data.run_repair_source_affinity import build_attestation, excluded_identities, read_jsonl  # noqa: E402


SCHEMA_VERSION = "ganesh-mini-repair-source-ontology/v1"
CAMPAIGN_SCHEMA = "ganesh-mini-repair-source-ontology-campaign/v1"
LANES = ("go", "java", "javascript", "typescript", "python", "rust")
REQUIRED_DATASET = {
    "go": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "java": "m-a-p/MdEval-Instruct",
    "javascript": "m-a-p/MdEval-Instruct",
    "typescript": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "python": "m-a-p/MdEval-Instruct",
    "rust": "Multilingual-Multimodal-NLP/McEval-Instruct",
}


def selection_key(lane: str, identifier: str) -> str:
    return hashlib.sha256(f"3505\0{lane}\0{identifier}".encode()).hexdigest()


def output_schema(batch_size: int) -> dict[str, Any]:
    verdict_properties: dict[str, Any] = {
        "primary_capability": {"type": "string", "enum": sorted(CAPABILITIES)},
        "decision": {"type": "string", "enum": ["accept", "reject"]},
        "capability_operation": {"type": "string", "minLength": 1},
        "defect_affordance": {"type": "string", "minLength": 1},
    }
    verdict_properties.update({field: {"type": "boolean"} for field in AFFINITY_FIELDS})
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object", "additionalProperties": False, "required": ["items"],
        "properties": {"items": {
            "type": "array", "minItems": batch_size, "maxItems": batch_size,
            "items": {
                "type": "object", "additionalProperties": False,
                "required": ["source_queue_id", "verdicts"],
                "properties": {
                    "source_queue_id": {"type": "string", "minLength": 1},
                    "verdicts": {
                        "type": "array", "minItems": len(CAPABILITIES), "maxItems": len(CAPABILITIES),
                        "items": {"type": "object", "additionalProperties": False,
                                  "required": list(verdict_properties), "properties": verdict_properties},
                    },
                },
            },
        }},
    }


def validate_payload(payload: Any, expected_ids: list[str]) -> list[dict[str, Any]]:
    items = payload.get("items") if isinstance(payload, dict) else None
    if not isinstance(items, list) or len(items) != len(expected_ids):
        raise ValueError("ontology classifier item count mismatch")
    by_id: dict[str, dict[str, Any]] = {}
    expected_fields = {"primary_capability", "decision", "capability_operation", "defect_affordance", *AFFINITY_FIELDS}
    for item in items:
        if not isinstance(item, dict) or set(item) != {"source_queue_id", "verdicts"}:
            raise ValueError("ontology classifier item shape mismatch")
        identifier = item.get("source_queue_id")
        verdicts = item.get("verdicts")
        if not isinstance(identifier, str) or identifier in by_id or not isinstance(verdicts, list):
            raise ValueError("ontology classifier IDs are malformed or duplicated")
        capabilities: set[str] = set()
        for verdict in verdicts:
            if not isinstance(verdict, dict) or set(verdict) != expected_fields:
                raise ValueError("ontology verdict shape mismatch")
            capability = verdict.get("primary_capability")
            decision = verdict.get("decision")
            if (
                capability not in CAPABILITIES or capability in capabilities
                or decision not in {"accept", "reject"}
                or any(type(verdict.get(field)) is not bool for field in AFFINITY_FIELDS)
                or not all(isinstance(verdict.get(field), str) and verdict[field].strip()
                            for field in ("capability_operation", "defect_affordance"))
                or (decision == "accept" and any(verdict[field] is not True for field in AFFINITY_FIELDS))
                or (decision == "reject" and all(verdict[field] is True for field in AFFINITY_FIELDS))
            ):
                raise ValueError("ontology verdict is internally inconsistent")
            capabilities.add(capability)
        if capabilities != set(CAPABILITIES):
            raise ValueError("ontology verdicts do not cover every capability exactly once")
        by_id[identifier] = item
    if set(by_id) != set(expected_ids):
        raise ValueError("ontology classifier IDs differ from request")
    return [by_id[identifier] for identifier in expected_ids]


def build_row(
    source: dict[str, Any], item: dict[str, Any], prompt: str, run: dict[str, Any],
    config: dict[str, Any], cli_identity: str, attestation_sha256: str, rank: int,
    batch_sources: list[dict[str, Any]], plan_sha256: str = PLAN_SHA256,
) -> dict[str, Any]:
    run_body = dict(run); run_body.pop("run_evidence_sha256", None)
    value: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION, "plan_sha256": plan_sha256,
        "source_queue_id": source["id"], "lane": source["lane"], "selection_rank": rank,
        "source_identity": {key: source["source"].get(key) for key in ("dataset", "revision", "record_id")},
        "source_record_sha256": source["source"]["source_record_sha256"],
        "stimulus_sha256": hashlib.sha256(source["stimulus"].encode()).hexdigest(),
        "batch_source_queue_ids": [row["id"] for row in batch_sources],
        "batch_source_records_sha256": canonical_sha256(batch_sources),
        "verdicts": sorted(item["verdicts"], key=lambda row: row["primary_capability"]),
        "raw_prompt": prompt, "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "raw_output": run["final_output"], "output_sha256": hashlib.sha256(run["final_output"].encode()).hexdigest(),
        "runtime_parameters": {"teacher": config, "cli_identity": cli_identity,
                               "run_evidence_sha256": canonical_sha256(run_body)},
        "run_evidence": run, "separation_attestation_sha256": attestation_sha256,
        "evaluation_artifacts_read": 0,
    }
    value["evidence_sha256"] = canonical_sha256(value)
    return value


def select_sources(
    source_rows: list[dict[str, Any]], eligible_ids: set[str], excluded: set[tuple[str, str, str]],
    per_lane: int, offset: int, lanes: tuple[str, ...] = LANES, dataset: str | None = None,
    excluded_source_queue_ids: set[str] | None = None,
) -> list[dict[str, Any]]:
    if len(set(lanes)) != len(lanes):
        raise ValueError("ontology lane selection contains duplicates")
    excluded_ids = excluded_source_queue_ids or set()
    selected: list[dict[str, Any]] = []
    for lane in lanes:
        choices = [row for row in source_rows if (
            row.get("lane") == lane and row.get("task_type") == "repair" and row.get("id") in eligible_ids
            and row.get("id") not in excluded_ids
            and source_key(row) not in excluded
            and row.get("source", {}).get("dataset") == (dataset or REQUIRED_DATASET[lane])
        )]
        choices.sort(key=lambda row: selection_key(lane, row["id"]))
        wave = choices[offset:offset + per_lane]
        if not wave:
            raise ValueError(f"{lane}: no sources remain for requested deterministic ontology wave")
        selected.extend(wave)
    return selected


def load_excluded_source_queue_ids(bound_rows: list[dict[str, Any]], paths: list[Path]) -> set[str]:
    bound_ids = {row.get("id") for row in bound_rows}
    excluded_ids: set[str] = set()
    for path in paths:
        rows = read_jsonl(path)
        identifiers = [row.get("id") for row in rows]
        if any(not isinstance(identifier, str) or not identifier for identifier in identifiers):
            raise ValueError(f"{path}: exclusion source queue contains a missing or malformed ID")
        if len(set(identifiers)) != len(identifiers):
            raise ValueError(f"{path}: exclusion source queue IDs are not unique")
        unknown = set(identifiers) - bound_ids
        if unknown:
            raise ValueError(f"{path}: exclusion source queue references IDs absent from the bound source queue")
        excluded_ids.update(identifiers)
    return excluded_ids


def ensure_attestation(path: Path, attestation: dict[str, Any]) -> None:
    """Validate an existing attestation or create it atomically without overwriting."""
    if path.exists():
        expected = json.loads(path.read_text(encoding="utf-8"))
        if expected != attestation:
            raise ValueError("source-separation attestation differs from the sealed comparison")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            json.dump(attestation, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
            temporary_path = Path(handle.name)
        try:
            os.link(temporary_path, path)
        except FileExistsError:
            expected = json.loads(path.read_text(encoding="utf-8"))
            if expected != attestation:
                raise ValueError("source-separation attestation differs from the sealed comparison")
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def decision_path(root: Path, row: dict[str, Any]) -> Path:
    return root / row["lane"] / f"{row['id']}.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--teacher-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--source-queue", type=Path, required=True)
    parser.add_argument("--exclude-source-queue", type=Path, action="append", default=[])
    parser.add_argument("--prior-corpus", type=Path, required=True)
    parser.add_argument("--v2-artifact", type=Path, action="append", required=True)
    parser.add_argument("--content-free-comparison", type=Path, required=True)
    parser.add_argument("--attestation", type=Path, required=True)
    parser.add_argument("--decision-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--per-lane", type=int, default=100)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--lane", choices=LANES, action="append")
    parser.add_argument("--dataset")
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--plan-sha256", default=PLAN_SHA256)
    args = parser.parse_args()
    if not 1 <= args.batch_size <= 8 or not 1 <= args.workers <= 12 or args.per_lane <= 0 or args.offset < 0:
        raise ValueError("invalid ontology campaign bounds")
    if (
        len(args.plan_sha256) != 64
        or any(character not in "0123456789abcdef" for character in args.plan_sha256)
    ):
        raise ValueError("ontology plan SHA-256 is malformed")
    config = json.loads(args.teacher_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    attestation = build_attestation(args.source_queue, args.content_free_comparison)
    ensure_attestation(args.attestation, attestation)
    source_rows = read_jsonl(args.source_queue)
    excluded_source_queue_ids = load_excluded_source_queue_ids(source_rows, args.exclude_source_queue)
    selected = select_sources(
        source_rows, set(attestation["eligible_source_queue_ids"]),
        excluded_identities(args.prior_corpus, args.v2_artifact), args.per_lane, args.offset,
        tuple(args.lane) if args.lane else LANES, args.dataset, excluded_source_queue_ids,
    )
    batches = [selected[index:index + args.batch_size] for index in range(0, len(selected), args.batch_size)]
    completed: dict[str, dict[str, Any]] = {}
    failures: list[dict[str, Any]] = []

    def run_batch(rows: list[dict[str, Any]], schema_path: Path) -> list[dict[str, Any]]:
        reusable: list[dict[str, Any]] = []
        for row in rows:
            path = decision_path(args.decision_root, row)
            if path.exists():
                value = json.loads(path.read_text(encoding="utf-8")); body = dict(value); claimed = body.pop("evidence_sha256", None)
                if claimed != canonical_sha256(body) or value.get("source_queue_id") != row["id"]:
                    raise ValueError(f"{row['id']}: existing ontology evidence is unsealed")
                reusable.append(value)
        if len(reusable) == len(rows):
            return reusable
        if reusable:
            raise ValueError("partial ontology batch cannot be resumed because raw run evidence binds the whole batch")
        prompt = ontology_affinity_prompt(rows)
        payload, run = invoke_codex(args.codex_bin, config, schema_path, prompt, "repair-source-ontology", rows[0]["lane"])
        run["run_evidence_sha256"] = canonical_sha256(run)
        items = validate_payload(payload, [row["id"] for row in rows])
        outputs = [build_row(row, item, prompt, run, config, cli_identity, attestation["attestation_sha256"],
                             args.offset + selected.index(row), rows, args.plan_sha256)
                   for row, item in zip(rows, items, strict=True)]
        for row, value in zip(rows, outputs, strict=True):
            path = decision_path(args.decision_root, row); path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
        return outputs

    with tempfile.TemporaryDirectory(prefix="ganesh-source-ontology-") as temp_name:
        schemas: dict[int, Path] = {}
        for size in {len(batch) for batch in batches}:
            path = Path(temp_name) / f"schema-{size}.json"
            path.write_text(json.dumps(output_schema(size), sort_keys=True) + "\n", encoding="utf-8")
            schemas[size] = path
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(run_batch, batch, schemas[len(batch)]): batch for batch in batches}
            for future in as_completed(futures):
                batch = futures[future]
                try:
                    for value in future.result():
                        completed[value["source_queue_id"]] = value
                except (CodexInvocationFailure, KeyError, OSError, RuntimeError, TypeError, ValueError) as exc:
                    failures.append({"source_queue_ids": [row["id"] for row in batch], "reason": str(exc)})
    ordered = [completed[row["id"]] for row in selected if row["id"] in completed]
    payload = b"".join(canonical_json(row) + b"\n" for row in ordered)
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_bytes(payload)
    coverage = {lane: {capability: 0 for capability in CAPABILITIES} for lane in LANES}
    for row in ordered:
        for verdict in row["verdicts"]:
            if verdict["decision"] == "accept":
                coverage[row["lane"]][verdict["primary_capability"]] += 1
    summary: dict[str, Any] = {
        "schema_version": CAMPAIGN_SCHEMA, "plan_sha256": args.plan_sha256,
        "status": "complete" if not failures and all(value >= 2 for lane in coverage.values() for value in lane.values()) else "failed",
        "selected": len(selected), "completed": len(ordered), "failures": failures,
        "coverage": coverage, "output_sha256": hashlib.sha256(payload).hexdigest(),
        "offset": args.offset, "per_lane": args.per_lane, "batch_size": args.batch_size,
        "excluded_source_queue_ids_sha256": canonical_sha256(sorted(excluded_source_queue_ids)),
        "excluded_source_queue_id_count": len(excluded_source_queue_ids),
        "separation_attestation_sha256": attestation["attestation_sha256"], "evaluation_artifacts_read": 0,
    }
    summary["summary_sha256"] = canonical_sha256(summary)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "completed": len(ordered), "failures": len(failures),
                      "minimum_coverage": min(value for lane in coverage.values() for value in lane.values())}, sort_keys=True))
    return 0 if summary["status"] == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
