# Array-validation follow-up, batch 13

2026-09-06. Positions 181–195 inspected against prompts, references and original
tests: 15 new / 204 unique outside-sample targeted inspections. Ten newly held
records: **156 additive / 159 including historical three**. Frozen 300 unchanged;
inspection is not seven-criterion approval.

| ID suffix | Finding | Result |
| --- | --- | --- |
| typescript-generation-0122 | Required minute lost in copied climate reading. | climate-hidden-minute-result.json |
| typescript-repair-0081 | Required widget ID lost in copied record. | widget-hidden-id-result.json |
| typescript-repair-0083 | Valid own __proto__ tab stack lost during object storage. | tab-stack-proto-key-result.json |
| typescript-generation-0123 | Required exchange ID lost during report transformation. | exchange-report-hidden-id-result.json |
| javascript-generation-0147 | Missing delta bypasses safe-integer validation. | capacity-deltas-sparse-result.json |
| javascript-generation-0148 | Missing choice bypasses string validation. | selection-choices-sparse-result.json |
| javascript-generation-0149 | Missing path segment accepted instead of rejected. | scalar-path-sparse-result.json |
| javascript-generation-0150 | Missing service order bypasses record validation. | service-orders-sparse-result.json |
| javascript-repair-0099 | Missing embed request bypasses record validation. | embed-requests-sparse-result.json |
| typescript-generation-0127 | Required validated entitlement status lost during copy. | entitlement-hidden-status-result.json |

Ten reproduced failures, no timeouts, in pinned network-disabled/resource-limited
sandboxes. JS exits `[1]`; TS compilation passes before behavioral failure.
Copy probes retain valid required own properties with non-enumerable descriptors.
Tab input is an ordinary JSON-parsed object; no prototype mutation is requested.
Original tests omit these boundary cases.

Scoped negative findings and remaining questions:

- TS generation0124 QueueWeave mutates track identity as explicitly required and
  returns a separate snapshot. Sparse typed input policy and enormous splice
  argument limits are unresolved, not counted as reproduced failures.
- TS generation0126 openCatalog validates tables and columns with for-of before
  field-by-field copying. Direct CatalogDatabase constructor validation is not
  specified like openCatalog validation; no extra obligation is inferred.
- JS generation0146 renderScoreTable validates all records with for-of before
  sorting/mapping; required fields read directly rather than lost in spread.
- JS repair0097 toggleSection validates for-of and constructs explicit fields.
- TS generation0129 renderArtifactDetails maps a fixed five-row array. Numeric
  display of very large integers needs clarity about exponent notation; no
  executed defect is claimed.
- Climate Fahrenheit conversion has an explicit arithmetic expression; overflow
  from that prescribed expression is not automatically a new numeric defect.
- Exchange elapsed difference beyond representable range remains a distinct
  numeric-domain question, not the required-field-copy diagnostic.
- Scalar projection numeric-key insertion order is a contract-clarity issue;
  its confirmed hold is malformed path validation only.

Continue position 196. No revised partition, training seal, generation restart
or new VM. GCS checkpoint verified through 149 holds; this batch awaits backup.
