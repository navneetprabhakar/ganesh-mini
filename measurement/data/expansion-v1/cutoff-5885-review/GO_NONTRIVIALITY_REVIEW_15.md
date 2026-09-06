# Go focused non-triviality review — batch 15

Positions211–225, full prompt/reference read; not a full new test/mutant review.
Nine criterion-positive, six non-triviality holds plus one static contract hold.
1246 total holds (1243 additive+3),3155 unique outside inspections. Resume226.

| Position | ID | Finding |
| --- | --- | --- |
| 211 | exp-v1-go-repair-0117 | Criterion-positive: balanced parser must reject a negative-depth prefix, not merely require final zero depth. |
| 212 | exp-v1-go-repair-0118 | Criterion-positive: missing sorted compaction requires maintaining distinct read/write positions on an independent buffer. |
| 213 | exp-v1-go-repair-0119 | Non-triviality hold: disclosed upper-bound literal replacement. |
| 214 | exp-v1-go-generation-0181 | Criterion-positive: byte ownership, nil shape and identity/content round-trip checks. Global duplicate precedence versus first input error remains outside focused approval. |
| 215 | exp-v1-go-generation-0182 | Non-triviality hold: direct arithmetic summary and zero-divisor guard. |
| 216 | exp-v1-go-generation-0183 | Criterion-positive: first equal attribute removal, nil-aware byte equality and nested snapshot ownership with ordered groups. |
| 217 | exp-v1-go-generation-0184 | Criterion-positive: validate before filtering, severity ordering and stable independent event history. |
| 218 | exp-v1-go-generation-0185 | Non-triviality hold: fixed two-channel value configuration with direct scalar setter and range guard. |
| 219 | exp-v1-go-repair-0123 | Criterion-positive: parser separates only the first equals sign so remaining value content survives; malformed fields produce no partial result. |
| 220 | exp-v1-go-repair-0124 | Non-triviality hold: direct square factor replacement in supplied recurrence. No unbounded recursion performance execution. |
| 221 | exp-v1-go-generation-0186 | Criterion-positive: filter validation precedes data inspection, optional bounds and OR/AND criteria combine with nil-preserving nested copies. |
| 222 | exp-v1-go-generation-0189 | Criterion-positive authentication flow; static contract hold: duplicates in credentials are prohibited, but the implementation detects duplicates only for the requested name. |
| 223 | exp-v1-go-generation-0190 | Criterion-positive: transcript protocol distinguishes exit-triggered termination from exhausted-input final prompt without examining later commands. |
| 224 | exp-v1-go-repair-0127 | Non-triviality hold: direct sender-versus-login assignment correction. |
| 225 | exp-v1-go-repair-0128 | Non-triviality hold: remove extraneous factor two around the already supplied full-range gap helper. |

No new candidate execution. Static generation0189 example: a valid requested
svc_a credential plus two other credentials both named svc_b. The specification
says duplicates in credentials return nil; the loop ignores both svc_b rows and
can authenticate svc_a. The separate matching-name duplicate sentence does not
expressly exempt nonmatching duplicates. No executed failure is claimed here.
Candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
