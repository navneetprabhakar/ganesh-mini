# Gate 3 post-qualification local readiness — 2026-09-30

Status: local assessment only; no full-pilot execution authority or ready card.

## Verified terminal state

Navneet asked to save artifacts, kill any VM, and continue locally. A fresh
read-only inventory of `executespecv1` returned no instances, disks, or
reserved addresses; the only network is `default`. There was no live Ganesh
resource to stop or delete. All 12 terminal objects of qualification attempt
`20260930T131906Z` are present in GCS; its independent backup verification
reported `verified`, and its finalization records backup-before-teardown and
double exact resource absence. The first `us-central1-a` attempt was a
separately finalized zero-runtime capacity refusal. No new GCloud resource was
created for this assessment.

## What the qualification establishes

The sealed 16-row/two-step report at
`measurement/gate3/capability-scale-v1/gcloud-qualification/20260930T131906Z/terminal-roundtrip/output/throughput.json`
passed with finite loss, 4,634,705,920 peak-VRAM bytes, and 37,480 input
tokens in 113.691 training seconds: 329.666 input tokens/second. The L4
hardware preflight separately passed at 23,659,151,360 CUDA-visible bytes,
one device, and BF16. This qualifies the mechanism and short-probe throughput,
not a full epoch, model quality, candidate selection, or Gate 3.

At that measured rate, 651,639 tokens take about 1,977 training seconds per
candidate and 3,953 seconds for the frozen `1e-5` and `3e-5` pair. A 1.5×
training-time margin is about 2,965 seconds per candidate, 5,930 seconds
combined. These are arithmetic planning operands, not full-job wall times or
cost claims: startup, validation, checkpointing, save/reload, canary and
development evaluation, backup, and capacity variability remain unmeasured.

## Local checks and explicit gaps

- Fresh static preflight at
  `measurement/gate3/capability-scale-v1/full-pilot-local-readiness-20260930/static-preflight.json`
  passed the sealed 900 rows, 651,639 input tokens, and 50 validation rows;
  report seal `e921f11edfb59f1d1fbf57336b36652b1ad142189071e20c213caf53f8272831`.
- Draft card at the same directory's `draft-card.json` is sealed at
  `8248aa6f07f9b30b7c9e5d4250554dfb58e268eb156bb1bd8a9e4740b505c265`
  with `prepared-not-executable` status. The local host is Darwin without
  CUDA; do not substitute MPS under the frozen pilot contract.
- The current provider binder and `run_sft.py` explicitly reject GCloud for
  full capability-pilot cards. A distinct fail-closed GCloud execution-card
  path is needed. It must bind the approved L4 floor, the exact frozen inputs,
  a fresh actual-host throughput/preflight, each candidate LR, host identity,
  checkpoint/backup schedule, cost and wall ceilings, and resume/stop rules.
- The full pilot needs two full-epoch candidates, the frozen 30-task canary
  comparison, then the selected candidate's 180-task development evaluation.
  The 360-task decision set remains closed. No AI review is human sign-off.
- The historical Gate 0B raw-report recovery gap is a separate release hold.

## Next safe local implementation

Implement and test a GCloud-specific capability-pilot card and controlled
runner/backup contract without allocating compute. Keep the qualification
card and all previous failed evidence immutable. Before any GCloud full-pilot
use, produce a versioned exact scope and conservative absolute cost ceiling
for Navneet's explicit approval. The previous $5 approval was
qualification-only and is consumed. Preserve complete checkpoints, raw
evaluation outputs, independent GCS verification, and double teardown
absence when a later authorized run completes.

Focused local tests (`test_cuda_host_floor`, `test_preflight_gate3_capability_pilot`,
`test_gcloud_gate3_qualification`, `test_inspect_model_archive`,
`test_package_workspace`) passed on 2026-09-30. This assessment is not a
training run or a model release decision.
