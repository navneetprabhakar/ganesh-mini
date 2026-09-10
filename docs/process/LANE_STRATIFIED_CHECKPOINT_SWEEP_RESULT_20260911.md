# Lane-stratified checkpoint sweep result

Status: terminal diagnostic; do not promote

Date: 2026-09-11 IST

## Outcome

The five earlier checkpoints from the completed Gate 4 v3 lane-stratified
probe were evaluated serially on the same frozen 30-task private development
screen. The measured pass curve was:

| Checkpoint tokens | Passes | Net versus base |
|---:|---:|---:|
| 78,487 | 5/30 | 0 |
| 156,090 | 5/30 | 0 |
| 239,231 | 3/30 | -2 |
| 312,423 | 6/30 | +1 |
| 389,093 | 5/30 | 0 |
| 466,614 final | 6/30 | +1 |

The upstream checkpoint scored 5/30. No earlier checkpoint exceeded the final
checkpoint, and no checkpoint passed the frozen continuation rule of net +2,
at least two improved product families, and zero lane regression. The two
6/30 checkpoints share the same lane profile: Go 0, Java 2, JavaScript 1,
TypeScript 1, Python 1, and Rust 1. TypeScript therefore remains below its
upstream 2/5 result.

Decision: `do-not-promote`. Do not open the full 180-task development surface,
train further from any v3 checkpoint, merge, quantize, or publish this model.
The sweep had diagnostic authority only.

## Interpretation

Earlier stopping is not the missing mechanism. Performance is non-monotonic,
but the best intermediate checkpoint only ties the final result. At 389,093
tokens, Go/Java/Python/Rust improve over base while the combined JavaScript and
TypeScript family falls from 3/10 to 0/10, leaving total passes unchanged.
This is continued cross-lane transfer interference, not simple end-of-epoch
overtraining.

The v3 recipe should not be scaled, rebalanced, or checkpoint-selected. The
sealed task-level trajectory audit confirms that 21/30 tasks fail at every
measured point, one passes everywhere, and only eight change status. Five of
those eight are the same `collapse-runs` archetype. Late training exchanges a
single Go pass for JavaScript and TypeScript passes and back again. This is
neither broad capability acquisition nor a stable early-stopping opportunity.

The next mechanism should preserve the exact six-lane batches but measure and
control gradient direction, not merely gradient mass. The leading bounded
design is a LoRA-only per-lane gradient-conflict audit followed by deterministic
gradient surgery only if the audit confirms negative pairwise interference.
If conflict is not confirmed, retire optimizer-only intervention and return to
corpus/task-diversity work. Do not train six full specialists or attempt adapter
merging before this cheaper causal check.

The resulting local-only mechanism plan is sealed at
`4e04c8029e42605d7c5aba913e97644a952e2c28bfc1140d278c7c76a936d73d`.
It grants no GCloud or promotion authority.

## Evidence and recovery

- execution proposal:
  `7c54481ab57c5538c0d779f6dbb9a51aeb78183684e38185e26aee400bb9867d`
- sweep manifest:
  `4c5c8b31d7dbeea1de913c3869fc901d8095036d2251700bf606aa9e5b495f37`
- checkpoint-sweep report:
  `55fb67ff6b1a438c0f14c617ede45f3ffdf0ac5a32694cac4afd5b73bc32742f`
- campaign result:
  `15041b9000812305fab0573cd72b16385bf2aa67efbb67226125f2b84bc20ddc`
- result summary:
  `1b8968595287d979e62cd2e0d29008c12a5559c62ccdfb61d4d44c46c2297bf0`
- task-level trajectory audit:
  `15629f7407727fb9477eb6da892d709f174589575225e807ca14ec88f64ce9cc`

The guest completed model work with startup exit code 0, but its shell
finalizer remained active after the campaign result was written. The rolling
GCS checkpoint had 680 objects and missed one late verifier file because it
captured a live directory. Under approved rescue proposal
`896b6115b51876a32abea65141b0a2872f05f5930f4b693684b85be938f501aa`,
temporary IAP-only SSH recovered the stable terminal directory.

The rescue prefix contains 332 objects/4,050,250 bytes. All 331 files listed
by `runtime-files.sha256` independently verified. The previously absent
`tokens-000000389093` TypeScript clamp-window verifier record is present at
generation `1789065599418864`. A fresh local summary replay produced the exact
report seal above.

The phase ledger is sealed and contains all eight phases, but retains
`status: running`; the separately sealed campaign result is
`complete-diagnostic`. This is a finalizer/bookkeeping defect and is recorded,
not silently rewritten. The historical startup source is generation-bound and
therefore remains byte-identical. Any new controller must replace the two
process-substitution `tee` drains with explicitly owned FIFOs plus a bounded
drain timeout before it can be admitted.

A compact control archive was uploaded and independently round-tripped at
`control.tar.gz#1789066231307402`; its SHA-256 is
`656dcc168aa86ec98940543fc7f61b73f5a2b52ea7461a837d08fb95785c50ff`.
The sealed result summary and teardown receipt were also round-tripped at
generations `1789066237742649` and `1789066241475254` respectively.

## Teardown and billing

The temporary firewall, exact VM, auto-delete disk, subnet, and network were
deleted. Two provider checks confirmed all five exact resources absent. Ganesh
compute billing is closed; only GCS artifacts remain for this attempt.

Project-wide GCS-only billing is still false because the unrelated detached
200 GiB balanced disk `laxmi-wmv2-training-01` remains in `us-central1-a`.
It was outside this proposal and was not modified. Estimated sweep compute plus
boot-disk cost is approximately `$1.06`, below the sealed `$1.762043024`
provider upper bound and `$2.25` absolute ceiling.
