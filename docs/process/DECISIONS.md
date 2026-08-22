# Decisions

## 2026-08-22 — Ganesh v0.1 training data authorized as seed corpus

Navneet Prabhakar explicitly authorized reuse of the Ganesh v0.1 training data
for `ganesh-mini-1.0`, stating that it is his data, already cleaned for the same
purpose, with only the backbone changing.

Consequences:

- Ownership, source-license suitability, and historical teacher provenance are
  accepted by user authority for this project and are not re-admission gates.
- The data will be imported from the committed Ganesh repository state with
  source paths, source commit, byte hashes, record IDs, and split lineage
  preserved.
- Mechanical checks remain mandatory: Qwen schema rendering, duplicate IDs,
  parseability, current compiler/runtime execution, and disjointness from the
  newly frozen Ganesh Mini development and decision sets.
- Re-execution failures are quality signals to quarantine or repair; they do
  not reopen the ownership decision.
- Additional data may be added later, but the v0.1 corpus is the first pilot
  and baseline training source.

Inspected committed Ganesh source revision:
`9552867c7641a5f11acadb84d19bfb8d723ab0ae`.

Seed inventory observed at that revision:

| Lane | Training | Validation | Source |
|---|---:|---:|---|
| Python | 468 | 30 | `data/train/multisource_python_v2/` |
| Go | 163 | 4 | `data/train/multiling_v1/go/` |
| Java | 146 | 4 | `data/train/multiling_v1/java/` |
| JavaScript | 222 | 4 | `data/train/multiling_v1/js/` |
| TypeScript | 218 | 4 | `data/train/multiling_v1/ts/` |
| Rust | 182 | 4 | `data/train/cuda_lora_v5/rust/` |
| **Total** | **1,399** | **50** | |

The Rust source differs from the `multiling_v1` paths because that committed
directory has no Rust lane. Its use is authorized, but its schema must be
normalized into the same Ganesh Mini contract.

## 2026-08-22 — Broad in-scope authorization; GCloud remains gated

Navneet Prabhakar authorized all actions required to complete the Ganesh Mini
objective without further approval requests, except GCloud usage.

Consequences:

- Local setup, downloads, dataset processing, long-running jobs, training,
  non-GCloud compute, benchmarking, repository operations, decision-set use
  under the frozen plan, and artifact publication are authorized.
- GCloud inspection, mutation, execution, and billing remain prohibited until
  explicitly authorized.
- Technical gates still apply. Authorization does not turn missing evaluation,
  invalid evidence, failed tests, or an unqualified model into a pass.

## 2026-08-22 — Recurring independent goal-alignment audit

A Codex heartbeat named `Audit Ganesh Mini goal alignment` runs every 30
minutes. Each run must spawn an independent read-only review subagent to compare
active work and repository changes with the original Ganesh Mini objective and
canonical plan.

If the reviewer reports `DIVERGENCE`, the primary task pauses further
mutations, training, downloads, and compute and waits for Navneet Prabhakar.
