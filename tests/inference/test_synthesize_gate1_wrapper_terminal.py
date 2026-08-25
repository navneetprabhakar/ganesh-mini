from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.inference.synthesize_gate1_wrapper_terminal import canonical_sha256, synthesize


PREFIX = "gs://bucket/run/wrapper-failure-attempt"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture(tmp_path: Path, code: str = "40\n") -> tuple[Path, Path, Path]:
    root = tmp_path / "wrapper"
    root.mkdir()
    controller_hash = "a" * 64
    wrapper_hash = "b" * 64
    (root / "bootstrap-files.sha256").write_text(
        f"{wrapper_hash}  /startup.sh\n{controller_hash}  /controller.sh\n"
    )
    (root / "controller-exit-code.txt").write_text(code)
    (root / "controller.stderr.log").write_text("invalid attempt id\n")
    (root / "controller.stdout.log").write_text("")
    objects = [
        {
            "object_uri": f"{PREFIX}/{path.name}",
            "downloaded_sha256": sha(path),
            "verified": True,
        }
        for path in sorted(root.iterdir())
    ]
    manifest = {
        "schema_version": "ganesh-mini-gcs-backup-manifest/v1",
        "status": "verified",
        "prefix": PREFIX,
        "object_count": len(objects),
        "objects": objects,
    }
    manifest["evidence_sha256"] = canonical_sha256(manifest)
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))
    card = {
        "schema_version": "ganesh-mini-staged-gcloud-execution/v1",
        "status": "authorized-executable",
        "launch": {
            "controller": {"sha256": controller_hash},
            "metadata_wrapper": {"sha256": wrapper_hash},
        },
    }
    card["execution_sha256"] = canonical_sha256(card)
    card_path = tmp_path / "card.json"
    card_path.write_text(json.dumps(card))
    return root, manifest_path, card_path


def test_synthesizes_exact_deletion_only_terminal_inventory(tmp_path: Path) -> None:
    root, manifest, card = fixture(tmp_path)
    output = tmp_path / "terminal"
    synthesize(manifest, root, card, output)
    assert (output / "startup-exit-code.txt").read_text() == "40\n"
    rows = (output / "runtime-files.sha256").read_text().splitlines()
    assert len(rows) == 6
    assert all("runtime-files.sha256" not in row for row in rows)
    assert {path.name for path in output.iterdir()} == {
        "bootstrap-files.sha256",
        "controller-exit-code.txt",
        "controller.stderr.log",
        "controller.stdout.log",
        "execution-card.json",
        "startup-exit-code.txt",
        "runtime-files.sha256",
    }


def test_rejects_zero_exit(tmp_path: Path) -> None:
    root, manifest, card = fixture(tmp_path, code="0\n")
    with pytest.raises(ValueError, match="nonzero exit"):
        synthesize(manifest, root, card, tmp_path / "terminal")


def test_rejects_wrapper_download_drift(tmp_path: Path) -> None:
    root, manifest, card = fixture(tmp_path)
    (root / "controller.stderr.log").write_text("changed\n")
    with pytest.raises(ValueError, match="absent or mismatched"):
        synthesize(manifest, root, card, tmp_path / "terminal")


def test_rejects_bootstrap_not_bound_to_card(tmp_path: Path) -> None:
    root, manifest, card = fixture(tmp_path)
    value = json.loads(card.read_text())
    value.pop("execution_sha256")
    value["launch"]["controller"]["sha256"] = "c" * 64
    value["execution_sha256"] = canonical_sha256(value)
    card.write_text(json.dumps(value))
    with pytest.raises(ValueError, match="does not bind"):
        synthesize(manifest, root, card, tmp_path / "terminal")
