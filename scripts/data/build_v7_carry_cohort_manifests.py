#!/usr/bin/env python3
"""Reconstruct and seal V7 carry/cohort manifests from immutable V5 sources."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_v6_carry_cohort_manifests import build as reconstruct_from_v5


V7_CONTRACT_ID = "capability-stratified-v7-order-insensitive-canonical-test-replay/v1"
V7_PLAN_SHA256 = "a07c86e6ae343c51b05078afd30f5da8f463f97c2e0cbf640037c0ef79d11ded"
V6_CARRY_SEAL = "f95270299363fe003e0f8b747f60071eb813d36b09c9c132198588625a2be8af"
V6_COHORT_SEAL = "188d3b5b3e95f71556321dc1262251375d641d8e23b3961c713985b81eb7e9de"
V6_READINESS_FAILURE_SEAL = "39a8264850aafb9c8b8db6ed9de4f8d6e0d46b4ad331329a4e2c21c6cce3f778"


def _file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value); claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field}")
    return value


def build(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    if _file_sha(args.plan) != V7_PLAN_SHA256:
        raise ValueError("V7 plan hash differs from frozen plan")
    v6_carry = _sealed(args.v6_carry, "manifest_sha256")
    v6_cohort = _sealed(args.v6_cohort, "manifest_sha256")
    v6_failure = _sealed(args.v6_readiness_failure, "report_sha256")
    if (
        v6_carry.get("manifest_sha256") != V6_CARRY_SEAL
        or v6_cohort.get("manifest_sha256") != V6_COHORT_SEAL
        or v6_failure.get("report_sha256") != V6_READINESS_FAILURE_SEAL
        or v6_failure.get("status") != "readiness-failed"
    ):
        raise ValueError("V6 comparison/no-go inputs differ from sealed evidence")

    v6_args = copy.copy(args)
    v6_args.plan = args.v6_plan
    try:
        v6_args.v5_v3_codex_runs = args.v5_v3_codex_runs.resolve().relative_to(Path.cwd().resolve())
    except ValueError:
        pass
    reconstructed_carry, reconstructed_cohort = reconstruct_from_v5(v6_args)
    if (
        reconstructed_carry != v6_carry
        or reconstructed_cohort != v6_cohort
    ):
        raise ValueError("V5-source reconstruction differs from sealed V6 comparison")

    rows = []
    for source in reconstructed_carry["rows"]:
        row = copy.deepcopy(source)
        row["schema_version"] = "ganesh-mini-gate2-v7-immutable-carry/v1"
        row["contract_id"] = V7_CONTRACT_ID
        prior = row.pop("carry_row_sha256")
        row["v6_comparison_carry_row_sha256"] = prior
        row["carry_row_sha256"] = canonical_sha256(row)
        rows.append(row)
    carry = {
        key: copy.deepcopy(value)
        for key, value in reconstructed_carry.items()
        if key not in {"schema_version", "contract_id", "plan_sha256", "rows", "rows_sha256", "manifest_sha256"}
    }
    carry.update({
        "schema_version": "ganesh-mini-gate2-v7-immutable-carry-manifest/v1",
        "contract_id": V7_CONTRACT_ID,
        "plan_sha256": V7_PLAN_SHA256,
        "v6_comparison_manifest_sha256": V6_CARRY_SEAL,
        "v6_readiness_failure_report_sha256": V6_READINESS_FAILURE_SEAL,
        "reconstruction_source": "v5-immutable-inputs",
        "rows": rows,
        "rows_sha256": canonical_sha256(rows),
    })
    carry["manifest_sha256"] = canonical_sha256(carry)

    cohort_rows = []
    for source, carry_row in zip(reconstructed_cohort["rows"], rows, strict=True):
        row = copy.deepcopy(source)
        row["schema_version"] = "ganesh-mini-gate2-v7-ordered-cohort-row/v1"
        row["contract_id"] = V7_CONTRACT_ID
        prior = row.pop("cohort_row_sha256")
        row["v6_comparison_cohort_row_sha256"] = prior
        row["carry_row_sha256"] = carry_row["carry_row_sha256"]
        row["cohort_row_sha256"] = canonical_sha256(row)
        cohort_rows.append(row)
    cohort = {
        key: copy.deepcopy(value)
        for key, value in reconstructed_cohort.items()
        if key not in {"schema_version", "contract_id", "plan_sha256", "carry_manifest_sha256", "rows", "rows_sha256", "manifest_sha256"}
    }
    cohort.update({
        "schema_version": "ganesh-mini-gate2-v7-ordered-cohort-manifest/v1",
        "contract_id": V7_CONTRACT_ID,
        "plan_sha256": V7_PLAN_SHA256,
        "carry_manifest_sha256": carry["manifest_sha256"],
        "v6_comparison_manifest_sha256": V6_COHORT_SEAL,
        "v6_readiness_failure_report_sha256": V6_READINESS_FAILURE_SEAL,
        "rows": cohort_rows,
        "rows_sha256": canonical_sha256(cohort_rows),
    })
    cohort["manifest_sha256"] = canonical_sha256(cohort)
    return carry, cohort


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (
        "plan", "v6-plan", "v6-carry", "v6-cohort", "v6-readiness-failure",
        "v5-execution-manifest", "v5-candidates", "v5-assignments",
        "v5-semantic-equivalence", "v5-v1-semantic-carry", "v5-v2-semantic-carry",
        "v5-terminal-inventory", "v5-terminal-artifacts", "v5-qualification",
        "v5-v3-codex-runs", "carry-output", "cohort-output",
    ):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    carry, cohort = build(args)
    for path, value in ((args.carry_output, carry), (args.cohort_output, cohort)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"carry": carry["manifest_sha256"], "cohort": cohort["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
