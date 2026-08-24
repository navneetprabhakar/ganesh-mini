# Project state

Last updated: 2026-08-25

## Current gate

Gate 1: execute the exact Qwen development baseline on the already frozen
180-task surface as the first phase of the approved staged L4 campaign.

Gate 0B is now passed. The approved `us-east1-b` Flex-start L4 execution used
Liger 0.8.2 only for Qwen3.5 fused linear cross-entropy and did not materialize
training logits. Exact package, CUDA, Triton, external-kernel, model-load,
text-only inference, frozen-vision, 2,944-token synthetic envelope, 16 real
optimizer steps, adapter save/reload, and safe merge all passed. Peak reserved
VRAM was 18,975,031,296 bytes against the frozen 22,548,578,304-byte ceiling.
Rank, optimizer, learning rates, data, sequence length, and serving context
remain unchanged.

The canonical Gate 0 report is now also `ready`. Its fused-loss CUDA admission
receipt cross-binds the approved card, immutable run plan, exact qualified
Linux/AMD64 image, 16-record/16-step qualification, adapter reload and safe
merge equivalence, double-read terminal backup, runtime inventory, cost bound,
post-run backup, and exact infrastructure absence. The canonical seals are
`6047b522f697be73b7d781b4e5021c8e29d23441767d660db6f9badc50422fd4`
for CUDA admission and
`adde675ce4db676c635ba864af0dd356c292e352443d4ed88607079059b346cc`
for Gate 0 readiness.

Native AMD64 verifier qualification is complete. GitHub Actions run
`32639381229` loaded the exact pinned image archive and passed all 12
development/decision tranches: 540 reference passes, 540 known-bad rejections,
and zero timeouts. All 15 JSON seals, runtime identities, output hashes, and
the global separation report were independently verified. The repaired
development-only workspace and baseline-runner readiness evidence are sealed.
Gate 1 now fails closed only because the exact Qwen development baseline does
not yet exist. Gate 0B no longer blocks that execution.

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
- Implemented a fail-closed Gate 0 readiness reporter. Its initial local
  macOS report was correctly `not_ready`; the canonical report is now ready
  only through the sealed qualified Linux CUDA evidence chain.
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
  and was sealed by
  `96ea9669e194c567f304c5462b2be9cc171555bba56ea10801186480bb347a06`.
  That historical seal is superseded by the native AMD64 result described
  below.
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
- A Linux seed-pilot preflight now fails on exactly `gate1_ready`. Gate 0,
  Gate 2, response-only rendering, token balance, recipe identity, and the
  exact 636,093-token prepared dataset all pass. This proves a successful
  baseline admission will remove the last non-compute pilot prerequisite.
- The production evaluation runner now batches by length and language,
  verifies concurrently in network-disabled sandboxes, resumes only sealed
  model/config/task/runtime/implementation-bound evidence, persists completed
  verification between generation batches, rejects cardinality and duplicate
  task defects, and emits result-compatible evidence for the paired scorer.
  The Qwen baseline is CUDA-bound to the same external kernel contract as Gate
  0. Gate 1 reopens all 180 task seals instead of trusting aggregate
  accounting. Cross-template comparison pairs on frozen source-task identity
  while preserving model-specific rendered-prompt hashes. Gate 1 is closed
  only on the unexecuted exact Qwen development baseline. The prior
  runner-readiness seal
  `4afb29fcfbc1bda3252bd7bb4e96158ef92efb1fc1cda82b1308701b0e6cb848`
  is historical. Its replacement binds the passed native run, global
  separation, repaired workspace, retention slice, Gate 1/2 reports, and the
  full test suite. A subsequent host-orchestration hardening superseded that
  replacement; the current 171-test evidence is sealed by
  `04c3beba85fab9dcef8f5931335029a375e788040b95b6a591bef3eeacf630f0`.
  The zero-task public diagnostic is retained as a complete exclusion result
  instead of weakening admission rules.
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
- The evaluation verifier contract has been migrated before baseline generation
  from unavailable Apple/ARM64-local images to six project-owned Linux/AMD64
  images. Every base manifest and toolchain version is pinned; TypeScript's
  package tarball is verified against its registry SHA-512 integrity value.
  The exact tag, image ID, and platform are checked before every sandbox run.
  Local readiness is 6/6 and sealed by
  `36c070d9d8554c7f2999b5e4d5bbacbc67664eb64ac2dc34196534de155737a1`.
  The 918,639,104-byte portable image archive is internally verified against
  its OCI tag/manifest/config/layer graph and sealed by manifest
  `aba48afc9f1a75d6911204fd1e49193a9908655ad7d0540ec9cd53c82396bac8`.
  The original deterministic development-only execution workspace contained
  exactly 180 tasks and excluded decision tasks, seed/training data, model
  outputs, and authoring code; it was sealed by
  `846cf0b64e3d1804cbbdaa44cb57a07da989e298c9ed7f3cd8f2c400dda625f5`.
  That workspace is historical. Its byte-reproducible replacement binds the
  repaired task seals. The baseline host audit then identified that an outer
  CUDA container using the host Docker socket could produce verifier bind
  paths invisible to the host daemon. The execution package now forces
  verifier temporary directories onto an identical host/container mount,
  keeps the model container offline, re-audits all six image identities after
  loading, preserves resumable outputs, and accepts only a complete exact-base
  180-task run. The twice-reproduced current archive has SHA-256
  `e64e3e78d3e5d1e0d97479c7e92de25babc89ce761002271e4206733bddbb209`
  and manifest seal
  `4d8e66ce89eabbcc08e6bf7520dd9b0baad5edc426ff27add07e4ab5aae5a8e9`.
  Historical ARM64 directionality results remain immutable but are explicitly
  non-current.
  A manually dispatched, read-only GitHub Actions workflow is prepared to
  load the exact private content-addressed image archive on native AMD64,
  execute all 1,080 reference and
  known-bad checks across development and decision surfaces with at most two
  concurrent tranches, rerun global decision separation, and return one sealed
  evidence archive. This is non-GCloud compute and does not expose a task to a
  model.
  The first dispatch, GitHub Actions run `32636800789`, independently loaded
  the exact archive but stopped before task execution because the host-audit
  code used a Docker Go-template helper (`dict`) unavailable on the runner.
  No directionality result was claimed. The controller now reads portable full
  Docker JSON and seals early failures; packaging now succeeds on partial
  diagnostics. The incomplete 161,802-byte artifact from that failed run was
  deleted, while GitHub's immutable run logs remain the failure evidence.
  The retry, run `32636958446`, executed every tranche. Ten passed; development
  tranches 1 and 2 failed six Go references at the obsolete 30-second limit.
  All 15 evidence seals verify. The full 170,686-byte evidence tar is preserved
  with SHA-256
  `fadd5ab16d2ecf8d53ef6a19b4eded9d093bcf3b922b664db147a23fefb0e098`.
  Development compiled lanes now use the already established 60-second rule;
  the six development manifests and overlap reports were regenerated without
  changing prompts or behavioral artifacts.
  The final retry, run `32639381229`, passed all 12 tranches and all 1,080
  executions with zero timeouts. The preserved 171,088-byte inner archive has
  SHA-256
  `dc44846887b2570885c7d082a5bb812bac56e6144523461c73bb29e7612849e2`;
  the passed-run receipt is sealed by
  `1877bb99a1cab96d962c14301cb6b453785c9487af8692d4c3c130c08afec73f`.
  The adopted top-level native evidence is sealed by
  `aed01c430f33c4580438b824993a9302e72726e4295c82b6e867745e81130cfb`,
  and the replacement zero-overlap global report is sealed by
  `a47d733caaf6d9db735a020dd182ab01cf1ffeb140f7984a846d5ac0d89cf53f`.
  The seed manifest was regenerated through the approved importer; its 1,399
  train and 50 validation records remained byte-identical. Gate 2 remains
  ready.

- Executed the approved Standard `g2-standard-8` L4 Gate 0B run under prefix
  `20260823T145734Z`. The provider exposed 23,659,151,360 CUDA bytes. Both
  recipes passed immutable identity, dependency, external-kernel, and
  non-thinking text-inference checks. BF16 LoRA failed after 91.20 seconds
  while requesting 96 MiB with 41.12 MiB free; the correctly triggered NF4
  QLoRA fallback failed after 148.42 seconds while requesting 512 MiB with
  445.12 MiB free. Both failures occurred in the 4,096-token synthetic
  backward envelope before any training record or optimizer step. The sealed
  run-result is
  `1fffbc66e2bda232b7a5b866fcfaf3094fac1ea4c54c5d76d4e03902d7063f91`.
  All 32 terminal objects were independently double-read from their pinned GCS
  generations under backup-manifest seal
  `087d7c89b1806ddbe61772ba44ba8ce5ccbe17c8dd18fb122aa29189784d8f85`.
  The VM, auto-delete disk, subnet, and VPC were deleted and are absent under
  proof seal
  `eb8171a24a2c893a7fad2a7806fb4f187af7dbb4b86b2d630aee7882c359071d`.

- Executed the approved bounded L4 v3 retry under prefix
  `20260823T152838Z`. Vision offload passed and released 662,833,664 BF16 CUDA
  bytes and 190,087,680 NF4 CUDA bytes. BF16 LoRA still OOMed while requesting
  96 MiB with 73.12 MiB free; QLoRA still OOMed while requesting 512 MiB with
  111.12 MiB free. Both failures remained inside the 4,096-token synthetic
  backward envelope, with zero training records and optimizer steps. The run
  result is sealed by
  `78a1af009066bc2403ad1e4d9ed6e3f865bb2666288bc4f27d95a61ca6d48ee7`.
  All 32 terminal objects and the VM inventory are independently verified by
  `ed92e5f42f4a076a347685ab829fa07a6644cce7e7c19f0cb9c6985d37d97c8a`.
  GPU billing stopped after 867.951 seconds, giving a compute upper estimate of
  `$0.20580668756242`. The VM, disk, subnet, and VPC are absent under proof
  `cda4d4b4a44f52b25dddac1e2f6939390499352da57336fc49e868baef52c8af`.

- Executed the approved bounded L4 v4 retry under prefix
  `20260823T165923Z` with the measured 3,072-token envelope. Both recipes
  again passed exact identity and text inference. BF16 LoRA OOMed while
  requesting 2.84 GiB with 2.65 GiB free. The correctly triggered NF4 QLoRA
  fallback reached backward but OOMed while requesting 48 MiB with 27.12 MiB
  free, a measured shortfall of 21,894,267 bytes. Neither recipe began a
  training record or optimizer step. The fail-closed run result is sealed by
  `67a691b9de7ed34a906b174a7bc4b0d80d23c42d93bee476c0987e687258d5c9`.
  All 32 terminal objects were independently downloaded and verified twice;
  the identical manifest seal is
  `b3d643fae56aa109c0ddd0d0f86e83e5f7fdca98fb899e03b977f2ade7e430e4`
  and the local verification record is sealed by
  `19529bb46c4fb587dece6c3ebe1364e34fca6c38aba14cf5a88b1ad4a5c6ca8b`.
  Billing stopped after 853.409 seconds, for a compute upper estimate of
  `$0.2023585195776689`. The VM, auto-delete disk, subnet, and VPC are absent
  under proof `00fe3d479e2db5f84c950ad1a19372ad252d8bc7b855f1c342bd3fde88bcdd8e`.

- Executed the approved bounded L4 v5 retry under prefix
  `20260823T180807Z` with the measured 2,944-token envelope. The initial
  `us-central1-a` create failed for provider capacity before any VM or disk
  existed; the same approved run was generation-pinned and reallocated to
  `us-central1-c`. Exact identity and text inference passed for both recipes.
  BF16 LoRA OOMed while requesting 2,925,527,040 bytes with 301,072,384 bytes
  free. NF4 QLoRA reached backward but OOMed while requesting 73,400,320 bytes
  with 9,568,256 bytes free, a 63,832,064-byte terminal shortfall. PyTorch
  simultaneously reported about 95,934,218 bytes reserved but unallocated,
  which exceeds that shortfall and makes allocator-segment tuning a measured
  next hypothesis rather than speculation. No training record or optimizer
  step ran. The fail-closed run result is sealed by
  `0519d41c66f5f410e9d6a4a01ff4f7c3af8650d0a86b7b40f9a25a666dd849c9`.
  All 32 terminal objects were independently downloaded and verified twice;
  the identical manifest seal is
  `bfed538722d9d23776e6bf75c51b6d024f86f0fe2e64f9f2571e9c30ea04d2cf`
  and the local verification record is sealed by
  `7fa2fca07cdb48936a1933cb1a2dbbb63fe0e5329ac572e9261b70d8d01ac480`.
  Billing stopped after 864.951 seconds, for a compute upper estimate of
  `$0.20509533396908667`. The VM, auto-delete disk, subnet, VPC, and matching
  routers are absent under proof
  `5af5685dd4f8b42118bfd2ad4148f5296ae61948d9dce31b28d46a363620be5c`.

- Attempted the approved bounded L4 v6 allocator retry under prefix
  `20260823T223044Z`. Standard `g2-standard-8` capacity was unavailable in
  `us-central1-c`; GCP explicitly directed the request to `us-central1-a`,
  where the one allowed capacity reallocation also returned
  `ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS` with no further available zone.
  Neither create produced a VM or disk, qualification did not start, and
  compute cost is `$0`. All six generation-pinned inputs were independently
  downloaded and verified twice under identical manifest
  `606e36225d7901041e103f1729178d4147b73cb68b61456393bc89eb78ba7712`.
  The temporary subnet and VPC were deleted; VM, disk, subnet, and VPC absence
  is sealed by
  `6f4c5509085c6e01489cd69552e273b9acdffb8871bb92a2ebff4f16d94ec9a0`.
  This is a provider-capacity abort, not qualification evidence; the allocator
  hypothesis remains untested.

- Attempted the approved regional Standard L4 retry under prefix
  `20260824T024709Z` with a 30-minute, `$1.00` incremental ceiling. The
  preflight selected `us-east4` because the project had 16 unused Standard L4
  quota, both authorized zones supported `g2-standard-8`, and the durable GCS
  bucket is co-located in `US-EAST4`. Both `us-east4-a` and the sole authorized
  fallback `us-east4-c` returned `ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS`
  before creating a VM or disk. No GPU, qualification process, training record,
  optimizer step, or compute billing existed. All seven generation-pinned
  inputs were independently downloaded twice under identical manifest
  `7e6347207863fa6ce1cfab8994031ead2a9d5bcc3e4a29d3ecb37c062566a3e3`.
  The temporary subnet and VPC were deleted; VM, disk, subnet, VPC, and router
  absence is sealed by
  `fae70b66d8043df4c08c049e1cd064e7c81db4d260c4fa9304b75e1c391c23f9`.
  This is another provider-capacity abort and supplies no allocator evidence.

- Submitted the approved G2 Standard L4 Flex-start request under prefix
  `20260824T160620Z`, with a two-hour request-valid duration, 30-minute maximum
  runtime, automatic VM deletion, and `$1.00` incremental ceiling. Preflight
  passed with 16 unused preemptible L4 quota, 5,000 unused preemptible vCPUs,
  co-located `US-EAST4` storage, and a conservative `$0.95` upper bound. GCP
  accepted the instance as `FLEX_START` and exposed it as `PENDING`, but the
  insert operation returned `ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS` after
  23.649 seconds instead of retaining the request for its declared two-hour
  validity. The VM never entered `RUNNING`; qualification, training records,
  optimizer steps, GPU runtime, and compute cost are all zero. Six
  generation-pinned inputs were independently downloaded twice under identical
  manifest
  `472df5930660c5e37cbdfd79115b9538ca04394921d3875cbad1e9b71ac6b2f1`.
  The terminal request, VM, disk, subnet, VPC, and router scope are absent under
  proof
  `91953aa7e563fdb423e0508e4e06319fcb8aa3be703572b4b5f24e275d91080d`.
  The allocator hypothesis remains untested.

- Executed the approved `us-east1-b` G2 L4 Flex-start run under prefix
  `20260824T161956Z`. The 23,659,151,360-byte L4 passed exact environment,
  external-kernel, model, tokenizer/template, and text-inference checks. BF16
  LoRA OOMed on a 2.72 GiB loss allocation. NF4 with
  `expandable_segments:True` passed training structure but still OOMed during
  the 2,944-token synthetic backward envelope; no real record or optimizer
  step ran. The BF16/NF4 evidence seals are
  `ee7a07c910d059393b1ba15cc516c4bf78a02921fb85f6003140880802c82669`
  and
  `f1d43f17c03b1833635d563d83be9e0a81d1a3370dbd90aaa6743f71dc057c50`.
  All 32 terminal objects passed two immutable-generation downloads under
  inventory hash
  `04eb8aa2204555a33a1c8117c017c678c9f3448060ee968bf15c7461e7743585`.
  The run-result, backup, and teardown seals are
  `c59d09d513a7e28f882d957e6ba22fbe2899edaf68cafea1a3ad4c0a17dba036`,
  `3c289a929bde8b673b3e7a411989f6ec3ace0808052f347b4dd29c9946408843`,
  and
  `11d6011b335c5771c1adcf50a0a30825bd8ae50c7556e189df5bbf27bb53c034`.
  VM, disk, subnet, VPC, and router scope are absent. The conservative
  incremental upper bound is `$0.5686070833333333`, below `$1.00`.

- Diagnosed the dominant 2,944-token allocation as full-vocabulary training
  loss materialization: 1,462,108,160 BF16 logit bytes become
  2,924,216,320 FP32 bytes in Transformers causal cross-entropy, matching the
  observed 2.72 GiB request. The local candidate now pins Liger Kernel 0.8.2
  and enables only Qwen3.5 fused linear cross-entropy with
  `skip_logits=True`. It fails closed if training returns logits. Sequence
  length, rank, alpha, data, optimizer, and serving behavior are unchanged.
  The full local suite passes: 197 passed, one intentional integration skip.

- Rebuilt the pinned Linux AMD64 CUDA image locally after increasing Docker
  Desktop from its inadequate 4 GiB/5-vCPU allocation to 12 GiB/8 vCPUs. The
  image is
  `ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1-liger082`, ID
  `sha256:cdaf068ffcb933120181168ebf6ae1546ddf81e01b2ad006a1a18dd2e43d9860`,
  and size 8,372,032,086 bytes. A network-disabled AMD64 smoke verified the
  exact Torch, Transformers, FLA, causal-conv1d, and Liger versions plus
  Liger's Qwen3.5 multimodal fused-loss forward and `skip_logits` contract.
  Two final workspace builds produced the identical 1,773,034-byte archive
  SHA-256
  `806a5a400278bf7c13092514f5f7b4d8fa0909697ff0cf6a0f9c2b6e8d503310`.
  The local prequalification is sealed by
  `32db10f29dcf15969ccf89db18e55586c1941a758e31c3754bafada529063c0f`.
  The approved execution card is sealed by
  `de09844691ea1ede2d9ef22e152b4289699b656fbf119523795a361207f96efa`.

- Passed Gate 0B under GCS prefix `20260824T180957Z`. BF16 LoRA completed all
  16 real records and optimizer steps after the full 2,944-token envelope.
  The qualification evidence seal is
  `d5c8df044c0b49b1473a2a13e163bcd7acfc06da09b1ea9a0bea75aa1d493a6a`.
  Adapter reload had zero maximum logit difference; safe merge produced finite
  logits with `0.125` maximum absolute difference. The merged 4,426,558,864-byte
  checkpoint and all other 40 terminal objects passed two independent
  generation-pinned reads. The backup, run-result, and teardown seals are
  `d4cd0d2f31f43e081183eef4ff191c2b3aa53eeb2e11763dd4dd723ad1f25cdf`,
  `b29db7d69b7a9653b6be7b4f79390d00a62f2176228f7a995a5ff0b48f85c84d`,
  and
  `95e4ed973cdc746795f0ee1b59045adbce1ceda8bb7af4a8902be86308bcf2f0`.
  Provider auto-delete removed the VM and disk; the subnet and VPC were also
  deleted. The conservative incremental upper bound is `$0.9686175`, below
  the approved `$1.00` ceiling.

## Next action

Gate 0B is complete. Execute the exact 180-task Qwen development baseline and
admit it through the fail-closed Gate 1 report. Then run the bounded
multilingual seed pilot under the qualified BF16 LoRA fused-loss contract.
Seed-pilot training remains blocked until Gate 1 is ready. The native verifier,
global separation, Gate 2 seed cascade, and baseline host audit are already
complete.

The local cloud layer now prepares one `g2-standard-12` L4 Flex-start VM in
`us-east1-b`, a two-hour provisioning window, an approved 18-hour maximum
runtime and USD 19.00 ceiling, 12 host vCPUs aligned with the frozen 12
verifier workers, two-minute incremental GCS synchronization, a 30-minute
terminal backup reserve, guest shutdown only after terminal backup, control-plane
VM/disk deletion with provider max-run deletion as a backstop,
exact-resource teardown proof, and double immutable-generation verification.
After the exact base result opens Gate 1, the same allocation runs both frozen
400k-token LR candidates and their development evaluations, seals LR
selection, runs the 636,093-token main seed SFT and its development evaluation,
and applies Gate 3 promotion. Evaluation and training are isolated in separate
sealed workspaces and offline containers; any failed phase stops the campaign.
The sealed preparation record is
`measurement/gate1/gcloud/preparation.json`. It is intentionally
`prepared-not-executable`: current account price/quota preflight,
generation-pinned uploads of both isolated workspaces and runtime assets, and
the final executable card are still missing. GCloud execution is explicitly
approved. The public-price conservative upper is `$18.357494264`; the absolute
ceiling is `$19.00`.
No GCloud action occurred while preparing it.

The executable-card and teardown tooling are now locally complete. The
executable-card builder requires the exact approval wording, a clean tracked
source commit, passed account preflight, exact temporary resource names, and
generation-pinned GCS identities. The guest rechecks those bindings before
downloading inputs. A wrapper supervisor retries durable backup before early
shutdown on controller failure. After execution, the finalizer double-verifies
the terminal prefix, validates the 180-task result or sealed failure, gates
deletion on the exact runtime and provider inventory, captures all four
provider IDs, proves VM/disk/network/subnet absence, and double-verifies the
post-delete evidence. The current replacement
preparation seal is
`5494db442cdf526737b14367b5a89bf5d775e3818d05338732d0100f52ddbed4`.
The tools have not been executed against GCloud and do not constitute a card
or approval.

The launch path is also locally complete. It verifies fresh sealed price
evidence and the applicable preemptible-or-standard quota pool, uploads all
local inputs by immutable generation, and double-verifies the preflight prefix
before creating the temporary VPC. A launch anomaly triggers verified GCS
failure backup followed by exact run-scoped VM/disk/subnet/network cleanup; an
exact absence proof and a second verified backup close that failure path. An
unverifiable backup fails closed. Large artifact hashing is streaming, and the
guest wrapper authenticates its own startup-script bytes. This preparation
does not create executable evidence: account preflight, uploads, the execution
card, and the 180-task baseline are still outstanding.

Successful execution now has a fail-closed admission bridge. After teardown
and the final double-verified post-delete backup, the finalizer reopens all
receipts, stages and rehashes every baseline output, atomically installs the
canonical Qwen baseline directory, and rebuilds Gate 1 readiness. Admission
requires `status=ready`; sealed failures remain preserved and torn down but are
never promoted. This removes the previous manual-copy step without changing
the frozen evaluation contract.

Fresh price evidence now has a canonical builder as well. It rejects stale or
future timestamps, non-Google sources, non-finite values, and any conservative
18-hour bound that reaches the approved ceiling.

The dependency-complete `.venv` suite passes with only the intentionally
disabled Docker integration test skipped. Forcing that optional test on the
Apple-Silicon Docker host is not a current native verifier result: the
Linux/AMD64 Go compiler exhausts the emulated container's 32-process sandbox
limit. The production Linux/AMD64 archive already passed all 1,080 executions
on GitHub Actions with zero timeouts, so the emulation failure does not alter
Gate 1. It remains a local portability diagnostic and must not be reported as
fresh native directionality evidence.

## Authorization state

All work within the Ganesh Mini objective is authorized, including the Ganesh
v0.1 seed corpus, local and non-GCloud compute, downloads, long-running jobs,
training, evaluation, repository operations, and artifact publication.

GCloud usage is the only standing authorization boundary. The approved
`us-east1` fused-loss Flex-start L4 execution is complete, double-verified in
GCS, and fully torn down; no run-scoped compute or network resource remains.
Non-GCloud compute remains standing-authorized. The staged Gate 1-through-3
campaign is explicitly approved for an 18-hour maximum and USD 19.00 ceiling,
but creation remains blocked until current price/quota, immutable uploads, and
the final executable card pass.

No recurring goal-alignment heartbeat or deviation-review subagent is active.
