# Rust generation review, batch 7

Positions 91–105 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections. Three new holds. Total 654 unique
outside-sample inspections, 391 additive plus historical three = 394 holds.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 91 | 0102 | Public rules and signatures, desired/current canonicalization, allowed replacement precedence, order-preserving filter. No new hold. |
| 92 | 0103 | Explicit API, required fields, duplicate detection including ignored keys, first equals and owned trimmed values. No new hold. |
| 93 | 0104 | Exact Cow lifetime API and borrowed/owned transitions. Small ownership exercise; nontriviality unresolved. No new hold. |
| 94 | 0105 | Hold: finite nonzero viewing direction rejected due to overflow in squared norm. |
| 95 | 0106 | Exact API and required loop constructs, wrapping recurrence. Original tests exhaust all 256 u8 counts. Pedagogical task; nontriviality unresolved. No new hold. |
| 96 | 0107 | Explicit protocol API, checked decimal parsing and byte lengths, exact trailing-byte rejection and owned Unicode text. No new hold. |
| 97 | 0108 | Exact API; connected n-node graph with n-1 edges establishes a tree, breadth-first parity preserves query order. No new hold. |
| 98 | 0109 | Explicit trait, field types and generic commission; saturating counters and exactly one initialization. Small trait exercise; nontriviality unresolved. No new hold. |
| 99 | 0110 | Explicit API and ownership, ordered IDs and preserved names. At most u32::MAX distinct nonzero IDs each with u32::MAX units, so total fits u64. No new hold. |
| 100 | 0111 | Hold: update accepts a publicly mutated invalid ID despite validating the entire proposed result. |
| 101 | 0112 | Explicit trait/API, exact escape sequence order and validate-before-mutate. No OS calls. No new hold. |
| 102 | 0114 | Explicit types/API, input-order validation then exact enum mapping, immutable positions. No new hold. |
| 103 | 0113 | Explicit API, checked dimension product and stable axis endpoints, explicit permitted NonFinite arithmetic errors. No new hold. |
| 104 | 0116 | Hold: quiet=+1 accepted despite literal 0-or-1 format; Unicode whitespace also returns wrong error. |
| 105 | 0117 | Exact borrowed API, char_indices slicing and snapshot before mutation. Small borrowing exercise; nontriviality unresolved. No new hold. |

Executed in pinned network-disabled/resource-limited Rust sandbox, all compile
successfully then fail assertions [0,101], with no timeout:

- `lens-finite-direction-result.json`, 1473 ms: origin eye, aim (0,0,-1e200),
  nonparallel unit up, ordinary FOV/focus and 1x1 image. Constructor unexpectedly
  returns None; squared length overflows despite finite nonzero direction.
  First loop case fails, so the subsequent -1e-200 case and ray assertions are
  **not reached**. Those are not additional executed results.
- `notice-entire-result-result.json`, 1531 ms: create valid rule, set public ID
  to zero, then apply otherwise valid expiry patch. Actual Ok(()) instead of
  InvalidId. Prompt requires entire proposed-result validation; original tests
  only update rules with valid base fields. The later state assertion is not
  reached, so no separately executed atomicity assertion is claimed.
- `profile-literal-syntax-result.json`, 1615 ms: quiet=+1 unexpectedly succeeds;
  independent test with U+2003 in a key returns UnknownField instead of the
  whitespace syntax error MalformedField. Two executed failures, one record hold.

No-hold is not admission approval. Frozen artifacts and scope v6 unchanged.
GCS verified through 391 holds / Rust batch 6 / 639 inspections. Batch 7 awaits
backup. Continue position 106. All 97 data tooling tests pass; tooling unchanged.
No new VM, training seal or revised partition.
