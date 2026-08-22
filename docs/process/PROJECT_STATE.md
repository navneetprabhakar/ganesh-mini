# Project state

Last updated: 2026-08-22

## Current gate

Gate 0: upstream identity, architecture, toolchain, and serving qualification.

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

## Not started

- Exact upstream revision pin and file-inventory hash
- Model download
- Local or CUDA inference
- Evaluation task authoring or freezing
- Seed evaluation-overlap check, pending frozen evaluation manifests
- Current-toolchain re-execution of seed records that have executable bundles
- Training
- Quantization
- Benchmark execution

## Next action

Complete Gate 0 runtime qualification: create the isolated Python 3.12
environment, download and byte-verify the pinned Qwen inventory, inspect actual
LoRA module/gradient coverage, and run inference, train/save/reload/merge, and
GGUF export smokes. In parallel, begin authoring and freezing the six-lane
development and decision task manifests against the completed evaluator.

## Authorization state

All work within the Ganesh Mini objective is authorized, including the Ganesh
v0.1 seed corpus, local and non-GCloud compute, downloads, long-running jobs,
training, evaluation, repository operations, and artifact publication.

GCloud usage is the only standing authorization boundary and requires explicit
user approval before any inspection, mutation, execution, or billing action.

An active 30-minute Codex heartbeat independently audits goal alignment. A
`DIVERGENCE` result pauses project mutations and compute until user direction.
