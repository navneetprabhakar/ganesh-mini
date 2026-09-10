import json
from collections import Counter
from pathlib import Path

from scripts.train.build_lane_stratified_probe import GROUP_COUNTS, LANES, TARGETS, build, canonical_sha256


def source_row(lane: str, index: int) -> dict:
    return {
        "source_id": f"{lane}-{index}",
        "id": f"{lane}-{index}",
        "lane": lane,
        "input_ids": [1, 2, 3, 4 + index],
        "attention_mask": [1, 1, 1, 1],
        "labels": [-100, -100, 3, 4 + index],
        "prompt_token_count": 2,
        "response_token_count": 2,
        "rendered_prompt_sha256": "a" * 64,
        "objective_weight": 99.0,
    }


def test_builder_creates_disjoint_exact_six_lane_optimizer_groups(tmp_path: Path) -> None:
    source = tmp_path / "source.jsonl"
    rows = [source_row(lane, index) for lane in LANES for index in range(8)]
    source.write_text("".join(json.dumps(row) + "\n" for row in rows))
    train, retention, manifest_path = tmp_path / "train.jsonl", tmp_path / "retention.jsonl", tmp_path / "manifest.json"

    manifest = build(source, train, retention, manifest_path, optimizer_groups=2, retention_per_lane=1, seed=7)

    training = [json.loads(line) for line in train.read_text().splitlines()]
    held_out = [json.loads(line) for line in retention.read_text().splitlines()]
    assert len(training) == 20
    assert len(held_out) == 6
    assert {row["source_id"] for row in training}.isdisjoint(row["source_id"] for row in held_out)
    for group_index in range(2):
        group = training[group_index * 10:(group_index + 1) * 10]
        assert Counter(row["lane"] for row in group) == Counter(GROUP_COUNTS)
        mass = Counter()
        for row in group:
            mass[row["lane"]] += row["objective_weight"]
            assert row["optimizer_group"] == group_index
        assert all(abs(mass[lane] - TARGETS[lane]) <= 1e-12 for lane in LANES)
    assert manifest["group_contract"]["every_group_contains_all_six_lanes"] is True
    claimed = manifest.pop("manifest_sha256")
    assert claimed == canonical_sha256(manifest)


def test_repository_lane_stratified_artifacts_are_reproducible(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[2]
    output = tmp_path / "prepared-train.jsonl"
    retention = tmp_path / "prepared-retention.jsonl"
    manifest_path = tmp_path / "manifest.json"
    report = build(
        root / "artifacts/train/expansion-pilot-v1/prepared-train.jsonl",
        output,
        retention,
        manifest_path,
    )
    committed = json.loads((root / "artifacts/train/expansion-lane-stratified-probe-v3/prepared-dataset-manifest.json").read_text())
    assert report["prepared_train"]["sha256"] == committed["prepared_train"]["sha256"]
    assert report["prepared_validation"]["sha256"] == committed["prepared_validation"]["sha256"]
