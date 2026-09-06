# Rust generation review, batch 8

Positions 106–120 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections. Three new holds. Total 669 unique
outside-sample inspections, 394 additive plus historical three = 397 holds.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 106 | 0120 | Explicit generic API, unconditional token traits, LIFO reusable slots and retirement branch. Pool-specific identity is not in the specified index/generation token; no extra identity requirement imposed. Private generation exhaustion not executed. No new hold. |
| 107 | 0118 | Explicit API, marker state machine, module validation and ordered borrowed sort. Newlines in otherwise allowed paths create an unresolved one-line-output contract envelope; not executed or counted. No new hold. |
| 108 | 0123 | Explicit API, take-at-turn-start simulation, checked operations and counts. Zero-round versus checked common-product overflow precedence unspecified; no invented oracle. No new hold. |
| 109 | 0126 | Explicit API, complete syntax validation before u32 parsing, patch validated then intentionally discarded. No new hold. |
| 110 | 0127 | Exact lookup/formatting API and preserved punctuation. Small formatting task; nontriviality unresolved. No new hold. |
| 111 | 0128 | Exact API, widened coordinate differences, half-open rectangle and independent clones. No new hold. |
| 112 | 0129 | Exact API, delegated VecDeque and conditional derives; representation expressly unrestricted. Small collection wrapper; nontriviality unresolved. No new hold. |
| 113 | 0130 | Hold: qualifying exact score can exceed u64; reference panics adding it. |
| 114 | 0131 | Exact API, retry count distinct from attempts, stop/escalate preserve unused outcomes. usize::MAX retries would require an unrepresentable attempts count; impractical envelope not executed or separately held. |
| 115 | 0133 | Hold: extra Self: Sized bound restricts the declared generic trait method. |
| 116 | 0134 | Static hold: required mix function is referenced but never supplied in the prompt; tests do not independently establish the required ranking. |
| 117 | 0135 | Explicit API, exact i32 conversion bounds, operand-order validation and checked multiplication. No new hold. |
| 118 | 0137 | Explicit API, safe ASCII-prefix byte offset, exact routes, comma arity and checked i64 sum. No new hold. |
| 119 | 0136 | Explicit API, bounded name length and checked offsets, owned UTF-8 and exact terminal position. Simultaneous error precedence unspecified. No new hold. |
| 120 | 0138 | Explicit API, owned continuous clone and widened i16 arithmetic with Euclidean remainder. No new hold. |

Executed probes in pinned network-disabled/resource-limited Rust sandbox:

- 0130 `segment-score-range-result.json`: length difference u64::MAX and low
  angle distance 1 qualify at supplied inclusive tolerances, requiring score
  u64::MAX+1 in a u64 field. Reference panics on addition, [0,101], 1450 ms,
  no timeout. No wrapping/clamping policy invented; the contract needs a range
  or output/error-policy correction. Probe's post-call length assertion is not
  reached because candidate code panics.
- 0133 `byte-source-unsized-result.json`: a generic caller bounded by
  `ByteSource + ?Sized` cannot use read_until because implementation adds a
  `Self: Sized` bound absent from the declared F: FnMut contract. Compile E0277,
  exit [1], 666 ms, no timeout; no test executable run. This is an API-bound
  mismatch, not a claim that the original SliceSource byte behavior failed.

0134 static evidence: prompt says to apply the supplied mix function from the
reference API contract but includes no definition or formula. Reference chooses
specific xor-shift/multiplication constants. Original tests check membership,
repeatability and prefix consistency, not an independent required score order.
No executed mutation-test result claimed. Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`;
prompt SHA-256 `612632a23b372de975c774ee3c4584beaa7e9a060463a9c41670ad87c6aa7cf2`;
original test SHA-256 `014604b8ea772f83042aeb5f4cea5f481637afcef2ac1c60004e7dc5cfb4fa1c`.

No-hold is not admission approval. Frozen artifacts and scope v6 unchanged.
GCS verified through 391 holds / Rust batch 6 / 639 inspections. Batches 7–8
await backup. Continue position 121. No new VM, training seal or revised partition.
