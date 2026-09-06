# Rust generation review, batch 1

Current gate: quality admission, not training ready. Review queue is the frozen
v6 inventory's Rust generation records outside the frozen 300 sample, in inventory
order: 684 records across first-pass and corrected strata. This differs from the
614-record first-pass-only missing-API stratum. No new generation or compute VM.

Positions 1–15 were read in full: prompt, reference implementation, original tests.
Fifteen new outside-sample inspections, three new holds: total 564 inspections,
382 additive plus historical three = 385 holds. No-hold is not quality approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 1 | 0001 | Complete signatures; decimal validation and sticky completion state consistent. No new hold. |
| 2 | 0002 | Static hold: absent reference API. Details below. |
| 3 | 0004 | Missing reference API and reproduced new-sample precedence violation. |
| 4 | 0007 | Complete API; prefix checks make UTF-8 slicing safe; root normalization and fallback consistent. No new hold. |
| 5 | 0009 | Complete API; validates duplicates before scheduling, deterministic tie-break and checked time. Unbounded allocation envelope not treated as a reproduced failure. No new hold. |
| 6 | 0010 | Complete API; preserves strings, checks header/rule restrictions, clones owned fields. Error precedence among multiple invalid fields unspecified. No new hold. |
| 7 | 0011 | Complete API; latch transitions and ordinary Debug format match. Small state machine; nontriviality remains pending. No new hold. |
| 8 | 0012 | Reproduced extra-token error classification defect. |
| 9 | 0013 | Explicit API; Rc-owned lifetime tracking and per-pool IDs, Drop and delegation consistent. No new hold. |
| 10 | 0014 | Explicit main signatures; cache checks, atomic malformed refresh and prescribed saturating expiry. Behavior at now=u64::MAX not separately adjudicated. No new hold. |
| 11 | 0015 | Recursive lower-bound helper, no slice copying, first-duplicate handling. No new hold. |
| 12 | 0016 | Complete API; owned clones and sorted BTreeMap wrapper. Nontriviality remains pending; no new hold. |
| 13 | 0018 | Topology preservation and message knowledge checks consistent. Blank-vs-empty neighbor wording and iterator side effects not adjudicated. No new hold. |
| 14 | 0019 | Complete API; Rc makes it neither Send nor Sync; takes slots on dequeue, no Clone bound. Original tests omit wrapped enqueue after dequeue and compile-negative auto-trait checks; reference inspection is not executed coverage. No new hold. |
| 15 | 0020 | Complete API and option validation. Infix wrapping-formula wording could be parenthesized more clearly; tests/reference use seed + i*17. No new hold for ambiguous grouping. |

## Candidate-bound static evidence: exp-v1-rust-generation-0002

Frozen candidate file SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
The entire user prompt lists method names then requires them to have “the
signatures shown by the reference API”; no signatures/reference API follow.
It does state balance/allocation types u128 and aliases, but not all parameter
and return types. In particular, the reference provides
`balance(&self, account: AccountId) -> u128`, returning zero if absent, and
the original `balances_allocations_and_missing_values_have_expected_defaults`
test requires `ledger.balance(7) == 0`. The prompt explicitly gives missing-pair
and missing-total defaults but not this missing-account balance result.
Original test file SHA-256:
`b7f4f0b8b828eba28d3efe9853194f26e9b5ac1bdfbd9c6e60c6b6b96b7e525d`.
This is a specification-completeness hold, not an executed runtime failure.

## Executed diagnostics

- 0004: add existing [5,10] with sample (6,1), then new [0,8] with sample
  (6,2). Contract says new sample wins; output retains 1. Original tests only
  exercise empty sample vectors. `segment-new-sample-precedence-result.json`,
  compiled successfully then failed assertion, [0,101], 1704 ms, no timeout.
  Prompt also says types have “the reference API” but omits fields/signatures.
- 0012: `(1 2)` has balanced parentheses and an extra operand at byte 3.
  Required UnexpectedToken(3), actual MissingClosingParen.
  `expression-extra-token-result.json`, [0,101], 1450 ms, no timeout.

Both run in pinned Rust 1.85 network-disabled/resource-limited sandboxes.
Rust test harness assertion failure exits 101, not 1; do not misclassify it as
a compiler/infrastructure failure or force it through the JS-specific group
loader assumption. No tooling was changed. Frozen artifacts remain unchanged.
GCS verified through the 382-hold array checkpoint; this batch awaits backup.
Continue Rust queue position 16. No training seal or revised admission partition.
