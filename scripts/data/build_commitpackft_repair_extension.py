#!/usr/bin/env python3
"""Build a sealed, content-blind CommitPackFT repair-source contingency pool."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


POLICY_SCHEMA = "ganesh-mini-gate2-commitpackft-source-policy/v1"
TAIL_POLICY_SCHEMA = "ganesh-mini-gate2-commitpackft-terminal-tail-policy/v1"
ROW_SCHEMA = "ganesh-mini-commitpackft-repair-source/v1"
MANIFEST_SCHEMA = "ganesh-mini-commitpackft-repair-extension-manifest/v1"
PARENT_PLAN_SHA256 = "4023a896300112f9f93f2a16698d549f203e3e75b4e71ae054f3a98463e2f0f0"
LICENSES = {
    "mit": ("MIT", "https://opensource.org/license/mit/"),
    "apache-2.0": ("Apache-2.0", "https://www.apache.org/licenses/LICENSE-2.0"),
    "bsd-2-clause": ("BSD-2-Clause", "https://opensource.org/license/bsd-2-clause/"),
    "bsd-3-clause": ("BSD-3-Clause", "https://opensource.org/license/bsd-3-clause/"),
    "isc": ("ISC", "https://opensource.org/license/isc-license-txt/"),
    "cc0-1.0": ("CC0-1.0", "https://creativecommons.org/publicdomain/zero/1.0/"),
    "unlicense": ("Unlicense", "https://unlicense.org/"),
}
LANGUAGE_LABELS = {"javascript": "JavaScript", "typescript": "TypeScript"}


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


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


def evidence_files(paths: list[Path]) -> list[Path]:
    files: set[Path] = set()
    for path in paths:
        if path.is_dir():
            files.update(item for item in path.rglob("*") if item.suffix in {".json", ".jsonl"})
        elif path.suffix in {".json", ".jsonl"}:
            files.add(path)
        else:
            raise ValueError(f"unsupported evidence path: {path}")
    return sorted(files, key=str)


def source_identity(value: Any) -> tuple[str, str, str] | None:
    if not isinstance(value, dict):
        return None
    fields = tuple(value.get(key) for key in ("dataset", "revision", "record_id"))
    if all(isinstance(item, str) and item for item in fields):
        return fields  # type: ignore[return-value]
    return None


def collect_exclusions(paths: list[Path]) -> tuple[set[tuple[str, str, str]], list[dict[str, Any]]]:
    identities: set[tuple[str, str, str]] = set()
    inventory: list[dict[str, Any]] = []
    for path in evidence_files(paths):
        inventory.append({"path": str(path), "bytes": path.stat().st_size, "sha256": file_sha256(path)})
        for node in walk(read_structured(path)):
            identity = source_identity(node)
            if identity is not None:
                identities.add(identity)
    return identities, inventory


def validate_policy(policy_path: Path, addendum_path: Path) -> dict[str, Any]:
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    body = dict(policy)
    claimed = body.pop("policy_sha256", None)
    source = policy.get("source")
    new_contents = policy.get("new_contents_policy")
    limits = policy.get("stimulus_limits")
    cohort = policy.get("cohort_policy")
    common_invalid = (
        claimed != sha256_bytes(canonical_json(body))
        or policy.get("parent_plan_sha256") != PARENT_PLAN_SHA256
        or policy.get("source_addendum_sha256") != file_sha256(addendum_path)
        or not isinstance(policy.get("selection_seed"), str) or not policy["selection_seed"]
        or not isinstance(source, dict) or source.get("dataset") != "bigcode/commitpackft"
        or source.get("revision") != "fc56fe33c030c6daa414c2b112c932b8eed085e6"
        or source.get("allowed_record_licenses") != list(LICENSES)
        or not isinstance(source.get("files"), dict)
        or not isinstance(limits, dict)
        or any(type(limits.get(key)) is not int or limits[key] <= 0 for key in (
            "subject_chars", "message_chars", "old_contents_chars"
        ))
        or cohort != {"minimum_distinct_datasets": 2, "maximum_per_dataset_per_cohort": 30}
        or new_contents != {
            "included_in_stimulus": False,
            "included_in_ordering": False,
            "included_in_output": False,
            "permitted_uses": ["complete_source_record_hash", "prohibited_marker_safety_filter"],
        }
        or not isinstance(policy.get("prohibited_markers"), list)
        or not policy["prohibited_markers"]
    )
    schema = policy.get("schema_version")
    if schema == POLICY_SCHEMA:
        schema_invalid = (
            policy.get("status") != "sealed-inactive-contingency"
            or policy.get("activation_condition") != "v8-terminal-global-120-source-match-infeasible"
            or type(policy.get("records_per_lane")) is not int or policy["records_per_lane"] != 1000
        )
    elif schema == TAIL_POLICY_SCHEMA:
        selection = policy.get("rank_selection")
        shards = policy.get("classification_shards")
        bindings = policy.get("terminal_bindings")
        expected_inventory_sha256 = selection.get("expected_inventory_ordered_identity_sha256") \
            if isinstance(selection, dict) else None
        selection_core = {key: selection.get(key) for key in (
            "lane", "zero_based_start", "count", "one_based_first_rank",
            "one_based_last_rank", "expected_inventory_records",
        )} if isinstance(selection, dict) else None
        schema_invalid = (
            policy.get("status") != "sealed-inactive-terminal-tail"
            or policy.get("activation_condition") != "v9-terminal-global-120-source-match-infeasible"
            or selection_core != {
                "lane": "typescript", "zero_based_start": 1000, "count": 3990,
                "one_based_first_rank": 1001, "one_based_last_rank": 4990,
                "expected_inventory_records": 4990,
            }
            or not isinstance(expected_inventory_sha256, str)
            or len(expected_inventory_sha256) != 64
            or any(character not in "0123456789abcdef" for character in expected_inventory_sha256)
            or shards != [
                {"shard": 1, "classifier_tail_offset": 0, "count": 998},
                {"shard": 2, "classifier_tail_offset": 998, "count": 998},
                {"shard": 3, "classifier_tail_offset": 1996, "count": 998},
                {"shard": 4, "classifier_tail_offset": 2994, "count": 996},
            ]
            or bindings != {
                "prior_addendum_sha256": "5d1301d7e277f6ea977e6ccc6740a33f877ed0d20cc4a535098b8947c2788049",
                "prior_policy_file_sha256": "7ab381b7a2be66b175a5833450b77489d8b7e91a9feeab54a170fa23e1e4dbb7",
                "prior_policy_sha256": "d17aa531b9ad1d95b186e544ecf6f68cf2626c79a56fb0ce587a0d2f5d686028",
                "v9_aggregate_file_sha256": "a3f27f9666c1f07f617c812fe816d811323adc26eccad3b0b7a55a26779cb295",
                "v9_aggregate_sha256": "6f1251d3e7db2c09f315b74784f550620fb6fb31f47a35b0ce8570cecf7b7614",
                "v9_queue_failure_file_sha256": "0b1aee312b2ebffbb04e2724e9b70d52748987db9fedf952ade4ebafa345e354",
                "v9_queue_failure_sha256": "0505bbdf7893e5458fe6c0ca65aca8be992262212a5089c120966dab84d6d47b",
            }
            or policy.get("full_ontology_required") is not True
            or policy.get("all_shards_must_finish") is not True
            or policy.get("early_stop_allowed") is not False
            or policy.get("content_retries_allowed") is not False
            or policy.get("further_v3_source_expansion_allowed") is not False
        )
    else:
        schema_invalid = True
    if common_invalid or schema_invalid:
        raise ValueError("CommitPackFT source policy is invalid or unsealed")
    return policy


def rank_selection(policy: dict[str, Any]) -> list[tuple[str, int, int]]:
    """Return lane, zero-based start, count while preserving the v1 behavior."""
    if policy["schema_version"] == POLICY_SCHEMA:
        return [(lane, 0, policy["records_per_lane"]) for lane in ("javascript", "typescript")]
    selection = policy["rank_selection"]
    return [(selection["lane"], selection["zero_based_start"], selection["count"])]


def bounded(value: str, maximum: int) -> str:
    value = value.strip()
    if len(value) <= maximum:
        return value
    boundary = value.rfind("\n", 0, maximum)
    cutoff = boundary if boundary >= maximum // 2 else maximum
    return value[:cutoff].rstrip() + "\n[truncated at sealed CommitPackFT boundary]"


def prohibited(row: dict[str, Any], markers: list[str]) -> bool:
    # new_contents is inspected only inside this fail-closed safety predicate.
    folded = " ".join(json.dumps(row, ensure_ascii=False).casefold().split())
    return any(marker.casefold() in folded for marker in markers)


def stable_order(policy: dict[str, Any], source_file: str, record_id: str) -> str:
    source = policy["source"]
    parts = (policy["selection_seed"], source["dataset"], source["revision"], source_file, record_id)
    return sha256_bytes("\0".join(parts).encode())


def stimulus(row: dict[str, Any], lane: str, limits: dict[str, int]) -> str:
    subject = bounded(row["subject"], limits["subject_chars"])
    message = bounded(row["message"], limits["message_chars"])
    old_contents = bounded(row["old_contents"], limits["old_contents_chars"])
    return (
        f"Commit subject:\n{subject}\n\nCommit message:\n{message}\n\n"
        f"Known-bad {LANGUAGE_LABELS[lane]} source:\n{old_contents}"
    )


def load_lane(
    path: Path, lane: str, policy: dict[str, Any], exclusions: set[tuple[str, str, str]],
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    metadata = policy["source"]["files"].get(lane)
    if not isinstance(metadata, dict):
        raise ValueError(f"policy has no pinned {lane} file")
    observed_bytes = path.stat().st_size
    observed_sha256 = file_sha256(path)
    if observed_bytes != metadata.get("bytes") or observed_sha256 != metadata.get("sha256"):
        raise ValueError(f"{lane} CommitPackFT snapshot hash or byte size drifted")
    reasons: Counter[str] = Counter()
    eligible: list[dict[str, Any]] = []
    required = ("commit", "old_file", "new_file", "old_contents", "new_contents", "subject", "message", "repos")
    with path.open("rb") as handle:
        for line_number, raw_with_newline in enumerate(handle, 1):
            raw = raw_with_newline.rstrip(b"\r\n")
            if not raw:
                reasons["empty_line"] += 1
                continue
            try:
                row = json.loads(raw)
            except (UnicodeDecodeError, json.JSONDecodeError):
                reasons["malformed_json"] += 1
                continue
            if not isinstance(row, dict) or any(not isinstance(row.get(key), str) for key in required):
                reasons["malformed_record"] += 1
                continue
            if row.get("lang") != LANGUAGE_LABELS[lane]:
                reasons["language_mismatch"] += 1
                continue
            license_key = row.get("license")
            if license_key not in LICENSES:
                reasons["license_not_allowlisted"] += 1
                continue
            if not all(row[key].strip() for key in ("commit", "old_file", "new_file", "subject", "message", "repos")):
                reasons["incomplete_lineage_or_prompt"] += 1
                continue
            if not row["old_contents"].strip():
                reasons["empty_old_contents"] += 1
                continue
            if prohibited(row, policy["prohibited_markers"]):
                reasons["prohibited_marker"] += 1
                continue
            record_id = f"{metadata['filename']}:line-{line_number:08d}"
            identity = (policy["source"]["dataset"], policy["source"]["revision"], record_id)
            if identity in exclusions:
                reasons["prior_lineage"] += 1
                continue
            repositories = [item.strip() for item in row["repos"].split(",") if item.strip()]
            if not repositories:
                reasons["incomplete_lineage_or_prompt"] += 1
                continue
            spdx, license_uri = LICENSES[license_key]
            item = {
                "lane": lane,
                "record_id": record_id,
                "source_file": metadata["filename"],
                "source_file_sha256": metadata["sha256"],
                "source_file_bytes": metadata["bytes"],
                "raw_line_sha256": sha256_bytes(raw),
                "source_record_sha256": sha256_bytes(canonical_json(row)),
                "commit": row["commit"],
                "old_file": row["old_file"],
                "new_file": row["new_file"],
                "repositories_raw": row["repos"],
                "repositories": repositories,
                "license": spdx,
                "license_uri": license_uri,
                "subject_sha256": sha256_bytes(row["subject"].encode()),
                "message_sha256": sha256_bytes(row["message"].encode()),
                "old_contents_sha256": sha256_bytes(row["old_contents"].encode()),
                "stimulus": stimulus(row, lane, policy["stimulus_limits"]),
            }
            item["selection_key"] = stable_order(policy, item["source_file"], record_id)
            eligible.append(item)
    eligible.sort(key=lambda item: (item["selection_key"], item["record_id"]))
    return eligible, dict(sorted(reasons.items()))


def queue_row(item: dict[str, Any], ordinal: int, policy: dict[str, Any]) -> dict[str, Any]:
    source = policy["source"]
    return {
        "schema_version": ROW_SCHEMA,
        "id": f"gate2-v3-commitpackft-{item['lane']}-repair-{ordinal:04d}",
        "lane": item["lane"],
        "task_type": "repair",
        "stimulus": item["stimulus"],
        "source": {
            "dataset": source["dataset"], "uri": source["uri"], "revision": source["revision"],
            "record_id": item["record_id"], "license": item["license"],
            "license_uri": item["license_uri"], "source_record_sha256": item["source_record_sha256"],
            "source_file": item["source_file"], "source_file_sha256": item["source_file_sha256"],
            "source_file_bytes": item["source_file_bytes"], "raw_line_sha256": item["raw_line_sha256"],
            "commit": item["commit"], "old_file": item["old_file"], "new_file": item["new_file"],
            "repositories_raw": item["repositories_raw"], "repositories": item["repositories"],
            "subject_sha256": item["subject_sha256"], "message_sha256": item["message_sha256"],
            "old_contents_sha256": item["old_contents_sha256"],
            "transformation": (
                "Native CommitPackFT repair stimulus from bounded commit subject, message, and old_contents; "
                "new_contents is quarantined and is not an answer, ordering input, prompt input, or output field"
            ),
        },
    }


def build(
    policy_path: Path, addendum_path: Path, snapshot_root: Path, prior_path: Path,
    v2_paths: list[Path], current_queue_path: Path, repair_evidence: list[Path],
) -> tuple[list[dict[str, Any]], dict[str, Any], bytes]:
    policy = validate_policy(policy_path, addendum_path)
    current_bytes = current_queue_path.read_bytes()
    if current_bytes and not current_bytes.endswith(b"\n"):
        raise ValueError("current source queue must end with LF")
    exclusion_paths = [prior_path, *v2_paths, current_queue_path, *repair_evidence]
    exclusions, exclusion_inventory = collect_exclusions(exclusion_paths)
    extension: list[dict[str, Any]] = []
    lanes: dict[str, Any] = {}
    selections = rank_selection(policy)
    tail_policy = policy["schema_version"] == TAIL_POLICY_SCHEMA
    for lane, start, count in selections:
        metadata = policy["source"]["files"][lane]
        # The terminal tail reconstructs the complete inventory committed before V9;
        # freshness exclusions are checked after slicing so the already-emitted first
        # 1,000 cannot renumber the sealed tail.
        eligible, rejected = load_lane(
            snapshot_root / metadata["filename"], lane, policy, set() if tail_policy else exclusions,
        )
        identity_projection = [
            {key: item[key] for key in ("record_id", "selection_key", "source_record_sha256", "raw_line_sha256")}
            for item in eligible
        ]
        inventory_sha256 = sha256_bytes(canonical_json(identity_projection))
        if tail_policy:
            selection = policy["rank_selection"]
            if (
                len(eligible) != selection["expected_inventory_records"]
                or inventory_sha256 != selection["expected_inventory_ordered_identity_sha256"]
            ):
                raise ValueError("terminal tail differs from the pre-V9 eligible inventory commitment")
        if start < 0 or count <= 0 or start + count > len(eligible):
            raise ValueError(f"{lane}: sealed rank slice is outside the eligible inventory")
        selected = eligible[start:start + count]
        selected_identities = {
            (policy["source"]["dataset"], policy["source"]["revision"], item["record_id"])
            for item in selected
        }
        collisions = selected_identities & exclusions
        if collisions:
            raise ValueError(f"{lane}: sealed rank slice collides with {len(collisions)} excluded source identities")
        extension.extend(queue_row(item, start + index + 1, policy) for index, item in enumerate(selected))
        lane_manifest = {
            "physical_records": sum(1 for line in (snapshot_root / metadata["filename"]).open("rb") if line.strip()),
            "eligible_inventory_records": len(eligible),
            "eligible_inventory_ordered_identity_sha256": inventory_sha256,
            "selected_records": len(selected),
            "selected_identity_sha256": sha256_bytes(canonical_json(identity_projection[start:start + count])),
            "rejections": rejected,
            "license_counts": dict(sorted(Counter(item["license"] for item in eligible).items())),
        }
        if tail_policy:
            lane_manifest.update({
                "selected_zero_based_start": start,
                "selected_zero_based_stop_exclusive": start + count,
                "selected_one_based_first_rank": start + 1,
                "selected_one_based_last_rank": start + count,
                "classification_shards": policy["classification_shards"],
            })
        lanes[lane] = lane_manifest
    ids = [row["id"] for row in extension]
    identities = [source_identity(row["source"]) for row in extension]
    if len(ids) != len(set(ids)) or None in identities or len(identities) != len(set(identities)):
        raise ValueError("CommitPackFT extension IDs or source identities are not unique")
    extension_bytes = b"".join(canonical_json(row) + b"\n" for row in extension)
    union_bytes = current_bytes + extension_bytes
    manifest: dict[str, Any] = {
        "schema_version": MANIFEST_SCHEMA,
        "status": "sealed-inactive-terminal-tail" if tail_policy else "sealed-inactive-contingency-pool",
        "activation_condition": policy["activation_condition"],
        "selection_contract": {
            "seed": policy["selection_seed"],
            "ordering": "sha256(seed\\0dataset\\0revision\\0source_file\\0physical_record_id)",
            "records_per_lane": selections[0][2],
            "content_blind": True, "capability_outcomes_used": False,
            "evaluation_content_read": False, "new_contents_in_stimulus_or_ordering_or_output": False,
        },
        "inputs": {
            "policy": {"path": str(policy_path), "sha256": file_sha256(policy_path),
                       "policy_sha256": policy["policy_sha256"]},
            "source_addendum": {"path": str(addendum_path), "sha256": file_sha256(addendum_path)},
            "prior_corpus": {"path": str(prior_path), "sha256": file_sha256(prior_path)},
            "v2_artifacts": [{"path": str(path), "sha256": file_sha256(path)} for path in v2_paths],
            "current_source_queue": {"path": str(current_queue_path), "bytes": len(current_bytes),
                                     "sha256": sha256_bytes(current_bytes)},
            "exclusion_inventory_sha256": sha256_bytes(canonical_json(exclusion_inventory)),
            "exclusion_identity_count": len(exclusions),
        },
        "lanes": lanes,
        "extension": {"records": len(extension), "bytes": len(extension_bytes),
                      "sha256": sha256_bytes(extension_bytes)},
        "union": {"records_added": len(extension), "bytes": len(union_bytes),
                  "sha256": sha256_bytes(union_bytes), "current_queue_is_exact_byte_prefix": True},
        "classification_launched": False, "gcloud_used": False,
    }
    if tail_policy:
        manifest["selection_contract"].update({
            "rank_selection": policy["rank_selection"],
            "classification_shards": policy["classification_shards"],
            "full_ontology_required": True, "all_shards_must_finish": True,
            "early_stop_allowed": False, "content_retries_allowed": False,
            "further_v3_source_expansion_allowed": False,
        })
    manifest["manifest_sha256"] = sha256_bytes(canonical_json(manifest))
    return extension, manifest, union_bytes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--source-addendum", type=Path, required=True)
    parser.add_argument("--snapshot-root", type=Path, required=True)
    parser.add_argument("--prior-corpus", type=Path, required=True)
    parser.add_argument("--v2-artifact", type=Path, action="append", required=True)
    parser.add_argument("--current-source-queue", type=Path, required=True)
    parser.add_argument("--repair-evidence", type=Path, action="append", default=[])
    parser.add_argument("--extension-output", type=Path, required=True)
    parser.add_argument("--union-output", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path, required=True)
    args = parser.parse_args()
    rows, manifest, union = build(
        args.policy, args.source_addendum, args.snapshot_root, args.prior_corpus,
        args.v2_artifact, args.current_source_queue, args.repair_evidence,
    )
    extension = b"".join(canonical_json(row) + b"\n" for row in rows)
    for path in (args.extension_output, args.union_output, args.manifest_output):
        path.parent.mkdir(parents=True, exist_ok=True)
    args.extension_output.write_bytes(extension)
    args.union_output.write_bytes(union)
    args.manifest_output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": manifest["status"], "records": len(rows),
                      "manifest_sha256": manifest["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
