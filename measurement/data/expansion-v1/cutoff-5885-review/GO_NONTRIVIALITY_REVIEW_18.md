# Go focused non-triviality review — batch 18

Positions256–270, full prompt/reference read; not a full new test/mutant review.
Ten criterion-positive, five non-triviality holds plus two contract/behavior holds.
1263 total holds (1260 additive+3),3200 unique outside inspections. Resume271.

| Position | ID | Finding |
| --- | --- | --- |
| 256 | exp-v1-go-repair-0142 | Non-triviality hold: direct ascending library sort replaces reverse sort. |
| 257 | exp-v1-go-repair-0144 | Non-triviality hold: direct final-digit parity literal correction. |
| 258 | exp-v1-go-generation-0217 | Criterion-positive: Unicode code-point/category validation, original account preservation and validate-before-secret replacement. This toy credential record is not production security guidance. |
| 259 | exp-v1-go-generation-0218 | Criterion-positive state machine; static contract hold: RequestRemoval excludes removal-pending although removal is specified from any non-removed state. Clarify that boundary rather than assume an exception. |
| 260 | exp-v1-go-generation-0219 | Criterion-positive: bounds/value invariant must survive both value and bounds updates, with embedded specialization. |
| 261 | exp-v1-go-generation-0220 | Criterion-positive: exactly one audit/metric per operation including failures, while workspace mutation remains transactional. Unspecified action labels and empty slice shapes are not all-seven-approved here. |
| 262 | exp-v1-go-generation-0221 | Non-triviality hold: direct fixed hourly formulas, scalar setters and one threshold bonus. |
| 263 | exp-v1-go-repair-0147 | Criterion-positive: independent string storage is expressly required, so correction includes strings.Clone beyond filtering empty labels. |
| 264 | exp-v1-go-repair-0148 | Non-triviality hold: direct Add-to-Mul substitution in already supplied exact rational parser/arithmetic. |
| 265 | exp-v1-go-generation-0224 | Non-triviality hold: prescribed scalar field projection and direct endpoint-host extraction. |
| 266 | exp-v1-go-generation-0225 | Criterion-positive: rolling non-empty maximum-subarray invariant with all-negative initialization and constant auxiliary space. |
| 267 | exp-v1-go-generation-0226 | Criterion-positive: set-once publication and atomic reset coordinated under locks across readers/writers. |
| 268 | exp-v1-go-generation-0227 | Criterion-positive: mutable metadata ownership must be detached in both directions while preserving nil/non-nil empty maps. |
| 269 | exp-v1-go-generation-0228 | Criterion-positive graph validation/ownership; executed framing hold because parent strings and edit fields lack an unambiguous group boundary. |
| 270 | exp-v1-go-repair-0149 | Criterion-positive: trailing-run finalization must apply the same run encoder as internal runs, preserving untouched non-space bytes. |

go_0228_revision_framing_probe-result.json: Go1.22.12 exit[1], no timeout,
27931ms. Two independently constructed public graphs create identical genesis and
two prior revisions. A revision with three parents/no edits and a revision with
one parent/one edit (the other two digests as path/content) receive identical
digests. Static encoding inspection shows identical serialized bytes due to absent
parent/edit counts. This is structural framing ambiguity, NOT a SHA-256 collision
discovery. No private fields or helpers were invoked by the diagnostic.
Additive test ran alongside original tests, not a separate known-bad rerun.
Network off,1CPU/512MiB/64PIDs/60s; task, code and output hashes retained.
Candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
