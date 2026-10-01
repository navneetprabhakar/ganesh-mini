#!/usr/bin/env python3
"""Validate a proposed Gate 3 corpus package without opening evaluation data.

Input is a JSON manifest with ``capability`` and ``replay`` JSONL file bindings
(``path``, ``sha256``), and five sealed JSON report bindings: ``admission``,
``replay_selection``, ``manual_review``, ``separation``, and ``tokenization``.
Each report has a canonical ``report_sha256`` and is bound by file SHA-256 in
the manifest. Reports use the small package-level contract checked below; a
future assembler must produce them from the upstream admission evidence.
The validator writes nothing and never opens an evaluation file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.audit_corpus_diversity import scaffold_fingerprint
from scripts.data.build_capability_corpus_plan import CAPABILITIES, LANES, TASK_TYPES


RIGHTS = ("prompt", "answer", "tests", "redistribution", "model_training")
TARGETS = {"go": .2, "java": .2, "javascript": .1, "typescript": .1, "python": .2, "rust": .2}
PASS_FIELDS = (
    "exact_training_passed", "normalized_training_passed", "fuzzy_training_passed",
    "exact_evaluation_passed", "normalized_evaluation_passed", "fuzzy_evaluation_passed",
)


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _bound_path(base: Path, binding: Any, label: str) -> Path:
    if not isinstance(binding, dict) or not isinstance(binding.get("path"), str) or not binding["path"]:
        raise ValueError(f"{label}: missing file binding")
    path = Path(binding["path"])
    if path.suffix not in {".json", ".jsonl"}:
        raise ValueError(f"{label}: unexpected file type")
    path = path if path.is_absolute() else base / path
    if hashlib.sha256(path.read_bytes()).hexdigest() != binding.get("sha256"):
        raise ValueError(f"{label}: file hash mismatch")
    return path


def _rows(base: Path, binding: Any, label: str) -> list[dict[str, Any]]:
    path = _bound_path(base, binding, label)
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"{label}: expected object rows")
    return rows


def _report(base: Path, binding: Any, label: str) -> dict[str, Any]:
    report = json.loads(_bound_path(base, binding, label).read_text(encoding="utf-8"))
    if not isinstance(report, dict):
        raise ValueError(f"{label}: expected object")
    body = dict(report)
    seal = body.pop("report_sha256", None)
    if seal != canonical_sha256(body):
        raise ValueError(f"{label}: invalid report seal")
    if report.get("status") != "passed" or report.get("evaluation_artifacts_read_by_construction") != 0:
        raise ValueError(f"{label}: report is not passed with zero construction evaluation reads")
    return report


def _identity(row: dict[str, Any]) -> str:
    sources = [value for value in (row.get("source"), row.get("lineage")) if value is not None]
    if not sources:
        raise ValueError("incomplete source lineage")
    keys = ("dataset", "revision", "record_id")
    identities = []
    for source in sources:
        if not isinstance(source, dict) or any(not isinstance(source.get(key), str) or not source[key]
                                                for key in (*keys, "source_record_sha256", "license")):
            raise ValueError("incomplete source lineage")
        if not re.fullmatch(r"[0-9a-f]{64}", source["source_record_sha256"]):
            raise ValueError("invalid source record hash")
        identities.append(tuple(source[key] for key in (*keys, "source_record_sha256")))
    if len(set(identities)) != 1:
        raise ValueError("conflicting source and lineage identities or hashes")
    assignment = row.get("qualification_assignment")
    if assignment is not None:
        if not isinstance(assignment, dict) or assignment.get("source_identity") != dict(zip(keys, identities[0][:3])) or assignment.get("source_record_sha256") != identities[0][3]:
            raise ValueError("qualification assignment source identity or hash differs")
    return canonical_sha256(identities[0][:3])


def _capability(row: dict[str, Any]) -> str:
    assignment = row.get("qualification_assignment")
    assigned = assignment.get("primary_capability") if isinstance(assignment, dict) else None
    top_level = row.get("primary_capability")
    if top_level is not None and assigned is not None and top_level != assigned:
        raise ValueError("conflicting primary capability labels")
    capability = top_level if top_level is not None else assigned
    if capability not in CAPABILITIES:
        raise ValueError("missing or unsupported primary capability")
    if assignment is not None and (not isinstance(assignment, dict) or assignment.get("cell_id") != f"{capability}/{row.get('lane')}/{row.get('task_type')}"):
        raise ValueError("qualification assignment cell differs")
    return capability


def _prompt(row: dict[str, Any]) -> str:
    messages = row.get("messages")
    if not isinstance(messages, list) or len(messages) != 2 or not all(isinstance(item, dict) for item in messages) or [item.get("role") for item in messages] != ["user", "assistant"]:
        raise ValueError("record needs one user and one assistant message")
    if any(not isinstance(item.get("content"), str) or not item["content"] for item in messages):
        raise ValueError("record has empty message content")
    return messages[0]["content"]


def validate(manifest_path: Path) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("schema_version") != "ganesh-mini-gate3-final-package/v1":
        raise ValueError("invalid package manifest schema")
    body = dict(manifest)
    if body.pop("manifest_sha256", None) != canonical_sha256(body):
        raise ValueError("invalid package manifest seal")
    if manifest.get("evaluation_artifacts_read_by_construction") != 0:
        raise ValueError("package construction exposed evaluation artifacts")
    base = manifest_path.parent
    capability = _rows(base, manifest.get("capability"), "capability")
    replay = _rows(base, manifest.get("replay"), "replay")
    if len(capability) != 720 or len(replay) != 180:
        raise ValueError("package must contain 720 capability and 180 replay rows")
    all_rows = capability + replay
    ids = [row.get("id") for row in all_rows]
    if any(not isinstance(identifier, str) or not identifier for identifier in ids) or len(set(ids)) != 900:
        raise ValueError("package needs 900 unique record IDs")
    sources = [_identity(row) for row in all_rows]
    if len(set(sources)) != 900:
        raise ValueError("package needs 900 unique source identities")
    for row in all_rows:
        if row.get("lane") not in LANES or row.get("task_type") not in TASK_TYPES:
            raise ValueError("unsupported lane or task type")
        if not isinstance(row.get("rights"), dict) or any(row["rights"].get(key) is not True for key in RIGHTS):
            raise ValueError("incomplete training rights")
        _prompt(row)
    cells = Counter((_capability(row), row["lane"], row["task_type"]) for row in capability)
    expected = {(cap, lane, kind) for cap in CAPABILITIES for lane in LANES for kind in TASK_TYPES}
    if set(cells) != expected or any(cells[cell] != 6 for cell in expected):
        raise ValueError("capability matrix must have six rows in each of 120 cells")
    pairs = Counter((row["lane"], row["task_type"]) for row in replay)
    if set(pairs) != {(lane, kind) for lane in LANES for kind in TASK_TYPES} or any(count != 15 for count in pairs.values()):
        raise ValueError("replay must have fifteen rows per lane and task type")
    scaffolds = Counter(scaffold_fingerprint(_prompt(row)) for row in all_rows)
    if max(scaffolds.values()) > 18:
        raise ValueError("normalized scaffold cluster exceeds 2 percent")

    digests = {"capability": canonical_sha256(capability), "replay": canonical_sha256(replay),
               "package": canonical_sha256(all_rows)}
    reports = {name: _report(base, manifest.get(name), name) for name in
               ("admission", "replay_selection", "manual_review", "separation", "tokenization")}
    for name, corpus in (("admission", "capability"), ("replay_selection", "replay")):
        report = reports[name]
        if report.get("records") != len(capability if corpus == "capability" else replay) or report.get("rows_sha256") != digests[corpus]:
            raise ValueError(f"{name}: row binding mismatch")

    review = reports["manual_review"]
    if review.get("package_rows_sha256") != digests["package"] or not isinstance(review.get("reviews"), list):
        raise ValueError("manual review binding missing")
    reviews_by_cap: dict[str, set[tuple[str, str]]] = {cap: set() for cap in CAPABILITIES}
    cap_by_id = {row["id"]: _capability(row) for row in capability}
    for item in review["reviews"]:
        if not isinstance(item, dict) or item.get("record_id") not in cap_by_id or item.get("primary_capability") != cap_by_id[item["record_id"]] or item.get("blind") is not True or item.get("verdict") != "pass" or not isinstance(item.get("reviewer_id"), str) or not item["reviewer_id"]:
            raise ValueError("invalid blind manual review")
        reviews_by_cap[item["primary_capability"]].add((item["record_id"], item["reviewer_id"]))
    if any(len({rid for rid, _ in reviews}) < 2 or len({reviewer for _, reviewer in reviews}) < 2
           for reviews in reviews_by_cap.values()):
        raise ValueError("two independent blind reviews per capability are required")

    separation = reports["separation"]
    if separation.get("package_rows_sha256") != digests["package"] or separation.get("content_exposure") != {
        "evaluation_content_serialized": 0, "evaluation_paths_or_task_ids_serialized": 0,
        "collision_identities_serialized": 0,
    }:
        raise ValueError("separation report exposes evaluation content or has wrong binding")
    sep_rows = separation.get("records")
    if not isinstance(sep_rows, list) or len(sep_rows) != 900 or {item.get("id") for item in sep_rows if isinstance(item, dict)} != set(ids):
        raise ValueError("separation does not cover exactly 900 rows")
    row_hashes = {row["id"]: canonical_sha256(row) for row in all_rows}
    if any(not isinstance(item, dict) or item.get("row_sha256") != row_hashes.get(item.get("id")) or
           any(item.get(field) is not True for field in PASS_FIELDS) for item in sep_rows):
        raise ValueError("separation has an unbound or failed row")

    token = reports["tokenization"]
    if token.get("package_rows_sha256") != digests["package"] or token.get("maximum_sequence_length") != 2944 or not isinstance(token.get("tokenizer_revision"), str) or not token["tokenizer_revision"] or not isinstance(token.get("chat_template_sha256"), str) or len(token["chat_template_sha256"]) != 64 or token.get("response_only_labels_verified") is not True:
        raise ValueError("tokenization contract or binding missing")
    token_rows = token.get("records")
    if not isinstance(token_rows, list) or len(token_rows) != 900 or {item.get("id") for item in token_rows if isinstance(item, dict)} != set(ids):
        raise ValueError("tokenization does not cover exactly 900 rows")
    mass = Counter()
    lane_by_id = {row["id"]: row["lane"] for row in all_rows}
    for item in token_rows:
        if (not isinstance(item, dict) or item.get("row_sha256") != row_hashes.get(item.get("id")) or
            type(item.get("input_tokens")) is not int or not 0 < item["input_tokens"] <= 2944 or
            type(item.get("supervised_tokens")) is not int or not 0 < item["supervised_tokens"] <= item["input_tokens"] or
            type(item.get("objective_weight")) not in (int, float) or not 0 < item["objective_weight"] < float("inf")):
            raise ValueError("invalid tokenization row")
        mass[lane_by_id[item["id"]]] += item["objective_weight"]
    total = sum(mass.values())
    if any(abs(mass[lane] / total - target) > 1e-6 for lane, target in TARGETS.items()):
        raise ValueError("supervised objective family balance failed")
    return {"status": "validated-not-sealed", "records": 900, "capability": 720, "replay": 180,
            "package_rows_sha256": digests["package"], "maximum_scaffold_cluster": max(scaffolds.values())}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(validate(args.manifest), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
