# Rust elementary-target reconciliation — batch 8

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

Continuation2026-09-08: positions226–240, seven fresh repair prompt/known-bad/
reference/test inspections and generation0196 full reread. Seven additional
holds, eight scoped positives. Remaining generation records reconcile prior
full inspections; no new execution claims.

| Unheld position | Candidate ID | Criterion finding |
| --- | --- | --- |
| 226 | exp-v1-rust-generation-0190 | RUST_STRATUM_REVIEW_11.md documents sequentially consistent compare/exchange retries with checked bounds. Criterion positive; original concurrent totals do not prove full-history linearizability. |
| 227 | exp-v1-rust-generation-0191 | RUST_STRATUM_REVIEW_11.md documents send-before-log ordering and exact failure propagation without modifying sent messages. Criterion positive. |
| 228 | exp-v1-rust-repair-0125 | Clarity hold: prose defines reach as number of checkpoints skipped over, but code/tests use maximum forward index distance (zero prohibits advancing). Clarify off-by-one domain in derived recovery; no executed failure claim. |
| 229 | exp-v1-rust-repair-0126 | Non-triviality hold: insert prescribed division by two into the wedge scalar formula; enum dispatch and formatting unchanged. IEEE behavior is explicitly allowed, not a new numeric correctness hold. |
| 230 | exp-v1-rust-repair-0127 | Fresh full repair inspection: preserve request multiplicity and order after complete catalog/request validation while missing errors remain distinct in first-requested order. Criterion positive. |
| 231 | exp-v1-rust-repair-0128 | Non-triviality hold: append directly prescribed may_exit=false reset after successful transition; guards, mode changes and other flag handling unchanged. |
| 232 | exp-v1-rust-generation-0189 | RUST_STRATUM_REVIEW_11.md documents bounded retry accounting and cap behavior. Criterion positive; maximum attempt-counter envelope not newly adjudicated. |
| 233 | exp-v1-rust-generation-0194 | RUST_STRATUM_REVIEW_11.md documents zero-limit callback suppression, stop-before-selection order and immediate limit termination. Criterion positive. |
| 234 | exp-v1-rust-generation-0195 | RUST_STRATUM_REVIEW_11.md documents validation before slice mutation and detached owned metadata/value copies; arbitrary f64 input explicitly allowed. Criterion positive. |
| 235 | exp-v1-rust-generation-0196 | Non-triviality hold: single initialization Boolean with directly prescribed authorization/error ordering and no additional payload or transitions. |
| 236 | exp-v1-rust-generation-0197 | RUST_STRATUM_REVIEW_12.md documents byte-safe delimiter scanning, literal nonrecursive replacements and no partial output on error. Criterion positive. |
| 237 | exp-v1-rust-generation-0198 | RUST_STRATUM_REVIEW_12.md documents checked shape before slicing and backward in-place merge preserving left-first stability. Criterion positive. |
| 238 | exp-v1-rust-repair-0129 | Non-triviality hold: convert missing exact-ID lookup into the explicitly prescribed MissingId error before an existing Boolean reset; unrelated ledger operations unchanged. |
| 239 | exp-v1-rust-repair-0130 | Non-triviality hold: literal decode mask4 to8 correction; coherent atomic loading and concurrency-safe read-modify-write setters unchanged. |
| 240 | exp-v1-rust-repair-0132 | Non-triviality hold: greater-than to greater-or-equal substitution in direct threshold comparison wrapper. |

Batch8 total14 holds,16 scoped positives. Cumulative240/942:91 new holds,
149 scoped positives. First-time Rust repair inspections112; outside unique
coverage4911. Corpus holds2237; sample165/135. Continue initially unheld241.
Original5885 and training gates unchanged. Positions226–240 await GCS backup.
