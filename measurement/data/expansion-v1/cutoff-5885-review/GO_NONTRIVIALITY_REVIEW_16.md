# Go focused non-triviality review — batch 16

Positions226–240, full prompt/reference read; not a full new test/mutant review.
Thirteen criterion-positive, two non-triviality holds plus two behavioral holds.
1250 total holds (1247 additive+3),3170 unique outside inspections. Resume241.

| Position | ID | Finding |
| --- | --- | --- |
| 226 | exp-v1-go-generation-0191 | Criterion-positive: context-aware permit acquisition, serialized delegation, deferred permit release and output ownership. Simultaneously ready cancellation/permit selection is not adjudicated by this focused pass. |
| 227 | exp-v1-go-generation-0193 | Criterion-positive: foreign-key ownership, selected zero values and validate-before-commit union of update columns. |
| 228 | exp-v1-go-generation-0194 | Criterion-positive: relative path validation, prescribed joined key identity and byte ownership. Different component splits sharing a joined key are expressly the same key, not an invented tuple collision. |
| 229 | exp-v1-go-generation-0195 | Criterion-positive authorized patch/side effects; executed behavioral hold for accepting an unknown capitalized JSON key. |
| 230 | exp-v1-go-generation-0197 | Criterion-positive: validated zero input identity, assigned IDs and sequence/ID ordered detached views. No feasible ID-exhaustion execution. |
| 231 | exp-v1-go-repair-0129 | Criterion-positive: zero-width fields still align while consuming no width, with checked padding and addition. |
| 232 | exp-v1-go-repair-0130 | Non-triviality hold: direct optional-zero guard in already supplied scalar validation. |
| 233 | exp-v1-go-repair-0131 | Criterion-positive: token/rank association must move together during stable sorting, beyond reversing the comparator. |
| 234 | exp-v1-go-generation-0199 | Criterion-positive: byte escape framing, nibble parsing, incomplete/error handling and detached buffers. Decoder does not promise canonical-only unescaped input. |
| 235 | exp-v1-go-generation-0200 | Criterion-positive: optimistic revisions, validation without trimming mutation and deep copies across CRUD. |
| 236 | exp-v1-go-generation-0201 | Criterion-positive: versioned ownership, filtered total and descending-primary/increasing-ID-tie pagination. Empty label filter semantics are not explicitly adjudicated here. |
| 237 | exp-v1-go-generation-0202 | Criterion-positive: generation changes including no-op updates, stop/remove lifecycle and failure-preserving state. |
| 238 | exp-v1-go-generation-0203 | Criterion-positive: fresh sorted callback arguments each attempt, exact readiness membership and wrapped failure count. Astronomical attempt-counter exhaustion is not an executed finding. |
| 239 | exp-v1-go-generation-0204 | Criterion-positive checked generator state; executed behavioral hold because output allocation is based on requested count rather than the finite 41-value sequence. |
| 240 | exp-v1-go-repair-0133 | Non-triviality hold: direct reversal of subtraction operands. |

go_0195_exact_patch_keys_probe-result.json: Go1.22.12 exit[1], no timeout,
27988ms. A body containing capitalized Name is accepted and changes the card even
though the allowed keys are name,slug,title. The later state assertion was not reached.
go_0204_bounded_generator_probe-result.json: Go1.22.12 exit[1], no timeout,
27548ms. PowersOfThree(MaxInt) panics with makeslice cap out of range although the
specified exhausted result has only 41 uint64 powers. Panic caught by the test;
this is not a sandbox OOM or a requested enormous output.
Both additive tests ran alongside original tests, not separate known-bad reruns.
Network off,1CPU/512MiB/64PIDs/60s; task, code and output hashes retained.
Candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
