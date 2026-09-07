# Go focused non-triviality review — batch 35

Positions511–525, full prompt/reference read; not a full new test/mutant review.
13 criterion-positive, two non-triviality holds plus one static behavioral hold.
1365 total holds (1362 additive+3),3455 unique outside inspections. Resume526.

| Position | ID | Finding |
| --- | --- | --- |
| 511 | exp-v1-go-generation-0439 | Criterion-positive concurrent reconciler; static behavioral hold: delimiter-joined namespace/name key is not injective for valid embedded-NUL identifiers. |
| 512 | exp-v1-go-generation-0441 | Criterion-positive: layered shadowing must distinguish absent from local nil data; immutable parent link, unlocked recursive fallback and defensive copies. |
| 513 | exp-v1-go-generation-0442 | Criterion-positive: preserve selected order/duplicates, sort a copied all-results slice and suppress partial reports while returning source error identity. |
| 514 | exp-v1-go-generation-0443 | Criterion-positive: copy request before goroutine launch, detached response and buffered channel/completion lifecycle. |
| 515 | exp-v1-go-generation-0444 | Criterion-positive: deterministic greatest-original-key precedence after folding, missing-versus-empty values and signed/unsigned parse fallbacks. |
| 516 | exp-v1-go-repair-0293 | Criterion-positive: normalize negative residue before overflow-safe modular addition; full-int bounds maintained. |
| 517 | exp-v1-go-repair-0295 | Criterion-positive: per-row ceiling carry and final count overflow checks without constructing overflowing row sums. |
| 518 | exp-v1-go-repair-0296 | Criterion-positive: folded alphabet is a set, so duplicate members cannot multiply each text rune's contribution. |
| 519 | exp-v1-go-generation-0445 | Criterion-positive: odd/even Manacher radii with mirrored bounds, earliest-offset ties and no sentinel reservation. |
| 520 | exp-v1-go-generation-0447 | Non-triviality hold: fixed errors.Is classification table and direct contextual error formatting/unwrapping wrapper. |
| 521 | exp-v1-go-generation-0448 | Criterion-positive: immutable ordered page catalog, path uniqueness/validation and standard HTML escaping. |
| 522 | exp-v1-go-generation-0449 | Criterion-positive: preorder first-error traversal with independent index path; hierarchy assumption does not imply an added cyclic-graph contract. |
| 523 | exp-v1-go-generation-0450 | Criterion-positive: bounded binary lengths, copied payloads, first-match removal clearing and multiplicity-aware containment. |
| 524 | exp-v1-go-repair-0297 | Non-triviality hold: direct lowercase alphabet endpoint literal correction. |
| 525 | exp-v1-go-repair-0298 | Criterion-positive: bounded worker pool, index-stable outputs and wait/close lifecycle. Empty-input versus invalid-configuration precedence is not newly adjudicated. |

Static review only. generation0439: with watch="" and leader=true, records
(namespace="a",name="b\\x00c") and (namespace="a\\x00b",name="c") produce the
same key and overwrite each other. No rule prohibits embedded NUL identifiers.
The escape notation denotes a NUL byte; no new execution is claimed.
Frozen candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

