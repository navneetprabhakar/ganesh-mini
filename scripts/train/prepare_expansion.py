#!/usr/bin/env python3
"""Materialize the sealed expansion corpus as a weighted response-only package."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.train.prepare_seed import LANES, _encode_rows, _write_jsonl, attach_objective_weights


ROOT = Path(__file__).resolve().parents[2]
TARGETS = {"go": 0.2, "java": 0.2, "javascript": 0.1, "typescript": 0.1, "python": 0.2, "rust": 0.2}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def build_manifest(
    *,
    source: Path,
    validation: Path,
    assessment_path: Path,
    assessment: dict[str, Any],
    prepared: Path,
    prepared_rows: list[dict[str, Any]],
    prepared_validation: Path,
    validation_rows: list[dict[str, Any]],
    template: Path,
    objective_shares: dict[str, float],
    maximum_length: int,
    seed: int,
    accumulation: int,
) -> dict[str, Any]:
    input_tokens = sum(len(row["input_ids"]) for row in prepared_rows)
    response = Counter({lane: 0 for lane in LANES})
    for row in prepared_rows:
        response[row["lane"]] += row["response_token_count"]
    manifest: dict[str, Any] = {
        "schema_version": "ganesh-mini-prepared-expansion/v1",
        "status": "ready",
        "model_id": "Qwen/Qwen3.5-2B",
        "revision": "15852e8c16360a2fea060d615a32b45270f8a8fc",
        "source": {"path": str(source.relative_to(ROOT)), "sha256": digest(source), "records": len(prepared_rows)},
        "source_assessment": {"path": str(assessment_path.relative_to(ROOT)), "sha256": digest(assessment_path), "status": assessment["status"]},
        "validation_source": {"path": str(validation.relative_to(ROOT)), "sha256": digest(validation), "records": len(validation_rows)},
        "rendering": {
            "chat_template_source": "chat_template.jinja",
            "chat_template_sha256": digest(template),
            "enable_thinking": False,
            "add_generation_prompt": False,
            "response_only_labels_verified": True,
            "response_boundary_method": "tokenizer-generation-prefix-differential-v1",
            "prompt_label_id": -100,
            "vision_token_count": 0,
            "sequence_length": maximum_length,
        },
        "objective": {
            "method": "unique-row-token-weighted-five-family-v2",
            "family_targets": TARGETS,
            "realized_normalized_weight_by_lane": objective_shares,
            "optimizer_group_scale": math.ceil(len(prepared_rows) / accumulation),
            "gradient_accumulation_steps": accumulation,
        },
        "prepared_train": {"path": str(prepared.relative_to(ROOT)), "sha256": digest(prepared), "records": len(prepared_rows), "input_tokens": input_tokens, "response_tokens_by_lane": dict(response)},
        "prepared_validation": {"path": str(prepared_validation.relative_to(ROOT)), "sha256": digest(prepared_validation), "records": len(validation_rows)},
        "seed": seed,
    }
    manifest["manifest_sha256"] = canonical_digest(manifest)
    return manifest


def prepare(
    *, source: Path, validation: Path, assessment_path: Path, output: Path,
    validation_output: Path, manifest_path: Path, maximum_length: int = 2944,
    seed: int = 3502, accumulation: int = 8,
) -> dict[str, Any]:
    from transformers import AutoTokenizer

    assessment = json.loads(assessment_path.read_text())
    sealed = assessment.get("sealed_corpus", {})
    if assessment.get("status") != "pilot-sufficient-corpus-sealed":
        raise ValueError("source assessment is not sealed")
    if sealed.get("sha256") != digest(source) or sealed.get("records") != 3225:
        raise ValueError("source does not match sealed assessment")
    tokenizer = AutoTokenizer.from_pretrained(ROOT / "models/qwen3.5-2b-15852e8", local_files_only=True)
    rows = _encode_rows(tokenizer, source, maximum_length)
    if len(rows) != sealed["records"] or len({row["source_id"] for row in rows}) != len(rows):
        raise ValueError("expansion rows are incomplete or duplicated")
    random.Random(seed).shuffle(rows)
    weighted, shares = attach_objective_weights(rows, TARGETS, accumulation)
    validation_rows = _encode_rows(tokenizer, validation, maximum_length)
    _write_jsonl(output, weighted)
    _write_jsonl(validation_output, validation_rows)
    manifest = build_manifest(
        source=source, validation=validation, assessment_path=assessment_path,
        assessment=assessment, prepared=output, prepared_rows=weighted,
        prepared_validation=validation_output, validation_rows=validation_rows,
        template=ROOT / "models/qwen3.5-2b-15852e8/chat_template.jinja",
        objective_shares=shares, maximum_length=maximum_length, seed=seed,
        accumulation=accumulation,
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "datasets/cache/expansion-v1/pilot-sealed-3225/train.jsonl")
    parser.add_argument("--validation", type=Path, default=ROOT / "data/seed/ganesh_v01/validation.jsonl")
    parser.add_argument("--assessment", type=Path, default=ROOT / "measurement/data/expansion-v1/PILOT_SUFFICIENCY_AND_THROUGHPUT_20260909.json")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/train/expansion-pilot-v1/prepared-train.jsonl")
    parser.add_argument("--validation-output", type=Path, default=ROOT / "artifacts/train/expansion-pilot-v1/prepared-validation.jsonl")
    parser.add_argument("--manifest", type=Path, default=ROOT / "artifacts/train/expansion-pilot-v1/prepared-dataset-manifest.json")
    args = parser.parse_args()
    print(json.dumps(prepare(source=args.source, validation=args.validation, assessment_path=args.assessment, output=args.output, validation_output=args.validation_output, manifest_path=args.manifest), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
