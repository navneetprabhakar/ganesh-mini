# Approved CPU verification campaign — 2026-09-05

Authorization: Navneet accepted the proposed VM with a $15 pre-tax budget and
an eight-hour maximum. Scope is qualification and executable verification of
the 5,885-row cutoff; no GPU or training and no regeneration of candidates.

- Project: executespecv1
- Instance: ganesh-mini-verify-20260905
- Zone: us-central1-a
- Machine: n2-standard-16 (16 vCPU, 64 GiB)
- Boot image: ubuntu-2204-jammy-v20260826, ubuntu-os-cloud
- Boot disk: 100 GiB pd-balanced
- Network/subnet: ganesh-mini-verify-20260905; 10.246.0.0/28
- Private-only VM with Private Google Access; no external IP, NAT, ingress
  firewall rules, or SSH deployment required. The initial public-IP create
  request was rejected by organization policy before resource creation.
- Runtime bound: provider max-run-duration=8h, termination action STOP,
  automatic restart disabled. Guest exits with poweroff after terminal backup.
- On-demand compute rate: $0.776944/hour, $6.215552 for eight hours.
  Disk at $0.000136986/GiB-hour adds $0.109589 for eight hours; no external IP
  charge. Storage/transfer contingency remains inside the $15 budget.
  Stopped disks still incur storage charges until cleanup.
- Price sources: https://cloud.google.com/products/compute/pricing/general-purpose
  and https://cloud.google.com/compute/disks-image-pricing
- Existing service account: 1061994342941-compute@developer.gserviceaccount.com;
  existing bucket access was checked, no IAM grant added.
- Bucket: ganesh-gate0-model-transfer-1061994342941
- Campaign prefix: ganesh-mini-1.0/verification/cutoff5885-20260905

Workspace archive SHA-256:
`608c825ee965a3b79fe6aa1ad77c7ab100295112a6f847a08fa016a9c5622b9b`.
The VM verifies this before extraction. Original Docker-package bundle hash:
`2de5e2625e77f38d895d32bb69592970d017dcdc6494ca807421eb8ff0065245`.
Verifier-image archive hash:
`1c5c8196cdcc595d755ea506f774dee8a5699e495fe67d7c4441e7a06c21b972`.
All six images retain their pinned identities and resource/network constraints.

Qualification uses one generation and one repair candidate per lane at 1, 4,
and 8 record workers. Every trial must accept all 12, preserving ID order.
The fastest successful configuration runs final admission using the existing
serial deduplication replay. Per-execution evidence is written locally and
progress is backed up every minute. Terminal artifacts include actual output,
rejections, counts, hashes, qualification timing, and a separate quality-review
pending marker. These tests do not waive the known quality-review defect.

After VM qualification passes, stop the redundant laptop verifier and preserve
its unfinished evidence. Retrieve and verify terminal output before deleting
the VM/disk, subnet, and network; retain evidence in the campaign prefix.
If runtime is exhausted, stop and retain the disk until evidence retrieval.
Do not automatically retry, restart, enlarge the VM, or extend the deadline.
