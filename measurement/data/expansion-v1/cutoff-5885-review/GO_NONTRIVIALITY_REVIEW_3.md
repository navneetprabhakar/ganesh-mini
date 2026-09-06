# Go focused non-triviality review — batch 3

Positions 31–45 of the preserved 757-record Go queue: full prompt/reference
read, not a new full test/mutant review. Ten criterion-positive, five elementary
target holds. Two additional contract/behavior holds: seven new corpus holds,
1174 total (1171 additive plus three historical), 2975 unique outside-sample
inspections. Sample decisions remain 170 positive/130 held. No admission seal.

| Position | ID | Finding |
| --- | --- | --- |
| 31 | exp-v1-go-repair-0015 | Criterion-positive: complete unsigned version grammar and major/minor interval precedence. |
| 32 | exp-v1-go-repair-0016 | Non-triviality hold: remove the explicit blank-line filter in a direct prefix-filter loop. |
| 33 | exp-v1-go-generation-0026 | Criterion-positive: normalized distinct codes, checked total and sorted independent output. |
| 34 | exp-v1-go-generation-0027 | Criterion-positive task, behavioral hold: finite opposite endpoints produce +Inf instead of representable zero midpoint. |
| 35 | exp-v1-go-generation-0028 | Criterion-positive stateful allocation; static API contradiction: Snapshot signature returns only map but all non-Count methods are required to return an error on nil receiver. |
| 36 | exp-v1-go-generation-0029 | Criterion-positive: normalized labels, duplicate constructor rejection and deep product copies. Zero-value initialization is not separately promised. |
| 37 | exp-v1-go-generation-0030 | Criterion-positive: conditional ordered segments, compact path and marker selection. Validation-before-compaction versus final displayed text remains outside this focused approval. |
| 38 | exp-v1-go-repair-0017 | Non-triviality hold: direct comparison reversal in elementary nearest-negative/positive scan. |
| 39 | exp-v1-go-repair-0018 | Non-triviality hold: replace reverse sort with ordinary sort in direct dictionary expansion. |
| 40 | exp-v1-go-repair-0019 | Non-triviality hold: expressly specified one-based position in elementary checksum loop. |
| 41 | exp-v1-go-repair-0020 | Non-triviality hold: independent allocation/copy in elementary clamping loop; no runtime defect asserted. |
| 42 | exp-v1-go-generation-0031 | Criterion-positive: bounded ordered prefix selection across distinct typed fields using reusable generic selector. Fixed data is expressly implementation-chosen; tests not re-adjudicated here. |
| 43 | exp-v1-go-generation-0032 | Criterion-positive: SHA/endian key construction and locked copied response state. No zero-value or concurrent caller-buffer-mutation guarantee invented. |
| 44 | exp-v1-go-generation-0033 | Criterion-positive: validation-atomic nested permission ownership and ordered registry. Simultaneously invalid replacement/missing key error precedence not re-adjudicated. |
| 45 | exp-v1-go-generation-0034 | Criterion-positive: layered typed configuration and zero-on-error. Normalized override-key collision order remains a possible contract question, not an executed finding. |

go_0027_finite_interpolation_probe-result.json: pinned Go 1.22.12, network off,
1 CPU/512 MiB/64 PIDs/60 seconds, exit [1], no timeout, 26919 ms. The added
review_test.go runs alongside original tests. Exact observed midpoint +Inf,
nil error; expected zero for endpoints -1e308/+1e308 at minutes 0/2 and query1.
Receipt preserves original task, additive diagnostic task, code/output and hashes.
No separate original-only/known-bad rerun. Frozen candidate SHA:
680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

Resume Go queue position46. Latest work postdates sample-closure GCS backup.
