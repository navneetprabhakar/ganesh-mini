from decimal import Decimal
from pathlib import Path

import pytest

from scripts.campaign.run_host import (
    CONTAINER_ADAPTER,
    CONTAINER_CONTROL,
    CONTAINER_MODEL,
    CONTAINER_OUTPUT,
    CONTAINER_TRAINING,
    Campaign,
    canonical_sha256,
    docker_container_name,
    external_mount,
)


def test_canonical_campaign_seal_is_order_independent() -> None:
    assert canonical_sha256({"b": 2, "a": 1}) == canonical_sha256({"a": 1, "b": 2})


def test_campaign_uses_lowercase_docker_names_for_utc_attempt_ids() -> None:
    assert docker_container_name("ganesh-train-20260825T061157Z-main") == "ganesh-train-20260825t061157z-main"


def test_remaining_fails_before_finalization_margin(tmp_path: Path) -> None:
    args = type("Args", (), {
        "output": tmp_path, "max_seconds": 1000, "attempt_id": "test",
        "hourly_cost_usd": Decimal("1"),
    })()
    campaign = Campaign(args)
    campaign.started -= 500
    with pytest.raises(RuntimeError, match="insufficient bounded time"):
        campaign.remaining(0)


def test_phase_ledger_is_hash_sealed(tmp_path: Path) -> None:
    args = type("Args", (), {
        "output": tmp_path, "max_seconds": 3600, "attempt_id": "test",
        "hourly_cost_usd": Decimal("1"),
    })()
    campaign = Campaign(args)
    campaign.record("isolation", "passed", roots=2)
    import json
    value = json.loads((tmp_path / "phase-ledger.json").read_text())
    claimed = value.pop("evidence_sha256")
    assert canonical_sha256(value) == claimed


def test_campaign_mounts_external_state_outside_read_only_workspace(tmp_path: Path) -> None:
    model = tmp_path / "model"
    workspace = tmp_path / "workspace"
    output = tmp_path / "output"
    shared_tmp = tmp_path / "shared-tmp"
    for path in (model, workspace, output, shared_tmp):
        path.mkdir()
    args = type("Args", (), {
        "output": output, "max_seconds": 3600, "attempt_id": "test",
        "hourly_cost_usd": Decimal("1"), "model": model,
    })()
    campaign = Campaign(args)
    campaign.docker = "/usr/bin/docker"
    base = " ".join(map(str, campaign.docker_base("ganesh-test", workspace)))
    assert "dst=/workspace,readonly" in base
    assert f"dst={CONTAINER_MODEL},readonly" in base
    assert "dst=/workspace/models" not in base

    training = tmp_path / "training"
    destination = output / "evaluation" / "candidate"
    config = output / "candidate.json"
    training.mkdir(); destination.mkdir(parents=True); config.write_text("{}")
    mounts = " ".join((
        f"type=bind,src={training.resolve()},dst={CONTAINER_TRAINING},readonly",
        f"type=bind,src={destination},dst={CONTAINER_OUTPUT}",
        f"type=bind,src={output},dst={CONTAINER_CONTROL},readonly",
    ))
    assert CONTAINER_ADAPTER == CONTAINER_TRAINING / "adapter-final"
    assert "/workspace/artifacts" not in mounts
    assert "/workspace/measurement" not in mounts
    assert "/workspace/configs" not in mounts

    with pytest.raises(ValueError, match="beneath /workspace"):
        external_mount(model, Path("/workspace/models/base"), readonly=True)
