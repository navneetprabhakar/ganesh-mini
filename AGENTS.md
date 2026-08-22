# Ganesh Mini Operating Instructions

## Objective

Build `ganesh-mini-1.0`, a laptop-runnable Qwen3.5 2B coding model that shows a
defensible improvement over its correctly served upstream checkpoint across
Go, Java, JavaScript/TypeScript, Python, and Rust.

## Required reading before changes

1. `docs/plans/GANESH_MINI_1_0_PLAN_PASS2.md`
2. `docs/process/DECISIONS.md`
3. `docs/process/PROJECT_STATE.md`
4. `docs/research/PRIMARY_SOURCES.md`
5. Current repository status and the relevant implementation paths

State the current gate, intended files, assumptions, and any hard stop before
implementation.

## Non-negotiable rules

- Measurement precedes training.
- Pin the exact upstream model revision and serving contract before baseline
  generation.
- In-scope local work, downloads, datasets, model training, long-running jobs,
  non-GCloud compute, benchmarking, artifact publication, and repository
  operations are user-approved. Do not stop merely to request authorization
  for these actions.
- Any GCloud usage remains a hard approval boundary. Do not inspect, create,
  start, stop, mutate, or bill GCloud resources without explicit user
  authorization for that usage.
- Ganesh v0.1 training data is explicitly authorized by the user for
  `ganesh-mini-1.0` and is the approved seed corpus. Do not reopen its ownership
  or provenance decision. Preserve source commit, file hashes, record IDs, and
  lineage; perform only compatibility, integrity, evaluation-separation, and
  current-toolchain execution checks.
- Public benchmark tasks, private development tasks, and private decision
  tasks never enter training.
- Preserve prompts, rendered prompt hashes, raw outputs, extracted code,
  verifier results, runtime parameters, model identity, and artifact hashes
  for every result used in a decision.
- Execute generated code only in resource-limited, network-disabled sandboxes.
- Do not report fabricated or reconstructed metrics as executed evidence.
- Publish only artifacts that pass the frozen release gates; publication is
  already authorized but failed or incomplete evidence still blocks release.

## Gate order

0. Upstream identity, architecture, toolchain, and text-only serving smoke.
1. Frozen evaluation contract and base baselines.
2. Authorized seed import, compatibility, and expansion admission.
3. Bounded multilingual pilot.
4. Main joint verified SFT.
5. Failure-targeted correction pass, if justified.
6. Untouched evaluation and Ganesh v0.1 comparison.
7. Merge, quantize, and laptop runtime certification.
8. Release decision.

Stop only at GCloud usage, a verified goal-divergence finding, a destructive
action whose target is ambiguous, or a genuine technical blocker. Training,
non-GCloud compute, decision-set opening under the frozen plan, and publication
do not require another authorization request.

The active 30-minute goal-alignment heartbeat performs an independent read-only
audit. If it reports `DIVERGENCE`, pause further mutations, training, downloads,
and compute, preserve current evidence, and wait for Navneet Prabhakar.
