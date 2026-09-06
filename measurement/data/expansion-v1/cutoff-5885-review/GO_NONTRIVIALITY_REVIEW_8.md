# Go focused non-triviality review — batch 8

Positions106–120, full prompt/reference read; not a full new test/mutant review.
Nine criterion-positive, six non-triviality holds plus one behavioral hold.
1203 total holds (1200 additive+3),3050 unique outside inspections. Resume121.

| Position | ID | Finding |
| --- | --- | --- |
| 106 | exp-v1-go-repair-0054 | Criterion-positive: framed envelope parsing preserves checksum and XOR payload boundaries using three-part split. Educational encoding, not a security recommendation. |
| 107 | exp-v1-go-generation-0087 | Non-triviality hold: direct fixed fare switch over two fields. |
| 108 | exp-v1-go-generation-0088 | Criterion-positive: zero-value CRUD initialization, sorted IDs and mutation validation. Eventual int ID wrap/reuse is an unexecuted boundary concern, not a claimed feasible probe; no private state injection. |
| 109 | exp-v1-go-generation-0089 | Non-triviality hold: direct bounded integer validation and conversion. |
| 110 | exp-v1-go-repair-0057 | Criterion-positive: explicit shared variable capture replaced with iteration-local ownership. This is not a claim about pre-Go1.22 implicit loop-variable semantics. |
| 111 | exp-v1-go-repair-0058 | Non-triviality hold: direct negated-boolean filter correction. |
| 112 | exp-v1-go-repair-0060 | Non-triviality hold: direct i to i*i correction in running totals. |
| 113 | exp-v1-go-generation-0091 | Criterion-positive: strict JSON unknown/trailing checks and normalized nil collection shapes. Non-JSON NaN is not an admitted JSON input. |
| 114 | exp-v1-go-generation-0092 | Criterion-positive: first-position/last-value duplicate semantics and URL query construction. Malformed existing query policy is unspecified, not a new executed failure. |
| 115 | exp-v1-go-generation-0093 | Criterion-positive: nil-safe clause collection, ordered removal and quoted serialization. |
| 116 | exp-v1-go-generation-0094 | Criterion-positive: nested map/slice/pointer deep-copy ownership and nil-versus-empty preservation. SecretLink fields are unspecified; reference adds Namespace/Name, but inspected original tests only require an empty SecretLink and pointer independence. No missing-field test failure established, so no API hold on that basis. Self-copy aliasing is not expressly promised. |
| 117 | exp-v1-go-generation-0095 | Criterion-positive: synchronized timestamp/sequence state with failure atomicity; executed behavioral hold for signed delta overflow bypassing the 41-bit limit. |
| 118 | exp-v1-go-generation-0096 | Non-triviality hold: direct three-field enrollment validation predicates. |
| 119 | exp-v1-go-repair-0061 | Non-triviality hold: apply supplied ASCII-fold helper to both endpoint comparisons. |
| 120 | exp-v1-go-repair-0062 | Criterion-positive: signed division/remainder correction implements floor buckets for negative readings; positive divisor excludes MinInt/-1 division. |

go_0095_delta_overflow_probe-result.json: Go1.22.12 exit[1], no timeout,
26690ms. Public constructor epoch MinInt64 then Next(MaxInt64) accepts a delta
larger than 41 bits and returns 18446744073705357313 with nil error. The probe's
later valid-call assertion was not reached. No private-field mutation involved.
Additive test ran alongside original tests, not a separate known-bad rerun.
Network off,1CPU/512MiB/64PIDs/60s; task, code and output hashes retained.
Candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
