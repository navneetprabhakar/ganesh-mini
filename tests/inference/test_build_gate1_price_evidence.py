from datetime import datetime, timedelta, timezone

import pytest

from scripts.inference.build_gate1_gcloud_preparation import canonical_sha256
from scripts.inference.build_gate1_price_evidence import build


NOW = datetime(2026, 8, 25, 12, 0, tzinfo=timezone.utc)
SOURCE = "https://cloud.google.com/products/compute/pricing/accelerator-optimized"


def make(**overrides):
    values = {
        "checked_at": (NOW - timedelta(minutes=5)).isoformat(),
        "source": SOURCE,
        "conservative_hourly_usd": "1.000416348",
        "support_reserve_usd": "0.35",
        "absolute_cost_ceiling_usd": "4.40",
        "now": NOW,
    }
    values.update(overrides)
    return build(**values)


def test_builds_canonical_fresh_price_evidence() -> None:
    evidence = make()
    claimed = evidence.pop("evidence_sha256")
    assert claimed == canonical_sha256(evidence)
    assert evidence["region"] == "us-east1"
    assert evidence["machine_type"] == "g2-standard-12"
    assert evidence["conservative_hourly_usd"] == "1.000416348"


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("checked_at", (NOW - timedelta(hours=25)).isoformat(), "current"),
        ("checked_at", (NOW + timedelta(minutes=6)).isoformat(), "future"),
        ("source", "https://example.com/pricing", "official Google Cloud"),
        ("conservative_hourly_usd", "nan", "finite"),
        ("conservative_hourly_usd", "1.02", "exceeds"),
        ("absolute_cost_ceiling_usd", "4.41", "exceeds"),
    ],
)
def test_rejects_untrusted_stale_or_over_budget_observations(field, value, message) -> None:
    with pytest.raises(ValueError, match=message):
        make(**{field: value})
