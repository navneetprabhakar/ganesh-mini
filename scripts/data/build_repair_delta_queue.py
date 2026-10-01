#!/usr/bin/env python3
"""Build a sealed, explicitly versioned repair-delta queue."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.build_capability_corpus_plan import CAPABILITIES, LANES, canonical_sha256, cell_contracts


PLAN_SHA256 = "4023a896300112f9f93f2a16698d549f203e3e75b4e71ae054f3a98463e2f0f0"
CONTRACT_ID = "capability-stratified-v3-repair-delta/v1"
SEED = 3503
V4_PLAN_SHA256 = "79849d2f8b70ba69572b4c3fa1761bdb413562c6f6d9a12537d93a1724812ef6"
V4_CONTRACT_ID = "capability-stratified-v4-repair-delta/v1"
V4_SEED = "ganesh-mini-gate2-v4-repair-delta-queue-v1"
ONTOLOGY_AGGREGATE_SCHEMA = "ganesh-mini-repair-source-ontology-aggregate/v1"
AFFINITY_FIELDS = (
    "capability_operation_present", "identifiable_defect_affordance",
    "self_contained_standard_library_feasible", "code_repair_material",
    "forbidden_dependency_absent",
)
QUALIFICATION_DATASETS = (
    "Multilingual-Multimodal-NLP/McEval-Instruct",
    "m-a-p/MdEval-Instruct",
)
DEFAULT_ADMISSION_CONFIG = ROOT / "configs/data/expansion_v1.json"
DEFAULT_RUNTIME_CONFIG = ROOT / "configs/eval/runtimes.json"
DEFAULT_V4_PREFLIGHT_CONFIG = ROOT / "configs/data/gate2_v4_post_teacher_preflight.json"


def contract_spec(version: str = "v3") -> dict[str, Any]:
    if version == "v3":
        return {
            "version": "v3", "plan_sha256": PLAN_SHA256, "contract_id": CONTRACT_ID,
            "seed": SEED, "id_prefix": "cap-v3",
            "assignment_schema": "ganesh-mini-repair-delta-assignment/v1",
            "manifest_schema": "ganesh-mini-repair-delta-queue-manifest/v1",
        }
    if version == "v4":
        return {
            "version": "v4", "plan_sha256": V4_PLAN_SHA256, "contract_id": V4_CONTRACT_ID,
            "seed": V4_SEED, "id_prefix": "cap-v4",
            "assignment_schema": "ganesh-mini-repair-delta-v4-assignment/v1",
            "manifest_schema": "ganesh-mini-repair-delta-v4-queue-manifest/v1",
        }
    raise ValueError(f"unsupported repair-delta contract version {version!r}")


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def source_key(row: dict[str, Any]) -> tuple[str, str, str]:
    candidate = row.get("candidate") if isinstance(row.get("candidate"), dict) else {}
    source = row.get("source") or row.get("lineage") or candidate.get("source") or {}
    key = tuple(source.get(field) for field in ("dataset", "revision", "record_id"))
    if not all(isinstance(value, str) and value for value in key):
        raise ValueError(f"{row.get('id')}: incomplete source identity")
    return key  # type: ignore[return-value]


def load_separation(path: Path, source_queue_sha256: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop("attestation_sha256", None)
    if (
        claimed != canonical_sha256(value)
        or value.get("source_queue_sha256") != source_queue_sha256
        or value.get("evaluation_content_exposed") is not False
        or value.get("exact_normalized_fuzzy_exclusion_complete") is not True
        or not isinstance(value.get("eligible_source_queue_ids"), list)
    ):
        raise ValueError("source separation attestation is invalid")
    value["attestation_sha256"] = claimed
    return value


def load_separation_bindings(
    bindings: list[tuple[Path, Path]], final_sources: dict[str, dict[str, Any]],
) -> tuple[dict[str, set[str]], list[dict[str, Any]]]:
    """Validate each attestation against its exact queue and the final queue superset."""
    if not bindings:
        raise ValueError("at least one source separation binding is required")
    eligibility: dict[str, set[str]] = {}
    manifests: list[dict[str, Any]] = []
    for attestation_path, bound_queue_path in bindings:
        bound_bytes = bound_queue_path.read_bytes()
        attestation = load_separation(attestation_path, hashlib.sha256(bound_bytes).hexdigest())
        bound_sources: dict[str, dict[str, Any]] = {}
        for row in read_jsonl(bound_queue_path):
            identifier = row.get("id")
            if not isinstance(identifier, str) or not identifier or identifier in bound_sources:
                raise ValueError("bound source queue contains a malformed or duplicate ID")
            bound_sources[identifier] = row
        eligible_ids = attestation["eligible_source_queue_ids"]
        if (
            len(eligible_ids) != len(set(eligible_ids))
            or any(not isinstance(identifier, str) or identifier not in bound_sources for identifier in eligible_ids)
        ):
            raise ValueError("source separation eligibility is malformed or outside its bound source queue")
        attestation_sha256 = attestation["attestation_sha256"]
        repair_projection = [
            bound_sources[identifier] for identifier in eligible_ids
            if bound_sources[identifier].get("task_type") == "repair"
        ]
        for row in repair_projection:
            if final_sources.get(row["id"]) != row:
                raise ValueError("final source queue changed or omitted an eligible bound repair row")
        repair_ids = {row["id"] for row in repair_projection}
        non_repair_projection = [
            bound_sources[identifier] for identifier in eligible_ids
            if bound_sources[identifier].get("task_type") != "repair"
        ]
        non_repair_missing = sum(row["id"] not in final_sources for row in non_repair_projection)
        non_repair_changed = sum(
            row["id"] in final_sources and final_sources[row["id"]] != row
            for row in non_repair_projection
        )
        if attestation_sha256 in eligibility:
            raise ValueError("duplicate source separation binding")
        eligibility[attestation_sha256] = repair_ids
        repair_payload = b"".join(canonical_json(row) + b"\n" for row in repair_projection)
        manifests.append({
            "attestation_sha256": attestation_sha256,
            "attestation_file_sha256": hashlib.sha256(attestation_path.read_bytes()).hexdigest(),
            "bound_source_queue_sha256": hashlib.sha256(bound_bytes).hexdigest(),
            "eligible_source_count": len(eligible_ids),
            "bound_repair_projection_count": len(repair_projection),
            "bound_repair_projection_sha256": hashlib.sha256(repair_payload).hexdigest(),
            "bound_non_repair_projection_count": len(non_repair_projection),
            "non_repair_missing_from_final_count": non_repair_missing,
            "non_repair_changed_or_colliding_count": non_repair_changed,
            "non_repair_difference_count": non_repair_missing + non_repair_changed,
        })
    return eligibility, manifests


def load_v4_affinity_aggregate_context(
    summary_path: Path, evidence_path: Path, source_queue_sha256: str,
    separation_attestation_sha256s: set[str],
) -> tuple[set[str], dict[str, Any]]:
    """Validate the sealed mixed-plan aggregate that authorizes V4 affinity input."""
    value = json.loads(summary_path.read_text(encoding="utf-8"))
    body = dict(value)
    claimed = body.pop("aggregate_sha256", None)
    compatible = value.get("compatible_plan_sha256s")
    allowed_compatible = {PLAN_SHA256}
    rows = read_jsonl(evidence_path)
    source_ids = [row.get("source_queue_id") for row in rows]
    ontology_plans = {
        row.get("plan_sha256") for row in rows
        if row.get("schema_version") == "ganesh-mini-repair-source-ontology/v1"
    }
    attestation_sha256s = value.get("separation_attestation_sha256s")
    if (
        claimed != canonical_sha256(body)
        or value.get("schema_version") != ONTOLOGY_AGGREGATE_SCHEMA
        or value.get("plan_sha256") != V4_PLAN_SHA256
        or not isinstance(compatible, list)
        or len(compatible) != len(set(compatible))
        or any(item not in allowed_compatible for item in compatible)
        or value.get("status") != "coverage-complete"
        or value.get("source_queue_sha256") != source_queue_sha256
        or value.get("combined_evidence_sha256") != hashlib.sha256(evidence_path.read_bytes()).hexdigest()
        or value.get("evaluation_artifacts_read") != 0
        or ontology_plans - {V4_PLAN_SHA256} != set(compatible)
        or not isinstance(attestation_sha256s, list)
        or len(attestation_sha256s) != len(set(attestation_sha256s))
        or set(attestation_sha256s) != separation_attestation_sha256s
        or type(value.get("unique_sources")) is not int
        or value["unique_sources"] != len(rows)
        or len(source_ids) != len(set(source_ids))
    ):
        raise ValueError("V4 affinity aggregate context is invalid or unsealed")
    return {V4_PLAN_SHA256, *compatible}, {
        "summary_file_sha256": hashlib.sha256(summary_path.read_bytes()).hexdigest(),
        "aggregate_sha256": claimed,
        "compatible_plan_sha256s": compatible,
    }


def load_affinity(
    path: Path, separation: str | dict[str, set[str]], sources: dict[str, dict[str, Any]],
    plan_sha256: str = PLAN_SHA256,
    allowed_plan_sha256s: set[str] | None = None,
    candidate_source_ids: set[str] | None = None,
) -> dict[tuple[str, str], dict[str, Any]]:
    allowed_plans = allowed_plan_sha256s or {plan_sha256}
    if plan_sha256 not in allowed_plans:
        raise ValueError("selected plan is absent from allowed ontology plans")
    separation_eligibility = {separation: set(sources)} if isinstance(separation, str) else separation
    output: dict[tuple[str, str], dict[str, Any]] = {}
    ontology_sources: set[str] = set()
    for row in read_jsonl(path):
        body = dict(row)
        claimed = body.pop("evidence_sha256", None)
        separation_sha256 = row.get("separation_attestation_sha256")
        separation_ok = (
            isinstance(separation_sha256, str)
            and separation_sha256 in separation_eligibility
            and row.get("source_queue_id") in separation_eligibility[separation_sha256]
        )
        if row.get("schema_version") == "ganesh-mini-repair-source-ontology/v1":
            source = sources.get(row.get("source_queue_id"))
            batch_ids = row.get("batch_source_queue_ids")
            batch_sources = [sources.get(identifier) for identifier in batch_ids] if isinstance(batch_ids, list) else []
            verdicts = row.get("verdicts")
            raw_prompt = row.get("raw_prompt")
            raw_output = row.get("raw_output")
            if (
                claimed != canonical_sha256(body)
                or row.get("plan_sha256") not in allowed_plans
                or not separation_ok
                or row.get("evaluation_artifacts_read") != 0
                or source is None or source.get("lane") != row.get("lane")
                or row.get("source_queue_id") in ontology_sources
                or row.get("source_record_sha256") != source.get("source", {}).get("source_record_sha256")
                or row.get("source_identity") != {
                    key: source.get("source", {}).get(key) for key in ("dataset", "revision", "record_id")
                }
                or row.get("stimulus_sha256") != hashlib.sha256(source["stimulus"].encode()).hexdigest()
                or not isinstance(batch_ids, list) or not batch_ids or len(set(batch_ids)) != len(batch_ids)
                or row.get("source_queue_id") not in batch_ids
                or any(item is None for item in batch_sources)
                or any(item.get("lane") not in LANES or item.get("task_type") != "repair" for item in batch_sources)
                or len({source_key(item) for item in batch_sources}) != len(batch_sources)
                or row.get("batch_source_records_sha256") != canonical_sha256(batch_sources)
                or not isinstance(raw_prompt, str) or raw_prompt != ontology_affinity_prompt(batch_sources)
                or row.get("prompt_sha256") != hashlib.sha256(raw_prompt.encode()).hexdigest()
                or not isinstance(raw_output, str)
                or row.get("output_sha256") != hashlib.sha256(raw_output.encode()).hexdigest()
                or not isinstance(row.get("runtime_parameters"), dict)
                or type(row.get("selection_rank")) is not int or row["selection_rank"] < 0
                or not isinstance(verdicts, list) or len(verdicts) != len(CAPABILITIES)
            ):
                raise ValueError("source-ontology evidence is incomplete or unsealed")
            seen: set[str] = set()
            expected_verdict_fields = {
                "primary_capability", "decision", "capability_operation", "defect_affordance",
                *AFFINITY_FIELDS,
            }
            for verdict in verdicts:
                capability = verdict.get("primary_capability") if isinstance(verdict, dict) else None
                decision = verdict.get("decision") if isinstance(verdict, dict) else None
                if (
                    not isinstance(verdict, dict)
                    or set(verdict) != expected_verdict_fields
                    or capability not in CAPABILITIES or capability in seen
                    or decision not in {"accept", "reject"}
                    or any(type(verdict.get(field)) is not bool for field in AFFINITY_FIELDS)
                    or (decision == "accept" and any(verdict.get(field) is not True for field in AFFINITY_FIELDS))
                    or (decision == "reject" and all(verdict.get(field) is True for field in AFFINITY_FIELDS))
                    or not all(isinstance(verdict.get(field), str) and verdict[field] for field in (
                        "capability_operation", "defect_affordance",
                    ))
                ):
                    raise ValueError("source-ontology verdict is malformed")
                seen.add(capability)
            if seen != set(CAPABILITIES):
                raise ValueError("source-ontology verdicts do not cover the frozen ontology")
            ontology_sources.add(source["id"])
            if candidate_source_ids is not None and source["id"] not in candidate_source_ids:
                continue
            for verdict in verdicts:
                capability = verdict["primary_capability"]
                cell_id = f"{capability}/{source['lane']}/repair"
                output[(cell_id, source["id"])] = {
                    **verdict, "schema_version": row["schema_version"],
                    "source_queue_id": source["id"], "cell_id": cell_id,
                    "selection_rank": row["selection_rank"],
                    "source_record_sha256": row["source_record_sha256"],
                    "stimulus_sha256": row["stimulus_sha256"],
                    "prompt_sha256": row["prompt_sha256"], "raw_prompt": row["raw_prompt"],
                    "output_sha256": row["output_sha256"], "raw_output": row["raw_output"],
                    "runtime_parameters": row["runtime_parameters"], "evidence_sha256": claimed,
                    "separation_attestation_sha256": separation_sha256,
                    "classification_mode": "full_ontology",
                }
            continue
        if (
            claimed != canonical_sha256(body)
            or row.get("schema_version") != "ganesh-mini-repair-source-affinity/v1"
            or not separation_ok
            or row.get("decision") not in {"accept", "reject"}
            or (row.get("decision") == "accept" and any(row.get(field) is not True for field in AFFINITY_FIELDS))
            or row.get("evaluation_artifacts_read") != 0
            or not all(isinstance(row.get(field), str) and row[field] for field in (
                "source_queue_id", "cell_id", "source_record_sha256", "stimulus_sha256",
                "capability_operation", "defect_affordance", "prompt_sha256", "output_sha256", "raw_output",
            ))
            or not isinstance(row.get("runtime_parameters"), dict)
            or type(row.get("selection_rank")) is not int or row["selection_rank"] < 0
        ):
            raise ValueError("source-affinity evidence is incomplete or unsealed")
        if candidate_source_ids is not None and row["source_queue_id"] not in candidate_source_ids:
            continue
        key = (row["cell_id"], row["source_queue_id"])
        if key in output:
            raise ValueError("duplicate source-affinity decision")
        output[key] = row
    return output


def repair_cells() -> list[dict[str, Any]]:
    return [cell for cell in cell_contracts() if cell["task_type"] == "repair"]


def affinity_prompt(cell: dict[str, Any], source: dict[str, Any]) -> str:
    visible = {
        "source_queue_id": source["id"], "lane": source["lane"], "task_type": source["task_type"],
        "stimulus": source["stimulus"],
        "source_lineage": {key: source["source"].get(key) for key in (
            "dataset", "revision", "record_id", "source_record_sha256",
        )},
        "primary_capability": cell["primary_capability"],
        "primary_capability_definition": CAPABILITIES[cell["primary_capability"]],
    }
    return f"""Classify one training-only repair stimulus for source affinity. Do not use tools or inspect files.
Input: {json.dumps(visible, separators=(",", ":"), ensure_ascii=False)}
Accept only if it contains a capability-specific operation and identifiable defect affordance, can become one
self-contained standard-library-only source file, is code-repair material rather than MCQ/prose/configuration, and
requires no filesystem, network, clock, randomness, installation, external dependency, framework, or service.
Return the fixed structured decision contract only. Evaluation disjointness is handled outside this classifier."""


def ontology_affinity_prompt(sources: list[dict[str, Any]]) -> str:
    visible = []
    for row in sources:
        item = {
            "source_queue_id": row["id"], "lane": row["lane"], "task_type": row["task_type"],
            "stimulus": row["stimulus"],
            "source_lineage": {key: row["source"].get(key) for key in (
                "dataset", "revision", "record_id", "source_record_sha256",
            )},
        }
        projected_fields = ("source_language", "target_lane", "original_role", "derivation_kind")
        if any(field in row for field in projected_fields):
            if not all(isinstance(row.get(field), str) and row[field] for field in projected_fields):
                raise ValueError("projected repair source has incomplete derivation metadata")
            transformation = row.get("source", {}).get("transformation")
            if not isinstance(transformation, str) or not transformation:
                raise ValueError("projected repair source has no transparent transformation text")
            item.update({field: row[field] for field in projected_fields})
            item["transformation"] = transformation
        visible.append(item)
    return f"""Classify each training-only repair stimulus independently against every capability. Do not use tools or inspect files.
Capability ontology: {json.dumps(CAPABILITIES, separators=(',', ':'), sort_keys=True)}
Inputs: {json.dumps(visible, separators=(',', ':'), ensure_ascii=False)}

For every input return exactly one verdict for every ontology capability. Multiple capabilities may pass. Accept a
capability only when the stimulus contains that capability-specific operation plus an identifiable defect affordance,
can become one self-contained standard-library-only source file, is actual code-repair material, and requires no
filesystem, network, clock, randomness, installation, external dependency, framework, or service. For a rejection,
set each boolean independently and explain the actual operation and defect affordance (or their absence). Do not force
the source into a capability. Return only the fixed structured contract. Evaluation separation is handled elsewhere."""


def selection_key(cell_id: str, source_id: str, seed: int | str = SEED) -> str:
    return hashlib.sha256(f"{seed}\0{cell_id}\0{source_id}".encode()).hexdigest()


def match_two_slot_sources(
    cells: list[dict[str, Any]],
    sources: dict[str, dict[str, Any]],
    affinity: dict[tuple[str, str], dict[str, Any]],
    datasets: tuple[str, ...] = QUALIFICATION_DATASETS,
    seed: int | str = SEED,
) -> dict[tuple[str, str], str]:
    """Deterministically solve the globally unique, dataset-capped two-cohort match."""
    if len(datasets) < 2 or len(set(datasets)) != len(datasets) or not all(datasets):
        raise ValueError("matcher requires an ordered list of at least two distinct approved datasets")
    if any(source.get("id") != identifier for identifier, source in sources.items()):
        raise ValueError("source map key differs from source queue ID")
    dataset_set = set(datasets)
    unknown_datasets = sorted({
        source.get("source", {}).get("dataset") for source in sources.values()
        if source.get("source", {}).get("dataset") not in dataset_set
    }, key=lambda value: "" if value is None else str(value))
    if unknown_datasets:
        raise ValueError(f"source pool contains unapproved datasets: {unknown_datasets}")
    identities = [source_key(source) for source in sources.values()]
    if len(set(identities)) != len(identities):
        raise ValueError("source pool contains duplicate lineage identities")
    slots = [(role, cell["cell_id"]) for role in ("primary", "reserve") for cell in cells]
    cell_by_id = {cell["cell_id"]: cell for cell in cells}
    if len(cell_by_id) != len(cells):
        raise ValueError("repair cells are duplicated")
    edges: dict[tuple[str, str], list[str]] = {}
    for slot in slots:
        _role, cell_id = slot
        cell = cell_by_id[cell_id]
        candidates: list[tuple[int, str, str]] = []
        for source_id, source in sources.items():
            decision = affinity.get((cell_id, source_id))
            prompt_ok = decision is not None and (
                decision.get("classification_mode") == "full_ontology"
                or decision.get("prompt_sha256") == hashlib.sha256(affinity_prompt(cell, source).encode()).hexdigest()
            )
            if (
                source["lane"] == cell["lane"]
                and source["source"].get("dataset") in dataset_set
                and decision is not None and decision["decision"] == "accept" and prompt_ok
                and decision["source_record_sha256"] == source["source"].get("source_record_sha256")
                and decision["stimulus_sha256"] == hashlib.sha256(source["stimulus"].encode()).hexdigest()
                and decision["output_sha256"] == hashlib.sha256(decision["raw_output"].encode()).hexdigest()
            ):
                candidates.append((decision["selection_rank"], selection_key(cell_id, source_id, seed), source_id))
        edges[slot] = [item[2] for item in sorted(candidates)]
        if len(edges[slot]) < 2:
            raise ValueError(f"{cell_id}: fewer than two affinity-qualified unique sources")

    # The plan permits no dataset to supply more than half of a cohort, with
    # an absolute ceiling of thirty. With two datasets and sixty cells this
    # necessarily retains the frozen exact 30/30 allocation. Additional
    # approved datasets share the same ceiling without acquiring a minimum.
    dataset_ceiling = min(30, len(cells) // 2)
    if dataset_ceiling == 0:
        raise ValueError("dataset balance requires at least two repair cells")
    quota = {
        role: {dataset: dataset_ceiling for dataset in datasets}
        for role in ("primary", "reserve")
    }
    assigned: dict[tuple[str, str], str] = {}
    used_sources: set[str] = set()

    def available(slot: tuple[str, str]) -> list[str]:
        role, _cell_id = slot
        return [
            source_id for source_id in edges[slot]
            if source_id not in used_sources
            and quota[role][sources[source_id]["source"]["dataset"]] > 0
        ]

    def quotas_feasible(unassigned: list[tuple[str, str]]) -> bool:
        for role in ("primary", "reserve"):
            role_slots = [slot for slot in unassigned if slot[0] == role]
            if sum(quota[role].values()) < len(role_slots):
                return False
            for dataset in datasets:
                remaining_capacity = quota[role][dataset]
                if remaining_capacity < 0:
                    return False
                other_capacity = sum(
                    quota[role][other] for other in datasets if other != dataset
                )
                needed = max(0, len(role_slots) - other_capacity)
                candidates = {
                    source_id
                    for slot in role_slots
                    for source_id in edges[slot]
                    if source_id not in used_sources
                    and sources[source_id]["source"]["dataset"] == dataset
                }
                if len(candidates) < needed:
                    return False
                capable_slots = sum(
                    any(
                        source_id not in used_sources
                        and sources[source_id]["source"]["dataset"] == dataset
                        for source_id in edges[slot]
                    )
                    for slot in role_slots
                )
                if capable_slots < needed:
                    return False
        return True

    def solve(unassigned: list[tuple[str, str]]) -> bool:
        if not unassigned:
            return True
        if not quotas_feasible(unassigned):
            return False
        choices = [(len(available(slot)), slot) for slot in unassigned]
        count, slot = min(choices, key=lambda item: (item[0], item[1][1], item[1][0]))
        if count == 0:
            return False
        role, _cell_id = slot
        remainder = [value for value in unassigned if value != slot]
        candidates = available(slot)
        # Scarcer datasets are attempted first; affinity rank/hash remains the
        # stable tie-break because ``edges`` is already deterministically sorted.
        dataset_supply = {
            dataset: len({
                source_id for pending in unassigned for source_id in edges[pending]
                if pending[0] == role and source_id not in used_sources
                and sources[source_id]["source"]["dataset"] == dataset
            })
            for dataset in datasets
        }
        dataset_minimum = {
            dataset: max(0, sum(slot[0] == role for slot in unassigned) - sum(
                quota[role][other] for other in datasets if other != dataset
            ))
            for dataset in datasets
        }
        order = {source_id: position for position, source_id in enumerate(edges[slot])}
        candidates.sort(key=lambda source_id: (
            dataset_supply[sources[source_id]["source"]["dataset"]]
            - dataset_minimum[sources[source_id]["source"]["dataset"]],
            datasets.index(sources[source_id]["source"]["dataset"]),
            order[source_id],
        ))
        for source_id in candidates:
            dataset = sources[source_id]["source"]["dataset"]
            assigned[slot] = source_id
            used_sources.add(source_id)
            quota[role][dataset] -= 1
            if solve(remainder):
                return True
            quota[role][dataset] += 1
            used_sources.remove(source_id)
            del assigned[slot]
        return False

    ordered_slots = sorted(slots, key=lambda value: (len(edges[value]), value[1], value[0]))
    if not solve(ordered_slots):
        if len(datasets) == 2:
            raise ValueError("accepted source graph cannot satisfy global uniqueness and 30/30 cohort quotas")
        raise ValueError("accepted source graph cannot satisfy global uniqueness and per-dataset cohort ceilings")
    return assigned


def build(
    plan_path: Path, source_queue_path: Path, prior_path: Path, v2_paths: list[Path],
    separation_path: Path | list[tuple[Path, Path]], affinity_path: Path,
    approved_datasets: tuple[str, ...] = QUALIFICATION_DATASETS,
    contract_version: str = "v3",
    affinity_summary_path: Path | None = None,
    tooling_readiness_sha256: str | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    spec = contract_spec(contract_version)
    if hashlib.sha256(plan_path.read_bytes()).hexdigest() != spec["plan_sha256"]:
        raise ValueError(f"{contract_version} plan hash mismatch")
    source_bytes = source_queue_path.read_bytes()
    source_rows = read_jsonl(source_queue_path)
    source_ids = [row.get("id") for row in source_rows]
    if (
        any(not isinstance(identifier, str) or not identifier for identifier in source_ids)
        or len(set(source_ids)) != len(source_ids)
    ):
        raise ValueError("source queue contains a malformed or duplicate ID")
    all_sources = {row["id"]: row for row in source_rows}
    bindings = [(separation_path, source_queue_path)] if isinstance(separation_path, Path) else separation_path
    separation_eligibility, separation_manifests = load_separation_bindings(bindings, all_sources)
    eligible_ids = set().union(*separation_eligibility.values())
    excluded = {source_key(row) for row in read_jsonl(prior_path)}
    for path in v2_paths:
        excluded.update(source_key(row) for row in read_jsonl(path))
    sources = {
        row["id"]: row for row in source_rows
        if row.get("lane") in LANES and row.get("task_type") == "repair"
        and row.get("id") in eligible_ids and source_key(row) not in excluded
    }
    affinity_context = None
    allowed_affinity_plans = {spec["plan_sha256"]}
    if contract_version == "v4":
        if not isinstance(tooling_readiness_sha256, str) or len(tooling_readiness_sha256) != 64:
            raise ValueError("V4 requires a validated tooling-readiness report seal")
        if affinity_summary_path is None:
            raise ValueError("V4 requires a sealed affinity aggregate summary")
        allowed_affinity_plans, affinity_context = load_v4_affinity_aggregate_context(
            affinity_summary_path, affinity_path, hashlib.sha256(source_bytes).hexdigest(),
            set(separation_eligibility),
        )
    affinity = load_affinity(
        affinity_path, separation_eligibility, all_sources, plan_sha256=spec["plan_sha256"],
        allowed_plan_sha256s=allowed_affinity_plans,
        candidate_source_ids=set(sources),
    )

    cells = repair_cells()
    slot_source = match_two_slot_sources(
        cells, sources, affinity, approved_datasets, seed=spec["seed"],
    )

    used: set[tuple[str, str, str]] = set()
    counts = {"primary": Counter(), "reserve": Counter()}
    output: list[dict[str, Any]] = []
    for role in ("primary", "reserve"):
        for cell in cells:
            source = sources[slot_source[(role, cell["cell_id"])]]
            decision = affinity[(cell["cell_id"], source["id"])]
            identity = source_key(source)
            if identity in used:
                raise ValueError("affinity assignment reused a source lineage identity")
            used.add(identity)
            counts[role][source["source"]["dataset"]] += 1
            output.append({
                "schema_version": spec["assignment_schema"],
                "contract_id": spec["contract_id"],
                "id": f"{spec['id_prefix']}-{cell['primary_capability']}-{cell['lane']}-repair-{role}",
                "role": role,
                "cohort": "first_pass" if role == "primary" else "reserve",
                "generation_eligible": role == "primary",
                "cell_id": cell["cell_id"],
                "primary_capability": cell["primary_capability"],
                "primary_capability_definition": CAPABILITIES[cell["primary_capability"]],
                "assigned_cross_cutting_dimension": cell["assigned_cross_cutting_dimension"],
                "lane": cell["lane"], "task_type": "repair",
                "source_queue_id": source["id"], "source": source["source"], "stimulus": source["stimulus"],
                "source_affinity_evidence_sha256": decision["evidence_sha256"],
                "source_separation_attestation_sha256": decision["separation_attestation_sha256"],
                "source_affinity_card": {
                    "capability_operation": decision["capability_operation"],
                    "defect_affordance": decision["defect_affordance"],
                },
            })
    if len(output) != 120 or len(used) != 120:
        raise ValueError(f"{contract_version} queue must bind 120 unique sources")
    approved_dataset_set = set(approved_datasets)
    for role in ("primary", "reserve"):
        role_counts = counts[role]
        if (
            sum(role_counts.values()) != 60
            or not set(role_counts).issubset(approved_dataset_set)
            or len(role_counts) < 2
            or any(value > 30 for value in role_counts.values())
        ):
            raise ValueError(f"{role}: dataset diversity contract failed")
    payload = b"".join(canonical_json(row) + b"\n" for row in output)
    manifest: dict[str, Any] = {
        "schema_version": spec["manifest_schema"],
        "status": "sealed-primary-generation-eligible",
        "plan_sha256": spec["plan_sha256"], "seed": spec["seed"],
        "approved_source_datasets": list(approved_datasets),
        "inputs": {
            "source_queue_sha256": hashlib.sha256(source_bytes).hexdigest(),
            "prior_corpus_sha256": hashlib.sha256(prior_path.read_bytes()).hexdigest(),
            "v2_artifact_sha256s": [hashlib.sha256(path.read_bytes()).hexdigest() for path in v2_paths],
            "separation_bindings": separation_manifests,
            "affinity_evidence_sha256": hashlib.sha256(affinity_path.read_bytes()).hexdigest(),
        },
        "assignments": 120, "primary_assignments": 60, "cell_bound_reserves": 60,
        "initial_generation_eligible": 60, "maximum_reserve_generation_eligible": 6,
        "absolute_candidate_budget": 66, "unique_source_identities": 120,
        "dataset_counts": {role: dict(sorted(value.items())) for role, value in counts.items()},
        "evaluation_artifacts_read": 0, "queue_sha256": hashlib.sha256(payload).hexdigest(),
    }
    if contract_version == "v4":
        manifest.update({"contract_version": "v4", "contract_id": spec["contract_id"]})
        manifest["inputs"]["affinity_aggregate"] = affinity_context
        manifest["inputs"]["tooling_readiness_report_sha256"] = tooling_readiness_sha256
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    return output, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--contract-version", choices=("v3", "v4"), default="v3")
    parser.add_argument("--source-queue", type=Path, required=True)
    parser.add_argument("--prior-corpus", type=Path, required=True)
    parser.add_argument("--v2-artifact", type=Path, action="append", required=True)
    separation_group = parser.add_mutually_exclusive_group(required=True)
    separation_group.add_argument(
        "--source-separation", type=Path,
        help="one attestation bound to --source-queue (single-queue form)",
    )
    separation_group.add_argument(
        "--source-separation-binding", type=Path, nargs=2, action="append",
        metavar=("ATTESTATION_JSON", "BOUND_SOURCE_QUEUE_JSONL"),
        help="repeat for ontology evidence bound to multiple source-queue snapshots",
    )
    parser.add_argument("--affinity-evidence", type=Path, required=True)
    parser.add_argument(
        "--affinity-summary", type=Path,
        help="sealed ontology aggregate summary; required by --contract-version v4",
    )
    parser.add_argument(
        "--tooling-readiness-report", type=Path,
        help="passed production-tooling fixture report; required by --contract-version v4",
    )
    parser.add_argument("--admission-config", type=Path, default=DEFAULT_ADMISSION_CONFIG)
    parser.add_argument("--runtimes", type=Path, default=DEFAULT_RUNTIME_CONFIG)
    parser.add_argument("--v4-preflight-config", type=Path, default=DEFAULT_V4_PREFLIGHT_CONFIG)
    parser.add_argument(
        "--tooling-fixtures", type=Path,
        help="explicit fixture bundle used by the report; omit for the deterministic default bundle",
    )
    parser.add_argument(
        "--approved-source-dataset", action="append",
        help="approved source dataset in deterministic preference order; repeat for each dataset",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    tooling_readiness_sha256 = None
    if args.contract_version == "v4":
        from scripts.data.run_v4_tooling_fixtures import validate_tooling_readiness_report
        if args.tooling_readiness_report is None:
            parser.error("--tooling-readiness-report is required by --contract-version v4")
        report = json.loads(args.tooling_readiness_report.read_text(encoding="utf-8"))
        validate_tooling_readiness_report(
            report, args.admission_config, args.runtimes, args.v4_preflight_config,
            args.tooling_fixtures,
        )
        tooling_readiness_sha256 = report["report_sha256"]
    rows, manifest = build(
        args.plan, args.source_queue, args.prior_corpus, args.v2_artifact,
        args.source_separation or [(value[0], value[1]) for value in args.source_separation_binding],
        args.affinity_evidence,
        tuple(args.approved_source_dataset or QUALIFICATION_DATASETS),
        args.contract_version,
        args.affinity_summary,
        tooling_readiness_sha256,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(b"".join(canonical_json(row) + b"\n" for row in rows))
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"assignments": 120, "manifest_sha256": manifest["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
