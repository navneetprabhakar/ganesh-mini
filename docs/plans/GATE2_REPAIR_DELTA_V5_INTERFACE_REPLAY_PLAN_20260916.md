# Gate 2 repair-delta V5 interface-replay qualification plan — 2026-09-16

Status: sealed local construction contract; no V5 execution is eligible
until this file, its implementation, and the readiness fixtures in section 7
are sealed

Contract identifier: `capability-stratified-v5-interface-replay/v1`

## 1. Decision context

The V4 first pass is a terminal failure under
`capability-stratified-v4-repair-delta/v1`. It generated and terminally
accounted for all 60 ordered primary candidates, with 5 artifacts ready for
admission, 55 terminal rejections, and 0 unresolved outcomes. The terminal
artifact file has SHA-256
`aae89dfe89c47742f5400c31217b653e6cb6f2a4ec3f5e2ad7c2023d54b31e63`;
the two-phase inventory seal is
`8fc2c4ea31628287ae5b8eb83353f13e1e5aebb1fa93af97256d255c3120e087`.
No V4 reserve became eligible and none may be relabeled or generated.

The observed failures separate into bounded interface defects and two teacher
content defects:

- 10/10 JavaScript witnesses imported the immutable reference and known-bad
  implementations as `reference.js` and `known_bad.js`, while the executor
  staged only one implementation as `solution.js`;
- 10/10 Rust witnesses were valid binary `fn main` programs, while the
  executor compiled them as test harnesses and ran zero tests;
- one Java witness encountered the JVM infrastructure signature
  `Properties init: Could not determine current working directory`, which was
  treated as a semantic exit and received no infrastructure replay;
- two TypeScript witnesses were invalid: one rejected the reference on its
  own assertion, and one used top-level `await` under the disclosed CommonJS
  compiler contract;
- 27 independent test-author responses emitted more than the exact two
  logical files accepted by the validator because the response schema had a
  lower bound but no upper bound;
- three Java test-author responses used a class other than the required
  `SolutionTest` entry point;
- one Go cross-cutting test asserted primary numeric correctness and therefore
  failed on the deliberately unfixed primary defect; and
- one TypeScript test suite imported Node test modules whose types were absent
  from the pinned compiler runtime.

These findings do not convert any V4 rejection into an admission. V5 is a new,
prospectively frozen qualification. It reuses immutable teacher output only
where the failure is demonstrably outside those teacher bytes, replaces the
two invalid TypeScript teacher outputs from fresh sources, and reruns every
downstream decision affected by the corrected interfaces.

## 2. Outcome contract

V5 is a complete ordered 60-cell repair qualification, not a selective retry
of failed cells. It covers the same ten primary capabilities crossed with all
six languages and repair task type. The unchanged, sealed V2 generation
equivalence must still cover all 60 generation cells.

V5 passes only when:

1. all 60 ordered repair cells are terminally accounted for;
2. the first pass meets every threshold in section 10;
3. any eligible reserves are generated and terminally accounted for under the
   same V5 contract;
4. all 60 repair cells have an admitted candidate and at least 60 repair
   candidates are admitted in total; and
5. the carried generation surface and V5 repair surface jointly cover all 120
   capability/language/task-type cells.

A pass qualifies the construction method only. It authorizes neither corpus
scaling nor training, GCloud, evaluation opening, model promotion, merge,
quantization, publication, or a release claim.

## 3. Frozen 60-candidate first-pass cohort

Before any V5 call, emit one ordered cohort manifest containing exactly one
primary entry for each of the 60 repair cells.

### 3.1 Fifty-eight immutable carries

Carry exactly 58 V4 teacher candidates and their teacher proofs byte-for-byte.
The carry manifest must bind, for every row:

- V4 candidate ID, cell ID, source identity, and source-record SHA-256;
- complete candidate SHA-256;
- complete teacher-proof evidence SHA-256;
- teacher-run evidence SHA-256;
- V4 queue-record SHA-256; and
- a fixed disposition of `immutable-v4-teacher-carry`.

The carried bytes may not be edited, corrected, re-prompted, or supplemented.
No V4 semantic, test-author, delta, separation, executable, admission, or
ready-for-admission status is implied by carrying teacher output.

### 3.2 Exactly two fresh TypeScript replacements

Do not carry the V4 teacher candidates for:

- `numeric_reasoning/typescript/repair`; or
- `stateful_workflows/typescript/repair`.

Select exactly one new primary source for each cell using seeded SHA-256 order
over accepted TypeScript repair sources. Selection may use only lane, cell,
dataset and revision, source identity and hash, license eligibility, and the
frozen exclusion ledger. It may not inspect stimulus text, candidate content,
evaluation material, or downstream outcomes when ranking sources.

Use seed `ganesh-mini-gate2-v5-interface-replay-primary-v1`. Exclude every
source in the sealed 3,225-row corpus, every V2 and V3 assignment, and all 120
V4 queue assignments, including V4's unused reserves. The two selected source
identities must be distinct and must be frozen before either teacher call.

Generate exactly one new teacher candidate for each replacement cell under a
V5 prompt that requires a witness executable under the exact TypeScript
CommonJS command without top-level `await`, Node type packages, external
dependencies, or witness-byte transformation. There is no teacher correction
call for either primary.

### 3.3 Cohort ordering and identity

The V5 cohort preserves the canonical capability-major, lane-minor ordering of
the 60 repair cells. Its manifest binds the 58 carry rows, two new-source rows,
plan SHA-256, runtime and preflight config hashes, tool identities, and ordered
cohort SHA-256. A duplicate, missing cell, changed carried hash, reused excluded
source, or reordered admission input fails closed before execution.

## 4. Corrected witness interfaces

All 60 candidates rerun post-teacher preflight under one sealed V5 evidence
schema. No V4 preflight result is carried.

### 4.1 JavaScript carried dual-artifact mode

For the ten carried JavaScript candidates, stage the immutable reference at
`reference.js`, the immutable known-bad at `known_bad.js`, and the immutable
witness at `cross_witness.js`. Execute the witness once with the pinned Node
runtime. The result passes only if the process exits zero and emits the exact
success marker once after its assertions.

The evidence binds both implementation hashes, all three staged paths and
byte hashes, the frozen command, runtime image identity, limits, output, and
sandbox contract. The executor may not rewrite imports or witness bytes. This
dual-artifact mode applies uniformly to all ten carried JavaScript candidates;
it is not selected from their individual outcomes.

### 4.2 Rust carried binary-witness mode

For the ten carried Rust candidates, compile the immutable witness as a normal
edition-2021 binary with its selected immutable implementation available as
`solution.rs`, then run that binary. Execute the same witness separately
against reference and known-bad. Both executions must exit zero and emit the
exact marker once. Compiling the witness with `rustc --test`, accepting zero
executed tests, or editing `fn main` is forbidden.

### 4.3 Java infrastructure classification

Classify the exact JVM startup signature
`Properties init: Could not determine current working directory` as verifier
infrastructure. It receives at most one byte-identical replay, with candidate,
witness, staged files, runtime, image, limits, command, and sandbox contract
unchanged. A second infrastructure result is `unresolved`; it is never a
semantic rejection or admission.

### 4.4 Other lanes and semantic requirements

Go, Java, TypeScript, and Python otherwise use their newly sealed, fixture-
qualified single-implementation witness commands. Reference and known-bad
must compile, and both must independently reach and pass the scheduled-
dimension witness. A non-infrastructure compile failure, a reference assertion
failure, a known-bad assertion failure, or missing success marker is a
terminal candidate rejection. It is not repaired.

## 5. Semantic-review carry and completion

The 37 V4 blind semantic reviews that were completed before test authorship may
be carried only through an explicit equivalence manifest proving:

- byte-identical teacher candidate and embedded known-bad;
- byte-identical cell labels and primary-capability definition;
- byte-identical semantic-review projection;
- unchanged semantic booleans and visibility contract; and
- exact prior semantic evidence and reviewer-run hashes.

If any field differs, that review is not carried. Run exactly one new blind
semantic review for each candidate without an equivalent review: the 21
carried candidates previously stopped at tooling preflight and the two fresh
TypeScript candidates, for 23 new reviews when all 37 equivalence checks pass.
There is no semantic-review correction or second call.

## 6. Exact test-author contract and uniform downstream rerun

Discard every V4 test-author artifact, including artifacts attached to the
five V4 ready outcomes. Run exactly one fresh independent test-author call for
each of all 60 V5 primary candidates.

The response schema contains exactly two named objects:

- `primary_discrimination`, with exactly one logical path, one non-empty
  content string, and at least two distinct valid-domain case IDs; and
- `cross_cutting`, with exactly one different logical path, one non-empty
  content string, and at least one case ID that asserts only the scheduled
  dimension.

No arrays of test files, additional role, additional property, or second file
for either role are allowed by the generation schema. The prompt and schema
must agree with the validator before any call.

Lane-specific instructions must name the canonical staging and runtime
constraints. In particular:

- Java content defines the runtime entry point `SolutionTest` with
  `static void main`;
- TypeScript uses self-contained assertions compatible with the pinned
  compiler and may not import `node:test`, `node:assert`, or unavailable type
  packages;
- Go places multiple primary cases in the one primary test file rather than
  emitting multiple files; and
- a cross-cutting suite may establish inputs and invoke the API, but may not
  assert the corrected primary result or fail first because the primary defect
  remains present in known-bad.

After test authorship, rerun the delta audit for every surviving candidate,
because the complete post-test candidate hash changes. Build one global
content-free separation report over the complete surviving post-test cohort,
then run the four suites and immediate final admission. Carry no V4 delta,
separation, executable, retry-ledger, lineage, final-admission, or ready status.

The final four-suite matrix remains:

- reference passes primary discrimination;
- reference passes cross-cutting;
- known-bad fails primary discrimination; and
- known-bad passes cross-cutting.

## 7. Mandatory pre-execution fixtures and readiness

No V5 teacher, semantic-review, test-author, or delta-audit call may run until
one sealed readiness report passes through the exact production code paths.
Fixtures must cover all six lanes, all approved provenance families, and the
following observed interface shapes:

- JavaScript dual-artifact witness staging with immutable reference and
  known-bad modules;
- Rust binary `fn main` witness compilation and marker execution;
- Java JVM current-working-directory infrastructure classification followed
  by one identical replay;
- rejection of a three-file test-author response before execution;
- rejection of a Java test without the `SolutionTest` entry point;
- rejection of a TypeScript test using unavailable Node test typings;
- rejection of a cross-cutting test whose assertion depends on repaired
  primary behavior; and
- one deliberately broken canonical staging case rejected before execution.

Positive fixtures must pass teacher-envelope validation, witness preflight,
strict test-author validation, canonical staging, the four executable suite
outcomes, evidence assembly, ordered accounting, and the exact final admission
validator. The readiness report binds fixture bytes, code and config hashes,
runtime images and commands, sandbox contract, validators, scheduler, and
output hashes. Hand-authored happy paths alone are insufficient; the fixed
fixtures must reproduce the carried V4 JavaScript and Rust witness shapes.

## 8. Go runtime and scheduler contract

V5 does not describe Go as having an aggregate 120-second candidate deadline.
The exact contract is:

- Go candidate concurrency is 1;
- TypeScript candidate concurrency is at most 2;
- Java, JavaScript, Python, and Rust candidate concurrency is at most 4 each;
- global candidate-verifier concurrency is at most 6;
- the four final suites for one candidate execute sequentially;
- each Go final-suite attempt has a 120-second sandbox timeout; and
- only a classified infrastructure failure may receive one byte-identical
  replay of that suite attempt.

The theoretical Go final-matrix ceiling is 480 seconds when all four first
attempts consume their limit and 960 seconds when every suite also consumes
one permitted replay. These are per-attempt bounds, not a promised runtime or
an aggregate deadline. Each Go compile/witness preflight attempt is separately
bounded at 120 seconds and follows the same one-replay infrastructure rule;
preflight time is not hidden inside the final-matrix figure.

All other lanes retain their explicitly sealed attempt limits. Every result
and retry row binds its effective limit. A dynamic remaining-time mutation is
not byte-identical and is forbidden.

## 9. Separation, visibility, and evidence

The V5 teacher, semantic reviewer, test author, and delta auditor retain the
V4 visibility boundaries. Public, private-development, and private-decision
evaluation content remains behind the content-free comparison boundary.

The complete post-test cohort passes exact, normalized, and fuzzy separation
against:

- every V5 peer and any later eligible reserve;
- the sealed 3,225-row corpus;
- all V2 qualification candidates;
- all V3 and V4 generated repair candidates;
- all prior source/candidate exclusions; and
- every evaluation surface through content-free sidecars only.

Preserve prompts and rendered-prompt hashes, raw structured outputs, candidate
and proof bytes, projections, reviewer and test-author evidence, witness and
suite inputs and outputs, runtime bindings, attempt limits, retry ledgers,
separation sidecars, lineage, terminal artifacts, and all artifact hashes.
Generated code executes only in the pinned network-disabled, resource-limited
sandbox.

## 10. Frozen first-pass gates

The ordered admission input is the complete 60-record terminal-artifact
cohort, never a ready-only envelope subset. It must reconcile admitted,
rejected, and unresolved outcomes to exactly 60 and preserve cohort order.

Before any reserve becomes eligible, require:

- all 60 primary candidates generated or immutably carried and terminally
  accounted for;
- zero unresolved candidates after the permitted replay;
- at least 54/60 final-validator admissions;
- at least 9/10 admissions in every language lane;
- at least 5/6 admissions for every primary capability;
- at least 10/12 admissions for every cross-cutting dimension;
- zero source collisions or lineage failures;
- zero separation failures among admitted records; and
- zero evaluation artifacts read outside the content-free boundary.

Failure of any threshold seals V5 as failed and forbids reserves.

## 11. Prebound reserves and absolute budgets

Before first-pass execution, deterministically prebind one fresh reserve source
for each of the 60 cells using seed
`ganesh-mini-gate2-v5-interface-replay-reserve-v1`. Reserve selection follows
the same content-blind fields and exclusions as section 3.2, is globally
unique, and excludes the two V5 primary replacement sources. A reserve source
is not generation-eligible merely because it is prebound.

If and only if every first-pass threshold passes, generate exactly one reserve
for every rejected cell, up to six. Each reserve uses the same V5 teacher,
preflight, review, strict test-author, delta, global separation, execution, and
final-admission contracts. There is no correction pass, second reserve,
candidate editing, witness editing, test editing, content-tailored prompt, or
ad hoc rerun.

Budgets are:

- first-pass cohort: exactly 60 candidates, comprising 58 immutable carries
  and 2 new teacher generations;
- conditional reserves: 0–6 new teacher generations;
- absolute terminal candidate budget: 66; and
- absolute new V5 teacher-generation budget: 8.

V5 passes only after every generated reserve is terminally accounted for, all
60 repair cells are admitted, at least 60 repair candidates are admitted in
total, and V2 generation equivalence yields combined 120/120 cell coverage.

## 12. Execution sequence

1. Seal this plan and its file SHA-256.
2. Freeze the 58-row immutable carry manifest, two fresh primary sources, 60
   fresh reserve sources, exclusion ledger, and ordered cohort manifest.
3. Implement and seal the V5 witness modes, infrastructure classifier, strict
   test-author schema, staging, scheduler, terminal accounting, and final
   validator bindings.
4. Pass and seal the readiness fixtures in section 7.
5. Generate exactly the two fresh TypeScript primaries.
6. Rerun preflight for the complete ordered 60-candidate cohort.
7. Validate 37 semantic-review equivalence rows and run the remaining 23 blind
   semantic reviews exactly once.
8. Run one new strict test-author call for every surviving primary, followed
   by new delta audits.
9. Freeze the complete post-test cohort, perform global content-free
   separation once, then execute suites and immediate final admission.
10. Seal the ordered first-pass report and apply the frozen thresholds.
11. If eligible, generate and process only the exact prebound reserves.
12. Emit the terminal V5 qualification and 120-cell coverage decision.

## 13. ETA and authorization boundaries

Low-confidence local wall-time estimate after the plan and implementation are
sealed is 6–12 hours for fixtures, the two new teacher candidates, 60 strict
test-author calls, downstream evidence, and first-pass adjudication, assuming
normal tool latency. Conditional reserves may add 1–3 hours. This estimate
closes only Gate 2. Later training, untouched evaluation, merge, quantization,
laptop certification, and release remain approximately 2–4 weeks and depend
on measured model-quality transfer.

This plan authorizes only local, non-GCloud implementation and the bounded V5
qualification after readiness passes. It authorizes no GCloud read, upload,
resource mutation, compute, or billing; no training; no evaluation opening;
and no publication. Existing standing scope governs local repository and
artifact operations, but no action may be represented as executed evidence
until its sealed output exists.

## 14. Hard stops

Stop before any model call if the carry manifest is not exactly 58 rows, either
fresh TypeScript source is not eligible and unique, any V4 queue source is
reused, the ordered cohort is not exactly 60 cells, implementation and fixture
hashes differ, or readiness fails.

After execution begins, stop and seal V5 without reserves if any first-pass
threshold fails, any unresolved outcome remains, ordered accounting differs
from 60, evaluation content crosses the boundary, a carried teacher byte is
modified, or evidence cannot be reproduced from its bindings. Stop before a
reserve if it was not prebound, its cell was not rejected in an otherwise
passing first pass, more than six reserves would be required, or the new
teacher-generation budget would exceed eight.

A V5 failure requires a new explicit construction decision. It does not
authorize selective correction, another interface replay under a new label,
or reinterpretation of V4/V5 failures as admissions.
