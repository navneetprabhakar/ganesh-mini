# Rust elementary-target reconciliation — batch 6

2026-09-07. Frozen initially unheld positions151–180: 13 new holds
and 17 scoped criterion positives. Eighteen repair prompts, known-bad
sources, references and original tests read in full; generation0117,0127,0129
reread in full. Other generation rows explicitly reconcile prior full notes.
Two isolated diagnostic probes compile then fail under pinned Rust1.85.0,
network-disabled resource-limited sandbox. Raw evidence preserves frozen input,
reference, test source, runtime identity and hashes. No training admission.

| Unheld position | Candidate ID | Criterion finding |
| --- | --- | --- |
| 151 | exp-v1-rust-repair-0075 | Non-triviality hold: prescribed wrapping_mul to saturating_mul substitution in a one-expression affine closure. |
| 152 | exp-v1-rust-repair-0076 | Non-triviality hold: replace literal 7 with prescribed 8 in an otherwise correct OnceLock weight table. |
| 153 | exp-v1-rust-generation-0117 | Fresh prompt/reference reread: Unicode byte-safe borrowed head and ownership snapshot before mutation impose substantive borrowing interaction. Criterion positive. |
| 154 | exp-v1-rust-generation-0120 | RUST_STRATUM_REVIEW_8.md documents generational tokens, LIFO slot reuse and retirement transitions. Criterion positive; private generation exhaustion remains unexecuted. |
| 155 | exp-v1-rust-repair-0077 | Fresh full repair inspection: stable removal must preserve the relationship between tab order and active index. Criterion positive. Public operations keep active at the final tab; original tests named after-active/next-tab do not exercise those unreachable branches. |
| 156 | exp-v1-rust-repair-0078 | Fresh full repair inspection: capacity equality protects in-place shifts while preserving bad-length, unsorted, full error precedence and atomicity. Criterion positive. |
| 157 | exp-v1-rust-repair-0079 | Non-triviality hold: greater-than to greater-or-equal tie change in a two-input trimmed-length selector; borrowing and trimming already correct. |
| 158 | exp-v1-rust-repair-0080 | Fresh full repair inspection: exclusive end must work for both ordinary and midnight-wrapping windows, with empty windows distinct. Criterion positive. |
| 159 | exp-v1-rust-generation-0118 | RUST_STRATUM_REVIEW_8.md documents marker-state parsing, module validation and ordered borrowed sorting. Criterion positive; newline-path/one-line-output wording remains unresolved. |
| 160 | exp-v1-rust-generation-0123 | RUST_STRATUM_REVIEW_8.md documents turn-start item ownership, checked simulation arithmetic and counts. Criterion positive; zero-round/common-product error precedence not newly resolved. |
| 161 | exp-v1-rust-generation-0126 | RUST_STRATUM_REVIEW_8.md documents complete syntax validation before numeric conversion including discarded patch field. Criterion positive. |
| 162 | exp-v1-rust-repair-0082 | Non-triviality hold: direct saturating_add to saturating_sub substitution in one command arm; previous-value handling unchanged. |
| 163 | exp-v1-rust-repair-0084 | Fresh full repair inspection: cooldown admission, failed-fire immutability, elapsed countdown and zero-duration repeated firing interact. Criterion positive. |
| 164 | exp-v1-rust-generation-0127 | Non-triviality hold: exact membership test followed by prescribed fixed warning formatting. |
| 165 | exp-v1-rust-generation-0128 | RUST_STRATUM_REVIEW_8.md documents widened coordinate differences, half-open rectangle bounds and independent clones. Criterion positive. |
| 166 | exp-v1-rust-generation-0129 | Non-triviality hold: unrestricted internal representation permits direct VecDeque forwarding for every operation and derived clone; no linked-list implementation required. |
| 167 | exp-v1-rust-generation-0131 | RUST_STRATUM_REVIEW_8.md documents retries versus attempts and preserving unconsumed outcomes on stop/escalation. Criterion positive; impractical maximum retry count not executed. |
| 168 | exp-v1-rust-repair-0085 | Non-triviality hold: add directly prescribed newly_added=false assignment to an already correct filtered fixed-field update loop. |
| 169 | exp-v1-rust-repair-0086 | Non-triviality hold: add prescribed min(100) to scalar fuel constructor; all dashboard formatting is unchanged. |
| 170 | exp-v1-rust-repair-0087 | Non-triviality hold: replace field assignment with prescribed whole-vitals assignment; unrelated complete text codec does not deepen the repair. |
| 171 | exp-v1-rust-repair-0088 | Non-triviality hold: replace None stub with direct inner Option.as_mut forwarding; wrapper conversions and map unchanged. |
| 172 | exp-v1-rust-generation-0135 | RUST_STRATUM_REVIEW_8.md documents checked i32 conversion, ordered operand validation and checked multiplication. Criterion positive. |
| 173 | exp-v1-rust-generation-0137 | RUST_STRATUM_REVIEW_8.md documents ASCII-prefix byte slicing, route/arity parsing and checked sum. Criterion positive. |
| 174 | exp-v1-rust-repair-0089 | Fresh full repair inspection: stable global path deduplication and merging into first accepted name require substantive ordered aggregation. Criterion positive; prose ordering of predicate versus path pruning remains a clarity question (original tests explicitly call predicate on pathless names). |
| 175 | exp-v1-rust-repair-0090 | Fresh full repair inspection: ordered nine-bit neighborhood encoding coupled with fixed-grid bounds and alternating outside state. Criterion positive; no large-step or overflow execution claimed. |
| 176 | exp-v1-rust-repair-0092 | Fresh full repair inspection: atomic cross-category namespace reservation must be symmetric while borrowed lookups remain category-specific. Criterion positive. |
| 177 | exp-v1-rust-generation-0144 | RUST_STRATUM_REVIEW_9.md documents Unicode scalar reversal within runs while preserving exact intervening Unicode whitespace. Criterion positive. |
| 178 | exp-v1-rust-repair-0093 | Correctness hold: executed finite-component sum overflow returns None; finite opposite-sign interval midpoint returns 0 instead of 0.5. Pinned rust-repair0093-finite-boundaries-result.json: compile0/test101, 1916ms, no timeout. |
| 179 | exp-v1-rust-repair-0095 | Correctness hold: public derived Default starts IDs at zero despite start-at-one contract. Pinned rust-repair0095-default-identity-result.json: compile0/test101, 1827ms, no timeout; actual Ok(0), expected Ok(1). |
| 180 | exp-v1-rust-repair-0096 | Clarity hold: place_sell 'similarly' follows explicit multiplication-overflow rejection for buys, but reference never checks sell product; clarify whether sell price product must be representable. No executed failure or unreachable private-ID overflow claim. |

Cumulative180/942:62 new holds,118 scoped criterion positives.
Eighty-two first-time Rust repair inspections bring unique outside coverage to4881.
Corpus holds2208; frozen sample165/135 unchanged. Continue initially unheld181.
Original5885 unchanged; no training seal or new VM.
