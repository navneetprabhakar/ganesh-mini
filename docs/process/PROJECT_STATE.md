# Project state

Last updated: 2026-08-23

## Current gate

Gate 0B and Gate 1 preparation in parallel:

- production Linux CUDA BF16 LoRA qualification, with NF4 QLoRA as fallback;
- frozen development and decision surfaces plus exact Qwen base baselines.

Local Apple runtime qualification and the first pinned Linux CUDA image
prebuild are complete. A Standard A100 attempt reached the qualification
container but failed during package identity before model loading because the
image omitted `torchvision`. Gate 0 remains fail-closed while the repaired
image awaits rebuild and NVIDIA requalification.

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
- The recurring 30-minute goal-alignment heartbeat is active.
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
  the root filesystem read-only. The repaired image has not yet been built or
  qualified.

## Not started or incomplete

- Production Linux CUDA BF16 LoRA runtime and peak-VRAM qualification
- NF4 QLoRA fallback qualification if the primary recipe crosses its measured
  memory or cost threshold
- Current-toolchain re-execution of seed records that have executable bundles
- Exact Qwen base baseline on the frozen development surface
- Seed-pilot training
- Candidate quantization and final laptop certification
- Ganesh v0.1 rerun on the Ganesh Mini decision surface

## Next action

The complete evaluation contract and global separation evidence are frozen.
The repaired Gate 0B retry card is prepared and sealed by
`6853e7e07b39c00383ebb4f9c3ee34180ee032aa9b5f589fefb4b86698ddca21`.
The local host is ARM64 and has only 7.2 GiB free, which is below the prior
8.17 GB compressed x86 CUDA image alone; no safe non-GCloud Linux x86 builder
is currently available, and unrelated Docker data will not be deleted to
manufacture space. Executing the card requires fresh explicit GCloud approval.
After the rebuilt image passes Gate 0B on NVIDIA, execute the exact Qwen base
baseline before opening the seed-pilot training gate.

## Authorization state

All work within the Ganesh Mini objective is authorized, including the Ganesh
v0.1 seed corpus, local and non-GCloud compute, downloads, long-running jobs,
training, evaluation, repository operations, and artifact publication.

GCloud usage is the only standing authorization boundary. The approved CPU
prebuild and Standard A100 attempt are terminally sealed. Their VMs, NAT,
router, subnet, and VPC are all verified absent; no project compute or temporary
network resource remains. Any new GCloud inspection, creation, or execution
requires explicit approval.

An active 30-minute Codex heartbeat independently audits goal alignment. A
`DIVERGENCE` result pauses project mutations and compute until user direction.
