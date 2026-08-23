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

## 2026-08-23 — CUDA prebuild retry succeeded; CPU resources torn down

Navneet Prabhakar approved the bounded recovery, resume, verification, backup,
and teardown starts needed to finish the already-created CPU prebuild resource.
This approval did not extend to A100 creation or CUDA qualification.

The first prebuild completed the Docker image but failed during archive export
with exit 141. `zstd` progress output generated a carriage-return-delimited
token too large for the GCE metadata logger's scanner, which closed the pipe.
The export now uses quiet mode. Provider serial output from that original boot
was no longer retrievable after stop/start; it was not reconstructed. The
limitation is sealed under recovery evidence
`cd6dbd1add64b6c8331ea1e06f1404ef2f59169a9a3f6223aa11866b17e06d6c`,
and attempt 1 remains failed, non-decision evidence.

Attempt 2 revalidated the same disk, VM identity, prior backup, recovery
finding, image identity, build inputs, workspace, and cost ceiling before
export. It produced image
`sha256:37b7cbcb8280d469bad6213bf09bfa0ccb2dba96a912aaa105183069c2ce5351`
(`ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1`) and an 8,167,013,739-byte
archive with SHA-256
`f2dafd6c0b82d46be441dfe2a5c2b23cd5f309e5061f20da3edf91e70eddb8f3`.
The exact 35-object terminal set is independently verified by backup seal
`f1a874deac5e5fadf19eeb29d2c4fb80376e62ed130f70439e2894ae6b4ec076`.

The first verifier boot failed because `gsutil -u` required a permission not
held by the VM service account. The verifier was changed to project-scoped
`gcloud storage cp`; a retry inside the approved aggregate 15-minute budget
verified all 35 objects. The deletion gate then passed with evidence seal
`7aac011553e05d5a29f446d7796fd3b159a2c5a81c6d70a16d572a4d6f5139d1`.
Its evidence was independently backed under seal
`933eef4f0f4d5ae39a2b743c980655ccb858ac72cb841c8217ad81703bd244ee`.

The CPU VM, NAT, and router were deleted only after verified backup. Their
absence is sealed by
`ac2b9c9f21e0b6f91d72a0d90d80f3eb8a55ea56432fb66980bae76d86e28358`.
The dedicated VPC and subnet remain intentionally for a no-NAT A100 run. No
compute is running, and no Gate 0B CUDA qualification is claimed. A Standard
`a2-highgpu-1g` execution remains a separate GCloud authorization boundary.

## 2026-08-23 — Standard A100 attempt failed on environment; all resources deleted

Navneet Prabhakar explicitly approved one Standard `a2-highgpu-1g` Gate 0B
attempt with a 1,200-second maximum runtime, no NAT or external IP, and the
mandatory verified-backup-before-delete lifecycle.

The VM exposed one NVIDIA A100-SXM4-40GB and loaded the exact sealed image and
generation-pinned workspace/model inputs. Qualification then failed during
package identity with `ModuleNotFoundError: No module named 'torchvision'`.
The failure occurred before model loading or training, so it is environment
evidence only and cannot qualify Gate 0B. FLA also warned that Triton fell back
to CPU; the failed attempt could not expose the swallowed underlying exception.

The terminal prefix contains 31 independently verified objects under seal
`9d1ed5d0e5407ef7f9397ba7e406952865f981eda61ee5d337990bfd298f114d`.
The deletion gate is sealed by
`a887e8201df39c7da120b075e61c443639091e451ae3e109dee2b8c0dedb99f4`.
After those records were independently backed, the VM, subnet, and VPC were
deleted; their absence is backed under seal
`24b148309a89282f6ec6bf043a5bb7ff81baaca5ea783fa71ec1bfe138ec2284`.
Provider serial output was unavailable after stop and was not reconstructed;
the provider error, startup logs, structured result, and lifecycle evidence are
preserved explicitly.

The local repair pins Torchvision 0.28.0 for Torch 2.13.0, imports
`qwen_vl_utils` during image build, initializes Torch CUDA and the Triton CUDA
backend before importing FLA, requires FLA to report NVIDIA CUDA, and mounts a
bounded executable Triton cache while retaining a read-only root, no-exec
general `/tmp`, and network-disabled execution. This repair is not a Gate 0B
pass; it requires a new image build and a separately approved NVIDIA run.

## 2026-08-23 — Rebuilt CUDA environment passed; qualifier contract drift failed

The explicitly approved repaired Gate 0B card ran under prefix
`ganesh-mini-1.0/gate0b/20260823T000950Z`. A temporary Standard
`e2-standard-8` VM built image
`sha256:b2f9335c64b208e2d692dc45c56df0790573951df835d34604f80e93d0b0f2a6`.
Its 8,174,282,938-byte archive has SHA-256
`229325473993a1d5b58baec3ed01fe9d3a49b253be92b39b93d9a52e307e3f9f`
and GCS generation `1787447318500114`. The prebuild terminal backup is sealed
by `8ab74078de47a0055ff8a46285b01148fa33d9a994e2cbc702afb18be876815a`.

One Standard `a2-highgpu-1g` VM then loaded the exact sealed image and pinned
offline inputs. Package imports and versions passed, including Torch 2.13.0,
Torchvision 0.28.0, Transformers 5.15.1, FLA 0.5.2, and causal-conv1d 1.7.0.
The VM proved one NVIDIA A100-SXM4-40GB, BF16 support, CUDA 13.0, cuDNN 92000,
and Triton CUDA architecture 80. The qualifier then failed before model loading
because it referenced the removed module attributes `chunk_gated_delta_rule`
and `fused_recurrent_gated_delta_rule`. This is harness contract drift, not a
model or CUDA qualification result. The failed result is sealed by
`8ddeff566da4a32abfb3586f90f0ca5196cacbaed299dcb52d9fec3b733b3df6`,
and the 31-object runtime backup by
`d407c689528356d007b29f08725f29f5dc7caae3334b13cbe11e9dfc7c0d83aa`.

Transformers 5.15.1 exposes decorated wrappers named
`torch_chunk_gated_delta_rule` and `torch_recurrent_gated_delta_rule`. Merely
checking that those wrappers exist would be insufficient because their
decorator may select a Torch fallback. The corrected decision rule inspects
each wrapper closure and requires the resolved causal-convolution
implementations to originate in `causal_conv1d` and both delta-rule
implementations to originate in `fla`, in addition to the existing CUDA backend
checks. An absent closure or non-external implementation fails qualification.

The CPU VM, GPU VM, disks, NAT, router, subnet, and VPC were deleted only after
independent GCS verification; post-delete evidence proves them absent. The
complete local evidence archive is generation `1787451344731424` with SHA-256
`c761399cef0729841d9eba74b1f12ee9b95f5b8f8ce0369b24c02f957218da98`.
Because the runtime bind-mounts the run-scoped workspace at `/workspace`, the
corrected qualifier can reuse the sealed image and offline bundle. A new
A100-only execution still requires a new sealed cost/authorization card; the
prior approval is exhausted and no GCloud resource remains.

The retry controller must also propagate `GANESH_ATTEMPT_ID` into the
qualification container, and every post-list GCS verification read must use the
listed object generation. These are prospective audit hardenings: the sealed
failed run used an immutable run prefix and two matching full-object reads, so
its failure evidence remains valid even though its structured `attempt_id` was
null.

## 2026-08-23 — Decision references require admission before full directionality

The first full runs for decision tranches 4 and 5 rejected every known-bad
artifact but exposed mechanical defects in generated references: unused Go
imports and identifier collisions, strict TypeScript typing/redeclarations,
Python indentation, and JavaScript identifier collisions. Behavioral cases and
verifier expectations were not weakened to obtain a pass.

For future authoring or regeneration, the workflow requires two operational
checks before the final 120-execution run:

1. compile or type-check all 60 generated references across the six lanes; and
2. execute a dedicated 60-reference admission sweep through the same pinned,
   network-disabled, resource-limited Docker verifier.

A 60/60 admission result is the prospective safeguard for proceeding to the
full sequential reference and known-bad run. Any unretained admission sweep in
this authoring cycle is treated only as an operational preflight; this record
makes no historical sequencing claim from it. Final release evidence comes
only from the independently sealed 120-execution controllers with exact
manifest, overlap, runtime, sandbox, and artifact hashes. Failed or superseded
results remain non-decision evidence.

The first failed tranche-4 evidence file was overwritten during repair before
it was copied to a superseded path. Its observed seal was
`874e2308f503a35b4cf74c4f9105f623816834526c51e9d50a36b4dd3d01f0dc`
with 34/60 reference passes, 60/60 known-bad rejections, and 26 failures. A
read-only search of the workspace, temporary storage, Codex storage, caches,
Trash, and application-support paths found no retained copy. The file was not
reconstructed. This is a process incident and the missing artifact cannot be
used as evidence; the admission requirement prevents the overwrite pattern for
subsequent tranches. Tranche 5's failed evidence is preserved explicitly.

The per-tranche overlap reports historically record comparison paths and
counts, not every comparison input revision. A new global decision-surface
audit closes that gap without changing executed results. It byte-binds the two
seed JSONL files and runtime configuration; verifies every development and
decision manifest/task seal; binds all six overlap and directionality reports
plus the tranche-1/2 shared cross-overlap report; and rechecks all 720 execution
rows against their exact artifact, runtime, image, output hashes, sandbox, and
exit polarity. It proves zero exact or normalized prompt overlap and is sealed
by `96ea9669e194c567f304c5462b2be9cc171555bba56ea10801186480bb347a06`.
