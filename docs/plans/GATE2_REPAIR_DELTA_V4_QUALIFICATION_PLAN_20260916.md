# Gate 2 repair-delta v4 qualification plan — 2026-09-16

Status: local construction contract; no v4 teacher call is eligible until the
tooling-compatibility preflight in section 5 passes

Contract identifier: `capability-stratified-v4-repair-delta/v1`

## 1. Decision context

The v3 repair-delta qualification is a terminal no-go. Its complete first pass
generated 60 candidates: 3 were rejected before separation, 49 reached
executable evidence, and 8 exhausted their single byte-identical
infrastructure replay. Final admission accepted 0 candidates, rejected 52,
and retained 8 as unresolved. The terminal qualification report is
`qualification-failed` at seal
`b2b718a1d61f3a6858b28f9b9938438548a89eb37e04a091ace5036f914c3727`.
No reserve became eligible and none was generated.

V3 exposed three independent implementation defects rather than evidence that
the revised repair semantics were intrinsically unworkable:

1. The verifier staged independently authored test files under content-addressed
   names while five frozen runtime commands expected one canonical filename.
   This produced 40 reference primary-suite failures dominated by missing test
   files. One additional candidate failed its known-bad cross-cutting suite.
2. Eight Go candidates ran as concurrent cold `linux/amd64` compilations on an
   Apple arm64 host. All 64 recorded suite attempts timed out after roughly 60
   seconds with no exit code or output, while the same pinned runtime completed
   the ninth Go candidate in 31–42 seconds. This is terminal v3 evidence, not a
   candidate retry opportunity.
3. Eight otherwise executable CommitPackFT candidates were rejected because
   final admission supported only the earlier generic source-key schema. The
   exact sealed CommitPackFT lineage was preserved, but the dataset-specific
   schema was not represented in the validator.

V4 does not reinterpret those outcomes, reuse v3 candidates, or relabel the
forbidden v3 reserves. It is a fresh construction round whose first purpose is
to prove that the exact executor and final validator agree before spending a
teacher call.

## 2. Outcome contract

V4 passes only when:

1. the sealed v2 generation-equivalence gate still validates all 60 generation
   cells without changing any v2 result; and
2. a fresh v4 repair cohort covers all 60 capability/language repair cells
   under the final admission validator.

A pass qualifies the construction method only. It authorizes neither scaling
nor training, GCloud, evaluation opening, model promotion, merge,
quantization, publication, or a release claim.

## 3. Freshness and candidate budget

Build a new deterministic queue with exactly 120 source assignments: 60
first-pass assignments and one conditional reserve assignment for each of the
same 60 cells. Use a new seed and new queue identity. Exclude:

- every source in the sealed 3,225-row corpus;
- every source assigned to any v2 qualification candidate;
- all 120 source identities preassigned by v3, including its unused reserves;
- every v3 generated candidate from peer-content separation; and
- every frozen evaluation surface through the content-free boundary.

Using a v3 reserve as a v4 primary is forbidden. Every source identity is
globally unique within v4. Both cohorts use at least two approved datasets and
no dataset supplies more than 50% of either cohort. Queue construction reads no
evaluation content.

The first pass is exactly 60 candidates, one per repair cell. Reserves become
eligible only after every first-pass threshold in section 8 passes. At most six
reserves may be generated, one for each rejected cell. The absolute generation
budget remains 66. There is no candidate correction pass or content-directed
rerun.

### 3.1 Pre-queue source-pool repair

The first read-only feasibility audit of the currently classified pool is
negative. After excluding 2,996 prior-corpus, 247 v2, and all 120 v3 source
lineages, 13,236 repair sources remain, but only 55/60 cells have two or more
accepted sources. The deficits are:

- `callbacks_and_events/python`: 0;
- `graph_and_tree/python`: 0;
- `callbacks_and_events/go`: 1;
- `callbacks_and_events/rust`: 1; and
- `graph_and_tree/rust`: 1.

Therefore v4 begins with one separately sealed source-pool extension, not with
queue construction or candidate generation. Use the native Go, Python, and
Rust files from pinned `bigcode/commitpackft` revision
`fc56fe33c030c6daa414c2b112c932b8eed085e6`:

| Lane | Pinned source path | Bytes | SHA-256 |
|---|---|---:|---|
| Go | `data/go/data.jsonl` | 12,417,842 | `05a65e973fcc6894a234fb382987cc25e26f053d60b032ea83540a5b36a528b8` |
| Python | `data/python/data.jsonl` | 135,858,935 | `d167da37e1058371c48e057cd8815d03700c867dd8bcf58e61420d4dcd288d73` |
| Rust | `data/rust/data.jsonl` | 7,411,711 | `5611f3701026acf3c43ba64da50f4f65a078e84fba56e2bf313e8f2996b0cc68` |

Download by exact revision and require byte and SHA-256 identity before
reading. Build each full permissively licensed eligible inventory with the
same native CommitPackFT rules already frozen for JavaScript and TypeScript:
quarantine `new_contents`, require a non-empty repair stimulus from bounded
commit metadata plus `old_contents`, preserve every raw/source/content hash,
and exclude all prior, v2, and v3 lineages. If any lane has fewer than 1,000
eligible records, stop before classification.

Freeze exactly the first 1,000 eligible records per lane—3,000 total—by
SHA-256 ordering with seed
`ganesh-mini-gate2-v4-native-commitpackft-repair-source-v1`. Selection occurs
before capability inspection and uses only lane, dataset/revision, record
identity, source hash, license eligibility, and the exclusion ledger. It may
not use capability keywords, evaluation material, v3 outcomes, or the five
observed deficit labels to rank records.

Classify all 3,000 preselected records once under the unchanged
source-affinity ontology. Do not top up a cell adaptively from observed
classifier output. The tranche succeeds only if every deficient cell reaches
at least two total accepted, fresh sources and all 60 cells remain queueable
under the two-dataset/50% rules. If it fails, seal the extension negative and
require a new source decision; do not draw another tranche under this plan.

## 4. Unchanged semantic construction rules

Retain the v3 repair-delta semantics and visibility boundaries:

- the sole semantic bug is in the assigned primary capability;
- the scheduled cross-cutting dimension is concrete and independently
  testable, but the known-bad already handles it correctly;
- the blind semantic reviewer never sees the teacher proof, reference, tests,
  verifier output, source stimulus, v2/v3 outcomes, or evaluation material;
- the independent test author never sees the reference, teacher proof,
  semantic decision, verifier output, source stimulus, or evaluation material;
- the delta auditor sees the specification, known-bad, reference, and assigned
  labels, but not tests, proof, verifier output, source stimulus, prior outcomes,
  or evaluation material; and
- separation occurs once over the complete post-test cohort before executable
  evidence is produced.

The v3 proof fields, semantic booleans, split test roles, delta requirements,
one-bug rule, separation checks, evidence seals, and lineage requirements stay
unchanged unless this plan explicitly strengthens them. V4 adds one sealed
`known_bad_cross_witness`: a valid-domain input and scheduled-dimension
assertion on which the reference and known-bad both reach and satisfy the
secondary behavior before the primary defect is fixed.

## 5. Mandatory tooling-compatibility preflight

No source queue may become generation-eligible and no v4 teacher call may run
until all items below pass under the exact final validator.

### 5.1 Canonical per-role test staging

Each test-author response contains exactly one logical file for each role. The
primary file contains at least two distinct valid-domain cases; the
cross-cutting file contains at least one isolated scheduled-dimension case.
When a role is executed alone, the runner stages that role's logical file to
the runtime's canonical test path:

| Lane | Canonical staged test path |
|---|---|
| Go | `solution_test.go` |
| Java | `SolutionTest.java` |
| JavaScript | `solution.test.js` |
| TypeScript | `solution.test.ts` |
| Python | `test_solution.py` |
| Rust | `solution_test.rs` |

The staging transform binds the authored content hash, logical path, canonical
path, role, runtime ID, candidate path, commands, and suite hash. It may rename
or copy bytes only; it may not edit test content. Java test content must expose
the runtime-expected `SolutionTest` entry point. The final admission validator
recomputes and verifies the same staging contract.

### 5.2 Candidate compilation preflight

Before semantic review or test authoring, compile or syntax-check both the
reference and known-bad implementation using a separately sealed per-lane
preflight command in the same pinned image, sandbox, candidate path, and
platform used for admission. No tests are present at this stage. Any source
that does not compile is a candidate rejection; it is not repaired or shown
compiler feedback.

At the same post-teacher/pre-test-author boundary, execute the sealed
`known_bad_cross_witness` against both implementations. Both must reach and
pass the scheduled-dimension assertion on the valid-domain witness. A witness
that is masked by the primary defect rejects the candidate. This prevents the
v3 Go failure in which a nominal aliasing test errored on the unfixed primary
key-selection defect before aliasing could be observed. Witness bytes and
results are hidden from the independent test author.

After test authoring and canonical staging, execute the final four-suite
matrix before marking an artifact ready:

- reference passes primary;
- reference passes cross-cutting;
- known-bad fails primary; and
- known-bad passes cross-cutting.

The controller's `ready-for-admission` state is valid only if an immediate
call to the unchanged final validator accepts the exact envelope. A local
controller status may never substitute for final admission.

### 5.3 Dataset-specific provenance schemas

Freeze exact source schemas per approved dataset. McEval and MdEval keep their
existing required and allowed fields. CommitPackFT may use only the additional
keys declared by its sealed source-pool policy and must bind the exact dataset
revision, source file hash, record identity, license, old/new content hashes,
selection rank, and transformation lineage. Unknown keys, missing keys, a
different revision, or a generic `additionalProperties` relaxation fail
closed.

### 5.4 End-to-end fixtures and runtime readiness

Before generation, pass sealed fixtures for every one of the six lanes and
every approved provenance family through teacher-envelope validation, test
staging, sandbox execution, evidence assembly, final admission, and terminal
summary. Each lane fixture must demonstrate the four expected suite outcomes
and one deliberately broken staging fixture must be rejected. The fixture
report binds code/config hashes, image identities, runtime commands, sandbox
contract, final validator, and output hashes.

V4 uses lane-aware executor limits on the current Apple arm64 host:

- Go candidate concurrency: 1;
- TypeScript candidate concurrency: at most 2;
- Java, JavaScript, Python, and Rust candidate concurrency: at most 4 each;
- global candidate-verifier concurrency: at most 6; and
- each candidate's four suite calls remain sequential.

Go receives a 120-second per-candidate execution envelope for this frozen
emulated runtime. The other lanes retain their existing limits. A native arm64
or multi-architecture Go image may replace emulation only through a separately
sealed runtime-contract revision and a repeated six-lane fixture preflight.

## 6. Source and separation contract

The source-affinity classifier retains the v3 content and visibility rules.
The new 120-source queue must additionally publish an exclusion ledger proving
that no v3 primary or reserve assignment was reused. If the single bounded
extension does not make a fresh balanced queue constructible, stop before
teacher generation and seal v4 as source-infeasible.

Every generated v4 candidate passes exact, normalized, and fuzzy separation
against:

- all v4 peers and any eligible reserves;
- the sealed 3,225-row corpus;
- all v2 qualification candidates;
- all 60 generated v3 repair candidates;
- all source/candidate exclusions already frozen by prior gates; and
- public, private-development, and private-decision evaluation surfaces only
  through the content-free comparison boundary.

No evaluation prompt, code, ID, path, or archetype may enter a teacher,
reviewer, test author, source classifier, correction context, or report.

## 7. Replay and terminal accounting

A timeout, container crash, or host interruption receives at most one
byte-identical infrastructure replay. Candidate bytes, staged test bytes,
runtime, limits, image, commands, and verifier contract must be identical and
bound in the retry ledger. If the second attempt remains infrastructure-only,
the candidate is `unresolved`, the complete first pass is terminally failed,
and reserves are forbidden.

The admission input is the ordered 60-record evidence-assembly cohort, not the
ready-only envelope subset. It retains pre-execution rejects, final-validator
rejects, and unresolved outcomes. The terminal report must reconcile exactly
60 generated candidates across admitted, rejected, and unresolved states.

## 8. Frozen gates

All 60 first-pass candidates must be generated and terminally accounted for.
Before reserves become eligible, require:

- zero unresolved candidates after the permitted replay;
- at least 54/60 final-validator admissions;
- at least 9/10 admissions in every language lane;
- at least 5/6 admissions for every primary capability;
- at least 10/12 admissions for every cross-cutting dimension;
- zero source collisions or lineage failures;
- zero separation failures among admitted records; and
- zero evaluation artifacts read outside the content-free boundary.

Failure of any threshold seals v4 as failed and forbids reserves. If the first
pass passes, generate exactly one prebound reserve for every rejected cell, up
to six. V4 passes only when all 60 repair cells and all 60 carried generation
cells are covered, at least 60 repair candidates are admitted, and every
generated reserve is terminally accounted for.

## 9. Execution sequence

1. Record the v3 terminal no-go in project state and decisions.
2. Implement canonical role staging, compile preflight, strict dataset source
   schemas, lane-aware scheduling, and complete terminal accounting.
3. Pass and seal six-lane and all-provenance end-to-end fixtures through the
   exact final admission path.
4. Freeze and classify the single content-blind source-extension tranche; prove
   fresh-source feasibility, then seal the new 120-source queue and its
   exclusion ledger.
5. Revalidate the v2 generation-equivalence evidence.
6. Generate all 60 fresh first-pass candidates in lane batches.
7. Complete blind review, independent tests, delta audit, global separation,
   lane-aware execution, and final admission.
8. Seal the first-pass result. Generate reserves only if every provisional
   threshold passed.
9. Emit the terminal v4 qualification and 120-cell coverage decision.

Expected local wall time after this plan is sealed is 18–36 hours if the single
source extension succeeds and tool latency is normal. This estimate closes only
Gate 2. A Gate 2 pass would still leave corpus scaling/assembly, a new bounded
training run, untouched evaluation, merge, quantization, laptop certification,
and release gates; the honest project-level ETA remains approximately 2–4
weeks and is conditional on measured model-quality transfer.

## 10. Hard stops and authorization

Stop and seal v4 without teacher generation if tooling fixtures or source
freshness fail. Stop and seal after generation if a first-pass threshold is
missed, a required cell remains empty after its one eligible reserve, the
66-candidate budget would be exceeded, evidence drifts, or evaluation content
crosses the boundary. A v4 failure requires another explicit construction
decision; it does not authorize retries under a new label.

This plan uses local, non-GCloud dataset work only. It authorizes no GCloud
read, upload, resource mutation, compute, or billing; no training; no public
evaluation opening; and no publication. Any later GCloud use retains its exact
proposal and explicit-approval boundary.
