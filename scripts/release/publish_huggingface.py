#!/usr/bin/env python3
"""Publish a release-eligible Ganesh Mini artifact set to one Hugging Face model repo."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SEAL_FIELDS = ("manifest_sha256", "report_sha256", "evidence_sha256", "run_sha256", "card_sha256")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    unsigned = dict(value)
    claimed = unsigned.pop(field, None)
    if claimed != canonical_sha256(unsigned):
        raise ValueError(f"invalid {field}: {path}")
    return value


def load_any_sealed(path: Path) -> tuple[dict[str, Any], str]:
    value = json.loads(path.read_text(encoding="utf-8"))
    present = [field for field in SEAL_FIELDS if field in value]
    if len(present) != 1:
        raise ValueError(f"evidence must contain exactly one recognized seal: {path}")
    field = present[0]
    return load_sealed(path, field), field


def expected_evidence_seals(decision: dict[str, Any]) -> set[str]:
    checks = {row.get("name"): row for row in decision.get("checks", [])}
    comparisons = checks.get("sealed_complete_decision_comparisons", {}).get("evidence", {})
    manifests = checks.get("required_manifests_complete", {}).get("evidence", {}).get("manifests", [])
    laptop = checks.get("laptop_evidence_and_artifacts_bound", {}).get("evidence", {})
    expected = {
        comparisons.get(name, {}).get("report_sha256")
        for name in ("qwen", "ganesh_v01", "quantization")
    }
    expected.add(laptop.get("laptop_evidence_sha256"))
    expected.update(row.get("seal") for row in manifests if row.get("passed") is True)
    if None in expected or len(expected) != 10:
        raise ValueError("release decision does not expose the complete ten-seal evidence closure")
    return expected


def evidence_remote_path(value: dict[str, Any], seal: str) -> str:
    schema = str(value.get("schema_version", "evidence"))
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", schema).strip("-").lower()
    return f"evidence/{slug}-{seal[:12]}.json"


def verified_release_inputs(
    decision_path: Path,
    artifact_manifest_path: Path,
    export_equivalence_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    decision = load_sealed(decision_path, "evidence_sha256")
    artifacts = load_sealed(artifact_manifest_path, "manifest_sha256")
    export = load_sealed(export_equivalence_path, "evidence_sha256")
    if (
        decision.get("schema_version") != "ganesh-mini-release-decision/v2"
        or decision.get("status") != "release-eligible"
        or decision.get("failed_checks") != []
        or not decision.get("checks")
        or not all(row.get("passed") is True for row in decision["checks"])
    ):
        raise ValueError("release decision is not eligible")
    if (
        artifacts.get("schema_version") != "ganesh-mini-release-artifacts/v1"
        or artifacts.get("status") != "built"
        or artifacts.get("model_name") != "ganesh-mini-1.0"
    ):
        raise ValueError("release artifact manifest is invalid")
    if (
        export.get("schema_version") != "ganesh-mini-export-equivalence/v1"
        or export.get("status") != "passed"
        or export.get("artifact_manifest_sha256") != artifacts["manifest_sha256"]
    ):
        raise ValueError("export equivalence is invalid or unbound")
    manifest_check = next(
        (row for row in decision["checks"] if row.get("name") == "required_manifests_complete"),
        None,
    )
    accepted_seals = {
        row.get("seal")
        for row in (manifest_check or {}).get("evidence", {}).get("manifests", [])
        if row.get("passed") is True
    }
    if artifacts["manifest_sha256"] not in accepted_seals or export["evidence_sha256"] not in accepted_seals:
        raise ValueError("release decision does not bind the supplied artifact evidence")
    return decision, artifacts, export


def artifact_files(manifest: dict[str, Any]) -> list[tuple[str, Path, str, int]]:
    artifacts = manifest["artifacts"]
    merged = artifacts["merged_bf16_hf"]
    merged_root = Path(merged["path"])
    if not merged_root.is_absolute():
        merged_root = ROOT / merged_root
    files: list[tuple[str, Path, str, int]] = []
    observed_inventory = []
    for row in merged["files"]:
        path = merged_root / row["path"]
        digest = file_sha256(path) if path.is_file() else None
        if digest != row["sha256"] or path.stat().st_size != row["bytes"]:
            raise ValueError(f"merged artifact file mismatch: {path}")
        observed_inventory.append(row)
        files.append((row["path"], path, digest, row["bytes"]))
    if canonical_sha256(observed_inventory) != merged.get("sha256"):
        raise ValueError("merged artifact aggregate hash mismatch")
    for key, remote in (("gguf_f16", "gguf/ganesh-mini-1.0-f16.gguf"), ("gguf_q8", "gguf/ganesh-mini-1.0-q8_0.gguf")):
        row = artifacts[key]
        path = Path(row["path"])
        if not path.is_absolute():
            path = ROOT / path
        digest = file_sha256(path) if path.is_file() else None
        if digest != row["sha256"] or path.stat().st_size != row["bytes"]:
            raise ValueError(f"{key} artifact mismatch: {path}")
        files.append((remote, path, digest, row["bytes"]))
    remote_paths = [row[0] for row in files]
    if len(remote_paths) != len(set(remote_paths)):
        raise ValueError("duplicate Hugging Face destination path")
    return sorted(files)


def build_plan(
    *,
    repo_id: str,
    visibility: str,
    decision_path: Path,
    artifact_manifest_path: Path,
    export_equivalence_path: Path,
    model_card_path: Path,
    evidence_paths: list[Path],
) -> tuple[dict[str, Any], list[tuple[str, Path]]]:
    if visibility not in {"private", "public"}:
        raise ValueError("visibility must be private or public")
    if "/" not in repo_id or repo_id.startswith("/") or repo_id.endswith("/"):
        raise ValueError("repo_id must be a Hugging Face namespace/name")
    decision, artifacts, export = verified_release_inputs(
        decision_path, artifact_manifest_path, export_equivalence_path
    )
    expected_seals = expected_evidence_seals(decision)
    supplied: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in evidence_paths:
        value, field = load_any_sealed(path)
        seal = value[field]
        if seal in supplied:
            raise ValueError(f"duplicate release evidence seal: {seal}")
        supplied[seal] = (path, value)
    already_supplied = {artifacts["manifest_sha256"], export["evidence_sha256"]}
    required_extras = expected_seals - already_supplied
    if set(supplied) != required_extras:
        raise ValueError(
            f"release evidence closure mismatch; missing={sorted(required_extras - set(supplied))}, "
            f"unexpected={sorted(set(supplied) - required_extras)}"
        )
    if not model_card_path.is_file():
        raise FileNotFoundError(model_card_path)
    upload: list[tuple[str, Path]] = [("README.md", model_card_path)]
    file_rows = [{"path_in_repo": "README.md", "sha256": file_sha256(model_card_path), "bytes": model_card_path.stat().st_size}]
    for remote, local, digest, size in artifact_files(artifacts):
        upload.append((remote, local))
        file_rows.append({"path_in_repo": remote, "sha256": digest, "bytes": size})
    for remote, local, seal in (
        ("evidence/release-decision.json", decision_path, decision["evidence_sha256"]),
        ("evidence/release-artifacts.json", artifact_manifest_path, artifacts["manifest_sha256"]),
        ("evidence/export-equivalence.json", export_equivalence_path, export["evidence_sha256"]),
    ):
        upload.append((remote, local))
        file_rows.append({"path_in_repo": remote, "sha256": file_sha256(local), "bytes": local.stat().st_size, "seal": seal})
    for seal, (local, value) in sorted(supplied.items()):
        remote = evidence_remote_path(value, seal)
        upload.append((remote, local))
        file_rows.append({"path_in_repo": remote, "sha256": file_sha256(local), "bytes": local.stat().st_size, "seal": seal})
    remote_paths = [remote for remote, _ in upload]
    if len(remote_paths) != len(set(remote_paths)):
        raise ValueError("duplicate Hugging Face destination path across release inputs")
    plan = {
        "schema_version": "ganesh-mini-huggingface-publication-plan/v1",
        "status": "ready",
        "repo_id": repo_id,
        "visibility": visibility,
        "revision": "main",
        "tag": "v1.0",
        "release_decision_sha256": decision["evidence_sha256"],
        "artifact_manifest_sha256": artifacts["manifest_sha256"],
        "export_equivalence_sha256": export["evidence_sha256"],
        "files": sorted(file_rows, key=lambda row: row["path_in_repo"]),
    }
    plan["plan_sha256"] = canonical_sha256(plan)
    return plan, upload


def publish(plan: dict[str, Any], upload: list[tuple[str, Path]], *, allow_existing: bool) -> dict[str, Any]:
    from huggingface_hub import CommitOperationAdd, HfApi

    api = HfApi()
    repo_id = plan["repo_id"]
    api.create_repo(
        repo_id=repo_id,
        repo_type="model",
        private=plan["visibility"] == "private",
        exist_ok=allow_existing,
    )
    commit = api.create_commit(
        repo_id=repo_id,
        repo_type="model",
        revision="main",
        commit_message="Publish ganesh-mini-1.0",
        operations=[CommitOperationAdd(path_in_repo=remote, path_or_fileobj=str(local)) for remote, local in upload],
    )
    api.create_tag(repo_id=repo_id, tag=plan["tag"], revision=commit.oid, repo_type="model", exist_ok=False)
    info = api.repo_info(repo_id=repo_id, repo_type="model", revision=commit.oid, files_metadata=False)
    observed = {item.rfilename for item in info.siblings}
    expected = {row["path_in_repo"] for row in plan["files"]}
    if not expected.issubset(observed):
        raise RuntimeError(f"published repository is missing files: {sorted(expected - observed)}")
    report = {
        "schema_version": "ganesh-mini-huggingface-publication/v1",
        "status": "published",
        "repo_id": repo_id,
        "visibility": plan["visibility"],
        "commit_oid": commit.oid,
        "commit_url": commit.commit_url,
        "tag": plan["tag"],
        "plan_sha256": plan["plan_sha256"],
        "published_paths": sorted(expected),
    }
    report["evidence_sha256"] = canonical_sha256(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-id", required=True)
    parser.add_argument("--visibility", choices=("private", "public"), required=True)
    parser.add_argument("--release-decision", type=Path, required=True)
    parser.add_argument("--artifact-manifest", type=Path, required=True)
    parser.add_argument("--export-equivalence", type=Path, required=True)
    parser.add_argument("--model-card", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--allow-existing", action="store_true")
    args = parser.parse_args()
    plan, upload = build_plan(
        repo_id=args.repo_id,
        visibility=args.visibility,
        decision_path=args.release_decision,
        artifact_manifest_path=args.artifact_manifest,
        export_equivalence_path=args.export_equivalence,
        model_card_path=args.model_card,
        evidence_paths=args.evidence,
    )
    report = publish(plan, upload, allow_existing=args.allow_existing) if args.execute else plan
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
