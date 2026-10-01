import hashlib
import json
from pathlib import Path

import pytest

from scripts.data.build_commitpackft_repair_extension import (
    LICENSES,
    PARENT_PLAN_SHA256,
    POLICY_SCHEMA,
    TAIL_POLICY_SCHEMA,
    build,
    canonical_json,
    load_lane,
    sha256_bytes,
)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in rows))


def source_row(index: int, language: str, **changes) -> dict:
    row = {
        "commit": f"{index:040x}", "old_file": f"src/file{index}.js",
        "new_file": f"src/file{index}.js", "old_contents": f"function f{index}(x) {{ return x + 1; }}",
        "new_contents": f"ANSWER_PATCH_TOKEN_{index}", "subject": f"Fix bounded operation {index}",
        "message": f"Repair the incorrect result for case {index}.", "lang": language,
        "license": "mit", "repos": f"owner/repo{index},fork/repo{index}",
    }
    row.update(changes)
    return row


def sealed_policy(path: Path, addendum: Path, files: dict[str, Path]) -> dict:
    policy = {
        "schema_version": POLICY_SCHEMA, "status": "sealed-inactive-contingency",
        "parent_plan_sha256": PARENT_PLAN_SHA256,
        "source_addendum_sha256": hashlib.sha256(addendum.read_bytes()).hexdigest(),
        "activation_condition": "v8-terminal-global-120-source-match-infeasible",
        "selection_seed": "ganesh-mini-gate2-v3-commitpackft-v1", "records_per_lane": 1000,
        "stimulus_limits": {"subject_chars": 256, "message_chars": 1000, "old_contents_chars": 3000},
        "cohort_policy": {"minimum_distinct_datasets": 2, "maximum_per_dataset_per_cohort": 30},
        "source": {
            "dataset": "bigcode/commitpackft", "uri": "https://example.test/commitpackft",
            "revision": "fc56fe33c030c6daa414c2b112c932b8eed085e6",
            "allowed_record_licenses": list(LICENSES), "files": {},
        },
        "prohibited_markers": ["humaneval", "mbpp", "multi-p-l-e", "multipl-e", "codefuseeval",
                               "codefuse eval", "livecodebench", "swe-bench", "swebench", "lbpp"],
        "new_contents_policy": {
            "included_in_stimulus": False, "included_in_ordering": False, "included_in_output": False,
            "permitted_uses": ["complete_source_record_hash", "prohibited_marker_safety_filter"],
        },
    }
    for lane, source in files.items():
        policy["source"]["files"][lane] = {
            "filename": str(source.relative_to(source.parents[2])), "bytes": source.stat().st_size,
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        }
    policy["policy_sha256"] = sha256_bytes(canonical_json(policy))
    path.write_text(json.dumps(policy, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return policy


def sealed_tail_policy(path: Path, addendum: Path, typescript: Path) -> dict:
    policy = {
        "schema_version": TAIL_POLICY_SCHEMA, "status": "sealed-inactive-terminal-tail",
        "parent_plan_sha256": PARENT_PLAN_SHA256,
        "source_addendum_sha256": hashlib.sha256(addendum.read_bytes()).hexdigest(),
        "activation_condition": "v9-terminal-global-120-source-match-infeasible",
        "selection_seed": "ganesh-mini-gate2-v3-commitpackft-v1",
        "rank_selection": {
            "lane": "typescript", "zero_based_start": 1000, "count": 3990,
            "one_based_first_rank": 1001, "one_based_last_rank": 4990,
            "expected_inventory_records": 4990,
            "expected_inventory_ordered_identity_sha256": "0" * 64,
        },
        "classification_shards": [
            {"shard": 1, "classifier_tail_offset": 0, "count": 998},
            {"shard": 2, "classifier_tail_offset": 998, "count": 998},
            {"shard": 3, "classifier_tail_offset": 1996, "count": 998},
            {"shard": 4, "classifier_tail_offset": 2994, "count": 996},
        ],
        "terminal_bindings": {
            "prior_addendum_sha256": "5d1301d7e277f6ea977e6ccc6740a33f877ed0d20cc4a535098b8947c2788049",
            "prior_policy_file_sha256": "7ab381b7a2be66b175a5833450b77489d8b7e91a9feeab54a170fa23e1e4dbb7",
            "prior_policy_sha256": "d17aa531b9ad1d95b186e544ecf6f68cf2626c79a56fb0ce587a0d2f5d686028",
            "v9_aggregate_file_sha256": "a3f27f9666c1f07f617c812fe816d811323adc26eccad3b0b7a55a26779cb295",
            "v9_aggregate_sha256": "6f1251d3e7db2c09f315b74784f550620fb6fb31f47a35b0ce8570cecf7b7614",
            "v9_queue_failure_file_sha256": "0b1aee312b2ebffbb04e2724e9b70d52748987db9fedf952ade4ebafa345e354",
            "v9_queue_failure_sha256": "0505bbdf7893e5458fe6c0ca65aca8be992262212a5089c120966dab84d6d47b",
        },
        "full_ontology_required": True, "all_shards_must_finish": True,
        "early_stop_allowed": False, "content_retries_allowed": False,
        "further_v3_source_expansion_allowed": False,
        "stimulus_limits": {"subject_chars": 256, "message_chars": 1000, "old_contents_chars": 3000},
        "cohort_policy": {"minimum_distinct_datasets": 2, "maximum_per_dataset_per_cohort": 30},
        "source": {
            "dataset": "bigcode/commitpackft", "uri": "https://example.test/commitpackft",
            "revision": "fc56fe33c030c6daa414c2b112c932b8eed085e6",
            "allowed_record_licenses": list(LICENSES),
            "files": {"typescript": {
                "filename": str(typescript.relative_to(typescript.parents[2])),
                "bytes": typescript.stat().st_size,
                "sha256": hashlib.sha256(typescript.read_bytes()).hexdigest(),
            }},
        },
        "prohibited_markers": ["humaneval", "mbpp", "multi-p-l-e", "multipl-e", "codefuseeval",
                               "codefuse eval", "livecodebench", "swe-bench", "swebench", "lbpp"],
        "new_contents_policy": {
            "included_in_stimulus": False, "included_in_ordering": False, "included_in_output": False,
            "permitted_uses": ["complete_source_record_hash", "prohibited_marker_safety_filter"],
        },
    }
    eligible, rejected = load_lane(typescript, "typescript", policy, set())
    assert len(eligible) == 4990 and rejected == {}
    projection = [
        {key: item[key] for key in ("record_id", "selection_key", "source_record_sha256", "raw_line_sha256")}
        for item in eligible
    ]
    policy["rank_selection"]["expected_inventory_ordered_identity_sha256"] = sha256_bytes(
        canonical_json(projection)
    )
    policy["policy_sha256"] = sha256_bytes(canonical_json(policy))
    path.write_text(json.dumps(policy, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return policy


def fixture(tmp_path: Path):
    snapshot = tmp_path / "snapshot"
    javascript = snapshot / "data/javascript/data.jsonl"
    typescript = snapshot / "data/typescript/data.jsonl"
    js_rows = [source_row(index, "JavaScript") for index in range(1000)]
    js_rows.extend([
        source_row(2001, "JavaScript", license="agpl-3.0"),
        source_row(2002, "JavaScript", old_contents=""),
        source_row(2003, "JavaScript", new_contents="copied from HumanEval answer"),
    ])
    ts_rows = [source_row(3000 + index, "TypeScript", old_file=f"src/file{index}.ts",
                          new_file=f"src/file{index}.ts") for index in range(1000)]
    write_jsonl(javascript, js_rows); write_jsonl(typescript, ts_rows)
    addendum = tmp_path / "addendum.md"; addendum.write_text("sealed fixture addendum\n", encoding="utf-8")
    policy_path = tmp_path / "policy.json"
    sealed_policy(policy_path, addendum, {"javascript": javascript, "typescript": typescript})
    prior = tmp_path / "prior.jsonl"; write_jsonl(prior, [])
    v2 = tmp_path / "v2.jsonl"; write_jsonl(v2, [])
    current = tmp_path / "current.jsonl"
    current_row = {
        "id": "existing", "lane": "python", "task_type": "repair", "stimulus": "existing",
        "source": {"dataset": "other", "revision": "rev", "record_id": "record",
                   "source_record_sha256": "a" * 64},
    }
    write_jsonl(current, [current_row])
    return policy_path, addendum, snapshot, prior, v2, current, current_row


def test_builds_fixed_content_blind_pool_and_quarantines_new_contents(tmp_path: Path) -> None:
    policy, addendum, snapshot, prior, v2, current, current_row = fixture(tmp_path)
    first = build(policy, addendum, snapshot, prior, [v2], current, [])
    second = build(policy, addendum, snapshot, prior, [v2], current, [])
    rows, manifest, union = first

    assert first == second
    assert len(rows) == 2000
    assert sha256_bytes(b"".join(canonical_json(row) + b"\n" for row in rows)) == (
        "c2181668cb6cfe8b3805dc3fde5d02a9d76ed34caad733daf5ae9291cf22c506"
    )
    assert sum(row["lane"] == "javascript" for row in rows) == 1000
    assert sum(row["lane"] == "typescript" for row in rows) == 1000
    assert len({(row["source"]["dataset"], row["source"]["revision"], row["source"]["record_id"])
                for row in rows}) == 2000
    serialized = b"".join(canonical_json(row) for row in rows)
    assert b"ANSWER_PATCH_TOKEN" not in serialized
    assert b'"new_contents"' not in serialized
    assert manifest["selection_contract"]["capability_outcomes_used"] is False
    assert manifest["lanes"]["javascript"]["eligible_inventory_records"] == 1000
    assert manifest["lanes"]["javascript"]["rejections"] == {
        "empty_old_contents": 1, "license_not_allowlisted": 1, "prohibited_marker": 1,
    }
    assert union.startswith(canonical_json(current_row) + b"\n")
    assert manifest["union"]["current_queue_is_exact_byte_prefix"] is True
    body = dict(manifest); seal = body.pop("manifest_sha256")
    assert seal == sha256_bytes(canonical_json(body))


def test_new_contents_cannot_change_stimulus_selection_or_order(tmp_path: Path) -> None:
    policy, addendum, snapshot, prior, v2, current, _ = fixture(tmp_path)
    first_rows, first_manifest, _ = build(policy, addendum, snapshot, prior, [v2], current, [])
    js_path = snapshot / "data/javascript/data.jsonl"
    raw = [json.loads(line) for line in js_path.read_text(encoding="utf-8").splitlines()]
    raw[0]["new_contents"] = "A_DIFFERENT_QUARANTINED_PATCH"
    write_jsonl(js_path, raw)
    sealed_policy(policy, addendum, {
        "javascript": js_path, "typescript": snapshot / "data/typescript/data.jsonl",
    })
    second_rows, second_manifest, _ = build(policy, addendum, snapshot, prior, [v2], current, [])

    first_visible = [(row["source"]["record_id"], row["stimulus"]) for row in first_rows]
    second_visible = [(row["source"]["record_id"], row["stimulus"]) for row in second_rows]
    assert first_visible == second_visible
    assert (first_manifest["lanes"]["javascript"]["selected_identity_sha256"]
            != second_manifest["lanes"]["javascript"]["selected_identity_sha256"])


def test_fails_closed_on_policy_addendum_and_snapshot_drift(tmp_path: Path) -> None:
    policy, addendum, snapshot, prior, v2, current, _ = fixture(tmp_path)
    value = json.loads(policy.read_text()); value["records_per_lane"] = 999
    policy.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError, match="policy"):
        build(policy, addendum, snapshot, prior, [v2], current, [])

    policy, addendum, snapshot, prior, v2, current, _ = fixture(tmp_path / "addendum")
    addendum.write_text("drifted\n", encoding="utf-8")
    with pytest.raises(ValueError, match="policy"):
        build(policy, addendum, snapshot, prior, [v2], current, [])

    policy, addendum, snapshot, prior, v2, current, _ = fixture(tmp_path / "snapshot")
    with (snapshot / "data/javascript/data.jsonl").open("ab") as handle:
        handle.write(b"\n")
    with pytest.raises(ValueError, match="snapshot"):
        build(policy, addendum, snapshot, prior, [v2], current, [])


def test_preserves_commit_file_repository_license_and_hash_lineage(tmp_path: Path) -> None:
    policy, addendum, snapshot, prior, v2, current, _ = fixture(tmp_path)
    rows, manifest, _ = build(policy, addendum, snapshot, prior, [v2], current, [])
    row = rows[0]
    source = row["source"]
    assert source["commit"] and source["old_file"] and source["new_file"]
    assert source["repositories"] == source["repositories_raw"].split(",")
    assert source["license"] == "MIT"
    assert all(len(source[field]) == 64 for field in (
        "source_file_sha256", "raw_line_sha256", "source_record_sha256",
        "subject_sha256", "message_sha256", "old_contents_sha256",
    ))
    assert manifest["lanes"]["javascript"]["license_counts"] == {"MIT": 1000}


def test_terminal_tail_is_complete_disjoint_deterministic_and_quarantined(tmp_path: Path) -> None:
    snapshot = tmp_path / "snapshot"
    javascript = snapshot / "data/javascript/data.jsonl"
    typescript = snapshot / "data/typescript/data.jsonl"
    write_jsonl(javascript, [source_row(index, "JavaScript") for index in range(1000)])
    write_jsonl(typescript, [
        source_row(5000 + index, "TypeScript", old_file=f"src/file{index}.ts",
                   new_file=f"src/file{index}.ts")
        for index in range(4990)
    ])
    first_addendum = tmp_path / "first-addendum.md"
    first_addendum.write_text("sealed first-pool fixture\n", encoding="utf-8")
    first_policy = tmp_path / "first-policy.json"
    sealed_policy(first_policy, first_addendum, {"javascript": javascript, "typescript": typescript})
    prior = tmp_path / "prior.jsonl"; write_jsonl(prior, [])
    v2 = tmp_path / "v2.jsonl"; write_jsonl(v2, [])
    base_queue = tmp_path / "base.jsonl"
    write_jsonl(base_queue, [{
        "id": "existing", "lane": "python", "task_type": "repair", "stimulus": "existing",
        "source": {"dataset": "other", "revision": "rev", "record_id": "record"},
    }])

    first_rows, first_manifest, _ = build(
        first_policy, first_addendum, snapshot, prior, [v2], base_queue, [],
    )
    assert "rank_selection" not in first_manifest["selection_contract"]
    first_ts = [row for row in first_rows if row["lane"] == "typescript"]
    current = tmp_path / "current-with-first-pool.jsonl"
    write_jsonl(current, [json.loads(line) for line in base_queue.read_text().splitlines()] + first_rows)

    tail_addendum = tmp_path / "tail-addendum.md"
    tail_addendum.write_text("sealed terminal-tail fixture\n", encoding="utf-8")
    tail_policy = tmp_path / "tail-policy.json"
    tail_policy_value = sealed_tail_policy(tail_policy, tail_addendum, typescript)
    first_build = build(tail_policy, tail_addendum, snapshot, prior, [v2], current, [])
    second_build = build(tail_policy, tail_addendum, snapshot, prior, [v2], current, [])
    rows, manifest, _ = first_build

    assert first_build == second_build
    assert len(rows) == 3990
    assert {row["lane"] for row in rows} == {"typescript"}
    assert rows[0]["id"].endswith("-1001")
    assert rows[-1]["id"].endswith("-4990")
    first_identities = {row["source"]["record_id"] for row in first_ts}
    tail_identities = {row["source"]["record_id"] for row in rows}
    assert first_identities.isdisjoint(tail_identities)
    assert len(first_identities | tail_identities) == 4990

    lane = manifest["lanes"]["typescript"]
    assert lane["eligible_inventory_records"] == 4990
    assert lane["eligible_inventory_ordered_identity_sha256"] == (
        first_manifest["lanes"]["typescript"]["eligible_inventory_ordered_identity_sha256"]
    ) == tail_policy_value["rank_selection"]["expected_inventory_ordered_identity_sha256"]
    assert (lane["selected_zero_based_start"], lane["selected_zero_based_stop_exclusive"]) == (1000, 4990)
    assert (lane["selected_one_based_first_rank"], lane["selected_one_based_last_rank"]) == (1001, 4990)

    shards = manifest["selection_contract"]["classification_shards"]
    cursor = 0
    for shard in shards:
        assert shard["classifier_tail_offset"] == cursor
        cursor += shard["count"]
    assert cursor == 3990
    assert [shard["count"] for shard in shards] == [998, 998, 998, 996]
    serialized = b"".join(canonical_json(row) for row in rows)
    assert b"ANSWER_PATCH_TOKEN" not in serialized
    assert b'"new_contents"' not in serialized

    source_rows = [json.loads(line) for line in typescript.read_text(encoding="utf-8").splitlines()]
    source_rows[0]["new_contents"] = "DIFFERENT_QUARANTINED_TAIL_PATCH"
    write_jsonl(typescript, source_rows)
    resealed = sealed_tail_policy(tail_policy, tail_addendum, typescript)
    changed_rows, changed_manifest, _ = build(
        tail_policy, tail_addendum, snapshot, prior, [v2], current, [],
    )
    assert [(row["source"]["record_id"], row["stimulus"]) for row in changed_rows] == [
        (row["source"]["record_id"], row["stimulus"]) for row in rows
    ]
    assert changed_manifest["lanes"]["typescript"]["eligible_inventory_ordered_identity_sha256"] == (
        resealed["rank_selection"]["expected_inventory_ordered_identity_sha256"]
    )

    drifted = json.loads(tail_policy.read_text())
    drifted["rank_selection"]["expected_inventory_ordered_identity_sha256"] = "a" * 64
    drifted.pop("policy_sha256")
    drifted["policy_sha256"] = sha256_bytes(canonical_json(drifted))
    tail_policy.write_text(json.dumps(drifted, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="pre-V9 eligible inventory commitment"):
        build(tail_policy, tail_addendum, snapshot, prior, [v2], current, [])
