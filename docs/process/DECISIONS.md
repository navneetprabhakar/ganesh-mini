# Decisions

## 2026-08-22 — Ganesh v0.1 training data authorized as seed corpus

Navneet Prabhakar explicitly authorized reuse of the Ganesh v0.1 training data
for `ganesh-mini-1.0`, stating that it is his data, already cleaned for the same
purpose, with only the backbone changing.

Consequences:

- Ownership, source-license suitability, and historical teacher provenance are
  accepted by user authority for this project and are not re-admission gates.
- The data will be imported from the committed Ganesh repository state with
  source paths, source commit, byte hashes, record IDs, and split lineage
  preserved.
- Mechanical checks remain mandatory: Qwen schema rendering, duplicate IDs,
  parseability, current compiler/runtime execution, and disjointness from the
  newly frozen Ganesh Mini development and decision sets.
- Re-execution failures are quality signals to quarantine or repair; they do
  not reopen the ownership decision.
- Additional data may be added later, but the v0.1 corpus is the first pilot
  and baseline training source.

Inspected committed Ganesh source revision:
`9552867c7641a5f11acadb84d19bfb8d723ab0ae`.

Seed inventory observed at that revision:

| Lane | Training | Validation | Source |
|---|---:|---:|---|
| Python | 468 | 30 | `data/train/multisource_python_v2/` |
| Go | 163 | 4 | `data/train/multiling_v1/go/` |
| Java | 146 | 4 | `data/train/multiling_v1/java/` |
| JavaScript | 222 | 4 | `data/train/multiling_v1/js/` |
| TypeScript | 218 | 4 | `data/train/multiling_v1/ts/` |
| Rust | 182 | 4 | `data/train/cuda_lora_v5/rust/` |
| **Total** | **1,399** | **50** | |

The Rust source differs from the `multiling_v1` paths because that committed
directory has no Rust lane. Its use is authorized, but its schema must be
normalized into the same Ganesh Mini contract.

## 2026-08-22 — Broad in-scope authorization; GCloud remains gated

Navneet Prabhakar authorized all actions required to complete the Ganesh Mini
objective without further approval requests, except GCloud usage.

Consequences:

- Local setup, downloads, dataset processing, long-running jobs, training,
  non-GCloud compute, benchmarking, repository operations, decision-set use
  under the frozen plan, and artifact publication are authorized.
- GCloud inspection, mutation, execution, and billing remain prohibited until
  explicitly authorized.
- Technical gates still apply. Authorization does not turn missing evaluation,
  invalid evidence, failed tests, or an unqualified model into a pass.

## 2026-08-22 — Recurring independent goal-alignment audit

A Codex heartbeat named `Audit Ganesh Mini goal alignment` runs every 30
minutes. Each run must spawn an independent read-only review subagent to compare
active work and repository changes with the original Ganesh Mini objective and
canonical plan.

If the reviewer reports `DIVERGENCE`, the primary task pauses further
mutations, training, downloads, and compute and waits for Navneet Prabhakar.

## 2026-08-22 — BF16 LoRA primary; NF4 QLoRA fallback

After reviewing the 2B backbone and the project's quality-first objective,
Navneet Prabhakar selected ordinary BF16 LoRA as the primary pilot mechanism.

Consequences:

- The primary CUDA pilot loads the frozen Qwen backbone in BF16 and trains
  rank-32 LoRA adapters with BF16 compute.
- The starting resource envelope is a CUDA GPU with at least 24 GB VRAM,
  sequence length 4,096, micro-batch 1, gradient checkpointing, and gradient
  accumulation.
- NF4 QLoRA is a predeclared fallback, not the default. It becomes eligible
  only after the primary recipe records an OOM, exceeds the frozen peak-VRAM
  ceiling, or breaches the execution card's cost threshold.
- Training quantization remains independent of release quantization. The
  selected adapter is merged into a BF16 reference checkpoint before F16 and
  Q8 GGUF export.
- Full-parameter fine-tuning remains unjustified for the 1,399-record seed
  corpus because its overfitting and forgetting risk is materially higher.

## 2026-08-22 — Bounded GCloud Gate 0B qualification authorized

Navneet Prabhakar explicitly authorized one bounded GCloud CUDA qualification
for the `bf16-lora-primary-v1` recipe.

Authorized scope:

- inspect the active authenticated GCloud account/project configuration without
  exposing credentials;
- provision one isolated NVIDIA GPU with at least 24 GiB VRAM;
- enforce a USD 5 absolute cost ceiling and the controller's 1,800-second wall
  ceiling;
- run the pinned 16-record BF16 LoRA qualification and preserve raw/sealed
  evidence;
- use the NF4 QLoRA fallback only if primary evidence records an allowed
  fallback trigger;
- back up all run data to GCS and verify object identities before teardown;
- terminate the VM after the verified GCS backup and record proof that the VM
  is absent.

This authorization does not include modifying, starting, stopping, or
inspecting unrelated existing GCloud resources. Every mutation must name the
resolved project explicitly.

Mandatory lifecycle order:

1. Resolve the dedicated GCS destination and pass a write/read/hash round trip.
2. Provision the isolated VM only after GCS preflight passes.
3. Upload configs, locks, logs, environment inventories, raw outputs,
   telemetry, adapters/checkpoints, merged artifacts, failures, and manifests
   during and after execution so preemption does not erase evidence.
4. Produce a GCS backup seal binding every object URI, generation, size, and
   SHA-256 to the terminal run manifest.
5. Delete the VM only after the backup seal exists.
6. Verify VM absence and preserve a teardown seal.

A missing backup seal or failed VM deletion is a terminal run failure and
cannot support Gate 0B qualification.

## 2026-08-22 — Gate 0B authorization exhausted; prebuild before another GPU run

The approved Gate 0B scope was exercised through three fail-closed, fully
sealed attempts. Navneet Prabhakar also explicitly approved the exact temporary
custom VPC, subnet, router, and NAT required by organization policy for a VM
without an external IP.

Observed terminal outcomes:

1. The pinned CUDA DLVM image did not include Docker. The VM stopped before
   input download, controller start, model loading, or training.
2. After pinning `docker.io=29.1.3-0ubuntu3~22.04.2`, the Dockerfile's optional
   BuildKit cache mount failed under the legacy CLI path. The VM stopped before
   model loading or training.
3. After removing that cache-only directive, GCE emitted a verified
   `compute.instances.preempted` system event while the Spot A100 was compiling
   `causal-conv1d`. The model and training still never started.

All attempts backed run data to generation-pinned GCS objects before VM
deletion. All run-scoped VMs, NATs, routers, subnets, and VPCs are absent. The
cumulative GPU upper cost is `$0.79037286`; the conservative retained bound is
`$4.92111752`, below the `$5` authorization ceiling. No CUDA qualification is
claimed, and the authorization permits no further VM recreation.

Consequence: another Gate 0B design must prebuild and content-seal the CUDA
image outside the bounded GPU window, then use preemption-resilient compute for
the actual qualification. Any such GCloud work requires fresh explicit user
approval.

## 2026-08-22 — Compiled decision lanes use a 60-second aggregate limit

Two fail-closed Docker directionality runs showed the frozen 30-second
aggregate task limit was flaky on the local Docker host: one Rust reference and
one Java reference timed out after successful compilation activity. The
verifier also exposed and fixed a bytes/string normalization defect in
`TimeoutExpired` reporting; the defect never converted a timeout into a pass.

The decision contract now uses 60 seconds for Go, Java, and Rust, while
JavaScript, TypeScript, and Python remain at 30 seconds. Tranche manifests,
intra-set overlap reports, the cross-tranche seal, runner bindings, and tests
were regenerated. Superseded evidence remains preserved and cannot satisfy the
current release gate.
