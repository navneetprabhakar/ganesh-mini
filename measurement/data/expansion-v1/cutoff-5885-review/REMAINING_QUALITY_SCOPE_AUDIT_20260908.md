# Remaining Gate 2 quality scope audit — 2026-09-08

## Boundary and conclusion

Read-only audit, conditional on main completing and validating the frozen Python
numeric/elementary queue of 668 initially-unheld records. This note does not assert
that integration has finished. Intended change: this isolated note only. No
candidate execution, cloud activity, central ledger/state change, admission,
new unique-row credit, or new hold recommendation.

The remaining work is **criterion-level closure reconciliation and versioned
recovery/admission**, not another automatic 5,500-record review. The frozen
inventory records where systematic defects reopened strata; its historical
`affected-strata-reopened` status is not a live unresolved-issue ledger. Likewise,
old notes saying “not seven-criterion approval” do not establish seven new review
queues per record. The controlling contract requires the deterministic sample to
cover all seven criteria and systematic findings to be resolved in affected strata.
It does not require every corpus row to undergo seven separate manual passes.

Sources: `docs/data/EXPANSION_V1.md` (Quality sampling and Admission sequence),
`docs/plans/GANESH_MINI_1_0_PLAN_PASS2.md`, `docs/process/PROJECT_STATE.md`,
`followup-systematic-groups-v7.json`, `stratum-followup-inventory-v14.json`,
`COVERAGE_RECONCILIATION.md`, and the reconciliation/review notes named below.
Paths without a directory are relative to this note's directory.

## Exact frozen scope membership, not unfinished-record counts

v14 contains 21 overlapping systematic groups and 21 distinct reopened strata:
5,500 unique records, including 278 frozen-sample records and 5,222 outside-sample
records. The figures below were recomputed by exact stratum-object membership
(lane, source, task type, rejection history), excluding only the group stratum's
population field. Heuristic tags were not used as defect or coverage evidence.

Six elementary groups plus Python numeric comprise seven groups addressed by the
latest lane passes. The other fourteen groups are listed here. Counts cannot be
summed across rows and **are not counts still needing review**.

| Systematic group | All members | Outside sample | Sample | Existing evidence to reconcile |
| --- | ---: | ---: | ---: | --- |
| java_unicode_blank_validation | 720 | 684 | 36 | Java combined follow-up and Java sample scope reconciliation v2. |
| sparse_element_validation | 655 | 622 | 33 | Array-focused and JS/TS residual reviews; relevant sample criteria notes. |
| subscription_registration_identity | 535 | 508 | 27 | Array/targeted and JS/TS residual reviews; registration-versus-function identity findings. |
| reference_accommodates_incorrect_test_or_api | 211 | 201 | 10 | Array/targeted and JS/TS residual reviews; do not treat passing accommodating tests as API correctness. |
| incomplete_rust_generation_api | 614 | 583 | 31 | Completed Rust generation reviews, with later Rust elementary per-ID reconciliation. |
| python_mapping_contract | 597 | 567 | 30 | Completed Python generation/repair notes and Python sample criteria; N/E alone does not settle a Mapping/API question. |
| python_invalid_enum_exception | 720 | 684 | 36 | Completed Python generation notes and Python sample criteria; required exception semantics remain the relevant question. |
| finite_intermediate_arithmetic | 576 | 547 | 29 | JS/TS residual and Python repair reviews; Python N follow-ups supplement but do not replace other lanes. |
| prototype_key_storage_loss | 516 | 490 | 26 | JS/TS residual reviews and sample criteria; actual property preservation rather than key-name heuristics. |
| required_property_copy_loss | 451 | 428 | 23 | JS/TS residual reviews and sample criteria; required copying/properties versus unpromised descriptor semantics. |
| javascript_reference_test_accommodation | 116 | 111 | 5 | JS/TS residual reviews and sample criteria; specification remains authoritative. |
| contradictory_suffix_uniqueness | 276 | 262 | 14 | JS/TS residual reviews and later TypeScript per-ID reconciliation. |
| java_null_query_list_validation | 635 | 603 | 32 | Java combined follow-up and Java sample scope reconciliation v2. |
| java_percentage_intermediate_overflow | 1086 | 1031 | 55 | Java combined follow-up, sample reconciliation v2 and page reconciliation. |

The relevant completed inspection queues are array-focused 544, targeted 10,
Rust generation 684, Python generation 684, Python repair 426, and JS/TS residual
587. `coverage-reconciliation-v1.json` reconciles their overlapping IDs to 2,930
unique outside-sample records in the older v6 scope, with no missing or extraneous
scope IDs. Later state records 757 new Go, 1,112 new Java and 423 first-time Rust
repair inspections: 2,930 + 757 + 1,112 + 423 = 5,222. This arithmetic agrees with
v14's outside-sample population; it is not a substitute for main's final exact-ID
join across all later notes. Python N/E adds no unique coverage.

The 385 records outside v14 include 22 original sample records and 363 outside
sample. Their absence from reopened strata is not universal clearance, but also
does not itself authorize inventing an additional mandatory 363-record queue.

## What is actually unresolved versus retained caveats

1. **Final closure accounting:** join each affected, surviving record to relevant
   prior criterion evidence or a current hold. The inventory supplies scope, not
   this disposition. No exact remaining unheld-defect count can defensibly be
   derived from the inventory or a text search for “pending.” Record explicit
   unresolved contract questions separately from generic limitations; re-read only
   those whose prior evidence cannot decide the scoped criterion. This audit does
   not establish an additional bulk inspection backlog.
2. **Python integration is a prerequisite, not assumed evidence:** main must
   reconcile all 668 IDs and numeric follow-up recommendations, including any
   bounded probe disposition, with the current holds. N/E closure cannot silently
   certify Mapping breadth, exception APIs, copy semantics or test independence.
3. **Sample adjudication is already complete:**
   `sample-criteria-reconciliation-v2.json` records all 300 original sample rows,
   165 positive and 135 held. A held sample item is not an undecided sample item.
   The six lane splits are Go 39/17, Java 29/31, JavaScript 10/20, Python 32/29,
   Rust 41/21 and TypeScript 14/17 (positive/held). Preserve this frozen sample;
   do not resample the original corpus to hide its failures.
4. **Java's newer groups are not untouched:**
   `JAVA_SAMPLE_SCOPE_RECONCILIATION_V2.md` reread all 34 then-positive sample
   records against null-query, percentage and page concerns, adding five blank
   holds. `JAVA_PAGE_RECONCILIATION_20260907.md` resolved the listed earlier page
   expressions and held generation-0716 for allocation before null validation.
   Their historical statements that cross-lane work remained open should not
   reopen Java automatically after the later lane passes finish.

Examples demonstrate why caveats need triage rather than automatic admission or
automatic holds. `PYTHON_GENERATION_REVIEW_46.md` retains arbitrary copy-side-effect
and scalar-subclass breadth notes for generation-0796/0798/0801/0802; these do not
alone identify a required-domain failure. The same note's generation-0797
“copying overwritten values versus selected-value wording” and generation-0799
released-memoryview question are more specific contract interpretations: if
still unheld and unresolved after later notes, resolve their actual prompt domain
before treating them as clearance. This audit has not freshly read those full
candidates and therefore makes no new adverse disposition for them.

Similarly, `RUST_STRATUM_REVIEW_46.md` distinguishes generation-0791's executed
optimal-action/score-sign check from uncertified exact score scale and internal
table bounds. Whether those details are required follows from the prompt, not
from the mere presence of a caveat. Java repair-0372/0414 concrete-array capacity
limitations are already explicitly bounded decisions in sample v2, not newly
discovered overflow holds. Do not conflate them with generation-0716's compact
standard-library list counterexample and actual receipt.

The calibrated Python sample already distinguishes required Mapping semantics
and explicit API contracts from unpromised callback side-effect shielding,
throwing equality, or finite intermediate requirements. Unbounded wall-clock,
allocation, arbitrary malicious custom-method, and private-ID exhaustion promises
must not be silently added. Conversely, an explicit domain contradiction, missing
required API, incorrect mandated exception, or cheaply representable valid case
remains actionable even when original tests pass.

## Admission blockers after quality reconciliation

Even perfect completion of the scoped reviews does not make the original corpus
trainable. The documented 2,597-hold checkpoint already leaves at most 3,288 of
5,885 original rows unheld, below the 4,000 lower bound; later additive holds
cannot repair that yield deficit. This is a dated sufficient bound, not a claim
about the concurrently changing final hold total.

`CORPUS_SUFFICIENCY_PAUSE_20260907.md` records authorization for versioned recovery;
there is no remaining user-permission blocker for that in-scope path.
`RECOVERY_TOOLING_PREFLIGHT_20260908.md` identifies the actual implementation gap:
the existing rejection-repair tool is behavioral-failure oriented, preserves the
prompt, and lacks the required separate immutable derived-version boundary. It
must not silently overwrite or relabel original held rows as recovered.

The concrete next sequence is: finish exact-ID criterion/hold reconciliation;
freeze the resulting original-corpus decision evidence; construct the authorized
versioned recovery path with parent IDs/hashes and explicit change classes;
produce independent tests for changed contracts; perform fresh pinned,
network-disabled resource-limited reference/known-bad execution and evaluation
separation/deduplication; verify quality and the approved corpus-size, task-mix and
five-family supervised-token objectives; seal only justified admitted artifacts.
Preserve evidence and backup receipts. No new GCloud use is authorized by this
audit, and no extra cloud resource is needed to reconcile the review records.

## Audit output

- 14 older overlapping systematic scope groups identified with exact membership
  counts; these are not 14 proven open queues.
- 0 new candidate inspections or unique-row credits; 0 new hold recommendations.
- No defensible exact count of residual unheld contract issues asserted.
- Main retains ownership of final Python integration, exact-ID validation,
  criterion closure, live counts and admission/recovery decisions.
