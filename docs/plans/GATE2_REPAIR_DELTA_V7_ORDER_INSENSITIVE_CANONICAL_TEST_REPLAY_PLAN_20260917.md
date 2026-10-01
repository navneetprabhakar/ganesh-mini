# Gate 2 repair-delta V7 order-insensitive canonical-test replay plan — 2026-09-17

Status: prospective local contract; implementation and readiness next

Contract: `capability-stratified-v7-order-insensitive-canonical-test-replay/v1`

## 1. Purpose and boundary

V6 is terminally stopped at pre-campaign readiness. Its content-free live
provider smoke returned the exact two required role objects, but returned them
in JSON member order `cross_cutting`, then `primary_discrimination`. The V6
local validator required the opposite serialized member order even though JSON
object member order is semantically irrelevant and the provider schema cannot
guarantee it. That made the V6 readiness condition impossible to establish.

The V6 smoke reached the provider and preserved its raw result at:

- path:
  `measurement/gate2/capability-stratified-v6-canonical-test-replay/readiness-v1/live-schema-runs/v6-live-schema-smoke.test_author.json`;
- file SHA-256:
  `24a0749d8de8d16907c2fb7814169ef64048d76d03b3d248a8cdf92d8e9d305e`;
- artifact seal:
  `2582bfa6b9e1dd98ec7994e31ab129ee4b400fb2947bc1facfc85394b5f54730`;
- response-schema SHA-256:
  `7faee5a48a1750563d1c47aaea77a488a97943bcba1bf1fac489274343a52822`;
  and
- run-evidence seal:
  `63da77817e6be490427d088c54c37a0863f6d3b73b2712ce1fa45f6d80d00046`.

V6 made zero candidate test-author calls, zero candidate delta-audit calls,
zero structural reauthor calls, and zero candidate executable decisions. It
produced no V6 test, admission, qualification, or candidate disposition that
V7 may carry. The V6 live-smoke response is diagnostic evidence only and is
not a V7 readiness pass or candidate artifact.

V7 corrects only that impossible serialized-key-order requirement. It keeps
the exact two-key set and makes the controller process the roles in one fixed
canonical order independent of provider serialization. Every other V6
visibility, authorship, staging, executable, retry, threshold, separation,
budget, and hard-stop rule remains unchanged.

A V7 pass qualifies the 60-cell repair corpus construction result only. It
does not authorize training, evaluation opening, publication, or release.

## 2. Immutable inputs and uniform V5 carry

Before any V7 model call, seal and bind:

- this V7 plan and its file SHA-256;
- the V6 plan at SHA-256
  `4fe6a1374c01a0a682bf256c91a141b36b26680bdb5279049070f4f143418ec1`;
- the terminal V6 readiness no-go report and its seal;
- the V6 live-smoke artifact and hashes listed in section 1;
- the V5 plan and all addenda;
- the V5 ordered 60-candidate execution manifest;
- the V5 terminal inventory and qualification result;
- the 60 exact V5 teacher candidate payloads and proofs;
- the 60 exact passing V5 semantic-review outcomes, including their
  interruption-carry lineage;
- the V2 generation-equivalence summary, admission report, and envelopes;
- runtime configuration, container digests, sandbox contract, and separation
  contract; and
- every V7 prompt, schema, adapter, validator, staging, retry, and readiness
  hash.

V7 retains all 60 V5 teacher candidates, proofs, and passing semantic outcomes
uniformly and byte-for-byte. It must independently reconstruct and seal this
carry from the V5 sources. It may verify equality to the sealed V6 carry
manifest, whose file SHA-256 is
`9023396c74567921a3dcdec3a05e2a1b5aea2cd437b63e7f4d5927cea04f362b`
and manifest seal is
`f95270299363fe003e0f8b747f60071eb813d36b09c9c132198588625a2be8af`,
but V6 is not the source of candidate or semantic content.

V7 carries zero V5 or V6 test-author output, executable result, admission
status, qualification status, or terminal disposition into a V7 decision.
Historical raw test-author outputs may be used only in offline readiness
regression and never as V7 candidate tests. The V6 live-smoke output may be
used only as the regression fixture proving member-order insensitivity.

Candidate order is the V5 canonical capability-major, lane-minor order. The
two V5 TypeScript replacement identities remain in their frozen cells. V7
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
review, V5 or V6 tests or outcomes, verifier output, training stimulus/source,
evaluation content, or another candidate.

The prompt says explicitly that the cross-cutting suite must pass the visible
known-bad while testing only the assigned secondary dimension. It must not
assert the corrected primary result.

After test authorship, run one fresh blind delta-audit call for every candidate
because the newly attached tests change the candidate envelope hash. The delta
auditor sees the specification, embedded known-bad, candidate reference,
language, primary capability, and assigned dimension. It does not see tests,
teacher proof, semantic review, executable results, V5 or V6 outcomes, source
data, or evaluation content. Require exactly one independent
capability-specific semantic delta and no second independent fix under the
existing sealed boolean contract. There is no delta-audit correction call.

## 4. Response schema and canonical controller order

The provider response is one JSON object whose member order is ignored. Its
key set must equal exactly:

`{"primary_discrimination", "cross_cutting"}`.

Missing keys, additional keys, duplicate serialized keys, or a non-object
response fail local validation. Each named object contains exactly:

- `content`: non-empty complete test source; and
- `case_ids`: a non-empty string array, with at least two locally unique IDs
  for primary and at least one locally unique ID for cross-cutting.

The provider JSON schema uses no unsupported `uniqueItems`; duplicate-ID and
exact-key enforcement remain local. The model does not choose a path.

After exact-key validation, the controller ignores source serialization order
and processes roles exactly once in this immutable canonical sequence:

1. `primary_discrimination`
2. `cross_cutting`

This sequence controls path injection, static validation, hashing, staging,
execution, ledger emission, terminal accounting, and any structural reauthor
diagnostic. Raw response bytes and their hash are preserved separately, so
normalizing role processing does not rewrite provider evidence.

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

Syntax patterns may produce diagnostics but never accept or reject a candidate
on semantic grounds. In particular,
`_v5_cross_depends_on_primary` has no decision authority.

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

V7 permits at most six fresh structural reauthor calls in total, each for a
different first-pass candidate and only when the first response fails local
response-schema or static lane-interface validation before any reference or
known-bad execution.

The reauthor sees the original section-3 projection plus only the exact local
contract violation. It still cannot see reference content, proof, semantic
evidence, executable output, or any V5 or V6 outcome. The original raw
response, failure, correction prompt, corrected response, and both hashes are
preserved.

No reauthor is permitted after semantic or executable adjudication begins. No
candidate code, known-bad code, test content, witness, or verifier output may
be hand-edited. A seventh structural failure seals V7 failed.

## 7. Frozen gates and budgets

First-pass budgets:

- ordered teacher candidates: exactly 60 immutable V5 carries;
- fresh V7 test-author calls: exactly 60;
- structural reauthor calls: 0–6;
- fresh blind delta-audit calls: exactly one for every structurally valid final
  test-author result, with a maximum of 60 and no correction;
- teacher generation calls: 0;
- semantic-review calls: 0 after the exact carry-equivalence audit;
- V5/V6 test-author or outcome carries: 0; and
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

If any threshold fails, V7 fails immediately and structural reauthoring is
forbidden. If they all pass, reauthor exactly the structurally rejected cells,
one call each, in frozen cohort order.

Final V7 passage requires:

- exactly 60/60 candidates admitted by the executable matrix;
- zero unresolved outcomes;
- zero source collisions or lineage failures;
- zero separation failures;
- zero evaluation artifacts read outside content-free separation; and
- V2 generation equivalence still passing for all 60 generation cells, for
  combined 120/120 capability/lane/type coverage.

There is no candidate reserve, teacher regeneration, test-semantic correction,
second reauthor, threshold waiver, or post-hoc selection. Any final executable
rejection seals V7 failed.

## 8. Readiness before the 60-call campaign

All readiness items must pass and be sealed before candidate test authorship:

1. Offline regression of all 60 V5 raw test-author responses through the V7
   adapter. This is diagnostic-only and creates no V7 test artifact. It must
   prove controller-owned paths eliminate Java path collisions, the ten former
   regex rejects are no longer syntax-adjudicated, and all observed forbidden
   JS/TS/Rust binding forms are explicitly detected.
2. A specific regression using the sealed V6 live-smoke response must prove
   that reversed JSON member order passes exact-key validation and produces the
   canonical controller sequence `primary_discrimination`, then
   `cross_cutting`. Negative fixtures must reject missing, additional, and
   duplicate serialized keys.
3. Unit fixtures for exact objects/keys, minimum and duplicate case IDs,
   controller path injection, lane import rules, visibility, retry eligibility,
   canonical role processing, hashes, and fail-closed terminal accounting.
4. Six-lane canonical-staging closure: one synthetic candidate per lane, two
   roles by two implementations, exactly 24 sandboxed suite executions, all
   matching the required PASS/FAIL matrix. Include negative fixtures for every
   V5 path/env/Cargo signature and the TypeScript strict-null pattern.
5. One fresh content-free live provider schema-admission smoke proving the
   exact V7 test-author response schema is accepted and locally validated under
   order-insensitive exact-key handling. Revalidate the already
   provider-compatible delta-audit schema locally. The V6 smoke cannot satisfy
   this item.
6. Six fresh training-only canaries, one per lane, under the final prompt and
   adapter. Require 6/6 structurally valid, canonical-compilable pairs and the
   exact executable matrix. A canary failure blocks the 60-call campaign.
7. A composite readiness report binding every input and implementation hash,
   the V6 no-go seal, the V7 carry and cohort seals, zero evaluation reads, and
   `status: passed`.

Readiness fixtures and canaries never enter training and do not count toward
qualification metrics.

## 9. Execution sequence

1. Seal this plan and its file SHA-256.
2. Seal the V6 pre-campaign readiness no-go and verify the evidence bound in
   section 1.
3. Build the exact V7 V5-source carry-equivalence and ordered-cohort manifests;
   verify their candidate/semantic payload hashes equal the V6 carry without
   treating V6 as their source.
4. Implement order-insensitive exact-key validation and fixed canonical
   controller processing without changing the preserved V6 validator.
5. Add focused tests and execute section-8 readiness in order.
6. If readiness passes, run exactly 60 fresh V7 test-author calls.
7. Seal raw first-pass accounting and apply section-7 eligibility gates.
8. If eligible, run only the exact ordered structural reauthor set, at most six.
9. Run the fresh blind delta audit for every structurally valid final test pair.
10. Run content-free global separation and the exact executable matrix.
11. Seal admission, qualification, 120-cell coverage, and the result narrative.
12. Only a V7 pass returns the project to Gate 3/4 training-entry assessment.

## 10. Scope, ETA, and hard stops

Implementation, readiness, and the local V7 campaign are authorized under the
standing non-GCloud scope. No GCloud read, write, resource action, or billing
is authorized by this plan.

Estimated warm path after implementation is 1–3 hours: 20–45 minutes for
readiness and canaries, 20–60 minutes for 60 parallel test-author calls, and
20–60 minutes for bounded sandbox execution and sealing. This is an estimate,
not evidence.

Stop and seal V7 failed on readiness failure, first-pass threshold failure,
more than six structural rejects, any non-structural reauthor attempt, any
final executable rejection, unresolved exhaustion, canonical-order or
accounting drift, visibility or evaluation-boundary breach, source/lineage
collision, or a goal-alignment `DIVERGENCE` finding.
