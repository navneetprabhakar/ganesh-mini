# Project state

Last updated: 2026-08-23

## Current gate

Gate 0B and Gate 1 preparation in parallel:

- production Linux CUDA BF16 LoRA qualification, with NF4 QLoRA as fallback;
- frozen development and decision surfaces plus exact Qwen base baselines.

Local Apple runtime qualification and the pinned Linux CUDA image prebuild are
complete. The latest Standard A100 retry passed package, A100/BF16, CUDA,
Triton, causal-conv1d, and the external FLA chunk-training kernel, but exposed
an exact Transformers 5.15.1 / FLA 0.5.2 recurrent-symbol mismatch before
model loading. The pre-import fused-kernel repair and the subsequently found
all-zero tokenizer assistant-mask repair are locally validated. Gate 0 remains
fail-closed until the repaired qualification executes on CUDA under a fresh
card.

## Completed

- Inspected the committed Ganesh v0.1 plan, training, data-rights, and
  benchmark history without modifying its dirty working tree.
- Verified that `Qwen/Qwen3.5-2B` is an Apache-2.0, post-trained, dense 2B
  checkpoint intended by Qwen for task-specific fine-tuning.
- Verified current Transformers and ms-swift support for Qwen3.5's hybrid
  Gated DeltaNet/full-attention architecture.
- Produced an initial plan and a second-pass critical revision.
- Defined separate Q8/8 GB and F16/16 GB laptop acceptance envelopes.
- Recorded the user's 2026-08-22 authorization to reuse the cleaned Ganesh
  v0.1 training data for the same purpose on the Qwen3.5 backbone.
- Located a 1,399-row training and 50-row validation seed inventory in the
  committed Ganesh source tree across all six compiler lanes.
- Pinned Qwen revision
  `15852e8c16360a2fea060d615a32b45270f8a8fc` and verified its immutable
  13-file, 4,571,274,023-byte upstream inventory without downloading weights.
- Implemented a fail-closed Gate 0 readiness reporter. Gate 0 remains
  `not_ready` until the runtime and smoke evidence exists.
- Deterministically imported all 1,399 training and 50 validation rows from the
  pinned Ganesh commit. No duplicate IDs or conversation groups were found.
- Implemented strict six-lane task/result/comparison schemas, paired scoring,
  five-family macro weighting, and a network-disabled Docker verifier.
- Proved reference-pass and known-bad-fail directionality on synthetic fixtures
  for all six lanes. Full unit suite passes; the Docker integration passes.
- Downloaded and byte-verified the exact 4,571,274,023-byte Qwen checkpoint.
- Locked the qualified Apple environment at Python 3.12.11, PyTorch 2.13.0,
  Transformers 5.15.1, and PEFT 0.19.1.
- Passed text-only non-thinking BF16 inference on MPS.
- Inspected 186 language-model linear modules across 12 target suffixes and
  verified adapter gradients while excluding 99 vision/head modules.
- Passed a 16-record LoRA train/save/reload/safe-merge smoke.
- Converted and ran both F16 and Q8_0 GGUF artifacts using pinned llama.cpp;
  the tiny runtime smoke measured 25.5 and 41.6 decode tokens/second,
  respectively. These are smoke measurements, not final laptop benchmarks.
- Added a fail-closed seed-pilot controller binding model, data, prerequisite,
  balancing, LoRA/QLoRA recipe, checkpoint, resume, budget, and stop-condition
  evidence.
- Audited the pinned Multi-LiveCodeBench v6 slice. All 1,050 language
  projections were excluded because none satisfies the strict task contract;
  no benchmark prompts were redistributed or admitted.
- The recurring 30-minute goal-alignment heartbeat was disabled at Navneet
  Prabhakar's explicit request; no replacement deviation check is active.
- Selected BF16 LoRA as the primary SFT mechanism and NF4 QLoRA as a
  measurement-gated fallback. The controller enforces separate recipe hashes
  and sealed fallback evidence.
- Implemented the exact Qwen base-inference runner with official non-thinking
  prompt rendering, bounded greedy generation, extraction, atomic evidence,
  resume accounting, and verifier integration. Its synthetic harness proof
  completed 6/6 executions but solved 0/6 underspecified synthetic tasks; this
  is runner evidence, not a base benchmark.
- Authored and sealed private development tranche 1: 30 tasks, five per lane,
  balanced 15 generation/15 repair. All prompts expose exact API/file contracts
  and examples; repair prompts include buggy source. Seed overlap is zero, all
  30 references pass, all 30 known-bad implementations fail, and timeouts are
  zero.
- Implemented the production CUDA qualification image/controller with BF16
  LoRA primary on at least 24 GiB and guarded NF4 QLoRA fallback on at least 16
  GiB. Static validation passes, but no CUDA execution is claimed because no
  non-GCloud NVIDIA provider credential, CLI, or local GPU is available.
- Authored and sealed development tranches 2–4: 90 additional tasks, bringing
  the private development surface to 120/180 tasks, 20 per lane. Across the
  three tranches, all 90 references pass, all 90 known-bad implementations
  fail, exact/normalized seed and cross-tranche overlap is zero, and timeouts
  are zero.
- Authored and sealed development tranches 5–6: 60 additional tasks, completing
  the private development surface at 180/180 tasks, 30 per lane and 90 each of
  generation and repair. Across the two tranches, all 60 references pass, all
  60 known-bad implementations fail, exact/normalized seed and cross-tranche
  overlap is zero, and timeouts are zero. The full local suite passes with one
  intentional integration skip.
- Completed the authorized bounded GCloud A100 Gate 0B execution without making
  a qualification claim. Three terminally sealed attempts exposed, in order:
  a missing Docker package in the pinned DLVM image, an optional BuildKit cache
  directive incompatible with the pinned Docker CLI, and verified GCE Spot
  preemption while compiling `causal-conv1d`. No attempt reached model loading
  or training. Cumulative GPU upper cost was `$0.79037286`; the retained
  conservative bound was `$4.92111752`, below the approved `$5` ceiling. Every
  input/runtime/failure/teardown set is generation-pinned and hash-sealed in
  GCS. That execution's VM, NAT, router, subnet, and VPC were deleted and
  independently absent before the later CPU prebuild resources were created.
- Authored all 360/360 private decision tasks, 60 per lane and balanced
  generation/repair. Decision tranche 3 is sealed by manifest
  `26f982c437000012d2eae1f4a3d77260b9f3798931dc938941e29c91f2e3a3d9`
  and zero-overlap report
  `dae97584f926381995f06232381425239fa35e1e0d83ce6b5404b93e0bba15d4`.
  Two independent Docker runs proved a 30-second aggregate limit flaky for
  compiled lanes, so Go/Java/Rust were revised to 60 seconds while JS/TS/Python
  remain at 30. Fresh Docker directionality now passes all 360 executions for
  tranches 1–3: 180/180 references pass, 180/180 known-bad implementations are
  rejected, and no execution times out. The evidence seals are tranche 1
  `8cf851703f67c3c80a0cdafba5e4e68adade135af9aa4f443837b670468005cf`,
  tranche 2
  `203965708f9a238a3e323ad4c7a8d9d7d3b5872764e83185ac5e578274a375a8`,
  and tranche 3
  `15d95ad2530d18410c1e1ebda0974bfc54b20208e29f1273aae5ae4a17a56289`.
  Tranches 4–6 add the final 180 tasks. Across the complete surface, all
  360/360 references pass, all 360/360 known-bad implementations are rejected,
  and no final execution times out. Their manifest/overlap/directionality seals
  are tranche 4
  `118dbb5086725bd36ceed09ba37d1f14c53a7f41d79e365c0a6260ac24fb2658` /
  `e66ee7d1a8fa67b044c4e16a8b1e766d4bdc13283380abdc5281b8453d6d1715` /
  `0119e33afb42cda47383d48e1b300b683732a0d30a8c5864ecd370675207857b`,
  tranche 5
  `ee52d232e2d44411a398ad680def61ffffd54722d8a8fc400ffdd2143d4240e3` /
  `251cee5751463ffa76159823b3ec939a6edbd66e328336ca65e7169022186de5` /
  `cd7cafdec42d97173e877fa74530c5daef3d4c1edded9df1b71de9dd453ecdb1`,
  and tranche 6
  `f97eb03d1206cb7135a520f2fb069a44375b9332a4e36ddc9f78cbb0ca6d7c89` /
  `80f4d7f340fc4994f97e8c332e9eea9a339c7eb4837f9d00595775b0ef1ba0ff` /
  `c9b3c9d888f5c438ca2a7666b620a599bd08da639ef24a42c9f78fa461706dfb`.
  The sealed failed tranche-5 result is preserved as non-decision evidence.
  The earlier failed tranche-4 file (seal
  `874e2308f503a35b4cf74c4f9105f623816834526c51e9d50a36b4dd3d01f0dc`,
  34/60 references, 60/60 known-bad rejections, 26 failures) was overwritten
  before preservation and could not be recovered; it is an explicit audit-gap
  incident and cannot support any decision claim.
  A global separation report byte-binds both seed JSONL files, every
  development and decision manifest/task, all overlap evidence, the shared
  tranche-1/2 cross-overlap evidence, the runtime configuration, and all 720
  final directionality executions. It proves zero exact or normalized overlap
  and is sealed by
  `96ea9669e194c567f304c5462b2be9cc171555bba56ea10801186480bb347a06`.
- Prebuilt and content-sealed the pinned production CUDA image on the same
  stopped CPU disk after the first archive export failed with exit 141. The
  failure was caused by unbounded `zstd` progress output exceeding the GCE
  metadata logger scanner limit; the retry uses quiet bounded export. The
  original boot's provider serial is unavailable and was not reconstructed, so
  attempt 1 remains failed, non-decision evidence.
- Verified prebuild attempt 2 as 35/35 generation-pinned GCS objects. The image
  is `ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1` with ID
  `sha256:37b7cbcb8280d469bad6213bf09bfa0ccb2dba96a912aaa105183069c2ce5351`;
  its compressed archive is 8,167,013,739 bytes with SHA-256
  `f2dafd6c0b82d46be441dfe2a5c2b23cd5f309e5061f20da3edf91e70eddb8f3`.
  The terminal backup seal is
  `f1a874deac5e5fadf19eeb29d2c4fb80376e62ed130f70439e2894ae6b4ec076`.
- Passed the deletion gate, backed its evidence, deleted the CPU VM, NAT, and
  router, and independently proved them absent. The post-delete backup seal is
  `ac2b9c9f21e0b6f91d72a0d90d80f3eb8a55ea56432fb66980bae76d86e28358`.
  The dedicated VPC and subnet were retained at this point for the later
  no-NAT A100 qualification.
- Ran the explicitly approved Standard A100 qualification attempt from the
  sealed image. The A100 identity, image load, offline inputs, and controller
  startup succeeded, but package identity failed after 31.85 seconds with
  `ModuleNotFoundError: No module named 'torchvision'`; neither the model nor
  training started, and no CUDA qualification is claimed. The exact 31-object
  runtime prefix is independently verified by seal
  `9d1ed5d0e5407ef7f9397ba7e406952865f981eda61ee5d337990bfd298f114d`.
  The deletion gate passed, the VM, retained subnet, and retained VPC were
  deleted, and six-object post-delete evidence is verified by seal
  `24b148309a89282f6ec6bf043a5bb7ff81baaca5ea783fa71ec1bfe138ec2284`.
- Diagnosed the repair locally: Qwen VL utilities import `torchvision` without
  declaring it; Torch 2.13.0 requires the matching Torchvision 0.28.0. FLA also
  initialized Triton before CUDA while the read-only container provided no
  writable executable Triton cache. The repaired definition pins Torchvision,
  initializes Torch and Triton before FLA, requires CUDA backends explicitly,
  and gives Triton a bounded executable tmpfs while keeping the network off and
  the root filesystem read-only.
- Rebuilt that repaired CUDA image on a temporary Standard `e2-standard-8` CPU
  VM. The image is
  `ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1`, ID
  `sha256:b2f9335c64b208e2d692dc45c56df0790573951df835d34604f80e93d0b0f2a6`;
  its 8,174,282,938-byte compressed archive has SHA-256
  `229325473993a1d5b58baec3ed01fe9d3a49b253be92b39b93d9a52e307e3f9f`
  and GCS generation `1787447318500114`. The 36-object terminal backup is
  independently verified by seal
  `8ab74078de47a0055ff8a46285b01148fa33d9a994e2cbc702afb18be876815a`.
- Passed the CPU deletion gate, deleted the VM, NAT, and router, and proved
  their absence. The 12-object deletion evidence is sealed by
  `112d95f7ce787c1c404d51d7b67ba3427b00ea1eebef35e8cc4319dbf63f57cd`.
- Ran the rebuilt image on one Standard A100. The exact pinned package set,
  NVIDIA A100-SXM4-40GB identity, BF16 support, CUDA 13.0, cuDNN 92000, and
  Triton CUDA architecture 80 passed. Qualification then failed after 32.74
  seconds because the harness requested removed Transformers attributes
  `chunk_gated_delta_rule` and `fused_recurrent_gated_delta_rule`. Model load
  and training did not begin, so Gate 0B remains unqualified. The structured
  failure is sealed by
  `8ddeff566da4a32abfb3586f90f0ca5196cacbaed299dcb52d9fec3b733b3df6`;
  the 31-object runtime backup is independently verified by seal
  `d407c689528356d007b29f08725f29f5dc7caae3334b13cbe11e9dfc7c0d83aa`.
- Passed the A100 deletion gate, deleted the GPU VM, subnet, and VPC, and
  independently proved all run-scoped instances, disks, networks, subnets, and
  routers absent. The deletion evidence is sealed by
  `f5adbff101728eaa3e559f9d047f35c7fd8535f9041d2df8d65cbd94f2a02d2b`;
  the post-delete absence backup is sealed by
  `9862d12c9a48d96253bfe06a0d39daf4bfb6ddd55b3d7224689b795fc86a1068`.
  The complete local run evidence is also archived to GCS generation
  `1787451344731424` with SHA-256
  `c761399cef0729841d9eba74b1f12ee9b95f5b8f8ce0369b24c02f957218da98`.
- Corrected the qualifier to inspect the decorated Transformers 5.15.1 kernel
  closures and require their resolved implementations to come from
  `causal_conv1d` and `fla`. This remains fail-closed and does not infer a CUDA
  pass from symbol presence. The runtime mounts the run-scoped workspace at
  `/workspace`, so the sealed image can be reused without rebuilding. The
  controller now forwards the attempt ID into the container, and both backup
  verification reads are generation-pinned. The full local suite passes with
  one intentional integration skip, and the independent second pass reports
  aligned.
- Ran the attribute-repair retry under GCS prefix
  `ganesh-mini-1.0/gate0b/20260823T030116Z`. The exact environment and three
  external CUDA kernel resolutions passed; the recurrent wrapper alone fell
  back to Transformers Torch because FLA 0.5.2 names the available fused
  implementation `fused_recurrent_gated_delta_rule`. The structured failure
  seal is
  `d7fdb89ce744524ec87ad4b10caf2cb189ef7fb61f61fb6e2e7c152a6f538e50`.
  The terminal backup seal is
  `39ed40945ded583ebbc47ebbbcf3e4d9faf899dcbbe418a741aef87a4ea86065`.
  No model load, optimizer step, or training occurred.
- Passed the retry's deletion gate, backed all run evidence to GCS, deleted
  the VM, disk, subnet, and VPC, and proved them absent. The composite deletion
  backup, deletion gate, and post-delete seals are respectively
  `a5e5c0779fe298ee0d915481e435fa22cccc017b2c17bde2d4947264c7d16204`,
  `7e1d4f9c3eb3dbbe558c4e972083dcc272e3dd1b95bb7f64bdb23d891d3bab88`,
  and `8d353de09d2e61f165f7eff0d2b6edcfcbcc43650bc202dbf6c7e5b4c1b3af07`.
  A final complete local-evidence archive is independently verified in GCS by
  manifest seal
  `f0e930840aebc876ea49f92e5ce4deabf59a3922a8ae4e72fcd2c5cd89a8316c`.
- Implemented a fail-closed pre-import compatibility alias that exposes FLA's
  fused recurrent CUDA implementation under the exact symbol Transformers
  5.15.1 requests. The existing closure inspection still requires the
  recurrent implementation to originate in `fla`; the Torch fallback remains
  disallowed. The retry path now shares one model load across inference and
  training qualification and assigns 12 vCPUs/72 GiB to the container.
  The full local suite passed at that point: 114 tests passed and one
  intentional integration test was skipped.
- Replaced the unusable all-zero Qwen assistant mask with tokenizer-owned
  prefix differencing. The exact pinned tokenizer proves response-only
  boundaries for all 1,449 seed and validation rows across the six lanes;
  prompt/scaffolding tokens are masked, terminal completion tokens are active,
  and non-prefix, empty, batched, or overlength records fail closed. The shared
  implementation is used by both CUDA qualification and seed-pilot
  preparation. After the broader controller repair, the full local suite has
  135 collected tests: 131 pass and four environment-dependent integration
  tests are intentionally skipped.
- Attempted the approved v3 card in `us-central1-a`; the provider returned
  `ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS` before creating a VM. The unused
  subnet and VPC were deleted and the exact v3 resources were proved absent.
- Ran the zone-only v4 retry in provider-suggested `us-central1-b`. All pinned
  inputs and the sealed CUDA image passed generation, size, and hash checks,
  but qualification exited before model load because the container entrypoint
  could not import `scripts.train.response_only`: `/workspace` was mounted but
  absent from `PYTHONPATH`. The 31-object composite backup is sealed by
  `5fb8e2dae08ff7924a55f72cc5a1bad10eb37e508a5b11560ec112d6b0d02e40`;
  the stopped-provider deletion gate is sealed by
  `df4f793d8607364ee86e1f8ba04cf162491ed8f3209f2e50d3ef44a9c7abb64d`.
  The VM, disk, subnet, and VPC were deleted and their absence is sealed by
  `8ac2896c7a397fc23649eb4ed02eaa53d5d4df112851cf0db14c4e335de79d9f`;
  the independently verified six-object post-delete backup is sealed by
  `632b86742d1191f82dad8aec3f8c68eae2c754579e61f783387ff00a3d56a78a`.
- The runner now exports `PYTHONPATH=/workspace` into the offline container,
  with a regression assertion and direct qualifier import smoke. Historical
  v3/v4 cards and hashes remain immutable; the next card must bind this changed
  runner and a new deterministic workspace archive.
- Ran the approved v5 qualification in `us-central1-b`. The repaired import
  path worked and the exact A100, BF16, CUDA/Triton/FLA kernels, package set,
  sealed image, and pinned model inventory passed. ms-swift 4.5.2 then stopped
  before model loading because automatic registry matching returned both
  `qwen3_5` and `ovis_ocr2`. The qualifier now explicitly requests
  `model_type="qwen3_5"` with downloads disabled and verifies the returned type
  and template. The VM was stopped after its 29-object terminal backup was
  verified, then deleted after a 33-object composite backup and deletion gate
  passed. VM, disk, subnet, and VPC absence and the six-object post-delete
  backup are independently sealed.
- Ran the approved v6 qualification in `us-central1-b`. Explicit ms-swift
  model selection correctly returned `model_type="qwen3_5"`; qualification
  then failed before model load because the harness incorrectly treated the
  type-level `ModelMeta.template=None` as a registry failure. The pinned
  ms-swift 4.5.2 source shows that Qwen3.5's template belongs to its model group
  and must be resolved separately. The qualifier now explicitly resolves both
  `model_type="qwen3_5"` and `template_type="qwen3_5"`, recording the nullable
  raw metadata field only as a diagnostic. The focused qualifier suite passes.
- V6's terminal backup, stopped-resource composite backup, deletion gate,
  exact absence proof, and post-delete backup are sealed by
  `5e80ce5264f434b47102706e16a9fa2dd8a494f0a166cf83e01e45b2e944a0c2`,
  `3f8e090c99829139a2cc7b4400f6e40a6e940eb05b8450ef5b2516e91d3b142a`,
  `f1a27123f1362dcfe7c9d55049d4464cf39180d0339145a52c2a3a0a3faba83a`,
  `05392d670d9617c3ffc46584db2531dec730e11c0055070da277696a5e902b0c`,
  and `6db8cc64584a9895a00822273a01a142999e3020552df843f9c9c1dae72876bd`.
  The VM, auto-deleted boot disk, subnet, and VPC are verified absent.
  The complete local run archive has SHA-256
  `dfbc2c8136b03e046245ca6fe318374bd2f54c341ef8c7ae0990ccc644639777`
  and its independent GCS verification is sealed by
  `7e14c80111eefd4f0564f1cf8a9c57081385ea008b55f33796c00e9dfe502f54`.

## Not started or incomplete

- Production Linux CUDA BF16 LoRA runtime and peak-VRAM qualification
- NF4 QLoRA fallback qualification if the primary recipe crosses its measured
  memory threshold
- Exact Qwen base baseline on the frozen development surface
- Seed-pilot training
- Candidate quantization and final laptop certification
- Ganesh v0.1 rerun on the Ganesh Mini decision surface

## Prepared after the latest audit repair

- Gate 2 is ready. All 1,449 authorized seed rows pass current-toolchain
  syntax/compile compatibility and have zero overlap with the 540 frozen
  development and decision tasks. The balanced pilot schedule contains 2,155
  sampled rows, 345,832 response tokens, and 636,093 input tokens; that exact
  input count is now the hard main-pilot ceiling.
- The production evaluation runner now batches by length and language,
  verifies concurrently in network-disabled sandboxes, resumes only sealed
  model/config/task-bound evidence, and emits result-compatible evidence for
  the paired scorer. Gate 1 is closed only on the unexecuted exact Qwen
  development baseline. The zero-task public diagnostic is retained as a
  complete exclusion result instead of weakening admission rules.
- The SFT engine is hash-bound, response-only, cost/time/VRAM bounded,
  checkpoint-resumable, validates held-out loss diagnostically, and requires
  save/reload logit reproduction. Its Qwen-specific structural guard freezes
  the nested vision tower, disables the actual language-model cache during
  training, restores serving cache, and computes the diagnostic macro across
  five product families rather than six compiler lanes. It reserves 600
  seconds for finalization and forces a resumable terminal checkpoint at a
  bounded stop. LR selection binds
  both complete 400k-token candidate runs and their exact 180-task development
  result collections.
- Training packaging is deterministic and excludes every evaluation surface
  while including the exact prepared train and validation inputs.
- Ganesh v0.1's five released adapters are provisioned from immutable Git
  objects and match the release hashes. Its full Gemma base inventory is
  pinned. Rust is explicitly routed to the base because v0.1 did not release a
  Rust adapter. Disk cleanup increased local free space to roughly 232 GiB, so
  the 23.9 GB base is no longer blocked on local storage; provisioning remains
  deferred until the comparison gate to avoid an unnecessary early download.
- Merge, GGUF F16/Q8 construction, constrained laptop certification, clustered
  statistical adjudication, Q8 retention, and final fail-closed release
  decision tooling are present but have not been executed on a trained model.

## Next action

Gate 0B remains closed because v6 did not reach model load, inference, or
training. An exact local Qwen graph deep dive found and repaired two latent
structural defects: the vision tower and active language cache were addressed
at the wrong object paths. It also removed the second backbone load, added
adapter/merge logit equivalence checks, corrected synthetic token accounting,
and fixed the SFT validation macro. Evidence is sealed by
`15330a2c847232d1acdf4c039a1bf34d5c9b7943fc5d12c0ff5e5e137ded5326`.
The sealed v7 card is now stale and must not run. No v7 GCloud inspection,
upload, or resource operation occurred. A replacement card must bind the
repaired source and add time for qualification and terminal backup before the
next paid VM attempts Gate 0B.
Only after that pass may the exact Qwen base baseline run;
seed-pilot training remains blocked until the base baseline exists. The VM
must preserve checkpoints and terminal evidence in GCS, pass independent
backup verification, stop, and then be deleted with an absence proof.

## Authorization state

All work within the Ganesh Mini objective is authorized, including the Ganesh
v0.1 seed corpus, local and non-GCloud compute, downloads, long-running jobs,
training, evaluation, repository operations, and artifact publication.

GCloud usage is the only standing authorization boundary. The latest approved
Standard A100 attempt under run `20260823T073110Z` is terminally sealed. Its
VM, disk, subnet, and VPC are verified absent; no project compute or temporary
network resource remains. Another paid launch requires a fresh card and
explicit approval for its additional GCloud exposure.

No recurring goal-alignment heartbeat or deviation-review subagent is active.
