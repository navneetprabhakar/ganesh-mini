# Rust elementary-target reconciliation — batch 8 (partial)

2026-09-08. Initially unheld positions211–225: seven holds and eight scoped
criterion positives. Eight repair prompt/known-bad/reference/test sets fully
read; generation0181 and0187 reread in full. Other generation records explicitly
reconcile cited prior inspections. No new diagnostic executions or admission.

| Unheld position | Candidate ID | Criterion finding |
| --- | --- | --- |
| 211 | exp-v1-rust-repair-0115 | Fresh full repair inspection: checked ceiling row count must agree with partial-row placements and checked pixel dimensions. Criterion positive. |
| 212 | exp-v1-rust-repair-0116 | Non-triviality hold: reverse one prescribed secondary key comparator; validation and escaping are unchanged. |
| 213 | exp-v1-rust-generation-0179 | RUST_STRATUM_REVIEW_11.md documents zero-count/width rules, checked inclusive final code and big-endian encoding. Criterion positive; huge allocation envelope not newly certified. |
| 214 | exp-v1-rust-repair-0117 | Fresh full repair inspection: collect Result before popping scope so early binding/body errors restore outer bindings. Criterion positive for Result-return paths; arithmetic overflow/panic cleanup is not specified or newly certified. |
| 215 | exp-v1-rust-repair-0118 | Non-triviality hold: substitute explicitly identified blinding coefficient in fixed modular formula; reduction and u128 arithmetic unchanged. |
| 216 | exp-v1-rust-repair-0120 | Non-triviality hold: replace Boolean conjunction with disjunction in the explicitly identified OR arm; eager operand evaluation and evaluator machinery unchanged. |
| 217 | exp-v1-rust-generation-0181 | Non-triviality hold: six-bit latch consists of direct bounds checks and bit set/clear/test wrappers. |
| 218 | exp-v1-rust-generation-0183 | RUST_STRATUM_REVIEW_11.md documents widened signed route distances and subtract-adjacent/add-bridge cost computation. Criterion positive under stated individual u64-fit guarantee. |
| 219 | exp-v1-rust-generation-0184 | RUST_STRATUM_REVIEW_11.md documents ordered duplicate tokens and ASCII trimming. Criterion positive; constructor association and vertical-tab policy remain unresolved. |
| 220 | exp-v1-rust-generation-0185 | RUST_STRATUM_REVIEW_11.md documents normalized stored items, retained terminal IDs, checked adjustments and sorted borrowed output. Criterion positive. |
| 221 | exp-v1-rust-generation-0186 | RUST_STRATUM_REVIEW_11.md documents checked integer operations including MIN/-1, finite real promotion/results and restricted text addition. Criterion positive. |
| 222 | exp-v1-rust-repair-0121 | Non-triviality hold: remove permissive trim and explicitly reject outer whitespace in an already complete fixed-format parser. |
| 223 | exp-v1-rust-repair-0122 | Fresh full repair inspection: retain existing catalog record until replacement normalization and revision validation succeed, preserving errors atomically. Criterion positive. |
| 224 | exp-v1-rust-repair-0124 | Non-triviality hold: direct exclusive-to-inclusive range substitution in a drain-and-extend wrapper; validation and ordered movement unchanged. |
| 225 | exp-v1-rust-generation-0187 | Non-triviality hold: trait/default-method demonstration consisting of prescribed string concatenations and direct generic forwarding. |

Cumulative225/942:84 new holds,141 scoped positives. First-time Rust repair
inspections105; outside unique coverage4904. Corpus holds2230; sample165/135.
Continue initially unheld226. Original5885 and training gates unchanged.
