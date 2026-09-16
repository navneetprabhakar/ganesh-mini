#!/usr/bin/env python3
"""Build the sealed v3 repair-delta primary and cell-bound reserve queue."""

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
AFFINITY_FIELDS = (
    "capability_operation_present", "identifiable_defect_affordance",
    "self_contained_standard_library_feasible", "code_repair_material",
    "forbidden_dependency_absent",
)
QUALIFICATION_DATASETS = (
    "Multilingual-Multimodal-NLP/McEval-Instruct",
    "m-a-p/MdEval-Instruct",
)


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def source_key(row: dict[str, Any]) -> tuple[str, str, str]:
    source = row.get("source") or row.get("lineage") or {}
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


def load_affinity(
    path: Path, separation_sha256: str, sources: dict[str, dict[str, Any]],
) -> dict[tuple[str, str], dict[str, Any]]:
    output: dict[tuple[str, str], dict[str, Any]] = {}
    ontology_sources: set[str] = set()
    for row in read_jsonl(path):
        body = dict(row)
        claimed = body.pop("evidence_sha256", None)
        if row.get("schema_version") == "ganesh-mini-repair-source-ontology/v1":
            source = sources.get(row.get("source_queue_id"))
            batch_ids = row.get("batch_source_queue_ids")
            batch_sources = [sources.get(identifier) for identifier in batch_ids] if isinstance(batch_ids, list) else []
            verdicts = row.get("verdicts")
            raw_prompt = row.get("raw_prompt")
            raw_output = row.get("raw_output")
            if (
                claimed != canonical_sha256(body)
                or row.get("plan_sha256") != PLAN_SHA256
                or row.get("separation_attestation_sha256") != separation_sha256
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
                    "classification_mode": "full_ontology",
                }
            if seen != set(CAPABILITIES):
                raise ValueError("source-ontology verdicts do not cover the frozen ontology")
            ontology_sources.add(source["id"])
            continue
        if (
            claimed != canonical_sha256(body)
            or row.get("schema_version") != "ganesh-mini-repair-source-affinity/v1"
            or row.get("separation_attestation_sha256") != separation_sha256
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
    visible = [{
        "source_queue_id": row["id"], "lane": row["lane"], "task_type": row["task_type"],
        "stimulus": row["stimulus"],
        "source_lineage": {key: row["source"].get(key) for key in (
            "dataset", "revision", "record_id", "source_record_sha256",
        )},
    } for row in sources]
    return f"""Classify each training-only repair stimulus independently against every capability. Do not use tools or inspect files.
Capability ontology: {json.dumps(CAPABILITIES, separators=(',', ':'), sort_keys=True)}
Inputs: {json.dumps(visible, separators=(',', ':'), ensure_ascii=False)}

For every input return exactly one verdict for every ontology capability. Multiple capabilities may pass. Accept a
capability only when the stimulus contains that capability-specific operation plus an identifiable defect affordance,
can become one self-contained standard-library-only source file, is actual code-repair material, and requires no
filesystem, network, clock, randomness, installation, external dependency, framework, or service. For a rejection,
set each boolean independently and explain the actual operation and defect affordance (or their absence). Do not force
the source into a capability. Return only the fixed structured contract. Evaluation separation is handled elsewhere."""


def selection_key(cell_id: str, source_id: str) -> str:
    return hashlib.sha256(f"{SEED}\0{cell_id}\0{source_id}".encode()).hexdigest()


def match_two_slot_sources(
    cells: list[dict[str, Any]],
    sources: dict[str, dict[str, Any]],
    affinity: dict[tuple[str, str], dict[str, Any]],
    datasets: tuple[str, str] = QUALIFICATION_DATASETS,
) -> dict[tuple[str, str], str]:
    """Deterministically solve the globally unique, dataset-balanced two-cohort match."""
    if len(datasets) != 2 or len(set(datasets)) != 2 or not all(datasets):
        raise ValueError("matcher requires exactly two distinct qualification datasets")
    if any(source.get("id") != identifier for identifier, source in sources.items()):
        raise ValueError("source map key differs from source queue ID")
    identities = [source_key(source) for source in sources.values()]
    if len(set(identities)) != len(identities):
        raise ValueError("source pool contains duplicate lineage identities")
    slots = [(role, cell["cell_id"]) for role in ("primary", "reserve") for cell in cells]
    cell_by_id = {cell["cell_id"]: cell for cell in cells}
    if len(cell_by_id) != len(cells):
        raise ValueError("repair cells are duplicated")
    dataset_set = set(datasets)
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
                candidates.append((decision["selection_rank"], selection_key(cell_id, source_id), source_id))
        edges[slot] = [item[2] for item in sorted(candidates)]
        if len(edges[slot]) < 2:
            raise ValueError(f"{cell_id}: fewer than two affinity-qualified unique sources")

    # With sixty slots in each cohort and a per-dataset ceiling of thirty,
    # both datasets must contribute exactly thirty sources to each cohort.
    quota = {role: {dataset: len(cells) // 2 for dataset in datasets} for role in ("primary", "reserve")}
    if len(cells) % 2:
        raise ValueError("dataset balance requires an even number of repair cells")
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
            for dataset in datasets:
                needed = quota[role][dataset]
                if needed < 0 or needed > len(role_slots):
                    return False
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
            return all(quota[role][dataset] == 0 for role in quota for dataset in datasets)
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
        order = {source_id: position for position, source_id in enumerate(edges[slot])}
        candidates.sort(key=lambda source_id: (
            dataset_supply[sources[source_id]["source"]["dataset"]]
            - quota[role][sources[source_id]["source"]["dataset"]],
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
        raise ValueError("accepted source graph cannot satisfy global uniqueness and 30/30 cohort quotas")
    return assigned


def build(
    plan_path: Path, source_queue_path: Path, prior_path: Path, v2_paths: list[Path],
    separation_path: Path, affinity_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if hashlib.sha256(plan_path.read_bytes()).hexdigest() != PLAN_SHA256:
        raise ValueError("v3 plan hash mismatch")
    source_bytes = source_queue_path.read_bytes()
    separation = load_separation(separation_path, hashlib.sha256(source_bytes).hexdigest())
    eligible_ids = set(separation["eligible_source_queue_ids"])
    excluded = {source_key(row) for row in read_jsonl(prior_path)}
    for path in v2_paths:
        excluded.update(source_key(row) for row in read_jsonl(path))
    source_rows = read_jsonl(source_queue_path)
    if len({row.get("id") for row in source_rows}) != len(source_rows):
        raise ValueError("source queue IDs are duplicated")
    sources = {
        row["id"]: row for row in source_rows
        if row.get("lane") in LANES and row.get("task_type") == "repair"
        and row.get("id") in eligible_ids and source_key(row) not in excluded
    }
    affinity = load_affinity(affinity_path, separation["attestation_sha256"], sources)

    cells = repair_cells()
    slot_source = match_two_slot_sources(cells, sources, affinity)

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
                "schema_version": "ganesh-mini-repair-delta-assignment/v1",
                "contract_id": CONTRACT_ID,
                "id": f"cap-v3-{cell['primary_capability']}-{cell['lane']}-repair-{role}",
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
                "source_affinity_card": {
                    "capability_operation": decision["capability_operation"],
                    "defect_affordance": decision["defect_affordance"],
                },
            })
    if len(output) != 120 or len(used) != 120:
        raise ValueError("v3 queue must bind 120 unique sources")
    for role in ("primary", "reserve"):
        role_counts = counts[role]
        if set(role_counts) != set(QUALIFICATION_DATASETS) or set(role_counts.values()) != {30}:
            raise ValueError(f"{role}: dataset diversity contract failed")
    payload = b"".join(canonical_json(row) + b"\n" for row in output)
    manifest: dict[str, Any] = {
        "schema_version": "ganesh-mini-repair-delta-queue-manifest/v1",
        "status": "sealed-primary-generation-eligible",
        "plan_sha256": PLAN_SHA256, "seed": SEED,
        "inputs": {
            "source_queue_sha256": hashlib.sha256(source_bytes).hexdigest(),
            "prior_corpus_sha256": hashlib.sha256(prior_path.read_bytes()).hexdigest(),
            "v2_artifact_sha256s": [hashlib.sha256(path.read_bytes()).hexdigest() for path in v2_paths],
            "separation_attestation_sha256": separation["attestation_sha256"],
            "affinity_evidence_sha256": hashlib.sha256(affinity_path.read_bytes()).hexdigest(),
        },
        "assignments": 120, "primary_assignments": 60, "cell_bound_reserves": 60,
        "initial_generation_eligible": 60, "maximum_reserve_generation_eligible": 6,
        "absolute_candidate_budget": 66, "unique_source_identities": 120,
        "dataset_counts": {role: dict(sorted(value.items())) for role, value in counts.items()},
        "evaluation_artifacts_read": 0, "queue_sha256": hashlib.sha256(payload).hexdigest(),
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    return output, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--source-queue", type=Path, required=True)
    parser.add_argument("--prior-corpus", type=Path, required=True)
    parser.add_argument("--v2-artifact", type=Path, action="append", required=True)
    parser.add_argument("--source-separation", type=Path, required=True)
    parser.add_argument("--affinity-evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    rows, manifest = build(
        args.plan, args.source_queue, args.prior_corpus, args.v2_artifact,
        args.source_separation, args.affinity_evidence,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(b"".join(canonical_json(row) + b"\n" for row in rows))
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"assignments": 120, "manifest_sha256": manifest["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
