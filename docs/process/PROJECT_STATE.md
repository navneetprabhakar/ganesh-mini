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

## Not started

- Exact upstream revision pin and file-inventory hash
- Model download
- Local or CUDA inference
- Evaluation task authoring or freezing
- Dataset download or admission
- Training
- Quantization
- Benchmark execution

## Next action

Implement Gate 0 as a bounded, testable toolchain probe. Before downloading
the model, record its exact revision, expected byte inventory, and download
size. A download larger than 5 GB is an approval stop.

## Approval state

No paid compute, long-running job, dataset admission, training run, decision
set opening, model publication, or dataset publication is authorized.
