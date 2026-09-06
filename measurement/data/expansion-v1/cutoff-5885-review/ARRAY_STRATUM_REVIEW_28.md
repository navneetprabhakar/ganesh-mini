# Array-validation follow-up, batch 28

Positions 406–420: 15 new / 428 unique outside-sample inspections. Ten new
holds: **292 additive / 295 including historical three**. Full prompts,
references and original tests inspected, including rereading the initially
truncated Pulse test. No duplicate holds added.

| Position | Candidate | Scoped finding |
| --- | --- | --- |
| 406 | TS repair0175 | Required curator name lost in spread copy. archive-required-curator-name-result.json, 2544 ms. |
| 407 | TS repair0173 | Elapsed 2^-54 with duration 1 incorrectly returns x=1 rather than 2^-54. pulse-small-elapsed-result.json, 2636 ms. Missing tuple slots and overflowing interpolation remain additional static concerns only. |
| 408 | JS generation0326 | Missing replacement entry accepted. warehouse-missing-replacement-result.json, 435 ms. Unchanged object identity explicitly permitted. |
| 409 | JS generation0329 | Required label lost from GET copy. directory-required-label-result.json, 443 ms. for-of later catches sparse records; no sparse hold inferred. |
| 410 | JS repair0217 | Internally dense parsed bytes, exact length and checksum; odd-length guard complements regex. No new hold. |
| 411 | JS repair0220 | for-of validates panels; fresh stable sorted wrapper list. Fractional widths in the gaps between stated intervals need oracle clarification; no new hold. |
| 412 | JS generation0327 | Required displayName lost from selected copy. member-page-required-display-name-result.json, 339 ms. |
| 413 | TS generation0266 | Missing tag accepted. record-shelf-missing-tag-result.json, 2098 ms. |
| 414 | TS repair0177 | Dense five-value safe integer validation, bounded subtraction and fresh geometry. No new hold. |
| 415 | TS repair0178 | Missing numeric value accepted. status-panel-missing-value-result.json, 2475 ms. |
| 416 | TS repair0179 | Required done=false lost from stored copy. work-archive-required-done-result.json, 2468 ms. |
| 417 | TS generation0267 | Uses round where prompt explicitly requires floor. Original test also expects incorrect 5-column distribution. cell-canvas-floor-fill-result.json, 2339 ms. |
| 418 | JS repair0221 | Trailing-newline hypothesis disproved by executed probe: TypeError was correctly thrown. version-trailing-newline-result.json, exit 0, 434 ms. No new hold. |
| 419 | JS generation0331 | Artificial one-job-per-worker restriction leaves a fitting second job unassigned. Original test's j4 expectation also contradicts remaining-capacity rule. workloads-remaining-capacity-result.json, 411 ms. |
| 420 | JS generation0342 | for-of shape/flag checks, exactly-one-active invariant and explicit copies. Exact relevant-fields wording does not unambiguously require rejecting extras. No new hold. |

Ten counterexamples failed without timeout in pinned network-disabled/resource-
limited sandboxes; the newline rejection probe passed. Negative findings are
not seven-criterion approvals. Frozen data/sample/partition unchanged; no
training seal or new VM. Scope v6 unchanged. GCS verified through 285 holds;
this batch awaits backup. Continue position 421 of 544 outside-sample array hits.
