# JavaScript/TypeScript residual review, batch 4

Positions 46–60 of 587 in the batch 1 queue. Full prompts, reference/corrected
source and original tests read, including known-bad source where present.
Eight new holds: 946 additive plus historical three = **949**;
**2,403** unique outside-sample inspections. Holds require disposition, not
final rejection, admission or seven-criterion approval.

| Position | ID suffix | Scoped finding |
| --- | --- | --- |
| 46 | javascript-repair-0021 | Dot boundary repairs suffix matching. ASCII/case/single-leading-dot rules agree; no stricter DNS requirement invented. No new hold. |
| 47 | javascript-generation-0032 | Hold: sparse initial array bypasses record validation. Prose integer versus safe-integer reference/test restriction also pending. Copying, normalized duplicates and exact lookup agree. |
| 48 | javascript-repair-0022 | Release deletes active lease; snapshot defines proto-safe properties. Lexical insertion versus numeric-key enumeration wording pending, no new hold. |
| 49 | typescript-generation-0033 | Token/phase validation, frozen copies and exact token preservation agree; large-integer increment scope pending. No new hold. |
| 50 | typescript-generation-0035 | BigInt amount, decimals 0–100, sign, padding and fraction trimming agree. No new hold. |
| 51 | typescript-generation-0036 | Hold: valid-address invalid metadata throws synchronously instead of returned Promise rejection. Original await/catch tests do not distinguish this. |
| 52 | typescript-repair-0021 | Ordered escaping repairs all five HTML characters; wrapper and whitespace preservation agree. No new hold. |
| 53 | typescript-repair-0022 | Preorder repaired; shared branches/cycle path handled. Hold: finite acyclic depth 10000 raises RangeError; runtime envelope pending. |
| 54 | typescript-repair-0023 | Map copy repairs aliasing. Hold: attachAll accepts blank key; global invariant versus set-specific requirement needs disposition. |
| 55 | javascript-generation-0037 | Hold: U+2028 accepted inside path despite line-break prohibition; Unicode line domain pending. Leading indentation omission matches explicit tests. |
| 56 | javascript-generation-0042 | Username normalization, exact password, duplicate checks, sparse rejection and fresh lists agree. No new hold. |
| 57 | javascript-repair-0028 | Duplicate Set repair and null-prototype safety agree. Hold: integer keys violate literal first-appearance enumeration; object-order contract disposition needed. |
| 58 | javascript-generation-0039 | Hold: backward arithmetic rounds an intermediate outside safe range even though inputs are explicitly safe. First boundary probe passed; adjacent probe reproduced wrong index. |
| 59 | javascript-generation-0040 | Hold: required-field pass inserts pinConfirmation before earlier phone format error. Explicit field-order violation. |
| 60 | typescript-generation-0037 | Group classification and callbacks agree at runtime. Exhaustive typed union makes future-kind remote path expressible only through casts; API/test quality pending. No new hold. |

Nine isolated pinned, network-disabled, resource-limited probes executed:
eight failed assertions (five JavaScript [1], three TypeScript [0,0,1]);
one JavaScript passing boundary control [0]. No timeout. Original tests read,
not rerun by isolated probes. Candidate/test/sample/partition unchanged.
Candidate SHA: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID suffix | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| javascript-generation-0032 | residual_inventory_0032 / residual-inventory-0032 | 527 | missing TypeError |
| typescript-generation-0036 | residual_localized_0036 / residual-localized-0036 | 4505 | synchronous metadata error |
| typescript-repair-0022 | residual_outline_0022 / residual-outline-0022 | 4471 | RangeError on acyclic input |
| typescript-repair-0023 | residual_slot_0023 / residual-slot-0023 | 2584 | blank key admitted |
| javascript-generation-0037 | residual_asset_0037 / residual-asset-0037 | 650 | Unicode line separator accepted |
| javascript-repair-0028 | residual_entries_0028 / residual-entries-0028 | 582 | numeric enumeration order |
| javascript-generation-0039 | residual_viewport_0039 / residual-viewport-0039 | 789 | passing control, n-1 index |
| javascript-generation-0039 | residual_viewport_0039_adjacent / residual-viewport-0039-adjacent | 437 | n-2 index: 9007199254740989 instead of 9007199254740988 |
| javascript-generation-0040 | residual_access_request_0040 / residual-access-request-0040 | 526 | wrong error key order |

Probe suffixes: `_probe.js` or `_probe.ts`; result suffix `-result.json`.
Batch 4 awaits backup; last verified GCS checkpoint is through residual 30.
Continue residual position 61. Remaining criteria/dispositions block admission.
