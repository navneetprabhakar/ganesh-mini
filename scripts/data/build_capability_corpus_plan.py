#!/usr/bin/env python3
"""Seal the local, non-executable Gate 2 capability-corpus contract."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
TASK_TYPES = ("generation", "repair")
CAPABILITIES = {
    "associative_aggregation": "group, join, index, count, or aggregate records through maps or equivalent associative collections",
    "binary_and_bitwise": "transform byte-oriented data, masks, flags, compact encodings, or checksums",
    "callbacks_and_events": "coordinate callback, listener, handler, or event-driven control flow with explicit completion semantics",
    "graph_and_tree": "traverse or transform explicit graph, tree, dependency, hierarchy, or path structures",
    "numeric_reasoning": "implement bounded numeric transformations, ranges, ratios, accumulation, or integer-safe arithmetic",
    "ordering_and_selection": "rank, sort, select, merge, or prioritize values with explicit deterministic tie behavior",
    "parsing_and_encoding": "parse, validate, normalize, encode, decode, or serialize a defined textual or structured format",
    "sequence_algorithms": "transform, scan, partition, window, segment, rotate, or combine ordered sequences",
    "stateful_workflows": "implement an isolated stateful component with explicit transitions, rollback, idempotency, or lifecycle rules",
    "string_and_unicode": "transform or analyze text with explicit character, normalization, whitespace, or Unicode semantics",
}
CROSS_CUTTING = (
    "duplicate_handling",
    "immutability_and_aliasing",
    "malformed_input",
    "stable_ordering",
    "state_isolation",
)


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(payload).hexdigest()


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop(field, None)
    if claimed != canonical_sha256(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def cell_contracts() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for capability_index, capability in enumerate(CAPABILITIES):
        for lane_index, lane in enumerate(LANES):
            for type_index, task_type in enumerate(TASK_TYPES):
                cross_index = capability_index * len(LANES) * len(TASK_TYPES) + lane_index * len(TASK_TYPES) + type_index
                rows.append({
                    "cell_id": f"{capability}/{lane}/{task_type}",
                    "primary_capability": capability,
                    "lane": lane,
                    "task_type": task_type,
                    "assigned_cross_cutting_dimension": CROSS_CUTTING[cross_index % len(CROSS_CUTTING)],
                    "qualification_drafts": 2,
                    "qualification_minimum_admitted": 1,
                    "pilot_minimum_admitted": 6,
                    "pilot_maximum_drafts": 10,
                })
    return rows


def build(diversity_path: Path, gradient_campaign_path: Path) -> dict[str, Any]:
    diversity = load_sealed(diversity_path, "report_sha256")
    campaign = load_sealed(gradient_campaign_path, "evidence_sha256")
    if (
        diversity.get("schema_version") != "ganesh-mini-training-corpus-diversity-audit/v1"
        or diversity.get("status") != "complete-non-evaluation-audit"
        or diversity.get("scope", {}).get("evaluation_surfaces_read") != 0
        or diversity.get("corpus", {}).get("records") != 3225
        or diversity.get("selected_probe", {}).get("records") != 640
    ):
        raise ValueError("diversity evidence does not support the construction plan")
    if (
        campaign.get("schema_version") != "ganesh-mini-expansion-campaign-result/v1"
        or campaign.get("status") != "completed-gradient-audit-no-conflict"
    ):
        raise ValueError("gradient campaign is not the required terminal diagnostic")

    cells = cell_contracts()
    plan: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-stratified-corpus-plan/v1",
        "status": "local-contract-sealed-qualification-implementation-next",
        "gate": 2,
        "source_evidence": {
            "diversity_audit_path": str(diversity_path),
            "diversity_audit_sha256": diversity["report_sha256"],
            "gradient_campaign_path": str(gradient_campaign_path),
            "gradient_campaign_sha256": campaign["evidence_sha256"],
            "evaluation_surfaces_read_for_plan": 0,
        },
        "ontology": {
            "primary_capabilities": CAPABILITIES,
            "cross_cutting_dimensions": list(CROSS_CUTTING),
            "assignment_rule": "exactly one primary capability and exactly one scheduled cross-cutting dimension per cell; a candidate may specify at most one additional cross-cutting dimension when intrinsically required",
            "forbidden_shortcut": "generic malformed/boundary/order/mutation boilerplate cannot count as primary-capability conformance",
        },
        "matrix": {
            "lanes": list(LANES),
            "task_types": list(TASK_TYPES),
            "cells": len(cells),
            "cell_contracts": cells,
        },
        "qualification": {
            "drafts": 240,
            "distinct_training_source_stimuli": 240,
            "minimum_admitted": 120,
            "minimum_admitted_per_cell": 1,
            "maximum_one_replacement_draft_per_missing_cell": True,
            "stop_if_any_cell_remains_empty": True,
            "purpose": "measure teacher conformance, executable yield, and matrix feasibility before authorizing full construction",
        },
        "pilot_corpus_target": {
            "new_records": 720,
            "new_records_per_cell": 6,
            "maximum_new_drafts": 1200,
            "broad_replay_records": 180,
            "broad_replay_records_per_lane_and_task_type": 15,
            "total_records": 900,
            "construction_authority": "the 240-draft non-GCloud qualification is authorized by standing project scope; expansion beyond qualification is conditional on a sealed passing qualification result",
        },
        "construction_isolation": {
            "source_selection": "training-source queues only; source stimulus must be unique within the new corpus",
            "classifier_visibility": "training source stimulus and ontology only",
            "teacher_visibility": "training stimulus, assigned primary capability, assigned cross-cutting dimension, and language runtime contract only",
            "test_author_visibility": "candidate specification only; no reference, known-bad implementation, evaluation data, or teacher context",
            "semantic_reviewer_visibility": "candidate specification and assigned ontology labels only; no evaluation data or verifier outputs",
            "evaluation_records_in_training": 0,
        },
        "admission": {
            "required": [
                "reference passes the pinned network-disabled verifier",
                "every known-bad implementation fails behaviorally",
                "semantic reviewer confirms the assigned primary capability is substantive",
                "runtime, dependency, timeout, and output contracts pass",
                "exact, normalized, and fuzzy separation from every training and evaluation surface passes",
                "source lineage, teacher evidence, record ID, rendered prompt hash, tests, and verifier evidence are sealed",
            ],
            "corpus_gates": {
                "all_120_cells_meet_minimum": True,
                "unique_source_stimulus_ratio": 1.0,
                "maximum_normalized_scaffold_cluster_share": 0.02,
                "minimum_blind_manual_reviews_per_primary_capability": 2,
                "maximum_correction_passes_per_candidate": 1,
            },
        },
        "hard_stops": [
            "qualification admits fewer than 120 records",
            "any qualification cell remains empty after its one bounded replacement",
            "any evaluation artifact is read by classifier, teacher, reviewer, or candidate construction",
            "capability conformance or executable admission fails",
            "pilot target requires more than 1200 new drafts",
            "global separation or lineage evidence is incomplete",
        ],
        "forbidden": [
            "deriving training specifications from private development or decision tasks",
            "using private task archetype names as teacher prompts or corpus labels",
            "reusing the unchanged all-edge-cases teacher instruction",
            "claiming semantic diversity from lexical tags or prompt uniqueness alone",
            "training, evaluation, promotion, merge, quantization, or publication",
            "any GCloud read, upload, mutation, or billing action",
        ],
        "gcloud_authority": "none",
        "training_authority": "none",
        "promotion_authority": "none",
    }
    plan["plan_sha256"] = canonical_sha256(plan)
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diversity-audit", type=Path, required=True)
    parser.add_argument("--gradient-campaign", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = build(args.diversity_audit, args.gradient_campaign)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": plan["status"], "plan_sha256": plan["plan_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
