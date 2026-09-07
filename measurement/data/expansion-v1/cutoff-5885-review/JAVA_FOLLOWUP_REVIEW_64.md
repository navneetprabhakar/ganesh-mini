# Java combined quality follow-up — batch 64

Positions946–960 of v14 Java queue1112, full prompt/reference read.
Twelve new holds: eight non-triviality and four static findings.
1953 total holds (1950 additive+3),4647 unique outside inspections. Resume961.
Approved versioned recovery remains pending; original corpus unchanged.

| Position | ID | Finding |
| --- | --- | --- |
| 946 | exp-v1-java-generation-0678 | Static hold: U+2003-only key/name/release and lookup key remain blank after trimming but pass required validation. Not executed. |
| 947 | exp-v1-java-repair-0449 | Non-triviality hold: direct OR-to-AND substitution for an explicitly prescribed two-enum boolean predicate. |
| 948 | exp-v1-java-repair-0450 | Criterion-positive decimal interpretation boundary replaces prefix-sensitive decode so leading-zero decimal strings do not become octal and hexadecimal prefixes are rejected. |
| 949 | exp-v1-java-repair-0452 | Non-triviality hold: prescribed empty-list branch or final-entry string concatenation on supplied validated input. |
| 950 | exp-v1-java-generation-0673 | Static hold: U+2003-only account ID passes required nonblank validation. Same-account identity wording and sequence-overflow boundaries need separate recovery review; not executed. |
| 951 | exp-v1-java-generation-0681 | Non-triviality hold: one delimiter check, two literal status mappings and a fixed malformed-result DTO. |
| 952 | exp-v1-java-generation-0682 | Non-triviality hold: directly transcribes prescribed scalar pre-increment, short-circuit constants and two follow-up increments. |
| 953 | exp-v1-java-generation-0683 | Non-triviality hold: scalar threshold filter followed by a single DTO property projection with independent null guards. |
| 954 | exp-v1-java-generation-0684 | Criterion-positive per-entry deep snapshot breaks both caller payload aliases and shared-payload aliases between distinct output records. |
| 955 | exp-v1-java-repair-0453 | Non-triviality hold: elementary string repetition loop endpoint change from <= to <. |
| 956 | exp-v1-java-repair-0455 | Non-triviality hold: substitutes the correct field into a prescribed literal toString format. |
| 957 | exp-v1-java-repair-0456 | Non-triviality hold: subtracts one from each last-element array index; all validation is supplied. |
| 958 | exp-v1-java-generation-0685 | Criterion-positive cumulative dependency across changes with checked long arithmetic, translated overflow exception and detached prefix-level output. |
| 959 | exp-v1-java-generation-0686 | Static hold: U+2003-only recognized values do not receive the required blank fallback. Also fixed three-key projection; not executed. |
| 960 | exp-v1-java-generation-0687 | Static hold: non-null DELETE permission collections containing null/nonpositive IDs are never validated, despite unqualified invalid-ID/null-entry rejection; only null DELETE permissions were exempted. Not executed. |

No new execution. Static findings are not executed results. Focused positives are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
