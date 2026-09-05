# Verification campaign backup receipt — 2026-09-06 IST

The VM completed all 5,885 candidates: 5,883 passed and two Rust references
timed out. The original report remains unchanged, including its strict-seal
failure status. A separate quality defect in Go leaves 5,882 review-eligible
rows and three held candidates. Quality review remains 3/300, incomplete.

## Verified GCS evidence

Campaign prefix:
`gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/`

- `results/`: 13 VM artifacts, including raw executions, admitted rows,
  admission report, qualifications, host/runtime information, terminal record,
  and bootstrap log. Each entry in `audit/verified-download.json` records
  object generation, byte count, and downloaded SHA-256. All 13 local copies
  were independently rehashed and matched during this follow-up.
- `audit/`: verified-download inventory, instance identity, resource absence,
  and both post-teardown inventories. The watcher required inventory and
  identity upload/download verification before deletion.
- `archive/full-evidence-20260906.tar.gz`: 122,389,351 bytes;
  generation `1788638543675053`; SHA-256
  `42a781572d80573e0ffffceb4c84e2c0f84a5f24e846c7aaba1a4e10d6405641`.
  Downloaded that exact generation to a separate local file and verified its
  SHA-256 matches. Archive contains the entire local expansion cache/history,
  expansion measurement evidence, retrieved VM artifacts/audits, data scripts
  and configs, and the handoff/decisions/expansion documentation as captured
  before this receipt. Later documentation and script changes are saved in
  a separate closeout bundle rather than rewriting this archive.

## Cleanup and billing limits

The campaign VM, disk, subnet, and network have been deleted after verified
VM backups. Both post-teardown Compute inventories (81 seconds apart) were
empty for instances, disks, snapshots, addresses, reservations, commitments,
forwarding rules, routers, and VPN tunnels. No VM remains to stop.

Additional read-only checks executed on 2026-09-06 IST returned exit 0 and
empty JSON arrays for these commands with `--project=executespecv1 --format=json`:

- `gcloud sql instances list`
- `gcloud container clusters list`
- `gcloud artifacts repositories list --location=all`
- `gcloud dns managed-zones list`

These are partial service inventories, not a billing-ledger certification.
Cloud Asset API was disabled in both original scans. Other services and
delayed billing postings remain unverified; do not claim GCS-only billing.
No unrelated resources were removed and no service APIs were enabled.

## Local validation

Partition source candidate hash matches the executed admission input hash.
Both partition outputs match their manifest hashes; 5,882 eligible rows are
exactly the original passed rows minus the held Go ID, with unique IDs and no
overlap with the three held candidates. Original rows are unchanged.
Fourteen focused tests passed (partition, cutoff preparation, VM helpers).
The original 300-row quality sample is retained, including flagged records.
