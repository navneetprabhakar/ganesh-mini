#!/usr/bin/env python3
"""Build a new 546/720 cohort by replacing exactly one overlength row."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from scripts.data.build_capability_corpus_plan import CAPABILITIES, LANES, TASK_TYPES, canonical_sha256
from scripts.data.build_capability_scale_queue import source_key


OLD_ID = "cap-scale-binary_and_bitwise-typescript-repair-first_pass-01"
NEW_ID = "cap-scale-binary_and_bitwise-typescript-repair-reserve-06"
CELL = "binary_and_bitwise/typescript/repair"


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sealed(path: Path, key: str = "report_sha256") -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    if body.pop(key, None) != canonical_sha256(body):
        raise ValueError(f"invalid seal: {path}")
    return value


def read_rows(path: Path) -> list[dict]:
    data = path.read_bytes()
    if not data or not data.endswith(b"\n"):
        raise ValueError(f"incomplete JSONL: {path}")
    return [json.loads(line) for line in data.splitlines()]


def assemble(old_capability: Path, old_manifest: Path, old_scale: Path,
             activation: Path, precheck: Path, matrix_admitted: Path,
             matrix_report: Path, matrix_terminal: Path) -> tuple[list[dict], list[dict], dict]:
    old_manifest_value = sealed(old_manifest, "manifest_sha256")
    old_rows = read_rows(old_capability)
    old_scale_rows = read_rows(old_scale)
    if old_manifest_value.get("status") != "passed" or old_manifest_value.get("capability_rows_sha256") != file_sha(old_capability):
        raise ValueError("old 720 cohort binding differs")
    if len(old_rows) != 720 or len(old_scale_rows) != 546 or sum(row["id"] == OLD_ID for row in old_rows) != 1:
        raise ValueError("old 720/546 cohort or replacement target differs")
    if {row["id"] for row in old_scale_rows} != {row["id"] for row in old_rows if row["id"].startswith("cap-scale-")}:
        raise ValueError("old 546 scale rows differ from 720 cohort")
    activation_value = sealed(activation)
    precheck_value = sealed(precheck)
    matrix_value = sealed(matrix_report)
    replacement = read_rows(matrix_admitted)
    terminal = read_rows(matrix_terminal)
    if (activation_value.get("status") != "activated" or precheck_value.get("status") != "passed" or
        precheck_value.get("completed_turn_tokens", 999999) > 2944 or
        matrix_value.get("status") != "passed" or matrix_value.get("counts") != {"admitted": 1} or
        len(replacement) != 1 or len(terminal) != 1 or replacement[0].get("id") != NEW_ID or
        replacement[0].get("qualification_assignment", {}).get("cell_id") != CELL):
        raise ValueError("replacement has not passed exact one-row gates")
    if precheck_value.get("activation_report_sha256") != activation_value["report_sha256"]:
        raise ValueError("token precheck does not bind activation")
    terminal_body = dict(terminal[0])
    if (terminal_body.pop("artifact_sha256", None) != canonical_sha256(terminal_body) or
        matrix_value.get("terminal_rows_sha256") != canonical_sha256(terminal) or
        matrix_value.get("terminal_artifact_sha256s") != [terminal[0]["artifact_sha256"]] or
        terminal[0].get("status") != "admitted" or
        terminal[0].get("candidate_sha256") != canonical_sha256(replacement[0]) or
        terminal[0].get("candidate_id") != NEW_ID):
        raise ValueError("matrix terminal evidence does not bind admitted row")
    new_row = replacement[0]
    capability = [new_row if row["id"] == OLD_ID else row for row in old_rows]
    scale = [new_row if row["id"] == OLD_ID else row for row in old_scale_rows]
    if len({row["id"] for row in capability}) != 720 or len({source_key(row) for row in capability}) != 720:
        raise ValueError("new cohort has duplicate records or sources")
    cells = Counter(row.get("cell_id") or row.get("qualification_assignment", {}).get("cell_id") for row in capability)
    expected = {f"{cap}/{lane}/{kind}" for cap in CAPABILITIES for lane in LANES for kind in TASK_TYPES}
    if set(cells) != expected or any(cells[cell] != 6 for cell in expected):
        raise ValueError("new 720 cohort is not six per cell")
    if len(scale) != 546 or sum(row["id"] == NEW_ID for row in scale) != 1 or OLD_ID in {row["id"] for row in scale}:
        raise ValueError("new 546 scale cohort has wrong replacement")
    report = {
        "schema_version": "ganesh-mini-gate3-token-length-replacement-assembly/v1",
        "status": "provisional-separation-and-quality-pending",
        "old_capability_manifest_sha256": old_manifest_value["manifest_sha256"],
        "old_capability_file_sha256": file_sha(old_capability),
        "old_scale_file_sha256": file_sha(old_scale),
        "activation_report_sha256": activation_value["report_sha256"],
        "token_precheck_report_sha256": precheck_value["report_sha256"],
        "matrix_report_sha256": matrix_value["report_sha256"],
        "matrix_admitted_file_sha256": file_sha(matrix_admitted),
        "matrix_terminal_file_sha256": file_sha(matrix_terminal),
        "replaced_id": OLD_ID,
        "replacement_id": NEW_ID,
        "cell_id": CELL,
        "records": 720,
        "scale_records": 546,
        "unique_record_ids": 720,
        "unique_source_identities": 720,
        "capability_rows_sha256": canonical_sha256(capability),
        "scale_rows_sha256": canonical_sha256(scale),
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return scale, capability, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("old_capability", "old_manifest", "old_scale", "activation", "precheck", "matrix_admitted", "matrix_report", "matrix_terminal", "output_scale", "output_capability", "output_report"):
        parser.add_argument(f"--{name.replace('_', '-')}", type=Path, required=True)
    args = parser.parse_args()
    if any(path.exists() for path in (args.output_scale, args.output_capability, args.output_report)):
        raise ValueError("assembly output already exists")
    scale, capability, report = assemble(args.old_capability, args.old_manifest, args.old_scale,
                                         args.activation, args.precheck, args.matrix_admitted, args.matrix_report, args.matrix_terminal)
    args.output_scale.parent.mkdir(parents=True, exist_ok=True)
    for path, rows in ((args.output_scale, scale), (args.output_capability, capability)):
        with path.open("x", encoding="utf-8") as handle:
            handle.write("".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows))
    with args.output_report.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": report["status"], "records": 720, "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
