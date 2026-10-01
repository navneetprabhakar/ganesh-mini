import hashlib
import json
from pathlib import Path

import pytest

from scripts.data.build_commitpackft_repair_extension import LICENSES, canonical_json
from scripts.data.build_v4_commitpackft_source_extension import (
    CONFIG_SCHEMA,
    LANES,
    PLAN_SHA256,
    POLICY_SCHEMA,
    build,
    sha256_bytes,
)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in rows))


def source_row(index: int, lane: str) -> dict:
    language = {"go": "Go", "python": "Python", "rust": "Rust"}[lane]
    suffix = {"go": "go", "python": "py", "rust": "rs"}[lane]
    return {
        "commit": f"{index:040x}", "old_file": f"src/file{index}.{suffix}",
        "new_file": f"src/file{index}.{suffix}", "old_contents": f"broken source {index}",
        "new_contents": f"SECRET_PATCH_{index}", "subject": f"Fix operation {index}",
        "message": f"Correct the bounded behavior for case {index}.", "lang": language,
        "license": "mit", "repos": f"owner/repo{index}",
    }


def seal_config(path: Path, sources: dict[str, Path]) -> dict:
    config = {
        "schema_version": CONFIG_SCHEMA, "dataset": "bigcode/commitpackft",
        "uri": "https://example.test/commitpackft",
        "revision": "fc56fe33c030c6daa414c2b112c932b8eed085e6",
        "revision_tree_cache_sha256": "a" * 64,
        "allowed_record_licenses": list(LICENSES), "files": {},
    }
    for lane, source in sources.items():
        config["files"][lane] = {
            "filename": f"data/{lane}/data.jsonl", "bytes": source.stat().st_size,
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        }
    path.write_text(json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return config


def seal_policy(
    path: Path, config: Path, prior: Path, v2: Path, v3: Path,
) -> dict:
    policy = {
        "schema_version": POLICY_SCHEMA, "status": "sealed-inactive-source-extension",
        "plan_sha256": PLAN_SHA256,
        "source_config_sha256": hashlib.sha256(config.read_bytes()).hexdigest(),
        "selection_seed": "ganesh-mini-gate2-v4-native-commitpackft-repair-source-v1",
        "lanes": list(LANES), "records_per_lane": 1000,
        "selection_contract": {
            "ordering": (
                "sha256(seed\\0lane\\0dataset\\0revision\\0source_file\\0record_id"
                "\\0quarantined_record_sha256)"
            ),
            "content_blind": True, "capability_keywords_used": False,
            "capability_outcomes_used": False, "evaluation_content_read": False,
            "adaptive_top_up_allowed": False,
        },
        "stimulus_limits": {"subject_chars": 256, "message_chars": 1000, "old_contents_chars": 3000},
        "prohibited_markers": ["humaneval", "mbpp", "multi-p-l-e", "multipl-e", "codefuseeval",
                               "codefuse eval", "livecodebench", "swe-bench", "swebench", "lbpp"],
        "new_contents_policy": {
            "included_in_stimulus": False, "included_in_ordering": False,
            "included_in_output": False,
            "permitted_uses": ["complete_source_record_hash", "prohibited_marker_safety_filter"],
        },
        "exclusion_bindings": {
            "prior_corpus_sha256": hashlib.sha256(prior.read_bytes()).hexdigest(),
            "v2_artifact_sha256s": [hashlib.sha256(v2.read_bytes()).hexdigest()],
            "v3_queue_sha256": hashlib.sha256(v3.read_bytes()).hexdigest(),
            "v3_queue_lineages": 120,
        },
        "classification_launched": False,
    }
    policy["policy_sha256"] = sha256_bytes(canonical_json(policy))
    path.write_text(json.dumps(policy, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return policy


def fixture(tmp_path: Path):
    root = tmp_path / "snapshot"
    sources = {}
    rows_by_lane = {}
    for lane_index, lane in enumerate(LANES):
        source = root / f"data/{lane}/data.jsonl"
        rows = [source_row(lane_index * 2000 + index, lane) for index in range(1001)]
        write_jsonl(source, rows); sources[lane] = source; rows_by_lane[lane] = rows
    config = tmp_path / "config.json"; seal_config(config, sources)
    first = rows_by_lane["go"][0]
    prior = tmp_path / "prior.jsonl"
    write_jsonl(prior, [{"source": {
        "dataset": "bigcode/commitpackft", "revision": "fc56fe33c030c6daa414c2b112c932b8eed085e6",
        "record_id": "data/go/data.jsonl:line-00000001",
        "source_record_sha256": sha256_bytes(canonical_json(first)),
    }}])
    v2 = tmp_path / "v2.jsonl"; write_jsonl(v2, [])
    v3 = tmp_path / "v3.jsonl"
    write_jsonl(v3, [{"source": {
        "dataset": "other", "revision": "rev", "record_id": f"record-{index}",
        "source_record_sha256": f"{index:064x}",
    }} for index in range(120)])
    policy = tmp_path / "policy.json"; seal_policy(policy, config, prior, v2, v3)
    return config, policy, sources, prior, v2, v3


def test_builds_exact_fresh_deterministic_tranche_and_quarantines_patch(tmp_path: Path) -> None:
    config, policy, sources, prior, v2, v3 = fixture(tmp_path)
    first = build(config, policy, sources, prior, [v2], v3)
    second = build(config, policy, sources, prior, [v2], v3)
    rows, manifest = first

    assert first == second
    assert len(rows) == 3000
    assert all(sum(row["lane"] == lane for row in rows) == 1000 for lane in LANES)
    assert len({tuple(row["source"][key] for key in (
        "dataset", "revision", "record_id", "source_record_sha256",
    )) for row in rows}) == 3000
    assert all(row["source"]["selection_rank"] in range(1, 1001) for row in rows)
    serialized = b"".join(canonical_json(row) for row in rows)
    assert b"SECRET_PATCH" not in serialized
    assert b'"new_contents"' not in serialized
    assert manifest["exclusions"] == {
        "prior_lineages": 1, "v2_lineages": 0, "v3_lineages": 120,
        "union_lineages": 121,
        "union_identity_sha256": manifest["exclusions"]["union_identity_sha256"],
    }
    assert manifest["classification_launched"] is False
    assert manifest["gcloud_used"] is False
    body = dict(manifest); seal = body.pop("manifest_sha256")
    assert seal == sha256_bytes(canonical_json(body))


def test_new_contents_cannot_change_selection_order_or_stimulus(tmp_path: Path) -> None:
    config, policy, sources, prior, v2, v3 = fixture(tmp_path)
    first_rows, _ = build(config, policy, sources, prior, [v2], v3)
    python_rows = [json.loads(line) for line in sources["python"].read_text().splitlines()]
    python_rows[0]["new_contents"] = "A_DIFFERENT_QUARANTINED_PATCH"
    write_jsonl(sources["python"], python_rows)
    seal_config(config, sources); seal_policy(policy, config, prior, v2, v3)
    second_rows, _ = build(config, policy, sources, prior, [v2], v3)
    assert [(row["id"], row["source"]["record_id"], row["stimulus"]) for row in first_rows] == [
        (row["id"], row["source"]["record_id"], row["stimulus"]) for row in second_rows
    ]


def test_fails_closed_on_payload_exclusion_and_minimum_drift(tmp_path: Path) -> None:
    config, policy, sources, prior, v2, v3 = fixture(tmp_path)
    with sources["rust"].open("ab") as handle:
        handle.write(b"\n")
    with pytest.raises(ValueError, match="exact pinned binding"):
        build(config, policy, sources, prior, [v2], v3)

    config, policy, sources, prior, v2, v3 = fixture(tmp_path / "exclusion")
    write_jsonl(v2, [{"source": {"dataset": "changed", "revision": "r", "record_id": "x",
                                      "source_record_sha256": "f" * 64}}])
    with pytest.raises(ValueError, match="v2 artifact"):
        build(config, policy, sources, prior, [v2], v3)

    config, policy, sources, prior, v2, v3 = fixture(tmp_path / "minimum")
    go_rows = [json.loads(line) for line in sources["go"].read_text().splitlines()][:1000]
    write_jsonl(sources["go"], go_rows)
    seal_config(config, sources); seal_policy(policy, config, prior, v2, v3)
    with pytest.raises(ValueError, match="fewer than 1,000"):
        build(config, policy, sources, prior, [v2], v3)
