# Java combined quality follow-up — batch 73

Positions1081–1095 of v14 Java queue1112, full prompt/reference read.
Ten new holds: three non-triviality and seven static findings.
2014 total holds (2011 additive+3),4782 unique outside inspections. Resume1096.
Approved versioned recovery remains pending; original corpus unchanged.

| Position | ID | Finding |
| --- | --- | --- |
| 1081 | exp-v1-java-repair-0514 | Static hold: U+2003-only SKU passes required nonblank validation even after positive-quantity repair. Not executed. |
| 1082 | exp-v1-java-repair-0515 | Static hold: U+2003-only service name passes required nonblank registration check. Service objects need not be deep copied by contract; not executed. |
| 1083 | exp-v1-java-repair-0516 | Non-triviality hold: directly changes a scalar loop start from odd to even for the prescribed filtered reduction; large-index stride overflow also needs boundary review. |
| 1084 | exp-v1-java-generation-0773 | Criterion-positive immutable page/count invariant is checked on decode and checked increments preserve selected-page positivity; leading zeros are not expressly prohibited. |
| 1085 | exp-v1-java-generation-0775 | Non-triviality hold: guarded fallback-index ternary and prescribed literal prompt formatting. |
| 1086 | exp-v1-java-generation-0776 | Static hold: U+2003-only classifier result is not mapped to Other despite required blank fallback. No classifier invocation-order rule is invented; not executed. |
| 1087 | exp-v1-java-generation-0777 | Static hold: strided int exponent += taskCount wraps for large termCount (e.g. Integer.MAX_VALUE with two workers), admitting negative exponents/failing an otherwise valid sum. Long-running boundary not executed. |
| 1088 | exp-v1-java-generation-0778 | Criterion-positive exact money adjustment and signed-magnitude BigInteger formatting preserve Long.MIN_VALUE and locale-independent cent/group formatting. |
| 1089 | exp-v1-java-generation-0779 | Criterion-positive immutable constructor values and duplicate-code validation before copied append preserve shelf ownership and original order. |
| 1090 | exp-v1-java-generation-0780 | Criterion-positive delimiter stack enforces matching nesting while distinguishing explicitly allowed ASCII text from malformed characters. |
| 1091 | exp-v1-java-repair-0517 | Criterion-positive inclusive rectangle bottom correction restores perimeter geometry; widened coordinates, clipped segments and deep row copies preserve off-image and ownership behavior. |
| 1092 | exp-v1-java-generation-0783 | Static hold: U+2003-only entree/accompaniment remains blank after trim but passes constructor validation. Not executed. |
| 1093 | exp-v1-java-generation-0784 | Static hold: U+2003-only ID/label/attribute keys or values pass required nonblank normalization. Public-method malformed-registry validation is also inconsistent and needs recovery review; not executed. |
| 1094 | exp-v1-java-generation-0785 | Static hold: U+2003-only announcement heading/body remains blank after trim but passes constructor validation. Identity-based listener snapshot semantics otherwise appear intact; not executed. |
| 1095 | exp-v1-java-generation-0786 | Non-triviality hold: direct transcription of the fully enumerated stateless phase/boolean-to-command decision table. |

No new execution. Static findings are not executed results. Focused positives are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
