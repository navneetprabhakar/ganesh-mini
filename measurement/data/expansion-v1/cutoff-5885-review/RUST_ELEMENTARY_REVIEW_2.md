# Rust elementary-target reconciliation — batch 2

2026-09-07. Frozen initially unheld positions31–60: five new holds and25
scoped criterion positives. Eleven repair prompts/known-bad references/corrected
references/original tests read in full. Two generation prompts/references reread;
remaining generation findings explicitly reconcile cited earlier full inspection
notes. No new candidate execution; no seven-criterion admission claim.

| Unheld position | Candidate ID | Criterion finding |
| --- | --- | --- |
| 31 | exp-v1-rust-repair-0015 | Fresh full repair inspection: fixed wire length, signed two's-complement boundary and endian round-trip consistency. Criterion positive. |
| 32 | exp-v1-rust-repair-0016 | Non-triviality hold: insert one prescribed ampersand mapping into an elementary character-replacement loop. |
| 33 | exp-v1-rust-generation-0025 | RUST_STRATUM_REVIEW_2.md documents validation-before-update and identity cascade across stored objects. Criterion positive. |
| 34 | exp-v1-rust-generation-0026 | RUST_STRATUM_REVIEW_2.md documents physical-line parsing, final-duplicate precedence and recognized-key extraction. Criterion positive. |
| 35 | exp-v1-rust-generation-0027 | RUST_STRATUM_REVIEW_2.md documents global height uniqueness and state-keyed ordered ranges. Criterion positive. |
| 36 | exp-v1-rust-generation-0030 | RUST_STRATUM_REVIEW_2.md documents validated revision transitions and retained old revision on removal. Criterion positive. |
| 37 | exp-v1-rust-repair-0017 | Non-triviality hold: replace two strict comparisons with non-strict comparisons in elementary adjacent-window predicates. |
| 38 | exp-v1-rust-repair-0019 | Fresh full repair inspection: Rc cloning must preserve shared interior-mutability identity, consumption visibility and no mutation on insufficient quota. Criterion positive. |
| 39 | exp-v1-rust-generation-0031 | RUST_STRATUM_REVIEW_2.md documents borrowed sorted inclusive queries and checked aggregation. Criterion positive. |
| 40 | exp-v1-rust-generation-0032 | RUST_STRATUM_REVIEW_2.md documents ordered left/right generic proof combination and depth validation. Criterion positive. |
| 41 | exp-v1-rust-generation-0033 | Non-triviality hold: optional snapshot lookup and fixed Debug-format field interpolation; fresh prompt/reference reread resolves earlier pending criterion. |
| 42 | exp-v1-rust-generation-0034 | RUST_STRATUM_REVIEW_2.md documents minimum/high-bid invariants, validation-before-mutation and terminal claim checks. Criterion positive. |
| 43 | exp-v1-rust-generation-0035 | RUST_STRATUM_REVIEW_2.md documents authorization, phase/deadline boundaries and terminal transitions. Criterion positive. |
| 44 | exp-v1-rust-generation-0036 | RUST_STRATUM_REVIEW_2.md documents finite ordered rectangles, inclusive intersections and insertion-preserving replacement. Criterion positive. |
| 45 | exp-v1-rust-repair-0021 | Fresh full repair inspection: content equality, canonical Rc allocation identity and lifetime beyond input buffers/pool growth. Criterion positive. |
| 46 | exp-v1-rust-repair-0022 | Non-triviality hold: literal suffix and length-bound replacement in an elementary filename predicate. |
| 47 | exp-v1-rust-repair-0023 | Fresh full repair inspection: zero-based half-open callback range preserves side effects, first-match short circuit and maximum-bound safety. Criterion positive. |
| 48 | exp-v1-rust-repair-0024 | Fresh full repair inspection: phantom-tagged handles must select identical read/write slots and remain valid after append. Criterion positive; tests do not constitute negative compile proof. |
| 49 | exp-v1-rust-generation-0037 | RUST_STRATUM_REVIEW_3.md documents Feistel forward/inverse arithmetic and key/block structure. Criterion positive, not cryptographic certification. |
| 50 | exp-v1-rust-generation-0038 | RUST_STRATUM_REVIEW_3.md documents independent typed journals with borrowed empty slices and ordered duplicate-preserving vectors. Criterion positive. |
| 51 | exp-v1-rust-generation-0039 | RUST_STRATUM_REVIEW_3.md documents bounded u128 allocation arithmetic and preservation of the total budget. Criterion positive. |
| 52 | exp-v1-rust-generation-0040 | RUST_STRATUM_REVIEW_3.md documents generic memoization including zero values and wrapping session identity. Criterion positive; unspecified panic retry policy is not certified. |
| 53 | exp-v1-rust-generation-0041 | RUST_STRATUM_REVIEW_3.md documents ordered recipients, membership/inbox invariants and sequence consumption. Criterion positive. |
| 54 | exp-v1-rust-generation-0042 | Non-triviality hold: two independent scalar guards around fixed-array read/write, prior-value return and fill/reset; fresh reread found no coupled register behavior. |
| 55 | exp-v1-rust-repair-0026 | Fresh full repair inspection: maximal grouping at exact capacity, zero-size items, complete prevalidation and subtraction-based overflow avoidance. Criterion positive. |
| 56 | exp-v1-rust-repair-0027 | Fresh full repair inspection: checked source/destination bounds before mutation and overlapping memmove semantics remove an unsafe nonoverlap assumption. Criterion positive. |
| 57 | exp-v1-rust-repair-0028 | Fresh full repair inspection: exact separator count precedes ordered empty-field errors, with Unicode trimming and owned results. Criterion positive. |
| 58 | exp-v1-rust-generation-0044 | RUST_STRATUM_REVIEW_3.md documents strict pair direction, ordered validation and saturating aggregation. Criterion positive; no new performance guarantee. |
| 59 | exp-v1-rust-generation-0047 | RUST_STRATUM_REVIEW_3.md documents circular replacement with exact wide mean and lower-median order statistics. Criterion positive. |
| 60 | exp-v1-rust-generation-0048 | RUST_STRATUM_REVIEW_3.md documents selected-branch traversal, checked arithmetic and active-path cycle detection permitting shared nodes. Criterion positive; unexecuted depth-envelope concerns remain separate. |

Rust cumulative60/942 initially unheld reconciled,14 new holds,46 scoped positives.
The25 first-time repair inspections across batches1–2 increase outside unique
coverage from4799 to4824; generation reconciliation adds no new unique credit.
Corpus holds2160 (2157 additive+historical3); sample165/135 unchanged.
Continue initially unheld61. GCS verified through2146 predates this Rust work.
Original5885 unchanged; no training seal or new VM.
