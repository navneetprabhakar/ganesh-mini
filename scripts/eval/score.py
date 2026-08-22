from __future__ import annotations

import argparse
from fractions import Fraction
from pathlib import Path
from typing import Any

from scripts.eval.contracts import ContractError, load_json, validate_result, write_json


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
FAMILIES = ("go", "java", "javascript_typescript", "python", "rust")


def _fraction(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "fraction": f"{value.numerator}/{value.denominator}",
        "decimal": float(value),
    }


def load_results(path: Path) -> list[dict[str, Any]]:
    files = sorted(path.glob("*.json")) if path.is_dir() else [path]
    if not files:
        raise ContractError(f"no JSON results found in {path}")
    results = [validate_result(load_json(file)) for file in files]
    ids = [result["task_id"] for result in results]
    if len(ids) != len(set(ids)):
        raise ContractError(f"duplicate task IDs in {path}")
    identities = {
        (
            result["model"]["model_id"], result["model"]["revision"],
            result["model"]["artifact_sha256"], result["model"]["serving_contract_sha256"],
        )
        for result in results
    }
    if len(identities) != 1:
        raise ContractError(f"mixed model identities in {path}")
    return results


def _cohort_metrics(results: list[dict[str, Any]]) -> dict[str, Any]:
    by_lane: dict[str, list[dict[str, Any]]] = {lane: [] for lane in LANES}
    for result in results:
        by_lane[result["language"]].append(result)
    missing = [lane for lane, lane_results in by_lane.items() if not lane_results]
    if missing:
        raise ContractError(f"all six lanes are required; missing={missing}")
    lane_metrics: dict[str, Any] = {}
    lane_rates: dict[str, Fraction] = {}
    for lane in LANES:
        passed = sum(result["passed"] for result in by_lane[lane])
        denominator = len(by_lane[lane])
        rate = Fraction(passed, denominator)
        lane_rates[lane] = rate
        lane_metrics[lane] = {"passed": passed, "denominator": denominator, "pass_at_1": _fraction(rate)}
    family_rates = {
        "go": lane_rates["go"],
        "java": lane_rates["java"],
        "javascript_typescript": (lane_rates["javascript"] + lane_rates["typescript"]) / 2,
        "python": lane_rates["python"],
        "rust": lane_rates["rust"],
    }
    macro = sum(family_rates.values(), Fraction()) / len(FAMILIES)
    return {
        "task_count": len(results),
        "lanes": lane_metrics,
        "families": {family: _fraction(family_rates[family]) for family in FAMILIES},
        "five_family_macro": _fraction(macro),
    }


def compare(base_results: list[dict[str, Any]], candidate_results: list[dict[str, Any]]) -> dict[str, Any]:
    base_by_id = {result["task_id"]: result for result in base_results}
    candidate_by_id = {result["task_id"]: result for result in candidate_results}
    if set(base_by_id) != set(candidate_by_id):
        raise ContractError(
            f"paired cohorts differ; base_only={sorted(set(base_by_id) - set(candidate_by_id))}, "
            f"candidate_only={sorted(set(candidate_by_id) - set(base_by_id))}"
        )
    paired = {lane: {"wins": 0, "losses": 0, "ties": 0, "denominator": 0} for lane in LANES}
    aggregate = {"wins": 0, "losses": 0, "ties": 0, "denominator": 0}
    for task_id in sorted(base_by_id):
        base = base_by_id[task_id]
        candidate = candidate_by_id[task_id]
        evidence_fields = (
            "surface", "language", "family", "task_sha256", "prompt_sha256", "rendered_prompt_sha256"
        )
        if any(base[field] != candidate[field] for field in evidence_fields):
            raise ContractError(f"task {task_id}: base/candidate evidence mismatch")
        bucket = paired[base["language"]]
        if candidate["passed"] and not base["passed"]:
            transition = "wins"
        elif base["passed"] and not candidate["passed"]:
            transition = "losses"
        else:
            transition = "ties"
        bucket[transition] += 1
        bucket["denominator"] += 1
        aggregate[transition] += 1
        aggregate["denominator"] += 1
    report = {
        "schema_version": "1.0",
        "base_model": base_results[0]["model"],
        "candidate_model": candidate_results[0]["model"],
        "base": _cohort_metrics(base_results),
        "candidate": _cohort_metrics(candidate_results),
        "paired": {"aggregate": aggregate, "lanes": paired},
    }
    base_macro = Fraction(
        report["base"]["five_family_macro"]["numerator"],
        report["base"]["five_family_macro"]["denominator"],
    )
    candidate_macro = Fraction(
        report["candidate"]["five_family_macro"]["numerator"],
        report["candidate"]["five_family_macro"]["denominator"],
    )
    report["five_family_macro_delta"] = _fraction(candidate_macro - base_macro)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute paired Ganesh Mini executable pass@1 metrics.")
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    write_json(args.output, compare(load_results(args.base), load_results(args.candidate)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
