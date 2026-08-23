from __future__ import annotations

import json
from pathlib import Path

from scripts.eval.verify_runtime_images import audit


def write_config(path: Path) -> None:
    path.write_text(json.dumps({
        "schema_version": "3.0", "platform": "linux/amd64",
        "runtimes": {"python": {
            "image": "python:test", "image_id": "sha256:" + "a" * 64,
            "manifest_digest": "sha256:" + "b" * 64,
            "rootfs_layers": ["sha256:" + "c" * 64], "platform": "linux/amd64",
        }},
    }))


def test_runtime_readiness_passes_only_exact_id_and_platform(tmp_path: Path) -> None:
    config = tmp_path / "runtimes.json"
    write_config(config)
    exact = json.dumps({
        "Id": "sha256:" + "b" * 64, "Os": "linux", "Architecture": "amd64",
        "Descriptor": {"digest": "sha256:" + "b" * 64, "annotations": {"config.digest": "sha256:" + "a" * 64}},
        "RootFS": {"Layers": ["sha256:" + "c" * 64]},
    })
    value = audit(config, lambda _tag: (0, exact, ""))
    assert value["status"] == "ready" and value["ready"] == 1


def test_runtime_readiness_reports_missing_or_wrong_images(tmp_path: Path) -> None:
    config = tmp_path / "runtimes.json"
    write_config(config)
    missing = audit(config, lambda _tag: (1, "", "not found"))
    assert missing["status"] == "blocked" and missing["ready"] == 0
    wrong = json.dumps({"Id": "sha256:" + "d" * 64, "Os": "linux", "Architecture": "arm64", "RootFS": {"Layers": []}})
    drift = audit(config, lambda _tag: (0, wrong, ""))
    assert drift["status"] == "blocked" and len(drift["failures"]) >= 2
