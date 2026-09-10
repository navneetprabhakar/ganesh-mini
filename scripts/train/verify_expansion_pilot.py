#!/usr/bin/env python3
"""Verify a completed Gate 4 expansion pilot without reconstructing evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal
from pathlib import Path
from typing import Any


def canonical_digest(value: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text())
    claimed = value.pop(field, None)
    if claimed != canonical_digest(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def retention_loss_check(run: dict[str, Any], guard: dict[str, Any]) -> dict[str, Any]:
    baseline = run.get("base_validation_loss_diagnostic", {}).get("supervised_token_mean", {})
    candidate = run.get("validation_loss_diagnostic", {}).get("supervised_token_mean", {})
    lanes = ("go", "java", "javascript", "typescript", "python", "rust")
    macro_key = "five_family_macro_mean"
    required = (*lanes, macro_key)
    valid = all(isinstance(baseline.get(key), (int, float)) and baseline[key] > 0 and isinstance(candidate.get(key), (int, float)) and candidate[key] >= 0 for key in required)
    lane_ratios = {lane: candidate[lane] / baseline[lane] for lane in lanes} if valid else {}
    macro_ratio = candidate[macro_key] / baseline[macro_key] if valid else None
    return {
        "name": "non_evaluation_retention_loss_guard",
        "passed": bool(
            valid
            and max(lane_ratios.values()) <= 1 + guard.get("maximum_relative_loss_increase_per_lane", -1)
            and macro_ratio is not None
            and macro_ratio <= 1 + guard.get("maximum_relative_five_family_macro_loss_increase", -1)
        ),
        "lane_candidate_to_base_ratios": lane_ratios,
        "five_family_macro_candidate_to_base_ratio": macro_ratio,
    }


def verify(card_path: Path, config_path: Path, run_path: Path, adapter_dir: Path) -> dict[str, Any]:
    card = load_sealed(card_path, "card_sha256")
    run = load_sealed(run_path, "evidence_sha256")
    config = json.loads(config_path.read_text())
    recipe = card.get("selected_recipe", {})
    config_schema = config.get("schema_version")
    expected_card_schema = {
        "ganesh-mini-expansion-pilot-config/v1": "ganesh-mini-expansion-pilot-card/v1",
        "ganesh-mini-expansion-pilot-config/v2": "ganesh-mini-expansion-pilot-card/v2",
        "ganesh-mini-expansion-pilot-config/v3": "ganesh-mini-expansion-pilot-card/v3",
        "ganesh-mini-expansion-pilot-config/v4": "ganesh-mini-expansion-pilot-card/v4",
    }.get(config_schema)
    identities = run.get("identities", {})
    state = run.get("state", {})
    provider = card.get("provider_execution") or {}
    checks = [
        {"name": "executable_card", "passed": expected_card_schema is not None and card.get("schema_version") == expected_card_schema and card.get("status") == "ready" and not card.get("failed_checks") and provider.get("provider") == "gcloud"},
        {"name": "config_identity", "passed": file_digest(config_path) == card.get("inputs", {}).get("config_sha256") and expected_card_schema is not None},
        {"name": "completed_training", "passed": run.get("schema_version") == "ganesh-mini-sft-run/v2" and run.get("status") == "complete" and state.get("seen_tokens", 0) >= card.get("control", {}).get("maximum_seen_tokens", 1) and run.get("planned_end_row") == card.get("data", {}).get("records")},
        {"name": "execution_identity", "passed": identities.get("card_sha256") == card.get("card_sha256") and identities.get("config_sha256") == card.get("inputs", {}).get("config_sha256") and identities.get("prepared_manifest_sha256") == card.get("inputs", {}).get("prepared_manifest_sha256") and identities.get("prepared_data_sha256") == card.get("inputs", {}).get("prepared_data_sha256") and identities.get("validation_data_sha256") == card.get("inputs", {}).get("validation_data_sha256") and identities.get("model_revision") == card.get("model", {}).get("revision") and identities.get("recipe_sha256") == canonical_digest(recipe) and identities.get("learning_rate") == str(recipe.get("learning_rate")) and identities.get("phase") == "expansion-pilot"},
        {"name": "save_reload", "passed": run.get("save_reload", {}).get("passed") is True},
        {"name": "vram_bound", "passed": isinstance(run.get("cuda", {}).get("peak_vram_bytes"), int) and run["cuda"]["peak_vram_bytes"] <= int(recipe.get("maximum_peak_vram_gb", 0) * 1024**3)},
        {"name": "cost_bound", "passed": Decimal(str(run.get("cost", {}).get("projected_final_usd", "Infinity"))) <= Decimal(str(provider.get("cost_ceiling_usd", -1))) and run.get("cost", {}).get("hourly_usd") == str(provider.get("hourly_cost_usd")) and run.get("cost", {}).get("ceiling_usd") == str(provider.get("cost_ceiling_usd"))},
    ]
    if config_schema in {"ganesh-mini-expansion-pilot-config/v3", "ganesh-mini-expansion-pilot-config/v4"}:
        guard = card.get("evaluation", {}).get("retention_loss_guard", {})
        checks.append(retention_loss_check(run, guard))
    if config_schema == "ganesh-mini-expansion-pilot-config/v4":
        audit = state.get("gradient_conflict_audit", {})
        audit_payload = {key: value for key, value in audit.items() if key != "audit_sha256"}
        checks.append({
            "name": "gradient_conflict_audit",
            "passed": bool(
                audit.get("schema_version") == "ganesh-mini-gradient-conflict-audit/v1"
                and audit.get("status") == "complete"
                and audit.get("identities") == identities
                and audit.get("audit_sha256") == canonical_digest(audit_payload)
                and audit.get("decision", {}).get("stage_2_allowed") is True
            ),
        })
    expected = run.get("adapter_files", {})
    observed = {str(path.relative_to(adapter_dir)): file_digest(path) for path in sorted(adapter_dir.rglob("*")) if path.is_file()}
    checks.append({"name": "adapter_identity", "passed": bool(expected) and observed == expected})
    failed = [item["name"] for item in checks if not item["passed"]]
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-expansion-pilot-terminal/v1",
        "status": "passed" if not failed else "failed",
        "card_sha256": card.get("card_sha256"),
        "run_evidence_sha256": run.get("evidence_sha256"),
        "adapter_files": observed,
        "checks": checks,
        "failed_checks": failed,
    }
    report["report_sha256"] = canonical_digest(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--card", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--adapter-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = verify(args.card, args.config, args.run, args.adapter_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "failed_checks": report["failed_checks"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
