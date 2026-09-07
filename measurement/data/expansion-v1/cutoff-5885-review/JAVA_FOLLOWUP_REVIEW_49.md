# Java combined quality follow-up — batch 49

Positions721–735 of v14 Java queue1112, full prompt/reference read.
Seven new holds: four non-triviality and three static behavioral/contract findings.
1828 total holds (1825 additive+3),4422 unique outside inspections. Resume736.

| Position | ID | Finding |
| --- | --- | --- |
| 721 | exp-v1-java-repair-0343 | Non-triviality hold: replaces direct class comparison with the standard-library proxy-class predicate. |
| 722 | exp-v1-java-repair-0344 | Criterion-positive signed modular normalization preserves circular-shift semantics for negative distances including MIN_VALUE without negative arraycopy ranges. |
| 723 | exp-v1-java-generation-0517 | Non-triviality hold: inheritance/accessor exercise directly formats three prescribed messages; no substantive algorithm or state invariant. |
| 724 | exp-v1-java-generation-0518 | Criterion-positive lazy synchronized singleton validates only first initialization and safely publishes one immutable instance while ignoring later parameters. |
| 725 | exp-v1-java-generation-0519 | Non-triviality hold: five literal answer pairs and three scalar outcomes; trim also fails to remove U+2003 surrounding whitespace under the stated normalization contract (static). |
| 726 | exp-v1-java-generation-0520 | Criterion-positive directory snapshot ownership and no-query-on-null boundary preserve lookup isolation and exact code matching. |
| 727 | exp-v1-java-generation-0521 | Criterion-positive grouped aggregation distinguishes null-only groups, COUNT semantics and exact rounded decimal average with first-occurrence ordering. |
| 728 | exp-v1-java-generation-0522 | Criterion-positive permission snapshot and dynamic-proxy dispatch distinguish Object methods from authorized submit calls. Target exception identity is not expressly required and is not certified. |
| 729 | exp-v1-java-repair-0345 | Non-triviality hold: flips status !=0 to ==0 in a supplied two-outcome callback wrapper. |
| 730 | exp-v1-java-repair-0346 | Criterion-positive recycled-cell clearing prevents prior binding state from leaking into a null-caption rebind while preserving supplied object identity. |
| 731 | exp-v1-java-generation-0523 | Criterion-positive nested registry operations enforce module/endpoint existence and duplicate boundaries while returning detached insertion-order path snapshots. |
| 732 | exp-v1-java-generation-0524 | Criterion-positive lifecycle callbacks precede state changes so thrown activation/deactivation preserves the prior registry state. Reentrant callback mutation is not an added requirement. |
| 733 | exp-v1-java-generation-0525 | Static arithmetic/contract hold: oversized rejected job cost is computed with multiplyExact before budget comparison. With battery0, cost2 and job{MAX_VALUE,0}, all returned counts/data/energy fit long but the reference throws instead of rejecting the job; clarify required-result versus intermediate overflow before admission. |
| 734 | exp-v1-java-generation-0526 | Static hold: U+2003-only displayName passes the required non-whitespace-content check. The task is also a three-literal greeting table. |
| 735 | exp-v1-java-generation-0527 | Static hold: U+2003-only caller-supplied encoding name passes required nonblank validation. |

No new execution. Static findings are not executed results. Focused positives
are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

