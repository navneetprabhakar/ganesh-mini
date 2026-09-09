import pytest

from scripts.train.qwen_runtime import configure_cuda_allocator
from scripts.train.run_sft import RollingLossGuard, bounded_training_wall, five_family_validation, initialize_cuda_measurement, planned_end, select_lora_targets, summarize_validation


def row(tokens: int) -> dict:
    return {"attention_mask":[1]*tokens}


def test_lr_budget_extends_to_complete_accumulation_boundary() -> None:
    rows=[row(10) for _ in range(20)]
    assert planned_end(rows,55,8)==8


def test_full_schedule_keeps_nondivisible_final_batch() -> None:
    rows=[row(10) for _ in range(11)]
    assert planned_end(rows,110,8)==11


def test_validation_macro_counts_javascript_and_typescript_as_one_family() -> None:
    result=five_family_validation({
        "go":[1.0],"java":[2.0],"javascript":[3.0],"typescript":[5.0],"python":[6.0],"rust":[7.0]
    })
    assert result["javascript_typescript_family_mean"]==4.0
    assert result["five_family_macro_mean"]==4.0


def test_validation_macro_fails_closed_when_a_lane_is_empty() -> None:
    with pytest.raises(RuntimeError,match="every frozen lane"):
        five_family_validation({
            "go":[1.0],"java":[2.0],"javascript":[3.0],"typescript":[],"python":[6.0],"rust":[7.0]
        })


def test_training_wall_reserves_finalization_from_both_bounds() -> None:
    assert bounded_training_wall(21600,10000)==9400
    assert bounded_training_wall(5000,10000)==4400


def test_training_wall_rejects_an_envelope_too_small_to_finalize() -> None:
    with pytest.raises(RuntimeError,match="insufficient training and finalization"):
        bounded_training_wall(650,10000)


def test_production_sft_allocator_contract_is_process_wide(monkeypatch) -> None:
    monkeypatch.delenv("PYTORCH_CUDA_ALLOC_CONF", raising=False)
    evidence=configure_cuda_allocator("expandable_segments:True")
    assert evidence["environment_variable"]=="PYTORCH_CUDA_ALLOC_CONF"
    assert evidence["value"]=="expandable_segments:True"


def test_cuda_measurement_initializes_selected_device_before_reset() -> None:
    calls=[]

    class FakeCuda:
        def set_device(self, device) -> None: calls.append(("set_device",device))
        def init(self) -> None: calls.append(("init",))
        def reset_peak_memory_stats(self) -> None: calls.append(("reset_peak_memory_stats",))

    class FakeTorch:
        cuda=FakeCuda()

        @staticmethod
        def device(value):
            calls.append(("device",value))
            return f"selected:{value}"

    selected=initialize_cuda_measurement(FakeTorch())
    assert selected=="selected:cuda:0"
    assert calls==[
        ("device","cuda:0"),
        ("set_device","selected:cuda:0"),
        ("init",),
        ("reset_peak_memory_stats",),
    ]


def test_conservative_target_policy_covers_only_attention_in_last_eight_layers() -> None:
    class Linear: pass
    modules=[]
    for layer in range(24):
        attention="self_attn" if layer%4==3 else "linear_attn"
        names=("q_proj","k_proj","v_proj","o_proj") if attention=="self_attn" else ("in_proj_qkv","in_proj_z","in_proj_a","in_proj_b","out_proj")
        modules.extend((f"model.language_model.layers.{layer}.{attention}.{name}",Linear()) for name in names)
        modules.append((f"model.language_model.layers.{layer}.mlp.down_proj",Linear()))
    policy={"scope":"last-n-attention-projections","model_layer_count":24,"layer_count":8,"full_attention_projections":["q_proj","v_proj"],"linear_attention_projections":["in_proj_qkv","out_proj"],"mlp_projections":[]}
    selected=select_lora_targets(modules,Linear,{"target_policy":policy})
    assert len(selected)==16
    assert all(16<=int(name.split(".")[3])<=23 for name in selected)
    assert not any("mlp" in name or "in_proj_z" in name or "k_proj" in name or "o_proj" in name for name in selected)


def test_capacity_policy_covers_all_attention_and_last_eight_mlps() -> None:
    class Linear: pass
    modules=[]
    for layer in range(24):
        attention="self_attn" if layer%4==3 else "linear_attn"
        names=("q_proj","k_proj","v_proj","o_proj") if attention=="self_attn" else ("in_proj_qkv","in_proj_z","in_proj_a","in_proj_b","out_proj")
        modules.extend((f"model.language_model.layers.{layer}.{attention}.{name}",Linear()) for name in names)
        modules.extend((f"model.language_model.layers.{layer}.mlp.{name}",Linear()) for name in ("gate_proj","up_proj","down_proj"))
    policy={"scope":"all-attention-plus-last-n-mlp","model_layer_count":24,"layer_count":8,"full_attention_projections":["q_proj","v_proj"],"linear_attention_projections":["in_proj_qkv","out_proj"],"mlp_projections":["gate_proj","up_proj","down_proj"]}
    selected=select_lora_targets(modules,Linear,{"target_policy":policy})
    assert len(selected)==72
    assert sum(".mlp." in name for name in selected)==24
    assert all(int(name.split(".")[3])>=16 for name in selected if ".mlp." in name)
    assert {int(name.split(".")[3]) for name in selected if ".self_attn." in name or ".linear_attn." in name}==set(range(24))
    assert not any("in_proj_z" in name or "k_proj" in name or "o_proj" in name for name in selected)


def test_robust_guard_uses_optimizer_groups_and_persists_trigger_evidence() -> None:
    contract={"warmup_optimizer_steps":4,"rolling_window_optimizer_steps":4,"minimum_history_optimizer_steps":4,"robust_z_threshold":8.0,"minimum_median_ratio":3.0,"mad_floor":1e-6,"consecutive_optimizer_groups":3}
    guard=RollingLossGuard(contract)
    assert not any(guard.observe(value)["triggered"] for value in (1.0,1.1,0.9,1.0))
    first=guard.observe(4.0); second=guard.observe(4.1); third=guard.observe(4.2)
    assert first["spike"] and first["streak"]==1
    assert second["spike"] and second["streak"]==2
    assert third["triggered"] and third["streak"]==3


def test_validation_diagnostic_reports_comparable_token_and_record_means() -> None:
    rows={lane:[{"loss":1.0,"response_tokens":1.0},{"loss":3.0,"response_tokens":3.0}] for lane in ("go","java","javascript","typescript","python","rust")}
    result=summarize_validation(rows)
    assert result["record_mean"]["five_family_macro_mean"]==2.0
    assert result["supervised_token_mean"]["five_family_macro_mean"]==2.5
