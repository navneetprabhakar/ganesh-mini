#!/usr/bin/env python3
"""Build the sealed, content-blind Gate 2 v4 native CommitPackFT tranche."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from scripts.data.build_commitpackft_repair_extension import LICENSES, bounded, canonical_json


PLAN_SHA256 = "79849d2f8b70ba69572b4c3fa1761bdb413562c6f6d9a12537d93a1724812ef6"
CONFIG_SCHEMA = "ganesh-mini-gate2-v4-commitpackft-native-source-config/v1"
POLICY_SCHEMA = "ganesh-mini-gate2-v4-commitpackft-native-source-policy/v1"
ROW_SCHEMA = "ganesh-mini-gate2-v4-repair-source/v1"
MANIFEST_SCHEMA = "ganesh-mini-gate2-v4-commitpackft-source-extension-manifest/v1"
LANES = ("go", "python", "rust")
LANGUAGE_LABELS = {"go": "Go", "python": "Python", "rust": "Rust"}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def valid_sha256(value: Any) -> bool:
    return (
        isinstance(value, str) and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def validate_config(path: Path) -> dict[str, Any]:
    config = json.loads(path.read_text(encoding="utf-8"))
    files = config.get("files")
    if (
        config.get("schema_version") != CONFIG_SCHEMA
        or config.get("dataset") != "bigcode/commitpackft"
        or config.get("revision") != "fc56fe33c030c6daa414c2b112c932b8eed085e6"
        or config.get("allowed_record_licenses") != list(LICENSES)
        or not valid_sha256(config.get("revision_tree_cache_sha256"))
        or not isinstance(config.get("uri"), str) or not config["uri"]
        or not isinstance(files, dict) or set(files) != set(LANES)
    ):
        raise ValueError("v4 CommitPackFT source config is invalid")
    for lane, metadata in files.items():
        if (
            not isinstance(metadata, dict)
            or set(metadata) != {"filename", "bytes", "sha256"}
            or metadata.get("filename") != f"data/{lane}/data.jsonl"
            or type(metadata.get("bytes")) is not int or metadata["bytes"] <= 0
            or not valid_sha256(metadata.get("sha256"))
        ):
            raise ValueError(f"v4 CommitPackFT {lane} source binding is invalid")
    return config


def validate_policy(path: Path, config_path: Path) -> dict[str, Any]:
    policy = json.loads(path.read_text(encoding="utf-8"))
    body = dict(policy)
    seal = body.pop("policy_sha256", None)
    expected_selection = {
        "ordering": (
            "sha256(seed\\0lane\\0dataset\\0revision\\0source_file\\0record_id"
            "\\0quarantined_record_sha256)"
        ),
        "content_blind": True,
        "capability_keywords_used": False,
        "capability_outcomes_used": False,
        "evaluation_content_read": False,
        "adaptive_top_up_allowed": False,
    }
    expected_new_contents = {
        "included_in_stimulus": False,
        "included_in_ordering": False,
        "included_in_output": False,
        "permitted_uses": ["complete_source_record_hash", "prohibited_marker_safety_filter"],
    }
    limits = policy.get("stimulus_limits")
    exclusions = policy.get("exclusion_bindings")
    if (
        seal != sha256_bytes(canonical_json(body))
        or policy.get("schema_version") != POLICY_SCHEMA
        or policy.get("status") != "sealed-inactive-source-extension"
        or policy.get("plan_sha256") != PLAN_SHA256
        or policy.get("source_config_sha256") != file_sha256(config_path)
        or policy.get("selection_seed") != "ganesh-mini-gate2-v4-native-commitpackft-repair-source-v1"
        or policy.get("lanes") != list(LANES)
        or policy.get("records_per_lane") != 1000
        or policy.get("selection_contract") != expected_selection
        or not isinstance(limits, dict)
        or any(type(limits.get(key)) is not int or limits[key] <= 0 for key in (
            "subject_chars", "message_chars", "old_contents_chars"
        ))
        or not isinstance(policy.get("prohibited_markers"), list)
        or not policy["prohibited_markers"]
        or policy.get("new_contents_policy") != expected_new_contents
        or not isinstance(exclusions, dict)
        or not valid_sha256(exclusions.get("prior_corpus_sha256"))
        or not isinstance(exclusions.get("v2_artifact_sha256s"), list)
        or not exclusions["v2_artifact_sha256s"]
        or not all(valid_sha256(value) for value in exclusions["v2_artifact_sha256s"])
        or not valid_sha256(exclusions.get("v3_queue_sha256"))
        or exclusions.get("v3_queue_lineages") != 120
        or policy.get("classification_launched") is not False
    ):
        raise ValueError("v4 CommitPackFT source policy is invalid or unsealed")
    return policy


def walk(value: Any) -> Iterable[Any]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def read_structured(path: Path) -> Any:
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return json.loads(path.read_text(encoding="utf-8"))


def source_identity(value: Any) -> tuple[str, str, str, str] | None:
    if not isinstance(value, dict):
        return None
    fields = tuple(value.get(key) for key in (
        "dataset", "revision", "record_id", "source_record_sha256",
    ))
    if all(isinstance(item, str) and item for item in fields):
        return fields  # type: ignore[return-value]
    return None


def identities(path: Path) -> set[tuple[str, str, str, str]]:
    return {identity for node in walk(read_structured(path)) if (identity := source_identity(node))}


def stable_order(
    policy: dict[str, Any], config: dict[str, Any], lane: str, source_file: str,
    record_id: str, quarantined_record_sha256: str,
) -> str:
    return sha256_bytes("\0".join((
        policy["selection_seed"], lane, config["dataset"], config["revision"],
        source_file, record_id, quarantined_record_sha256,
    )).encode())


def prohibited(row: dict[str, Any], markers: list[str]) -> bool:
    # new_contents is visible only to this fail-closed safety predicate.
    folded = " ".join(json.dumps(row, ensure_ascii=False).casefold().split())
    return any(marker.casefold() in folded for marker in markers)


def stimulus(row: dict[str, Any], lane: str, limits: dict[str, int]) -> str:
    return (
        f"Commit subject:\n{bounded(row['subject'], limits['subject_chars'])}\n\n"
        f"Commit message:\n{bounded(row['message'], limits['message_chars'])}\n\n"
        f"Known-bad {LANGUAGE_LABELS[lane]} source:\n"
        f"{bounded(row['old_contents'], limits['old_contents_chars'])}"
    )


def load_lane(
    path: Path, lane: str, config: dict[str, Any], policy: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    metadata = config["files"][lane]
    if path.stat().st_size != metadata["bytes"] or file_sha256(path) != metadata["sha256"]:
        raise ValueError(f"{lane} CommitPackFT payload differs from its exact pinned binding")
    required = (
        "commit", "old_file", "new_file", "old_contents", "new_contents",
        "subject", "message", "repos",
    )
    rejected: Counter[str] = Counter()
    eligible: list[dict[str, Any]] = []
    with path.open("rb") as handle:
        for line_number, raw_with_newline in enumerate(handle, 1):
            raw = raw_with_newline.rstrip(b"\r\n")
            if not raw:
                rejected["empty_line"] += 1
                continue
            try:
                row = json.loads(raw)
            except (UnicodeDecodeError, json.JSONDecodeError):
                rejected["malformed_json"] += 1
                continue
            if not isinstance(row, dict) or any(not isinstance(row.get(key), str) for key in required):
                rejected["malformed_record"] += 1
                continue
            if row.get("lang") != LANGUAGE_LABELS[lane]:
                rejected["language_mismatch"] += 1
                continue
            license_key = row.get("license")
            if license_key not in LICENSES:
                rejected["license_not_allowlisted"] += 1
                continue
            if not all(row[key].strip() for key in (
                "commit", "old_file", "new_file", "subject", "message", "repos",
            )):
                rejected["incomplete_lineage_or_prompt"] += 1
                continue
            if not row["old_contents"].strip():
                rejected["empty_old_contents"] += 1
                continue
            if prohibited(row, policy["prohibited_markers"]):
                rejected["prohibited_marker"] += 1
                continue
            repositories = [item.strip() for item in row["repos"].split(",") if item.strip()]
            if not repositories:
                rejected["incomplete_lineage_or_prompt"] += 1
                continue
            record_id = f"{metadata['filename']}:line-{line_number:08d}"
            source_record_sha256 = sha256_bytes(canonical_json(row))
            ordering_row = {key: value for key, value in row.items() if key != "new_contents"}
            quarantined_record_sha256 = sha256_bytes(canonical_json(ordering_row))
            spdx, license_uri = LICENSES[license_key]
            item = {
                "lane": lane, "record_id": record_id, "source_file": metadata["filename"],
                "source_file_sha256": metadata["sha256"], "source_file_bytes": metadata["bytes"],
                "raw_line_sha256": sha256_bytes(raw), "source_record_sha256": source_record_sha256,
                "quarantined_record_sha256": quarantined_record_sha256,
                "commit": row["commit"], "old_file": row["old_file"], "new_file": row["new_file"],
                "repositories_raw": row["repos"], "repositories": repositories,
                "license": spdx, "license_uri": license_uri,
                "subject_sha256": sha256_bytes(row["subject"].encode()),
                "message_sha256": sha256_bytes(row["message"].encode()),
                "old_contents_sha256": sha256_bytes(row["old_contents"].encode()),
                "stimulus": stimulus(row, lane, policy["stimulus_limits"]),
            }
            item["selection_key"] = stable_order(
                policy, config, lane, metadata["filename"], record_id, quarantined_record_sha256,
            )
            eligible.append(item)
    eligible.sort(key=lambda item: (item["selection_key"], item["record_id"]))
    return eligible, dict(sorted(rejected.items()))


def queue_row(
    item: dict[str, Any], rank: int, config: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": ROW_SCHEMA,
        "id": f"gate2-v4-commitpackft-{item['lane']}-repair-{rank:04d}",
        "lane": item["lane"], "task_type": "repair", "stimulus": item["stimulus"],
        "source": {
            "dataset": config["dataset"], "uri": config["uri"], "revision": config["revision"],
            "record_id": item["record_id"], "license": item["license"],
            "license_uri": item["license_uri"], "source_record_sha256": item["source_record_sha256"],
            "source_file": item["source_file"], "source_file_sha256": item["source_file_sha256"],
            "source_file_bytes": item["source_file_bytes"], "raw_line_sha256": item["raw_line_sha256"],
            "quarantined_record_sha256": item["quarantined_record_sha256"],
            "commit": item["commit"], "old_file": item["old_file"], "new_file": item["new_file"],
            "repositories_raw": item["repositories_raw"], "repositories": item["repositories"],
            "subject_sha256": item["subject_sha256"], "message_sha256": item["message_sha256"],
            "old_contents_sha256": item["old_contents_sha256"], "selection_rank": rank,
            "transformation": (
                "Native CommitPackFT repair stimulus from bounded commit subject, message, and old_contents; "
                "new_contents is quarantined and is not an answer, ordering input, prompt input, or output field"
            ),
        },
    }


def build(
    config_path: Path, policy_path: Path, lane_paths: dict[str, Path], prior_path: Path,
    v2_paths: list[Path], v3_queue_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    config = validate_config(config_path)
    policy = validate_policy(policy_path, config_path)
    bindings = policy["exclusion_bindings"]
    if file_sha256(prior_path) != bindings["prior_corpus_sha256"]:
        raise ValueError("prior corpus differs from the sealed exclusion binding")
    if [file_sha256(path) for path in v2_paths] != bindings["v2_artifact_sha256s"]:
        raise ValueError("v2 artifact list differs from the sealed exclusion binding")
    if file_sha256(v3_queue_path) != bindings["v3_queue_sha256"]:
        raise ValueError("v3 queue differs from the sealed exclusion binding")
    prior = identities(prior_path)
    v2 = set().union(*(identities(path) for path in v2_paths))
    v3 = identities(v3_queue_path)
    if len(v3) != bindings["v3_queue_lineages"]:
        raise ValueError("v3 queue does not contain the sealed 120 unique source lineages")
    excluded = prior | v2 | v3

    output: list[dict[str, Any]] = []
    lane_manifest: dict[str, Any] = {}
    for lane in LANES:
        inventory, rejected = load_lane(lane_paths[lane], lane, config, policy)
        projection = [
            {key: item[key] for key in (
                "record_id", "selection_key", "source_record_sha256", "raw_line_sha256", "license",
            )}
            for item in inventory
        ]
        fresh = [item for item in inventory if (
            config["dataset"], config["revision"], item["record_id"], item["source_record_sha256"]
        ) not in excluded]
        fresh_projection = [
            {key: item[key] for key in (
                "record_id", "selection_key", "source_record_sha256", "raw_line_sha256", "license",
            )}
            for item in fresh
        ]
        if len(fresh) < policy["records_per_lane"]:
            raise ValueError(f"{lane}: fewer than 1,000 fresh eligible records")
        selected = fresh[:policy["records_per_lane"]]
        output.extend(queue_row(item, rank, config) for rank, item in enumerate(selected, 1))
        lane_manifest[lane] = {
            "source_file": str(lane_paths[lane]),
            "physical_records": sum(1 for line in lane_paths[lane].open("rb") if line.strip()),
            "permissive_eligible_inventory_records": len(inventory),
            "permissive_eligible_inventory_sha256": sha256_bytes(canonical_json(projection)),
            "excluded_lineages": len(inventory) - len(fresh),
            "fresh_eligible_inventory_records": len(fresh),
            "fresh_eligible_inventory_sha256": sha256_bytes(canonical_json(fresh_projection)),
            "selected_records": len(selected),
            "selected_identity_sha256": sha256_bytes(canonical_json(fresh_projection[:1000])),
            "rejections": rejected,
            "eligible_license_counts": dict(sorted(Counter(item["license"] for item in inventory).items())),
            "selected_license_counts": dict(sorted(Counter(item["license"] for item in selected).items())),
        }
    source_ids = [row["id"] for row in output]
    source_lineages = [source_identity(row["source"]) for row in output]
    if (
        len(output) != 3000 or len(set(source_ids)) != 3000
        or None in source_lineages or len(set(source_lineages)) != 3000
        or set(source_lineages) & excluded
    ):
        raise ValueError("v4 source extension is not 3,000 fresh unique lineages")
    payload = b"".join(canonical_json(row) + b"\n" for row in output)
    manifest: dict[str, Any] = {
        "schema_version": MANIFEST_SCHEMA, "status": "sealed-inactive-source-extension",
        "plan_sha256": PLAN_SHA256,
        "inputs": {
            "config": {"path": str(config_path), "sha256": file_sha256(config_path)},
            "policy": {"path": str(policy_path), "sha256": file_sha256(policy_path),
                       "policy_sha256": policy["policy_sha256"]},
            "prior_corpus": {"path": str(prior_path), "sha256": file_sha256(prior_path)},
            "v2_artifacts": [{"path": str(path), "sha256": file_sha256(path)} for path in v2_paths],
            "v3_queue": {"path": str(v3_queue_path), "sha256": file_sha256(v3_queue_path)},
        },
        "exclusions": {
            "prior_lineages": len(prior), "v2_lineages": len(v2), "v3_lineages": len(v3),
            "union_lineages": len(excluded),
            "union_identity_sha256": sha256_bytes(canonical_json(sorted(excluded))),
        },
        "selection_contract": policy["selection_contract"], "lanes": lane_manifest,
        "extension": {"records": len(output), "bytes": len(payload), "sha256": sha256_bytes(payload)},
        "classification_launched": False, "gcloud_used": False,
    }
    manifest["manifest_sha256"] = sha256_bytes(canonical_json(manifest))
    return output, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--go-source", type=Path, required=True)
    parser.add_argument("--python-source", type=Path, required=True)
    parser.add_argument("--rust-source", type=Path, required=True)
    parser.add_argument("--prior-corpus", type=Path, required=True)
    parser.add_argument("--v2-artifact", type=Path, action="append", required=True)
    parser.add_argument("--v3-queue", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    rows, manifest = build(
        args.config, args.policy,
        {"go": args.go_source, "python": args.python_source, "rust": args.rust_source},
        args.prior_corpus, args.v2_artifact, args.v3_queue,
    )
    payload = b"".join(canonical_json(row) + b"\n" for row in rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": manifest["status"], "records": len(rows),
        "extension_sha256": manifest["extension"]["sha256"],
        "manifest_sha256": manifest["manifest_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
