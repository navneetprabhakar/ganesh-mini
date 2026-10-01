# Gate 3 full capability pilot on GCloud — prospective execution boundary

Status: local implementation in progress; **not a ready execution card**.
The prior qualification-only $5 authorization is closed. Do not allocate
under that card or present the short probe as model-quality evidence.

## Frozen work

Run one unique 900-row, 651,639-input-token epoch for each of the two
predeclared learning rates, `1e-5` and `3e-5`, with the admitted 720 capability
plus 180 replay package. Keep the pinned Qwen revision, BF16 attention-only
rank-8 LoRA, response-only loss, 2,944-token limit, family weights, fused
loss, checkpoint and stop rules. Use one Linux L4 satisfying the separately
approved 22-GiB CUDA-visible/BF16/single-device contract per candidate.
The 360-task decision set remains closed.

After both candidates finish and their checkpoints are verified, run the
frozen 30-task canary on each and select by the existing no-regression rule.
Run all 180 private development tasks only on the selected candidate. Keep
training and evaluation workspaces separate; generated code executes only in
the network-disabled resource-limited verifier. Do not claim Gate 3 success
until these executable quality checks, save/reload equivalence, and evidence
seals pass.

## Planning evidence and ceiling request

The independently verified L4 qualification measured 329.666 input
tokens/second over 16 longest unique rows and two optimizer steps. At that
rate the pair is about 3,953 training seconds before startup, validation,
checkpointing, evaluation and backup. A 1.5x training-time allowance is
about 5,930 seconds. This is a sizing operand, **not a full-job ETA**.

For `us-central1`, the currently published on-demand g2-standard-8 price is
$0.853624312/hour; a 200-GiB balanced persistent disk is approximately
$0.0273972/hour, so a two-hour VM-plus-disk provider STOP upper is
$1.762043024. Sources checked 2026-09-30:
https://cloud.google.com/products/compute/pricing/accelerator-optimized
and https://cloud.google.com/compute/disks-image-pricing.

Proposed **$15 absolute incremental ceiling** for Gate 3 full-pilot training
and executable evaluation only, subject to Navneet's explicit acceptance:

- Up to four allocated two-hour L4 stages (two training candidates, up to two
  evaluation stages): $7.048172096 conservative VM-plus-disk upper.
- $2 reserved for four cross-region input-transfer allowances at $0.50 each.
- $5.951827904 remaining for checkpoint/evidence storage, backup operations,
  cleanup and scheduling variance. A candidate or evaluation stage stops
  before exceeding both its own bound and this cumulative ceiling.

No automatic paid retry after an allocated failure. A zero-runtime stockout
may move to a prebound US zone only after exact backup, cleanup and double
absence. A larger host, longer runtime, extra candidate, main Gate 4 SFT, or
release task is outside this proposal. Pricing is an upper-bound model, not
an invoice or a guarantee of capacity. Recompute the budget if the scope,
host, price or disk changes.

## Required readiness before any allocation

1. Seal a new evaluation-free workspace and exact model materializer/input
   generations, plus a distinct GCloud candidate card for each LR. The
   GCloud provider card/runner branch has initial local tests, but this alone
   is **not launch-ready**.
2. Implement and test actual-host short preflight, card binding and provider
   STOP; periodic checkpoint upload; terminal manifest/independent two-download
   GCS verification; and backup-before-deletion with double exact resource
   absence. No candidate training starts on a draft card.
3. Seal a separate evaluation workspace with the frozen task IDs and
   verifier contract. Keep private prompts out of the training workspace and
   open only the authorized canary/development surfaces.
4. Obtain the explicit incremental ceiling and exact scope approval before
   any new GCloud inspection, upload or allocation for this plan.

Hugging Face model publication is already authorized **only after** all
frozen release gates pass. A successful Gate 3 pilot is not Gate 8. The
historical Gate 0B raw-report recovery gap remains a release hold.
