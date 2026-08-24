from decimal import Decimal
from pathlib import Path

import pytest

from scripts.campaign.run_host import Campaign, canonical_sha256


def test_canonical_campaign_seal_is_order_independent() -> None:
    assert canonical_sha256({"b": 2, "a": 1}) == canonical_sha256({"a": 1, "b": 2})


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
