# Rust elementary-target reconciliation — batch 13

2026-09-08. Initially unheld361–375: nine holds and six scoped positives.
Seven fresh complete repair inspections and generation0307/0309/0310/0311
prompt/reference rereads; remaining generation reconciles cited prior notes.
No new execution and no training admission.

| Unheld position | Candidate ID | Criterion finding |
| --- | --- | --- |
| 361 | exp-v1-rust-generation-0305 | RUST_STRATUM_REVIEW_18.md documents scalar-column offsets, trimmed-part ranges, error precedence and checked decimal overflow. Criterion positive; leading zeroes alone do not establish overflow. |
| 362 | exp-v1-rust-repair-0201 | Non-triviality hold: remove final sort from an already ordered line parser; header, ownership and field validation unchanged. |
| 363 | exp-v1-rust-repair-0203 | Non-triviality hold: add explicitly required edge=None assignment, already demonstrated by release; state encoder/decoder unchanged. |
| 364 | exp-v1-rust-repair-0204 | Fresh full repair inspection: same-desk half-open conflicts must accept adjacency without losing overlap rejection, ordering or atomic admission. Criterion positive; publicly corrupted prior reservations remain outside this reconciliation. |
| 365 | exp-v1-rust-generation-0307 | Non-triviality hold: three independent elementary utilities, direct filter/join, prescribed byte mapping and bounded timestamp subtraction. Bundling does not add interacting state. |
| 366 | exp-v1-rust-generation-0309 | Non-triviality hold: two scalar validations followed by trimmed field copying into receipt; no admission state. |
| 367 | exp-v1-rust-generation-0310 | Non-triviality hold: direct data constructor, two-field copied replacement and literal template; no validation or algorithm. |
| 368 | exp-v1-rust-generation-0311 | Non-triviality hold: direct conversion to ordered sets followed by two standard difference operations. |
| 369 | exp-v1-rust-generation-0312 | RUST_STRATUM_REVIEW_18.md documents private version/key context, exact response length, error clearing and XOR payload handling. Criterion positive; multi-gigabyte resource envelope not executed. |
| 370 | exp-v1-rust-repair-0205 | Non-triviality hold: replace optional symbolic-name fallback with explicitly prescribed literal-field getter; settings and ownership unchanged. |
| 371 | exp-v1-rust-repair-0206 | Fresh full repair inspection: removing a zone must remove exactly its tool IDs from the second index while preserving other zones and allowing clean future reuse. Criterion positive. |
| 372 | exp-v1-rust-repair-0207 | Non-triviality hold: add take to fourth independent optional field, copying the three adjacent correct implementations; build validation unchanged. |
| 373 | exp-v1-rust-repair-0208 | Non-triviality hold: change one dispatch target to explicitly named maintain operation; selector handling, payload checks and counters unchanged. |
| 374 | exp-v1-rust-generation-0313 | RUST_STRATUM_REVIEW_18.md documents const getters, bit masks, reserved-bit preservation and range rejection. Criterion positive. |
| 375 | exp-v1-rust-generation-0314 | RUST_STRATUM_REVIEW_18.md documents bytewise wrapping fingerprint and canonical string equality with fixed vectors. Criterion positive; not a cryptographic-security claim. |

Cumulative375/942:150 new holds,225 scoped positives;176 first-time Rust repairs.
Outside unique coverage4975; corpus holds2296; sample165/135 unchanged.
Continue initially unheld376. GCS through360; this batch awaits backup.

Continuation2026-09-08: initially unheld376–390. Eight full fresh repair
inspections and generation0318/0322 prompt/reference rereads; other generation
rows reconcile cited notes. Eight holds and seven scoped positives.
One new pinned Rust1.85.0 probe compiled then failed without timeout:1577ms,
network disabled,1CPU,512MiB,64PIDs,60s. Complete original and diagnostic task,
reference, hashes, runtime identity and raw output preserved in result JSON.

| Unheld position | Candidate ID | Criterion finding |
| --- | --- | --- |
| 376 | exp-v1-rust-generation-0315 | RUST_STRATUM_REVIEW_18.md documents trimmed ASCII commands and permanent closure. Criterion positive; already-closed batch response cardinality remains ambiguous. |
| 377 | exp-v1-rust-generation-0317 | RUST_STRATUM_REVIEW_18.md documents final marker, exact suffixes, ASCII numeric grammar, bounded endpoints and inclusive range. Criterion positive. |
| 378 | exp-v1-rust-generation-0318 | Non-triviality hold: two literal signal mappings and ordinary signed integer to_string wrapper. |
| 379 | exp-v1-rust-repair-0209 | Fresh full repair inspection: release callback must precede notice for dequeued FIFO packet while terminal/empty behavior and replacement callbacks remain correct. Criterion positive. |
| 380 | exp-v1-rust-repair-0210 | Fresh full repair inspection: validate complete catalog, including skipped historical entries, before appending either ledger or audit records. Criterion positive. |
| 381 | exp-v1-rust-repair-0211 | Non-triviality hold: apply explicitly requested ASCII lowercasing before direct command dispatch; parsing/arity and elapsed-time rendering unchanged. |
| 382 | exp-v1-rust-repair-0212 | Non-triviality hold: substitute locator for label in explicitly locator-based duplicate check; trimming, stored text and module tuple handling unchanged. |
| 383 | exp-v1-rust-generation-0322 | Static numeric hold: 500000000 ASCII9 digits each contribute9 under both checksum parities, so sum4500000000 exceeds u32. Unrestricted input has no length cap; debug overflow or wrapped release sum invalidates correctness. No large allocation or execution claimed. |
| 384 | exp-v1-rust-generation-0324 | RUST_STRATUM_REVIEW_19.md documents endpoint preservation, status boundaries, both markers and Unicode scalar length. Criterion positive; ModuleInfo signatures and description remain underspecified. |
| 385 | exp-v1-rust-repair-0213 | Non-triviality hold: correct one literal anti-diagonal coordinate in a fixed4x4 table; win-line selection unchanged. Public helper length beyond8 is not specified and remains unresolved. |
| 386 | exp-v1-rust-repair-0214 | Non-triviality hold: replace clear-all with direct matching-index removal from a unique flat child list. Factory-only wording versus public Clone and source-defined owner panic remain unresolved API issues. |
| 387 | exp-v1-rust-repair-0215 | Executed contract hold: construct1x1 buffer, set public width2, put_pixel(1,0) panics with slice end8 beyond length4 despite never-panics promise. rust-repair0215-public-width-result.json: compile0/test101,1577ms,no timeout. No private-field manipulation. |
| 388 | exp-v1-rust-repair-0216 | Non-triviality hold: swap two explicitly ordered fields in snapshot tuple; unrelated generic formatting/addition wrappers unchanged. |
| 389 | exp-v1-rust-generation-0325 | RUST_STRATUM_REVIEW_19.md documents exact descriptor API, first-equals parsing, duplicate/unknown/empty-field rejection and nonmutation. Criterion positive. |
| 390 | exp-v1-rust-generation-0326 | RUST_STRATUM_REVIEW_19.md documents endpoint character/dot rules, ordered unique inserts and atomic rejection/removal. Criterion positive. |

Batch13 total17 holds,13 scoped positives. Cumulative390/942:158 new holds,
232 scoped positives;184 first-time Rust repairs; outside unique coverage4983.
Corpus holds2304; sample165/135 unchanged. Continue initially unheld391.
GCS through360; positions361–390 and new canvas probe await backup.
Original5885 unchanged; no training admission.

