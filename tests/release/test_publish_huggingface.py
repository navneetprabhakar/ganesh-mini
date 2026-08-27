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


def fixture(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
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
    decision = sealed({
        "schema_version": "ganesh-mini-release-decision/v2",
        "status": "release-eligible",
        "failed_checks": [],
        "checks": [{
            "name": "required_manifests_complete",
            "passed": True,
            "evidence": {"manifests": [
                {"seal": manifest["manifest_sha256"], "passed": True},
                {"seal": export["evidence_sha256"], "passed": True},
            ]},
        }],
    }, "evidence_sha256")
    card = tmp_path / "README.md"
    card.write_text("---\nlicense: apache-2.0\n---\n# Ganesh Mini\n", encoding="utf-8")
    return (
        write(tmp_path / "decision.json", decision),
        write(tmp_path / "artifacts.json", manifest),
        write(tmp_path / "export.json", export),
        card,
    )


def test_publication_plan_is_sealed_and_contains_all_release_files(tmp_path: Path) -> None:
    decision, artifacts, export, card = fixture(tmp_path)
    plan, uploads = build_plan(
        repo_id="forge/ganesh-mini-1.0",
        visibility="public",
        decision_path=decision,
        artifact_manifest_path=artifacts,
        export_equivalence_path=export,
        model_card_path=card,
    )
    assert plan["status"] == "ready"
    assert canonical_sha256({key: value for key, value in plan.items() if key != "plan_sha256"}) == plan["plan_sha256"]
    assert {remote for remote, _ in uploads} == {row["path_in_repo"] for row in plan["files"]}


def test_publication_rejects_changed_artifact(tmp_path: Path) -> None:
    decision, artifacts, export, card = fixture(tmp_path)
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
        )
