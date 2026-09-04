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

Gates 0–2 are complete. The exact Qwen checkpoint, six-lane private evaluation
contract, 20/180 development baseline, and authorized Ganesh v0.1 seed are
sealed. The first Gate 3 pilot trained but regressed to 13/180; it is rejected,
not a release candidate. Gate 3 v2 uses one unique seed epoch, explicit five-
family token weighting, conservative attention-only LoRA, and robust optimizer-
level anomaly detection. Its `1e-5` candidate completed all 461,235 input
tokens with improved held-out loss and exact adapter reload equivalence. The
canary then stopped on a missing verifier-image orchestration defect before an
executable score existed; `3e-5`, LR selection, and the full development run
remain incomplete. The defect is repaired. A sealed continuation now imports
the completed `1e-5` adapter without retraining it, loads and audits all six
verifier images first, trains only `3e-5`, evaluates both canaries, and performs
the frozen full-development adjudication. Automatic VM restart is explicitly
disabled. The exact VM service account's bucket read/write IAM is verified
before any compute or temporary network resource is created. Another GCloud
campaign requires fresh explicit approval.

No `ganesh-mini-1.0` weights have been released. Gates 4–8 remain evidence-
dependent: main SFT, optional correction, untouched decision evaluation against
the exact Qwen base and a fresh Ganesh v0.1 run, merge, F16/Q8 export, laptop
certification, release adjudication, and Hugging Face publication. Release
tooling exists and fails closed, but none of those pending results are claimed
as executed evidence.

The canonical execution plan is
[`docs/plans/GANESH_MINI_1_0_PLAN_PASS2.md`](docs/plans/GANESH_MINI_1_0_PLAN_PASS2.md).
It supersedes the first-pass plan after a deliberate critical review. The
first pass is retained as design history.

The current operational continuation and recovery guide is
[`docs/process/HANDOFF.md`](docs/process/HANDOFF.md). Its status snapshot is
time-stamped; live expansion counts must always be read from the production
state and verified against the corpus hash before acting.

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
