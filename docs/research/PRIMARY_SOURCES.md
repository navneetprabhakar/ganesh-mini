# Primary sources

Verified on 2026-08-22. These links inform the plan but do not replace pinned
revisions and local evidence during execution.

## Backbone and runtime

- Qwen model card: <https://huggingface.co/Qwen/Qwen3.5-2B>
  - Apache-2.0
  - post-trained causal language model with vision encoder
  - 2B language-model parameters, 24 layers, 248,320-token padded embedding
  - native 262,144-token context
  - non-thinking is the default for the 2B checkpoint
  - official vLLM text-only mode skips vision profiling to free KV-cache RAM
- Qwen configuration:
  <https://huggingface.co/Qwen/Qwen3.5-2B/blob/main/config.json>
- Transformers Qwen3.5 implementation notes:
  <https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/qwen3_5.md>
  - hybrid 3:1 Gated DeltaNet/full-attention stack
  - fast DeltaNet kernels require current optional dependencies; fallback is
    slower and more memory hungry
- ms-swift Qwen3.5 Transformers training example:
  <https://github.com/modelscope/ms-swift/blob/main/examples/models/qwen3_5/transformers.sh>
- ms-swift training documentation:
  <https://github.com/modelscope/ms-swift/blob/main/docs/source_en/Instruction/Pre-training-and-Fine-tuning.md>
  - supports SFT, LoRA, and QLoRA with the Transformers backend
  - exact Qwen3.5 dependency and recipe compatibility still has to be pinned
    and proven by the Gate 0 smoke test

## Candidate training data

- NVIDIA OpenCodeInstruct:
  <https://huggingface.co/datasets/nvidia/OpenCodeInstruct>
  - CC-BY-4.0, five million instruction records, unit-test fields
  - candidate source only; its shipped tests and language coverage must be
    independently measured before admission
- NVIDIA Open-SWE-Traces:
  <https://huggingface.co/datasets/nvidia/Open-SWE-Traces>
  - CC-BY-4.0, repository-level agent trajectories
  - optional later source; long tool trajectories are not automatically a good
    fit for a 2B single-file laptop model

## Candidate public diagnostics

- Multi-LiveCodeBench: <https://github.com/Multi-LCB/Multi-LCB>
  - explicitly supports Python, Java, Rust, Go, TypeScript, and JavaScript
- Microsoft DevBench: <https://github.com/microsoft/devbench>
  - 1,800 completion tasks; useful for Python, Java, JavaScript, and TypeScript
- Multi-SWE-bench: <https://github.com/multi-swe-bench>
  - multilingual repository issue resolution including Java, TypeScript,
    JavaScript, Go, and Rust; a stretch evaluation, not a v1 promotion blocker
