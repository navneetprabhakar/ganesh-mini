# Rust generation review, batch 36

Positions 526–540 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections; one static contract/test hold.
Total 1,089 unique outside-sample inspections; 464 additive plus historical
three = 467 holds. Inspection is not seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 526 | 0614 | Ordered owned roster add/remove, boundary IDs and failure atomicity agree. No new hold. |
| 527 | 0616 | Trimmed recognized fields, ignored unknown keys and duplicate presence agree. Empty unknown key well-formedness unspecified; no new hold. |
| 528 | 0618 | Shortest LEB128, owned payload and complete consumption agree. LengthTooLarge covers cursor addition overflow as well as usize conversion; narrow-target branch not newly executed. No new hold. |
| 529 | 0615 | Text output paths and UTF-8 body lengths agree. Group-path duplicates are not tracked; whether duplicate full paths means all nodes or collected files remains pending. No new hold. |
| 530 | 0619 | Strict hex, big-endian products and bounded modular accumulator agree. No new hold. |
| 531 | 0620 | Required selected entries, duplicate ignored entries and retained colon values agree. Line-ending grammar remains pending; no new hold. |
| 532 | 0622 | Last-valid wins, exact one equals and ordinary Rust number/bool parsing agree. No new hold. |
| 533 | 0624 | Required docs/derives, stored float bits and six-value flatten order agree. Computed NaN equivalence is not exact payload guarantee; no new hold. |
| 534 | 0623 | Static hold: zero-capacity test requires Mailbox equality/debug absent from requested traits. Ordinary mutex/condvar FIFO and wake paths agree; destructor reentrancy/poison wake behavior remains pending. |
| 535 | 0625 | Ignored caller IDs, exact accession lookup and borrowed insert result agree. Private exhaustion and constructor presentation remain pending; no new hold. |
| 536 | 0626 | Byte stage mapping, token uniqueness and owner-XOR wrapping sum agree. No new hold; not a cryptographic proof claim. |
| 537 | 0627 | Split-whitespace dispatch, exact command arities and failure nonmutation agree. No new hold. |
| 538 | 0628 | Constructor clamps/masks and ordinary lane iteration agree. Public lane_count above 32 can panic in all_steady; invalid externally constructed state contract remains pending. No new hold. |
| 539 | 0629 | Exact payload/reply masks preserve all reserved bits. No new hold. |
| 540 | 0632 | Per-document validation priority, byte NUL offsets and Unicode word splitting agree. No new hold. |

0623: Original validates_capacity_and_reports_configuration test uses
assert_eq!(Mailbox::<i32>::limited(0), Err(QueueConfigError::ZeroCapacity)).
Comparing Result requires Mailbox: PartialEq and Debug even for an Err result.
The prompt requires these traits for the error enums, but only Clone for
Mailbox. Reference adds pointer-identity equality and Debug to satisfy the
caller; these are not stated requirements. A conforming queue with only the
requested traits would fail compilation of the original test. This is a
static test-contract hold, not a newly executed queue-runtime failure.

No new sandbox execution in this batch. Original tests/candidates unchanged.
Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scope v6 unchanged. Continue 541. No new VM or training seal.
