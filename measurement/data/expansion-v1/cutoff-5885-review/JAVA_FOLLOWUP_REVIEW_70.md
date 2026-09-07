# Java combined quality follow-up — batch 70

Positions1036–1050 of v14 Java queue1112, full prompt/reference read.
Five new holds: three non-triviality and two static contract findings.
1990 total holds (1987 additive+3),4737 unique outside inspections. Resume1051.
Approved versioned recovery remains pending; original corpus unchanged.

| Position | ID | Finding |
| --- | --- | --- |
| 1036 | exp-v1-java-repair-0493 | Non-triviality hold: directly substitutes the explicitly supplied closed-interval upper comparator in a linear count. |
| 1037 | exp-v1-java-repair-0494 | Non-triviality hold: replaces one branch with the prescribed constant RESET result in a stateless enum table. |
| 1038 | exp-v1-java-repair-0495 | Criterion-positive int EOF sentinel is checked before narrowing to char, preserving valid U+FFFF and propagating read errors without closing caller resource. |
| 1039 | exp-v1-java-repair-0496 | Criterion-positive stage-then-commit array update validates every result before mutation and preserves original operands when changes aliases balances. |
| 1040 | exp-v1-java-generation-0746 | Non-triviality hold: scalar string holder with direct concatenation and fluent return-this wrapper. |
| 1041 | exp-v1-java-generation-0747 | Static contract hold: revision is stored as int and unchecked increment wraps rather than increasing after Integer.MAX_VALUE; no revision bound/overflow policy is specified. Long-history boundary not executed; clarify recovery policy. |
| 1042 | exp-v1-java-generation-0748 | Criterion-positive identity-tagged FIFO simulation rotates outranked entries and tracks the requested original element through removals without mutating input. |
| 1043 | exp-v1-java-generation-0749 | Criterion-positive immutable element construction copies attribute iteration order and preserves missing-hidden visibility semantics during detached inspection. |
| 1044 | exp-v1-java-generation-0750 | Criterion-positive parent-before-child structure computes depths and leaf status, normalizes signed modular products and uses checked final difference arithmetic. |
| 1045 | exp-v1-java-repair-0497 | Criterion-positive escape ordering handles original ampersands before generating entity text, preventing double escaping newly inserted entities. |
| 1046 | exp-v1-java-repair-0498 | Criterion-positive selected-field direction control preserves ascending identity tie-breaker independently of primary reversal across typed comparator choices. |
| 1047 | exp-v1-java-repair-0500 | Criterion-positive removal of narrowing cast preserves full epoch-second values beyond 32-bit range with fixed-offset and calendar validation. |
| 1048 | exp-v1-java-generation-0745 | Static contract hold: unqualified ids-must-be-positive requirement conflicts with Login.accountId stored as any trimmed nonempty String, accepting negative/nonnumeric IDs. Freeze account-ID type/domain before recovery; not executed. |
| 1049 | exp-v1-java-generation-0751 | Criterion-positive two-pointer merge consumes duplicate runs from both sorted inputs while preserving global ascending uniqueness. |
| 1050 | exp-v1-java-generation-0753 | Criterion-positive joint move-count/winner consistency checks compose with row/column/diagonal detection on bounded boards; no additional game-history rule is inferred. |

No new execution. Static findings are not executed results. Focused positives are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
