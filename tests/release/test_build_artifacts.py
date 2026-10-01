import hashlib
import json
from pathlib import Path

import pytest

from scripts.release.build_artifacts import (
    QWEN_MODEL_ID,
    QWEN_REVISION,
    GGUF_TARGET_FLAGS,
    canonical_sha256,
    validate_base_model,
    validate_selected_run,
    save_optional_processor,
)


def test_release_base_model_is_bound_to_pinned_inventory_and_readiness(tmp_path: Path) -> None:
    model = tmp_path / "model"
    model.mkdir()
    weights = model / "weights.bin"
    weights.write_bytes(b"pinned")
    inventory = {
        "model_id": QWEN_MODEL_ID,
        "revision": QWEN_REVISION,
        "files": [{
            "path": "weights.bin",
            "size": weights.stat().st_size,
            "sha256": hashlib.sha256(weights.read_bytes()).hexdigest(),
        }],
    }
    inventory_path = tmp_path / "inventory.json"
    inventory_path.write_text(json.dumps(inventory))
    readiness = {
        "status": "ready",
        "failed_checks": [],
        "model_id": QWEN_MODEL_ID,
        "revision": QWEN_REVISION,
        "inventory_sha256": canonical_sha256(inventory),
    }
    readiness["report_sha256"] = canonical_sha256(readiness)
    readiness_path = tmp_path / "readiness.json"
    readiness_path.write_text(json.dumps(readiness))

    identity = validate_base_model(model, inventory_path, readiness_path)
    assert identity["revision"] == QWEN_REVISION
    assert identity["readiness_report_sha256"] == readiness["report_sha256"]

    weights.write_bytes(b"changed")
    with pytest.raises(ValueError, match="pinned inventory"):
        validate_base_model(model, inventory_path, readiness_path)


def test_release_adapter_requires_complete_v2_run_and_exact_hashes(tmp_path: Path) -> None:
    adapter = tmp_path / "adapter"
    adapter.mkdir()
    weights = adapter / "adapter_model.safetensors"
    weights.write_bytes(b"adapter")
    run = {
        "schema_version": "ganesh-mini-sft-run/v2",
        "status": "complete",
        "identities": {"model_revision": QWEN_REVISION},
        "save_reload": {"passed": True},
        "adapter_files": {"adapter_model.safetensors": hashlib.sha256(weights.read_bytes()).hexdigest()},
    }
    run["evidence_sha256"] = canonical_sha256(run)
    path = tmp_path / "run.json"
    path.write_text(json.dumps(run))
    assert validate_selected_run(path, adapter)["evidence_sha256"] == run["evidence_sha256"]

    run["schema_version"] = "ganesh-mini-sft-run/v1"
    run.pop("evidence_sha256")
    run["evidence_sha256"] = canonical_sha256(run)
    path.write_text(json.dumps(run))
    with pytest.raises(ValueError, match="repaired-recipe"):
        validate_selected_run(path, adapter)


def test_text_only_merge_skips_missing_optional_processor_backend(tmp_path: Path) -> None:
    class MissingVisionBackend:
        @staticmethod
        def from_pretrained(*args: object, **kwargs: object) -> object:
            raise ImportError("torchvision and Pillow are unavailable")

    assert save_optional_processor(MissingVisionBackend, tmp_path, tmp_path) is False


def test_target_gguf_does_not_advertise_missing_speculative_mtp_layer() -> None:
    assert GGUF_TARGET_FLAGS == ("--no-mtp",)
