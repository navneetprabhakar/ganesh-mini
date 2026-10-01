# Gate 2 repair-delta V6 canonical-test replay plan — 2026-09-17

Status: prospective local contract; implementation and readiness next

Contract: `capability-stratified-v6-canonical-test-replay/v1`

## 1. Purpose and boundary

V5 is terminally sealed as `qualification-failed` at report seal
`f169894cc32557388ec7812180d1524502af1ae35c310e8f31f3c4177e5452e5`.
Its 60 ordered outcomes remain 29 admitted, 31 rejected, and 0 unresolved.
Nothing in V6 changes, retries, or relabels a V5 disposition.

The complete post-run audit found a single bounded mechanism across all 31
rejects: the independent-test interface was inconsistent with its validator
and canonical staging. Ten syntactically valid cross-cutting suites were
rejected by an over-broad regex, four Java role objects collided on a path the
controller should own, and 17 suites could not locate the implementation or
required an unavailable runner convention. No V5 reject demonstrated a bad
reference implementation.

V6 requalifies the complete 60-cell repair surface under a new prospective
test-author and staging contract. It carries candidate content uniformly and
reruns independent test authorship uniformly. It is not a selective replay of
only failed V5 cells.

A V6 pass qualifies the 60-cell repair corpus construction result only. It
does not authorize training, evaluation opening, publication, or release.

## 2. Immutable inputs

Before any V6 model call, seal and bind:

- the V5 plan and all addenda;
- the V5 ordered 60-candidate execution manifest;
- the V5 terminal inventory and qualification result;
- the 60 exact teacher candidate payloads and proofs;
- the 60 exact passing semantic-review outcomes, including their interruption
  carry lineage;
- the V2 generation-equivalence summary, admission report, and envelopes;
- runtime configuration, container digests, sandbox contract, and separation
  contract; and
- all V6 prompt, schema, adapter, validator, staging, retry, and readiness
  hashes.

V6 carries all 60 teacher candidates, proofs, and passing semantic outcomes
byte-for-byte. It carries zero V5 test-author output, executable result,
admission status, or terminal disposition into a V6 decision. Historical raw
test-author outputs may be used only in the offline readiness regression in
section 8 and never as V6 candidate tests.

Candidate order is the V5 canonical capability-major, lane-minor order. The
two V5 TypeScript replacement identities remain in their frozen cells. V6
generates no teacher candidate or teacher proof.

## 3. Independent test-author visibility

Run one fresh test-author call for every ordered candidate. The author sees
only:

- specification;
- embedded known-bad implementation;
- language lane;
- primary-capability name and generic definition;
- assigned cross-cutting dimension and its frozen generic definition;
- canonical candidate filename, canonical test filename, execution command,
  and exact permitted local module/import form; and
- the response contract below.

The author never sees the teacher candidate/reference, teacher proof, semantic
review, V5 tests or outcomes, verifier output, training stimulus/source,
evaluation content, or another candidate.

The prompt says explicitly that the cross-cutting suite must pass the visible
known-bad while testing only the assigned secondary dimension. It must not
assert the corrected primary result.

After test authorship, run one fresh blind delta-audit call for every candidate
because the newly attached tests change the candidate envelope hash. The delta
auditor sees the specification, embedded known-bad, candidate reference,
language, primary capability, and assigned dimension. It does not see tests,
teacher proof, semantic review, executable results, V5 outcomes, source data,
or evaluation content. Require exactly one independent capability-specific
semantic delta and no second independent fix under the existing sealed boolean
contract. There is no delta-audit correction call.

## 4. Response schema and controller-owned paths

The provider response contains exactly two named objects in this order:
`primary_discrimination` and `cross_cutting`. Each object contains only:

- `content`: non-empty complete test source; and
- `case_ids`: a non-empty string array, with at least two locally unique IDs
  for primary and at least one locally unique ID for cross-cutting.

The provider JSON schema uses no unsupported `uniqueItems`; duplicate-ID
enforcement remains local. The model does not choose a path.

The controller injects distinct logical role paths and canonical execution
paths deterministically. Injected-path hashes are recorded separately from raw
response hashes. The canonical lane contract is:

| Lane | Candidate | Test | Required local binding |
|---|---|---|---|
| Go | `solution.go` | `solution_test.go` | `package solution`; no relative source include |
| Java | `Solution.java` | `SolutionTest.java` | same default package; `SolutionTest.main` |
| JavaScript | `solution.js` | `solution.test.js` | `require('./solution.js')` only |
| TypeScript | `solution.ts` | `solution.test.ts` | relative module `./solution`; no Node typings |
| Python | `solution.py` | `test_solution.py` | import `solution`/`from solution`; no parent path |
| Rust | `solution.rs` | `solution_test.rs` | `#[path = "solution.rs"] mod solution;`; direct `rustc --test` |

Static validation rejects parent-relative imports, unexpected candidate module
names, dynamic environment/argv target selection, Cargo-only compile-time
macros, network/subprocess access, unavailable third-party dependencies, and
lane-incompatible entry points. These are structural findings, not semantic
adjudication.

## 5. Exact executable adjudication

Delete `_v5_cross_depends_on_primary` from decision authority. Syntax patterns
may produce diagnostics but never accept or reject a candidate.

After static validation and content-free global separation, execute each role
against the exact reference and embedded known-bad under final canonical
staging. Admission requires this matrix:

| Implementation | Primary suite | Cross-cutting suite |
|---|---|---|
| Reference | PASS | PASS |
| Known-bad | FAIL | PASS |

All four executions use pinned, network-disabled, resource-limited containers.
Preserve commands, images, digests, staged-file hashes, stdout, stderr, exit
codes, durations, timeouts, classifier outputs, and retry ledgers.

A reference assertion failure, known-bad primary pass, or known-bad cross fail
is a candidate-local terminal rejection. A compile/import/interface failure is
not reclassified as semantic. Infrastructure replay remains limited to one
byte-identical replay only when the frozen classifier labels an execution as
infrastructure.

## 6. Bounded structural reauthoring

V6 permits at most six fresh structural reauthor calls in total, each for a
different first-pass candidate and only when the first response fails local
response-schema or static lane-interface validation before any reference or
known-bad execution.

The reauthor sees the original section-3 projection plus only the exact local
contract violation. It still cannot see reference content, proof, semantic
evidence, executable output, or any V5 outcome. The original raw response,
failure, correction prompt, corrected response, and both hashes are preserved.

No reauthor is permitted after semantic or executable adjudication begins. No
candidate code, known-bad code, test content, witness, or verifier output may
be hand-edited. A seventh structural failure seals V6 failed.

## 7. Frozen gates and budgets

First-pass budgets:

- ordered teacher candidates: exactly 60 immutable carries;
- fresh test-author calls: exactly 60;
- structural reauthor calls: 0–6;
- fresh blind delta-audit calls: exactly one for every structurally valid final
  test-author result, with a maximum of 60 and no correction;
- teacher generation calls: 0;
- semantic-review calls: 0 after the exact carry-equivalence audit;
- executable candidate suites: exactly four per structurally valid candidate,
  plus at most one identical replay per classified infrastructure failure.

Before structural reauthoring is eligible, the raw first pass must have:

- all 60 test-author calls terminally accounted;
- zero unresolved model invocations after permitted identical transport replay;
- at least 54 structurally valid test pairs;
- at least 9 structurally valid pairs in every lane;
- at least 5 structurally valid pairs for every capability;
- at least 10 structurally valid pairs for every cross-cutting dimension;
- no more than six structural-only rejects; and
- zero visibility, lineage, source-collision, or evaluation-boundary failures.

If any threshold fails, V6 fails immediately and structural reauthoring is
forbidden. If they all pass, reauthor exactly the structurally rejected cells,
one call each, in frozen cohort order.

Final V6 passage requires:

- exactly 60/60 candidates admitted by the executable matrix;
- zero unresolved outcomes;
- zero source collisions or lineage failures;
- zero separation failures;
- zero evaluation artifacts read outside content-free separation; and
- V2 generation equivalence still passing for all 60 generation cells, for
  combined 120/120 capability/lane/type coverage.

There is no candidate reserve, teacher regeneration, test-semantic correction,
second reauthor, threshold waiver, or post-hoc selection. Any final executable
rejection seals V6 failed.

## 8. Readiness before the 60-call campaign

All readiness items must pass and be sealed before candidate test authorship:

1. Offline regression of all 60 V5 raw test-author responses through the V6
   adapter. This is diagnostic-only and creates no V6 test artifact. It must
   prove controller-owned paths eliminate Java path collisions, the ten former
   regex rejects are no longer syntax-adjudicated, and all observed forbidden
   JS/TS/Rust binding forms are explicitly detected.
2. Unit fixtures for exact objects/keys, minimum and duplicate case IDs,
   controller path injection, lane import rules, visibility, retry eligibility,
   ordering, hashes, and fail-closed terminal accounting.
3. Six-lane canonical-staging closure: one synthetic candidate per lane, two
   roles by two implementations, exactly 24 sandboxed suite executions, all
   matching the required PASS/FAIL matrix. Include negative fixtures for every
   V5 path/env/Cargo signature and the TypeScript strict-null pattern.
4. One content-free live provider schema-admission smoke proving the exact V6
   test-author response schema is accepted and locally validated. Revalidate
   the already provider-compatible delta-audit schema locally.
5. Six fresh training-only canaries, one per lane, under the final prompt and
   adapter. Require 6/6 structurally valid, canonical-compilable pairs and the
   exact executable matrix. A canary failure blocks the 60-call campaign.
6. A composite readiness report binding every input and implementation hash,
   recording zero evaluation reads and `status: passed`.

Readiness fixtures and canaries never enter training and do not count toward
qualification metrics.

## 9. Execution sequence

1. Seal this plan and its file SHA-256.
2. Build the exact V6 carry-equivalence and ordered-cohort manifests.
3. Implement the no-path response schema, controller path injection, lane
   interface validator, executable adjudicator, structural retry ledger, and
   terminal accounting.
4. Add focused tests and execute section-8 readiness in order.
5. If readiness passes, run exactly 60 fresh test-author calls.
6. Seal raw first-pass accounting and apply section-7 eligibility gates.
7. If eligible, run only the exact ordered structural reauthor set, at most six.
8. Run the fresh blind delta audit for every structurally valid final test pair.
9. Run content-free global separation and the exact executable matrix.
10. Seal admission, qualification, 120-cell coverage, and the result narrative.
11. Only a V6 pass returns the project to Gate 3/4 training-entry assessment.

## 10. Scope, ETA, and hard stops

Implementation, readiness, and the local V6 campaign are authorized under the
standing non-GCloud scope. No GCloud read, write, resource action, or billing
is authorized by this plan.

Estimated warm path after implementation is 1–3 hours: 20–45 minutes for
readiness and canaries, 20–60 minutes for 60 parallel test-author calls, and
20–60 minutes for bounded sandbox execution and sealing. This is an estimate,
not evidence.

Stop and seal V6 failed on readiness failure, first-pass threshold failure,
more than six structural rejects, any non-structural reauthor attempt, any
final executable rejection, unresolved exhaustion, ordering/accounting drift,
visibility or evaluation-boundary breach, source/lineage collision, or a
goal-alignment `DIVERGENCE` finding.
