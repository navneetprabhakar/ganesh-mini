#!/usr/bin/env python3
"""Fail closed before deleting a stopped Gate 0B VM."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("prebuild", "runtime", "gate1-baseline", "gate3-campaign"), required=True)
    parser.add_argument("--backup-manifest", type=Path, required=True)
    parser.add_argument("--resource-state", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    serial_group = parser.add_mutually_exclusive_group(required=True)
    serial_group.add_argument("--serial-evidence", type=Path)
    serial_group.add_argument("--serial-unavailable-evidence", type=Path)
    parser.add_argument("--operations-evidence", type=Path, required=True)
    parser.add_argument("--system-events-evidence", type=Path, required=True)
    parser.add_argument("--expected-resource-name", required=True)
    parser.add_argument("--expected-resource-id", required=True)
    parser.add_argument("--expected-prefix", required=True)
    parser.add_argument("--instance-absence-evidence", type=Path)
    parser.add_argument("--disk-absence-evidence", type=Path)
    parser.add_argument("--integrity-mode", choices=("strict", "quarantine"), default="strict")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.backup_manifest.read_text())
    claimed = manifest.pop("evidence_sha256", None)
    if claimed != canonical_sha256(manifest):
        raise SystemExit("backup manifest evidence seal is invalid")
    if manifest.get("status") != "verified" or manifest.get("prefix") != args.expected_prefix:
        raise SystemExit("backup manifest status or prefix mismatch")
    objects = manifest.get("objects", [])
    if not objects or not all(row.get("verified") for row in objects):
        raise SystemExit("backup manifest is empty or contains unverified objects")
    object_prefix = args.expected_prefix.rstrip("/") + "/"
    if any(not str(row.get("object_uri", "")).startswith(object_prefix) for row in objects):
        raise SystemExit("backup manifest contains an out-of-prefix object")
    rows = {row["object_uri"].removeprefix(object_prefix): row for row in objects}
    if len(rows) != len(objects):
        raise SystemExit("backup manifest contains duplicate objects")
    inventory_row = rows.get("runtime-files.sha256")
    if inventory_row is None or inventory_row.get("downloaded_sha256") != file_sha256(args.inventory):
        raise SystemExit("downloaded runtime inventory is absent or does not match its remote object")
    inventory: dict[str, str] = {}
    if args.integrity_mode == "strict":
        for line in args.inventory.read_text().splitlines():
            digest, relative = line.split(None, 1)
            inventory[relative.lstrip("*").removeprefix("./")] = digest
        for relative, digest in inventory.items():
            row = rows.get(relative)
            if row is None or row.get("downloaded_sha256") != digest:
                raise SystemExit(f"terminal backup is missing or mismatches local inventory: {relative}")
    if args.serial_evidence is not None:
        serial_relative = "provider/serial-port.log"
        serial_path = args.serial_evidence
        serial_status = "captured"
    else:
        serial_relative = "provider/serial-port-unavailable.txt"
        serial_path = args.serial_unavailable_evidence
        serial_status = "provider-unavailable-recorded"
    resource = json.loads(args.resource_state.read_text())
    resource_status = resource.get("status")
    resource_relative = "provider/resource-deleted.json" if resource_status == "DELETED" else "provider/resource-terminated.json"
    provider = {
        serial_relative: serial_path,
        "provider/operations.json": args.operations_evidence,
        "provider/system-events.json": args.system_events_evidence,
        resource_relative: args.resource_state,
    }
    if resource_status == "DELETED":
        if args.instance_absence_evidence is None or args.disk_absence_evidence is None:
            raise SystemExit("automatic deletion requires instance and disk absence evidence")
        provider["provider/absence-instance.json"] = args.instance_absence_evidence
        provider["provider/absence-disk.json"] = args.disk_absence_evidence
    for relative, path in provider.items():
        if not path.is_file() or path.stat().st_size == 0:
            raise SystemExit(f"provider evidence is missing or empty: {path}")
        row = rows.get(relative)
        if row is None or row.get("downloaded_sha256") != file_sha256(path):
            raise SystemExit(f"provider evidence is absent or mismatched in terminal backup: {relative}")
    if args.integrity_mode == "strict" and set(rows) != set(inventory) | {"runtime-files.sha256"} | set(provider):
        raise SystemExit("terminal backup object set does not exactly equal local plus provider evidence inventory")
    if resource.get("name") != args.expected_resource_name or str(resource.get("id")) != args.expected_resource_id:
        raise SystemExit("resource identity does not match the authorized VM")
    if resource_status == "DELETED":
        claimed = resource.pop("evidence_sha256", None)
        if claimed != canonical_sha256(resource):
            raise SystemExit("automatic deletion evidence seal is invalid")
        if resource.get("schema_version") != "ganesh-mini-gcloud-deleted-instance/v1" or resource.get("instance_termination_action") != "DELETE":
            raise SystemExit("automatic deletion evidence contract mismatch")
        if json.loads(args.instance_absence_evidence.read_text()) != [] or json.loads(args.disk_absence_evidence.read_text()) != []:
            raise SystemExit("automatically deleted instance or disk is still present")
        operations = json.loads(args.operations_evidence.read_text())
        required = {"compute.instances.guestTerminate", "compute.instances.deferredDelete"}
        observed = {
            row.get("operationType")
            for row in operations
            if str(row.get("targetId")) == args.expected_resource_id
            and str(row.get("targetLink", "")).endswith("/instances/" + args.expected_resource_name)
            and row.get("status") == "DONE"
        }
        if not required <= observed:
            raise SystemExit("provider operations do not prove guest termination and automatic deletion")
        resource["evidence_sha256"] = claimed
    elif resource_status != "TERMINATED":
        raise SystemExit(f"resource must be stopped or automatically deleted before teardown: {resource_status}")
    evidence = {
        "schema_version": "ganesh-mini-gcloud-deletion-gate/v1",
        "status": "passed",
        "phase": args.phase,
        "expected_prefix": args.expected_prefix,
        "backup_manifest_sha256": claimed,
        "resource_name": args.expected_resource_name,
        "resource_id": args.expected_resource_id,
        "resource_status": resource_status,
        "resource_state_sha256": file_sha256(args.resource_state),
        "provider_serial_status": serial_status,
        "object_count": len(objects),
        "integrity_mode": args.integrity_mode,
        "admission_eligible": args.integrity_mode == "strict",
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
