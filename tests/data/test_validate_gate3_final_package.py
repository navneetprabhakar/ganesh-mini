from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import CAPABILITIES, LANES, TASK_TYPES
from scripts.data.validate_gate3_final_package import _capability, _identity, canonical_sha256, validate


RIGHTS = {key: True for key in ("prompt", "answer", "tests", "redistribution", "model_training")}
TARGETS = {"go": .2, "java": .2, "javascript": .1, "typescript": .1, "python": .2, "rust": .2}
PASS_FIELDS = (
    "exact_training_passed", "normalized_training_passed", "fuzzy_training_passed",
    "exact_evaluation_passed", "normalized_evaluation_passed", "fuzzy_evaluation_passed",
)


def word(number: int) -> str:
    chars = []
    while True:
        chars.append(chr(97 + number % 26))
        number //= 26
        if not number:
            return "".join(reversed(chars))


def write_json(path: Path, value: object) -> dict:
    path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")
    return {"path": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def write_jsonl(path: Path, rows: list[dict]) -> dict:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    return {"path": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def write_manifest(path: Path, value: dict) -> None:
    body = dict(value)
    body.pop("manifest_sha256", None)
    body["manifest_sha256"] = canonical_sha256(body)
    write_json(path, body)


def report(base: dict) -> dict:
    base = {"status": "passed", "evaluation_artifacts_read_by_construction": 0, **base}
    base["report_sha256"] = canonical_sha256(base)
    return base


def fixture_package(tmp_path: Path) -> tuple[Path, dict, list[dict], list[dict]]:
    capability = []
    replay = []

    def row(lane: str, kind: str, cap: str | None = None) -> dict:
        n = len(capability) + len(replay)
        value = {
            "id": f"row-{n}", "lane": lane, "task_type": kind,
            "source": {"dataset": "fixture", "revision": "r1", "record_id": f"source-{n}",
                       "source_record_sha256": f"{n + 1:064x}", "license": "MIT"},
            "rights": RIGHTS,
            "messages": [{"role": "user", "content": f"Implement unique{word(n)} behavior"},
                         {"role": "assistant", "content": "return result"}],
        }
        if cap:
            value["primary_capability"] = cap
        return value

    for cap in CAPABILITIES:
        for lane in LANES:
            for kind in TASK_TYPES:
                for _ in range(6):
                    capability.append(row(lane, kind, cap))
    for lane in LANES:
        for kind in TASK_TYPES:
            for _ in range(15):
                replay.append(row(lane, kind))
    all_rows = capability + replay
    package_hash = canonical_sha256(all_rows)
    reviews = []
    for cap in CAPABILITIES:
        selected = [row for row in capability if row["primary_capability"] == cap][:2]
        for n, selected_row in enumerate(selected):
            reviews.append({"record_id": selected_row["id"], "primary_capability": cap,
                            "reviewer_id": f"reviewer-{n}", "blind": True, "verdict": "pass"})
    separation = [{"id": row["id"], "row_sha256": canonical_sha256(row),
                   **{field: True for field in PASS_FIELDS}} for row in all_rows]
    tokens = [{"id": row["id"], "row_sha256": canonical_sha256(row), "input_tokens": 80,
               "supervised_tokens": 20, "objective_weight": TARGETS[row["lane"]] / 150}
              for row in all_rows]
    reports = {
        "admission": report({"records": 720, "rows_sha256": canonical_sha256(capability)}),
        "replay_selection": report({"records": 180, "rows_sha256": canonical_sha256(replay)}),
        "manual_review": report({"package_rows_sha256": package_hash, "reviews": reviews}),
        "separation": report({"package_rows_sha256": package_hash, "records": separation,
                              "content_exposure": {"evaluation_content_serialized": 0,
                                                   "evaluation_paths_or_task_ids_serialized": 0,
                                                   "collision_identities_serialized": 0}}),
        "tokenization": report({"package_rows_sha256": package_hash, "maximum_sequence_length": 2944,
                                "tokenizer_revision": "fixture-revision", "chat_template_sha256": "a" * 64,
                                "response_only_labels_verified": True, "records": tokens}),
    }
    manifest = {"schema_version": "ganesh-mini-gate3-final-package/v1",
                "evaluation_artifacts_read_by_construction": 0,
                "capability": write_jsonl(tmp_path / "capability.jsonl", capability),
                "replay": write_jsonl(tmp_path / "replay.jsonl", replay)}
    for name, value in reports.items():
        manifest[name] = write_json(tmp_path / f"{name}.json", value)
    path = tmp_path / "manifest.json"
    write_manifest(path, manifest)
    return path, manifest, capability, replay


def test_accepts_complete_synthetic_package(tmp_path: Path) -> None:
    path, _, _, _ = fixture_package(tmp_path)
    assert validate(path)["status"] == "validated-not-sealed"


def test_rejects_duplicate_source_even_with_refreshed_file_hash(tmp_path: Path) -> None:
    path, manifest, capability, replay = fixture_package(tmp_path)
    replay[0]["source"] = capability[0]["source"]
    manifest["replay"] = write_jsonl(tmp_path / "replay.jsonl", replay)
    write_manifest(path, manifest)
    with pytest.raises(ValueError, match="unique source identities"):
        validate(path)


def test_rejects_missing_review_report(tmp_path: Path) -> None:
    path, manifest, _, _ = fixture_package(tmp_path)
    del manifest["manual_review"]
    write_manifest(path, manifest)
    with pytest.raises(ValueError, match="manual_review: missing file binding"):
        validate(path)


def test_rejects_eval_exposure_in_sealed_report(tmp_path: Path) -> None:
    path, manifest, _, _ = fixture_package(tmp_path)
    report_path = tmp_path / "separation.json"
    value = json.loads(report_path.read_text(encoding="utf-8"))
    value["evaluation_artifacts_read_by_construction"] = 1
    del value["report_sha256"]
    manifest["separation"] = write_json(report_path, report(value))
    write_manifest(path, manifest)
    with pytest.raises(ValueError, match="zero construction evaluation reads"):
        validate(path)


def test_rejects_missing_token_row(tmp_path: Path) -> None:
    path, manifest, _, _ = fixture_package(tmp_path)
    report_path = tmp_path / "tokenization.json"
    value = json.loads(report_path.read_text(encoding="utf-8"))
    value["records"].pop()
    del value["report_sha256"]
    manifest["tokenization"] = write_json(report_path, report(value))
    write_manifest(path, manifest)
    with pytest.raises(ValueError, match="tokenization does not cover"):
        validate(path)


def test_rejects_wrong_objective_mass(tmp_path: Path) -> None:
    path, manifest, _, _ = fixture_package(tmp_path)
    report_path = tmp_path / "tokenization.json"
    value = json.loads(report_path.read_text(encoding="utf-8"))
    value["records"][0]["objective_weight"] *= 2
    del value["report_sha256"]
    manifest["tokenization"] = write_json(report_path, report(value))
    write_manifest(path, manifest)
    with pytest.raises(ValueError, match="objective family balance"):
        validate(path)


def test_rejects_scaffold_cluster_above_eighteen(tmp_path: Path) -> None:
    path, manifest, capability, _ = fixture_package(tmp_path)
    for row in capability[:19]:
        row["messages"][0]["content"] = "Implement repeated behavior"
    manifest["capability"] = write_jsonl(tmp_path / "capability.jsonl", capability)
    write_manifest(path, manifest)
    with pytest.raises(ValueError, match="scaffold cluster"):
        validate(path)


def test_prior_replay_lineage_only_source_shape(tmp_path: Path) -> None:
    _, _, capability, replay = fixture_package(tmp_path)
    prior = replay[0]
    prior["lineage"] = prior.pop("source")
    assert _identity(prior) != _identity(capability[0])


def test_capability_assignment_only_label_shape(tmp_path: Path) -> None:
    _, _, capability, _ = fixture_package(tmp_path)
    candidate = capability[0]
    name = candidate.pop("primary_capability")
    source = candidate["source"]
    candidate["qualification_assignment"] = {
        "primary_capability": name,
        "cell_id": f"{name}/{candidate['lane']}/{candidate['task_type']}",
        "source_identity": {key: source[key] for key in ("dataset", "revision", "record_id")},
        "source_record_sha256": source["source_record_sha256"],
    }
    assert _capability(candidate) == name
    assert _identity(candidate)


def test_rejects_conflicting_source_hashes(tmp_path: Path) -> None:
    _, _, _, replay = fixture_package(tmp_path)
    prior = replay[0]
    prior["lineage"] = dict(prior["source"])
    prior["lineage"]["source_record_sha256"] = "f" * 64
    with pytest.raises(ValueError, match="conflicting source and lineage"):
        _identity(prior)


def test_rejects_assignment_source_hash_conflict(tmp_path: Path) -> None:
    _, _, capability, _ = fixture_package(tmp_path)
    candidate = capability[0]
    source = candidate["source"]
    candidate["qualification_assignment"] = {
        "primary_capability": candidate["primary_capability"],
        "cell_id": f"{candidate['primary_capability']}/{candidate['lane']}/{candidate['task_type']}",
        "source_identity": {key: source[key] for key in ("dataset", "revision", "record_id")},
        "source_record_sha256": "f" * 64,
    }
    with pytest.raises(ValueError, match="assignment source identity or hash differs"):
        _identity(candidate)
