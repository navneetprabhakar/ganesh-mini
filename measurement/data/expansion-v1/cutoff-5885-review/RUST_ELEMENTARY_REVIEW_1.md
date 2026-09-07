# Rust elementary-target reconciliation — batch 1

2026-09-07. Frozen queue rust-elementary-followup-queue-v1.json:
1006 outside-sample records, 64 prior-held exclusions, 942 initially unheld.
Positions 1–30 explicitly reconciled: 9 new holds and 21 scoped
criterion positives. This is not seven-criterion admission.

Fourteen repair records received fresh full prompt/known-bad/reference/original-test
inspection. Generation records use the explicitly cited prior full inspection
notes or a fresh prompt/reference reread as stated per row. Prior "no hold" alone
was not used as criterion approval. No new candidate execution in this batch.

| Unheld position | Candidate ID | Criterion finding |
| --- | --- | --- |
| 1 | exp-v1-rust-generation-0001 | Fresh prompt/reference reread: decimal validation, attempt counting and sticky completion interact. Criterion positive. |
| 2 | exp-v1-rust-repair-0001 | Fresh prompt/known-bad/reference/tests: macro stringify spelling, Debug-only values and once-only left-to-right formatting are substantive. Criterion positive. |
| 3 | exp-v1-rust-repair-0002 | Fresh full inspection: character-count to UTF-8 byte-boundary repair, oversized count and replacement of old runs. Criterion positive. |
| 4 | exp-v1-rust-repair-0003 | Fresh full inspection: checked arithmetic before aliased-slot mutation and index-only cross-arena identity. Criterion positive. |
| 5 | exp-v1-rust-repair-0004 | Non-triviality hold: prompt names the missing separator; correction inserts one semicolon in an otherwise unchanged recursive macro. |
| 6 | exp-v1-rust-generation-0007 | Fresh prompt/reference reread: platform root normalization preserves UTF-8 boundaries and fallback precedence. Criterion positive. |
| 7 | exp-v1-rust-generation-0009 | Prior full inspection in RUST_STRATUM_REVIEW_1.md explicitly documents duplicate validation, deterministic scheduling ties and checked time. Those coupled behaviors satisfy this criterion; no new source/execution claim. |
| 8 | exp-v1-rust-generation-0010 | Fresh prompt/reference reread: case-insensitive header uniqueness, restricted text grammar and owned policy matching. Criterion positive. |
| 9 | exp-v1-rust-generation-0011 | Non-triviality hold: one-bit transition predicate, reset and fixed Debug rendering; reread resolves the prior pending criterion. |
| 10 | exp-v1-rust-repair-0005 | Fresh full inspection: zero/aligned padding boundary, checked output-length arithmetic and independent owned bytes. Criterion positive. |
| 11 | exp-v1-rust-repair-0006 | Fresh full inspection: strict tie comparison preserves earliest borrowed identity, including equal/extreme signals. Criterion positive. |
| 12 | exp-v1-rust-repair-0007 | Non-triviality hold: direct vector clone plus one-field rename repairs a move error; no larger state or ownership interaction beyond the clone wrapper. |
| 13 | exp-v1-rust-repair-0008 | Fresh full inspection: length decrement follows successful node removal, preserving linked LIFO invariants and zero-sized-element reuse. Criterion positive. |
| 14 | exp-v1-rust-generation-0013 | RUST_STRATUM_REVIEW_1.md full inspection documents Rc lifetime ownership, per-pool identifiers, Drop and delegation. Explicitly reconciled as substantive ownership behavior. |
| 15 | exp-v1-rust-generation-0014 | RUST_STRATUM_REVIEW_1.md documents cache checks, atomic malformed refresh and saturating expiry. Criterion positive; the separately unspecified terminal-clock policy is not newly certified. |
| 16 | exp-v1-rust-generation-0015 | RUST_STRATUM_REVIEW_1.md documents recursive lower-bound search without slice copies and first-duplicate selection. Criterion positive. |
| 17 | exp-v1-rust-generation-0016 | Non-triviality hold: direct BTreeMap CRUD/length/default wrappers and cloned values collection; full reread found no additional state invariant. |
| 18 | exp-v1-rust-generation-0018 | RUST_STRATUM_REVIEW_1.md documents topology preservation and message-knowledge validation. Criterion positive; earlier wording/iterator concerns are not silently promoted to all-criterion approval. |
| 19 | exp-v1-rust-repair-0009 | Non-triviality hold: replace capacity() with len() in a direct String wrapper; surrounding methods delegate unchanged. |
| 20 | exp-v1-rust-repair-0010 | Non-triviality hold: one field-selector correction in fixed-format output beside already-correct prescribed escaping. |
| 21 | exp-v1-rust-repair-0011 | Fresh full inspection: valid replacement must return old address, while failed validation retains previous exact-key mapping and ordered owned names. Criterion positive. |
| 22 | exp-v1-rust-repair-0012 | Non-triviality hold: elementary delimiter joining with direct first-element separator suppression. |
| 23 | exp-v1-rust-generation-0019 | RUST_STRATUM_REVIEW_1.md documents Rc auto-trait constraints, slot ownership transfer and no Clone bound. Criterion positive; omitted wrapped-enqueue/negative-compile tests remain historical coverage limitations. |
| 24 | exp-v1-rust-generation-0020 | Fresh prompt/reference reread: duplicate/missing option parser, strict unsigned grammar and deterministic wrapping generation. Criterion positive; this does not resolve a different arithmetic-grouping interpretation. |
| 25 | exp-v1-rust-generation-0021 | RUST_STRATUM_REVIEW_2.md documents minimal ordered change planning and copy-before-commit application. Criterion positive, not new execution. |
| 26 | exp-v1-rust-generation-0022 | Non-triviality hold: fully prescribed method-resolution syntax and three literal formatting wrappers. |
| 27 | exp-v1-rust-generation-0023 | Fresh prompt/reference reread: count-error/zero-count short-circuit prevents entry calls and preserves retrieval error/text. Criterion positive for dependency-call ordering. |
| 28 | exp-v1-rust-generation-0024 | RUST_STRATUM_REVIEW_2.md documents checked points/round arithmetic, ranking ties and reclaim boundary. Criterion positive; expired-unreclaimed replacement wording is not newly certified. |
| 29 | exp-v1-rust-repair-0013 | Non-triviality hold: add the missing sort() call to an already-provided elementary stride extraction/reinsertion loop. |
| 30 | exp-v1-rust-repair-0014 | Fresh full inspection: multiplication and addition overflow guards plus the distinct isize allocation boundary, including zero-sized elements. Criterion positive. |

All fourteen repairs are outside the historical v6 inspected union and the later
Go/Java queues: unique outside-sample inspections increase from 4799 to 4813.
Re-reviewing the sixteen generation records adds no unique inspection credit.
Total corpus holds 2155 (2152 additive plus historical 3). Frozen sample remains
165 positive / 135 held. Continue initially unheld position 31 of 942.
The2146 GCS checkpoint predates this queue and batch. Original5885 unchanged.
