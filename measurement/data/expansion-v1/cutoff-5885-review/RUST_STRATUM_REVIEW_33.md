# Rust generation review, batch 33

Positions 481–495 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections; one static API and one sandbox-backed
hold. Total 1,044 unique outside-sample inspections; 460 additive plus historical
three = 463 holds. Inspection is not seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 481 | 0557 | Canonical byte lengths/counts, UTF-8 boundaries, ordered replacement and complete consumption agree. Public malformed catalog state remains outside tested construction invariants; no new hold. |
| 482 | 0559 | Global expiry sweep, backward-tick saturation, insertion-age preservation and timestamp/ID eviction agree. No new hold. |
| 483 | 0560 | Generic left fold starts at Default and preserves input. No new hold; elementary scope pending. |
| 484 | 0561 | Exclusive movement and fixed event order, independent preference toggles agree. No new hold. |
| 485 | 0564 | Sequence assignment and append share mutex; snapshots own data; poison recovery is visible but not exercised by original tests. Private exhaustion not executed. No new hold. |
| 486 | 0562 | Exact weights, XOR, exhaustive keys and stable ties agree. Unicode invalid-column/odd-length priority, line endings and large-score resource envelope remain pending; no new hold. |
| 487 | 0565 | Strict two-phase peak scan handles equal values and boundaries without subtraction. No new hold. |
| 488 | 0567 | Agent-first earliest compatible dispatch and retained unmatched order agree. Assignment field widths inferred from ID types; no new hold. |
| 489 | 0570 | Ordered publications, owned fields and widened u128 sum agree. Floating-point mean has ordinary rounding, not integer truncation; no new hold. |
| 490 | 0569 | Static hold: absent referenced API leaves constructor, finish argument types and accessor names/signatures unspecified. Empty detailed-message behavior also pending. |
| 491 | 0572 | Sandbox hold: squared norm overflows for finite velocity and collapses a representable positive step to zero. |
| 492 | 0573 | Global IDs, oldest visible delivery, atomic tick-overflow handling and acknowledgement agree. Saturating delivery count, empty-topic overflow priority and contradictory acknowledged-capacity wording remain pending; no new hold. |
| 493 | 0575 | Standard scalar/list/default cases agree. Extra-colon rejection and comma in bare item restrictions are not explicit; grammar interpretation pending, no new hold. |
| 494 | 0576 | Factory isolation, owned previous value and non-destructive fetch agree. Moving replaced String rather than redundant cloning preserves observable ownership contract. No new hold. |
| 495 | 0571 | State invariant, exact field order and encoded forms agree. Leading-zero decode rejection exceeds explicit field-order wording unless canonical applies to entire input; pending, no new hold. |

0569: Prompt asks for "methods shown by the reference API" but supplies no
reference API. Original tests require Reporter::new(Mode), status_line,
prefix/message/ticks/is_finished/error_output accessor names and
finish_ok/finish_error(Option<&str>). No standalone declarations establish
these caller requirements. Reference also suppresses empty set_message in
Detailed mode despite "every message" wording; this was inspected only, not
executed. Static API hold is independently established.

0572: `stable_step_norm_probe.rs` ran against the unmodified reference in the
pinned network-disabled, resource-limited Rust 1.85.0 verifier. Compile 0/test
101, 1,623 ms, no timeout. Cell width 1, velocity (1e200,0), zero gradient,
motion enabled and no deformation cap returned 0 rather than approximately
1e-200 (relative tolerance 1e-12). Both the norm and expected reciprocal are
representable; squaring before square root causes avoidable overflow.
Result: `stable-step-norm-result.json`.

Original tests/candidates unchanged. Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scope v6 unchanged. Continue 496. No new VM or training seal.
