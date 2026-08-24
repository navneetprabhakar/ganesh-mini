# CUDA Gate 0 qualification

This image has two ordered qualification recipes. Gate 0B qualifies
`bf16-lora-primary-v1` first on one Linux NVIDIA GPU with at least 24 GiB
VRAM. `nf4-qlora-fallback-v1` is a separate 16 GiB fallback, not the default
training recipe. Both use sequence length 2,944, microbatch 1, gradient
checkpointing, LoRA r32/alpha64/dropout 0.05, response-only labels, Liger
0.8.2 fused linear cross-entropy without training-logit materialization, and
a 16-record train/save/reload/merge smoke.

The runner also performs a clearly labelled synthetic 2,944-active-token
backward-only memory-envelope probe with no optimizer step. The 16 real seed
records remain the only optimizer-stepped records. Evidence reports their
actual lengths, rendered hashes, adapter gradient coverage, throughput, and
peak allocated/reserved CUDA memory.

This directory is not execution evidence. A recipe passes only when its
`qualification-<recipe>.json` reports `status: passed` on a target host.

Host prerequisites:

- Docker with NVIDIA Container Toolkit and exactly one visible GPU;
- compute capability 8.0+ and BF16 support;
- at least 24 GiB VRAM for the primary or 16 GiB for the fallback;
- the pinned model and authorized seed JSONL already local; and
- `GANESH_GPU_HOURLY_USD` set and an external cost guard within the explicitly
  approved run ceiling.

Run the primary first:

```bash
GANESH_GPU_HOURLY_USD=0.80 scripts/cuda/run_qualification.sh \
  models/qwen3.5-2b-15852e8 \
  data/seed/ganesh_v01/train.jsonl \
  outputs/cuda/gate0
```

The fallback requires the primary attempt's evidence:

```bash
GANESH_GPU_HOURLY_USD=0.80 \
GANESH_PRIMARY_QUALIFICATION_EVIDENCE=outputs/cuda/gate0/qualification-bf16-lora-primary-v1.json \
scripts/cuda/run_qualification.sh \
  models/qwen3.5-2b-15852e8 \
  data/seed/ganesh_v01/train.jsonl \
  outputs/cuda/gate0 \
  nf4-qlora-fallback-v1
```

The image build may use the network; the target GPU run uses a prebuilt,
content-sealed image and no package network access. Its runtime must stay
within the active execution card's controller and cost bounds.
Qualification runs with `--network none`,
a read-only repository mount, one GPU, a 32 GiB host-memory limit, and an
execution-card timeout. The external provider lifecycle guard must include
host provisioning, verified GCS backup, automatic VM deletion, and complete
network teardown within the explicitly approved incremental ceiling.
