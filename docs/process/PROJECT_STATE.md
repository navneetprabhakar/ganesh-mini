# Project state

Last updated: 2026-08-27

## Current gate

Gate 3 v2 attempt `20260827T090603Z` is fully finalized as a strict sealed
failure. The first boot encountered a bucket-IAM 403 before model loading or
optimizer progress. Granting the run's default Compute Engine service account
bucket-scoped object access and resetting the same VM repaired that bootstrap
failure. No training state was resumed or reused from the failed boot.

The `1e-5` candidate then completed the frozen unique epoch: all 1,399 rows,
461,235 input tokens, 242,406 supervised response tokens, and 175 optimizer
steps in 1,560.65 seconds. Save/reload equivalence passed with zero maximum
logit difference. Its five-family validation record mean improved from
`0.3703169807` to `0.3598691403`, and its supervised-token mean improved from
`0.3766998041` to `0.3665855866`. These are diagnostic loss improvements, not
executable promotion evidence. The complete training result is sealed by
`d885af11f3c7346959b2fcfadd6b77c6009bca99410f527038f923ad09f1c5a0`;
the final adapter file hashes include
`6a6ccf88c85a5c16d3569bdedc8ccb5662eeb79f583006a777c7ba2d2f51fc8d`.

The first 30-task canary failed after generating five Go responses because the
host had loaded only the CUDA model image. The six pinned verifier images had
historically been loaded as a side effect of rerunning Gate 1; the Gate 3-only
path correctly reused the canonical Gate 1 result and therefore skipped that
side effect. Docker reported `No such image: ganesh-mini-go-verify:amd64-v1`.
This is an orchestration defect, not a model-quality result. No canary score is
admissible, `3e-5` did not train, LR selection and the 180-task evaluation did
not run, and the current evidence cannot decide whether the seed data is
sufficient.

The repaired campaign now loads, identity-checks, and audits the complete
verifier archive before any paid training. Unit coverage rejects a missing
image load, and the archive-executed rehearsal proves verifier preparation
precedes candidate training. The evaluation workspace, archive, rehearsal,
and non-executable preparation seals are now
`6e001b04de84d785feaf96dbd42ce5adcad62fd8e7a6cc969c991e4f90222532`,
`56c29ec107782fe2870496f4d54ab0fb466269a535210d88823afb1d4f2ae7dd`,
`dff92b7d1cf9676ea59f6e5ba66c10ee7447647c84dfd19a876714d126e18594`,
and `bedaf55f5309c40d0044f1d1aff8aa3ae080dead312091fd56a4ea92e9ad04eb`.

The independently generation-pinned 75-object terminal backup passed under
seal `93d7206401744b7c66e55800352f87a2204d084ae88119d3f6c5038b769f9fb5`.
Terminal validation is `sealed-failure` under
`8adbed352c7e1799468262097225f84a4488736e98c294cce038e8f524b76986`.
The strict deletion gate, exact four-resource absence proof, finalization, and
14-object final post-delete backup are sealed respectively by
`ae8c7556d08ecfeb05b208f95bbd8859cf1a76932230457a27065216209e2086`,
`ecf74ca24bb77c8ccb833326ada8ba6dc5e00dca94d499c1ab6c94271884c394`,
`efb4e971c58873a09ee7575cd17916c1baf951e7ce093c5d82aab89cba6dfc6d`,
and `fea0b331acd56baf7eefcb6591656c3c76f35c5da2313f507380792a32c6fc37`.
The exact VM, boot disk, subnet, and VPC are absent. The run approval is
exhausted; another GCloud execution requires a fresh explicit approval.

Gate 3 is closed after the fully finalized staged attempt
`20260826T042539Z`. Gate 1 revalidation reproduced the canonical base score of
20/180 on the same exact Qwen revision and serving contract, although raw
outputs and the run seal differ from the earlier CUDA run and remain separate
revalidation evidence under run seal
`57ea58ece793aee30b8c104dadff5c837d568f5f3effbb5f9770bada91fd64da`.
The original admitted Gate 1 baseline remains canonical and was not
overwritten.

The LR `1e-4` candidate completed 400,652 seen tokens, adapter save/reload,
and all 180 development tasks. It passed 13/180 versus the same-run base's
20/180: Go 2/30, Java 2/30, JavaScript 3/30, TypeScript 1/30, Python 5/30,
and Rust 0/30. Five-family macro fell from 10.0% to 7.33%; paired transitions
were 10 wins, 17 losses, and 153 ties. It therefore cannot be promoted. The
LR `2e-4` candidate reached 339,550 seen tokens and preserved three
checkpoints, then the configured consecutive-loss-spike guard stopped the run.
Its evaluation, LR selection, main 636,093-token SFT, and promotion
adjudication did not execute. Gate 3 therefore requires a data/mechanism and
stop-guard correction before another bounded pilot; scaling is not justified.

The terminal is a strict `sealed-failure` under seal
`8b4acfa783446a210c15ddfc47db71c255c1a8ac6d4ed3616f6f72571ddc03fa`.
The generation-pinned 805-object terminal backup is verified under seal
`e9f1439b6b8b1d5c1b17b8e28c7c4e16344d7a1847c47216d051456cb2ffe180`.
GCP had automatically deleted the exact VM and boot disk under the card's
`instanceTerminationAction=DELETE` contract; provider operations prove guest
shutdown followed by deferred deletion. The finalizer verified that lifecycle,
deleted the remaining subnet and VPC, and proved all four identities absent.
Deletion-gate, finalization, and final 13-object post-delete backup seals are
`3028a74002243b0627f8b90489da06a1b1b18ba16efa14ea7ab7b85d6ce6f57a`,
`f0b6a8049f1d440a2d2e5b602ea62330c1fb30a944d985fe1f7f2ca387743c58`,
and `96bc79aed2a1819dffbb74c1e88278dd8e151bf48d366da0de814bec9aae6c14`.
No run-scoped GCloud resource remains. Another GCloud execution requires a
fresh explicit approval.

The Gate 3 v2 mechanism is now partly executed on CUDA. The
rejected v1 config and 2,155-row duplicated schedule remain immutable
historical evidence. The new versioned config uses all 1,399 authorized rows
exactly once: 461,235 input tokens and 242,406 response tokens. Raw response
volume is not balanced, so every row carries a supervised-token objective
coefficient. The prepared-manifest audit proves the normalized objective is
Go 20%, Java 20%, JavaScript 10%, TypeScript 10%, Python 20%, and Rust 20%,
with one effective epoch and no repeated source ID. Its manifest seal is
`1b24782e32dcab4ea2e42a80564c45cba29fdcff0c198f7c7df465595e3f7edf`.

The repaired primary recipe is BF16 LoRA rank 8/alpha 16 on 16 attention
projections in layers 16–23, excluding every MLP and gating projection. Its
learning-rate candidates are `1e-5` and `3e-5`. The trainer now measures the
untouched base and adapter on the same validation rows, records both record-
mean and supervised-token-mean diagnostics, and replaces adjacent-record loss
comparisons with a post-warmup optimizer-group rolling median/MAD detector
that also preserves group min/mean/max and gradient norm telemetry.

Development tranche 1 is frozen as the deterministic Gate 3 canary: 30 tasks,
five per lane, selected structurally without reading model results. It can
triage the two complete LR candidates but cannot decide promotion or enter
training. The selected candidate still requires the full 180-task development
evaluation. Its manifest seal is
`0b7483141ba64ba223bc976ed7711ad847bc1056888be0e7bd9d261b85cffa44`.

The current Gate 3 v2 evaluation-workspace, training-workspace,
runtime-rehearsal, and non-executable preparation seals are respectively
`6e001b04de84d785feaf96dbd42ce5adcad62fd8e7a6cc969c991e4f90222532`,
`874ac3f8f2bf226a6dd100c470f46ee39b7e7f1591ec5324042e985de17b4ae1`,
`dff92b7d1cf9676ea59f6e5ba66c10ee7447647c84dfd19a876714d126e18594`,
and `bedaf55f5309c40d0044f1d1aff8aa3ae080dead312091fd56a4ea92e9ad04eb`.
The evaluation archive is byte-reproducible at SHA-256
`56c29ec107782fe2870496f4d54ab0fb466269a535210d88823afb1d4f2ae7dd`.
The regenerated local training preflight is `ready` with no failed checks under
card seal
`c33be811a3eaeda5033bcd93313577f0eb716b8bd42a8514da9f41b40eedba0e`.
That preflight is superseded by the approved and rehydrated execution path
described above.

Gate 1 is complete. Approved attempt `20260825T153823Z` executed all 180
frozen private development tasks against exact revision
`15852e8c16360a2fea060d615a32b45270f8a8fc`, with first-EOS trimming and
resource-limited network-disabled verifiers. The exact base passed 20/180
tasks: Go 0/30, Java 2/30, JavaScript 4/30, TypeScript 6/30, Python 5/30,
and Rust 3/30. Run seal
`a04361a047080bc479328d52d8be23fabcedb2b42ebbf0a059775e32db823ceb`
and 365-file admission seal
`c7d7d33d59d804a3dcd1b0f98e5aed9f409b229a3c31d85f1ef19f5b021faa62`
bind the canonical result. Gate 1 readiness is `ready` under seal
`d827ece3d324633a6fc6b0a46be55dcd87a87fb565358d3f2704806ced154971`.

Gate 3 training admission also passed, but the first 0.0001 LR candidate
stopped before model loading or any optimizer/token progress. In the exact
Torch/CUDA image, `torch.cuda.reset_peak_memory_stats(0)` raised
`RuntimeError: Invalid device argument` before the CUDA context had been
explicitly selected and initialized. Production SFT now selects `cuda:0`,
initializes CUDA, then resets the current device's counters without an integer
argument. The call-order regression test, archive rehearsal, and full local
suite pass. The resealed training archive, training manifest, and preparation
seals are
`d06c4d2a71828c61514d62ae3d1c8dccf6b5e8e9d9d403527b7f95833d919688`,
`9af762e484c04f54e1728adca9d87a9214c991cfed78bc9cc78a656bfa45fe19`,
and `b38dcbbb4a8ba0bbbe5a9bbac138ebe335cc0f14e9ceb39b0a171882374cdc5a`.

Strict terminal validation, finalization, and exact resource absence passed
under seals
`c299e90402004e9ce014f0b04f3fa0f2ae9d33211d3fa5971a7c1f58aecad351`,
`94963d2fd2deed795d6a883633f2d8cb2064e36cd4b8c6426c95720a1cf36f5a`,
and `1bb8e75d6662083f8da1b27655507952a913c19234b21ecfd7c35b3a1264e7c1`.
The VM, disk, subnet, and VPC are absent. The final 14-object post-delete GCS
backup is verified under seal
`9a34c63e37a75211234edb5de977c4da5f92e4381e352b4b85fce4a319fbf419`.

That historical repair was superseded by Gate 3 v2. The latest Gate 3-only
attempt completed one of the two planned unique-row candidates but stopped on
the verifier-image orchestration defect before any admissible canary result.
Its approval is exhausted and no run-scoped resource remains.

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
development-only v1 workspace and baseline-runner readiness evidence were
sealed before Gate 1 execution. Gate 1 subsequently completed; its canonical
result and the current Gate 3 v2 workspace are recorded above.

The superseded pre-Gate-1 evaluation-workspace manifest seal was
`f6551430af4c5a2cd2ad5d7bcbdcf4daf3105136682c146535e2a2a11c2da5b0`;
the corresponding v1 training-workspace manifest seal was
`9af762e484c04f54e1728adca9d87a9214c991cfed78bc9cc78a656bfa45fe19`.
The v1 archive-executed runtime rehearsal seal was
`7c280c5a5c8ec8c28891818d5171dbdea3507dc11eca6799f86cde2d71d50406`,
and its non-executable preparation seal was
`b38dcbbb4a8ba0bbbe5a9bbac138ebe335cc0f14e9ceb39b0a171882374cdc5a`.

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

- Gate 3 v2 completion: the `3e-5` candidate, both complete 30-task canaries,
  LR selection, and the selected candidate's 180-task development evaluation
- Evidence-triggered 4,000–8,000-row expansion, if the repaired seed remains
  insufficient
- Main joint verified SFT and optional correction pass
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
  The release path now also has a pinned llama.cpp server backend for sealed
  F16/Q8 evaluation, a six-lane export-equivalence verifier, and a fail-closed
  Hugging Face publisher. Gate 8 requires sealed raw-result-set roots, a fresh
  Ganesh v0.1 comparison, seed/readiness/execution-card/training-run lineage,
  artifact-to-training binding, export equivalence, quantization retention,
  and both laptop profiles. These controls are locally tested; they do not
  constitute executed release evidence.
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
  A manually dispatched, read-only GitHub Actions workflow was historically
  used to load the exact private content-addressed image archive on native AMD64,
  execute all 1,080 reference and
  known-bad checks across development and decision surfaces with at most two
  concurrent tranches, rerun global decision separation, and return one sealed
  evidence archive. This is non-GCloud compute and does not expose a task to a
  model. That workflow has since been removed and GitHub Actions is disabled
  for this repository; the sealed historical results remain evidence.
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

Gate 0B, Gate 1, and Gate 2 are complete. Gate 3 v2 has one valid completed
`1e-5` training artifact but no executable canary result. The local verifier-
loading repair, v2 workspace, and campaign rehearsal are sealed. The next
cloud action, after a fresh explicit approval and clean execution card, should
reuse the generation-pinned completed `1e-5` adapter as an immutable candidate
input, run its canary, train `3e-5`, run that canary, select the LR, and execute
the selected candidate's full 180-task evaluation. It must not retrain `1e-5`
unless resume/import validation cannot prove the exact completed artifact.

Data expansion remains premature. Comparable validation loss moved in the
right direction across all five product families, but executable behavior was
never measured. Only the completed canaries and full development evaluation
can distinguish seed insufficiency from a useful conservative seed adapter.

The local cloud layer now prepares a Gate 3-only campaign on one
`g2-standard-12` L4 Flex-start VM in an explicitly approved `us-east1` G2 zone.
It allows two hours for provisioning, caps runtime at four hours, reserves the
last 30 minutes for terminal backup, and caps incremental cost at USD 5.00.
This bound is based on executed attempt `20260826T042539Z`: 400,652 training
tokens took 1,845 seconds and a full 180-task candidate evaluation took 1,710
seconds. Two 461,235-token candidates, two 30-task canaries, and one full
selected-candidate evaluation therefore retain substantial contingency without
the obsolete 18-hour envelope.

The evaluation v2 workspace seals the canonical 180-task base result and the
deterministic canary. The training v2 workspace seals the unique-row weighted
seed and contains no evaluation surface. The guest verifies the canonical Gate
1 report against the bundled base run, trains both candidates, selects on the
canary under the frozen rule, and fully evaluates only the selected already-
trained candidate. It does not regenerate the base and does not run a third SFT.

The preparation record at `measurement/gate3/gcloud/preparation.json` is a
repaired full-campaign fallback and is `prepared-not-executable`. Before asking
for another cloud approval, a continuation preparation must additionally bind
the completed `1e-5` candidate as an immutable imported input and prove that
the controller cannot retrain or replace it. Fresh price/quota preflight,
generation-pinned uploads, and a clean-commit execution card remain missing.
The public-price conservative upper is `$4.351665392`, below the proposed USD
5.00 ceiling. The launcher retains two-minute GCS checkpoints, fail-closed
backup, exact-resource teardown proof, and double immutable-generation
verification. Its maximum-runtime action is `STOP`, not `DELETE`, so the boot
disk survives until the local finalizer independently verifies the complete
terminal GCS inventory. Only then may the finalizer delete the VM, disk,
subnet, and VPC. Any terminal-integrity or deletion-gate failure preserves the
stopped resources. No GCloud action occurred while preparing this revision.

The terminal validator is now version-aware. Historical Gate 1 success still
requires its generated baseline, while Gate 3 v2 success requires both
candidate training artifacts, both canary task-evidence collections, sealed LR
selection with exact collection hashes and lane counts, the selected
candidate's complete SFT and save/reload evidence, its 180-task collection,
every promotion check, and the terminal campaign seal. The output has a
dedicated Gate 3 terminal schema. This prevents both a valid reused-baseline
run from being rejected by the obsolete Gate 1 contract and an incomplete
candidate path from being trusted through phase-ledger claims alone.

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
attempt in `us-east1-c` is complete, sealed, and fully torn down. Its
conditional `us-east1-d` fallback was not activated because `c` provisioned.
Any replacement GCloud execution requires fresh explicit approval plus current
price/quota preflight and a new executable card.

No recurring goal-alignment heartbeat or deviation-review subagent is active.

## 2026-08-25 — Staged retry reached the campaign, failed on Docker-name case, and was fully torn down

Approved attempt `20260825T061157Z` passed fresh price, quota, identity,
absence, and two-read GCS preflight; provisioned one `g2-standard-12` L4
Flex-start VM immediately in `us-east1-c`; and authenticated every immutable
input generation. The guest verified both isolated workspaces, Gate 0 and Gate
2 receipts, the exact upstream model, the qualified CUDA image, the offline
Docker bundle, and all verifier images. CUDA image import and NVIDIA Docker
configuration also completed successfully.

The campaign then failed after workspace isolation and before the first of 180
baseline tasks. The outer controller correctly requires the canonical
uppercase UTC attempt ID, but the nested baseline host reused that evidence ID
as a Docker container name and still allowed only lowercase slug characters.
Its sealed diagnostic is `staged campaign failed: invalid baseline attempt ID`.
No baseline metric, training step, decision prompt, or candidate artifact was
produced; Gate 1 remains closed.

The controller and wrapper backed the runtime and diagnostic envelope to GCS
and shut the VM down. Finalization rejected that envelope because the
checkpoint command had appended to `gcs-backup.log` inside the directory it
was simultaneously hashing and uploading. The inventory therefore recorded
the empty-file hash while GCS preserved the subsequently written 4,746-byte
log. This is a genuine integrity failure, not an admissible terminal result.

Because the normal finalizer failed closed before deletion, the exact stopped
VM, auto-delete disk, subnet, and VPC were then deleted explicitly. Four
independent exact-name provider listings are empty. Their five-object manual
teardown envelope was downloaded twice by immutable generation under backup
seal `5e210a79f37ea445a87d5b3f3c76657c618e86cdc60c12f60d6df1de75cc2747`;
the manifest itself is also stored in GCS at generation `1787639587497426`.
No run-scoped resource remains.

The permanent repair preserves the uppercase attempt ID in every evidence
contract while deriving lowercase-only names for baseline, training, and
evaluation containers. Checkpoint output now stays under `/var/log`; all
runtime writers are stopped and awaited before that fixed log is copied into
the evidence tree and the terminal inventory is written. Regression tests use
the exact production ID `20260825T061157Z` and enforce stop, capture, hash, then
backup ordering. The rebuilt non-executable preparation seal is
`ef3bc566ed3db33602d27e2d15ad52541674e6febce9cb8af92ba08a13950bf8`.
The approved one-retry GCloud scope is consumed; another cloud execution needs
fresh explicit approval.

## 2026-08-25 — Retry exposed a post-create generation overwrite and was fully torn down

Approved retry `20260825T055326Z` passed fresh price/quota/identity/absence
preflight and two-read GCS verification, then provisioned immediately in
`us-east1-c`. The fixed UTC attempt-ID contract passed. The controller stopped
before downloading any model or verifier assets because the launcher uploaded
the execution card once to bind its immutable generation, created the VM, and
then uploaded the same card path again alongside the launch receipt. With
bucket object versioning unavailable, the second upload replaced the bound
generation. The guest correctly rejected the stale generation URI and exited
`1`. No baseline task, training step, or decision prompt executed.

The VM was stopped immediately after the anomaly was confirmed. The guest had
already backed a six-object partial runtime envelope and a four-object wrapper
failure envelope. Their independent backup seals are
`6597132edc1f8444da5527544ad27316cc2f98cfeebcb1e9b8c78f67b086b7ba`
and
`29460913df428feb9c6f10bd44e52ae795987263324e897b703bdbd1b3a9e796`.
The finalizer now permits recovery from this partial state only after verifying
its original inventory and wrapper independently, requiring matching nonzero
exit codes and diagnostics, and preserving the original inventory bytes inside
the recovered terminal envelope.

The recovered terminal is correctly `sealed-failure` under seal
`797012a6f738b620cb17bdc25a54fd8f6c0bb87ff935af7654bfc73722f1b45d`.
Deletion-gate seal
`45cfc61789af7dde2b48c42976a70a481af138468601315000a465a2f843f1d7`
passed. The VM, auto-delete disk, subnet, and VPC were deleted; absence-proof
seal
`591491e56d98abe382c4bd427259887ef4e493072f35521c300c096c2ae0d35f`
proves all four identities absent. Finalization seal
`1c78b87a257672d5a417485727fe23e554867dd74a0aa6e56d57a5545592cad1`
and final 15-object post-delete backup seal
`fa1ad6dede3deeb6318b8ef3a53b5615aedca829492a8f279679793b4091c7f1`
close the attempt. Provider timestamps bound creation-to-stop to about 157
seconds; this is not an asserted invoice amount.

The launcher now uploads only the new launch receipt after VM creation and
never overwrites generation-bound bindings or the execution card. Direct tests
enforce this ordering and the partial-terminal recovery invariants. The full
suite passes with the one intentional Docker integration skip. The rebuilt
non-executable preparation seal is
`404b92eca32b6b19832abab41329a47e3e2b180fb132c874c4d67223641bdc97`.
Gate 1 remains closed and training has not started. The one-retry GCloud
approval is consumed; another execution requires fresh explicit approval.

## 2026-08-25 — Provisioned Gate 1 attempt failed before baseline and was fully torn down

Approved run `20260825T052909Z` passed fresh preflight, immutable input upload,
and executable-card binding, then provisioned one `g2-standard-12` Flex-start
VM in `us-east1-c`. The metadata wrapper authenticated and downloaded the exact
controller, but the controller rejected the launcher-generated UTC attempt ID:
the launcher emitted `20260825T052909Z` while the controller allowed only
lowercase slug characters. It exited `40` before creating the runtime evidence
directory. No model or verifier image download, baseline task, training step,
or decision-set access occurred.

The wrapper backed its exact four-object failure envelope to GCS. Because the
failure preceded runtime inventory creation, the finalizer was hardened to
recover only from an empty terminal prefix plus that independently double-read
exact wrapper envelope. Recovery binds both bootstrap hashes to the execution
card, requires a nonzero integer exit and nonempty diagnostics, then creates a
sealed terminal inventory without promoting any model result. Terminal
validation seal
`56b3d0f6d3215dfd1f8d1ef4b473f195ce0e29eb5c7c6450c3a2c12e6221e87a`
correctly records `sealed-failure`; deletion-gate seal
`9dc479102c03a838a8e2b7d248b0ea114bbfed30d817550dc61d0f168747144f`
records `passed`.

The VM, auto-delete disk, subnet, and VPC were deleted. Provider queries and
absence-proof seal
`349071ab20135cbb8e506863de0468b1118e0805e8483278ab2e52107aab154d`
prove all four exact identities absent. The finalization seal is
`35bedced6370830b8ce1406efa8ca9b712f6c4b487cabb6f0807420c2a471f32`;
the final 14-object post-delete backup seal is
`6d64a411d904c8ce540c1e84e6773ff7b4e2c28385459c207225cea01cf3139c`.
The provider timestamps bound creation-to-stop to about 132 seconds, far below
the approved runtime and cost ceilings; this is a conservative time bound, not
an asserted invoice amount.

The permanent controller contract now accepts only the launcher's exact
`YYYYMMDDTHHMMSSZ` attempt format, and focused recovery/validation tests pass.
The rebuilt non-executable preparation seal is
`4f6cda6e3a1b3003d59385ecd80685048df9c09f2a074ef0af1bd2b89b7e4a7c`.
Gate 1 remains closed, no training has started, and the conditional
`us-east1-d` fallback is no longer authorized because `us-east1-c` provisioned.

## 2026-08-25 — Staged campaign launch reached provider stockout and was fully torn down

Approved run `20260824T204540Z` passed account, project, current price, quota,
machine/image, exact-resource-absence, and GCS round-trip preflight. All sealed
evaluation, training, model, image, verifier, controller, and execution-card
inputs were uploaded with immutable generations and the preflight prefix passed
independent double reads before infrastructure creation.

The `g2-standard-12` Flex-start create in `us-east1-b` exited before a VM or
disk was provisioned. Its interactive provider stderr reported
`ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS`, but the launcher did not redirect
that stderr into the run directory; therefore the exact provider message is
not decision-grade sealed evidence and must not be reconstructed as such. The
sealed record proves create exit code `1`, an empty create JSON, and complete
absence of the exact VM, disk, subnet, and network identities. The temporary
subnet and VPC were deleted after the first verified failure backup. Cleanup
seal `63b8e20e9a1caeb2659d66f5bae4c170bd2d241a897dd868567b073c25e0efbd`
and final 68-object backup seal
`c7222bd9917be67b5fb458f704d363821704d53b234b1d94061209c7dc17ff92`
close the attempt. No VM or GPU runtime occurred; only storage/API operations
and short-lived free network objects were used.

Before another request, the launcher now captures provider-create stderr,
binds the execution card to the selected approved zone, and permits only the
official G2/L4 zones `us-east1-b`, `us-east1-c`, and `us-east1-d`. Immutable
GCS verification still performs two independent generation-pinned reads per
object, now with a bounded default of eight concurrent objects to remove the
serial cleanup bottleneck. The replacement preparation seal is
`682b9466b306dffe9c3155a5828cc46e075138edc9f7aa338472bd01b1e0c34c`.

Gate 1 remains closed and no training has started. The next GCloud action is
blocked on a fresh explicit approval. The recommended bounded fallback is one
aggregate campaign attempt sequence in `us-east1-c`, then `us-east1-d` only if
`c` fails before provisioning, with at most one running VM and the existing
18-hour runtime and USD 19 aggregate incremental ceiling.

## 2026-08-25 — Gate 1 Linux bytecode mutation failed closed and was repaired

Approved attempt `20260825T085926Z` passed fresh price, quota, resource
absence, GCS round-trip, immutable input, and double-read preflight checks. It
provisioned `g2-standard-12` VM `ganesh-mini-g1-l4-20260825t085926z` in
`us-east1-c`. All staged downloads matched their hashes. The offline Docker
installation, NVIDIA container runtime, qualified CUDA image load, exact image
ID, and GPU inspection passed.

The campaign stopped before baseline generation with controller exit `1` and
the exact diagnostic `extracted development workspace file set mismatch`.
Workspace isolation had passed immediately before the baseline helper import.
On Linux, that import created in-tree `__pycache__` files because the extracted
workspace was host-writable; the helper then correctly rejected the mutation.
The earlier Mac rehearsal did not expose this because that interpreter directs
bytecode to an external user cache.

The terminal is a strict `sealed-failure` under seal
`cbc3bb69978ad0bcd526f195b94526aa71caf03d48ccb7356b24dd240e500334`.
Deletion gate
`090f96e55c1f3ba857e9bf8cccb409cc14fc627b54be3f269fe2478a139dc257`
passed. The exact VM, auto-delete disk, subnet, and VPC were deleted; absence
proof
`ba7e3cf424d8c981a280ece41dfdfddcf186803cc2af4312d77f81e7a9e8adf7`
proves all four absent. Finalization seal
`84b11ce6b3cb2703e610bf4024dbf2c824be57a959c11f35af57c1dc675fd7f4`
and final post-delete backup seal
`308d4da01f815963808989aec625644d2df4d75d3a9aaafd51187c4a164de1bd`
close the attempt. Provider start-to-stop time was about 536 seconds; this is a
runtime bound, not an asserted invoice amount.

The startup controller now invokes the campaign with `python3 -B`, and the
campaign independently sets `sys.dont_write_bytecode`. The runtime rehearsal
forces in-tree bytecode semantics, imports the archived modules, and asserts
that the extracted file set remains identical to the 214-file manifest. The
evaluation archive is resealed at
`f5a1518ab6d24d3fce649838fb623115988478b508541a5ccb05c13842b868eb`;
the rehearsal and preparation seals are
`e9d39a0e486c192b05c62810e8ef94fbb39c665c96f2d66af5cad0b009a10902`
and
`4e52713bcf6caa2f4438a21de8e408c42724d7f34f61c16a238bb88690eca0b9`.
The complete local suite passes. Gate 1 remains closed, no training has
started, and the consumed one-attempt approval does not authorize another VM.

## 2026-08-25 — GitHub Actions removed

At the user's direction, both repository workflows were removed and GitHub
Actions was disabled at repository level. Historical native AMD64 and Gate 1
workflow run IDs remain provenance records only. Current validation is local
or part of an explicitly approved GCloud execution; no push or manual GitHub
workflow can run.

## 2026-08-25 — Read-only nested Docker mounts failed closed and were removed

Approved attempt `20260825T103213Z` provisioned one `g2-standard-12` Flex-start
L4 VM in `us-east1-c`. Fresh price/quota/resource-absence/GCS preflight passed;
all immutable downloads, hashes, Docker and NVIDIA setup, exact CUDA image,
verifier runtime readiness, bytecode immutability, and workspace isolation
passed. The base container then exited `125` before model loading because the
host model directory targeted `/workspace/models/qwen3.5-2b-15852e8`. That
target did not exist in the sealed archive, and Docker could not create it
beneath the read-only `/workspace` bind. No baseline task, inference token,
training step, or decision prompt executed.

Terminal validation is correctly `sealed-failure` under seal
`189a75945ba4619cab3a781090b588a6614dd86f835d2108a37f28551732d125`.
The deletion gate seal is
`a8f6762bb0a2c1439950beeaad8e753c0f28013bc636855b7d67421f3674189b`;
absence proof
`3f2a08d74b521eb1a139505b2d77e4c7986aa1819408043135d5e32bae27189b`
proves the exact VM, auto-delete disk, subnet, and VPC absent. Finalization seal
`ad2b702484b4a4d0fcc1b0d8569fd7fa49ac079a8e5d96a7330f900b4717f5c9`
and final 14-object post-delete backup seal
`84fb612a6b279a678635d2623d488840e31c72d60b2ce236d2af4fbcc3a03084`
close the attempt. Provider start-to-stop time was about 588 seconds; this is a
runtime bound, not an asserted invoice amount.

The repair removes the whole nested-mount failure class. External model,
training/adapter, output, and control binds use independent top-level container
paths; `/workspace` remains the only sealed read-only code/data bind. Runtime
path overrides do not mutate the frozen config or logical evidence paths. A
mount guard rejects external targets at or beneath `/workspace`, and the
archive rehearsal executes the exact archived baseline/campaign builders.
Evaluation archive seal
`497fdc835ac134d2a20a5fee96e063d60511ef6555f9e2df40db82d054ee5e2c`,
rehearsal seal
`8747337210b167a9b0099e605b98c3b7fbcf1e3b291066687b887fad3765aea0`,
and preparation seal
`7131fb8c768fad2c70bec28d36fb375a92d2e52911803265deec6559208628da`
bind the repaired bytes. The full local suite passes. Gate 1 remains closed;
the consumed approval does not authorize another GCloud VM.
