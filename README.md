# Ganesh Mini

Ganesh Mini is a verification-driven project to specialize
`Qwen/Qwen3.5-2B` for five programming-language families:

- Go
- Java
- JavaScript, with TypeScript as a separately measured compiler lane
- Python
- Rust

The planned trained model is `ganesh-mini-1.0`. The release target is a merged
reference checkpoint plus laptop-oriented GGUF F16 and Q8 artifacts. Q8 is
targeted at an 8 GB RAM machine and F16 at a 16 GB RAM machine, both at a
bounded 8,192-token runtime context. The upstream 262k context claim is not a
laptop acceptance criterion.

## Current status

Planning and local qualification are complete. The exact Qwen checkpoint and
authorized Ganesh v0.1 seed are downloaded/imported and hash-verified. Apple
BF16 inference, LoRA round-trip, and F16/Q8 GGUF runtime smokes pass. Production
CUDA/QLoRA qualification, frozen evaluation tasks, base baselines, and seed
training have not started. No GCloud resource has been used.

The canonical execution plan is
[`docs/plans/GANESH_MINI_1_0_PLAN_PASS2.md`](docs/plans/GANESH_MINI_1_0_PLAN_PASS2.md).
It supersedes the first-pass plan after a deliberate critical review. The
first pass is retained as design history.

## Design principles

- Measure the correctly served base before training.
- Treat JavaScript and TypeScript as one product family but two evaluation
  lanes.
- Train the languages jointly and balance by tokens, not row count.
- Use the user-authorized Ganesh v0.1 training corpus as the seed dataset.
  Preserve its lineage and hashes, convert it for Qwen without changing its
  semantics, and keep it disjoint from the new evaluation surfaces.
- Keep public benchmarks diagnostic; use a frozen private decision suite for
  the promotion decision.
- Compare `ganesh-mini-1.0` with both its Qwen base and Ganesh v0.1 on the same
  tasks and verifier contracts, while reporting quality and efficiency
  separately.
- A completed training job is not a successful model.

## Repository map

- `docs/plans/`: initial and reviewed execution plans.
- `docs/process/`: current state and approval boundaries.
- `docs/research/`: primary-source notes used by the plan.

Implementation directories will be added only as their gates open, so empty
scaffolding does not imply that data or training is ready.
