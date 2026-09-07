# Java combined quality follow-up — batch 65

Positions961–975 of v14 Java queue1112, full prompt/reference read.
Nine new holds: six non-triviality and three static findings.
1962 total holds (1959 additive+3),4662 unique outside inspections. Resume976.
Approved versioned recovery remains pending; original corpus unchanged.

| Position | ID | Finding |
| --- | --- | --- |
| 961 | exp-v1-java-generation-0688 | Criterion-positive literal delimiter parsing preserves later assignment characters, last-value/original-order duplicates and a copied accepted-key filter; trimming semantics explicitly specified. |
| 962 | exp-v1-java-generation-0690 | Criterion-positive escape tokenization and whole-string DP distinguish wildcard zero-or-more paths from literal UTF-16 code units and reject dangling escapes. |
| 963 | exp-v1-java-repair-0457 | Criterion-positive replacement-versus-accumulation lifetime invariant removes retained old buffers and preserves independent deep copies of newly opened buffers. |
| 964 | exp-v1-java-repair-0458 | Non-triviality hold: identity function returning its input after removing an unwanted regex call. |
| 965 | exp-v1-java-repair-0460 | Static hold: canonical predicate still accepts explicitly forbidden -0, which Long.parseLong decodes as zero. Not executed. |
| 966 | exp-v1-java-generation-0691 | Non-triviality hold: two literal enum formats over a direct DTO mapping with independent validation. |
| 967 | exp-v1-java-generation-0692 | Non-triviality hold: direct per-element use of the exact BigDecimal.valueOf/setScale/HALF_UP/toPlainString pipeline prescribed in the prompt. |
| 968 | exp-v1-java-generation-0693 | Criterion-positive ROOT-normalized text and inclusive-time query composes detached result creation with overflow-safe two-key ordering while retaining duplicates and validating all articles. |
| 969 | exp-v1-java-generation-0694 | Static hold: U+2003-only requested email remains blank after trimming but bypasses malformed-request rejection, producing lookup behavior instead. Not executed. |
| 970 | exp-v1-java-generation-0695 | Non-triviality hold: direct transcription of both supplied diagonal equations and border predicates in nested rendering loops. |
| 971 | exp-v1-java-generation-0696 | Non-triviality hold: fixed five-bit literal-name mapping with explicitly prescribed unknown/conflict predicates. |
| 972 | exp-v1-java-repair-0461 | Criterion-positive legal-state transition guard rejects PAUSE from NEW or PAUSED while preserving sequenced history and terminal STOPPED behavior. |
| 973 | exp-v1-java-repair-0462 | Criterion-positive rule dispatch selects exactly one matching callback per element and preserves callback exceptions without invoking the other rule. |
| 974 | exp-v1-java-repair-0464 | Static hold: newline joining uses character length as an interior-line counter, losing initial empty lines; opener, empty string, x, terminator yields x instead of newline+x. Not executed. |
| 975 | exp-v1-java-generation-0697 | Non-triviality hold: four literal scalar arithmetic operations delegated to checked standard-library wrappers with prescribed error translation. |

No new execution. Static findings are not executed results. Focused positives are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
