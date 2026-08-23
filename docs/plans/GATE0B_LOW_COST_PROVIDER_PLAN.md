# Gate 0B low-cost provider plan

Status: proposed; no replacement compute launched

Date: 2026-08-23

## Decision

Target one non-preemptible RunPod Secure Cloud pod with an NVIDIA A40 48 GB.
Keep the frozen `bf16-lora-primary-v1` recipe, exact Qwen revision, dependency
lock, 16-record qualification corpus, evidence schema, and 50-minute controller
contract unchanged.

The A40 is an Ampere GPU with 48 GB ECC memory and native BF16 Tensor Core
support. It exceeds the recipe's 24 GiB admission floor without changing to
QLoRA. RunPod's published Secure Cloud rate on 2026-08-23 is `$0.44/GPU-hour`,
so 50 minutes is `$0.366667`. Use a `$0.60` hard ceiling for one attempt,
including a short provider/driver preflight and storage allowance.

Sources:

- RunPod current rental rates: <https://www.runpod.io/articles/guides/ai-server-cost>
- RunPod Pod API: <https://docs.runpod.io/api-reference/pods/POST/pods>
- NVIDIA A40 specification: <https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a40/proviz-print-nvidia-a40-datasheet-us-nvidia-1469711-r8-web.pdf>

## Why not the other cheap paths

| Option | 50-minute compute | Finding |
|---|---:|---|
| RunPod A40 48 GB | `$0.366667` | Preferred: adequate BF16 memory and non-preemptible pricing |
| Lambda A6000 48 GB | `$0.908333` | Operational fallback; VM semantics are simpler but cost is about 2.5x A40 |
| GCP Spot A100 40 GB | `$1.767342` upper bound | Minimal migration, but repeats the observed preemption failure mode |
| GCP Standard A100 40 GB | `$3.061154` compute upper bound | Canceled as too expensive |
| GCP/RunPod L4 24 GB | lower | Rejected for the primary recipe: marketed 24 GB does not provide safe margin over the frozen 24 GiB floor |

RunPod and Lambda figures are published provider rates and exclude applicable
tax. The GCP Spot figure uses this project's last sealed `$2.12081/hour` upper
bound; Spot prices are dynamic and would require reverification plus explicit
GCloud approval.

## Portability work before launch

1. Package the already qualified CUDA filesystem as the Pod's primary image;
   do not rely on nested Docker for Gate 0B.
2. Add a provider-neutral entrypoint that records provider identity, GPU name,
   VRAM, compute capability, driver, allowed CUDA version, host RAM, disk, and
   price before downloading model inputs.
3. Fail within five minutes if the host driver cannot run the pinned CUDA 13
   image, the GPU is not a full 48 GB A40/A6000-class device, BF16 is false, or
   host memory/disk do not satisfy the controller.
4. Run qualification with network disabled after all generation/hash-pinned
   inputs are present.
5. Copy terminal evidence to the local controller, hash it independently,
   upload it to a fresh generation-pinned GCS prefix, verify the complete GCS
   manifest, and only then terminate the Pod.
6. Record provider deletion/absence evidence. Never treat a stopped but still
   billable Pod or volume as terminated.

## Preconditions

- RunPod API access and funded balance must be present. No local RunPod CLI or
  API-key environment variable was detected on 2026-08-23.
- A fresh provider-specific execution card must bind the immutable image,
  workspace, model, provider offer, price, runtime, backup, and deletion
  contracts.
- The user's GCS-backup requirement means the final evidence upload and
  verification are GCloud usage. That storage-only use requires explicit
  approval even though the GPU compute is non-GCloud.

Until these preconditions are satisfied, Gate 0B remains closed and no paid
replacement resource may launch.
