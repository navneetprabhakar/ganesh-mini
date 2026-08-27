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
- PyTorch 2.13 release-candidate pairing:
  <https://dev-discuss.pytorch.org/t/pytorch-2-13-rc1-produced-for-pytorch-torchvision/3401>
  - binds Torch 2.13.0 to Torchvision 0.28.0, including CUDA 13.0 wheels
- bitsandbytes 0.49.2 `Params4bit` implementation:
  <https://github.com/bitsandbytes-foundation/bitsandbytes/blob/0.49.2/bitsandbytes/nn/modules.py>
  - moves packed 4-bit data and its quantization state through
    `Params4bit.to`, including CUDA-to-CPU movement for the frozen,
    text-inactive vision tower
- Transformers import utilities:
  <https://huggingface.co/docs/transformers/v5.8.1/en/internal/import_utils>
  - fast image-processing modules require the vision, Torch, and Torchvision
    backends; the selected Qwen checkpoint retains an image-text architecture
    even though the product contract is text-only
- Flash Linear Attention installation contract:
  <https://github.com/fla-org/flash-linear-attention/blob/main/INSTALL.md>
  - version 0.5 splits `fla-core` from model/layer packaging and requires an
  explicit backend extra; CUDA uses upstream Triton with a matching Torch
  installation
- Liger Kernel repository and v0.8.2 release:
  <https://github.com/linkedin/Liger-Kernel> and
  <https://github.com/linkedin/Liger-Kernel/releases/tag/v0.8.2>
  - v0.8.2 exposes Qwen3.5 dense and multimodal patch functions
  - its fused linear cross-entropy path computes training loss without
    materializing the complete vocabulary logits tensor
  - Ganesh Mini enables only that loss path; other Liger kernel replacements
    remain disabled until separately justified and qualified

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
- McEval-Instruct:
  <https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct>
  - CC-BY-SA-4.0, 35,943 instruction rows across 36 programming languages
  - the pinned target-language inventory is useful for drafting but provides
    no independent behavioral tests and is not directly admitted
- MdEval-Instruct:
  <https://huggingface.co/datasets/m-a-p/MdEval-Instruct>
  - MIT, 16,008 synthetic repair conversations produced by injecting bugs
  - source-provided tests are useful evidence but do not satisfy the current
    independent-test requirement on their own
- Codex CLI non-interactive mode:
  <https://learn.chatgpt.com/docs/non-interactive-mode>
  - `codex exec` supports ephemeral runs, JSONL events, output schemas, and a
    separate final-output file
  - Ganesh Mini uses isolated architect and test-author invocations and seals
    raw run evidence because the requested model alias is not snapshot-pinned

## Candidate public diagnostics

- Multi-LiveCodeBench: <https://github.com/Multi-LCB/Multi-LCB>
  - explicitly supports Python, Java, Rust, Go, TypeScript, and JavaScript
- Microsoft DevBench: <https://github.com/microsoft/devbench>
  - 1,800 completion tasks; useful for Python, Java, JavaScript, and TypeScript
- Multi-SWE-bench: <https://github.com/multi-swe-bench>
  - multilingual repository issue resolution including Java, TypeScript,
    JavaScript, Go, and Rust; a stretch evaluation, not a v1 promotion blocker
