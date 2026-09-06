# Array-validation follow-up, batch 20

Completed positions 286–300: 14 new / 308 unique outside-sample inspections.
Six new holds: **220 additive / 223 including historical three**.
TS generation0195 was already inspected and held in TARGETED_STRATUM_REVIEW.md;
its repeated diagnostic below is corroborating evidence, not another hold or
unique inspection. The pre-backup uniqueness check caught the duplicate; no
224-hold archive was created.

| ID suffix | Finding | Result prefix |
| --- | --- | --- |
| typescript-generation-0189 | Large valid integer duration has incorrect minutes and scientific-notation hours. | remaining-large-integer-format |
| typescript-generation-0190 | Unique ID promise conflicts with mandated base/suffix scheme for A, A, A-2. | generated-label-id-collision |
| javascript-generation-0220 | Forbidden own id key bypasses changes validation when non-enumerable. | archive-hidden-forbidden-key |
| javascript-repair-0150 | Accepts non-plain metrics objects despite plain-object contract. | viewport-nonplain-record |
| typescript-generation-0195 | Unsubscribing later duplicate callback removes first registration and changes delivery order. | workshop-subscription-identity |
| typescript-generation-0196 | Missing fetched category bypasses validation and is cached. | category-cache-missing-entry |
| typescript-repair-0129 | Record with missing tag is returned rather than ignored. | sticker-missing-tag |

All result prefixes refer to sibling -result.json files. All seven diagnostics
failed at runtime without timeout; TypeScript compilation succeeded. Generated
code ran only in pinned network-disabled/resource-limited sandboxes.
The duration oracle converts the actual represented integer to BigInt, not the
decimal spelling 1e25. The ID case is a contradictory specification, like TS
generation0173 biography keys, not a proposed arbitrary naming change.

Scoped negatives: TS repair0125 spreads its tuple before numeric validation;
repair0126 has no malformed-input policy and explicitly reuses original objects
(locale ordering interpretation remains open); repair0127 escapes every required
field with bounded entity keys. JS generation0217 validates a fixed dense field
list; generation0221 maps internally created items (invalid-body versus missing-ID
priority is underspecified); repair0148 explicitly scopes Object.keys ordering;
generation0223 validates shape via indexed traversal; generation0228 uses ordinary
map/filter semantics without an element-validation requirement. No blanket approvals.

Continue position 301. GCS verified through 217 holds / batch 19, not this batch.
