from __future__ import annotations

import argparse
import math
import random
import re
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

from scripts.eval.contracts import ContractError, load_json, sha256_object, validate_result, write_json


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
FAMILIES = ("go", "java", "javascript_typescript", "python", "rust")
SEMANTIC_ID = re.compile(r"^(dev|decision)-t\d+-(go|java|javascript|typescript|python|rust)-(.+)$")


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
    results=[]
    for file in files:
        value=load_json(file)
        if value.get("schema_version")=="ganesh-mini-task-evidence/v2":
            unsigned=dict(value); claimed=unsigned.pop("evidence_sha256",None)
            if claimed!=sha256_object(unsigned): raise ContractError(f"invalid task evidence seal: {file}")
            value=value.get("verification",{}).get("result")
        results.append(validate_result(value))
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
    quality = {"malformed": 0, "repetitive": 0, "truncated": 0, "non_code": 0}
    starts=[]; ends=[]
    artifact_sizes = set()
    for result in results:
        candidate = result["candidate"]
        raw, code = candidate["raw_output"], candidate["extracted_code"]
        lines = [line.strip() for line in code.splitlines() if line.strip()]
        quality["non_code"] += not bool(code.strip())
        quality["malformed"] += not bool(code.strip())
        quality["repetitive"] += len(lines) >= 8 and len(set(lines)) / len(lines) < 0.5
        params = result["inference"]["parameters"]
        quality["truncated"] += params.get("stopped_at_eos") is False and params.get("output_tokens") == params.get("max_new_tokens")
        try:
            start = datetime.fromisoformat(result["inference"]["started_at"])
            end = datetime.fromisoformat(result["inference"]["completed_at"])
            starts.append(start); ends.append(end)
        except ValueError:
            pass
        if isinstance(params.get("artifact_size_bytes"), int):
            artifact_sizes.add(params["artifact_size_bytes"])
    artifact_bytes = next(iter(artifact_sizes)) if len(artifact_sizes) == 1 else None
    total_seconds=max(0.0,(max(ends)-min(starts)).total_seconds()) if starts and ends else 0.0
    return {
        "task_count": len(results),
        "lanes": lane_metrics,
        "families": {family: _fraction(family_rates[family]) for family in FAMILIES},
        "five_family_macro": _fraction(macro),
        "quality_failures": quality,
        "efficiency": {
            "artifact_size_bytes": artifact_bytes,
            "quality_per_model_gb": float(macro) / (artifact_bytes / 10**9) if artifact_bytes else None,
            "verified_tasks_per_wall_clock_hour": len(results) * 3600 / total_seconds if total_seconds else None,
        },
    }


def _semantic_family(result: dict[str, Any]) -> str:
    match = SEMANTIC_ID.match(result["task_id"])
    return f"{match.group(1)}-t{result['task_id'].split('-t',1)[1].split('-',1)[0]}-{match.group(3)}" if match else result["task_id"]


def _mcnemar_exact(wins: int, losses: int) -> dict[str, Any]:
    discordant = wins + losses
    if discordant == 0:
        return {"discordant": 0, "two_sided_exact_p": 1.0}
    tail = sum(math.comb(discordant, value) for value in range(min(wins, losses) + 1)) / 2**discordant
    return {"discordant": discordant, "two_sided_exact_p": min(1.0, 2 * tail)}


def _cluster_statistics(deltas: dict[str, list[int]], seed: int = 3502, draws: int = 20000) -> dict[str, Any]:
    clusters = sorted(deltas)
    cluster_means = [sum(deltas[key]) / len(deltas[key]) for key in clusters]
    observed = sum(cluster_means) / len(cluster_means)
    rng = random.Random(seed)
    bootstrap = []
    for _ in range(draws):
        sample = [cluster_means[rng.randrange(len(cluster_means))] for _ in cluster_means]
        bootstrap.append(sum(sample) / len(sample))
    bootstrap.sort()
    lower = bootstrap[int(0.025 * (draws - 1))]
    upper = bootstrap[int(0.975 * (draws - 1))]
    extreme = 0
    for _ in range(draws):
        statistic = sum(value if rng.getrandbits(1) else -value for value in cluster_means) / len(cluster_means)
        extreme += abs(statistic) >= abs(observed)
    return {
        "method": "semantic-family-cluster-bootstrap-and-sign-permutation",
        "effective_cluster_n": len(clusters), "row_n": sum(map(len, deltas.values())),
        "mean_paired_delta": observed, "confidence_level": 0.95,
        "bootstrap_ci": {"lower": lower, "upper": upper, "draws": draws, "seed": seed},
        "two_sided_permutation_p": (extreme + 1) / (draws + 1),
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
    cluster_deltas: dict[str, list[int]] = {}
    for task_id in sorted(base_by_id):
        base = base_by_id[task_id]
        candidate = candidate_by_id[task_id]
        evidence_fields = (
            "surface", "language", "family", "task_sha256", "prompt_sha256"
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
        cluster_deltas.setdefault(_semantic_family(base), []).append(int(candidate["passed"]) - int(base["passed"]))
    report = {
        "schema_version": "1.0",
        "base_model": base_results[0]["model"],
        "candidate_model": candidate_results[0]["model"],
        "base": _cohort_metrics(base_results),
        "candidate": _cohort_metrics(candidate_results),
        "paired": {
            "aggregate": aggregate, "lanes": paired,
            "mcnemar": _mcnemar_exact(aggregate["wins"], aggregate["losses"]),
            "cluster_aware": _cluster_statistics(cluster_deltas),
        },
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
