# Ganesh Mini

Ganesh Mini is a verification-driven project to specialize
`Qwen/Qwen3.5-2B` for five programming-language families:

- Go
- Java
- JavaScript, with TypeScript as a separately measured compiler lane
- Python
- Rust

The experimental checkpoint is named `ganesh-mini-1.0`. A merged reference
checkpoint and GGUF F16 and Q8 artifacts were exported, but the intended 8 GB
Q8 and 16 GB F16 laptop profiles were not certified. The measured public
serving contract uses an 8,192-token context; the upstream 262k context claim
is not a laptop acceptance result.

## Current status

This project iteration is closed. Its selected bounded pilot did not pass the
frozen Gate 3 private-development quality criteria; Gates 4–7 were not run,
the private decision set remains unopened, and Gate 8 release eligibility is
**NO-GO**. The independent Gate 0B raw-report recovery gap also remains open.
Neither a public checkpoint upload nor a public benchmark changes those gate
decisions.

At the user's direction, the experimental checkpoint, adapter, and GGUF
exports are nevertheless available under
[`Executespec/ganesh-mini-1.0`](https://huggingface.co/Executespec/ganesh-mini-1.0).
The model card contains only public benchmark assessment, with no private
evaluation scores or improvement claim. On the full pinned, locally executed
MultiPL-E HumanEval diagnostic, Ganesh Mini passed **338/952** tasks versus
**339/952** for correctly served Qwen upstream (8 paired wins, 9 losses).
This is not an official leaderboard result or laptop-runtime certification.
The public [method and sealed report](https://huggingface.co/Executespec/ganesh-mini-1.0/tree/main/benchmarks/public-multipl-e-full)
document the exact diagnostic. Raw benchmark outputs remain local.

The canonical execution plan is
[`docs/plans/GANESH_MINI_1_0_PLAN_PASS2.md`](docs/plans/GANESH_MINI_1_0_PLAN_PASS2.md).
It supersedes the first-pass plan after a deliberate critical review. The
first pass is retained as design history.

The historical execution and recovery record is
[`docs/process/HANDOFF.md`](docs/process/HANDOFF.md). The final disposition is
documented in [`docs/process/PROJECT_STATE.md`](docs/process/PROJECT_STATE.md).

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

Generated models and raw evidence are not stored in Git. Public reports are
published alongside the experimental checkpoint; internal gate evidence is
retained separately.
