# Gate 0B GCP Standard L4 plan

Status: two executions complete; memory-capacity failure; resources deleted

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

## Executed outcome

The first `us-central1-b` create failed on provider capacity before VM/disk
creation. The zone-only retry in `us-central1-a` passed identity, external
kernels, model load, and text inference. BF16 LoRA and its correctly triggered
NF4 QLoRA fallback both OOMed in the 4,096-token backward envelope before the
first training record. Gate 0B remains closed. The 32-object terminal GCS
backup is independently verified under seal
`087d7c89b1806ddbe61772ba44ba8ce5ccbe17c8dd18fb122aa29189784d8f85`;
the VM, disk, subnet, and VPC are absent under seal
`eb8171a24a2c893a7fad2a7806fb4f187af7dbb4b86b2d630aee7882c359071d`.

The approved v3 retry moved the frozen vision tower to CPU and measured the
expected CUDA release: 662,833,664 bytes for BF16 and 190,087,680 bytes for
NF4. Both recipes nevertheless OOMed in the same 4,096-token synthetic
backward envelope before the first training record. Its 32-object terminal
backup is independently verified under seal
`ed92e5f42f4a076a347685ab829fa07a6644cce7e7c19f0cb9c6985d37d97c8a`;
all four resources are absent under seal
`cda4d4b4a44f52b25dddac1e2f6939390499352da57336fc49e868baef52c8af`.

Corpus measurement changes the next contract: the longest of 2,155 prepared
training records is 2,938 tokens and every validation record is shorter than
1,024. A 3,072-token envelope therefore preserves every prepared token while
removing 1,024 synthetic tokens that no training example uses. Rank, alpha,
optimizer, effective batch, learning-rate candidates, response-only labels,
model revision, and serving context remain unchanged.
