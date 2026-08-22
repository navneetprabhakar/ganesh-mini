import json
from pathlib import Path

import pytest

from scripts.cuda.qualify import (
    FALLBACK_RECIPE,
    PRIMARY_RECIPE,
    canonical_sha256,
    append_journal,
    load_and_validate_config,
    select_records,
    write_evidence,
)

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "configs/cuda/qwen3_5_2b_gate0.json"


def test_pinned_primary_and_fallback_validate() -> None:
    config = load_and_validate_config(CONFIG, ROOT)
    assert config["qualification_order"] == [PRIMARY_RECIPE, FALLBACK_RECIPE]
    primary = config["recipes"][PRIMARY_RECIPE]
    assert primary["minimum_vram_bytes"] == 24 * 1024**3
    assert primary["quantization"] is None
    assert primary["sequence_length"] == 4096
    assert (primary["micro_batch_size"], primary["rank"], primary["alpha"], primary["dropout"]) == (1, 32, 64, 0.05)
    assert primary["gradient_checkpointing"] and primary["response_only"]
    fallback = config["recipes"][FALLBACK_RECIPE]
    assert fallback["quantization"] == {"bits": 4, "type": "nf4", "double_quantization": True, "compute_dtype": "bfloat16"}
    assert config["packages"]["bitsandbytes"] == "0.49.2"


def test_primary_recipe_mutation_fails_closed(tmp_path: Path) -> None:
    source = json.loads(CONFIG.read_text())
    source["recipes"][PRIMARY_RECIPE]["rank"] = 16
    path = tmp_path / "config.json"
    path.write_text(json.dumps(source))
    with pytest.raises(ValueError, match="primary recipe changed"):
        load_and_validate_config(path, ROOT)


def test_budget_increase_fails_closed(tmp_path: Path) -> None:
    source = json.loads(CONFIG.read_text())
    source["budget"]["maximum_usd"] = 5.01
    path = tmp_path / "config.json"
    path.write_text(json.dumps(source))
    with pytest.raises(ValueError, match="authorized bound"):
        load_and_validate_config(path, ROOT)


def test_write_evidence_seals_canonical_bytes(tmp_path: Path) -> None:
    path = tmp_path / "evidence.json"
    write_evidence({"status": "failed", "reason": "no GPU"}, path)
    value = json.loads(path.read_text()); claimed = value.pop("evidence_sha256")
    assert claimed == canonical_sha256(value)


def test_journal_appends_durable_json_lines(tmp_path: Path) -> None:
    path = tmp_path / "qualification.journal.jsonl"
    append_journal(path, {"phase": "identity", "state": "started"})
    append_journal(path, {"phase": "identity", "state": "completed"})
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    assert [row["state"] for row in rows] == ["started", "completed"]
    assert all(row["recorded_at"] for row in rows)


class FakeTokenizer:
    def apply_chat_template(self, messages, *, tokenize, add_generation_prompt):
        assert not add_generation_prompt
        return messages[-1]["content"]

    def __call__(self, rendered, *, add_special_tokens):
        assert not add_special_tokens
        return type("Tokens", (), {"input_ids": rendered.split()})()


def test_record_selection_is_length_stratified(tmp_path: Path) -> None:
    path = tmp_path / "records.jsonl"
    rows = [
        {"id": "b", "messages": [{"role": "assistant", "content": "one two three"}]},
        {"id": "c", "messages": [{"role": "assistant", "content": "one two"}]},
        {"id": "a", "messages": [{"role": "assistant", "content": "one"}]},
    ]
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))
    selected = select_records(path, FakeTokenizer(), 2, 4096)
    assert [item["row"]["id"] for item in selected] == ["a", "b"]


def test_runner_defaults_primary_and_guards_fallback_order() -> None:
    runner = (ROOT / "scripts/cuda/run_qualification.sh").read_text()
    assert 'recipe="${4:-bf16-lora-primary-v1}"' in runner
    assert "GANESH_PRIMARY_QUALIFICATION_EVIDENCE" in runner
    assert '--recipe "$recipe"' in runner


def test_gpu_startup_is_prebuilt_generation_pinned_and_offline() -> None:
    startup = (ROOT / "scripts/cuda/gcloud_startup_gate0b.sh").read_text()
    assert "GANESH_IMAGE_ARCHIVE_URI" in startup
    assert startup.count("must include a GCS generation") == 1
    assert "download_verified" in startup
    assert "WORKSPACE_ARCHIVE_SHA256" in startup and "MODEL_ARCHIVE_SHA256" in startup
    assert "DOCKER_BUNDLE_SHA256" in startup
    assert "docker load" in startup
    assert "apt-get" not in startup
    assert "docker build" not in startup
    assert "docker pull" not in startup
    assert "nvidia-ctk runtime configure --runtime=docker" in startup


def test_runner_requires_exact_preloaded_image_and_disables_pull_and_network() -> None:
    runner = (ROOT / "scripts/cuda/run_qualification.sh").read_text()
    assert "GANESH_CUDA_IMAGE_ID" in runner
    assert "docker build" not in runner
    assert "--pull=never" in runner
    assert "--network none" in runner


def test_cpu_prebuild_has_a_hard_deadline_and_seals_oci_archive() -> None:
    prebuild = (ROOT / "scripts/cuda/prebuild_cuda_image.sh").read_text()
    startup = (ROOT / "scripts/cuda/gcloud_prebuild_gate0b.sh").read_text()
    assert "3600" in prebuild and "timeout --signal=TERM" in prebuild
    assert "docker save" in prebuild and "cuda-image.docker.tar.zst.sha256" in prebuild
    assert 'docker_package_version="29.1.3-0ubuntu3~22.04.2"' in startup
    assert "--download-only" in startup
    assert "base-dpkg-packages.tsv" in startup and "bundle-files.sha256" in startup
    assert "prebuild-manifest.json" in startup


def test_cuda_dockerfile_does_not_require_optional_buildx_component() -> None:
    dockerfile = (ROOT / "containers/cuda/Dockerfile").read_text()
    assert "--mount=type=cache" not in dockerfile
    assert "uv sync --frozen" in dockerfile


def test_docker_context_excludes_models_and_measurement_archives() -> None:
    ignore = (ROOT / ".dockerignore").read_text().splitlines()
    assert ignore[0] == "**"
    assert "!pyproject.toml" in ignore and "!uv.lock" in ignore
    assert all("models" not in row and "measurement" not in row for row in ignore[1:])


def test_execution_card_never_claims_executed_evidence() -> None:
    card = json.loads((ROOT / "measurement/cuda/execution_card.json").read_text())
    assert card["status"] == "not_ready"
    assert card["gcloud_inspected_or_used"] is False
    assert card["execution"]["maximum_cost_usd"] <= 5
    assert card["provider_discovery"]["secret_values_inspected"] is False
    assert card["qualification_order"] == [PRIMARY_RECIPE, FALLBACK_RECIPE]
