# Python generation review, batch 2

Positions 16–30 of the 684-record v6 outside-sample Python generation queue.
Fifteen full prompt/reference/original-test inspections. Eight new holds:
two static, six sandbox-confirmed. Total 492 additive plus historical three
= 495 holds; 1,263 unique outside-sample inspections. Not admission approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 16 | 0017 | Static hold: gather stops at first failing result instead of waiting for all work before raising. Separate args/kwargs deepcopy alias semantics pending. |
| 17 | 0018 | Owner mapping snapshots before consuming rows; scoped node reuse and final-extension removal agree. General sequence and dotfile interpretation pending; no new hold. |
| 18 | 0014 | Static hold: exact case-sensitive runs required, but reference casefolds and original tests accept aaAAaa. |
| 19 | 0019 | Product order, validation and width-zero identity agree. Empty-alphabet enormous width loops unnecessarily; resource envelope unexecuted. No new hold. |
| 20 | 0021 | Canonical paths, exact alias and copied nonempty bytes agree. New-object identity for empty bytes remains a contract/runtime edge, not new hold. |
| 21 | 0022 | Exact records, ordered versions and nested deep copies agree. Custom metadata scalar domains and recursion depth pending; no new hold. |
| 22 | 0023 | Hold: finite integer rejected by float conversion; representable 200% change becomes infinity through subtraction overflow. |
| 23 | 0024 | Hold: zero-period compound identity fails at -100% and rounds a principal beyond context precision. |
| 24 | 0025 | Hold: unhashable kind raises TypeError instead of required ValueError. Extra-key sorting/reserved __extra__ collision also unresolved. |
| 25 | 0026 | Exact integer strict two-thirds threshold, first index and prevalidation agree. No new hold. |
| 26 | 0027 | Positive proper divisor pairs, perfect-square deduplication and inclusive range agree. Unbounded range/trial division capacity pending; no new hold. |
| 27 | 0028 | Hold: explicit empty format specification {name:} is accepted despite prohibition on format specifications. |
| 28 | 0029 | Hold: finite large integer coordinates rejected even when resulting distance is small and representable. |
| 29 | 0030 | Hold: valid finite geometry with representable boundary and t produces inf/nan/inf. |
| 30 | 0031 | Nine distinct selectors, exact name whitelist and independent ordered snapshot agree. No new hold. |

0017: `gather` is a list comprehension calling each Ticket.result. If one
raises, no later tickets are awaited; prompt explicitly says waits for all
submitted work. Original exception tests do not assert later work completion.
Static control-flow finding; no new runtime result claimed.

0014: Prompt compares characters exactly including case. Both `aAaa` and
`aaAAaa` revisit lowercase a after uppercase A and must fail. Original tests
require true; reference uses char.casefold(). Static prompt/test conflict.

All diagnostics below use the pinned Python 3.11.15 network-disabled and
resource-limited sandbox, exit 1 without timeout, with original task and hashes
preserved in the corresponding result.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0023 | readings_finite_numeric_probe.py / readings-finite-numeric-result.json | 424 | OverflowError on 10**400; infinity instead of 200.0 on -1e308 to 1e308. |
| 0024 | growth_zero_period_probe.py / growth-zero-period-result.json | 656 | Decimal InvalidOperation for zero**zero; five-digit context rounds identity result. |
| 0025 | compile_kind_validation_probe.py / compile-kind-validation-result.json | 413 | TypeError unhashable list instead of ValueError for malformed kind. |
| 0028 | render_empty_spec_probe.py / render-empty-spec-result.json | 457 | Required ValueError was not raised. |
| 0029 | route_integer_coordinate_probe.py / route-integer-coordinate-result.json | 548 | OverflowError while validating 10**400 coordinate; required total would be 7.0. |
| 0030 | box_finite_intermediate_probe.py / box-finite-intermediate-result.json | 408 | (inf, nan, inf) instead of (1e308, 0.0, 2.0). |

Original tests/candidates/sample unchanged. Candidate-file SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scope v6 unchanged; these rows already belong to reopened strata. Continue 31.
No new VM or training seal. Backup through Rust 684 predates Python batches.
