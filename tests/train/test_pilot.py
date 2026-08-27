from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts/train/pilot.py"
SPEC = importlib.util.spec_from_file_location("training_pilot", MODULE_PATH)
assert SPEC and SPEC.loader
pilot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pilot)


def write_sealed(path: Path, value: dict, digest_field: str) -> dict:
    sealed = dict(value)
    sealed[digest_field] = pilot.canonical_sha256(sealed)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sealed), encoding="utf-8")
    return sealed


@pytest.fixture
def project(tmp_path: Path) -> tuple[Path, Path]:
    for relative in (
        "configs/train/seed_pilot.json",
        "configs/model/qwen3_5_2b.contract.json",
        "configs/data/ganesh_v01_seed.json",
        "manifests/datasets/ganesh_v01_seed.json",
        "data/seed/ganesh_v01/train.jsonl",
        "data/seed/ganesh_v01/validation.jsonl",
    ):
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)

    config_path = tmp_path / "configs/train/seed_pilot.json"
    config = json.loads(config_path.read_text())
    config["control"]["maximum_seen_tokens"] = 112
    config_path.write_text(json.dumps(config), encoding="utf-8")
    model = config["model"]
    template_sha = "b" * 64
    gate0_checks = [
        {"name": name, "passed": True, "evidence": ({"sha256": template_sha} if name == "chat_template" else {})}
        for name in sorted(pilot.REQUIRED_GATE0_CHECKS)
    ]
    write_sealed(
        tmp_path / config["prerequisites"]["gate0_report_path"],
        {
            "gate": 0,
            "status": "ready",
            "model_id": model["model_id"],
            "revision": model["revision"],
            "checks": gate0_checks,
            "failed_checks": [],
        },
        "report_sha256",
    )
    write_sealed(
        tmp_path / config["prerequisites"]["gate1_report_path"],
        {"gate": 1, "status": "ready", "model_id": model["model_id"], "revision": model["revision"], "evaluation_contract_frozen": True, "base_baseline_complete": True, "decision_prompts_exposed": False},
        "evidence_sha256",
    )
    write_sealed(
        tmp_path / config["prerequisites"]["gate2_report_path"],
        {"gate": 2, "status": "ready", "model_id": model["model_id"], "revision": model["revision"], "seed_manifest_sha256": config["data"]["source_manifest_sha256"], "train_sha256": config["data"]["train_sha256"], "validation_sha256": config["data"]["validation_sha256"], "compatibility_passed": True, "evaluation_overlap_passed": True},
        "evidence_sha256",
    )
    prepared_path = tmp_path / "artifacts/train/seed-pilot/prepared-train.jsonl"
    prepared_path.parent.mkdir(parents=True, exist_ok=True)
    token_counts = {"go": 20, "java": 20, "javascript": 10, "typescript": 10, "python": 20, "rust": 20}
    rows = []
    for lane, response_count in token_counts.items():
        input_ids = [1, 2] + list(range(10, 10 + response_count))
        rows.append(json.dumps({"id": f"record-{lane}", "lane": lane, "input_ids": input_ids, "labels": [-100, -100] + input_ids[2:], "prompt_token_count": 2, "rendered_prompt_sha256": "c" * 64}))
    prepared_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    validation_path = tmp_path / "artifacts/train/seed-pilot/prepared-validation.jsonl"
    validation_rows = []
    for index in range(50):
        lane = pilot.LANES[index % len(pilot.LANES)]
        validation_rows.append(json.dumps({"id":f"validation-{index}","lane":lane,"input_ids":[1,2,3],"attention_mask":[1,1,1],"labels":[-100,-100,3],"prompt_token_count":2,"rendered_prompt_sha256":"d"*64}))
    validation_path.write_text("\n".join(validation_rows) + "\n", encoding="utf-8")
    write_sealed(
        tmp_path / config["data"]["prepared_manifest_path"],
        {
            "passed": True,
            "model_id": model["model_id"],
            "revision": model["revision"],
            "train_sha256": config["data"]["train_sha256"],
            "validation_sha256": config["data"]["validation_sha256"],
            "rendering": {
                "chat_template_source": "chat_template.jinja",
                "chat_template_sha256": template_sha,
                "upstream_tokenizer_applied": True,
                "add_generation_prompt": False,
                "response_only_labels_verified": True,
                "prompt_label_id": -100,
                "vision_token_count": 0,
            },
            "prepared_train_path": "artifacts/train/seed-pilot/prepared-train.jsonl",
            "prepared_train_sha256": pilot.file_sha256(prepared_path),
            "prepared_train_records": 6,
            "prepared_train_input_tokens": 112,
            "prepared_validation_path": "artifacts/train/seed-pilot/prepared-validation.jsonl",
            "prepared_validation_sha256": pilot.file_sha256(validation_path),
            "prepared_validation_records": 50,
            "sampled_response_tokens_by_lane": token_counts,
            "effective_epochs_by_lane": {lane: 2.5 for lane in pilot.LANES},
        },
        "manifest_sha256",
    )
    return tmp_path, config_path


def test_repository_config_is_ready_after_gate1_admission() -> None:
    card = pilot.build_execution_card(ROOT / "configs/train/seed_pilot.json", ROOT, system="Linux")
    assert card["status"] == "ready"
    assert card["failed_checks"] == []
    assert len(card["card_sha256"]) == 64


def test_repository_linux_pilot_binds_all_ready_gate_evidence() -> None:
    card = pilot.build_execution_card(ROOT / "configs/train/seed_pilot.json", ROOT, system="Linux")
    assert card["status"] == "ready"
    assert card["failed_checks"] == []
    assert card["prerequisite_evidence"]["gate0"] == json.loads((ROOT / "measurement/gate0/readiness.json").read_text())["report_sha256"]
    assert card["prerequisite_evidence"]["gate1"] == json.loads((ROOT / "measurement/gate1/readiness.json").read_text())["evidence_sha256"]
    assert card["prerequisite_evidence"]["gate2"] == json.loads((ROOT / "measurement/gate2/readiness.json").read_text())["report_sha256"]


def test_repository_v2_pilot_is_unique_weighted_and_conservative() -> None:
    card=pilot.build_execution_card(ROOT/"configs/train/seed_pilot_v2.json",ROOT,system="Linux")
    assert card["status"]=="ready",card["failed_checks"]
    recipe=card["selected_recipe"]
    assert recipe["recipe_id"]=="bf16-lora-conservative-v2"
    assert recipe["lora_rank"]==8
    assert recipe["learning_rate_candidates"]==[0.00001,0.00003]
    assert recipe["target_policy"]["scope"]=="last-n-attention-projections"
    assert card["budgets"]["maximum_seen_tokens"]==461235


def test_ready_card_binds_model_seed_rendering_balance_and_budget(project: tuple[Path, Path]) -> None:
    root, config_path = project
    card = pilot.build_execution_card(config_path, root, system="Linux")
    assert card["status"] == "ready", card["failed_checks"]
    assert card["model"]["revision"] == "15852e8c16360a2fea060d615a32b45270f8a8fc"
    assert card["strategy"]["selected_recipe_id"] == "bf16-lora-primary-v1"
    assert card["selected_recipe"]["base_loading"] == "bfloat16"
    assert "quantization_type" not in card["selected_recipe"]
    assert card["selected_recipe"]["compute_dtype"] == "bfloat16"
    assert card["selected_recipe"]["gradient_checkpointing"] is True
    assert card["selected_recipe"]["micro_batch_size"] == 1
    assert card["selected_recipe"]["vision_frozen"] is True
    assert card["selected_recipe"]["maximum_effective_epochs"] == 3.0
    unsigned = dict(card)
    claimed = unsigned.pop("card_sha256")
    assert pilot.canonical_sha256(unsigned) == claimed


def test_wrong_host_and_mutated_seed_fail_closed(project: tuple[Path, Path]) -> None:
    root, config_path = project
    with (root / "data/seed/ganesh_v01/train.jsonl").open("a", encoding="utf-8") as handle:
        handle.write("{}\n")
    with pytest.raises(pilot.PreflightError):
        pilot.build_execution_card(config_path, root, system="Darwin")


def test_response_only_and_half_family_proofs_are_required(project: tuple[Path, Path]) -> None:
    root, config_path = project
    config = json.loads(config_path.read_text())
    path = root / config["data"]["prepared_manifest_path"]
    manifest = json.loads(path.read_text())
    manifest.pop("manifest_sha256")
    manifest["rendering"]["response_only_labels_verified"] = False
    manifest["sampled_response_tokens_by_lane"]["javascript"] = 200
    write_sealed(path, manifest, "manifest_sha256")
    card = pilot.build_execution_card(config_path, root, system="Linux")
    assert card["status"] == "not_ready"
    assert "prepared_dataset" in card["failed_checks"]


def test_resume_is_hash_bound_and_epoch_capped(project: tuple[Path, Path]) -> None:
    root, config_path = project
    card = pilot.build_execution_card(config_path, root, system="Linux")
    checkpoint = {
        "schema_version": "ganesh-mini-training-checkpoint/v1",
        "run_id": card["run_id"],
        "selected_recipe_id": card["selected_recipe"]["recipe_id"],
        "selected_recipe_sha256": pilot.canonical_sha256(card["selected_recipe"]),
        "step": 100,
        "seen_tokens": 100,
        "effective_epochs_by_lane": {lane: 1.0 for lane in pilot.LANES},
        "checkpoint_path": "checkpoint-100",
        "checkpoint_sha256": "a" * 64,
        "config_sha256": card["inputs"]["config_sha256"],
        "dataset_manifest_sha256": card["inputs"]["prepared_manifest_sha256"],
        "created_at": "2026-08-22T00:00:00+00:00",
    }
    checkpoint = pilot.sealed(checkpoint, "evidence_sha256")
    pilot.validate_resume(checkpoint, card)
    checkpoint["effective_epochs_by_lane"]["rust"] = 3.1
    checkpoint = pilot.sealed({key: value for key, value in checkpoint.items() if key != "evidence_sha256"}, "evidence_sha256")
    with pytest.raises(pilot.PreflightError, match="effective epochs"):
        pilot.validate_resume(checkpoint, card)


def test_config_rejects_sequential_or_unbalanced_language_recipe(project: tuple[Path, Path]) -> None:
    root, config_path = project
    config = json.loads(config_path.read_text())
    config["data"]["family_token_targets"]["javascript"] = 0.2
    config["data"]["family_token_targets"]["typescript"] = 0.0
    config_path.write_text(json.dumps(config), encoding="utf-8")
    card = pilot.build_execution_card(config_path, root, system="Linux")
    assert card["status"] == "not_ready"
    assert "five_family_balance" in card["failed_checks"]


def test_nf4_fallback_without_primary_measurement_is_rejected(project: tuple[Path, Path]) -> None:
    root, config_path = project
    config = json.loads(config_path.read_text())
    config["strategy"] = {
        "selected_recipe_id": "nf4-qlora-fallback-v1",
        "fallback_reason": "primary_cuda_oom",
        "fallback_qualification_path": "artifacts/train/seed-pilot/fallback.json",
    }
    config_path.write_text(json.dumps(config), encoding="utf-8")
    card = pilot.build_execution_card(config_path, root, system="Linux")
    assert card["status"] == "not_ready"
    assert "fallback_qualified" in card["failed_checks"]


@pytest.mark.parametrize(
    ("reason", "measurements"),
    [
        ("primary_cuda_oom", {"cuda_oom_observed": True}),
        ("primary_peak_vram_exceeded", {"peak_vram_gb": 23.5}),
    ],
)
def test_nf4_fallback_requires_valid_sealed_primary_evidence(
    project: tuple[Path, Path], reason: str, measurements: dict
) -> None:
    root, config_path = project
    config = json.loads(config_path.read_text())
    evidence_path = root / "artifacts/train/seed-pilot/fallback.json"
    config["strategy"] = {
        "selected_recipe_id": "nf4-qlora-fallback-v1",
        "fallback_reason": reason,
        "fallback_qualification_path": "artifacts/train/seed-pilot/fallback.json",
    }
    config_path.write_text(json.dumps(config), encoding="utf-8")
    primary, fallback = config["recipes"]["primary"], config["recipes"]["fallback"]
    write_sealed(
        evidence_path,
        {
            "schema_version": "ganesh-mini-fallback-qualification/v1",
            "passed": True,
            "model_id": config["model"]["model_id"],
            "revision": config["model"]["revision"],
            "primary_recipe_id": primary["recipe_id"],
            "primary_recipe_sha256": pilot.canonical_sha256(primary),
            "fallback_recipe_id": fallback["recipe_id"],
            "fallback_recipe_sha256": pilot.canonical_sha256(fallback),
            "reason": reason,
            "primary_attempt": {
                "attempt_id": "primary-attempt-1",
                "observed_at": "2026-08-22T00:00:00+00:00",
                "measurement_source": {
                    "primary_cuda_oom": "cuda_runtime",
                    "primary_peak_vram_exceeded": "gpu_telemetry",
                }[reason],
                "measurement_sha256": "d" * 64,
            },
            "measurements": measurements,
        },
        "evidence_sha256",
    )
    card = pilot.build_execution_card(config_path, root, system="Linux")
    assert card["status"] == "ready", card["failed_checks"]
    assert card["selected_recipe"]["quantization_type"] == "nf4"


def test_qwen_template_prefix_is_used_for_response_only_labels() -> None:
    class Tokenizer:
        def apply_chat_template(self, messages: list[dict], **kwargs: object) -> object:
            if kwargs["tokenize"] is False:
                return "prompt" if kwargs["add_generation_prompt"] else "promptanswer"
            return {
                "input_ids": [10, 11]
                if kwargs["add_generation_prompt"]
                else [10, 11, 12, 13]
            }

    rendered = pilot.render_response_only(
        Tokenizer(),
        {"id": "x", "lane": "rust", "messages": [{"role": "user", "content": "task"}, {"role": "assistant", "content": "answer"}]},
    )
    assert rendered["labels"] == [-100, -100, 12, 13]
    assert rendered["prompt_token_count"] == 2
    assert rendered["response_token_count"] == 2


def test_non_prefix_generation_prompt_fails_closed() -> None:
    class Tokenizer:
        def apply_chat_template(self, messages: list[dict], **kwargs: object) -> object:
            if kwargs["tokenize"] is False:
                return "prompt" if kwargs["add_generation_prompt"] else "otheranswer"
            return {"input_ids": [1, 2] if kwargs["add_generation_prompt"] else [1, 3, 4]}

    with pytest.raises(pilot.PreflightError, match="not a token prefix"):
        pilot.render_response_only(
            Tokenizer(),
            {"id": "x", "lane": "go", "messages": [{"role": "user", "content": "task"}, {"role": "assistant", "content": "answer"}]},
        )
