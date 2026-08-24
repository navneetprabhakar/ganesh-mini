# Ganesh Mini 1.0 execution plan — pass 2

Status: canonical plan

Date: 2026-08-22

## 1. Outcome contract

Build `ganesh-mini-1.0` from the post-trained `Qwen/Qwen3.5-2B` checkpoint.
The model must improve executable coding correctness across five product
language families while remaining useful on a personal laptop.

There are six evaluation lanes:

1. Go
2. Java
3. JavaScript
4. TypeScript
5. Python
6. Rust

JavaScript and TypeScript receive half-weight each when computing the
five-family macro score. They remain separate everywhere else.

Planned artifacts:

- merged BF16 Hugging Face checkpoint as the reference artifact;
- GGUF F16 for a 16 GB RAM laptop;
- GGUF Q8 for an 8 GB RAM laptop;
- optional LoRA adapter for reproducibility, never as the only release.

The primary runtime contract is text-only, non-thinking, 8,192-token context.
Vision and 262k context are out of scope for the laptop acceptance claim.

## 2. Core strategy

Use two supervised passes, not immediate RL:

- **Pass A — joint verified SFT:** teach the six lanes together using
  execution-verified generation and repair records, token-balanced across the
  five product families.
- **Pass B — failure-targeted correction:** continue from the best Pass A
  checkpoint on clusters that the correctly served base and Pass A candidate
  still fail, with 15–20% replay from the broad Pass A mix to control
  forgetting.

RLVR, DPO, ORPO, or repository-level trajectory training is a later mechanism
decision. It becomes eligible only if Pass A produces a real gain and the
remaining failures have a reliable, non-gameable preference or reward signal.

Why this is the default:

- A 2B model benefits more from dense, clean supervision than from a complex
  optimizer wrapped around weak or leaky rewards.
- Joint training reduces sequential-language forgetting.
- A separate correction pass makes the improvement mechanism measurable.
- BF16 LoRA avoids quantizing the frozen 2B backbone during optimization and is
  the primary quality-oriented recipe when it fits the selected GPU.
- NF4 QLoRA is a predeclared fallback for measured LoRA OOM or peak-VRAM
  failure. A cost-only switch requires a separately qualified cheaper host;
  QLoRA on the same GPU is not assumed to reduce cost. It does not define the
  final inference format.

## 3. Gates

### Gate 0 — upstream and toolchain qualification

1. Pin the exact Qwen revision, license, tokenizer/chat template, config, and
   expected file inventory.
2. Record model and processor byte sizes before download.
3. Pin a known-working Python 3.12, Transformers, PEFT, ms-swift,
   flash-linear-attention, causal-conv1d, PyTorch, CUDA, and llama.cpp matrix.
   Qualify BF16 LoRA first and the bitsandbytes NF4 path separately as fallback.
4. Prove text-only inference with the official chat template in non-thinking
   mode.
5. Inspect actual module names and gradient coverage. Do not inherit Gemma LoRA
   target modules.
6. Run a 16-record train/save/reload/merge smoke test and require numerically
   plausible loss plus byte-identical manifest tracking.
7. Convert the untouched base to GGUF and smoke both F16 and Q8 before assuming
   the trained model can be exported.

Exit: one reproducible serving and export contract with raw evidence. No
quality claim and no main training authorization.

### Gate 1 — evaluation before training

Freeze three disjoint surfaces before selecting training records:

- **Diagnostic:** public Multi-LiveCodeBench plus compatible portions of
  EvalPlus and DevBench. Public scores are useful but never the sole promotion
  evidence. If the frozen admission policy yields zero compatible public
  tasks, retain the complete exclusion report and proceed on the private
  development surface; do not weaken licensing, reference, or known-bad
  requirements merely to manufacture a diagnostic score.
- **Development:** 30 private tasks per lane, 180 total, equally split between
  code generation and bug repair.
- **Decision:** 60 private tasks per lane, 360 total, equally split between
  generation and repair. Prompts stay sealed until one declared final opening.

Every private task must have independently authored tests, a known-good
reference, at least one known-bad implementation that the tests reject,
toolchain pins, timeout limits, and immutable hashes. Generated code runs in a
network-disabled sandbox.

Baseline the exact upstream Qwen checkpoint on diagnostic and development
surfaces. Keep thinking mode out of the primary score; it may be reported as a
separate experiment with its own serving contract.

Exit: frozen task manifests, fail-closed verifiers, base results, and zero
decision-prompt exposure.

### Gate 2 — seed import, compatibility, and expansion

The user-authorized Ganesh v0.1 corpus is the starting dataset. At inspected
source commit `9552867c7641a5f11acadb84d19bfb8d723ab0ae`, the selected seed
inventory is 1,399 training rows and 50 validation rows:

| Lane | Training | Validation | Source path |
|---|---:|---:|---|
| Python | 468 | 30 | `data/train/multisource_python_v2/` |
| Go | 163 | 4 | `data/train/multiling_v1/go/` |
| Java | 146 | 4 | `data/train/multiling_v1/java/` |
| JavaScript | 222 | 4 | `data/train/multiling_v1/js/` |
| TypeScript | 218 | 4 | `data/train/multiling_v1/ts/` |
| Rust | 182 | 4 | `data/train/cuda_lora_v5/rust/` |
| **Total** | **1,399** | **50** | |

This corpus does not need a new ownership, license, or historical-teacher
provenance decision. Import it with source commit, paths, byte hashes, record
IDs, and original split lineage preserved. Normalize it to the Qwen chat
schema, rerun it on current language toolchains, and check it against the new
evaluation manifests. These are compatibility and integrity checks, not a
fresh rights-admission process.

Use the cleaned seed first. Do not inflate it to a predetermined scale before
measuring the Qwen base and seed-trained pilot. If the seed produces a credible
but capacity-limited gain, expand toward 20,000–60,000 verified records based
on measured per-lane failure clusters. Larger 60,000–120,000 runs remain an
option only if the smaller expansion has not saturated.

Composition rules:

- balance training tokens 20% each across Go, Java, JavaScript/TypeScript,
  Python, and Rust;
- split the JavaScript-family allocation roughly equally between JavaScript
  and TypeScript unless measured yield makes that impossible;
- target roughly 60% generation and 40% repair;
- include standard-library, data-structure, concurrency, parsing, error
  handling, API-contract, and edge-case work; avoid a corpus dominated by
  competitive-programming puzzles;
- keep most examples within the laptop product envelope; long repository
  trajectories do not dominate a single-file coding model.

Every newly added non-v0.1 row needs:

- source URI, immutable source revision, record ID, and transformation lineage;
- source and output rights fields with an allowlisted license/terms decision;
- language/compiler version and deterministic executable result;
- exact and fuzzy deduplication against all evaluation surfaces and within the
  corpus;
- prompt, answer, tests, execution transcript, and content hashes;
- quality labels and rejection reason when excluded.

NVIDIA OpenCodeInstruct is a candidate expansion source, not pre-approved data.
Its tests must be re-run and sampled with stronger independent tests.
Open-SWE-Traces is optional for a later agentic/repository phase. These new
sources follow the full rights and provenance gate; that requirement does not
retroactively apply to the explicitly authorized v0.1 seed.

Exit: an immutable seed manifest with per-lane token counts, source-file
hashes, compatibility results, evaluation-overlap report, and converted
train/validation hashes. Any expansion gets a separate rights and provenance
manifest.

### Gate 3 — bounded multilingual pilot

Run the first pilot on the full 1,399-row v0.1 seed corpus. Because its lane
sizes differ, sample by a five-family token-weight policy and report both seen
tokens and effective epochs per lane. Preserve the original 50 validation rows
for loss diagnostics, but select the model only on the new private development
surface.

Starting recipe, subject to the Gate 0 smoke result:

- BF16 base loading with BF16 LoRA compute on a CUDA GPU with at least 24 GB;
- freeze vision components;
- response-only loss using the exact Qwen chat template;
- 2,944-token training sequence length with packing only after a packing
  equivalence test;
- LoRA rank 32, alpha 64, dropout 0.05;
- micro-batch 1, gradient checkpointing, and gradient accumulation to reach the
  frozen effective batch size;
- a fixed token budget capped at three balanced effective epochs, with
  half-epoch checkpoints, cosine schedule, and warmup ratio 0.03;
- learning rate selected by a tiny predeclared two-point pilot, not an open
  sweep;
- checkpoint on a token interval and score only the private development set.

The original 4,096-token envelope was reduced to 3,072 only after two sealed
L4 executions showed that both LoRA and QLoRA OOM before the first training
record. The 3,072-token NF4 fallback then reached backward but missed capacity
by 21,894,267 bytes. The current 2,944-token envelope is still not a data
truncation concession: the frozen prepared corpus contains 2,155 sampled
training records, the longest is 2,938 tokens, and no train or validation
record exceeds 2,944. The model's serving context contract is unchanged.

The sealed 2,944-token L4 retry failed NF4 backward with a 63,832,064-byte
allocation shortfall while PyTorch reported about 95,934,218 bytes reserved
but unallocated. A later `us-east1` Flex-start execution tested the versioned
`expandable_segments:True` allocator contract. It reduced fragmentation but
NF4 still failed the synthetic backward envelope, with only 59.12 MiB free and
a 46 MiB request followed by a 20 MiB allocator mapping failure. The allocator
is therefore insufficient by itself.

The measured dominant allocation was vocabulary loss materialization. At 2,944
tokens, Qwen's 248,320-token vocabulary creates 1,462,108,160 BF16 logit bytes;
the Transformers causal-LM loss upcasts that tensor to 2,924,216,320 FP32 bytes,
matching the observed BF16 2.72 GiB allocation request. The executed versioned
qualification uses Liger Kernel 0.8.2 only for fused linear cross-entropy, so
training loss is computed without materializing full-vocabulary logits. RoPE,
RMSNorm, SwiGLU, sequence length, rank, optimizer, data, and serving behavior
remain unchanged. Gate 0B passed this contract on one L4: the full envelope,
16 real optimizer steps, adapter save/reload, safe merge, and peak-VRAM ceiling
all passed. This qualifies the mechanism; it is not a model-quality result.

To avoid repeated L4 provisioning and repeated loading of the same qualified
assets, Gate 1 and the bounded Gate 3 loop may execute as one staged campaign
on a single VM. This does not collapse the gates: the exact base baseline must
open Gate 1 before the training workspace is mounted; each LR candidate must
finish its frozen 400,000-token budget and complete development evaluation;
the sealed LR rule must select the main-run rate; and the main 636,093-token
seed run must complete development evaluation and promotion adjudication.
Evaluation and training use separate content-sealed workspaces and separate
offline containers. A failed phase stops later phases. Runtime evidence is
backed to GCS throughout, and teardown still requires independently verified
terminal backup and exact resource-absence proof.

The fallback recipe changes only base loading to bitsandbytes 4-bit NF4 with
BF16 adapter compute. It is eligible only after the primary recipe records an
OOM or exceeds the frozen peak-VRAM ceiling. Record the trigger and keep all
other comparable parameters fixed. A smaller memory footprint alone is not a
quality or cost result.

Exit: proceed only if at least four of five product families improve, no lane
shows a material regression, formatting/truncation failures do not increase,
and save/reload results reproduce. Otherwise change data or mechanism before
scaling.

### Gate 4 — Pass A joint verified SFT

If the seed pilot qualifies, either promote it directly to Pass B or run one
technically validated expansion recipe on a frozen 20k–60k mix. The decision is based on
per-lane learning curves and failure coverage, not a row-count target. Rank 64
is the initial expansion candidate if the pilot shows gradient coverage and no
overfit; rank 32 is the predeclared lower-capacity fallback. Sequence length
may move to 8,192 only if measured training cost and example-length coverage
justify it.

Select checkpoints on the development surface using:

- five-family macro executable pass@1;
- per-lane regressions and paired task transitions;
- malformed, repetitive, truncated, and non-code rates;
- a small frozen general instruction-following retention suite.

Validation loss is diagnostic and cannot select the release by itself.

### Gate 5 — Pass B failure-targeted correction

Cluster failures from the base and selected Pass A checkpoint without viewing
decision prompts. Build a separately admitted correction set that oversamples
real failure mechanisms rather than languages with easier test generation.

Continue the adapter for at most 20–35% of Pass A's token budget, mixing
15–20% broad replay. Keep the best Pass A checkpoint as a mandatory comparator.
Pass B is rejected if gains come from format mimicry, verifier exploitation,
or material loss in a previously improved lane.

### Gate 6 — final evaluation and comparison

Open the private decision suite once for these immutable candidates:

- exact upstream `Qwen/Qwen3.5-2B`;
- selected Ganesh Mini Pass A checkpoint;
- selected Ganesh Mini Pass B checkpoint, if it qualified;
- Ganesh v0.1, served through its own pinned chat template and extraction
  contract on the identical tasks.

Ganesh v0.1 is a reference competitor, not the causal baseline: it has a
different 12B backbone and a different resource envelope. Report four views:

1. per-lane and five-family macro pass@1;
2. paired wins, losses, ties, confidence intervals, and McNemar result versus
   Qwen base;
3. quality per model GB and verified tasks per wall-clock hour;
4. peak RSS, startup time, prompt/decode throughput, and energy if available.

Public diagnostic results are reported separately and labelled for possible
training contamination. Historical Ganesh v0.1 scores are not mixed with new
results; it must be rerun on the frozen Ganesh Mini harness.

### Gate 7 — merge, quantize, and laptop certification

1. Merge the selected adapter into a BF16 reference checkpoint.
2. Convert from the merged reference to GGUF F16 and Q8 using one pinned
   llama.cpp revision.
3. Run an export equivalence sample across all six lanes before benchmarking.
4. Certify on actual machines or constrained test hosts:
   - Q8: peak RSS at or below 7 GB on an 8 GB profile at 8,192 context;
   - F16: peak RSS at or below 14 GB on a 16 GB profile at 8,192 context.
5. Record artifact bytes, hashes, load time, prompt/decode tokens per second,
   thermal throttling, and failures.
6. Rerun the decision outputs only for quantization equivalence; do not use
   quantization results to tune the model.

If F16 misses 16 GB or Q8 misses 8 GB, narrow the runtime claim. Do not reduce
context or hide OS overhead after seeing the result.

### Gate 8 — release decision

Release is eligible only if all of the following hold:

- Ganesh Mini beats the Qwen base on the five-family macro decision score;
- paired aggregate improvement is statistically supported, with exact
  numerator and denominator reported;
- no compiler lane regresses by more than two tasks on the 60-task lane;
- Q8 retains at least 98% of the merged reference checkpoint's solved decision
  tasks, or the exact loss is explicitly accepted;
- both advertised RAM profiles pass;
- data rights, provenance, training, model, benchmark, and quantization
  manifests are complete;
- limitations are explicit, including whether Ganesh v0.1 remains stronger in
  absolute correctness.

Publication to Hugging Face or another registry is authorized after every
technical release gate passes. A failed candidate remains a documented
experiment, not version 1.0.

## 4. Cost and execution controls

Before each training run, create and retain an execution card containing:

- exact dataset and manifest hashes;
- model revision and expected download bytes;
- recipe and package-lock hashes;
- accelerator type/count, provider, region, provisioning model, and hourly
  price;
- measured tokens/second from a bounded pilot;
- expected duration, hard-stop duration, expected cost, and cost ceiling;
- checkpoint interval, durable upload target, resume behavior, and teardown
  plan;
- explicit stop conditions.

The card is an evidence and cost-control artifact, not an approval request.
Local and non-GCloud execution are authorized. GCloud is the sole standing
approval boundary and must not be used without explicit user authorization.
The Qwen3.5 hybrid architecture must be benchmarked before extrapolating Gemma
v0.1 throughput.

## 5. What is intentionally not copied from Ganesh v0.1

- Gemma-specific model loading, target modules, chat template, and serving
  flags
- historical evaluation sets as new decision evidence
- historical benchmark numerators as comparable evidence
- Python-first sequential language expansion
- public-benchmark-only release claims
- the assumption that a successful adapter load means a successful model

The authorized v0.1 training corpus is deliberately reused. Other reusable
concepts are the fail-closed executable verifiers, immutable manifests, raw
evidence retention, checkpoint resume discipline, and exact resource execution
cards. Code implementing those concepts is still reviewed before it is ported.

## 6. Immediate implementation queue

1. Add Gate 0 model-inventory and dependency-lock tooling with tests.
2. Add the six-lane verifier interface and sandbox contract.
3. Define task and result JSON Schemas before authoring evaluation data.
4. Build a base inference smoke harness that preserves rendered prompts and
   raw outputs.
5. Download and verify the exact pinned model inventory after recording its
   expected size and immutable identities.

Training starts only after its technical predecessor gates pass. This is a
readiness dependency, not an authorization dependency.
