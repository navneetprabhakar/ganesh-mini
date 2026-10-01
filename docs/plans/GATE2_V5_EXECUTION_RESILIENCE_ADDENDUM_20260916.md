# Gate 2 V5 execution-resilience addendum — 2026-09-16

Status: sealed execution-resilience correction; execution remains ineligible
unless the V5 controller validates the exact carry and attempt manifests below

Applies to: `capability-stratified-v5-interface-replay/v1`

## 1. Immutable controlling inputs

This addendum does not create a new cohort or reinterpret any completed V4 or
V5 result. It binds the following existing contracts and artifacts:

- V5 base plan SHA-256:
  `132501466e58e88b6aaebc412aac37e561b103ae8df8f50a9ac43d3aab7cc04b`;
- source-feasibility addendum SHA-256:
  `01a8415fa9122f163aa58f5cf6578bb1ff2502346cb197a11af14b373d922da3`;
- budget-clarification addendum SHA-256:
  `1933b409b656ab90cf4a82e44b0b2b7dc29d4701d3a162add64db179319a4899`;
- ordered cohort manifest seal:
  `ced9dbe122274130af132c4b6e0c845cd52225280367b654140d068690c72391`;
- execution-cohort manifest seal:
  `138c0dff1263278cae17bdab4c497f00fabec336f5ffded26daf0a30fae51e9d`;
- semantic-equivalence manifest seal:
  `e3e868f32ac86821e946b619f3e140c62d397c80f2af259395ce203ebc721e30`;
- composite-readiness report seal:
  `2dab989164473a5b249be0c2b21bd30beb453b927c46aa735d5f7afd7c13d796`;
- Codex configuration canonical SHA-256:
  `ee449bb3eee569aa0805bd0791bc1c6a0c1c5e06289af588e5cd99c7dd7a2838`;
  and
- V5 interruption-accounting report seal:
  `f939b1380e4f4f3e8aa0cf7bb0bded52b18ec099c4aeb9d1df12f95d8c2360e6`.

The ordered first pass remains exactly 60 candidates: 58 immutable V4 teacher
carries and two already generated fresh TypeScript primaries. The 59 reserve
source bindings, first-pass-only Java graph/tree cell, maximum five generated
reserves, terminal ceiling 65, and new-teacher ceiling seven remain unchanged.
No teacher output may be regenerated or edited because of an orchestration
interruption.

The original composite-readiness report and execution-cohort manifest remain
immutable construction evidence because the two fresh teacher results bind
them. They are not regenerated. Resilience mode narrowly supersedes only the
composite report's live file-hash check for
`scripts/data/run_repair_delta_two_phase.py` and
`scripts/data/run_repair_delta_evidence.py`. The V2 attempt manifest must bind
both old and current hashes for those two paths, require every other path in
the composite runtime inventory to remain byte-identical, and additionally
bind the interruption accountant and resilience-manifest validator. Drift in
any other readiness path is a hard stop.

## 2. Evidence-based classification of the interrupted attempt

`primary-two-phase-v1` did not emit a campaign inventory, pre-separation
candidate artifact, post-test cohort, separation report, executable result,
admission result, or qualification result. It therefore has zero candidate
dispositions and no defensible acceptance, rejection, unresolved, coverage,
or threshold metric.

The cause of interruption is `unknown-not-evidenced`. Absence of an artifact
is not evidence of model failure, stage failure, timeout, rejection, or an
unresolved candidate. Logs, process observations, elapsed time, or expected
scheduler behavior may not be used to reconstruct missing metrics.

The only committed new work is three sealed semantic-review stage artifacts.
The deterministic interruption-accounting report verified their artifact and
run seals, exact V5 input and prompt hashes, current candidate and assignment
projections, Codex configuration, CLI identity, successful completion event,
zero tool use, and evaluation-read count zero:

| Candidate | File SHA-256 | Stage artifact seal | Run evidence seal |
|---|---|---|---|
| `cap-v4-associative_aggregation-java-repair-primary` | `b82fe8b9ba3b24becc89ddada7bc6a45d3c61a659d0ef60dd74f284a2e00c327` | `b78b868c564dcab15080aa22cf74f8624b111fa0fecba937bb0137f9d7a86ff6` | `ba25eaf8cf06e56b289345bd446864ff43e771aea4e2ec882a62f5b26110e669` |
| `cap-v4-associative_aggregation-javascript-repair-primary` | `138fbd509d34cca9786a4a558cfafdb9504b367de1640ba22ddd301aa866cbf7` | `9cff9af13bee32a60145e1b604f4e6fd907f03f66bc75353b0495f904746bb21` | `e304541247ce5b705598cfa030360e5b4a0a3f678ed533ae6251daecc54b2659` |
| `cap-v4-associative_aggregation-rust-repair-primary` | `71da67597ee5af749e13c4be8f2ce71c19601638bb90f6867ce247ceee64f43e` | `2aa048a1d038b81ea5192f5ae90e41afbedf5f4e918fdedd9407c38da5c5768a` | `90c7c6349ccd2257b9586ec32b097fea0d97325fd9b871188f21e78c8c4f229b` |

All three belong to the frozen set of 23 required new reviews. Their six
semantic booleans are true, but that is only a completed semantic-stage result;
it is not a candidate admission or qualification outcome. Twenty required new
semantic reviews have no committed artifact.

## 3. Permitted carry of the three completed reviews

The three stage artifacts may be consumed exactly once as completed V5
semantic calls. They are not rerun. Reuse is permitted only when a deterministic
carry validator proves all of the following before dispatch:

1. file, artifact, and embedded run-evidence seals match section 2;
2. contract version is V5 and stage is `semantic_review`;
3. candidate ID is in the sealed 23-review-required partition;
4. semantic projection, full prompt, input SHA-256, response schema, Codex
   configuration, CLI identity, and evaluation-read marker are unchanged;
5. the run returned zero, did not time out, had no parse error or disallowed
   tool item, and contains a completed turn; and
6. conversion to semantic evidence uses the unchanged V5 semantic-evidence
   builder and remains bound to the unchanged pre-test candidate.

Any mismatch fails closed. It does not authorize a replacement review. A
copied file without an explicit carry manifest is not sufficient. The carry
manifest must bind this addendum, the interruption-accounting report, all three
source artifacts, and the target attempt version.

The 37 V4-equivalent semantic reviews remain governed by the existing sealed
semantic-equivalence manifest. They are not part of the three interrupted-run
artifacts. The resulting semantic accounting is exactly 37 prior equivalents,
three completed V5 calls carried from the interrupted attempt, and 20 remaining
new V5 calls: 60 reviews total, with exactly 23 new V5 calls across attempts.

## 4. Prospective checkpoint and resume contract

The next attempt uses a new immutable attempt directory; it must not overwrite
or append ambiguously to `primary-two-phase-v1`. Before model dispatch it emits
a sealed attempt manifest binding all hashes in section 1, this addendum's
eventual file hash, the three-artifact carry manifest, tool identities, output
root, and ordered 60 candidate IDs.

Every model stage is a content-addressed transaction:

1. derive the exact stage input and output path;
2. write a sealed `running` intent containing attempt ID, candidate, stage,
   input hash, config hash, and start timestamp;
3. invoke one isolated stage call;
4. validate the response and complete run evidence;
5. write the final artifact to a same-filesystem temporary path, flush and
   atomically rename it; and
6. append a sealed ledger event referencing the final artifact hash.

Only the atomically published final artifact is completed evidence. A running
intent, temporary file, provider thread, stdout fragment, or response without a
valid final seal is `uncommitted`. On restart, an exact completed artifact is
reused; an invalid final artifact is a hard stop; an uncommitted stage may be
called again but both physical attempts remain disclosed in the ledger. Such a
retry is interruption recovery, not a semantic correction call, and it cannot
change the input.

After the startup manifest gate, pre-separation work retains the existing
candidate-local transaction order: interface preflight, semantic review when
not carried, test authorship, and delta audit. Different candidates may
advance through those stages concurrently under the frozen lane scheduler; a
global semantic or test-author barrier is not required. Every completed stage
must still be published atomically before that candidate advances, and exactly
the three carried reviews suppress their corresponding new semantic calls.

The mandatory global barrier remains immediately before separation. At that
point the controller must seal accounting for all ordered 60 candidates,
including candidate-local terminal semantic or tooling outcomes, prove there
is no running or uncommitted stage, freeze the complete surviving post-test
cohort, and only then run one global content-free separation. Phase two then
executes the four-suite matrix under the frozen scheduler, performs immediate
final admission, and emits exact ordered terminal accounting. Candidate-local
terminal outcomes are never silently skipped.

## 5. Interruption ledger and terminal accounting

The ledger is append-only and hash-chained. Each event includes attempt ID,
monotonic sequence, prior-event SHA-256, candidate ordinal and ID, cell, stage,
logical-call ordinal, physical-attempt ordinal, exact input SHA-256, state,
artifact SHA-256 when complete, classification, and evaluation-read count.
Allowed states are `intent`, `completed`, `terminal-rejected`, `unresolved`,
and `uncommitted-at-interruption`.

An interruption snapshot must inventory every expected artifact path and
partition work without overlap into:

- completed and reusable;
- completed terminal candidate outcome;
- unresolved under an already exhausted identical infrastructure replay;
- uncommitted and eligible for exact-input recovery; or
- not started.

The snapshot never fills gaps from memory or logs. It reports stage counts, not
qualification rates. Qualification metrics become valid only after the sealed
ordered terminal artifact contains all 60 primary IDs in canonical order and
the admission output partitions the same IDs across admitted, rejected, and
unresolved exactly once.

## 6. Hard stops and authorization boundary

Stop before any new model call if the three-artifact carry does not validate,
the ordered cohort or any controlling hash changes, any logical semantic call
would be duplicated, an invalid final artifact exists, or the ledger cannot
account for a physical attempt. Do not delete the interrupted directory.

The runtime interface for this correction is explicit. V5 startup must require
`--v5-resilience-addendum`, `--v5-semantic-interruption-carry`, and
`--v5-attempt-manifest`; validate all three before constructing any model-stage
adapter; require the attempt manifest's output root to equal the requested new
output root; merge exactly the three validated semantic-evidence objects into
the existing 37-review carry map; and remove exactly those three IDs from the
23-review dispatch set. No implicit scan of the old attempt directory is an
acceptable substitute. A controller without this interface is not compliant
with this addendum and must stop before a model call.

This addendum changes only execution durability and accounting. It
does not weaken any semantic, test, executable, separation, distribution,
reserve, budget, training, evaluation, GCloud, publication, or release gate.
It authorizes no model call until the exact manifest validator is integrated
and covered by readiness tests through the actual production path.
