# Gate 3 capability-data pilot execution contract — 2026-09-24

Status: prospective runtime implementation contract; not a ready execution
card or a model-quality result. Non-GCloud training authority already exists.

## Exact inputs

- Data-package admission: `measurement/gate3/capability-scale-v1/token-length-replacement-v1/final-package/data-package-seal.json`, report seal `149b030f11bc0eb054f0a4d511432f33b4123e3b65fab77c2166dca23d1190aa`.
- Prepared pilot: `artifacts/train/gate3-capability-pilot-v2/prepared-manifest.json`, manifest seal `4bae0de2096ce8ae973d0f7b3ecc9214d8b6ef2e3addfb31cc4afd37446c2d01`; 900 unique rows, 651,639 input tokens, prepared-train SHA-256 `6f43f373c34fd61749b44ef73eb8803f9f0df33ad13b2358ee6efde95fe5fa1f`.
- Frozen 50-row prepared validation SHA-256 `6a9d3aa37b30bc2672517f6d63113011de5f8156aa1049e588fdc70a36b77f46`; a fresh local encoding was byte-identical.
- Qwen revision `15852e8c16360a2fea060d615a32b45270f8a8fc`.

The earlier 1,399-row seed-pilot and 3,225-row expansion-pilot cards do not
describe this cohort. Their evidence, checkpoints, and failed results stay
immutable and cannot be relabeled as a capability-data pilot.

## Frozen quality and runtime boundaries

Use the qualified BF16, attention-only rank-8 LoRA mechanism, response-only
loss, 2,944-token maximum, single Linux CUDA device with at least 24 GB VRAM,
fused linear cross-entropy, and objective weights giving Go/Java/Python/Rust
20% each and JavaScript/TypeScript 10% each. One unique epoch is exactly
651,639 input tokens; no duplication, truncation, or sequence-length increase.
The old full-epoch two-learning-rate comparison (`1e-5`, `3e-5`) and the frozen
30-task canary selection rule should be retained unless a separately justified
and versioned change is made. Full 180-task private development promotion
follows candidate selection; the 360-task private decision surface stays
closed. Validation loss is diagnostic, never a substitute for executable
promotion.

Each candidate must have its own immutable execution card binding exact
prepared data, tokenizer/model and dependency locks, host hardware, provider,
price, wall and cost ceilings, measured throughput, checkpoint schedule,
durable retention, resume behavior, and stop conditions. A card is `ready`
only after a fail-closed preflight on the actual host. A local MPS device is
not a CUDA substitute. Non-GCloud CUDA compute is within existing authority;
GCloud usage requires a fresh explicit authorization and must not be inspected
or used under this contract alone.

## Required implementation before launch

1. Add a distinct capability-pilot config/card schema rather than changing
   frozen seed/expansion schemas. Bind 900 rows and 651,639 tokens, both
   prepared file hashes, the data-package seal, and the existing model contract.
2. Extend or wrap the SFT runner so it accepts only that new card/schema,
   checks one-epoch token and row accounting, keeps optimizer-group anomaly
   detection and save/reload equivalence, and writes resumable hash-sealed
   telemetry/checkpoints. Test rejection of old cards and altered data.
3. Preflight the actual single-CUDA host and record a short bounded throughput
   measurement before setting time/cost ceilings. Do not extrapolate an old
   GCloud L4 rate as if it were measured on a new provider.
4. Seal training/evaluation workspace separation; execute the 30-task canary
   for both completed LR candidates, select by the existing no-regression
   rule, then run 180 development tasks on the selected candidate. Require
   at least four of five product families improved, no material lane
   regression, no formatting/truncation increase, and reproducible save/reload.
5. Preserve complete raw evidence and final backup before any compute teardown.

Until these checks pass, Gate 3 is open and Gates 4–8, Hugging Face model
publication, and paper-quality model-result claims remain downstream.
