# Java combined quality follow-up — batch 48

Positions706–720 of v14 Java queue1112, full prompt/reference read.
Seven new holds: four non-triviality and three static behavioral findings.
1821 total holds (1818 additive+3),4407 unique outside inspections. Resume721.

| Position | ID | Finding |
| --- | --- | --- |
| 706 | exp-v1-java-generation-0505 | Non-triviality hold: prescribed scalar label formatting plus standard Base64 wrapper and independent character guards. |
| 707 | exp-v1-java-generation-0506 | Criterion-positive full monotonic sequence validation and append boundary preserve immutable journal ownership; maximum-size allocation is not certified. |
| 708 | exp-v1-java-generation-0507 | Criterion-positive access-ordered bounded registry correctly couples successful reads/replacements to eviction order and independent instances. |
| 709 | exp-v1-java-generation-0508 | Non-triviality hold: direct conjunction of prescribed scalar/map validity predicates with a whitespace scan, without substantive algorithm or state transition. |
| 710 | exp-v1-java-generation-0510 | Criterion-positive whole-map validation and unique requested-order projection distinguish present empty preferred values from missing-key fallback. |
| 711 | exp-v1-java-repair-0337 | Static hold: default regex \\s does not recognize U+2003 separators although the command grammar allows whitespace characters. |
| 712 | exp-v1-java-repair-0338 | Criterion-positive key-presence repair distinguishes absent owner from a valid empty owner while retaining whole-map validation. |
| 713 | exp-v1-java-repair-0339 | Non-triviality hold: changes the supplied index comparison from > to >=. |
| 714 | exp-v1-java-repair-0340 | Non-triviality hold: adjusts the already supplied separator boundary condition by one. |
| 715 | exp-v1-java-generation-0512 | Static hold: take:2147483648 is a valid nonnegative decimal count larger than any current string but parseInt rejects it instead of retaining the string. Prompt supplies no int upper bound. |
| 716 | exp-v1-java-generation-0513 | Static hold: truncated GZIP frame declaring count MAX_VALUE triggers eager ArrayList allocation before truncation validation, yielding resource failure rather than required IllegalArgumentException. Untrusted item length is likewise allocated before reading; not executed. |
| 717 | exp-v1-java-generation-0515 | Criterion-positive ordered reflective property fallback distinguishes a successful null from failed reads and merges lexicographic bean snapshots with stable overwrite positions. |
| 718 | exp-v1-java-generation-0516 | Criterion-positive fragment-boundary reconstruction handles split CRLF, first comma payload preservation and terminal versus internal empty records. |
| 719 | exp-v1-java-repair-0341 | Criterion-positive iterator-owned removal repairs traversal invalidation without mutating the original list. |
| 720 | exp-v1-java-repair-0342 | Criterion-positive encounter-ordered deduplication restores the first-appearance invariant lost by unordered set iteration. |

No new execution. Static findings are not executed results. Focused positives
are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

