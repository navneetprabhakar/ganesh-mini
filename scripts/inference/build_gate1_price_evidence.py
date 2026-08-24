#!/usr/bin/env python3
"""Seal a fresh official-price observation for the bounded Gate 1 launcher."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlparse

ROOT_HINT = Path(__file__).resolve().parents[2]
if str(ROOT_HINT) not in sys.path:
    sys.path.insert(0, str(ROOT_HINT))

from scripts.inference.build_gate1_gcloud_preparation import canonical_sha256


ALLOWED_SOURCE_HOSTS = {"cloud.google.com", "docs.cloud.google.com"}


def build(
    *,
    checked_at: str,
    source: str,
    conservative_hourly_usd: str,
    support_reserve_usd: str,
    absolute_cost_ceiling_usd: str,
    now: datetime | None = None,
) -> dict[str, str]:
    observed = datetime.fromisoformat(checked_at.replace("Z", "+00:00"))
    if observed.tzinfo is None:
        raise ValueError("checked-at must include a timezone")
    current = now or datetime.now(timezone.utc)
    age = current.astimezone(timezone.utc) - observed.astimezone(timezone.utc)
    if age < timedelta(minutes=-5) or age > timedelta(hours=24):
        raise ValueError("price observation must be current and not future-dated")
    parsed = urlparse(source)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_SOURCE_HOSTS:
        raise ValueError("price source must be an official Google Cloud HTTPS page")
    try:
        hourly = Decimal(conservative_hourly_usd)
        reserve = Decimal(support_reserve_usd)
        ceiling = Decimal(absolute_cost_ceiling_usd)
    except InvalidOperation as error:
        raise ValueError("price values must be finite decimals") from error
    if not all(value.is_finite() for value in (hourly, reserve, ceiling)):
        raise ValueError("price values must be finite decimals")
    upper = hourly * Decimal(18) + reserve
    if hourly <= 0 or reserve < 0 or ceiling > Decimal("19.00") or upper >= ceiling:
        raise ValueError("price observation exceeds the Gate 1 approval envelope")
    value = {
        "schema_version": "ganesh-mini-gate1-price-evidence/v1",
        "status": "verified",
        "checked_at": observed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "region": "us-east1",
        "machine_type": "g2-standard-12",
        "source": source,
        "conservative_hourly_usd": str(hourly),
        "support_reserve_usd": str(reserve),
        "absolute_cost_ceiling_usd": str(ceiling),
    }
    value["evidence_sha256"] = canonical_sha256(value)
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checked-at", required=True, help="timezone-aware ISO-8601 observation time")
    parser.add_argument("--source", required=True)
    parser.add_argument("--conservative-hourly-usd", required=True)
    parser.add_argument("--support-reserve-usd", default="0.35")
    parser.add_argument("--absolute-cost-ceiling-usd", default="19.00")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    evidence = build(
        checked_at=args.checked_at,
        source=args.source,
        conservative_hourly_usd=args.conservative_hourly_usd,
        support_reserve_usd=args.support_reserve_usd,
        absolute_cost_ceiling_usd=args.absolute_cost_ceiling_usd,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
