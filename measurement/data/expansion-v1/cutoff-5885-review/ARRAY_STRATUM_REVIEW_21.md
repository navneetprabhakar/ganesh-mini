# Array-validation follow-up, batch 21

Complete: positions 301–315 inspected; 15 new / 323 unique outside-sample
inspections. Nine new holds: **229 additive / 232 including historical three**.

- TS repair0131 loses a valid required non-enumerable ID during copying, so get
  cannot find the record: operator-required-id-copy-result.json.
- JS generation0231 accepts a missing provider item: bin-snapshot-missing-item-result.json.
- JS generation0232 loses a valid required non-enumerable job ID on enqueue:
  queue-required-job-id-copy-result.json.

All three runtime checks failed without timeout in pinned network-disabled,
resource-limited sandboxes; TypeScript compilation succeeded. No duplicate hold
IDs were present before these probes. TS generation0198 builds dense class tokens
and explicitly merges style records; JS generation0229 stores only individually
validated points. No new holds for those scoped observations, not approvals.

Positions 306–310:

- JS repair0154 readOwnPath: a missing path segment returns not-found rather
  than TypeError (own-path-missing-segment-result.json; 335 ms).
- TS generation0199 calculateWorkspace: fixed dense numeric validation and
  bounds constrain subtraction; fresh rectangles preserve order. No new hold.
- TS generation0202 renderNoteDocument: escapes specified text entities and
  treats body as trusted; no malformed-array policy, so no sparse-input hold.
- JS generation0237 buildActivationPlan: a missing dependency reaches unknown
  dependency handling, raising RangeError rather than TypeError
  (activation-missing-dependency-type-result.json; 338 ms).
- JS generation0238 applyShelfCommand: a singleton missing item survives both
  validation and duplicate check before clear (shelf-command-missing-item-result.json;
  373 ms).

Positions 311–315:

- JS generation0239 toggleExclusiveSection loses own enumerable __proto__ key
  through ordinary object assignment (section-proto-key-result.json; 366 ms).
- JS repair0158 runningTotals accepts a missing finite-number element and
  calculates NaN (running-totals-missing-value-result.json; 353 ms). Overflow
  of valid numbers is explicitly permitted normal JS arithmetic, not a hold.
- JS repair0159 routeAnnouncement validates every session with for-of before
  filtering and returns fresh objects with required fields. No new hold.
- JS generation0240 reconcileBalances validates both arrays with for-of,
  uses a Map for IDs, enforces safe integer bounds and returns fresh required
  fields; no new hold from the reviewed pattern.
- JS generation0243 createDocumentIndex accepts a missing label despite the
  string-array requirement (document-index-missing-label-result.json; 393 ms).

All six later probes failed their contract assertions without timeout in the
pinned network-disabled/resource-limited sandbox. Full prompts, references and
original tests were inspected. No new hold duplicates; negative findings are
scoped observations, not seven-criterion approvals. Continue position 316.
GCS verified through 223 holds / batch 20 / v6; batch 21 awaits backup.
