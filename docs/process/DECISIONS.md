# Decisions

## 2026-08-27 — Host campaign entrypoints must bootstrap the sealed workspace root

Gate 3 continuation attempt `20260827T113051Z` verified every generation-pinned
input, installed the offline Docker bundle, loaded the qualified CUDA image,
and then failed before candidate import, CUDA model work, canary evaluation, or
training. The host invoked the archived controller by absolute file path;
Python consequently placed `scripts/campaign`, rather than the archived
workspace root, on `sys.path`. Importing
`scripts.eval.verify_runtime_images` raised `ModuleNotFoundError`.

This is the same import-path class previously caught inside qualification
containers, but at a distinct host-controller boundary. The repaired
controller now bootstraps its repository root before project imports, while
the startup wrapper also supplies the exact archived workspace through
`PYTHONPATH`. Archive rehearsal executes the controller directly under
Python isolated mode with caller `PYTHONPATH` removed, so either an omitted
bootstrap or a missing archived module fails before another cloud launch.
The rebuilt evaluation-workspace manifest, deterministic archive, isolated
runtime rehearsal, and non-executable preparation are sealed by
`c0e1938c7d9574aaae128a787d38c41f3549b56bb9be99fae2f08c3e5008ff05`,
`3c738bf40fe3cda1fb62b4ae7b0d88da265a8318f082c63d91527cfb7c9cc6ef`,
`9c07e39823095cd93f26b580f238ecf9c5f23ad7c3d3d924109dd2f74fba93c1`,
and `915ddc4fdd90641283b9c49f3025f8519dda48c0f208582a566a1d1e623d9eb9`.

The failed attempt had one boot with automatic restart disabled and consumed
no optimizer step. Its terminal evidence is a strict sealed failure. Terminal
backup, finalization, exact four-resource absence, and final post-delete backup
are sealed respectively by
`206a9f8fa0c13a282614524675449712f03ae0dfdd3d44760f51b21c8958d30d`,
`63d08fa9b7be8dc2af81e4d0e228f227077f34a5f303a67435129fac3a7b7978`,
`db8c975853b9e7812b87cdaffb1c0af697e7e09cc2f502a4faae115f0abbc3f8`,
and `6526129fc7289a6dcdf52c32f855c75dc2240b055f490e8f6c0eb029f34c4633`.
No campaign resource remains and the approval is exhausted.

## 2026-08-27 — Final artifacts and release must bind the repaired run and exact runtime

A downstream readiness audit found that Gate 8 still admitted
`ganesh-mini-sft-run/v1`, while the repaired unique-row, five-family-weighted
training engine emits `ganesh-mini-sft-run/v2`. That stale contract would have
rejected a valid repaired run or encouraged selection of an obsolete recipe.
Release lineage now requires a complete v2 run, exact pinned Qwen revision,
successful save/reload evidence, and adapter files that rehash exactly before
merge. The run-evidence schema is updated to the executed v2 structure.

Artifact construction previously trusted the supplied base directory and an
unsealed GGUF record. It now reopens the sealed Gate 0 readiness report,
matches the exact upstream inventory, verifies every local base file, verifies
the sealed Gate 0 GGUF evidence and exact llama.cpp converter, quantizer, and
CLI binaries, and records those identities in the release manifest.

Laptop certification now takes the sealed artifact manifest rather than a
caller-provided revision string. It verifies the checked-out llama.cpp commit,
CLI binary, and both GGUF hashes before measurement. Release adjudication binds
that certification back to the artifact manifest, requires the exact same
frozen decision-task set for the Qwen, Ganesh v0.1, and quantization
comparisons, and proves that the decision candidate is the merged release
artifact. Publication independently requires the exact Qwen base identity and
the bound llama.cpp CLI identity. These are readiness controls only; no final
artifact, laptop result, release decision, or publication is claimed.

## 2026-08-27 — Continue Gate 3 from the completed candidate; never auto-restart training

The completed `1e-5` candidate from attempt `20260827T090603Z` is now a
minimal deterministic input bundle rather than a reason to repeat training.
The bundle contains only the final adapter and sealed run evidence. Its four
files are independently matched to the generation-verified terminal backup,
the source execution card, the strict terminal validation, the frozen model
revision, the 461,235-token/1,399-row epoch, and save/reload equivalence. The
candidate manifest, archive, run, and adapter seals are respectively
`5b882126fe59fcd28f6b1e9ffe578929b0b65ac0bd39fbd029f0baa0e3f325a7`,
`95a4a1054bab679dfd3255b752eac01ff3c6d42467304348a8ecff048dc998da`,
`d885af11f3c7346959b2fcfadd6b77c6009bca99410f527038f923ad09f1c5a0`,
and `6a6ccf88c85a5c16d3569bdedc8ccb5662eeb79f583006a777c7ba2d2f51fc8d`.

The continuation imports and revalidates that candidate against the current
frozen model, configuration, prepared-data manifest, recipe, token budget, and
adapter file hashes. It reruns the `1e-5` canary with the now-mandatory verifier
runtime, trains only the missing `3e-5` epoch, runs the same canary, applies the
frozen LR rule, and evaluates the selected candidate on all 180 development
tasks. Terminal admission distinguishes the imported candidate from the newly
trained candidate and independently verifies every terminal adapter file.

The earlier VM reset was an explicit bootstrap retry after a pre-training IAM
403, not a training restart. Nonetheless, the provider default had
`automaticRestart=true`. Future execution explicitly uses
`--no-restart-on-failure`; a host failure ends the attempt and preserves
checkpoint evidence instead of silently rebooting. The earlier preflight also
proved bucket access only for the signed-in launcher account, not for the VM
service account. The repaired launcher resolves and binds the exact Compute
Engine service account, reads the bucket IAM policy, and fails before uploads
or resource creation unless that identity has bucket-scoped object read/write
access. The VM is then created with that same explicitly bound identity. The
new non-executable
proposal is bounded to three VM hours, including a 30-minute backup reserve,
with a conservative USD 3.50 ceiling. It remains non-executable until fresh
price/quota/service-account-IAM checks, generation-pinned uploads, an exact
card, and explicit GCloud approval exist.

## 2026-08-27 — Gate 3 v2 first candidate is valid; verifier preparation must be explicit

Approved attempt `20260827T090603Z` repaired an initial bucket-IAM 403 by
granting the run VM's default Compute Engine service account bucket-scoped
object access and resetting the same VM. That reset occurred before model
loading, optimizer state, or training tokens, so it does not invalidate the
subsequent candidate.

The `1e-5` candidate completed all 1,399 unique rows, 461,235 input tokens,
242,406 supervised tokens, and 175 optimizer steps. Adapter save/reload had
zero maximum logit difference. Five-family validation record mean improved
from `0.3703169807` to `0.3598691403`; supervised-token mean improved from
`0.3766998041` to `0.3665855866`. This establishes safe learning and a valid
completed candidate, but validation loss remains diagnostic rather than a
promotion score.

The first canary generated five Go responses and then failed closed because
`ganesh-mini-go-verify:amd64-v1` was absent from the host Docker store. The
staged controller previously loaded verifier images only through the Gate 1
baseline helper. Gate 3 v2 intentionally reused the canonical baseline and
therefore never invoked that helper. No canary score is admitted, `3e-5` did
not run, and no data-sufficiency decision can be made from this attempt.

Verifier preparation is now a first-class campaign phase. Before any paid
candidate training, the host verifies the frozen verifier bundle and runtime
configuration, loads the exact archive, audits all six image identities, seals
the readiness result, and stops on any defect. The archived runtime rehearsal
requires this phase to occur before the candidate loop.

The local finalizer initially exposed a separate macOS Bash 3.2 defect when an
empty optional array was expanded under `set -u`. It failed before deletion,
after preserving the verified terminal result. The portable repair appends
optional arguments only when the array is non-empty. A fresh finalization pass
then accepted the strict sealed failure, deleted the exact stopped VM, disk,
subnet, and VPC, proved all four absent, and independently verified the final
post-delete GCS receipt. No run-scoped GCloud resource remains.

The next approved Gate 3 campaign should import the exact completed `1e-5`
adapter and its run evidence, evaluate its canary, train and evaluate `3e-5`,
then continue the frozen LR-selection and full-development contract. Retraining
the completed candidate is unnecessary unless a fail-closed import verifier
cannot establish its identity and completeness. Expansion data remains gated
on executable candidate evidence, which this attempt did not produce.

## 2026-08-27 — Rehydrate qualified inputs; never reuse deleted GCS generations

The first approved Gate 3 v2 invocation (`20260827T084230Z`) failed closed at
bucket preflight. The historical transfer bucket had been deleted, so the
generation-pinned model, CUDA-image, and offline-Docker-bundle URIs were no
longer resolvable. Preflight created no compute or networking resource; exact
VM, disk, subnet, and VPC absence was reconfirmed.

The qualified contents remained recoverable without changing the training
mechanism. The local model has the exact 13-file, 4,571,274,023-byte pinned
Qwen revision. The local CUDA image retains qualified image ID
`sha256:cdaf068ffcb933120181168ebf6ae1546ddf81e01b2ad006a1a18dd2e43d9860`.
The three pinned Ubuntu Docker packages and the complete bundle-file manifest
reproduce their historical hashes. New archive bytes are therefore admitted
only through a rehydration seal that binds those content identities to their
new archive hashes.

The Gate 3 launcher now uploads all three recovered archives to the new run's
immutable input prefix and binds their actual GCS generations. The executable
card validates those hashes and sizes against the rehydration evidence. The
guest must still verify every download and the loaded CUDA image ID. Deleted
bucket generations are never reconstructed, aliased, or treated as live
evidence.

## 2026-08-27 — Gate 3 v2 repairs the optimization objective before new data

The rejected pilot exposed two mechanism defects independent of GCP. The
prepared schedule balanced response-token totals by duplicating seed rows, but
the trainer averaged the already-token-averaged loss of every record equally.
The actual gradient objective therefore followed record frequency rather than
the declared five-family token balance. The v1 adapter also exposed every
eligible language-model linear projection in all 24 layers at rank 32 and
learning rates `1e-4`/`2e-4`; this was materially more aggressive than the
authorized v0.1 recipe and is consistent with the observed executable
regressions.

Gate 3 v2 keeps all 1,399 authorized source rows exactly once. Their 461,235
input tokens and 242,406 response tokens remain naturally imbalanced, but
explicit loss coefficients reconstruct an exact 20% objective for Go, Java,
JavaScript/TypeScript, Python, and Rust, with JavaScript and TypeScript at 10%
each. The prepared manifest proves one effective epoch in every lane and no
duplicate source ID.

The v2 adapter is rank 8/alpha 16 and targets 16 attention projections only in
layers 16–23: q/v in full-attention layers and fused qkv/output in linear-
attention layers. MLP and gating projections are excluded. The two frozen
learning rates are `1e-5` and `3e-5`. Each runs one complete unique epoch; the
selected complete candidate is the pilot, so no redundant third seed-training
pass occurs.

The adjacent-record three-spike guard is retired. V2 records raw loss min,
mean, and max, weighted optimizer-group loss, group objective weight, and
gradient norm. Only three consecutive post-warmup optimizer-group anomalies
against a rolling median/MAD and a 3x median ratio stop training. Anomalous
groups do not contaminate the reference window.

Development tranche 1 is frozen as a structural 30-task canary, five tasks per
lane. It may triage checkpoints or the two LR candidates but cannot select
promotion and can never enter training. The selected LR receives the complete
180-task development evaluation. Base and adapter validation losses are also
captured on the same 50 held-out records as record and supervised-token means;
they remain diagnostic, not promotion evidence.

The existing v0.1 corpus remains the authorized seed. New data is not admitted
before this controlled mechanism test. If v2 is safe but insufficient, the
next data step is a separately admitted 4,000–8,000-record execution-verified
diagnostic expansion emphasizing repair, APIs, parsing, error handling,
concurrency, and measured base failures.

The previous 18-hour/USD 19 campaign envelope is not reused. Executed timing
evidence shows 400,652 training tokens in 1,845 seconds and a full 180-task
candidate evaluation in 1,710 seconds. Gate 3 v2 therefore uses a four-hour VM
maximum, a 30-minute terminal-backup reserve, and a USD 5 absolute incremental
ceiling. This is a fresh Gate 3-only preparation and still requires explicit
GCloud approval before preflight, upload, or resource creation.

The maximum-runtime action is `STOP`, not `DELETE`. Google Compute Engine
supports both actions for standalone Flex-start VMs; `STOP` preserves the boot
disk until independent terminal-backup verification. The finalizer may delete
the VM, disk, subnet, and VPC only after the generation-pinned GCS inventory
and Gate 3 terminal contract pass. An integrity or deletion-gate failure backs
up the finalizer evidence and preserves the stopped resources rather than
entering quarantine teardown. Source:
<https://cloud.google.com/compute/docs/instances/create-flex-start-vm>.

Terminal admission independently opens both complete SFT evidence files, both
30-task canary runs and their sealed task results, the LR-selection bindings,
the selected 180-task run, and every promotion check. A phase-ledger entry by
itself is not sufficient. Gate 3 terminal output has its own v2 schema, while
the historical Gate 1 schema remains unchanged.

## 2026-08-27 — Seed pilot rejected; preserve canonical baseline and revise before scaling

Staged attempt `20260826T042539Z` revalidated the exact Qwen base at 20/180,
then completed the full 400,652-token LR `1e-4` candidate and its 180-task
development evaluation. The candidate passed 13/180, reduced five-family macro
from 10.0% to 7.33%, and produced 10 paired wins against 17 losses. Go gained
two tasks, Java and Python were flat by count, while JavaScript lost one,
TypeScript lost five, and Rust lost three. Better malformed/repetition counts
do not compensate for executable-correctness regression. LR `1e-4` is rejected
and cannot become Ganesh Mini 1.0.

LR `2e-4` reached 339,550 seen tokens before the predeclared
consecutive-loss-spike guard stopped it. Because that guard observes adjacent
heterogeneous record losses rather than a stable windowed divergence signal,
the stop is valid under the frozen card but is not sufficient evidence that
the optimizer itself diverged. No LR `2e-4` evaluation, LR selection, main
run, or promotion adjudication occurred. Another pilot must revise and reseal
both the seed-data strategy and the loss-anomaly contract; it must not merely
scale or promote either partial result.

The earlier admitted baseline from attempt `20260825T153823Z` remains
canonical. Revalidation has the same exact model identity, serving contract,
and 20/180 aggregate score but different raw CUDA outputs and run seal, so it
is retained as separate evidence rather than overwriting the frozen canonical
baseline.

The execution used automatic VM deletion. After credentials were restored,
the finalizer required the sealed launch identity, matching guest-terminate
and deferred-delete provider operations, and exact instance/disk absence before
accepting the already-deleted lifecycle. It then double-verified the complete
terminal backup, deleted the exact remaining subnet and VPC, proved all four
resource identities absent, and double-verified the post-delete receipt. This
recovery is valid only for an execution card explicitly binding
`instanceTerminationAction=DELETE`; a merely missing VM cannot pass it.

## 2026-08-25 — Generation-bound inputs are write-once within a campaign

Retry `20260825T055326Z` proved that content-identical re-upload is not safe
after a guest has received a generation-pinned GCS URI. The launcher replaced
the execution-card object's generation after VM creation, so the guest could
no longer resolve the card generation embedded in its metadata. This was a
control-plane ordering defect, not a content-hash mismatch or model failure.

All objects referenced by guest metadata are now write-once for the lifetime
of a campaign. After VM creation, the launcher may upload only a distinct
launch-receipt path. Tests reject any later bindings or execution-card upload.

A partial terminal prefix may be made deletion-eligible only after its original
generation-pinned object set and runtime inventory are independently verified,
the original inventory bytes are retained in the recovered envelope, wrapper
bootstrap hashes bind the card, and the partial/wrapper nonzero exit codes
agree. Recovery remains deletion-only and cannot admit a baseline.

## 2026-08-25 — Provisioning consumes the zone fallback; early wrapper failures remain deletion-safe

The approved staged fallback allowed `us-east1-d` only if `us-east1-c` failed
before provisioning. Run `20260825T052909Z` provisioned in `us-east1-c`, so the
conditional fallback is consumed and cannot be used as an automatic retry.
A new GCloud execution requires fresh explicit approval and a new card.

The run failed before baseline generation because the controller's attempt-ID
regex contradicted the launcher's canonical UTC timestamp. The contract is now
one exact format, `YYYYMMDDTHHMMSSZ`. This failure is not evidence against the
model, evaluation surface, fused-loss recipe, or L4 capacity; it occurred
before those assets were downloaded or executed.

An authenticated metadata-wrapper failure may occur before a controller can
create `runtime-files.sha256`. The finalizer may synthesize a deletion-only
terminal envelope only when the terminal prefix is empty, the wrapper prefix
independently verifies as the exact four expected objects, its two bootstrap
hashes match the card-bound wrapper and controller, its exit is nonzero, and a
diagnostic is nonempty. Such an envelope can unlock evidence-safe teardown but
can never pass Gate 1 or be admitted as a baseline.

## 2026-08-23 — Standard A100 v8 stopped before VM creation on cost

Navneet Prabhakar stopped the approved Standard `a2-highgpu-1g` Gate 0B v8
attempt after its reverified 50-minute upper bound reached `$3.31115417`, and
requested a cheaper alternative. The stop occurred before VM or boot-disk
creation, GPU allocation, model loading, qualification, or training.

The generation-pinned inputs remain in the run-scoped GCS prefix as historical
evidence. The briefly created subnet and VPC were deleted. Exact post-abort
queries prove the planned VM, disk, subnet, and VPC absent; the proof is sealed
by `940fbca74ba6ba349c58ff558313f4ef9d3e94f2e97027a8172a57b668233d86`.
No GPU compute charge was incurred. Negligible GCS storage/operation charges
are not asserted as zero.

The v8 plan is historical and cannot be resumed. Gate 0B remains closed.

Navneet clarified that the requested alternative must remain within GCP and
approved one non-Spot Standard `g2-standard-8` L4 attempt for at most 3,600
seconds and `$1.00` incremental cost, including temporary networking, GCS
backup verification, and teardown. BF16 LoRA remains primary. The existing NF4
QLoRA fallback may run only after sealed evidence records primary CUDA OOM or a
peak-VRAM ceiling breach. This replacement requires a new sealed execution
card; the earlier non-GCloud A40 proposal is withdrawn.

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

## 2026-08-23 — Native AMD64 evidence aligns development compiled timeouts

GitHub Actions run `32636958446` loaded and verified the exact portable image
archive, passed native runtime readiness, and completed all 12 development and
decision directionality tranches. Ten tranches passed. Development tranches 1
and 2 failed solely because six Go references crossed the development
surface's 30-second aggregate limit. Five produced no output before timeout;
`dev-t2-go-encode-csv-field` printed a successful `go test` result before
container teardown crossed 30 seconds. All 540 known-bad executions were
rejected as expected. This is infrastructure-timing evidence, not a behavioral
test failure.

All 15 nested and top-level JSON seals were independently recomputed. The
downloaded archive has SHA-256
`fadd5ab16d2ecf8d53ef6a19b4eded9d093bcf3b922b664db147a23fefb0e098`;
the GitHub artifact server digest is
`sha256:305d90cc547d372f685dcb37d53cf410e5552f6f699afe6c4bb953b523116926`.
The complete archive and a sealed receipt are preserved in the repository.

The development surface still used the obsolete 30-second aggregate limit
for every language, while the decision surface already used 60 seconds for
Go, Java, and Rust after prior native compilation flakiness. Because no Qwen
baseline output has been generated, the defect is repaired before measurement
by applying that existing compiled-lane rule consistently to development.
Prompts, references, known-bad implementations, tests, images, non-timeout
resource limits, and pass thresholds are unchanged.

This repair intentionally invalidates all prior development task and manifest
seals, development directionality evidence, the global separation report, the
development-only execution workspace, and the baseline-runner readiness seal.
They remain historical evidence and cannot support Gate 1. Fresh native AMD64
directionality and global separation must pass before baseline generation.

## 2026-08-23 — Native AMD64 verifier qualification passes after timeout alignment

GitHub Actions run `32639381229` executed the repaired contract at source
commit `bbdc7b3c43f3ee98e6bb9a81c4c2c304f1b8a86b`. All 12 development and
decision tranches passed: 540/540 reference solutions passed, 540/540
known-bad implementations were rejected, and no execution timed out. The run
used the exact schema-3 identities for all six pinned Linux/AMD64 verifier
images. All 15 JSON seals and every captured stdout/stderr hash were
independently recomputed.

The full inner evidence archive is preserved at SHA-256
`dc44846887b2570885c7d082a5bb812bac56e6144523461c73bb29e7612849e2`.
The passed-run receipt is sealed by
`1877bb99a1cab96d962c14301cb6b453785c9487af8692d4c3c130c08afec73f`;
the adopted top-level evidence by
`aed01c430f33c4580438b824993a9302e72726e4295c82b6e867745e81130cfb`;
and the replacement global separation report by
`a47d733caaf6d9db735a020dd182ab01cf1ffeb140f7984a846d5ac0d89cf53f`.

The development-only baseline workspace was rebuilt twice and reproduced the
same archive bytes, SHA-256
`d528f958778cecb0ddcceb273c09b4e934605811d68172bcf97255f353156d80`.
Its canonical manifest is sealed by
`c66b964fac10bb34863996b6b1dcbe94eccfa345c4d6471fc0cb46da6d0efb85`.
The seed manifest was regenerated through the pinned importer solely to bind
the replacement global-separation report; the train and validation JSONL
hashes remained unchanged. Gate 2 remains ready. Gate 1 now fails only on the
not-yet-executed exact Qwen base development baseline, which remains downstream
of a successful Gate 0B serving qualification.

## 2026-08-23 — Baseline execution requires a host-visible shared verifier path

The frozen model runner executes inside the qualified CUDA image but invokes
the six verifier images through the host Docker socket. A normal container
temporary directory exists only in the outer container namespace; passing it
as a child Docker bind source would make the host daemon resolve a nonexistent
path. This would fail after expensive model setup despite the runner and
verifiers being individually correct.

The baseline host controller now allocates verifier temporary directories on
one absolute path mounted identically into the model container. It also keeps
the outer container network-disabled and read-only, binds the exact model and
output paths over the sealed workspace, loads and re-audits the six pinned
verifier images, enforces a bounded named-container lifetime with forced
cleanup, preserves resumable generation/task evidence, and accepts completion
only for the exact Qwen revision with all 180 development tasks present.

The development workspace includes the controller and runtime-image auditor.
It was rebuilt twice with identical archive SHA-256
`e64e3e78d3e5d1e0d97479c7e92de25babc89ce761002271e4206733bddbb209`;
its canonical manifest is sealed by
`4d8e66ce89eabbcc08e6bf7520dd9b0baad5edc426ff27add07e4ab5aae5a8e9`.
This supersedes the preceding workspace only; it does not change or invalidate
the frozen tasks, native directionality evidence, global separation, serving
parameters, or Gate 2 seed bytes. The full suite now collects 171 tests: 170
pass, one integration test is intentionally skipped, and none fail.

## 2026-08-23 — Standard L4 proves the remaining Gate 0B blocker is memory

The approved Standard `g2-standard-8` launch first encountered provider
capacity exhaustion in `us-central1-b` before a VM or disk existed. The same
sealed infrastructure was retried in the provider-suggested `us-central1-a`
zone. The resulting L4 exposed 23,659,151,360 CUDA bytes and passed the exact
package, CUDA 13.0, cuDNN, Triton, external causal-convolution/FLA kernel,
Qwen revision, tokenizer/template, and non-thinking text-inference checks.

BF16 LoRA OOMed in the synthetic 4,096-token backward envelope after 91.20
seconds while requesting 96 MiB with 41.12 MiB free. This produced the sealed
`primary_cuda_oom` fallback trigger. NF4 QLoRA then repeated all identity and
inference checks and OOMed in the same envelope after 148.42 seconds while
requesting 512 MiB with 445.12 MiB free. Neither recipe started a training
record or optimizer step. Gate 0B therefore remains closed; the result must not
be described as training or qualification success. The run-result seal is
`1fffbc66e2bda232b7a5b866fcfaf3094fac1ea4c54c5d76d4e03902d7063f91`.

The 32-object terminal prefix was independently read twice by immutable GCS
generation and is verified under seal
`087d7c89b1806ddbe61772ba44ba8ce5ccbe17c8dd18fb122aa29189784d8f85`.
The VM, auto-delete disk, subnet, and VPC were deleted; all four exact names
are absent under seal
`eb8171a24a2c893a7fad2a7806fb4f187af7dbb4b86b2d630aee7882c359071d`.

The failed graph retained the frozen 331,416,576-parameter vision tower on the
GPU even though the product and dataset are text-only. BF16 storage for that
tower alone is 662,833,152 bytes. The next local repair therefore moves only
that already-frozen, text-inactive tower to CPU, empties the CUDA allocator,
and requires measured before/after release. The official bitsandbytes 0.49.2
`Params4bit.to` path moves packed data and quantization state across devices,
so the same fail-closed mechanism applies to QLoRA. The qualifier now enforces
the peak ceiling immediately after the envelope and every optimizer step;
production SFT enforces it after every backward micro-step. Model revision,
training data, response-only masks, 4,096-token length, rank 32, alpha 64,
optimizer, learning-rate candidates, and fallback order are unchanged.

This is a plausible capacity repair, not CUDA evidence. Another GCloud run
requires a new sealed card and fresh explicit approval.

## 2026-08-23 — Frozen-vision offload passes, but 4,096 tokens remain infeasible on L4

The approved bounded Standard L4 v3 retry executed source commit
`0791087e98da1073ed8ea641ff42e2f9f944c04f`. Exact package, CUDA, Triton,
external-kernel, model, tokenizer, template, and text-only inference identity
passed for both recipes. The repair then moved the frozen vision tower to CPU
and measured real allocator release: 662,833,664 bytes for BF16 and
190,087,680 bytes for NF4. This proves the repair worked as implemented.

It was not enough. BF16 LoRA OOMed in the 4,096-token synthetic backward
envelope while requesting 96 MiB with 73.12 MiB free and 21.96 GiB reported in
use. The correctly triggered NF4 QLoRA fallback OOMed in the same envelope
while requesting 512 MiB with 111.12 MiB free and 21.92 GiB reported in use.
Gradient checkpointing was active. Neither recipe started a training record or
optimizer step, so Gate 0B remains closed. The run-result seal is
`78a1af009066bc2403ad1e4d9ed6e3f865bb2666288bc4f27d95a61ca6d48ee7`.

All 32 terminal GCS objects were downloaded twice by immutable generation and
matched the VM-generated runtime inventory. The independent manifest seal is
`ed92e5f42f4a076a347685ab829fa07a6644cce7e7c19f0cb9c6985d37d97c8a`.
GPU billing stopped after 867.951 seconds. The VM, disk, subnet, and VPC were
deleted and are absent under proof
`cda4d4b4a44f52b25dddac1e2f6939390499352da57336fc49e868baef52c8af`.

The next change is measurement-driven rather than a blind memory tweak. The
frozen prepared training set contains 2,155 sampled records and 636,093 input
tokens. Its longest record is 2,938 tokens; all 50 validation records are at
most 919 tokens. Therefore a versioned 3,072-token training envelope preserves
every prepared record and token across all six compiler lanes. It removes
1,024 synthetic envelope tokens that no actual training record uses. The
model's serving context capability, revision, data bytes, response-only labels,
rank 32, alpha 64, optimizer, effective batch size, learning-rate candidates,
and fallback order do not change.

The CUDA qualification schema advances to v4 and the training config to v2 so
historical 4,096-token evidence cannot be confused with the new contract. The
3,072-token contract is local preparation only until fresh CUDA evidence
passes; any new GCloud execution still requires explicit approval.

## 2026-08-23 — 3,072 tokens nearly fits NF4 on L4 but remains unqualified

The approved Standard L4 v4 retry executed the versioned 3,072-token envelope
from source commit `b24124c71b8e6b60ca3619b2213482f7d9991267`. Exact model,
tokenizer, template, packages, kernels, GPU identity, and text inference passed
for BF16 and NF4. BF16 LoRA OOMed while requesting 2.84 GiB with 2.65 GiB free.
NF4 QLoRA then reached its backward envelope and OOMed while requesting 48 MiB
with 27.12 MiB free. The 21,894,267-byte shortfall is small but is still a hard
Gate 0B failure. No training record or optimizer step ran.

The result is sealed by
`67a691b9de7ed34a906b174a7bc4b0d80d23c42d93bee476c0987e687258d5c9`.
The 32-object terminal backup was independently downloaded twice, both
manifests equal
`b3d643fae56aa109c0ddd0d0f86e83e5f7fdca98fb899e03b977f2ade7e430e4`,
and both runtime inventories passed. Billing stopped after 853.409 seconds;
the exact VM, disk, subnet, and VPC were deleted and are absent.

Allocator fragmentation is not the primary next lever: PyTorch reported only
24.19 MiB reserved but unallocated. The measured prepared-data maximum is
2,938 tokens. Therefore the next admissible local capacity change is a
versioned 2,944-token training and qualification envelope, which preserves all
prepared records and tokens while removing another 128 unused synthetic
tokens. Rank, alpha, response-only masks, optimizer, effective batch, learning
rates, data bytes, model revision, serving contract, and fallback order remain
unchanged. This is a prepared hypothesis, not qualification evidence, and any
new GCloud run still needs fresh explicit approval.

## 2026-08-23 — 2,944 tokens exposes allocator segmentation as the next measured lever

The approved Standard L4 v5 retry executed the complete-corpus 2,944-token
envelope from source commit `1511d041a0fe343739fdbc9e00c76ad84334c23f`.
The initial `us-central1-a` create failed for provider capacity before a VM or
disk existed. The same approved single run was generation-pinned and moved to
`us-central1-c`, where exact model, tokenizer, template, package, kernel, GPU,
and text-inference identity passed for BF16 and NF4.

BF16 LoRA OOMed in the backward envelope while requesting 2,925,527,040 bytes
with 301,072,384 bytes free. NF4 QLoRA reached its backward envelope and OOMed
while requesting 73,400,320 bytes with 9,568,256 bytes free. The terminal
shortfall was 63,832,064 bytes. No training record or optimizer step ran, so
Gate 0B remains closed. The result is sealed by
`0519d41c66f5f410e9d6a4a01ff4f7c3af8650d0a86b7b40f9a25a666dd849c9`.

All 32 terminal GCS objects were downloaded twice by immutable generation;
the manifests are identical under
`bfed538722d9d23776e6bf75c51b6d024f86f0fe2e64f9f2571e9c30ea04d2cf`,
and both runtime inventories passed. GPU billing stopped after 864.951
seconds, with a compute upper estimate of `$0.20509533396908667`. The exact VM,
auto-delete disk, subnet, VPC, and matching router scope are absent under
`5af5685dd4f8b42118bfd2ad4148f5296ae61948d9dce31b28d46a363620be5c`.

This run changes the next lever. PyTorch reported approximately 91.49 MiB
reserved but unallocated at the NF4 failure, exceeding the roughly 60.88 MiB
allocation shortfall. Therefore `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`
is now an evidence-backed capacity hypothesis. It must be a versioned runtime
contract shared by qualification and production SFT, rather than an ad hoc VM
environment change. Sequence length stays at 2,944 because it already
preserves all prepared records; rank, alpha, response-only masks, optimizer,
effective batch, learning rates, data bytes, model revision, serving contract,
and fallback order remain unchanged. Fresh GCloud execution still requires
explicit approval.

## 2026-08-24 — Allocator retry aborted before allocation on regional L4 stockout

Navneet Prabhakar approved one Standard L4 Gate 0B v6 retry for at most 30
minutes and `$0.50` incremental cost. The generation-pinned request first
targeted `us-central1-c`. GCP returned
`ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS` before creating a VM or disk and
explicitly identified `us-central1-a` as the available replacement. The one
card-authorized capacity reallocation then returned the same stockout in
`us-central1-a`, with no further available zone. No VM, disk, GPU allocation,
qualification process, or compute billing existed in either attempt.

All six uploaded input objects were independently downloaded twice by
immutable generation. Both manifests equal
`606e36225d7901041e103f1729178d4147b73cb68b61456393bc89eb78ba7712`
and carry internal evidence
`e41edf8f752e3d0d9fbf81cfdae9d611c76ea2646670621396af49109731669c`.
The temporary subnet and VPC were deleted, and all exact run-scoped resource
names are absent under proof
`6f4c5509085c6e01489cd69552e273b9acdffb8871bb92a2ebff4f16d94ec9a0`.

This attempt supplies no evidence for or against expandable allocator
segments. Gate 0B remains closed. Repeating `us-central1` immediately is not
justified; the next bounded card should inspect and select Standard L4
capacity in another GCP region, or wait for regional stock to recover. Any
such GCloud inspection or launch requires fresh explicit approval.

## 2026-08-24 — A second Standard L4 region also stocked out before allocation

Navneet Prabhakar raised the approved regional Gate 0B ceiling to `$1.00` for
one 30-minute Standard L4 attempt. Read-only preflight chose `us-east4`: the
project had 16 unused Standard L4 quota, `us-east4-a` and `us-east4-c` both
officially supported G2, and the durable input bucket was already located in
`US-EAST4`. A conservative `$1.50` hourly guard plus `$0.20` reserve bounded
the attempt at `$0.95` before resource creation.

Both authorized zones returned
`ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS`. Neither create produced a VM or
disk, so GPU allocation, qualification, training, and compute billing were all
zero. All seven input objects were independently downloaded twice by immutable
generation; both manifests equal
`7e6347207863fa6ce1cfab8994031ead2a9d5bcc3e4a29d3ecb37c062566a3e3`.
The subnet and VPC were deleted, and all exact resource names plus the matching
router scope are absent under proof
`fae70b66d8043df4c08c049e1cd064e7c81db4d260c4fa9304b75e1c391c23f9`.

Gate 0B remains closed and the expandable-segment allocator remains untested.
After stockouts in both `us-central1` and `us-east4`, another blind retry in
either region is not evidence-driven. A fresh GCloud authorization should
first freeze a capacity-oriented path: a new documented G2 region with a
bounded zone set, or non-Spot queued/flex-start Compute Engine after its
scheduling, cancellation, and cost controls are verified.

## 2026-08-24 — Flex-start was accepted as pending but rejected immediately

Navneet Prabhakar approved one `g2-standard-8` L4 Flex-start request with a
two-hour provisioning window, 30-minute runtime, and `$1.00` incremental
ceiling. The `us-east4` preflight passed: 16 preemptible L4 GPUs and 5,000
preemptible vCPUs were unused, storage was co-located, exact resources were
absent, and the conservative cost guard was `$0.95`.

Compute Engine accepted the object with provisioning model `FLEX_START`, state
`PENDING`, request validity `7200` seconds, maximum runtime `1800` seconds, and
termination action `DELETE`. Nevertheless, operation
`operation-1787587773532-659cd363f0b3c-ec25845a-d2e2bda7` failed after 23.649
seconds with `ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS`. The VM never entered
`RUNNING`, so compute cost, qualification work, training records, and optimizer
steps were zero. A creating boot disk was automatically removed with the failed
request. Six GCS inputs passed two immutable-generation downloads under
manifest
`472df5930660c5e37cbdfd79115b9538ca04394921d3875cbad1e9b71ac6b2f1`;
the request, VM, disk, subnet, VPC, and router scope are absent under proof
`91953aa7e563fdb423e0508e4e06319fcb8aa3be703572b4b5f24e275d91080d`.

This is provider-capacity behavior, not evidence against the allocator or
training recipe. The next attempt must change capacity scope—another region or
a managed GCP job surface—not retry `us-east4` under the same mechanism.

## 2026-08-24 — Allocator alone is insufficient; fuse Qwen3.5 training loss

The approved `us-east1-b` `g2-standard-8` Flex-start run executed under prefix
`20260824T161956Z` on one 23,659,151,360-byte NVIDIA L4. Exact package, CUDA,
kernel, model, tokenizer, template, and non-thinking text-inference checks
passed. The frozen vision tower was offloaded and measured for both recipes.

BF16 LoRA then OOMed while the causal-LM loss requested 2.72 GiB. The correctly
triggered NF4 fallback, with `expandable_segments:True`, passed model structure
checks but OOMed during the 2,944-token synthetic backward envelope. It had
59.12 MiB free at a 46 MiB request and then failed a 20 MiB allocator mapping
with about 19.1 MiB free. No real training record or optimizer step ran. The
allocator hypothesis is executed and rejected as a sufficient repair. The BF16
and NF4 result seals are respectively
`ee7a07c910d059393b1ba15cc516c4bf78a02921fb85f6003140880802c82669`
and
`f1d43f17c03b1833635d563d83be9e0a81d1a3370dbd90aaa6743f71dc057c50`.

The failure size identifies the dominant allocation. At 2,944 tokens and a
248,320-token vocabulary, BF16 logits occupy 1,462,108,160 bytes. Transformers
upcasts them to FP32 for causal cross-entropy, requiring 2,924,216,320 bytes,
the observed 2.72 GiB request. The selected repair pins Liger Kernel 0.8.2 and
enables only its Qwen3.5 fused linear cross-entropy path. Training calls must
use `skip_logits=True` and fail closed unless the returned logits are absent.
Liger RoPE, RMSNorm, SwiGLU, and standalone cross-entropy replacements remain
disabled. Sequence length 2,944, rank 32, alpha 64, data, response-only masks,
optimizer, effective batch, learning-rate candidates, and serving contract do
not change.

All 32 terminal GCS objects passed two immutable-generation downloads. Both
inventories hash to
`04eb8aa2204555a33a1c8117c017c678c9f3448060ee968bf15c7461e7743585`.
The run-result, backup-verification, and teardown-proof seals are respectively
`c59d09d513a7e28f882d957e6ba22fbe2899edaf68cafea1a3ad4c0a17dba036`,
`3c289a929bde8b673b3e7a411989f6ec3ace0808052f347b4dd29c9946408843`,
and
`11d6011b335c5771c1adcf50a0a30825bd8ae50c7556e189df5bbf27bb53c034`.
The VM, auto-delete disk, subnet, VPC, and router scope are absent. The
conservative incremental upper bound is `$0.5686070833333333`, below `$1.00`.
Gate 0B remains closed until the fused-loss image passes fresh CUDA evidence.

Local prequalification subsequently passed. The rebuilt Linux AMD64 image is
`ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1-liger082`, ID
`sha256:cdaf068ffcb933120181168ebf6ae1546ddf81e01b2ad006a1a18dd2e43d9860`,
and size 8,372,032,086 bytes. A network-disabled smoke verified the exact
package versions and Liger Qwen3.5 `lce_forward_for_multimodal` contract with
`skip_logits`. Two independent workspace builds produced archive SHA-256
`de4cb24c5c78c501c02e1d31d532ba8ddad9d05e3fc83c822548c1253e2e0a94`.
The complete local prequalification is sealed by
`32db10f29dcf15969ccf89db18e55586c1941a758e31c3754bafada529063c0f`.
This is build evidence, not a CUDA or Gate 0B pass.

## 2026-08-25 — Fused linear cross-entropy passes Gate 0B on one L4

The approved `us-east1-b` `g2-standard-8` Flex-start execution ran under GCS
prefix `20260824T180957Z`. Liger Kernel 0.8.2 replaced only Qwen3.5 training
loss with `lce_forward_for_multimodal` and `skip_logits=True`; RoPE, RMSNorm,
SwiGLU, rank 32, alpha 64, optimizer, data, the complete-corpus 2,944-token
envelope, and serving behavior were unchanged.

Exact environment, GPU, Triton, FLA recurrent compatibility, package, kernel,
ms-swift, model-load, tokenizer/template, and text-only inference checks
passed. The frozen vision tower moved to CPU and released 662,833,664 CUDA
bytes. Fused loss did not materialize training logits. The full synthetic
backward envelope and all 16 real optimizer steps passed. Peak reserved VRAM
was 18,975,031,296 bytes against the frozen 22,548,578,304-byte maximum.
Adapter reload matched exactly; safe merge returned finite logits with a
maximum absolute difference of `0.125`. Qualification evidence is sealed by
`d5c8df044c0b49b1473a2a13e163bcd7acfc06da09b1ea9a0bea75aa1d493a6a`.

All 41 terminal objects, including the 4,426,558,864-byte merged checkpoint,
passed two independent immutable-generation reads under backup seal
`d4cd0d2f31f43e081183eef4ff191c2b3aa53eeb2e11763dd4dd723ad1f25cdf`.
The guest's 40-entry runtime inventory matched with zero missing objects or
hash mismatches. Provider auto-delete removed the VM and disk at the bounded
runtime; the subnet and VPC were deleted afterward. Run-result and teardown
seals are
`b29db7d69b7a9653b6be7b4f79390d00a62f2176228f7a995a5ff0b48f85c84d`
and
`95e4ed973cdc746795f0ee1b59045adbce1ceda8bb7af4a8902be86308bcf2f0`.
Even charging through deletion completion plus the frozen support reserve,
the conservative incremental upper bound is `$0.9686175`, below `$1.00`.

Gate 0B is passed. The next dependency is the exact 180-task upstream Qwen
development baseline and fail-closed Gate 1 report. This result establishes
technical trainability only; it makes no coding-quality improvement claim.

## 2026-08-25 — Gate 1 uses one 12-vCPU L4 with resumable evidence

Gate 1 has no admissible model output yet. Its local execution preparation now
binds the exact 180-task development workspace, native Linux/AMD64 verifier
archive, qualified fused-loss CUDA image, pinned Qwen archive, offline Docker
bundle, host controller, and metadata wrapper. The record is sealed but
explicitly non-executable until a fresh GCloud approval, account-specific
price/quota preflight, immutable GCS generations for the local inputs, and a
final execution card exist.

The proposed host is `g2-standard-12` rather than the previously qualified
8-vCPU shape. It still has one 24 GB L4, while its 12 vCPUs and 48 GB host RAM
match the frozen four-row generation batches and 12 concurrent verifier
workers. Generation, extraction, and network-disabled compilation overlap;
NVML is sampled every five seconds and resumable evidence is checkpointed to
GCS every two minutes. This is utilization alignment, not a model or
evaluation-contract change.

The proposed Flex-start request waits at most two hours and runs at most four
hours. The controller reserves 900 seconds for terminal inventory and backup,
requests guest shutdown only after the terminal backup succeeds, uses provider
`DELETE` at the maximum runtime as a backstop, and requires control-plane
VM/disk deletion and absence proof plus two immutable-generation reads of
every terminal object before Gate 1 admission. Public `us-east1` pricing
checked on 2026-08-25 lists `g2-standard-12` at `$0.790328877`/hour for DWS
Flex-start and `$1.000416348`/hour on demand. The conservative four-hour
compute bound plus a `$0.35` support reserve is `$4.351665392`; the proposed
absolute approval ceiling is `$4.40`. Current account pricing and quota must
still be checked after approval and before any upload or resource creation.

No GCloud API, CLI, upload, inspection, or resource action occurred during
this preparation. Gate 1 remains closed, and pilot training remains blocked.

## 2026-08-25 — Gate 1 execution and teardown are card-bound end to end

The Gate 1 preparation now includes the executable-card builder, execution
schema, terminal validator, finalizer, and terminal-validation schema. Its
replacement seal is
`53383b112d033b3e0a4bcbb60c1206f5adbabad70d6959702239a5acfc79078b`.
This supersedes only the earlier local Gate 1 preparation record; no frozen
evaluation task, serving parameter, or executed evidence changed.

An executable card can be produced only after the exact Gate 1 approval text,
a clean tracked source commit, current price/quota/machine preflight, exact
resource-absence and bucket round-trip checks, and generation-pinned uploads
all exist. It rejects a cost upper bound above `$4.40`, unpinned GCS URIs,
drifted local assets, substituted Gate 0B model/image/Docker objects, a mutable
boot-image family, or incomplete controller/wrapper bindings. The guest
controller independently compares every execution, cost, input, CUDA image,
controller, and wrapper metadata value to the sealed card before model or
verifier input download continues. The metadata wrapper supervises the
controller: success is shut down only after the terminal backup returns, while
a nonzero bootstrap/controller exit gets three bounded backup attempts for
both runtime state and wrapper diagnostics before shutdown.

The post-run finalizer requires the exact card source commit and stopped VM
identity. It captures provider evidence, appends it to the terminal prefix,
downloads every terminal object twice by immutable generation, reopens the
runtime inventory, and validates either the exact 180-task baseline or a
sealed failure. The common deletion gate now admits a `gate1-baseline` phase
but retains its exact inventory/provider-object equality requirement. Only
after that gate passes may the exact VM, disk, subnet, and network be deleted.
Their provider IDs are captured before deletion. The finalizer then proves all
four exact identities absent, uploads the teardown evidence and final receipt,
and double-verifies the completed post-delete prefix.

A sealed failure is deletion-eligible after durable backup but cannot pass
Gate 1. This distinction prevents an anomaly from retaining paid resources
without misrepresenting it as a quality result. No GCloud action occurred
while implementing or testing this local lifecycle.

## 2026-08-25 — Gate 1 launch is preflight-backed and failure-atomic

The prepared Gate 1 lifecycle now includes a single card-bound launcher and a
strict current-price evidence schema. The launcher checks the exact approval,
clean source commit, price ceiling and freshness, machine and boot-image
identity, applicable Flex-start quota, exact resource absence, and a GCS
round trip before uploading immutable inputs. It supports Google's documented
quota behavior: an established preemptible quota pool is mandatory once
present; otherwise the standard quota pool is checked as the permitted
fallback. Preflight evidence is uploaded and double-read before the first
temporary network mutation.

Large local inputs are hashed incrementally rather than loaded into memory.
The startup wrapper also verifies its own byte size and SHA-256 before invoking
the downloaded controller. If any command fails after resource creation starts,
the launcher backs and double-verifies its failure evidence first, then deletes
only the exact run-scoped VM, disk, subnet, and network that exist. It then
proves all four identities absent and double-verifies the teardown evidence.
If backup cannot be verified, deletion fails closed for operator recovery instead of
discarding the only diagnostic copy. Normal terminal execution still uses the
separate deletion-gated finalizer.

The replacement preparation seal is
`cda29e15803889910bb61a14f0ef6494a58a9a8d2f4b25afe7726f128da3371c`.
No GCloud command or account inspection occurred while adding or testing this
launcher. Gate 1 still has no model outputs and remains closed.

## 2026-08-25 — Successful Gate 1 evidence is admitted atomically after teardown

The finalizer now distinguishes resource deletion from model-result admission.
Both successful and failed executions remain deletion-eligible after verified
backup, but only a terminal result with `status=passed` can enter the canonical
baseline path. Admission occurs after the final teardown receipt has itself
been uploaded and independently double-verified.

The admission tool reopens the terminal-validation, finalization, and final
post-delete backup seals; requires the backed finalization receipt to match the
local receipt; validates the exact completed Qwen run; stages and rehashes every
downloaded output file; and atomically installs the directory at
`measurement/inference/development/qwen3.5-2b-base-v1`. It then rebuilds the
fail-closed Gate 1 report and requires `status=ready` before writing a sealed
admission receipt. Existing canonical output is never overwritten, and a
sealed failure is explicitly skipped.

The replacement preparation seal is
`cda29e15803889910bb61a14f0ef6494a58a9a8d2f4b25afe7726f128da3371c`.
No GCloud operation or model evaluation occurred while closing this local
post-run gap.

## 2026-08-25 — Zone stockout does not weaken gates; fallback stays within us-east1

The approved `us-east1-b` staged request failed before provisioning. The
provider's exact stockout stderr was visible interactively but was not captured
in the sealed run directory, so the project records only what the artifacts
prove: create exit code `1`, no provider create JSON, and verified absence of
the exact run-scoped VM, disk, subnet, and network after teardown. Future
launches capture create stderr before the failure trap backs evidence.

Capacity failure does not justify bypassing measurement or starting training.
Gate 1 remains the first VM phase. The same campaign may be retried only in an
explicitly approved G2/L4 zone. The launcher and executable-card builder now
accept `us-east1-b`, `us-east1-c`, or `us-east1-d`, bind the selected zone into
preflight, approval, and execution evidence, and reject every other zone.

The preferred next approval covers a sequential `us-east1-c` then
`us-east1-d` fallback, where the second request occurs only if the first fails
before provisioning. At most one VM may exist, and the existing 18-hour
runtime and USD 19 incremental ceiling are aggregate across the sequence. This
preserves region and pricing while avoiding a new approval cycle for another
zero-runtime stockout.

Failure cleanup still requires two independent immutable-generation reads
before deletion and again after absence proof. Those reads now execute with
bounded eight-object concurrency; verification semantics and deterministic
manifest ordering are unchanged.

The preparation also includes a canonical price-evidence builder. It accepts
only a timezone-aware observation no more than 24 hours old, an official
Google Cloud HTTPS source, finite decimal values, and a four-hour conservative
bound strictly below the `$4.40` ceiling. This removes hand-authored evidence
hashes while retaining the requirement to re-observe official pricing after
approval and immediately before execution.

## 2026-08-25 — Executed Gate 0B evidence replaces the stale local dependency failure

The historical Gate 0 report was generated on macOS and remained `not_ready`
because Linux-only training dependencies were intentionally absent there. That
report was never updated after the fused-loss L4 qualification passed, so the
seed-pilot controller still rejected `gate0_ready` despite the project state
correctly recording Gate 0B success.

The canonical repair does not reinterpret the old local result. A dedicated
admission verifier now cross-binds the sealed local fused-loss prequalification,
approved v14 card, immutable execution plan, exact CUDA image ID, passed
16-record/16-step qualification, fused-loss and serialization checks, double-
read terminal backup, runtime inventory, cost ceiling, infrastructure absence,
and independently backed post-run receipts. Its evidence seal is
`6047b522f697be73b7d781b4e5021c8e29d23441767d660db6f9badc50422fd4`.

The Gate 0 reporter was executed offline inside that exact local Linux/AMD64
image, where the full pinned dependency matrix passed. The resulting canonical
readiness seal is
`adde675ce4db676c635ba864af0dd356c292e352443d4ed88607079059b346cc`.
The seed-pilot prerequisite set now fails on exactly the unexecuted Gate 1
baseline. No GCloud operation or new model qualification occurred in this
promotion step.

## 2026-08-25 — One staged L4 campaign supersedes the Gate-1-only VM

Navneet Prabhakar approved replacing the four-hour Gate-1-only proposal with
one `us-east1-b` `g2-standard-12` Flex-start campaign: at most two hours of
provisioning wait, 18 hours of runtime, and USD 19.00 incremental cost. Early
shutdown and deletion remain mandatory. The public on-demand rate used for the
conservative ceiling is `$1.000416348`/hour; 18 hours plus the `$0.35` support
reserve is `$18.357494264`, below the approved ceiling. Current account price
and quota still must pass immediately before creation.

The VM runs the exact Qwen development baseline first. Training cannot start
unless the complete 180-task evidence opens Gate 1. It then runs the two frozen
400,000-token learning-rate candidates sequentially, evaluates each on the
same development surface, seals the predeclared LR selection, runs the exact
636,093-token main seed SFT, evaluates it, and applies the frozen Gate 3
promotion rule. This is one capacity allocation, not one ungated job.

The development and seed corpora remain in separate content-sealed workspaces.
Evaluation containers cannot see training data; training containers receive
only seed data and sealed Gate 0/1/2 reports and cannot see evaluation tasks.
All model containers remain network-disabled. Changed runtime evidence is
incrementally synchronized to GCS every two minutes, the terminal inventory is
independently downloaded twice by immutable generation, and the VM and all
temporary networking are deleted only after verified backup. Any failed phase,
OOM, non-finite loss, evidence mismatch, cost/time breach, or backup anomaly
stops subsequent phases. A valid base baseline is still admitted after
teardown if a later training phase fails, preventing needless remeasurement.

## 2026-08-25 — Evidence IDs and Docker names are separate contracts

Canonical campaign attempt IDs remain exact uppercase UTC timestamps in
execution cards, ledgers, labels, GCS prefixes, and validation receipts. Docker
container names are a derived transport identifier and are normalized to
lowercase without changing the evidence ID. This derivation applies uniformly
to the base baseline, both learning-rate candidates, the main SFT, and every
candidate evaluation. Production-format regression tests are required; a
generic lowercase test slug is insufficient coverage.

Live backup logs are never members of the directory being synchronized. The
checkpoint command writes outside the evidence tree; checkpoint and NVML
writers are stopped and awaited; the fixed checkpoint log is copied once; and
only then is the terminal inventory hashed. Terminal evidence with any
inventory mismatch remains deletion-motivating but result-inadmissible. If
that fail-closed check prevents automated cleanup after the VM is already
stopped, exact resources may be deleted under the existing teardown approval
only after the failure envelope is durable, followed by exact-name absence
proof and independently verified GCS backup.

## 2026-08-25 — VM archives must equal current source, not merely old manifests

The recurring Gate 1 failures had two independent classes: provider capacity
before provisioning and preventable integration defects after provisioning.
The last three provisioned failures all stopped before the first baseline
task. The decisive defect in attempt `20260825T061157Z` was split-brain
execution: the launcher and controller came from current `HEAD`, while the
controller invoked campaign and baseline-host modules extracted from an older
evaluation archive. Unit tests imported current source, so they passed without
testing the bytes the VM actually executed.

Preparation now rehashes every file named by both workspace manifests and
requires exact equality with current repository source. The evaluation archive
contains only its actual inference/campaign runtime files; the training archive
contains only its actual preflight/SFT runtime files. Both archives are rebuilt
deterministically. The training manifest records a repository-relative archive
path so a fresh Linux checkout can reproduce it. A dedicated rehearsal safely
extracts the sealed evaluation archive, imports its modules in an isolated
Python process, and exercises the exact failed uppercase UTC ID across the base
container, two LR train/eval pairs, and main train/eval pair. Local release
preparation rebuilds both workspaces before running the full suite and this
rehearsal. The preparation builder requires the rehearsal seal to bind the
current evaluation manifest and archive, so launch preparation cannot bypass
it.

The three sealed prepared seed artifacts (manifest plus train and validation
JSONL, about 7.4 MB) are versioned in the private repository. They are required
source inputs for deterministic training-workspace reconstruction; leaving
them only in an ignored local directory made fresh-checkout validation
illusory. Large model, image, checkpoint, and output artifacts remain excluded.

Terminal integrity and resource lifecycle are also separate decisions. Strict
inventory validation remains mandatory for result admission. If it fails after
all GCS objects have been downloaded and generation-verified and the exact VM
is stopped, a quarantine deletion gate may authorize teardown using the exact
card-bound resource identity and provider evidence. Quarantine finalization is
explicitly marked `complete-quarantined` and is never admission-eligible. This
prevents corrupted evidence from becoming a benchmark result without leaving a
paid VM stranded. No GCloud command was executed during this repair.

## 2026-08-25 — Sealed workspaces must remain bytecode-immutable during imports

Provisioned Gate 1 attempt `20260825T085926Z` proved that archive/source
alignment at launch is necessary but insufficient. Both extracted workspace
file sets initially matched their manifests. Importing the baseline module on
Linux then created `__pycache__` files inside the evaluation root, and the
baseline helper's repeated identity check correctly failed before generation.
Mac rehearsals had redirected bytecode outside the workspace and therefore did
not reproduce the mutation.

All VM-host Python execution against sealed workspaces now disables bytecode at
the interpreter boundary with `-B`; the campaign repeats the guard through
`sys.dont_write_bytecode`. Runtime rehearsal forces in-tree cache semantics,
imports the archived modules, and requires the post-import file set to equal
the manifest exactly. Ignoring `__pycache__` during verification was rejected:
the correct invariant is that execution must not mutate a sealed input, not
that the verifier should tolerate undeclared files.

The failed attempt is not baseline evidence and cannot open Gate 1. Its strict
terminal backup, deletion gate, exact-resource absence proof, and post-delete
backup are valid lifecycle evidence only. A fresh GCloud approval is required
for another campaign attempt.

## 2026-08-25 — Repository CI is disabled

The project does not use GitHub Actions. Both the push-triggered Gate 1 runtime
integrity workflow and the manually dispatched native AMD64 directionality
workflow are removed, and Actions is disabled for the repository. Historical
workflow results remain immutable execution evidence but create no continuing
CI dependency. Required workspace reconstruction, unit tests, runtime-bundle
rehearsal, and preparation sealing run locally or inside an explicitly
approved compute campaign.

## 2026-08-25 — External runtime state cannot be mounted beneath a sealed workspace

Attempt `20260825T103213Z` established that making `/workspace` read-only while
binding model, adapter, configuration, or output paths beneath it is not a
valid isolation design. Docker must create a missing nested mountpoint before
starting the container; it cannot do so through an already read-only parent
bind. Adding empty directories to the archive was rejected as a brittle fix
because every future external path would depend on archive layout.

The durable contract is one sealed read-only `/workspace` bind plus independent
top-level mounts for runtime state. The evaluator accepts explicit model,
adapter, and output locations while continuing to hash the frozen config and
emit its logical evidence paths. Campaign code constructs external mounts
through a guard that rejects `/workspace` and every descendant. The archived
runtime rehearsal executes both the base and campaign mount builders and
enforces this invariant before a preparation seal can be issued.

The failed run remains lifecycle evidence only and cannot open Gate 1. All
temporary GCloud resources were deleted after verified GCS backup. Another
cloud campaign requires fresh explicit GCloud approval; local repair, tests,
repository push, and preparation sealing do not.

## 2026-08-25 — CUDA serving compatibility must not import training code eagerly

Approved attempt `20260825T140310Z` provisioned one `g2-standard-12`
Flex-start L4 VM in `us-east1-c`. Fresh price, quota, exact-resource absence,
GCS round-trip, and immutable generation-pinned input checks passed. Offline
Docker/NVIDIA setup passed, the loaded CUDA image matched the expected image
ID, and all six native AMD64 verifier images matched their sealed config and
manifest identities.

The campaign stopped before model loading and before the first baseline task.
The isolated evaluation workspace correctly excluded `scripts/train`, but
`scripts.cuda.qualify` imported `scripts.train.qwen_runtime` eagerly even
though evaluation uses only `install_fla_recurrent_compatibility` and
`kernel_identity`. The exact result was `ModuleNotFoundError: No module named
'scripts.train'`. No inference token or optimizer step ran, and the failed
attempt is not baseline evidence.

Terminal validation is `sealed-failure` under seal
`915befcfb5d8c93d39d369a84abcadb543ffbe122968b6983ef6ed4521d27aaf`.
Terminal backup seal
`05f01002f1aa050462f6b1c0c65b7a11e82857a59700f5e858a2e789f119e165`
passed before deletion. Deletion gate seal
`409bf6ab0c83d7f9a5507c85099d48c39aee7d2551708c8b65411e21d7929480`
and absence proof
`1b378af04f32c43c08a46b644a6d64886d4185d1bd02c63e6e8d03901be94f65`
prove the exact VM, auto-delete disk, subnet, and VPC absent. Finalization seal
`9336e411e964793c577e8d3f779e4c7e69c9214583f7056c420c7e978861a45d`
and final post-delete backup seal
`0052b790551123e32696bdb6c9f82403c20a62dbebb0ca97e2a414ca46d5e687`
close the lifecycle.

Training-only qualification imports are now lazy. The sealed-archive runtime
rehearsal imports the exact CUDA serving helpers while asserting that the
archive contains no `scripts/train` directory, so this dependency-boundary
failure cannot pass preparation again. The resealed evaluation archive,
rehearsal, and preparation hashes are
`8af2f7d2b92b66d6919ee15d5eb06fb2701e678ef8302d022eae77a94abfb2a1`,
`ba782354c142114121cc34d557b19ca2852b9dc48fe58b97fccb2f63de4a7da3`,
and `d51f342615e3fa77203df45701d757dae8a821938a0ad964ce60c4b813db74ec`.
Another cloud execution requires fresh explicit GCloud approval.

## 2026-08-25 — Verifier resource failures cannot become quality scores

Approved attempt `20260825T143537Z` was the first staged Gate 1 run to load the
exact Qwen base and generate development answers. Four of four inspected Go
tasks were recorded as failed because `go test` could not fork compiler tools
inside the task's 64-PID cgroup. Docker's one-CPU quota throttles time but does
not change the host CPU count observed by the Go toolchain, so the compiler
still scheduled excessive parallel jobs on a 12-vCPU G2 host. At least one
answer was syntactically valid-looking; these results therefore measure the
host boundary, not model quality.

The 64-PID security limit remains unchanged. Verifier containers now set
`GOMAXPROCS=1`, `GOFLAGS=-p=1`, and `CARGO_BUILD_JOBS=1`, keeping compiled
toolchains within that boundary. Known infrastructure signatures—including
PID exhaustion, Docker/OCI failures, missing process exit codes, and container
runtime exit codes—raise a runner error and cannot be persisted as ordinary
model failures. This is enforced in both the production batched evaluator and
the synthetic runner. Batched generation also trims each row at its first EOS;
padding emitted while longer batch peers continue is no longer stored as model
output.

The live campaign was stopped by removing only the base container, allowing
the controller's normal failure, terminal-backup, and shutdown path to run.
Terminal backup seal
`fc20c38eea9ab2c3b630768dc8364760ed1bb1c501044c9feb49e3e54a14c313`
contains 50 verified objects. The incomplete baseline correctly has no
admissible run; terminal validation is quarantined under seal
`2cb8485e8a54989678ae203740966b7f12ba8b335cc5478877895596d17789a6`.
Deletion gate
`e67da65d1062a9719cf8a2c19f5b46c71a9fc72cf14e6df71c5f7501c3b5a27e`,
absence proof
`3303b338e160fccd866422c870a602b6887230e01145627fc769f737bdc41af3`,
strict finalization
`8eb2de2fec896bfb8ae361004faa1d20e94edc7b472be8e7890ca4cb22328307`,
and final post-delete backup
`f04a3555027a7cd9c7ecbfc4210ca6edd50d1d88957c592153611435864dbb73`
close the lifecycle. Provider start-to-stop time was about 1,135 seconds; this
is a runtime bound, not an asserted invoice amount.

The repaired evaluation archive, manifest, runtime rehearsal, and preparation
seals are
`9fe60b7b4526fa34d60eb7523494a738762069e47e4d202bcdbf6f80c6115138`,
`f6551430af4c5a2cd2ad5d7bcbdcf4daf3105136682c146535e2a2a11c2da5b0`,
`7c280c5a5c8ec8c28891818d5171dbdea3507dc11eca6799f86cde2d71d50406`,
and `6ce15ca15de7f7bcad2402d836de155ea5e65b411ac8bec883b0977cb3a3d937`.
Six-language Docker integration and the complete local suite pass. Training
remains blocked until a fresh exact-base baseline opens Gate 1.

## 2026-08-25 — Gate 1 admitted; CUDA counters require an initialized device

Approved attempt `20260825T153823Z` completed the frozen 180-task exact-base
development baseline without verifier infrastructure errors. The base passed
20/180 overall: Go 0, Java 2, JavaScript 4, TypeScript 6, Python 5, and Rust 3
out of 30 tasks per lane. The canonical run seal is
`a04361a047080bc479328d52d8be23fabcedb2b42ebbf0a059775e32db823ceb`;
365 admitted files are bound by admission seal
`c7d7d33d59d804a3dcd1b0f98e5aed9f409b229a3c31d85f1ef19f5b021faa62`.
Gate 1 readiness is now `ready` under seal
`d827ece3d324633a6fc6b0a46be55dcd87a87fb565358d3f2704806ced154971`.

Training preflight passed and preserved evaluation/training isolation. The
first LR candidate then failed before model loading, token accounting, or an
optimizer step because the exact Torch/CUDA build rejected
`torch.cuda.reset_peak_memory_stats(0)` with `Invalid device argument` before
an active CUDA device had been explicitly established. Peak-memory accounting
must still begin before model loading, so the repair selects `cuda:0`, calls
CUDA initialization, and resets counters on the current device with no integer
argument. A production call-order regression test prevents the pre-load reset
from moving or reverting to the rejected form.

The training archive, manifest, and non-executable preparation are resealed at
`d06c4d2a71828c61514d62ae3d1c8dccf6b5e8e9d9d403527b7f95833d919688`,
`9af762e484c04f54e1728adca9d87a9214c991cfed78bc9cc78a656bfa45fe19`,
and `b38dcbbb4a8ba0bbbe5a9bbac138ebe335cc0f14e9ceb39b0a171882374cdc5a`.
The archive rehearsal and full local suite pass.

Terminal validation seal
`c299e90402004e9ce014f0b04f3fa0f2ae9d33211d3fa5971a7c1f58aecad351`,
strict finalization seal
`94963d2fd2deed795d6a883633f2d8cb2064e36cd4b8c6426c95720a1cf36f5a`,
absence proof
`1bb8e75d6662083f8da1b27655507952a913c19234b21ecfd7c35b3a1264e7c1`,
and final 14-object backup seal
`9a34c63e37a75211234edb5de977c4da5f92e4381e352b4b85fce4a319fbf419`
close the attempt. The exact VM, auto-delete disk, subnet, and VPC are absent.
The consumed approval authorizes no second VM; continuing Gate 3 requires a
fresh explicit GCloud retry approval.

## 2026-08-27 — Release evidence is transitive and publication is fail-closed

Gate 8 may not trust aggregate scores or an arbitrary list of sealed files in
isolation. Every decision comparison now seals the exact base, candidate, and
frozen source-task result sets. Release adjudication requires the exact Qwen
base identity, a fresh Ganesh v0.1 rerun, the complete 360-task/60-per-lane
contract, seed and readiness lineage, the selected training execution card and
run evidence, artifact-to-run binding, six-lane BF16/F16/Q8 export
equivalence, Q8 decision retention, and hash-bound laptop certification.

The GGUF decision path uses the pinned local llama.cpp revision through one
loopback-only `llama-server`, with reasoning disabled, greedy generation, raw
token evidence, and the existing network-disabled verifier harness. Hugging
Face publication is a separate fail-closed operation: it accepts only a sealed
`release-eligible` decision, rehashes every merged and GGUF artifact, uploads
only release artifacts, aggregate evidence, and the model card, then verifies
the resulting repository commit. Private benchmark prompts and raw outputs
are never publication inputs.

## 2026-08-27 — Correct the data before training again

The completed seed result is negative executable evidence: the `1e-4` adapter
passed 13/180 development tasks against 20/180 for the exact base. Lower
validation loss does not override that result. More epochs, a larger LoRA
rank, or immediate preference optimization would reuse an insufficient signal
and are rejected.

Expansion v1 is fixed at 6,000 execution-verified SFT rows with Go, Java,
Python, and Rust at 1,200 each; JavaScript and TypeScript at 600 each; and a
3,600/2,400 generation/repair split. Authenticated Codex CLI 0.144.4 with
`gpt-5.6-sol` at medium reasoning may draft tasks and independent tests in
separate ephemeral, schema-constrained contexts, but its output has no
privileged status. Every admitted row must pass a
network-disabled behavioral harness, reject at least one known-bad solution,
and clear exact/fuzzy separation from all evaluation surfaces. Public
benchmark tasks remain prohibited. Another model-training run cannot begin
until the dataset is sealed and the stratified quality sample passes.

## 2026-08-27 — Codex CLI teacher requires isolated critics and executable admission

The first one-per-lane Codex CLI qualification admitted only Java. Go lacked
the verifier's required module support file, JavaScript used the wrong module
contract, TypeScript tests required unavailable Node types, Python contained a
real alias-preservation defect, and Rust tests constructed an impossible
boundary value. Treating structured output as qualified data would therefore
have admitted a broken corpus.

Explicit pinned runtime contracts and Go module support raised admission to
4/6. An architect critic, isolated from tests and evaluation data, corrected
the JavaScript reference. A test critic that saw the TypeScript specification
and test only—not reference or known-bad code—corrected its strict-compiler
failure. The combined six-row qualification passed 6/6 with zero tool events
under admission seal
`0aeedf655a23eacf67cab8d10bf8a4a40e3366c94b779f1734c8b22aa3dece36`.
This qualifies construction of a 60-row tranche, not the 6,000-row dataset.
The iterative qualification consumed 523,568 input and 82,931 output tokens;
full-scale construction must demonstrate materially better batched efficiency
before it is accepted as the production method.
