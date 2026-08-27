import json
from pathlib import Path

import pytest

from scripts.release.publish_huggingface import build_plan, canonical_sha256


def sealed(value: dict, field: str) -> dict:
    value = dict(value)
    value[field] = canonical_sha256(value)
    return value


def write(path: Path, value: dict) -> Path:
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def fixture(tmp_path: Path) -> tuple[Path, Path, Path, Path, list[Path]]:
    import hashlib

    merged = tmp_path / "merged"
    merged.mkdir()
    config = merged / "config.json"
    config.write_bytes(b"{}")
    config_sha = hashlib.sha256(b"{}").hexdigest()
    inventory = [{"path": "config.json", "bytes": 2, "sha256": config_sha}]
    f16 = tmp_path / "f16.gguf"
    q8 = tmp_path / "q8.gguf"
    f16.write_bytes(b"f16")
    q8.write_bytes(b"q8")
    manifest = sealed({
        "schema_version": "ganesh-mini-release-artifacts/v1",
        "status": "built",
        "model_name": "ganesh-mini-1.0",
        "base_model": {
            "model_id": "Qwen/Qwen3.5-2B",
            "revision": "15852e8c16360a2fea060d615a32b45270f8a8fc",
        },
        "llama_cpp": {"llama_cli_sha256": "c" * 64},
        "artifacts": {
            "merged_bf16_hf": {"path": str(merged), "sha256": canonical_sha256(inventory), "files": inventory},
            "gguf_f16": {"path": str(f16), "bytes": 3, "sha256": hashlib.sha256(b"f16").hexdigest()},
            "gguf_q8": {"path": str(q8), "bytes": 2, "sha256": hashlib.sha256(b"q8").hexdigest()},
        },
    }, "manifest_sha256")
    export = sealed({
        "schema_version": "ganesh-mini-export-equivalence/v1",
        "status": "passed",
        "artifact_manifest_sha256": manifest["manifest_sha256"],
    }, "evidence_sha256")
    comparisons = [
        sealed({"schema_version": "1.0", "kind": kind}, "report_sha256")
        for kind in ("qwen", "ganesh-v01", "quantization")
    ]
    laptop = sealed({"schema_version": "ganesh-mini-laptop-certification/v1", "status": "passed"}, "evidence_sha256")
    seed = sealed({"schema_version": "ganesh-mini-seed-manifest/v1"}, "manifest_sha256")
    readiness = sealed({"schema_version": "ganesh-mini-readiness/v1", "status": "ready"}, "report_sha256")
    execution_card = sealed({"schema_version": "ganesh-mini-training-execution-card/v1", "status": "ready"}, "card_sha256")
    training = sealed({"schema_version": "ganesh-mini-sft-run/v2", "status": "complete"}, "evidence_sha256")
    lineage = [seed, readiness, execution_card, training]
    decision = sealed({
        "schema_version": "ganesh-mini-release-decision/v2",
        "status": "release-eligible",
        "failed_checks": [],
        "checks": [
            {
                "name": "sealed_complete_decision_comparisons",
                "passed": True,
                "evidence": {
                    "qwen": {"report_sha256": comparisons[0]["report_sha256"]},
                    "ganesh_v01": {"report_sha256": comparisons[1]["report_sha256"]},
                    "quantization": {"report_sha256": comparisons[2]["report_sha256"]},
                },
            },
            {
                "name": "laptop_evidence_and_artifacts_bound",
                "passed": True,
                "evidence": {"laptop_evidence_sha256": laptop["evidence_sha256"]},
            },
            {
                "name": "required_manifests_complete",
                "passed": True,
                "evidence": {"manifests": [
                    *[{"seal": value[next(field for field in ("manifest_sha256", "report_sha256", "card_sha256", "evidence_sha256") if field in value)], "passed": True} for value in lineage],
                    {"seal": manifest["manifest_sha256"], "passed": True},
                    {"seal": export["evidence_sha256"], "passed": True},
                ]},
            },
        ],
    }, "evidence_sha256")
    card = tmp_path / "README.md"
    card.write_text("---\nlicense: apache-2.0\n---\n# Ganesh Mini\n", encoding="utf-8")
    evidence = [
        *[write(tmp_path / f"comparison-{index}.json", value) for index, value in enumerate(comparisons)],
        write(tmp_path / "laptop.json", laptop),
        *[write(tmp_path / f"lineage-{index}.json", value) for index, value in enumerate(lineage)],
    ]
    return (
        write(tmp_path / "decision.json", decision),
        write(tmp_path / "artifacts.json", manifest),
        write(tmp_path / "export.json", export),
        card,
        evidence,
    )


def test_publication_plan_is_sealed_and_contains_all_release_files(tmp_path: Path) -> None:
    decision, artifacts, export, card, evidence = fixture(tmp_path)
    plan, uploads = build_plan(
        repo_id="forge/ganesh-mini-1.0",
        visibility="public",
        decision_path=decision,
        artifact_manifest_path=artifacts,
        export_equivalence_path=export,
        model_card_path=card,
        evidence_paths=evidence,
    )
    assert plan["status"] == "ready"
    assert canonical_sha256({key: value for key, value in plan.items() if key != "plan_sha256"}) == plan["plan_sha256"]
    assert {remote for remote, _ in uploads} == {row["path_in_repo"] for row in plan["files"]}


def test_publication_rejects_changed_artifact(tmp_path: Path) -> None:
    decision, artifacts, export, card, evidence = fixture(tmp_path)
    manifest = json.loads(artifacts.read_text())
    Path(manifest["artifacts"]["gguf_q8"]["path"]).write_bytes(b"changed")
    with pytest.raises(ValueError, match="gguf_q8 artifact mismatch"):
        build_plan(
            repo_id="forge/ganesh-mini-1.0",
            visibility="private",
            decision_path=decision,
            artifact_manifest_path=artifacts,
            export_equivalence_path=export,
            model_card_path=card,
            evidence_paths=evidence,
        )


def test_publication_rejects_incomplete_evidence_closure(tmp_path: Path) -> None:
    decision, artifacts, export, card, evidence = fixture(tmp_path)
    with pytest.raises(ValueError, match="closure mismatch"):
        build_plan(
            repo_id="forge/ganesh-mini-1.0",
            visibility="public",
            decision_path=decision,
            artifact_manifest_path=artifacts,
            export_equivalence_path=export,
            model_card_path=card,
            evidence_paths=evidence[:-1],
        )
