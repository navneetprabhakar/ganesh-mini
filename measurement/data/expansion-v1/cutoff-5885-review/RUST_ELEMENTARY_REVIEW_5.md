# Rust elementary-target reconciliation — batch 5

2026-09-07. Frozen initially unheld positions121–150: nine new holds and21
scoped criterion positives. Thirteen repair prompts/known-bad/reference/tests
read in full; five generation prompts/references reread. Other generation rows
explicitly reconcile cited prior full inspections. No new execution or
seven-criterion admission claim.

| Unheld position | Candidate ID | Criterion finding |
| --- | --- | --- |
| 121 | exp-v1-rust-generation-0093 | RUST_STRATUM_REVIEW_6.md documents first-equals parsing, duplicate unknown-key rejection and complete-record validation. Criterion positive. |
| 122 | exp-v1-rust-generation-0094 | RUST_STRATUM_REVIEW_6.md documents root invariant, layer-local writes, reverse lookup and deep-cloned scopes. Criterion positive. |
| 123 | exp-v1-rust-generation-0095 | RUST_STRATUM_REVIEW_6.md documents conditional exactly-once callbacks, ordered normalization and stable owned-string deduplication. Criterion positive. |
| 124 | exp-v1-rust-generation-0096 | RUST_STRATUM_REVIEW_6.md documents checked command arithmetic and exact arity. Criterion positive; historical trailing-whitespace wording is not resolved by this criterion review. |
| 125 | exp-v1-rust-repair-0061 | Fresh full repair inspection: unsigned magnitude handles i32::MIN before modulo reduction, keeping the mathematical band bounded. Criterion positive. |
| 126 | exp-v1-rust-repair-0062 | Non-triviality hold: remove rev() from a fixed-prefix message formatting and join loop. |
| 127 | exp-v1-rust-repair-0063 | Non-triviality hold: direct checked_add to checked_mul substitution in a one-expression wrapper. |
| 128 | exp-v1-rust-repair-0064 | Non-triviality hold: direct from_be_bytes to from_le_bytes substitution in a one-expression fixed-array decoder. |
| 129 | exp-v1-rust-generation-0098 | RUST_STRATUM_REVIEW_6.md documents checked handle-count transitions and uniqueness without aggregation overflow. Criterion positive. |
| 130 | exp-v1-rust-generation-0100 | RUST_STRATUM_REVIEW_6.md documents clone-before-commit patches and first-invalid-patch indices. Criterion positive; within-patch multi-error precedence is not newly certified. |
| 131 | exp-v1-rust-generation-0101 | RUST_STRATUM_REVIEW_6.md documents lookup-before-replacement validation, atomic revision and owned sorted results. Criterion positive. |
| 132 | exp-v1-rust-generation-0102 | RUST_STRATUM_REVIEW_7.md documents desired/current canonicalization, allowed replacement precedence and stable filtering. Criterion positive. |
| 133 | exp-v1-rust-repair-0065 | Fresh full repair inspection: Unicode scalar truncation retains iterator remainder to add omission marker only when needed. Criterion positive. |
| 134 | exp-v1-rust-repair-0066 | Non-triviality hold: remove an explicitly prohibited reserved term from a directly prescribed scalar allocation formula. |
| 135 | exp-v1-rust-repair-0067 | Fresh full repair inspection: shutdown closes permanently and drops stored values before return; rejected insertion preserves ownership of the live value. Criterion positive. |
| 136 | exp-v1-rust-repair-0068 | Non-triviality hold: one wrapping_add to saturating_add substitution in a scalar meter wrapper; existing borrowed-self return is unchanged. |
| 137 | exp-v1-rust-generation-0103 | RUST_STRATUM_REVIEW_7.md documents required fields and duplicate validation even for ignored keys, plus first-equals parsing. Criterion positive. |
| 138 | exp-v1-rust-generation-0104 | Fresh prompt/reference reread: Cow must preserve borrowed/owned representation on no-op and detach only on mutation. Criterion positive for observable ownership behavior. |
| 139 | exp-v1-rust-generation-0106 | Non-triviality hold: three syntactic loop variants of the same prescribed two-value wrapping recurrence. |
| 140 | exp-v1-rust-generation-0107 | RUST_STRATUM_REVIEW_7.md documents checked decimal framing, byte lengths, strict trailing-byte rejection and owned Unicode payloads. Criterion positive. |
| 141 | exp-v1-rust-generation-0108 | RUST_STRATUM_REVIEW_7.md documents tree validation from connectivity/edge count and breadth-first query parity. Criterion positive. |
| 142 | exp-v1-rust-repair-0069 | Non-triviality hold: replace unwrap() with ok() in a direct first-field trim/parse wrapper. |
| 143 | exp-v1-rust-repair-0070 | Non-triviality hold: change the explicitly incompatible Sized bound to ?Sized in a direct size_of_val forwarding wrapper. |
| 144 | exp-v1-rust-repair-0071 | Fresh full repair inspection: entry API resolves conflicting mutable borrows while preserving existing counters and exposing only the selected mutable value. Criterion positive. |
| 145 | exp-v1-rust-generation-0109 | Non-triviality hold: prescribed flag assignments, one default cache value and saturating count increments with direct trait forwarding. |
| 146 | exp-v1-rust-generation-0110 | RUST_STRATUM_REVIEW_7.md documents ordered nonzero identifiers and bounded u64 total derived from u32 key/value cardinality. Criterion positive. |
| 147 | exp-v1-rust-generation-0112 | Fresh prompt/reference reread: validate dimensions before atomically changing both dimensions and the ordered escape sequence; same-size resize still updates sequence. Criterion positive. |
| 148 | exp-v1-rust-generation-0114 | Fresh prompt/reference reread: global ID uniqueness and ordered full-input validation before detached scene projection. Criterion positive. |
| 149 | exp-v1-rust-repair-0073 | Fresh full repair inspection: exact failure threshold couples counter/open state and success resets both. Criterion positive; original maximum-limit test executes four failures, not u32::MAX transitions. |
| 150 | exp-v1-rust-repair-0074 | Fresh full repair inspection: skip the seeded first value while preserving maximal-run state, separated equal values and final-run flush. Criterion positive. |

Cumulative150/942 initially unheld:49 new holds,101 scoped criterion positives.
The64 first-time Rust repair inspections raise unique outside coverage to4863.
Corpus holds2195; sample165/135 unchanged. Continue initially unheld151.
Original5885 unchanged; no training seal or new VM.
