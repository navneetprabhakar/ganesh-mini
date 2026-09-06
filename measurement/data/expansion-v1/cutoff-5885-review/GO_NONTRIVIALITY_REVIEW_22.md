# Go focused non-triviality review — batch 22

Positions316–330, full prompt/reference read; not a full new test/mutant review.
11 criterion-positive, four non-triviality holds plus three behavioral holds.
1289 total holds (1286 additive+3),3260 unique outside inspections. Resume331.

| Position | ID | Finding |
| --- | --- | --- |
| 316 | exp-v1-go-generation-0268 | Criterion-positive: Unicode-aware lowercasing, output-level deduplication, code-mode eligibility and limit interact. |
| 317 | exp-v1-go-repair-0177 | Non-triviality hold: direct odd-versus-even middle-element condition correction. |
| 318 | exp-v1-go-repair-0179 | Non-triviality hold: direct omitted final-element repair in a supplied interleaving loop. |
| 319 | exp-v1-go-repair-0180 | Criterion-positive exact uint64 arithmetic; executed behavioral hold: remainder times 100 still overflows. |
| 320 | exp-v1-go-generation-0271 | Criterion-positive: validated sorted ledger with detached construction/query storage and inclusive cutoff. |
| 321 | exp-v1-go-generation-0273 | Criterion-positive: versioned status transitions, validation before mutation and sorted independent list. Constructor use is provided; zero-value usability not required. No astronomical update-count execution. |
| 322 | exp-v1-go-generation-0275 | Criterion-positive: ASCII identifier grammar, unrestricted-delete prevention and ordered parameter ownership. Nested argument deep copying is not required. |
| 323 | exp-v1-go-generation-0276 | Criterion-positive signed claims and temporal boundaries; executed behavioral hold: appended newline accepted outside specified base64url format. |
| 324 | exp-v1-go-repair-0182 | Criterion-positive: enforce bounded retained records without retaining dropped backing-array references; deep copies and zero capacity. |
| 325 | exp-v1-go-repair-0183 | Criterion-positive: signed digit counting must handle minimum int without negation. Sum-overflow policy not adjudicated here. |
| 326 | exp-v1-go-repair-0184 | Non-triviality hold: direct positive-only guard excludes zero from supplied sign partition. |
| 327 | exp-v1-go-generation-0277 | Criterion-positive: atomic load-or-create, empty-value presence, zero-value map initialization and detached concurrent snapshot. |
| 328 | exp-v1-go-generation-0278 | Non-triviality hold: direct division/remainder and elementary rectangle formulas. Ordinary Go int behavior expressly allowed, so no overflow defect claimed. |
| 329 | exp-v1-go-generation-0279 | Criterion-positive: locked expected-stage transition, terminal state and copied original ordering. |
| 330 | exp-v1-go-generation-0280 | Criterion-positive strict parser/error categories; executed behavioral hold: JSON null reaches semantic validation rather than malformed-object rejection. |

Executed additive probes, Go1.22.12 exit[1], no timeout:
- go_0180_uint64_percent_probe-result.json,28435ms: live=2^63,target=MaxUint64 returns1, expected99. Quotient decomposition does not protect remainder*100.
- go_0276_signature_newline_probe-result.json,28963ms: generated token plus newline verifies successfully, outside prescribed unpadded URL-safe alphabet.
- go_0280_null_shape_probe-result.json,27810ms: null returns ErrInvalidBadge rather than ErrMalformedBadge despite exactly-one-object contract.
Original tests retained. Network off,1CPU/512MiB/64PIDs/60s. Complete task,
code, runtime and output hashes in receipts. No new known-bad rerun claimed.
Frozen candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

