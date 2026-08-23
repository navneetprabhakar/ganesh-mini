# Gate 0B GCP Standard L4 plan

Status: approved infrastructure; implementation preflight

Date: 2026-08-23

## Decision

Use one non-Spot `g2-standard-8` VM in `us-central1` with one NVIDIA L4,
8 vCPUs, and 32 GiB host RAM. Keep the exact Qwen revision, dependency lock,
16-record corpus, response-only masking, sequence length 4,096, rank 32,
micro-batch 1, gradient checkpointing, save/reload/merge checks, and evidence
contract.

The current Iowa Standard price is `$0.853624312/hour`. A 3,600-second maximum
plus `$0.10` storage/operation reserve gives an incremental bound of
`$0.953624312`, below the user-approved `$1.00` ceiling.

Source: <https://cloud.google.com/products/compute/pricing/accelerator-optimized>

## Hardware-specific qualification

- BF16 LoRA remains primary.
- Admit an L4 only when it exposes at least 22 GiB CUDA memory, compute
  capability at least 8.0, and native BF16 support.
- Fail the primary recipe when measured peak VRAM exceeds 21 GiB, leaving
  runtime headroom below the physical device limit.
- The NF4 QLoRA fallback is eligible only when the sealed primary evidence
  records CUDA OOM or the frozen peak-VRAM ceiling breach.
- Bound the offline container to 8 CPUs and 28 GiB RAM. Reject hosts exposing
  fewer than 8 CPUs or 30 GiB physical RAM.

These changes qualify a cheaper hardware envelope; they do not alter model,
data, optimization, or evaluation parameters.

## Lifecycle

1. Bind a new card and deterministic workspace to the pushed repair commit.
2. Reverify Standard G2 price and exact zone/image availability.
3. Upload generation-pinned inputs and prove all exact resource names absent.
4. Create a fresh VPC/subnet with Private Google Access and no external IP,
   router, or NAT; create one `g2-standard-8` VM.
5. Fail closed on hardware, package, kernel, hash, cost, or deadline mismatch.
6. Run BF16 LoRA qualification; run QLoRA only on a sealed allowed trigger.
7. Verify the terminal GCS manifest before stopping or deleting compute.
8. Delete VM, disk, subnet, and VPC and independently prove all absent.

No Gate 1 baseline or seed-pilot training is included in this one-VM approval.
