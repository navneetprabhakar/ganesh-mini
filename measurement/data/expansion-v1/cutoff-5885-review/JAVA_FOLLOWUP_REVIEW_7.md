# Java combined quality follow-up — batch 7

Positions91–105 of v14 Java queue1112, full prompt/reference read.
Thirteen new holds: seven non-triviality and six static behavioral findings.
1481 total holds (1478 additive+3),3792 unique outside inspections. Resume106.

| Position | ID | Finding |
| --- | --- | --- |
| 91 | exp-v1-java-repair-0043 | Non-triviality hold: changes the supplied count increment from two to one. |
| 92 | exp-v1-java-repair-0044 | Non-triviality hold: reverses supplied queue traversal to prescribed FIFO order. Static additional defects: U+2003 waiter passes nonblank validation and Set.of() cancellation input can throw from contains(null). |
| 93 | exp-v1-java-generation-0063 | Non-triviality hold: direct action-to-literal-message projection; the stored level does not influence later outcomes and nesting semantics are explicitly absent. |
| 94 | exp-v1-java-generation-0067 | Criterion-positive member/detail snapshots; static hold: U+2003-only member ID/name accepted despite nonblank constructors. |
| 95 | exp-v1-java-generation-0068 | Criterion-positive: UTF-8 byte escaping, nullable-versus-empty fields and ordered query delimiter assembly. |
| 96 | exp-v1-java-generation-0069 | Criterion-positive duplicate-aware earliest invitation removal; static hold: U+2003-only pending/action handles pass nonblank validation. |
| 97 | exp-v1-java-generation-0072 | Criterion-positive validated immutable catalog transitions; static hold: U+2003-only product ID/name or command target accepted. |
| 98 | exp-v1-java-repair-0045 | Non-triviality hold: direct integer-to-double division cast in the prescribed percentage formula; supplied validation remains unchanged. |
| 99 | exp-v1-java-repair-0046 | Criterion-positive handler installation before dispatch; static hold: U+2003-only destination remains accepted despite blank-destination rejection. |
| 100 | exp-v1-java-repair-0047 | Criterion-positive: private per-text-key locks repair synchronization across distinct equal String objects without locking caller-owned values. |
| 101 | exp-v1-java-repair-0048 | Non-triviality hold: replaces OR with the explicitly required AND. Static additional defect: U+2003 code/zone/required-zone remains accepted despite nonblank requirements. |
| 102 | exp-v1-java-generation-0070 | Criterion-positive callback snapshot/full validation; static hold: U+2003 source is not replaced with placeholder and U+2003 placeholder is accepted. |
| 103 | exp-v1-java-generation-0071 | Criterion-positive overflow-safe remaining-balance settlement; static hold: U+2003-only contributor identifier passes nonblank validation. |
| 104 | exp-v1-java-generation-0073 | Non-triviality hold: direct standard payment formula and scalar guards. Static additional defect: tiny positive annual rate such as 1e-20 makes 1+monthlyRate round to 1 and returns infinity for balance1/paymentCount1. |
| 105 | exp-v1-java-generation-0074 | Non-triviality hold: direct locale-root lowercase/contains filtering wrapper with null guards; no separate Unicode-casefold claim. |

No new execution. Unicode findings use the established U+2003 mismatch, not
inferred locale-specific case folding. The Set.of null-query concern extends
the collection-validation pattern but is explicitly static, not a List-probe
result claimed for Set. The payment counterexample has a finite expected final
result close to one; no intrinsically unrepresentable payment is demanded.
Focused positives are not admission or full seven-criterion approval.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

