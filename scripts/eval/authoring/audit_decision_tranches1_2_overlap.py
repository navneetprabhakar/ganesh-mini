#!/usr/bin/env python3
"""Bind and compare the first two private decision tranches deterministically."""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path
from typing import Any

from scripts.eval.contracts import load_json, sha256_object, sha256_text, validate_task, write_json

ROOT = Path(__file__).resolve().parents[3]
MANIFESTS = (
    "manifests/evaluation/private/decision-tranche1.json",
    "manifests/evaluation/private/decision-tranche2.json",
)
OUTPUT = ROOT / "manifests/evaluation/private/decision-tranches1-2-cross-overlap.json"


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def load_prompts(relative: str) -> tuple[dict[str, Any], list[dict[str, str]]]:
    manifest = load_json(ROOT / relative)
    rows: list[dict[str, str]] = []
    for entry in manifest["tasks"]:
        task = validate_task(load_json(ROOT / entry["path"]))
        if sha256_object(task) != entry["sha256"]:
            raise RuntimeError(f"task hash mismatch: {entry['task_id']}")
        text = task["prompt"]["text"]
        rows.append({
            "task_id": task["task_id"],
            "exact": sha256_text(text),
            "normalized": sha256_text(normalized(text)),
        })
    return manifest, rows


def build() -> dict[str, Any]:
    first_manifest, first = load_prompts(MANIFESTS[0])
    second_manifest, second = load_prompts(MANIFESTS[1])
    first_exact = {row["exact"]: row["task_id"] for row in first}
    first_normalized = {row["normalized"]: row["task_id"] for row in first}
    exact = [
        {"tranche1_task_id": first_exact[row["exact"]], "tranche2_task_id": row["task_id"]}
        for row in second if row["exact"] in first_exact
    ]
    normalized_hits = [
        {"tranche1_task_id": first_normalized[row["normalized"]], "tranche2_task_id": row["task_id"]}
        for row in second if row["normalized"] in first_normalized
    ]
    duplicate_ids = sorted({row["task_id"] for row in first} & {row["task_id"] for row in second})
    if exact or normalized_hits or duplicate_ids:
        raise RuntimeError("decision tranche cross-overlap detected")
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-decision-cross-overlap/v1",
        "status": "passed",
        "manifests": [
            {"path": MANIFESTS[0], "sha256": first_manifest["manifest_sha256"], "task_count": len(first)},
            {"path": MANIFESTS[1], "sha256": second_manifest["manifest_sha256"], "task_count": len(second)},
        ],
        "normalization": "NFKC + Unicode casefold + whitespace collapse",
        "exact_prompt_overlaps": exact,
        "normalized_prompt_overlaps": normalized_hits,
        "duplicate_task_ids": duplicate_ids,
    }
    report["report_sha256"] = sha256_object(report)
    write_json(OUTPUT, report)
    return report


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True))
