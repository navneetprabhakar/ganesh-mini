# Rust generation review, batch 44

Positions 646–660 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections; one sandbox-confirmed hold.
Total 1,209 unique outside-sample inspections; 476 additive plus historical
three = 479 holds. Inspection is not seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 646 | 0757 | Hold: early checked-sum overflow prevents required inspection of a later mismatched kind. |
| 647 | 0758 | Widened sum and Euclidean remainder implement wrapping coordinates; accepted signed decimals/leading zeroes agree. No new hold. |
| 648 | 0759 | Frame filtering retains order and computes owned summary scalars. No new hold. |
| 649 | 0760 | Strict option parsing ordinary paths agree. Global whitespace versus duplicate-value precedence remains pending; plus sign in base-ten u8 not expressly forbidden. No new hold. |
| 650 | 0761 | First bad title, independent owned desktop lists and event/body handling agree. No new hold. |
| 651 | 0762 | Copied lane cause/pending state, clear signal and nonmutating invalid calls agree. Allocation envelope pending; no new hold. |
| 652 | 0763 | First unescaped equals and escape validation across unmatched keys agree. Physical-line CR interpretation remains unspecified; no new hold. |
| 653 | 0764 | Short-circuit And/Choose and checked Add agree. Competing operand errors and recursion capacity remain pending; no new hold. |
| 654 | 0765 | Initial/blocked positions retained; bounded coordinates keep increment safe. Trace allocation envelope pending; no new hold. |
| 655 | 0766 | Generation/enabled/refresh/settings precedence and required-refresh marker policy agree. Ordered duplicate settings preserved. No new hold. |
| 656 | 0767 | First duplicate ID, FIFO drains, saturation and post-event stable removal agree. Caller-created duplicate public units outside constructor remain unspecified; no new hold. |
| 657 | 0768 | Ordered routes, empty extension creation, bounds and strict little-endian codec agree. Payload bounds precede point allocation; huge route count fails on missing count. No new hold. |
| 658 | 0769 | Exact single-at address rule, ASCII whitespace and sender-first validation agree; formatting owned and literal. No new hold. |
| 659 | 0771 | Prefix-only base validation precedes optional token; uppercase UTF-8 percent encoding and literal HTML agree with explicit contract. Not production URL/HTML security certification. No new hold. |
| 660 | 0773 | ASCII-digit prevalidation and per-step modulo-ten accumulation agree. Output allocation envelope remains pending; no checksum overflow defect. No new hold. |

0757 evidence: `aggregate_kind_priority_probe.rs` and
`aggregate-kind-priority-result.json`. Three readings have amounts MAX, 1, 0
and kinds n, n, wrong. Prompt requires inspecting every kind and returning the
first mismatch before otherwise summing. Reference interleaves checks and
returns at the second reading's overflow. Probe expecting UnexpectedKind
compiled (0), failed assertion (test exit 101), 1,625 ms, no timeout, inside
the pinned network-disabled/resource-limited Rust sandbox. Assertion output
does not print the actual variant; the early Overflow path is static code
evidence, not a claimed printed observation.

Original tests/candidates unchanged. Frozen SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scope v6 unchanged. Continue 661. No new VM or training seal.
