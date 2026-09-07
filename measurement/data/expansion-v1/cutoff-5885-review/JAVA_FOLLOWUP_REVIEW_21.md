# Java combined quality follow-up — batch 21

Positions301–315 of v14 Java queue1112, full prompt/reference read.
Nine new holds: four non-triviality and five static behavioral/contract findings.
1606 total holds (1603 additive+3),4002 unique outside inspections. Resume316.

| Position | ID | Finding |
| --- | --- | --- |
| 301 | exp-v1-java-generation-0213 | Non-triviality hold: fixed selector table returning prescribed uppercase/lowercase library wrappers or literal bracket concatenation. |
| 302 | exp-v1-java-generation-0214 | Criterion-positive independent registry lifecycle, archived-state checks and snapshot stability; static hold: U+2003-only Document ID passes blank rejection. |
| 303 | exp-v1-java-generation-0215 | Criterion-positive independent shared-across-style sequence consumption and explicit exhausted state avoid wraparound. No private-field injection or unstated post-exhaustion peek contract is used. |
| 304 | exp-v1-java-repair-0141 | Criterion-positive operation-order repair enforces the post-append capacity invariant, including zero capacity and oversized initial logs. |
| 305 | exp-v1-java-repair-0142 | Non-triviality hold: removes the existing-total/max detour and substitutes desiredTotal into the already supplied quotient/remainder distribution. |
| 306 | exp-v1-java-repair-0143 | Non-triviality hold: fixes a standalone percentage formula using widened multiply-before-divide; cursor behavior is already complete and unrelated to the repair. No overflow defect remains in the corrected formula. |
| 307 | exp-v1-java-repair-0144 | Criterion-positive detached selected-list snapshot repair; static hold: U+2003-only endpoints/fallback pass nonblank validation. |
| 308 | exp-v1-java-generation-0217 | Criterion-positive code-point workers coordinate with predicate-loop wait/notify and source-index turns. Very large worker counts and interruption cleanup are not newly executed or certified. |
| 309 | exp-v1-java-generation-0221 | Criterion-positive identifier grammar and escaped literal rendering preserve requested field order/duplicates and optional-condition syntax without changing input. |
| 310 | exp-v1-java-generation-0222 | Criterion-positive immutable settings and copied nested row results; static contract hold: positive decimal max.rows value 01 is rejected by a no-leading-zero regex although the prompt does not impose canonical decimal spelling. |
| 311 | exp-v1-java-repair-0145 | Criterion-positive exact lexical grammar and long parsing replace lossy floating conversion, preserving explicit trim semantics and full signed range. |
| 312 | exp-v1-java-repair-0146 | Non-triviality hold: adds ArithmeticException to the supplied catch clause to handle zero divisors; Java integer division semantics are explicitly requested. |
| 313 | exp-v1-java-repair-0148 | Criterion-positive staging snapshots both operands before computing every exact sum and committing, including target/deltas aliasing. Null queries operate on copied ArrayLists. |
| 314 | exp-v1-java-generation-0218 | Criterion-positive immutable tag ownership and validated filtering; static hold: U+2003-only title/category/tag pass nonblank validation. |
| 315 | exp-v1-java-generation-0220 | Criterion-positive exact pair-scoped sequence allocation, checked exhaustion and immutable history append; static hold: U+2003-only account/exercise/dialect pass nonblank validation. |

No new execution. The max.rows grammar finding is a contract/label hold, not an
executed result or permission to rewrite the prompt. ArrayList null queries are
not conflated with List.of failures. Focused positives are not admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
