#!/usr/bin/env python3
"""Restore pinned source lineage lost by pre-fix expansion repair outputs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.generate_expansion_qualification import canonical_json
from scripts.data.repair_expansion_rejections import classify_rejection, corrected_source, read_jsonl


ANNOTATIONS = {
    "reference": "reference corrected against independent tests",
    "tests": "independent tests strengthened after rejection",
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def restore(
    original: list[dict[str, Any]], repaired: list[dict[str, Any]], report: dict[str, Any],
) -> list[dict[str, Any]]:
    if len(original) != len(repaired):
        raise ValueError("original/repaired row counts differ")
    rejection_types = {item["id"]: classify_rejection(item["reason"]) for item in report["rejected"]}
    output: list[dict[str, Any]] = []
    for before, after in zip(original, repaired, strict=True):
        if before["id"] != after["id"]:
            raise ValueError("original/repaired row order or IDs differ")
        record_id = before["id"]
        if record_id not in rejection_types:
            if canonical_json(before) != canonical_json(after):
                raise ValueError(f"{record_id}: accepted row changed during repair")
            output.append(after)
            continue
        restored = dict(after)
        restored["source"] = corrected_source(before, ANNOTATIONS[rejection_types[record_id]])
        output.append(restored)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--repaired", type=Path, required=True)
    parser.add_argument("--admission-report", type=Path, required=True)
    parser.add_argument("--teacher-evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    original_bytes = args.original.read_bytes()
    repaired_bytes = args.repaired.read_bytes()
    report = json.loads(args.admission_report.read_text(encoding="utf-8"))
    teacher = json.loads(args.teacher_evidence.read_text(encoding="utf-8"))
    if report["input_sha256"] != sha256_bytes(original_bytes):
        raise ValueError("admission report does not bind original candidates")
    if teacher["input_sha256"] != sha256_bytes(original_bytes):
        raise ValueError("teacher evidence does not bind original candidates")
    if teacher["output_sha256"] != sha256_bytes(repaired_bytes):
        raise ValueError("teacher evidence does not bind repaired candidates")
    rows = restore(read_jsonl(args.original), read_jsonl(args.repaired), report)
    payload = b"".join(canonical_json(row) + b"\n" for row in rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    evidence = {
        "schema_version": "ganesh-mini-expansion-lineage-restoration/v1",
        "original_sha256": sha256_bytes(original_bytes), "admission_report_sha256": report["report_sha256"],
        "teacher_evidence_sha256": teacher["evidence_sha256"], "teacher_output_sha256": sha256_bytes(repaired_bytes),
        "restored_ids": [item["id"] for item in report["rejected"]],
        "output": {"path": str(args.output), "bytes": len(payload), "sha256": sha256_bytes(payload)},
    }
    evidence["evidence_sha256"] = sha256_bytes(canonical_json(evidence))
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"restored": len(evidence["restored_ids"]), "sha256": evidence["output"]["sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
