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

This decision was superseded on 2026-08-23 when Navneet Prabhakar explicitly
disabled further deviation checks. No recurring goal-alignment automation or
review subagent remains active.

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
  ceiling. Cost alone is not a fallback trigger unless a cheaper host is
  separately qualified; quantizing on the same GPU is not presumed cheaper.
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

The previous card's conservative `$5` cumulative ceiling is exhausted for a
second full Standard A100 upper bound. The A100-only retry therefore binds its
own exact `$5.75` absolute ceiling through instance metadata, startup
controller, and qualification runner; missing, nonpositive, or reached ceiling
values fail closed. The card records a `$1.474461667` incremental upper bound
and `$5.723091194` conservative cumulative upper bound. Gate 0B truthfully
includes a bounded 16-record optimizer/save/reload/merge training smoke, but it
does not authorize or perform seed-pilot or main training.

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

## 2026-08-23 — Attribute-repair A100 retry exposed an FLA symbol mismatch

Navneet Prabhakar approved continuation of all project steps, requested that
VM/GPU utilization be maximized, disabled further deviation checks, and asked
the work to continue unless an anomaly occurred.

The A100-only retry ran under prefix
`ganesh-mini-1.0/gate0b/20260823T030116Z`. It proved the exact pinned package
set, one NVIDIA A100-SXM4-40GB, BF16, CUDA 13.0, cuDNN 92000, Triton CUDA
architecture 80, both causal-conv1d kernels, and the external FLA chunk kernel.
It then failed after 33.86 seconds because Transformers 5.15.1 requested
`fla.ops.gated_delta_rule.recurrent_gated_delta_rule`, while FLA 0.5.2 exports
the equivalent CUDA decode implementation as
`fused_recurrent_gated_delta_rule`. Transformers silently selected its Torch
fallback. Model loading and training did not begin, so Gate 0B remains closed.
The failed result is sealed by
`d7fdb89ce744524ec87ad4b10caf2cb189ef7fb61f61fb6e2e7c152a6f538e50`;
the 28-object terminal backup is sealed by
`39ed40945ded583ebbc47ebbbcf3e4d9faf899dcbbe418a741aef87a4ea86065`.

The stopped VM was deleted only after the 31-object composite deletion backup
passed under seal
`a5e5c0779fe298ee0d915481e435fa22cccc017b2c17bde2d4947264c7d16204`
and deletion-gate seal
`7e1d4f9c3eb3dbbe558c4e972083dcc272e3dd1b95bb7f64bdb23d891d3bab88`.
The VM, disk, subnet, and VPC are absent. The nine-object post-delete backup is
sealed by
`8d353de09d2e61f165f7eff0d2b6edcfcbcc43650bc202dbf6c7e5b4c1b3af07`.
The complete local run archive is independently verified in GCS with SHA-256
`29d0d8e7b7266a85d05f909fed36d2bde01cad21450c0605c6f3c2a8883d31b3`
and manifest seal
`f0e930840aebc876ea49f92e5ce4deabf59a3922a8ae4e72fcd2c5cd89a8316c`.

The repair does not weaken qualification to accept the slower Torch fallback.
It installs a process-local alias from FLA's requested recurrent symbol to its
fused recurrent CUDA implementation before Qwen3.5 is imported, then retains
the closure-origin check requiring the resolved implementation to come from
`fla`. This preserves the external chunk kernel for training and the fused
recurrent kernel for single-token cached decode. Any late installation,
missing fused implementation, non-callable symbol, or non-FLA implementation
fails closed. A further paid run is not started until this anomaly repair is
fully validated and bound into a fresh execution card. The next qualifier also
shares one base-model load between inference and the 16-record training smoke
and raises the A100 container envelope from 8 vCPUs/32 GiB to the host's 12
vCPUs with a 72 GiB ceiling, reducing idle setup time without changing the
frozen recipe.

## 2026-08-23 — Response-only labels use tokenizer prefix differencing

The pinned Qwen3.5 tokenizer warns that its chat template has no Jinja
`generation` block and returns an all-zero assistant mask. Relying on
`return_assistant_tokens_mask=True` would therefore fail the CUDA qualifier on
its first real training record and would also block seed-pilot preparation.

Response-only boundaries are now derived exclusively through two renderings by
the exact tokenizer with thinking disabled: the conversation before its final
assistant message with `add_generation_prompt=True`, and the complete
conversation with `add_generation_prompt=False`. The former must be an exact
text and token prefix of the latter. Prompt and tokenizer-owned generation
scaffolding receive label `-100`; the terminal answer and tokenizer-owned
end-of-turn suffix remain active. No Qwen token ID or delimiter is hard-coded.

Empty responses, non-prefix renderings, batched records, non-text messages, and
any completed turn over the frozen maximum length fail closed. Silent response
truncation is prohibited. The exact pinned Transformers 5.15.1 tokenizer proves
the boundary for all 1,449 imported train and validation records across the six
lanes. This is local preparation evidence, not a CUDA or Gate 0B pass.

## 2026-08-23 — Zero-task public diagnostic is admitted without weakening the contract

The frozen Multi-LiveCodeBench v6 importer admitted zero of 1,050 language
projections. Its complete, hash-bound exclusion report records ambiguous source
licensing and the absence of independently runnable reference and known-bad
artifacts. Gate 1 accepts `no_compatible_tasks` as the diagnostic outcome while
still requiring the exact 180-task private development baseline. No public
score is reported, and admission rules are not relaxed to manufacture one.

The seed-pilot token ceiling is the exact input-token count of its prepared,
balanced schedule. The prior 24-million-token placeholder contradicted the
three-effective-epoch cap and is retired. Validation loss is retained only as
a diagnostic; executable development results select checkpoints and promotion.

For the final decision, “statistically supported” is frozen as both a strictly
positive lower bound from the semantic-family cluster bootstrap and a
two-sided cluster sign-permutation p-value at or below 0.05. Row-level exact
McNemar is reported but does not override clustered dependence. This rule is
declared before any decision candidate is opened.

## 2026-08-23 — Gate 0B v4 exposed a container import-path omission

The v3 create request in `us-central1-a` failed before VM creation with
`ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS`. Its empty temporary network was
deleted. A zone-only v4 card retained the exact model, image, package set,
machine type, runtime recipe, and cost bound while moving to provider-suggested
`us-central1-b`.

The v4 VM verified every generation-pinned input and loaded the sealed CUDA
image. The qualification container then failed before model load with
`ModuleNotFoundError: No module named 'scripts'`. The image entrypoint executes
`/workspace/scripts/cuda/qualify.py`; Python therefore places
`/workspace/scripts/cuda`, not the repository root, on `sys.path`. Mounting the
repository at `/workspace` was insufficient for imports from `scripts.train`.

The repair exports `PYTHONPATH=/workspace` only inside the already
network-disabled, read-only qualification container. It does not change the
model, dependencies, kernel checks, training recipe, GPU allocation, or
response-only semantics. Historical cards remain immutable. A subsequent paid
retry requires a fresh card and workspace archive binding the changed runner.
The v4 composite backup, deletion gate, resource-absence proof, and
post-delete backup are sealed respectively by
`5fb8e2dae08ff7924a55f72cc5a1bad10eb37e508a5b11560ec112d6b0d02e40`,
`df4f793d8607364ee86e1f8ba04cf162491ed8f3209f2e50d3ef44a9c7abb64d`,
`8ac2896c7a397fc23649eb4ed02eaa53d5d4df112851cf0db14c4e335de79d9f`,
and `632b86742d1191f82dad8aec3f8c68eae2c754579e61f783387ff00a3d56a78a`.

The repaired workspace was reproduced byte-for-byte at SHA-256
`5435e154d27d6f96b5de2174c46651e2fc0b060d634344e38dea338ae38aa647`
and bound to pushed commit `d318f595c1319e32db37ea24f9a9c94515d79fa8` in the
v5 preparation card. V5 is not authorized by the prior card because it adds a
new maximum GCloud exposure; its requested incremental ceiling is USD 2.40.

## 2026-08-23 — Gate 0B v5 requires explicit ms-swift model selection

V5 verified the exact A100, BF16 support, CUDA/Triton/FLA backends and kernels,
all pinned packages, the sealed image, and the pinned Qwen model inventory. It
then failed before model loading because ms-swift 4.5.2 found two registered
types for the checkpoint architecture: `qwen3_5` and `ovis_ocr2`.

This is deterministic registry ambiguity, not permission to change the model
or packages. The repair calls ms-swift with `model_type="qwen3_5"` and
`download_model=False`, then still requires the resolved type and template to
both equal `qwen3_5`. A unit test proves both explicit arguments and the
fail-closed identity result. Historical evidence remains immutable.

V5's terminal backup, stopped-resource composite backup, deletion gate,
resource-absence proof, and post-delete backup are sealed respectively by
`49ea1bb8f3b14a806ae6deb301a0b54524078f19ebd1ad0eb07088ec49d78603`,
`98d623b6b7d6f3a9c064ddcfe2d5166800cd5ff0098ef55b0ec6193014126ba0`,
`e48a68d2ad21d629bb011eafe942735ddcef57d88c44351debc21ce07f2e5924`,
`5b145138f0f8fa7a6bc65ad8cec9add718caf3d3879f69b45490f618d6244fd3`,
and `b3f294f2608ce73ef059caf7126ebfe17a6a645548365d07c73b14baaa82479e`.

## 2026-08-23 — Gate 0B v6 separates model registration from template resolution

V6 proved that explicit ms-swift model selection resolves the pinned local
checkpoint as `qwen3_5`, but the qualifier incorrectly required
`ModelMeta.template` to equal `qwen3_5`. In ms-swift 4.5.2, the registered
Qwen3.5 template is attached to its `ModelGroup`; selecting an explicit model
type for a generically named local directory returns the type-level
`ModelMeta`, whose direct `template` field is legitimately `None` and whose
`candidate_templates` contains `qwen3_5`. Template selection is a separate
registry operation performed by `get_template_meta`.

The repaired identity check therefore remains fully explicit and fail-closed:
it calls `get_model_info_meta(..., model_type="qwen3_5",
download_model=False)`, requires the resulting model type to be `qwen3_5`,
then calls `get_template_meta(..., template_type="qwen3_5")` and requires the
resolved template type to be `qwen3_5`. It records the raw model-meta template
and candidate list as diagnostic evidence. This follows the pinned ms-swift
4.5.2 registry implementation; it does not infer success from a nullable
field or weaken the serving contract.

V6 stopped before model weights were loaded, inference ran, or an optimizer
step occurred. Its structured failure is sealed by
`3a1a81dd11b7f42cce2461988cc87dd77e15bd0d310e0a19548b3f236b5ff266`.
The 29-object terminal backup, 33-object stopped-resource composite backup,
deletion gate, exact resource-absence proof, and six-object post-delete backup
are sealed respectively by
`5e80ce5264f434b47102706e16a9fa2dd8a494f0a166cf83e01e45b2e944a0c2`,
`3f8e090c99829139a2cc7b4400f6e40a6e940eb05b8450ef5b2516e91d3b142a`,
`f1a27123f1362dcfe7c9d55049d4464cf39180d0339145a52c2a3a0a3faba83a`,
`05392d670d9617c3ffc46584db2531dec730e11c0055070da277696a5e902b0c`,
and `6db8cc64584a9895a00822273a01a142999e3020552df843f9c9c1dae72876bd`.
The exact VM, boot disk, subnet, and VPC are absent. Another GCloud attempt
requires a fresh execution card and explicit approval.

The complete 153,688-byte local v6 run archive is stored at GCS generation
`1787472611940869` with SHA-256
`dfbc2c8136b03e046245ca6fe318374bd2f54c341ef8c7ae0990ccc644639777`.
Its independent backup manifest is sealed by
`7e14c80111eefd4f0564f1cf8a9c57081385ea008b55f33796c00e9dfe502f54`.

The local v7 preparation card is sealed by
`408ab2dc4ad60f55b72867611e499d65d9394cb7a0c696f22018a859132dbdb7`.
It binds pushed source commit `2c509c77b07f6cc4b8dfe93ddd21d743ca51d93d`
and a twice-reproduced workspace archive with SHA-256
`9c8cca903eacb876ad9967a2bed23c16efdc7f1691c5c57f0ef2ecad434e20e1`.
The card remains explicitly unapproved; no v7 GCloud action is permitted until
Navneet Prabhakar approves its separate USD 2.40 incremental ceiling.

## 2026-08-23 — Exact Qwen structure deep dive supersedes Gate 0B v7

The exact pinned checkpoint was instantiated with empty weights under the
pinned Transformers and ms-swift contracts before another paid run. This
proved that Qwen3.5 exposes its vision tower at `model.model.visual`, its
language model at `model.model.language_model`, and its active cache setting at
`model.model.language_model.config.use_cache`. The earlier qualification and
production SFT paths attempted `model.visual` and wrote only the outer config,
so the explicit vision-freeze evidence was wrong and the real language cache
remained enabled during long-sequence backward.

A shared fail-closed structure guard now freezes all 297 vision tensors
(331,416,576 parameters), disables the actual language cache for training, and
restores it for serving. The exact empty-weight graph exposes 186 eligible
language linear modules. Adapter serialization now unloads the in-memory PEFT
adapter and reloads its saved bytes into the same frozen base, eliminating a
second backbone load. Qualification compares trained and saved/reloaded logits
at absolute tolerance 0.01, then requires the BF16 safe-merged logits to be
finite and close at absolute tolerance 0.25 and relative tolerance 0.02.

The production SFT engine uses the same structural guard and serialized
adapter lifecycle. Its held-out loss diagnostic now combines JavaScript and
TypeScript into one family before calculating the frozen five-family macro.
The 4,096-token synthetic probe reports 4,096 input tokens, 64 masked prompt
tokens, and 4,032 supervised tokens, and all qualification losses must be
finite and positive. Production SFT now reserves 600 seconds inside both its
wall and cost bounds for finalization and writes a resumable checkpoint at the
latest optimizer boundary whenever training stops bounded.

The full local suite passes 147 tests with one intentional integration skip.
The exact local reproduction and repair record is sealed by
`15330a2c847232d1acdf4c039a1bf34d5c9b7943fc5d12c0ff5e5e137ded5326`.
The temporary 287 MB diagnostic dependency directory was deleted afterward.

V7 is immutable but stale and cannot authorize execution of these changed
sources. V6 timing evidence also shows 433 seconds elapsed before container
qualification began, leaving only 1,367 seconds under v7 for model load,
11,318 backward tokens, serialization, safe merge, and merged checkpoint
write. The replacement card must bind the repaired commit and archive and add
controller and terminal-backup margin. No GCloud action occurred during this
deep dive.

The replacement v8 card binds pushed repair commit
`4873d337e62a57ec20ac43ff625616850a108607` and a twice-reproduced 1,770,400-byte
workspace archive with SHA-256
`1e4eabbd78e9829897345e14e374da6554c8d63c7552aa63c33db5fd41ffd652`.
It increases the total lifetime from 2,100 to 3,000 seconds, assigns 2,400
seconds to setup plus qualification and 600 seconds to terminal inventory and
backup, and requests an incremental ceiling of USD 3.32 using the last
verified hourly upper bound. The card is sealed by
`7cd638f18feff39e0cfe8301b627846a4f05d09ae281801f734189856693fd80`
and remains explicitly unapproved. Price must be reverified after approval and
before resource creation.

## 2026-08-23 — Gate 1 baseline evidence is runtime- and task-bound

The production baseline path was audited before any private development model
output existed. Four fail-open conditions were repaired: resumed files did not
bind the current implementation or backend runtime, duplicate task IDs and
backend output-count mismatches were not rejected, completed verifier futures
were not persisted until all generation ended, and Gate 1 trusted the
aggregate run file without reopening its 180 task evidence files.

The exact-Qwen development configuration now requires CUDA. The backend
installs and records the same pinned FLA recurrent compatibility alias used by
Gate 0 and, on CUDA, requires the external causal-convolution and FLA kernel
identities. Resume admission binds the runner, extractor, result builder,
sandbox verifier, runtime configuration, Qwen CUDA compatibility source,
backend identity, model, config, and task.

Gate 1 now validates exact coverage of all 180 frozen development tasks and
reopens every sealed task evidence file. It independently checks the original
task hash, model-rendered task hash, prompt hashes, model/runtime/config
identity, executable result seal, pass accounting, and run-row seal. An
aggregate file without those artifacts cannot open the gate.

Cross-template comparisons use the outer frozen source-task binding for
pairing. Each candidate still retains its independently hashed rendered prompt
and rendered-task identity. This is necessary for the later Ganesh v0.1
comparison because its Gemma chat template must not be forced to equal Qwen's.
No model output or decision prompt was opened during this repair. The local
baseline-runner readiness evidence is sealed by
`4afb29fcfbc1bda3252bd7bb4e96158ef92efb1fc1cda82b1308701b0e6cb848`.

## 2026-08-23 — Evaluation verifiers target the production Linux/AMD64 host

The frozen runtime configuration previously named six images that existed
only in the deleted local Docker store. The five reconstructed language images
were built for Linux/ARM64, while the Rust image came from an unrelated local
toolchain and had no recoverable public registry source. Loading those images
on an A100 Linux/AMD64 host would either fail with `exec format error` or make
the verifier environment unrecoverable. This is a measurement defect, not a
training defect, and it was found before any Qwen baseline output existed.

The runtime contract is therefore migrated to schema 3 and explicitly pins
`linux/amd64`, one locally resolvable project tag, its OCI manifest digest,
image-config digest, and complete RootFS DiffID chain for Go 1.22.12, Java
21.0.11, Node 22.23.2, TypeScript 5.5.4, Python
3.11.15, and Rust 1.85.0. Each project Dockerfile pins its base manifest.
TypeScript is installed from a versioned tarball only after its registry
SHA-512 integrity value passes; Python has no unnecessary package install.
Sandbox admission inspects the tag, ID, OS, and architecture before executing
with `--pull never`, `--platform linux/amd64`, and no network.

The portable Docker archive is not trusted merely because `docker save`
succeeded. Its audit binds every tag through the OCI index to the exact image
manifest and confirms that the referenced manifest, config, and layers are all
present. The adopted runtime config SHA-256 is
`3c639129f12323ed17127dc938ac6c0c9a5bea8af29332a6b38432c5c9de5d77`;
local readiness is sealed by
`36c070d9d8554c7f2999b5e4d5bbacbc67664eb64ac2dc34196534de155737a1`,
and the image-bundle manifest is sealed by
`aba48afc9f1a75d6911204fd1e49193a9908655ad7d0540ec9cd53c82396bac8`.

Docker Desktop's containerd image store reports the OCI manifest digest as
`.Id`, while classic Docker commonly reports the config digest. Treating that
field alone as portable identity would reject the same archive on one host or
admit an under-specified image on another. Schema 3 handles both stores: a
containerd descriptor must match both frozen digests, a classic store must
match the frozen config digest, and both must match the full RootFS chain and
platform. Result evidence uses the immutable repository-plus-manifest
reference and records the stable config digest as `image_id`.

Two forced uncached builds proved that BuildKit does not reproduce the exact
TypeScript layer metadata across builds even with `SOURCE_DATE_EPOCH=0`.
Therefore fresh builds are provenance diagnostics, not the execution
identity. The executable verifier set is the one internally checked portable
archive with SHA-256
`1c5c8196cdcc595d755ea506f774dee8a5699e495fe67d7c4441e7a06c21b972`.
Native hosts must download that exact private asset, verify its archive hash,
load it, and then prove schema-3 identity before any task runs.

This migration intentionally invalidates the earlier ARM64-bound
directionality evidence for current gate decisions. Those records remain
unaltered as historical evidence. The global decision-separation audit now
accepts only schema 3 and fails on an old image identity. A fresh native
Linux/AMD64 directionality pass is mandatory before Gate 1 may close; local
Apple-Silicon emulation is diagnostic only because Go startup consumed roughly
64 seconds against a 60-second production task budget even though the inner
test itself completed in milliseconds.

The first native dispatch, GitHub Actions run `32636800789`, proved the private
release asset could be downloaded, hash-verified, and loaded on Ubuntu AMD64.
It stopped before image readiness or task execution because the host inventory
used Docker's non-portable `dict` Go-template helper, which the runner rejected.
The repair requests `{{json .}}` and selects fields in Python. It also writes a
sealed controller-failure record and packages whatever diagnostics exist, so a
future early failure cannot again leave only an incomplete tar. The invalid
161,802-byte partial artifact from the failed run was deleted; the GitHub run
logs remain available. This run contributes no directionality or gate result.
