# Array-validation follow-up, final batch 36

Positions 526–544 complete the fixed 544-position queue. Nineteen positions,
eighteen new unique inspections (536 was initially inspected), twelve new holds.
Total: 549 unique outside-sample inspections; 379 additive plus historical three
= 382 holds. Full prompts, reference implementations and original tests read.

| Position | TS candidate | Scoped finding |
| --- | --- | --- |
| 526 | repair0244 | Missing link accepted; workspace-frame-missing-link-result.json. |
| 527 | generation0370 | Whole-array validation, explicit field copies, fiscal years 2000–9999. No new hold. |
| 528 | repair0247 | Primitive inputs and private dense storage. Blank lookup policy ambiguous; no new hold. |
| 529 | generation0368 | Gregorian 0099 date rejected; workshop-early-year-result.json. |
| 530 | generation0378 | Two-pass validation before group assignments; private scalar records. No new hold. |
| 531 | repair0251 | Validation before ID consumption; private boards, copied notes. No new hold. |
| 532 | generation0384 | Required userId lost; credentials-required-userid-result.json. |
| 533 | generation0379 | Required streamKey lost; audio-required-stream-result.json. |
| 534 | generation0380 | Required units lost, NaN totals; invoice-book-required-units-result.json. |
| 535 | generation0381 | Inherited constructor returned for missing setting; configuration-inherited-lookup-result.json. |
| 536 | generation0383 | Already initially inspected and held; no duplicate count. |
| 537 | repair0255 | Extra caller id overrides generated ID; member-input-id-override-result.json. |
| 538 | repair0256 | Whole-array validation. Backslash-in-key escape wording ambiguous; original test expects it unchanged. No new hold. |
| 539 | generation0386 | Exact prescribed geometry formulas; finite output not required. Approximation helper accepts NaN, a static oracle weakness, not a reproduced reference defect. No new hold. |
| 540 | generation0387 | Required label lost; warehouse-bin-required-label-result.json. |
| 541 | generation0388 | Required ownerCode lost; device-required-owner-result.json. |
| 542 | generation0389 | Required note body lost; note-event-required-body-result.json. |
| 543 | repair0257 | Required code lost; supply-lot-required-code-result.json. |
| 544 | repair0259 | Missing contact skipped; contact-strip-missing-contact-result.json. |

All twelve diagnostics compiled and failed at runtime [0,0,1], without timeout,
in pinned network-disabled/resource-limited sandboxes. The object-copy probes
use valid typed records with nonenumerable required fields, not opaque metadata.
No-hold inspections do not constitute seven-criterion admission approval.

Deduplication: initial ten + 544 queue positions minus five initial overlaps
(42, 298, 437, 453, 536) = 549 unique outside-sample inspections. Frozen 300
sample remains separate. Scope v6 remains 11 groups / 14 strata / 3,085 review
records, not a rejection count. Other systematic strata and quality criteria
remain pending. No training seal or new VM. GCS verified through 370 holds;
this final batch awaits backup.
