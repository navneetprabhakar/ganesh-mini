# Gate 2 repair-delta qualification plan — 2026-09-14

Status: new local contract; implementation not started

Contract identifier: `capability-stratified-v3-repair-delta/v1`

## 1. Decision context

The sealed v2 qualification remains a valid no-go: 217/247 candidates were
admitted, 119/120 cells were covered, and `numeric_reasoning/python/repair`
remained empty after its single permitted replacement. This plan does not
rewrite, relabel, or append another retry to v2.

The failure is not isolated evidence of Python numeric weakness. In the final
v2 semantic review, all 120 generation candidates passed while 18 of 127 repair
candidates failed. In the terminal cell, all three candidates made the
scheduled secondary `malformed_input` behavior the actual repair delta. Their
numeric behavior was already substantially correct. The v2 teacher contract
allowed the sole bug to fall in either the primary capability or the scheduled
cross-cutting dimension, so the generated repair could train the wrong skill.

The smallest balanced surface affected by that construction defect is all 60
repair cells: ten capabilities crossed with six language lanes. Retrying only
the observed empty cell would be adaptive gate-shopping. Repeating the 60
unchanged generation cells would add cost without testing the changed repair
contract. This v3 contract therefore requalifies every repair cell and carries
forward v2 generation evidence only through an explicit equivalence gate.

## 2. Outcome contract

V3 passes only when both conditions hold:

1. the unchanged v2 generation surface remains valid and covers all 60
   generation cells; and
2. a fresh v3 repair cohort admits at least one record in every one of the 60
   repair cells under the revised repair-delta rules.

Passing v3 closes the Gate 2 construction-method qualification. It does not
authorize corpus scaling, training, evaluation opening, GCloud use, model
promotion, merge, quantization, or publication. Those actions retain their
later gates.

## 3. Frozen scope and budget

The v3 first pass contains exactly 60 fresh candidates:

- ten primary capabilities;
- six lanes: Go, Java, JavaScript, TypeScript, Python, and Rust;
- repair task type only;
- one candidate per capability/lane repair cell;
- twelve assignments for each of the five cross-cutting dimensions.

If and only if the first pass meets every provisional threshold in section 9,
each rejected cell may receive one reserve candidate. The first-pass thresholds
limit reserves to six. Absolute generation budget is therefore 66 candidates.
There is no candidate correction pass, seventh reserve, optional stopping, or
content-based rerun. An infrastructure-only replay may repeat the identical
candidate and runtime contract as described in section 10.

All 60 primary source identities and one conditional reserve assignment for
each of the 60 cells are selected and sealed before any v3 teacher call. This
creates 120 preassigned source identities while preserving the 66-candidate
generation cap: only reserves for first-pass rejected cells may be generated,
and no more than six rejected cells may become reserve-eligible. All sources
must be fresh training-only sources, globally unique within v3, absent from the
prior 3,225-row corpus, and disjoint from all 247 v2 qualification candidates.

## 4. Source-affinity gate

A source-affinity classifier sees only the training stimulus, source lineage,
lane, task type, and capability ontology. It must confirm all of the following
before a source can enter the sealed queue:

- the stimulus contains a capability-specific operation and an identifiable
  defect affordance;
- the task can become one self-contained standard-library-only source file;
- the source is code-repair material rather than an MCQ, prose-only question,
  framework configuration, environment task, or external-service workflow;
- no filesystem, network, clock, randomness, package installation, or external
  dependency is required.

Evaluation disjointness is not inferred by this classifier. Before the
classifier runs, the existing content-free separation process must exclude all
exact, normalized, and fuzzy matches to frozen evaluation surfaces and bind the
result without exposing evaluation content, paths, IDs, or archetypes to the
classifier.

The 120-assignment queue must use at least two approved source datasets, and no
one dataset may supply more than 50% of either the primary cohort or the
conditional-reserve cohort. Classifier evidence, input hashes, output hashes,
prompt hashes, runtime parameters, and decisions are sealed. A source rejected
before queue sealing is replaced only by the next item in the deterministic
ordering; after the queue is sealed, source selection cannot react to teacher
output.

## 5. Revised repair-delta teacher contract

The teacher sees one accepted source-affinity card, source lineage, the primary
capability, scheduled cross-cutting dimension, lane runtime contract, and the
rules below. It sees no evaluation prompt, reference, output, verifier record,
private archetype, v2 candidate text, or v2 outcome.

Every candidate must contain exactly one semantic bug. That bug must be in the
assigned primary capability. The scheduled cross-cutting dimension must be
concrete and testable, but the known-bad implementation must already handle it
correctly. Fixing only the secondary dimension must not solve the task.

The teacher emits the existing candidate schema plus a separately sealed
repair-delta proof sidecar containing:

- `capability_operation`;
- `defective_intermediate_or_decision`;
- `valid_domain_counterexample`;
- `minimal_capability_specific_patch`;
- `scheduled_dimension_obligation`;
- `known_bad_already_satisfies_scheduled_dimension`;
- `cross_dimension_only_patch_cannot_solve`; and
- `capability_remains_substantive_without_cross_clause`.

The proof is structural evidence, not self-certification. Missing or internally
inconsistent fields reject the candidate before test authoring. It is stored as
a sidecar so the existing candidate record does not silently change schema.

## 6. Independent semantic and test contracts

The blind semantic reviewer sees only the candidate specification, embedded
known-bad source, assigned capability, and scheduled dimension. It does not see
the teacher-authored repair-delta proof, reference solution, authored tests,
verifier output, training stimulus, source dataset, v2 outcomes, or evaluation
material. It independently derives these measured booleans:

- `repair_delta_requires_primary_capability`;
- `scheduled_dimension_is_concrete_and_secondary`;
- `known_bad_already_satisfies_scheduled_dimension`;
- `cross_dimension_only_patch_cannot_solve`;
- `capability_remains_substantive_without_cross_clause`; and
- `generic_boilerplate_is_not_primary`.

Any false value is a semantic reject.

After blind review, a deterministic consistency gate compares the reviewer's
independent findings with the teacher proof. A disagreement rejects the
candidate; the reviewer is never rerun with the proof exposed.

The independent test author sees only the candidate specification, embedded
known-bad source, assigned capability definition, and scheduled dimension. It
does not see the reference, teacher proof, semantic review, verifier output, or
evaluation material. Tests are emitted under distinct, hashed
`primary_discrimination` and `cross_cutting` roles. Every candidate requires at
least two valid-domain primary-discrimination cases and at least one
scheduled-dimension-only case; an empty or undersized role is rejected before
execution. Executable admission requires:

- the reference passes both suites;
- the known-bad fails at least one primary-discrimination test on valid-domain
  input;
- the known-bad passes every cross-cutting-only test; and
- the generated code runs only in the existing resource-limited,
  network-disabled sandbox.

This prevents malformed-input, ordering, aliasing, duplicate, or state-handling
patches from masquerading as capability-specific repairs.

A separate delta auditor sees the specification, embedded known-bad source,
reference solution, assigned capability, and scheduled dimension, but no tests,
verifier result, teacher proof, source stimulus, v2 outcome, or evaluation
material. It must identify exactly one independent semantic delta, confirm that
the delta is capability-specific, and reject references that introduce multiple
independent fixes. This evidence is sealed independently of semantic review and
test authoring.

## 7. Separation, lineage, and evidence

Every v3 candidate must pass exact, normalized, and fuzzy separation against:

- its 59 first-pass peers and any eligible reserves;
- the sealed 3,225-row prior corpus;
- all 217 admitted v2 qualification records; and
- the frozen public, private-development, and private-decision evaluation
  surfaces through the existing content-free separation boundary.

No evaluation prompt, code, task identifier, path, or archetype may enter a
teacher, reviewer, source-classifier, or correction context. Every result used
in a decision preserves its prompt, rendered-prompt hash, raw output, extracted
code, tests, verifier transcript, runtime parameters, source identity, record
ID, and artifact hashes.

## 8. Generation-equivalence gate

V3 may carry forward the v2 generation results only if an independent report
confirms:

- v2 remains sealed as `qualification-failed` at summary seal
  `293ebd4d38e4200a9de6bd45ba1a9ba4d0f9c0707ce632ba0be8241f41195139`;
- all 120 v2 generation candidates were dispositioned and passed the final
  semantic review;
- 114 were admitted and every one of the 60 generation cells has at least one
  admission;
- v3 changes no generation teacher, semantic, test, separation, execution, or
  runtime rule; and
- all referenced v2 input, output, and nested evidence seals still validate.

If any equivalence condition fails, v3 stops. It cannot silently expand into a
partial generation rerun. A separately versioned full 120-cell plan would then
be required.

## 9. Frozen pass gates

### First-pass repair gate

All 60 first-pass candidates must be generated and terminally dispositioned.
Before reserves become eligible, the first pass must achieve:

- at least 54/60 fully admitted;
- at least 9/10 admitted in every language lane;
- at least 5/6 admitted for every primary capability;
- at least 10/12 admitted for every cross-cutting dimension;
- zero source collisions or lineage failures;
- zero separation failures among admitted records; and
- zero evaluation artifacts read outside the content-free separation process.

Failure of any provisional threshold seals v3 as failed and forbids reserves.

### Final repair gate

Generate exactly one reserve for every first-pass rejected cell, up to six.
Every reserve follows the same source-affinity, teacher, semantic, test,
separation, execution, and evidence rules. All reserves must receive a terminal
disposition. V3 passes only if:

- all 60 repair cells have at least one admitted v3 record;
- with `r` generated reserves, at least 60 of `60 + r` generated candidates
  are admitted; complete cell coverage therefore implies a minimum yield of
  60/66 even at the maximum reserve count;
- every admitted record satisfies every frozen gate;
- no reserve or result is selected post hoc; and
- the combined immutable coverage map contains all 60 carried generation cells
  and all 60 freshly qualified repair cells.

The final report binds the v2 admission and qualification seals, v3 plan and
queue hashes, all v3 evidence, the equivalence report, and the combined 120-cell
coverage map. It must say `qualification-passed-via-v3-repair-delta` or
`qualification-failed`; v2 remains unchanged in either case.

## 10. Replay and hard-stop rules

A timeout, container crash, or host interruption is not a candidate rejection.
One infrastructure-only replay is allowed only with byte-identical candidate,
tests, runtime, and verifier contract plus a sealed retry ledger. An unresolved
second infrastructure failure leaves the candidate undispositioned and fails
the tranche.

Stop and seal v3 as failed for any of the following:

- a first-pass threshold is missed;
- any repair cell remains empty after its one reserve;
- more than 66 candidates would be required;
- a source, candidate, or evidence hash drifts after sealing;
- evaluation material enters construction or review;
- any required lineage, separation, semantic, or executable evidence is
  incomplete; or
- a gate would need to be weakened after observing output.

V3 failure does not authorize v4. Preserve all results and return to a new
explicit construction decision.

## 11. Fast execution sequence

1. Implement and test the source-affinity card, repair-delta proof sidecar,
   split test roles, delta auditor, semantic booleans, equivalence report, and
   v3 summarizer locally.
2. Seal the 120-source deterministic primary/conditional-reserve queue and all
   runtime/prompt contracts.
3. Generate the 60 primary candidates in six lane batches concurrently.
4. Run semantic review and global separation concurrently after generation.
5. Execute eligible candidates with bounded record/verifier concurrency.
6. Finalize all 60 dispositions and evaluate the first-pass thresholds.
7. If eligible, generate and process the fixed reserve set once.
8. Emit the sealed v3 report and combined coverage decision.

Expected warm-path wall time after implementation is 2–4 hours. The 4–8 hour
estimate for implementation, generation, review, sandbox execution, evidence
validation, and one infrastructure replay is low-confidence and assumes normal
local tool latency. This estimate closes only Gate 2. If v3 passes, corpus assembly,
training, untouched evaluation, merge, quantization, laptop certification, and
release gates still remain; the project-level ETA remains approximately 1–3
weeks and depends on measured training transfer.

## 12. Authorization boundary

This plan authorizes no GCloud read, upload, mutation, compute, or billing. It
authorizes no model training and no public release. Implementation and local
qualification are covered by the standing non-GCloud dataset-work scope after
this versioned contract is recorded. Any later GCloud execution still requires
its own exact proposal and explicit approval.
