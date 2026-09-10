#!/usr/bin/env python3
"""Verify and seal the lane checkpoint-sweep GCS upload receipt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.inference.build_lane_checkpoint_sweep_upload_plan import canonical_sha256, file_sha256


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop(field, None)
    if claimed != canonical_sha256(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def same_bytes(left: Path, right: Path) -> bool:
    with left.open("rb") as left_stream, right.open("rb") as right_stream:
        while True:
            left_chunk = left_stream.read(8 * 1024 * 1024)
            right_chunk = right_stream.read(8 * 1024 * 1024)
            if left_chunk != right_chunk:
                return False
            if not left_chunk:
                return True


def build(base: Path, completed_at: str) -> dict[str, Any]:
    plan = load_sealed(base / "gcloud-upload-plan.json", "upload_plan_sha256")
    approval = load_sealed(base / "gcloud-upload-approval.json", "approval_sha256")
    if (
        approval.get("status") != "approved"
        or approval.get("approved_plan_sha256") != plan["upload_plan_sha256"]
        or approval.get("maximum_new_bytes") != plan["maximum_new_bytes"]
    ):
        raise ValueError("upload approval does not bind the sealed plan")
    rows = []
    for planned in plan["objects"]:
        name = planned["destination"].rsplit("/", 1)[-1]
        metadata = json.loads((base / "upload/metadata" / f"{name}.json").read_text())
        roundtrip = base / "upload/roundtrip" / name
        source = base.parents[2] / planned["source"]
        expected_name = planned["destination"].split("/", 3)[-1]
        generation = metadata.get("generation")
        checks = {
            "generation": isinstance(generation, str) and generation.isdigit(),
            "metadata_name": metadata.get("name") == expected_name,
            "metadata_size": str(metadata.get("size")) == str(planned["size_bytes"]),
            "source_size": source.stat().st_size == planned["size_bytes"],
            "source_sha256": file_sha256(source) == planned["sha256"],
            "roundtrip_size": roundtrip.stat().st_size == planned["size_bytes"],
            "roundtrip_sha256": file_sha256(roundtrip) == planned["sha256"],
            "roundtrip_bytes": same_bytes(source, roundtrip),
        }
        if not all(checks.values()):
            raise ValueError(f"upload verification failed: {name}: {checks}")
        rows.append({
            **planned,
            "generation": generation,
            "generation_uri": f"{planned['destination']}#{generation}",
            "checks": checks,
        })
    receipt: dict[str, Any] = {
        "schema_version": "ganesh-mini-lane-checkpoint-sweep-gcloud-upload-receipt/v1",
        "status": "complete",
        "completed_at": completed_at,
        "project": plan["project"],
        "bucket": plan["bucket"],
        "upload_plan_sha256": plan["upload_plan_sha256"],
        "approval_sha256": approval["approval_sha256"],
        "operation_scope": "six create-only uploads plus exact-generation roundtrip verification; no compute or infrastructure operations",
        "compute_or_infrastructure_actions": [],
        "object_count": len(rows),
        "uploaded_bytes": sum(row["size_bytes"] for row in rows),
        "objects": rows,
    }
    receipt["receipt_sha256"] = canonical_sha256(receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--completed-at", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    receipt = build(args.base.resolve(), args.completed_at)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"receipt_sha256": receipt["receipt_sha256"], "uploaded_bytes": receipt["uploaded_bytes"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
