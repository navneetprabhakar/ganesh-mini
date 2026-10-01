#!/usr/bin/env python3
"""Repeat blind quality reviews for the affected primary capability."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.generate_expansion_qualification import invoke_codex, verify_codex_version
from scripts.data.review_gate3_capability_sample import prompt, schema, validate_payload


CAPABILITY = "binary_and_bitwise"
NEW_ID = "cap-scale-binary_and_bitwise-typescript-repair-reserve-06"
OLD_GENERATION_ID = "cap-scale-binary_and_bitwise-rust-generation-first_pass-03"


def sealed(path: Path, field: str = "report_sha256") -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    if body.pop(field, None) != canonical_sha256(body):
        raise ValueError(f"invalid sealed input: {path}")
    return value


def run(capability_path: Path, assembly_path: Path, scale_separation_path: Path,
        old_review_path: Path, config_path: Path, codex_bin: str, output_dir: Path) -> dict:
    assembly = sealed(assembly_path)
    separation = sealed(scale_separation_path)
    old_review = sealed(old_review_path)
    rows = [json.loads(line) for line in capability_path.read_text(encoding="utf-8").splitlines()]
    if (len(rows) != 720 or assembly.get("capability_rows_sha256") != canonical_sha256(rows) or
        assembly.get("status") != "provisional-separation-and-quality-pending" or
        separation.get("status") != "passed" or len(separation.get("records", [])) != 546 or
        old_review.get("status") != "passed"):
        raise ValueError("cohort, separation or historical quality evidence differs")
    by_id = {row["id"]: row for row in rows}
    if len(by_id) != 720:
        raise ValueError("duplicate capability ID")
    selected = [by_id[OLD_GENERATION_ID], by_id[NEW_ID]]
    if any(row.get("qualification_assignment", {}).get("primary_capability") != CAPABILITY for row in selected):
        raise ValueError("affected capability assignment differs")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(codex_bin, config["codex_cli_version"])
    output_dir.mkdir(parents=True, exist_ok=True)
    schema_path = output_dir / "review-schema.json"
    schema_text = json.dumps(schema(), indent=2, sort_keys=True) + "\n"
    if schema_path.exists() and schema_path.read_text(encoding="utf-8") != schema_text:
        raise ValueError("review schema drift")
    if not schema_path.exists():
        schema_path.write_text(schema_text, encoding="utf-8")
    artifacts = []
    for row in selected:
        kind = row["task_type"]
        path = output_dir / f"{kind}-review.json"
        review_prompt = prompt([row])
        if path.exists():
            artifact = sealed(path, "artifact_sha256")
            if artifact.get("prompt_sha256") != hashlib.sha256(review_prompt.encode()).hexdigest():
                raise ValueError("existing review prompt differs")
        else:
            payload, evidence = invoke_codex(codex_bin, config, schema_path, review_prompt,
                                             "gate3-token-length-blind-quality", kind)
            items = validate_payload(payload, [row])
            artifact = {
                "schema_version": "ganesh-mini-gate3-token-length-blind-quality-batch/v1",
                "reviewer_id": f"independent-blind-codex-token-length-{kind}",
                "reviewer_kind": "independent-codex-cli",
                "task_type": kind,
                "assembly_report_sha256": assembly["report_sha256"],
                "scale_separation_report_sha256": separation["report_sha256"],
                "candidate_id": row["id"],
                "candidate_sha256": canonical_sha256(row),
                "prompt_sha256": hashlib.sha256(review_prompt.encode()).hexdigest(),
                "schema_sha256": hashlib.sha256(schema_text.encode()).hexdigest(),
                "cli_identity": cli_identity,
                "items": items,
                "run_evidence": evidence,
                "run_evidence_sha256": canonical_sha256(evidence),
                "evaluation_artifacts_read": 0,
            }
            artifact["artifact_sha256"] = canonical_sha256(artifact)
            with path.open("x", encoding="utf-8") as handle:
                json.dump(artifact, handle, indent=2, sort_keys=True)
                handle.write("\n")
        validate_payload({"items": artifact["items"]}, [row])
        artifacts.append(artifact)
    failed = [item["id"] for artifact in artifacts for item in artifact["items"] if item["verdict"] != "pass"]
    report = {
        "schema_version": "ganesh-mini-gate3-token-length-quality-result/v1",
        "status": "passed" if not failed else "failed",
        "primary_capability": CAPABILITY,
        "assembly_report_sha256": assembly["report_sha256"],
        "scale_separation_report_sha256": separation["report_sha256"],
        "historical_quality_report_sha256": old_review["report_sha256"],
        "reviewer_kinds": [artifact["reviewer_kind"] for artifact in artifacts],
        "reviewer_ids": [artifact["reviewer_id"] for artifact in artifacts],
        "reviewed_ids": [row["id"] for row in selected],
        "batch_artifact_sha256s": [artifact["artifact_sha256"] for artifact in artifacts],
        "failed_ids": failed,
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    report_path = output_dir / "quality-review-report.json"
    if report_path.exists() and json.loads(report_path.read_text(encoding="utf-8")) != report:
        raise ValueError("quality report drift")
    if not report_path.exists():
        with report_path.open("x", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2, sort_keys=True)
            handle.write("\n")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("capability", "assembly_report", "scale_separation", "historical_quality", "output_dir"):
        parser.add_argument(f"--{name.replace('_', '-')}", type=Path, required=True)
    parser.add_argument("--codex-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--codex-bin", default="codex")
    args = parser.parse_args()
    report = run(args.capability, args.assembly_report, args.scale_separation,
                 args.historical_quality, args.codex_config, args.codex_bin, args.output_dir)
    print(json.dumps({"status": report["status"], "reviewed": len(report["reviewed_ids"]), "failed": len(report["failed_ids"]), "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
