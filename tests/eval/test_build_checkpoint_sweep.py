import json
from pathlib import Path

import pytest

from scripts.eval.build_checkpoint_sweep import build, canonical_digest
from scripts.eval.contracts import sha256_object


def sealed(value: dict, field: str) -> dict:
    value[field] = canonical_digest(value)
    return value


def fixture(tmp_path: Path, count: int = 6) -> tuple[Path, Path]:
    identities = {"card_sha256": "a" * 64, "recipe_sha256": "b" * 64}
    run = sealed({"status": "complete", "identities": identities}, "evidence_sha256")
    run_path = tmp_path / "run-evidence.json"
    run_path.write_text(json.dumps(run))
    checkpoints = tmp_path / "checkpoints"
    for index in range(count):
        directory = checkpoints / f"tokens-{index + 1:012d}"
        directory.mkdir(parents=True)
        manifest = sealed({"status": "complete", "identities": identities, "files": []}, "manifest_sha256")
        (directory / "manifest.json").write_text(json.dumps(manifest))
    return run_path, checkpoints


def test_builds_five_unmeasured_checkpoint_configs(tmp_path: Path) -> None:
    run, checkpoints = fixture(tmp_path)

    configs, manifest = build(run, checkpoints, Path("/training"))

    assert len(configs) == 5
    assert manifest["status"] == "diagnostic-only"
    assert manifest["promotion_authority"] == "none"
    assert manifest["measured_final_checkpoint"] == "tokens-000000000006"
    assert all(config["adapter"]["checkpoint_manifest"].startswith("/training/checkpoints/") for _, config in configs)


def test_binds_explicit_served_model_prefix(tmp_path: Path) -> None:
    run, checkpoints = fixture(tmp_path)

    configs, _ = build(
        run,
        checkpoints,
        Path("/training"),
        "ganesh-mini-1.0-lane-stratified-v3",
    )

    assert all(
        config["adapter"]["served_model_id"].startswith(
            "ganesh-mini-1.0-lane-stratified-v3-tokens-"
        )
        for _, config in configs
    )


def test_rejects_invalid_served_model_prefix(tmp_path: Path) -> None:
    run, checkpoints = fixture(tmp_path)

    with pytest.raises(ValueError, match="lowercase identifier"):
        build(run, checkpoints, Path("/training"), "Ganesh Mini v3")


def test_rejects_missing_checkpoint(tmp_path: Path) -> None:
    run, checkpoints = fixture(tmp_path, count=5)

    with pytest.raises(ValueError, match="expected six"):
        build(run, checkpoints, Path("/training"))


def test_rejects_checkpoint_from_other_training_run(tmp_path: Path) -> None:
    run, checkpoints = fixture(tmp_path)
    path = sorted(checkpoints.glob("tokens-*/manifest.json"))[0]
    manifest = json.loads(path.read_text())
    manifest.pop("manifest_sha256")
    manifest["identities"] = {"card_sha256": "c" * 64, "recipe_sha256": "b" * 64}
    path.write_text(json.dumps(sealed(manifest, "manifest_sha256")))

    with pytest.raises(ValueError, match="does not bind"):
        build(run, checkpoints, Path("/training"))


def test_checkpoint_sweep_uses_project_utf8_canonicalization() -> None:
    value = {"diagnostic": "entrée"}

    assert canonical_digest(value) == sha256_object(value)
