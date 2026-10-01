#!/usr/bin/env python3
"""Prepare the sealed 900-row capability package for the frozen CUDA pilot."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.seal_gate3_data_package import seal as validate_data_package
from scripts.train.prepare_seed import _encode_rows, _write_jsonl, attach_objective_weights


ROOT = Path(__file__).resolve().parents[2]
TARGETS = {"go": .2, "java": .2, "javascript": .1, "typescript": .1, "python": .2, "rust": .2}
MODEL_REVISION = "15852e8c16360a2fea060d615a32b45270f8a8fc"


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sealed(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    if body.pop("report_sha256", None) != canonical_sha256(body):
        raise ValueError(f"invalid report seal: {path}")
    return value


def prepare(package_manifest: Path, data_seal_path: Path, token_report_path: Path,
            validation_path: Path, prepared_validation_path: Path,
            output_train: Path, output_manifest: Path) -> dict:
    package = validate_data_package(package_manifest)
    data_seal = sealed(data_seal_path)
    token_report = sealed(token_report_path)
    if (data_seal.get("status") != "data-package-passed-pilot-pending" or
        data_seal.get("report_sha256") != package.get("report_sha256") or
        token_report.get("status") != "passed" or token_report.get("maximum_sequence_length") != 2944 or
        token_report.get("package_rows_sha256") != data_seal.get("package_rows_sha256") or
        token_report.get("response_only_labels_verified") is not True or
        token_report.get("tokenizer_revision") != MODEL_REVISION):
        raise ValueError("data package or tokenization evidence differs")
    manifest = json.loads(package_manifest.read_text(encoding="utf-8"))
    source = package_manifest.parent / manifest["canonical_training_jsonl"]["path"]
    if file_sha(source) != data_seal["canonical_training_jsonl_sha256"]:
        raise ValueError("canonical source file differs")
    if file_sha(validation_path) != "76ed2f3d1a2ab4eb3dddc673dfd76449f88f638b1e7d73e8c39040094c91cb35":
        raise ValueError("frozen 50-row validation source differs")
    from transformers import AutoTokenizer
    model = ROOT / "models/qwen3.5-2b-15852e8"
    tokenizer = AutoTokenizer.from_pretrained(model, local_files_only=True)
    encoded = _encode_rows(tokenizer, source, 2944)
    by_id = {row["id"]: row for row in encoded}
    token_by_id = {row["id"]: row for row in token_report["records"]}
    if len(encoded) != 900 or len(by_id) != 900 or len(token_by_id) != 900:
        raise ValueError("prepared package row count differs")
    for identifier, row in by_id.items():
        attested = token_by_id.get(identifier)
        if (attested is None or len(row["input_ids"]) != attested["input_tokens"] or
            len(row["labels"]) - row["prompt_token_count"] != attested["supervised_tokens"]):
            raise ValueError(f"{identifier}: tokenization differs from sealed report")
    random.Random(3502).shuffle(encoded)
    weighted, shares = attach_objective_weights(encoded, TARGETS, 8)
    if any(abs(shares[lane] - target) > 1e-6 for lane, target in TARGETS.items()):
        raise ValueError("frozen lane objective balance differs")
    for row in weighted:
        if abs(row["objective_weight"] - token_by_id[row["id"]]["objective_weight"]) > 1e-12:
            raise ValueError(f"{row['id']}: objective weight differs from sealed report")
    validation = _encode_rows(tokenizer, validation_path, 2944)
    if len(validation) != 50:
        raise ValueError("frozen validation count differs")
    validation_bytes = "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"
                               for row in validation).encode("utf-8")
    if (not prepared_validation_path.is_file() or
        hashlib.sha256(validation_bytes).hexdigest() != file_sha(prepared_validation_path) or
        file_sha(prepared_validation_path) != "6a9d3aa37b30bc2672517f6d63113011de5f8156aa1049e588fdc70a36b77f46"):
        raise ValueError("prepared validation differs from frozen 50-row encoding")
    if output_train.exists() or output_manifest.exists():
        raise ValueError("prepared pilot output already exists")
    _write_jsonl(output_train, weighted)
    record = {
        "schema_version": "ganesh-mini-gate3-capability-pilot-prepared/v2",
        "status": "prepared-not-trained",
        "model_id": "Qwen/Qwen3.5-2B",
        "revision": MODEL_REVISION,
        "data_package_report_sha256": data_seal["report_sha256"],
        "package_manifest_sha256": data_seal["package_manifest_sha256"],
        "tokenization_report_sha256": token_report["report_sha256"],
        "source_training_jsonl_sha256": file_sha(source),
        "validation_source_sha256": file_sha(validation_path),
        "prepared_train_sha256": file_sha(output_train),
        "prepared_validation_sha256": file_sha(prepared_validation_path),
        "prepared_validation_records": len(validation),
        "prepared_train_records": 900,
        "prepared_train_input_tokens": sum(len(row["input_ids"]) for row in weighted),
        "maximum_sequence_length": 2944,
        "realized_normalized_weight_by_lane": shares,
        "random_seed": 3502,
        "gradient_accumulation_steps": 8,
        "evaluation_artifacts_read_by_construction": 0,
        "training_executed": False,
    }
    record["manifest_sha256"] = canonical_sha256(record)
    output_manifest.parent.mkdir(parents=True, exist_ok=True)
    with output_manifest.open("x", encoding="utf-8") as handle:
        json.dump(record, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("package_manifest", "data_seal", "token_report", "validation", "prepared_validation", "output_train", "output_manifest"):
        parser.add_argument(f"--{name.replace('_', '-')}", type=Path, required=True)
    args = parser.parse_args()
    record = prepare(args.package_manifest, args.data_seal, args.token_report, args.validation,
                     args.prepared_validation,
                     args.output_train, args.output_manifest)
    print(json.dumps({"status": record["status"], "records": 900, "input_tokens": record["prepared_train_input_tokens"], "manifest_sha256": record["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
