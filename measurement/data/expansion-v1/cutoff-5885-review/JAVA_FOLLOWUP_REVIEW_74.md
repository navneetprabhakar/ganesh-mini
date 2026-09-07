# Java combined quality follow-up — batch 74

Positions1096–1110 of v14 Java queue1112, full prompt/reference read.
Nine new holds: three non-triviality and six static findings.
2023 total holds (2020 additive+3),4797 unique outside inspections. Resume1111.
Approved versioned recovery remains pending; original corpus unchanged.

| Position | ID | Finding |
| --- | --- | --- |
| 1096 | exp-v1-java-generation-0787 | Non-triviality hold: direct checked +/-1 and before/after ternary over scalars, plus prescribed char-sign conversion. |
| 1097 | exp-v1-java-generation-0788 | Static hold: U+2003-only Category/Message leaf text survives trim and passes required nonblank validation. XML hardening and direct-element checks do not cure this field defect. Not executed. |
| 1098 | exp-v1-java-generation-0789 | Static hold: U+2003-only target remains blank after trim but passes pre-mutation validation and can remove entries. Not executed. |
| 1099 | exp-v1-java-generation-0790 | Non-triviality hold: fully enumerated stateless enum transition table plus prescribed exception-to-string wrapper. |
| 1100 | exp-v1-java-generation-0781 | Static hold: percentage multiplication/addition can overflow when the percentage and final payment fit; Long.MAX_VALUE subtotal with 10000 discount basis points should yield full discount and zero total but multiplyExact fails. Not executed; same reopened percentage scope. |
| 1101 | exp-v1-java-generation-0792 | Static hold: U+2003-only jobCode/queue passes required nonblank field validation. Not executed. |
| 1102 | exp-v1-java-generation-0793 | Criterion-positive immutable capacity/enrollment invariant and all-criterion matching preserve explicit null-value wildcard semantics and source order. Null criterion key is rejected by NPE; query rejection type is not expressly frozen, so no fabricated wrong-exception finding. |
| 1103 | exp-v1-java-generation-0797 | Non-triviality hold: two prescribed regex checks followed by literal status selection and string concatenation. |
| 1104 | exp-v1-java-generation-0798 | Criterion-positive persistent node rebuilding preserves prior chains, replacement position and nullable-value versus absent-node distinction. |
| 1105 | exp-v1-java-generation-0800 | Static hold: U+2003-only device serial/model and nonnull team name passes mandatory blank validation. Not executed. |
| 1106 | exp-v1-java-generation-0795 | Criterion-positive type-directed exact integer conversion handles BigInteger/BigDecimal/range/fraction constraints, rejects nonfinite doubles and builds detached immutable converted lists. |
| 1107 | exp-v1-java-generation-0796 | Static hold: U+2003-only endpoint URI/protocol/region passes constructor blank rejection. Full-list null validation before limit handling otherwise remains intact; not executed. |
| 1108 | exp-v1-java-generation-0802 | Criterion-positive immutable date-order invariant and full-list validation precede inclusive field-specific range queries; whitespace-only labels expressly allowed. |
| 1109 | exp-v1-java-generation-0803 | Criterion-positive selected-pair validation separates primary from detail errors and preserves exact source identity while translating only the selected carrier fields. |
| 1110 | exp-v1-java-generation-0804 | Criterion-positive immutable ordered page updates preserve identity-specific hover/close behavior and exact original-bar return on missing close. |

No new execution. Static findings are not executed results. Focused positives are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
