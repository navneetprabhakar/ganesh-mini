# Rust generation review, batch 27

Positions 391–405 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections; two static holds and one sandbox
hold. Total 954 unique outside-sample inspections; 447 additive plus historical
three = 450 holds. Inspection is not seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 391 | 0454 | Authentication-before-availability, exact map-key lookup and cloned JSON-labelled reply agree. No new hold. |
| 392 | 0455 | Exact register getters, masks, writable-only write and reset agree. No new hold. |
| 393 | 0456 | Static hold: named registry methods lack signatures; tests impose owned account creation and three-argument owner addition. |
| 394 | 0457 | Generic clone utilities and exclusive decreasing range agree. Loop condition prevents decrement below i64::MIN; huge result allocation remains envelope question. No new hold. |
| 395 | 0458 | Catalog uniqueness, resource order and body-then-title substitutions agree. Substitution inside inserted body follows stated sequence; no invented literal-body rule. No new hold. |
| 396 | 0459 | Record lifecycle, per-record histories and prevalidated errors agree. Private history length cannot practically reach u64 exhaustion; no executed exhaustion finding. No new hold. |
| 397 | 0460 | Rectangular validation, optional lookup and saturating-add-before-capacity-clamp agree. No new hold. |
| 398 | 0461 | Exact separator grouping clones maximal nonempty runs in order. No new hold; elementary scope pending. |
| 399 | 0462 | Hypot norm, radius-only volume validation and atomic finite-coordinate translation agree. Read-only finite-output requirement is not stated; no new hold. |
| 400 | 0464 | Exact callback count, zero rejection, terminator and capacity label agree. Actual storage always allocates a Vec; prompt says report Inline by threshold without explicitly requiring stack storage. Quality/meaningfulness question retained, no new hold. |
| 401 | 0465 | Sandbox hold: Unicode trim removes non-ASCII whitespace despite ASCII-only trimming requirement. |
| 402 | 0467 | Active-low RGB order, stop-on-error and post-success index advance agree. Common associated error type bound and exact LineError generic declaration are unstated; completeness remains pending. No new hold. |
| 403 | 0468 | Disabled-entry bypass, normalized destination validation, duplicates and independent ordered outputs agree. No new hold. |
| 404 | 0463 | Static hold: callback alias definitions/setter signatures are omitted while tests require specific boxed mutable callback methods. |
| 405 | 0470 | Global sequences and newest-ten selection with timestamp/sequence ordering agree. Private sequence exhaustion is unspecified and not executed. No new hold. |

0456 declares data types but only lists registry method names. Original tests
require create_twin(Vec<u8>) returning Result<TwinId, RegistryError> and
add_owner(id, entity, proof), rather than e.g. add_owner(id, OwnerClaim).
The prompt provides no such signatures. The reference's checked transition
from the maximum ID to None was inspected, not reached in execution.

0465: `extension_ascii_trim_probe.rs` and `extension-ascii-trim-result.json`
preserve a pinned network-disabled/resource-limited diagnostic. The input
contains U+2003 around its ID and a U+2003 capability. These are literal data
under ASCII-only trimming; the first assertion shows the ID becomes plain
"id" instead. The capability assertion follows it and is not reached after
the ID failure; static inspection separately shows the capability is dropped.
Original tests use only ASCII whitespace and omit this case.

0463 names callback aliases and says callback setter methods exist, but gives
neither alias definitions nor setter names/signatures. Tests require
set_input_done_callback, set_decoder_event_callback and
set_format_changed_callback accepting boxed closures, and concrete event
argument ownership. The reference's queue/order/format behavior agrees, but
does not complete the missing prompt API.

Static holds are not runtime failures. Original tests/candidates unchanged.
Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scope v6 unchanged. Continue 406. No new VM or training seal.
