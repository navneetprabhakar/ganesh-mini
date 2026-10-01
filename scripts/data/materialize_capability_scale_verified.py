#!/usr/bin/env python3
"""Replace provisional pre-test envelopes with exact admitted matrix envelopes."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_capability_scale_queue import source_key
from scripts.data.run_capability_scale_delta_audits import _write_json_atomic, _write_jsonl_atomic
from scripts.data.run_capability_scale_final_matrix import _jsonl, _sealed, _stable_teacher_projection


ASSEMBLY_SEAL = "4f5845d95193e3cbb5df7ff32a1c47c7b432bf484229b7162251addd81384e40"
STAGES = {
    "canary": (
        "canary-v2-reserves/matrix-reauthor", "canary-v2-reserves/matrix", "canary-v1/matrix-passed",
    ),
    "first_pass": (
        "first-pass-v2/test-reauthor-v1/matrix",
        "first-pass-v2/go-single-worker-v1/result",
        "first-pass-v2/final-matrix-v1",
    ),
    "reserve": (
        "first-pass-v2/go-single-worker-v1/reserve-v1/correction-v1/matrix",
        "first-pass-v2/go-single-worker-v1/reserve-v1/matrix",
    ),
    "prospective": ("prospective-replacement-v1/matrix",),
}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_stage(root: Path, name: str) -> tuple[dict[str, dict[str, Any]], str]:
    folder = root / name
    report = _sealed(json.loads((folder / "matrix-report.json").read_text(encoding="utf-8")), "report_sha256", name)
    terminal = _jsonl(folder / "terminal-artifacts.jsonl")
    admitted = _jsonl(folder / "admitted.jsonl")
    if (
        report.get("terminal_rows_sha256") != canonical_sha256(terminal)
        or report.get("terminal_artifact_sha256s") != [row.get("artifact_sha256") for row in terminal]
        or report.get("evaluation_artifacts_read") != 0
        or report.get("counts", {}).get("admitted") != len(admitted)
    ):
        raise ValueError(f"{name}: matrix report/admitted count drift")
    by_terminal = {row.get("candidate_id"): row for row in terminal}
    by_admitted = {row.get("id"): row for row in admitted}
    if len(by_terminal) != len(terminal) or len(by_admitted) != len(admitted):
        raise ValueError(f"{name}: repeated candidate identity")
    for identifier, candidate in by_admitted.items():
        result = by_terminal.get(identifier)
        if (
            result is None or result.get("status") != "admitted"
            or result.get("candidate_sha256") != canonical_sha256(candidate)
            or result.get("evaluation_artifacts_read") != 0
        ):
            raise ValueError(f"{name}/{identifier}: admitted candidate differs from terminal matrix")
    return by_admitted, report["report_sha256"]


def materialize(root: Path, assembly_dir: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    report = _sealed(json.loads((assembly_dir / "report.json").read_text(encoding="utf-8")), "report_sha256", "provisional scale assembly")
    provisional = _jsonl(assembly_dir / "candidates.jsonl")
    if (
        report.get("report_sha256") != ASSEMBLY_SEAL
        or report.get("schema_version") != "ganesh-mini-gate3-scale-provisional-assembly/v2"
        or report.get("candidate_rows_sha256") != canonical_sha256(provisional)
        or len(provisional) != 546 or report.get("unique_source_identities") != 546
    ):
        raise ValueError("provisional assembly is not the repaired 546-row cohort")
    stage_data = {name: load_stage(root, name) for group in STAGES.values() for name in group}
    output: list[dict[str, Any]] = []
    bindings: list[dict[str, str]] = []
    counts: Counter[str] = Counter()
    for ordinal, partial in enumerate(provisional):
        group = "canary" if ordinal < 12 else "first_pass" if ordinal < 530 else "reserve" if ordinal < 545 else "prospective"
        matches = [
            (name, stage_data[name][0][partial["id"]], stage_data[name][1])
            for name in STAGES[group] if partial["id"] in stage_data[name][0]
        ]
        if not matches:
            raise ValueError(f"{partial['id']}: no admitted matrix envelope in {group}")
        name, candidate, seal = matches[0]
        if (
            canonical_sha256(_stable_teacher_projection(candidate)) != canonical_sha256(_stable_teacher_projection(partial))
            or source_key(candidate) != source_key(partial)
            or len([item for item in candidate.get("verification_task", {}).get("files", []) if item.get("role") == "test"]) != 2
        ):
            raise ValueError(f"{partial['id']}: admitted matrix envelope changed teacher content or lacks independent tests")
        output.append(candidate)
        counts[group] += 1
        bindings.append({"id": candidate["id"], "stage": name, "matrix_report_sha256": seal, "candidate_sha256": canonical_sha256(candidate)})
    if counts != {"canary": 12, "first_pass": 518, "reserve": 15, "prospective": 1}:
        raise ValueError("materialized cohort composition differs")
    if len({row["id"] for row in output}) != 546 or len({source_key(row) for row in output}) != 546:
        raise ValueError("materialized cohort reuses ID or source")
    result: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate3-scale-materialized/v1",
        "status": "verified-envelopes-separation-pending",
        "records": 546,
        "provisional_assembly_report_sha256": ASSEMBLY_SEAL,
        "provisional_assembly_file_sha256": file_sha256(assembly_dir / "candidates.jsonl"),
        "materialized_rows_sha256": canonical_sha256(output),
        "stage_counts": dict(counts), "bindings": bindings,
        "evaluation_artifacts_read": 0,
    }
    result["report_sha256"] = canonical_sha256(result)
    return output, result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scale-root", type=Path, required=True)
    parser.add_argument("--assembly-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists():
        raise ValueError("materialized scale output already exists")
    rows, report = materialize(args.scale_root, args.assembly_dir)
    _write_jsonl_atomic(args.output_dir / "candidates.jsonl", rows)
    _write_json_atomic(args.output_dir / "report.json", report)
    print(json.dumps({"status": report["status"], "records": 546, "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
