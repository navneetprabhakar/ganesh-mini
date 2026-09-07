# Java combined quality follow-up — batch 45

Positions661–675 of v14 Java queue1112, full prompt/reference read.
Thirteen new holds: six non-triviality, six static behavioral and one executed.
1801 total holds (1798 additive+3),4362 unique outside inspections. Resume676.

| Position | ID | Finding |
| --- | --- | --- |
| 661 | exp-v1-java-generation-0474 | Non-triviality hold: operator switch delegates exact arithmetic to three standard-library methods and two directly specified division guards. |
| 662 | exp-v1-java-repair-0313 | Non-triviality hold: replaces index zero with size minus one in a supplied guarded list removal. |
| 663 | exp-v1-java-repair-0314 | Criterion-positive signed remainder repair preserves bucket semantics for negative values including MIN_VALUE rather than relying on overflowing absolute value. |
| 664 | exp-v1-java-repair-0315 | Non-triviality hold: removes the WARN disjunct from the ERROR branch in a two-literal router. |
| 665 | exp-v1-java-repair-0316 | Non-triviality hold: substitutes the already computed tail offset in a supplied arraycopy wrapper. |
| 666 | exp-v1-java-generation-0475 | Static hold: U+2003-only message passes nonblank-after-trimming validation. No stronger callback-mutation contract is inferred. |
| 667 | exp-v1-java-generation-0476 | Static hold: U+2003-only Zone label passes required nonblank validation. |
| 668 | exp-v1-java-generation-0477 | Static hold: U+2003-only Tool name or origin passes required nonblank validation. |
| 669 | exp-v1-java-generation-0478 | Static hold: U+2003-only Listing code or title passes nonblank validation; final page end also uses int addition despite overflow-free offset requirement (not executed for this candidate). |
| 670 | exp-v1-java-generation-0479 | Static hold: U+2003-only Location fields pass nonblank validation. Canonical directory names have an explicit trimmed-empty rule and are not independently held for nonblank. |
| 671 | exp-v1-java-generation-0480 | Static hold: snapshot normalization retains U+2003-only elements instead of discarding blank elements. |
| 672 | exp-v1-java-repair-0317 | Criterion-positive positional null-result preservation fixes output/input alignment while retaining ordered single callback invocation and immediate propagation. |
| 673 | exp-v1-java-repair-0318 | Executed hold: virtual immutable list of MAX_VALUE size, page2147484/size1000 should yield647 rows; int end addition wraps negative and throws IllegalArgumentException. Pinned Java compile0/run1, no timeout,2934ms; java-repair0318-page-end-overflow-result.json. |
| 674 | exp-v1-java-repair-0319 | Non-triviality hold: substitutes the standard-library case-insensitive prefix predicate in a fully supplied normalization wrapper. |
| 675 | exp-v1-java-repair-0320 | Non-triviality hold: adds one before the standard-library month lookup. |

The page-end probe uses a lazy AbstractList, not a multi-billion-element allocation.
Reconcile prior page-end arithmetic positives before admission; the existing Java
percentage group alone does not establish page-offset coverage.
Static findings are not executed results. Focused positives are not full
seven-criterion approval or admission. Network-disabled resource-limited probe.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

