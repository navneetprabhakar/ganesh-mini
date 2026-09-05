"""Finite local watcher: retrieve stopped VM evidence, verify it, then clean up."""
import argparse
import base64
import hashlib
import json
import subprocess
import time
from pathlib import Path

PROJECT = "executespecv1"
NAME = "ganesh-mini-verify-20260905"
ZONE = "us-central1-a"
PREFIX = "gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/results/"
AUDIT_PREFIX = PREFIX.removesuffix("results/") + "audit/"


def run(*args):
    return subprocess.check_output(["gcloud", *args, "--project=" + PROJECT], text=True, timeout=300)


def backup_verified(path):
    """Require the audit's exact bytes to survive a GCS upload/download roundtrip."""
    url = AUDIT_PREFIX + path.name
    run("storage", "cp", str(path), url)
    metadata = json.loads(run("storage", "objects", "describe", url, "--format=json"))
    downloaded = path.with_suffix(path.suffix + ".gcs-verified")
    run("storage", "cp", url + "#" + str(metadata["generation"]), str(downloaded))
    if hashlib.sha256(downloaded.read_bytes()).digest() != hashlib.sha256(path.read_bytes()).digest():
        raise RuntimeError("GCS audit roundtrip failed: " + url)


def billing_resource_inventory():
    """Read-only project-wide checks; inventory is not a real-time billing ledger."""
    checks = {
        name: ("compute", name, "list", "--format=json")
        for name in ("instances", "disks", "snapshots", "addresses", "reservations",
                     "commitments", "forwarding-rules", "routers", "vpn-tunnels")
    }
    checks["all_assets"] = ("asset", "search-all-resources", "--scope=projects/1061994342941", "--format=json")
    result = {"recorded_at_unix": time.time(), "resources": {}, "errors": {},
              "limitation": "Billing postings can lag; all_assets requires review for services beyond Compute. Do not claim GCS-only billing from empty Compute inventory alone."}
    for name, command in checks.items():
        try:
            result["resources"][name] = json.loads(run(*command))
        except (subprocess.SubprocessError, ValueError) as error:
            result["errors"][name] = str(error)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + 9*3600
    while time.monotonic() < deadline:
        instance = json.loads(run("compute", "instances", "describe", NAME, "--zone="+ZONE, "--format=json"))
        if str(instance["id"]) != args.instance_id:
            raise RuntimeError("instance identity changed; refusing cleanup")
        (args.output / "instance-latest.json").write_text(json.dumps(instance, indent=2))
        if instance["status"] == "TERMINATED":
            break
        time.sleep(60)
    else:
        raise RuntimeError("provider deadline exceeded; inspect VM, no automatic extension")
    listing = json.loads(run("storage", "ls", "--json", PREFIX+"*"))
    (args.output / "remote-listing.json").write_text(json.dumps(listing, indent=2))
    # Ask for per-object metadata: listing layout varies between SDK releases.
    urls = [line for line in run("storage", "ls", PREFIX+"*").splitlines() if line.startswith(PREFIX)]
    if PREFIX+"terminal.json" not in urls:
        raise RuntimeError("terminal backup missing; retain stopped disk for recovery")
    verified = []
    for url in urls:
        metadata = json.loads(run("storage", "objects", "describe", url, "--format=json"))
        generation = str(metadata["generation"])
        target = args.output / url.rsplit("/", 1)[1]
        run("storage", "cp", url+"#"+generation, str(target))
        data = target.read_bytes()
        md5 = metadata.get("md5_hash", metadata.get("md5Hash"))
        if not md5 or base64.b64encode(hashlib.md5(data).digest()).decode() != md5 or len(data) != int(metadata["size"]):
            raise RuntimeError("download differs from remote object: " + url)
        verified.append({"url": url, "generation": generation, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    report_path = args.output / "final.admission.json"
    if report_path.exists():
        report = json.loads(report_path.read_text())
        result = args.output / "final.admitted.jsonl"
        if hashlib.sha256(result.read_bytes()).hexdigest() != report["output_sha256"]:
            raise RuntimeError("final admitted output hash mismatch")
    terminal = json.loads((args.output / "terminal.json").read_text())
    required = {"terminal.json", "bootstrap.log"}
    if terminal["exit_code"] == 0:
        required.update({"final.admission.json", "final.admitted.jsonl", "executions.jsonl",
                         "qualification.json", "qualification-1.json", "qualification-4.json",
                         "qualification-8.json", "docker-info.json", "host.txt"})
    if not required.issubset({item["url"].rsplit("/", 1)[1] for item in verified}):
        raise RuntimeError("required campaign evidence missing in GCS; preserve disk")
    backup_path = args.output / "verified-download.json"
    backup_path.write_text(json.dumps(verified, indent=2))
    # GCS, not only the laptop, must hold the verified backup inventory and
    # resource identity before any deletion occurs.
    backup_verified(backup_path)
    backup_verified(args.output / "instance-latest.json")
    # Only the named campaign resources are deleted, after all backup bytes match.
    run("compute", "instances", "delete", NAME, "--zone="+ZONE, "--quiet")
    run("compute", "networks", "subnets", "delete", NAME, "--region=us-central1", "--quiet")
    run("compute", "networks", "delete", NAME, "--quiet")
    absence = {}
    for resource, location in (("instances", "--zones="+ZONE), ("disks", "--zones="+ZONE)):
        absence[resource] = json.loads(run("compute", resource, "list", location, "--filter=name="+NAME, "--format=json"))
    absence["networks"] = json.loads(run("compute", "networks", "list", "--filter=name="+NAME, "--format=json"))
    absence["subnets"] = json.loads(run("compute", "networks", "subnets", "list", "--regions=us-central1", "--filter=name="+NAME, "--format=json"))
    (args.output / "resource-absence.json").write_text(json.dumps(absence, indent=2))
    if any(absence.values()):
        raise RuntimeError("campaign resources remain after cleanup")
    backup_verified(args.output / "resource-absence.json")
    for pass_number in (1, 2):
        if pass_number == 2:
            time.sleep(60)
        inventory_path = args.output / f"post-teardown-inventory-{pass_number}.json"
        inventory_path.write_text(json.dumps(billing_resource_inventory(), indent=2))
        backup_verified(inventory_path)
    print("Campaign resources removed after verified GCS backup. Two post-teardown inventories saved in GCS; review them and billing lag before claiming GCS-only charges.", flush=True)


if __name__ == "__main__":
    main()
