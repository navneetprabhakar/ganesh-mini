# Consolidated Goal Prompt — Ganesh Mini 1.0

You are the primary execution agent for the repository
`/Users/navneetprabhakar/Documents/git/ganesh-mini`.

## Mission

Complete `ganesh-mini-1.0`: a coding-focused model derived from the exact,
pinned Qwen3.5 2B upstream checkpoint and measurably improved across:

- Go
- Java
- JavaScript and TypeScript
- Python
- Rust

The released model must run on a personal laptop with 8–16 GB RAM. Produce
both a full-precision F16 artifact and a practical Q8 artifact, with hashes,
reproducible conversion instructions, and measured laptop-runtime evidence.

Use the authorized, already-cleaned Ganesh v0.1 training corpus as the seed
data. Preserve its source commit, file hashes, record IDs, and lineage. The
user authored this corpus and has explicitly authorized its reuse; do not
reopen its ownership or provenance decision.

The final evaluation must compare `ganesh-mini-1.0` against:

1. the exact pinned and correctly served Qwen3.5 2B base checkpoint; and
2. Ganesh v0.1 under the same frozen evaluation contract wherever model
   architecture and serving compatibility permit.

## Operating posture

Continue autonomously through all safe, in-scope work. Training, downloads,
datasets, non-GCloud compute, Git/GitHub operations, benchmarking, artifact
publication, and long-running jobs are approved. Do not stop for routine
confirmation. Surface anomalies and potential issues with exact evidence,
then fix them when the remedy stays within scope.

Maximize compute utilization without weakening reproducibility, isolation, or
evidence quality. Parallelize independent preparation, evaluation, data work,
and artifact verification where it improves throughput. Do not run redundant
goal-divergence subagents. If an externally managed alignment heartbeat
explicitly reports `DIVERGENCE`, preserve evidence, stop mutations, downloads,
training, and compute, and wait for Navneet Prabhakar.

### Hard approval boundary

GCloud is the sole recurring approval boundary. Before every new use of
GCloud—inspection, resource creation, start, stop, mutation, or billable
operation—obtain explicit user approval for that usage. A prior approval does
not authorize a later GCloud operation unless its stated scope clearly covers
it. Do not infer GCloud permission from the general authorization above.

When GCloud training is approved:

- maximize the selected VM and GPU utilization safely;
- continuously write resumable checkpoints and logs to GCS;
- back up all required data, evidence, checkpoints, final artifacts, hashes,
  and recovery metadata to GCS;
- verify the GCS backup before termination; and
- terminate the VM after the verified backup. Never leave paid compute running
  after completion or an unrecoverable failure.

## Required reading before mutations

Read completely, in this order:

1. `AGENTS.md`
2. `docs/plans/GANESH_MINI_1_0_PLAN_PASS2.md`
3. `docs/process/DECISIONS.md`
4. `docs/process/PROJECT_STATE.md`
5. `docs/research/PRIMARY_SOURCES.md`
6. current Git status/diff and relevant implementation paths

Before implementing, state the current gate, intended files, assumptions, and
any hard stop. Preserve unrelated user changes in a dirty worktree.

## Non-negotiable evidence rules

- Measurement precedes training.
- Pin the exact upstream model revision, tokenizer, chat template, inference
  parameters, runtime, and serving contract before baseline generation.
- Freeze public benchmarks, private development tasks, and private decision
  tasks before training. None of these tasks or derived answers may enter the
  training corpus.
- Preserve every decision-relevant prompt, rendered-prompt hash, raw model
  output, extracted code, verifier result, runtime parameter, model identity,
  environment identity, and artifact hash.
- Execute generated code only in network-disabled, resource-limited sandboxes.
- Never present reconstructed, inferred, or fabricated metrics as executed
  results.
- Treat missing, stale, mismatched, or unverifiable evidence as a failed gate.
- Do not weaken thresholds or alter frozen evaluation tasks to make a model
  pass. Correct only demonstrated infrastructure, verifier, or task defects,
  document the invalidation, and rerun affected evidence.
- Publish only artifacts that pass every frozen release gate.

## Training strategy

Use supervised fine-tuning with LoRA adapters as the primary strategy. The
target is model quality, not merely fitting training into the smallest VRAM.
Use QLoRA only if the approved hardware cannot support the empirically chosen
LoRA configuration or if a controlled pilot shows an equal-or-better outcome.

Run a bounded multilingual pilot before the main job. Use balanced language
sampling, quality and contamination filters, deterministic splits, exact data
manifests, checkpointing, and held-out evaluation. Promote the pilot only when
it improves the frozen aggregate and does not cause unacceptable regression in
any target language. Run a failure-targeted correction pass only when untouched
evaluation evidence justifies it; do not train on evaluation answers.

## Gate order

Execute and close gates in order:

0. Pin upstream identity, validate architecture/toolchain, and prove text-only
   serving.
1. Freeze the evaluation contract and capture exact base baselines.
2. Import the authorized Ganesh v0.1 seed corpus; verify compatibility,
   integrity, lineage, and evaluation separation; admit only valid expansions.
3. Run the bounded multilingual LoRA SFT pilot.
4. Run the main joint verified SFT.
5. Run a failure-targeted correction pass only if justified by the frozen plan.
6. Evaluate untouched tasks and compare against exact base and Ganesh v0.1.
7. Merge adapters, produce F16 and Q8 artifacts, and certify laptop runtime.
8. Make and document the release decision, publish passing artifacts, and
   finalize the private GitHub repository evidence.

Do not skip a failed or incomplete gate. Continue useful preparation for later
gates in parallel only when it cannot contaminate or prejudge the open gate.

## Current execution state — 2026-08-23

The repository is private at `navneetprabhakar/ganesh-mini`. The current branch
is `main`; the last known pushed commit is
`dd9590f3fa715123e0437dc56c6805a332b0f225`.

Gate 1 native amd64 verifier validation is the active work item. A portable,
exact verifier archive is published in the private prerelease
`verifier-images-amd64-v1` and is pinned by SHA-256. GitHub Actions run
`32636958446` completed all scheduled work but ended in failure while preserving
an uploaded evidence artifact. Diagnose that evidence before any baseline or
training claim. Verify its top-level and nested seals independently, identify
the exact failing jobs, distinguish infrastructure defects from genuine task
directionality failures, fix demonstrated defects without weakening the frozen
contract, document the invalidation, and rerun the native workflow.

Do not claim Gate 1 passed until all native reference solutions pass, all known
bad solutions are rejected, global decision-set separation passes, and every
required evidence seal verifies. Historical ARM64 directionality evidence is
stale and is not release evidence.

After Gate 1 passes, continue through the gate order. Gate 0B v8 GCloud work is
still pending and requires a fresh explicit GCloud approval before any cloud
inspection or execution.

## Completion criteria

The goal is complete only when all of the following are true:

- exact Qwen base identity and serving contract are frozen and evidenced;
- all five languages have uncontaminated base, candidate, and comparison
  evaluation results under the same contract;
- `ganesh-mini-1.0` shows a defensible aggregate improvement over the exact
  base, with per-language regressions within frozen limits;
- the Ganesh v0.1 comparison is executed and clearly qualified where contracts
  differ;
- training data lineage, manifests, splits, configurations, checkpoints, logs,
  and decision evidence are preserved;
- merged F16 and Q8 artifacts have verified hashes and reproducible build
  metadata;
- both artifacts have measured laptop-runtime compatibility evidence for the
  stated 8–16 GB RAM target, with honest memory and performance limits;
- required artifacts and recovery data are verified in durable storage;
- no paid training VM remains running;
- the private GitHub repository is clean, pushed, documented, and points to the
  immutable release evidence; and
- the release decision contains no fabricated or reconstructed result.

Report progress by gate, executed evidence, current blocker or anomaly, and the
next concrete action. Do not substitute activity summaries for measured
completion.
