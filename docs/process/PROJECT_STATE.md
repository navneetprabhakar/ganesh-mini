# Project state

Last updated: 2026-08-22

## Current gate

Gate 0B and Gate 1 preparation in parallel:

- production Linux CUDA BF16 LoRA qualification, with NF4 QLoRA as fallback;
- frozen development and decision surfaces plus exact Qwen base baselines.

Local Apple runtime qualification is complete. Gate 0 remains fail-closed only
because the production CUDA matrix cannot be proven on Darwin.

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

## Not started or incomplete

- Production Linux CUDA BF16 LoRA runtime and peak-VRAM qualification
- NF4 QLoRA fallback qualification if the primary recipe crosses its measured
  memory or cost threshold
- Remaining development authoring: 150 tasks, 25 per lane
- Decision authoring and sealing: 360 tasks, 60 per lane
- Seed evaluation-overlap check, pending frozen evaluation manifests
- Current-toolchain re-execution of seed records that have executable bundles
- Exact Qwen base baseline on the frozen development surface
- Seed-pilot training
- Candidate quantization and final laptop certification
- Ganesh v0.1 rerun on the Ganesh Mini decision surface

## Next action

Qualify the exact production Linux CUDA BF16 LoRA recipe on non-GCloud compute,
measuring peak VRAM and throughput. Qualify NF4 QLoRA only as the predeclared
fallback. In parallel, complete and freeze the remaining six-lane development
and decision task manifests against the completed verifier. Then execute the
exact Qwen base baseline before opening the seed-pilot training gate.

## Authorization state

All work within the Ganesh Mini objective is authorized, including the Ganesh
v0.1 seed corpus, local and non-GCloud compute, downloads, long-running jobs,
training, evaluation, repository operations, and artifact publication.

GCloud usage is the only standing authorization boundary and requires explicit
user approval before any inspection, mutation, execution, or billing action.

An active 30-minute Codex heartbeat independently audits goal alignment. A
`DIVERGENCE` result pauses project mutations and compute until user direction.
