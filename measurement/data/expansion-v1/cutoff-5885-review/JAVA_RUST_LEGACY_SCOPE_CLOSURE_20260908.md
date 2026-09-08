# Java/Rust legacy systematic-group closure accounting — 2026-09-08

Scope: the four remaining named groups in `REMAINING_QUALITY_SCOPE_AUDIT_20260908.md`. This is criterion-specific evidence reconciliation, not fresh population inspection, training admission, or release approval. ZERO new unique-row coverage, ZERO candidate executions, ZERO proposed new holds. Main owns disposition integration.

## Frozen accounting and join

Inputs: `stratum-followup-inventory-v14.json`, historical `datasets/cache/expansion-v1/review-partition-v1/review-eligible.jsonl`, and `additional-holds.json` at SHA256 `e496e2b954d68471cfe2cac98446a47032ac2111da853f0ff8475155326eb510`. Additive holds2718 plus historical3 = total2721. One historical hold is outside the inventory; counting only inventory exclusions would incorrectly report2720 globally.

Membership is the union of the group's explicit `strata`, matching all four stratum fields, ignoring only its population count. Do not use heuristic tags to select rows. Survivors are eligible historical IDs minus additive holds. Overlapping group memberships are not distinct records.

| Group | Affected | Held | Surviving | Sample survivors | Outside survivors | Missing outside per-ID evidence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| java_unicode_blank_validation | 720 | 381 | 339 | 15 | 324 | 0 |
| java_null_query_list_validation | 635 | 330 | 305 | 14 | 291 | 0 |
| java_percentage_intermediate_overflow | 1086 | 593 | 493 | 27 | 466 | 0 |
| incomplete_rust_generation_api | 614 | 185 | 429 | 20 | 409 | 0 |

The three Java groups contain527 unique surviving IDs; Rust adds429, for956 unique survivors (48 sample,908 outside). All Java outside IDs join exact full-ID rows in `JAVA_FOLLOWUP_REVIEW_1.md` through `_75.md`; Rust outside IDs join four-digit generation IDs in `RUST_STRATUM_REVIEW_1.md` through `_46.md`. Later Rust elementary rows are joined by full generation ID, never by a repair with the same numeric suffix. Sample evidence is `JAVA_SAMPLE_SCOPE_RECONCILIATION_V2.md` and `SEVEN_CRITERIA_RUST.md`, reconciled with `sample-criteria-reconciliation-v2.json`. This is complete existing coverage, not a claim to have reread956 candidates here.

## Java: supported closure of all three named groups

Recommend closing the legacy population-level reopen flags for these three criteria using the existing per-ID combined review plus the later sample/page reconciliation. No genuinely unresolved Unicode-blank, null-query-list, or percentage-intermediate contract ID was identified in the surviving evidence.

- Unicode blank: combined review distinguishes unrestricted whitespace rejection from an explicit `trim` contract; `JAVA_SAMPLE_SCOPE_RECONCILIATION_V2.md` subsequently holds generation0394/0782 and repair0041/0241/0243, removing the sample gap. Those IDs are already excluded above. Unicode case equivalence caveats on repair0322/0360 are not whitespace-blank findings and must not reopen this criterion.
- Null query/list validation: complete validation must precede query shortcuts only where the prompt requires it. Sample generation0253/0308/0379/0458 and repair0418/0475 give explicit traversal/prevalidation evidence. Combined generation0531 validates nested data before the result limit. Explicitly allowed null generation0680 is not a defect.
- Percentage intermediate overflow: combined review and sample arithmetic reconciliation remove the original percentage defects; `JAVA_PAGE_RECONCILIATION_20260907.md` separately reconciles numeric page concerns. Page generation0269/0287/0378/0583 and repair0265 widen before risky arithmetic; generation0408/repair0293 use bounded or subtraction-based checks. Generation0716 is already held for a concrete allocation-before-validation contract problem. Repair0372/0414 have already adjudicated concrete-array resource bounds; do not replace them with virtual-array/private-state witnesses.

Surviving generation0320/0347/0376/0506 carry large concrete collection/count capacity caveats, not an identified percentage numerator overflow. Generation0604 explicitly follows double arithmetic, not a promise of extra numerical stability. Generation0194 error precedence,0522 target exception identity, and0668 deliberately ambiguous sentinel are unrelated to these three groups. These caveats remain visible without becoming fabricated failures or blanket re-review obligations.

## Rust: bounded residual contract adjudication, not429-row rereview

Existing sample and generation reviews support API-scope closure for424 of429 surviving affected rows, with the five exact IDs below retained as unresolved contract adjudication. Their later elementary positives do not resolve API questions. Full prompt/reference/tests for these five were read in this accounting pass; no diagnostic was executed and no hold is inferred merely from the prior word `pending`.

| Candidate ID | Existing generation / elementary evidence | Exact residual question |
| --- | --- | --- |
| exp-v1-rust-generation-0164 | STRATUM10 / ELEMENTARY7 | AccessGate lists method names but only types `destroy`. Reference/tests select boolean `try_read`/`try_write`, unit blocking acquisitions and shared receivers. Decide whether those required call signatures are adequately inferable from prose or constitute an underspecified public API. Scheduling-test bounded-yield risk is separate, not proof of a missing API. |
| exp-v1-rust-generation-0403 | STRATUM23 / ELEMENTARY17 | Prompt says exact two-public-field CardLedger while also explicitly requiring internal remembered operations; reference adds a private BTreeSet. Decide whether the displayed struct is an externally constructible literal contract or a public-field sketch. Constructors and state requirements favor sketch, but exact literal wording remains a specific conflict. Duplicate malformed-event priority is separate. |
| exp-v1-rust-generation-0467 | STRATUM27 / ELEMENTARY19 | Prompt allows three generic OutputLine types with associated errors but never defines LineError's generic shape or requires common error types. Reference restricts all three errors to one E; tests use one line/error type and only is_err. Heterogeneous errors versus a homogeneous bound is a real API choice not settled by those tests. |
| exp-v1-rust-generation-0528 | STRATUM31 / ELEMENTARY22 | Builder method return signatures and `common traits` are incomplete. Reference permits another for_user after fetching while retaining the prior token/routes. Decide whether staged completion is per selected user or merely historical completion, and whether inferred Result<Self,PlanError> signatures suffice. No invented repeated-stage failure oracle. |
| exp-v1-rust-generation-0533 | STRATUM31 / ELEMENTARY22 | Exported macro invocation grammar is not frozen, and reference `$crate::SplatVector` relies on the original harness importing that trait at crate root when solution.rs is a module. Determine intended root/module consumer contract. Positive element count is a stated input domain, not by itself a requirement to reject count0. |

The exact residual list is therefore generation0164/0403/0467/0528/0533, all Rust. These are proposed adjudication targets, not automatically failed rows. The bounded next action is contract interpretation for these five, with a sandbox compile probe only if the interpretation requires it; tests cannot settle an unstated contract by themselves.

### Prior caveats that do not establish missing API contracts

Prompt rereads resolve these as sufficient API sketches for this specific closure recommendation:

- Generation0152/0184/0212/0583/0625 give typed operations grouped with the sole owning type and self-taking methods. Constructor association is a natural coherent interpretation, not an absent method/type. Existing per-ID tests agree. No new execution claim; private exhaustion and large-read caveats remain separate.
- Generation0101 names public fields whose String/u32 types are supplied by the typed update methods and owned clone requirement. This is not an unspecified field-type family like held sample0291.
- Generation0541 supplies all method signatures but sketches `pub struct MemoryEndpoint;` beside explicitly required per-instance FIFO storage. Treat that declaration as opaque storage placeholder, consistent with sample generation0065's established sketch interpretation, not a new exact-unit-layout failure.
- Generation0655 spells out every field, enum variant and method type. Unrequested extra derives and inaccessible sequence exhaustion are not incomplete API.
- Generation0278 states downstream capability/privacy requirements and generic blanket behavior. Same-crate-only original testing is an oracle coverage limitation, not an absent public contract; a separate-crate diagnostic would test that already explicit contract. Do not count it among the five missing/ambiguous contract cases.
- Generation0791 exact score versus action-choice evidence concerns semantics/oracle coverage, not missing API. Resource envelopes, unspecified competing-error order, recursion bounds, and elementary concerns elsewhere are not silently globally approved by this closure.

## Integration recommendation

Close the three Java systematic criterion groups; replace the broad Rust API reopen with the five explicit adjudication IDs above. Preserve all other criterion dispositions and all existing holds. This report neither certifies every remaining semantic caveat nor requests a blanket rerun or rereview. Recovery admission and frozen release gates remain separate work.
