# Rust elementary-target reconciliation — batch 12

2026-09-08. Initially unheld331–345: eight holds and seven scoped positives.
Ten fresh complete repair inspections; generation0282/0285 prompt/reference
rereads; remaining generation reconciles cited prior full notes.
Two diagnostic probes executed in pinned Rust1.85.0, network disabled,1CPU,
512MiB,64PIDs,60s limit. Both compiled and failed assertions without timeout.
Original tasks/references, probe tasks, hashes, image identity and output saved
in the respective result JSON. Original corpus unchanged; no training admission.

| Unheld position | Candidate ID | Criterion finding |
| --- | --- | --- |
| 331 | exp-v1-rust-repair-0181 | Executed contract hold: valid MIN_POSITIVE camera, unit texture/depth produces origin0.0 outside promised [-1,0). Literal rem_euclid formula and strict interval conflict at rounding boundary. Probe rust-repair0181-half-open-origin-result.json: compile0/test101,1476ms, no timeout. |
| 332 | exp-v1-rust-repair-0183 | Non-triviality hold: swap two explicitly prescribed yes/no Boolean literals; parsing, line errors and rendering unchanged. |
| 333 | exp-v1-rust-repair-0184 | Non-triviality hold: replace upper-bound min with explicitly specified max in elementary paired extrema update; locking, poison recovery and snapshot machinery unchanged. Poison behavior not newly executed. |
| 334 | exp-v1-rust-generation-0278 | RUST_STRATUM_REVIEW_16.md documents capability-gated trait shape and generic Copy blanket implementation. Criterion positive; same-crate harness does not certify downstream privacy. |
| 335 | exp-v1-rust-generation-0282 | Non-triviality hold: direct transcription of four ordered empty/equality checks and fixed result variants; no session or interacting state. |
| 336 | exp-v1-rust-repair-0185 | Non-triviality hold: replace true assignment with a single Boolean toggle; fixed appearance accessors and rendering unchanged. |
| 337 | exp-v1-rust-repair-0186 | Executed numeric hold: finite MAX sigma returns density0 at x0 because normalization denominator overflows, although reordered expression yields representable positive2.219190097936194e-309. Probe rust-repair0186-large-sigma-result.json: compile0/test101,1357ms, no timeout. |
| 338 | exp-v1-rust-repair-0187 | Fresh full repair inspection: preserve_required must override all_optional consistently for explicit null and absent endpoints while retaining parse errors/defaults. Criterion positive. |
| 339 | exp-v1-rust-repair-0188 | Fresh full repair inspection: validate rename before mutation after key resolution, preserving all other catalog fields and exact slug behavior. Criterion positive; trimming is validation, not mandatory stored normalization. |
| 340 | exp-v1-rust-generation-0285 | Non-triviality hold: fixed seven-line formatting with direct enum/Boolean literal mapping and bounded hexadecimal formatting. |
| 341 | exp-v1-rust-generation-0287 | RUST_STRATUM_REVIEW_17.md documents validated registration and owned sorted snapshots. Criterion positive; invalid apply identifier/error precedence remains unresolved. |
| 342 | exp-v1-rust-generation-0288 | RUST_STRATUM_REVIEW_17.md documents checked adjustment before mutation and owned lexicographic output. Criterion positive. |
| 343 | exp-v1-rust-repair-0190 | Fresh full repair inspection: selector uniqueness tracks keys, not repeated values, while preserving input order and all-or-nothing parsing. Criterion positive; no extra escaping grammar imposed. |
| 344 | exp-v1-rust-repair-0191 | Fresh full repair inspection: compare-exchange retry must saturate before decrement without wrapped storage and preserve linearizable returned values under contention. Criterion positive; original concurrency tests inspected, not rerun. |
| 345 | exp-v1-rust-repair-0192 | Clarity hold: prose ignores blank/all-blank lines, but tests explicitly reject whitespace-only lines while reference skips only empty lines. Non-triviality concern also applies to deleting final reverse from ordered parser. No executed failure claimed. |

Cumulative345/942:135 new holds,210 scoped positives;160 first-time Rust repairs.
Outside unique coverage4959; corpus holds2281; frozen sample165/135 unchanged.
Continue initially unheld346. GCS through330; this batch and two probes await backup.

Continuation2026-09-08: initially unheld346–360. Nine fresh complete repair
inspections and generation0304 prompt/reference reread; other generation rows
reconcile cited full prior notes. Six holds and nine scoped positives; no new
execution. API/oracle issues explicitly remain open where noted.

| Unheld position | Candidate ID | Criterion finding |
| --- | --- | --- |
| 346 | exp-v1-rust-repair-0189 | Fresh full repair inspection: sliding rays stop at either side's occupied square, allow only opposing capture and preserve sorted legal moves and atomic application. Criterion positive. |
| 347 | exp-v1-rust-repair-0193 | Fresh full repair inspection: defer ticket consumption until every job and cumulative cost validates, committing dispatcher and signal together. Criterion positive; private ticket exhaustion and cost-overflow oracle coverage remain unresolved. |
| 348 | exp-v1-rust-repair-0194 | Non-triviality hold: swap explicitly named actual/expected fields in the mismatch constructor; hashing, owned snapshot and iterator cursor unchanged. |
| 349 | exp-v1-rust-repair-0195 | Non-triviality hold: directly prescribed fully qualified trait-call substitution. Known-bad generic body also lacks Display bound required by its free call, so behavioral-only mutant qualification remains unresolved. |
| 350 | exp-v1-rust-repair-0196 | Non-triviality hold: replace lowercase conversion with directly prescribed clone; case-insensitive key matching, duplicate ambiguity and debug logging unchanged. |
| 351 | exp-v1-rust-generation-0295 | RUST_STRATUM_REVIEW_17.md documents maximum historical counts, saturating limits, bounded stop and consumed finish. Criterion positive. |
| 352 | exp-v1-rust-generation-0296 | RUST_STRATUM_REVIEW_17.md documents validation before per-record predicate, stable path deduplication and borrowed optional output. Criterion positive. |
| 353 | exp-v1-rust-generation-0299 | RUST_STRATUM_REVIEW_17.md documents cancellation precedence, owned unchanged identifiers and ordered duplicate chunks. Criterion positive. |
| 354 | exp-v1-rust-generation-0300 | RUST_STRATUM_REVIEW_17.md documents checked field slices, tag-offset policy errors, field-start truncation and exact trailing position. Criterion positive. |
| 355 | exp-v1-rust-repair-0197 | Non-triviality hold: change unconditional false to true after successful insertion; maximum-count guard and consuming wrapper remain unchanged. |
| 356 | exp-v1-rust-repair-0198 | Non-triviality hold: replace one index literal in the fully prescribed four-case edge-color table; validation and cloning unchanged. |
| 357 | exp-v1-rust-repair-0199 | Fresh full repair inspection: reject duplicate namespace before replacing the owned trait object, preserving original registration and subsequent shutdown behavior. Criterion positive; arbitrary stateful namespace accessors are not newly adjudicated. |
| 358 | exp-v1-rust-repair-0200 | Fresh full repair inspection: distinguish absent argument from present empty argument for flags, while typed options retain their separate missing/malformed paths. Criterion positive; whitespace-only name validation is stronger in source/tests than prose nonempty wording and remains unresolved. |
| 359 | exp-v1-rust-generation-0302 | RUST_STRATUM_REVIEW_18.md documents specified fingerprint, zero-secret precedence, ordered alias replacement and no mutation on errors. Criterion positive; public duplicate slots remain unresolved. |
| 360 | exp-v1-rust-generation-0304 | Non-triviality hold: fixed HTML scaffold and direct prescribed five-character escape mapping with one optional attribute; no parser or interacting state. No URL-safety claim inferred. |

Batch12 total14 holds,16 scoped positives. Cumulative360/942:141 new holds,
219 scoped positives;169 first-time Rust repairs, outside unique coverage4968.
Corpus holds2287; sample165/135 unchanged. Continue initially unheld361.
GCS through330; positions331–360 and two probes await backup. Originals unchanged.

