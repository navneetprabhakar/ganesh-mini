#!/usr/bin/env python3
"""Run resumable, isolated source-affinity classification for v3 repairs."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_repair_delta_queue import (
    AFFINITY_FIELDS, PLAN_SHA256, affinity_prompt, canonical_json, repair_cells, source_key,
)
from scripts.data.generate_expansion_qualification import (
    CodexInvocationFailure, invoke_codex, verify_codex_version,
)


COMPARISON_SCHEMA = "ganesh-mini-content-free-source-comparison/v1"
AFFINITY_SCHEMA = "ganesh-mini-repair-source-affinity/v1"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_comparison(path: Path, source_queue_sha256: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    claimed = body.pop("comparison_sha256", None)
    visibility = value.get("visibility")
    excluded = value.get("excluded_source_queue_ids")
    if (
        claimed != canonical_sha256(body)
        or value.get("schema_version") != COMPARISON_SCHEMA
        or value.get("source_queue_sha256") != source_queue_sha256
        or value.get("exact_normalized_fuzzy_comparison_complete") is not True
        or not isinstance(value.get("comparison_manifest_sha256"), str)
        or len(value["comparison_manifest_sha256"]) != 64
        or not isinstance(excluded, list) or len(set(excluded)) != len(excluded)
        or not isinstance(visibility, dict)
        or visibility.get("evaluation_content_exposed_to_construction") is not False
        or visibility.get("evaluation_identifiers_exposed_to_construction") is not False
        or visibility.get("evaluation_paths_exposed_to_construction") is not False
    ):
        raise ValueError("content-free source comparison is invalid or unsealed")
    return value


def build_attestation(source_queue_path: Path, comparison_path: Path) -> dict[str, Any]:
    source_bytes = source_queue_path.read_bytes()
    rows = read_jsonl(source_queue_path)
    if len({row.get("id") for row in rows}) != len(rows):
        raise ValueError("source queue IDs are not unique")
    comparison = load_comparison(comparison_path, sha256_bytes(source_bytes))
    source_ids = {row["id"] for row in rows}
    excluded = set(comparison["excluded_source_queue_ids"])
    if not excluded.issubset(source_ids):
        raise ValueError("content-free exclusions reference unknown source IDs")
    attestation: dict[str, Any] = {
        "schema_version": "ganesh-mini-repair-source-separation-attestation/v1",
        "source_queue_sha256": sha256_bytes(source_bytes),
        "comparison_manifest_sha256": comparison["comparison_manifest_sha256"],
        "comparison_sha256": comparison["comparison_sha256"],
        "exact_normalized_fuzzy_exclusion_complete": True,
        "eligible_source_queue_ids": sorted(source_ids - excluded),
        "excluded_source_count": len(excluded),
        "evaluation_content_exposed": False,
        "visibility": {
            "content_free_result_only": True,
            "evaluation_content_visible": False,
            "evaluation_identifiers_visible": False,
            "evaluation_paths_visible": False,
        },
    }
    attestation["attestation_sha256"] = canonical_sha256(attestation)
    return attestation


def candidate_source(row: dict[str, Any]) -> dict[str, Any]:
    candidate = row.get("candidate") if isinstance(row.get("candidate"), dict) else row
    return candidate


def excluded_identities(prior_path: Path, v2_paths: list[Path]) -> set[tuple[str, str, str]]:
    excluded = {source_key(candidate_source(row)) for row in read_jsonl(prior_path)}
    for path in v2_paths:
        excluded.update(source_key(candidate_source(row)) for row in read_jsonl(path))
    return excluded


def request_key(cell_id: str, source_id: str) -> str:
    return hashlib.sha256(f"3504\0{cell_id}\0{source_id}".encode()).hexdigest()


def plan_requests(
    source_rows: list[dict[str, Any]], eligible_ids: set[str], excluded: set[tuple[str, str, str]],
    candidates_per_cell: int,
) -> list[dict[str, Any]]:
    if not 2 <= candidates_per_cell <= 10:
        raise ValueError("candidates-per-cell must be 2..10")
    eligible = [
        row for row in source_rows
        if row.get("id") in eligible_ids and row.get("task_type") == "repair"
        and source_key(row) not in excluded
    ]
    used: set[tuple[str, str, str]] = set()
    requests: list[dict[str, Any]] = []
    for cell in repair_cells():
        choices = [row for row in eligible if row.get("lane") == cell["lane"] and source_key(row) not in used]
        choices.sort(key=lambda row: request_key(cell["cell_id"], row["id"]))
        if len(choices) < candidates_per_cell:
            raise ValueError(f"{cell['cell_id']}: insufficient unique source-affinity requests")
        for rank, row in enumerate(choices[:candidates_per_cell]):
            used.add(source_key(row))
            requests.append({"cell": cell, "source": row, "selection_rank": rank})
    if len({source_key(item["source"]) for item in requests}) != len(requests):
        raise ValueError("source-affinity request plan reuses source identities")
    return requests


def classifier_schema() -> dict[str, Any]:
    properties: dict[str, Any] = {
        "decision": {"type": "string", "enum": ["accept", "reject"]},
        "capability_operation": {"type": "string", "minLength": 1},
        "defect_affordance": {"type": "string", "minLength": 1},
    }
    properties.update({field: {"type": "boolean"} for field in AFFINITY_FIELDS})
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object",
        "additionalProperties": False, "required": list(properties), "properties": properties,
    }


def validate_payload(payload: Any) -> dict[str, Any]:
    expected = {"decision", "capability_operation", "defect_affordance", *AFFINITY_FIELDS}
    if (
        not isinstance(payload, dict) or set(payload) != expected
        or payload.get("decision") not in {"accept", "reject"}
        or not isinstance(payload.get("capability_operation"), str) or not payload["capability_operation"].strip()
        or not isinstance(payload.get("defect_affordance"), str) or not payload["defect_affordance"].strip()
        or any(type(payload.get(field)) is not bool for field in AFFINITY_FIELDS)
        or (payload["decision"] == "accept" and any(payload[field] is not True for field in AFFINITY_FIELDS))
        or (payload["decision"] == "reject" and all(payload[field] is True for field in AFFINITY_FIELDS))
    ):
        raise ValueError("source-affinity output is internally inconsistent")
    return payload


def build_affinity_row(
    request: dict[str, Any], payload: dict[str, Any], raw_prompt: str, raw_output: str,
    run: dict[str, Any], config: dict[str, Any], cli_identity: str, separation_sha256: str,
) -> dict[str, Any]:
    payload = validate_payload(payload)
    source = request["source"]
    run_body = dict(run)
    run_body.pop("run_evidence_sha256", None)
    run_sha256 = canonical_sha256(run_body)
    evidence: dict[str, Any] = {
        "schema_version": AFFINITY_SCHEMA,
        "source_queue_id": source["id"], "cell_id": request["cell"]["cell_id"],
        "selection_rank": request["selection_rank"], "decision": payload["decision"],
        **{field: payload[field] for field in AFFINITY_FIELDS},
        "capability_operation": payload["capability_operation"],
        "defect_affordance": payload["defect_affordance"],
        "source_record_sha256": source["source"]["source_record_sha256"],
        "stimulus_sha256": hashlib.sha256(source["stimulus"].encode()).hexdigest(),
        "raw_prompt": raw_prompt, "prompt_sha256": hashlib.sha256(raw_prompt.encode()).hexdigest(),
        "raw_output": raw_output, "output_sha256": hashlib.sha256(raw_output.encode()).hexdigest(),
        "runtime_parameters": {"teacher": config, "cli_identity": cli_identity,
                               "run_evidence_sha256": run_sha256},
        "run_evidence": run,
        "separation_attestation_sha256": separation_sha256,
        "evaluation_artifacts_read": 0,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    return evidence


def verify_completed(
    path: Path, request: dict[str, Any], config: dict[str, Any], cli_identity: str, separation_sha256: str,
) -> dict[str, Any] | None:
    if not path.exists():
        return None
    row = json.loads(path.read_text(encoding="utf-8"))
    body = dict(row); claimed = body.pop("evidence_sha256", None)
    prompt = affinity_prompt(request["cell"], request["source"])
    if (
        claimed != canonical_sha256(body)
        or row.get("source_queue_id") != request["source"]["id"]
        or row.get("cell_id") != request["cell"]["cell_id"]
        or row.get("selection_rank") != request["selection_rank"]
        or row.get("raw_prompt") != prompt
        or row.get("prompt_sha256") != hashlib.sha256(prompt.encode()).hexdigest()
        or row.get("separation_attestation_sha256") != separation_sha256
        or row.get("runtime_parameters", {}).get("teacher") != config
        or row.get("runtime_parameters", {}).get("cli_identity") != cli_identity
    ):
        raise ValueError(f"existing affinity decision fails its sealed contract: {path}")
    validate_payload({key: row[key] for key in ("decision", "capability_operation", "defect_affordance", *AFFINITY_FIELDS)})
    return row


def classify_one(
    request: dict[str, Any], output_path: Path, schema_path: Path, config: dict[str, Any],
    codex_bin: str, cli_identity: str, separation_sha256: str,
) -> dict[str, Any]:
    reused = verify_completed(output_path, request, config, cli_identity, separation_sha256)
    if reused is not None:
        return reused
    prompt = affinity_prompt(request["cell"], request["source"])
    payload, run = invoke_codex(
        codex_bin, config, schema_path, prompt, "repair-source-affinity", request["cell"]["lane"],
    )
    raw_output = run["final_output"]
    row = build_affinity_row(request, payload, prompt, raw_output, run, config, cli_identity, separation_sha256)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(row, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return row


def decision_path(root: Path, request: dict[str, Any]) -> Path:
    cell = request["cell"]
    return root / cell["lane"] / cell["primary_capability"] / f"{request['selection_rank']:02d}.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--teacher-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--source-queue", type=Path, required=True)
    parser.add_argument("--prior-corpus", type=Path, required=True)
    parser.add_argument("--v2-artifact", type=Path, action="append", required=True)
    parser.add_argument("--content-free-comparison", type=Path, required=True)
    parser.add_argument("--attestation", type=Path, required=True)
    parser.add_argument("--decision-root", type=Path, required=True)
    parser.add_argument("--affinity-output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--candidates-per-cell", type=int, default=6)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--codex-bin", default="codex")
    args = parser.parse_args()
    if not 1 <= args.workers <= 12:
        raise ValueError("workers must be 1..12")

    config = json.loads(args.teacher_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    attestation = build_attestation(args.source_queue, args.content_free_comparison)
    args.attestation.parent.mkdir(parents=True, exist_ok=True)
    args.attestation.write_text(json.dumps(attestation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    requests = plan_requests(
        read_jsonl(args.source_queue), set(attestation["eligible_source_queue_ids"]),
        excluded_identities(args.prior_corpus, args.v2_artifact), args.candidates_per_cell,
    )
    results: dict[int, dict[str, Any]] = {}
    failures: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="ganesh-affinity-schema-") as temp_name:
        schema_path = Path(temp_name) / "schema.json"
        schema_path.write_text(json.dumps(classifier_schema(), sort_keys=True) + "\n", encoding="utf-8")
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(
                    classify_one, request, decision_path(args.decision_root, request), schema_path,
                    config, args.codex_bin, cli_identity, attestation["attestation_sha256"],
                ): index for index, request in enumerate(requests)
            }
            for future in as_completed(futures):
                index = futures[future]
                try:
                    results[index] = future.result()
                except (CodexInvocationFailure, KeyError, OSError, RuntimeError, TypeError, ValueError) as exc:
                    failures.append({"request": requests[index]["source"]["id"], "reason": str(exc)})
    ordered = [results[index] for index in sorted(results)]
    output_bytes = b"".join(canonical_json(row) + b"\n" for row in ordered)
    args.affinity_output.parent.mkdir(parents=True, exist_ok=True); args.affinity_output.write_bytes(output_bytes)
    accepted = sum(row["decision"] == "accept" for row in ordered)
    accepted_by_cell: dict[str, int] = {}
    for row in ordered:
        if row["decision"] == "accept":
            accepted_by_cell[row["cell_id"]] = accepted_by_cell.get(row["cell_id"], 0) + 1
    summary: dict[str, Any] = {
        "schema_version": "ganesh-mini-repair-source-affinity-campaign/v1", "plan_sha256": PLAN_SHA256,
        "status": "complete" if not failures and len(accepted_by_cell) == 60 and min(accepted_by_cell.values()) >= 2 else "failed",
        "attestation_sha256": attestation["attestation_sha256"], "planned": len(requests),
        "completed": len(ordered), "accepted": accepted, "accepted_by_cell": dict(sorted(accepted_by_cell.items())),
        "affinity_output_sha256": sha256_bytes(output_bytes), "failures": failures,
        "evaluation_artifacts_read": 0,
    }
    summary["summary_sha256"] = canonical_sha256(summary)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if summary["status"] == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
