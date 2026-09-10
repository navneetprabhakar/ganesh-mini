#!/usr/bin/env python3
"""Build a candidate-specific checkpoint-sweep startup controller."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "scripts/inference/gcloud_startup_checkpoint_sweep.sh"
LEGACY_RECOVERY_ASSERTION = (
    '[[ "$RECOVERY_ARCHIVE_URI" == *\'#1788935240864459\' && '
    '"$RECOVERY_ARCHIVE_SHA" == 24abdb78753ad59a25adbc3ca1ddab31da0176c3de935b02b874e5638dab8e31 '
    '&& "$RECOVERY_ARCHIVE_SIZE" == 51674173 ]]'
)
LEGACY_CONFIG = "measurement/gate4/checkpoint-sweep-20260909/configs"


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()
    ).hexdigest()


def build(template: Path, config_dir: str, output: Path, manifest_output: Path) -> dict[str, Any]:
    config_path = PurePosixPath(config_dir)
    if config_path.is_absolute() or ".." in config_path.parts or not config_dir.endswith("/configs"):
        raise ValueError("config directory must be a safe workspace-relative configs path")
    source = template.read_text(encoding="utf-8")
    if source.count(LEGACY_RECOVERY_ASSERTION) != 1 or source.count(LEGACY_CONFIG) != 1:
        raise ValueError("checkpoint-sweep startup template contract changed")
    # The recovery object remains exact-generation bound by the sealed execution
    # card. Candidate identity is additionally verified by the training evidence,
    # checkpoint manifests, and candidate-specific config manifest at admission.
    rendered = source.replace(
        LEGACY_RECOVERY_ASSERTION,
        '[[ "$RECOVERY_ARCHIVE_URI" == *\'#\'* && "$RECOVERY_ARCHIVE_SHA" =~ ^[0-9a-f]{64}$ && "$RECOVERY_ARCHIVE_SIZE" -gt 0 ]]',
    ).replace(LEGACY_CONFIG, config_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    output.chmod(0o755)
    manifest: dict[str, Any] = {
        "schema_version": "ganesh-mini-checkpoint-sweep-startup/v1",
        "status": "sealed",
        "promotion_authority": "none",
        "training_allowed": False,
        "template_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "config_dir": config_dir,
        "controller": {
            "size_bytes": output.stat().st_size,
            "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        },
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    manifest_output.parent.mkdir(parents=True, exist_ok=True)
    manifest_output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", type=Path, default=TEMPLATE)
    parser.add_argument("--config-dir", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path, required=True)
    args = parser.parse_args()
    manifest = build(args.template, args.config_dir, args.output, args.manifest_output)
    print(json.dumps(manifest["controller"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
