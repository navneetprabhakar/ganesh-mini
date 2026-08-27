#!/usr/bin/env python3
"""Apply the frozen Ganesh Mini 1.0 release gates without inventing evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
QWEN_MODEL_ID = "Qwen/Qwen3.5-2B"
QWEN_REVISION = "15852e8c16360a2fea060d615a32b45270f8a8fc"
SEAL_FIELDS = ("manifest_sha256", "report_sha256", "evidence_sha256", "run_sha256", "card_sha256")
REQUIRED_MANIFEST_SCHEMAS = {
    "seed": "ganesh-mini-seed-manifest/v1",
    "readiness": "ganesh-mini-readiness/v1",
    "execution_card": "ganesh-mini-training-execution-card/v1",
    "training_run": "ganesh-mini-sft-run/v2",
    "artifacts": "ganesh-mini-release-artifacts/v1",
    "export_equivalence": "ganesh-mini-export-equivalence/v1",
}


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def verified_seal(value: dict[str, Any], field: str) -> str | None:
    claimed = value.get(field)
    if not isinstance(claimed, str) or len(claimed) != 64:
        return None
    unsigned = dict(value)
    unsigned.pop(field)
    return claimed if canonical_sha256(unsigned) == claimed else None


def total_passes(cohort: dict[str, Any]) -> int:
    return sum(int(cohort["lanes"][lane]["passed"]) for lane in LANES)


def check(name: str, passed: bool, **evidence: Any) -> dict[str, Any]:
    return {"name": name, "passed": bool(passed), "evidence": evidence}


def comparison_contract(value: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    try:
        seal = verified_seal(value, "report_sha256")
        base = value["base"]
        candidate = value["candidate"]
        paired = value["paired"]
        paired_lanes = paired["lanes"]
        lane_denominators = {lane: paired_lanes[lane]["denominator"] for lane in LANES}
        base_lane_denominators = {lane: base["lanes"][lane]["denominator"] for lane in LANES}
        candidate_lane_denominators = {lane: candidate["lanes"][lane]["denominator"] for lane in LANES}
        aggregate = paired["aggregate"]
        evidence = value["evidence"]
        base_macro = base["five_family_macro"]["decimal"]
        candidate_macro = candidate["five_family_macro"]["decimal"]
        macro_delta = value["five_family_macro_delta"]["decimal"]
        macro_valid = (
            all(isinstance(item, (int, float)) for item in (base_macro, candidate_macro, macro_delta))
            and 0 <= base_macro <= 1
            and 0 <= candidate_macro <= 1
            and abs((candidate_macro - base_macro) - macro_delta) <= 1e-12
        )
        evidence_bound = all(
            isinstance(evidence.get(key), str) and len(evidence[key]) == 64
            for key in ("base_result_set_sha256", "candidate_result_set_sha256", "source_task_set_sha256")
        )
        lane_transitions_complete = all(
            sum(int(paired_lanes[lane].get(key, -1)) for key in ("wins", "losses", "ties")) == 60
            for lane in LANES
        )
        lane_passes_valid = all(
            0 <= int(base["lanes"][lane].get("passed", -1)) <= 60
            and 0 <= int(candidate["lanes"][lane].get("passed", -1)) <= 60
            for lane in LANES
        )
        valid = (
            value.get("schema_version") == "1.0"
            and seal is not None
            and base.get("task_count") == 360
            and candidate.get("task_count") == 360
            and aggregate.get("denominator") == 360
            and sum(aggregate.get(key, -1) for key in ("wins", "losses", "ties")) == 360
            and set(lane_denominators.values()) == {60}
            and set(base_lane_denominators.values()) == {60}
            and set(candidate_lane_denominators.values()) == {60}
            and lane_transitions_complete
            and lane_passes_valid
            and evidence_bound
            and macro_valid
        )
        return valid, {
            "report_sha256": seal,
            "base_model": value.get("base_model"),
            "candidate_model": value.get("candidate_model"),
            "base_tasks": base.get("task_count"),
            "candidate_tasks": candidate.get("task_count"),
            "paired_denominator": aggregate.get("denominator"),
            "lane_denominators": lane_denominators,
            "base_lane_denominators": base_lane_denominators,
            "candidate_lane_denominators": candidate_lane_denominators,
            "result_sets": evidence,
        }
    except (KeyError, TypeError, ValueError):
        return False, {"report_sha256": None, "error": "incomplete comparison contract"}


def manifest_contract(paths: list[Path]) -> tuple[bool, list[dict[str, Any]], dict[str, Any] | None, dict[str, Any] | None]:
    rows = []
    required: dict[str, tuple[dict[str, Any], str]] = {}
    schema_to_name = {schema: name for name, schema in REQUIRED_MANIFEST_SCHEMAS.items()}
    for path in paths:
        try:
            value = load(path)
            present = [field for field in SEAL_FIELDS if field in value]
            field = present[0] if len(present) == 1 else None
            seal = verified_seal(value, field) if field else None
            passed = seal is not None
            schema = value.get("schema_version")
            name = schema_to_name.get(schema)
            if name is not None:
                if name in required:
                    passed = False
                else:
                    required[name] = (value, file_sha256(path))
                if name == "seed":
                    passed = passed and value.get("total_records", 0) > 0 and isinstance(value.get("source_revision"), str)
                elif name == "readiness":
                    passed = passed and value.get("status") == "ready" and value.get("model_id") == QWEN_MODEL_ID and value.get("revision") == QWEN_REVISION
                elif name == "execution_card":
                    passed = passed and value.get("status") == "ready" and value.get("output_model_name") == "ganesh-mini-1.0"
                elif name == "training_run":
                    passed = (
                        passed and value.get("status") == "complete"
                        and value.get("identities", {}).get("model_revision") == QWEN_REVISION
                        and value.get("save_reload", {}).get("passed") is True
                    )
                elif name == "artifacts":
                    base = value.get("base_model", {})
                    llama = value.get("llama_cpp", {})
                    passed = (
                        passed and value.get("status") == "built" and value.get("model_name") == "ganesh-mini-1.0"
                        and base.get("model_id") == QWEN_MODEL_ID and base.get("revision") == QWEN_REVISION
                        and all(isinstance(base.get(key), str) and len(base[key]) == 64 for key in ("inventory_sha256", "readiness_report_sha256", "artifact_sha256"))
                        and isinstance(llama.get("revision"), str) and len(llama["revision"]) == 40
                        and isinstance(llama.get("llama_cli_sha256"), str) and len(llama["llama_cli_sha256"]) == 64
                    )
                elif name == "export_equivalence":
                    passed = passed and value.get("status") == "passed" and value.get("task_count") == 6
            rows.append({
                "path": str(path),
                "sha256": file_sha256(path),
                "schema_version": schema,
                "seal_field": field,
                "seal": seal,
                "passed": passed,
            })
        except (OSError, json.JSONDecodeError, TypeError):
            rows.append({"path": str(path), "sha256": None, "seal": None, "passed": False})
    seed_entry = required.get("seed")
    readiness_entry = required.get("readiness")
    card_entry = required.get("execution_card")
    training_entry = required.get("training_run")
    artifact_entry = required.get("artifacts")
    export_entry = required.get("export_equivalence")
    seed, seed_file_sha = seed_entry if seed_entry else ({}, "")
    readiness = readiness_entry[0] if readiness_entry else {}
    card = card_entry[0] if card_entry else {}
    training = training_entry[0] if training_entry else {}
    artifact_manifest = artifact_entry[0] if artifact_entry else None
    export_equivalence = export_entry[0] if export_entry else None
    linked = (
        set(required) == set(REQUIRED_MANIFEST_SCHEMAS)
        and readiness.get("seed_manifest_seal") == seed.get("manifest_sha256")
        and readiness.get("seed_manifest_sha256") == seed_file_sha
        and card.get("inputs", {}).get("seed_manifest_sha256") == seed_file_sha
        and training.get("identities", {}).get("card_sha256") == card.get("card_sha256")
        and artifact_manifest is not None
        and artifact_manifest.get("selected_run_evidence_sha256") == training.get("evidence_sha256")
        and export_equivalence is not None
        and export_equivalence.get("artifact_manifest_sha256") == artifact_manifest.get("manifest_sha256")
    )
    valid = bool(rows) and all(row["passed"] for row in rows) and linked
    return valid, rows, artifact_manifest, export_equivalence


def adjudicate(
    base_comparison: dict[str, Any],
    ganesh_v01_comparison: dict[str, Any],
    quant_comparison: dict[str, Any],
    laptop: dict[str, Any],
    manifests: list[Path],
) -> dict[str, Any]:
    base_valid, base_contract = comparison_contract(base_comparison)
    v01_valid, v01_contract = comparison_contract(ganesh_v01_comparison)
    quant_valid, quant_contract = comparison_contract(quant_comparison)
    laptop_seal = verified_seal(laptop, "evidence_sha256")
    manifests_valid, manifest_evidence, artifact_manifest, export_equivalence = manifest_contract(manifests)

    base_model = base_comparison.get("base_model", {})
    candidate_model = base_comparison.get("candidate_model", {})
    v01_base_model = ganesh_v01_comparison.get("base_model", {})
    v01_candidate_model = ganesh_v01_comparison.get("candidate_model", {})
    exact_model_contract = (
        base_valid
        and base_model.get("model_id") == QWEN_MODEL_ID
        and base_model.get("revision") == QWEN_REVISION
        and candidate_model.get("revision") == QWEN_REVISION
        and str(candidate_model.get("model_id", "")).startswith("ganesh-mini-1.0")
        and v01_valid
        and v01_base_model.get("model_id") == "ganesh-v0.1"
        and v01_candidate_model == candidate_model
    )

    delta = base_comparison.get("five_family_macro_delta", {}).get("decimal")
    paired = base_comparison.get("paired", {})
    cluster = paired.get("cluster_aware", {})
    bootstrap = cluster.get("bootstrap_ci", {})
    lane_deltas = {
        lane: base_comparison.get("candidate", {}).get("lanes", {}).get(lane, {}).get("passed", -10**9)
        - base_comparison.get("base", {}).get("lanes", {}).get(lane, {}).get("passed", 0)
        for lane in LANES
    }
    try:
        merged = total_passes(quant_comparison["base"])
        q8 = total_passes(quant_comparison["candidate"])
        retention = q8 / merged if merged else 1.0
    except (KeyError, TypeError, ValueError):
        merged = q8 = 0
        retention = 0.0

    profiles = laptop.get("profiles", {}) if isinstance(laptop, dict) else {}
    artifacts = artifact_manifest.get("artifacts", {}) if artifact_manifest else {}
    q8_artifact = artifacts.get("gguf_q8", {})
    f16_artifact = artifacts.get("gguf_f16", {})
    q8_profile = profiles.get("q8", {})
    f16_profile = profiles.get("f16", {})
    quant_base_model = quant_comparison.get("base_model", {})
    quant_candidate_model = quant_comparison.get("candidate_model", {})
    quant_artifacts_bound = (
        quant_valid
        and quant_base_model.get("artifact_sha256") == artifacts.get("merged_bf16_hf", {}).get("sha256")
        and candidate_model.get("artifact_sha256") == artifacts.get("merged_bf16_hf", {}).get("sha256")
        and quant_candidate_model.get("artifact_sha256") == q8_artifact.get("sha256")
        and str(quant_base_model.get("model_id", "")).startswith("ganesh-mini-1.0")
        and str(quant_candidate_model.get("model_id", "")).startswith("ganesh-mini-1.0")
    )
    laptop_artifacts_bound = (
        laptop_seal is not None
        and laptop.get("schema_version") == "ganesh-mini-laptop-certification/v1"
        and laptop.get("status") == "passed"
        and laptop.get("artifact_manifest_sha256") == (artifact_manifest or {}).get("manifest_sha256")
        and laptop.get("llama_cpp_revision") == (artifact_manifest or {}).get("llama_cpp", {}).get("revision")
        and laptop.get("llama_cli_sha256") == (artifact_manifest or {}).get("llama_cpp", {}).get("llama_cli_sha256")
        and q8_profile.get("artifact", {}).get("sha256") == q8_artifact.get("sha256")
        and f16_profile.get("artifact", {}).get("sha256") == f16_artifact.get("sha256")
        and isinstance(q8_artifact.get("sha256"), str)
        and isinstance(f16_artifact.get("sha256"), str)
    )

    v01_delta = ganesh_v01_comparison.get("five_family_macro_delta", {}).get("decimal")
    source_task_sets = {
        contract.get("result_sets", {}).get("source_task_set_sha256")
        for contract in (base_contract, v01_contract, quant_contract)
    }
    same_decision_surface = base_valid and v01_valid and quant_valid and len(source_task_sets) == 1 and None not in source_task_sets
    checks = [
        check("sealed_complete_decision_comparisons", base_valid and v01_valid and quant_valid,
              qwen=base_contract, ganesh_v01=v01_contract, quantization=quant_contract),
        check("identical_frozen_decision_surface", same_decision_surface, source_task_set_sha256=next(iter(source_task_sets)) if same_decision_surface else None),
        check("exact_model_and_reference_identities", exact_model_contract,
              qwen_base=base_model, ganesh_mini=candidate_model, ganesh_v01=v01_base_model),
        check("positive_five_family_macro", base_valid and isinstance(delta, (int, float)) and delta > 0, delta=delta),
        check(
            "cluster_supported_improvement",
            base_valid
            and isinstance(bootstrap.get("lower"), (int, float))
            and bootstrap["lower"] > 0
            and isinstance(cluster.get("two_sided_permutation_p"), (int, float))
            and cluster["two_sided_permutation_p"] <= 0.05,
            cluster_aware=cluster,
        ),
        check("no_lane_regresses_more_than_two", base_valid and all(value >= -2 for value in lane_deltas.values()), lane_pass_deltas=lane_deltas),
        check("ganesh_v01_reference_executed", v01_valid, comparison=v01_contract, ganesh_mini_minus_v01_macro=v01_delta),
        check("quantization_comparison_binds_release_artifacts", quant_artifacts_bound,
              merged_model=quant_base_model, q8_model=quant_candidate_model),
        check("q8_retains_98_percent", quant_artifacts_bound and retention >= 0.98, merged_solved=merged, q8_solved=q8, retention=retention),
        check("laptop_evidence_and_artifacts_bound", laptop_artifacts_bound, laptop_evidence_sha256=laptop_seal, q8=q8_profile, f16=f16_profile),
        check("q8_8gb_profile", laptop_artifacts_bound and q8_profile.get("passed") is True and q8_profile.get("peak_rss_bytes", 8 * 1024**3) <= 7 * 1024**3, profile=q8_profile),
        check("f16_16gb_profile", laptop_artifacts_bound and f16_profile.get("passed") is True and f16_profile.get("peak_rss_bytes", 16 * 1024**3) <= 14 * 1024**3, profile=f16_profile),
        check("six_lane_export_equivalence", export_equivalence is not None and export_equivalence.get("status") == "passed", evidence_sha256=export_equivalence.get("evidence_sha256") if export_equivalence else None),
        check("required_manifests_complete", manifests_valid, manifests=manifest_evidence),
    ]
    eligible = all(row["passed"] for row in checks)
    report = {
        "schema_version": "ganesh-mini-release-decision/v2",
        "model_name": "ganesh-mini-1.0",
        "status": "release-eligible" if eligible else "release-blocked",
        "checks": checks,
        "failed_checks": [row["name"] for row in checks if not row["passed"]],
        "reference_comparison": {
            "ganesh_v01_report_sha256": v01_contract.get("report_sha256"),
            "ganesh_mini_minus_v01_five_family_macro": v01_delta,
            "ganesh_v01_stronger_absolute_correctness": isinstance(v01_delta, (int, float)) and v01_delta < 0,
        },
    }
    report["evidence_sha256"] = canonical_sha256(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-comparison", type=Path, required=True)
    parser.add_argument("--ganesh-v01-comparison", type=Path, required=True)
    parser.add_argument("--quant-comparison", type=Path, required=True)
    parser.add_argument("--laptop-certification", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = adjudicate(
        load(args.base_comparison),
        load(args.ganesh_v01_comparison),
        load(args.quant_comparison),
        load(args.laptop_certification),
        args.manifest,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if report["status"] == "release-eligible" else 2


if __name__ == "__main__":
    raise SystemExit(main())
