# Java combined quality follow-up — batch 4

Positions46–60 of v14 Java queue1112 (identical ordering to v13), full
prompt/reference read. Eleven holds: four non-triviality, seven other static
behavior/contract findings.1450 total holds (1447 additive+3),3747 unique outside
inspections. Resume61. No new execution in this batch.

| Position | ID | Finding |
| --- | --- | --- |
| 46 | exp-v1-java-generation-0026 | Static hold: canonical numeric node tokens have no int bound in the prompt, but validToken rejects 2147483648; the valid tree 2147483648,*,* is rejected. |
| 47 | exp-v1-java-generation-0031 | Non-triviality hold: three literal tab-to-title/message mappings and a default error. |
| 48 | exp-v1-java-generation-0033 | Non-triviality hold: fixed prefix/whitespace/status guards and direct inclusive health-range classification; explicit whitespace scan covers U+2003. |
| 49 | exp-v1-java-generation-0034 | Criterion-positive: typed parsing preserves decimal scale, validates cross-field date ordering and normalizes parse exception classes; trim is explicit. |
| 50 | exp-v1-java-generation-0035 | Criterion-positive: uniqueness-checked ordered CSV/JSON serialization under constrained fields. The prompt's broad ASCII-letter wording versus specified email punctuation is left as an unadjudicated wording concern. |
| 51 | exp-v1-java-generation-0036 | Static hold: U+2003 endpoints accepted despite nonblank requirement; NUL-joined path keys also do not preserve elementwise lexicographic ordering for unrestricted names. |
| 52 | exp-v1-java-repair-0022 | Non-triviality hold: adds an else to exclude null from the already supplied IdentityHashMap. |
| 53 | exp-v1-java-repair-0023 | Non-triviality hold: direct floor-to-ceil primitive substitution. Static additional defect: two Long.MAX_VALUE samples are valid but Math.addExact throws instead of producing a report. |
| 54 | exp-v1-java-repair-0024 | Criterion-positive selective state preservation; static prompt/reference hold: U+2003-only Panel IDs remain accepted despite explicit nonblank requirement, beyond the claimed single repaired bug. |
| 55 | exp-v1-java-generation-0037 | Criterion-positive: validated scope filtering, frequency-to-rarity reduction and sorted set partitions with detached getters. |
| 56 | exp-v1-java-generation-0038 | Criterion-positive synchronized board; static hold: U+2003-only Card ID/label accepted by trim().isEmpty(). |
| 57 | exp-v1-java-generation-0039 | Criterion-positive menu snapshot and exact callback gating; static hold: U+2003-only option code/caption accepted despite nonblank requirement. |
| 58 | exp-v1-java-generation-0040 | Criterion-positive segmented cursor/capacity transitions; static contract/label hold: unlimited segment text can have unrepresentable int aggregate length and no stated overflow policy; length accumulation silently wraps. |
| 59 | exp-v1-java-generation-0042 | Criterion-positive ID assignment after validation and detached snapshots; static hold: U+2003-only title accepted despite nonblank requirement. |
| 60 | exp-v1-java-repair-0025 | Criterion-positive: captures invocation context into submitted tasks instead of reading the caller thread's ThreadLocal in workers. |

Static details: generation0036 equal-cost paths [S,A,Z] and [S,A\\u0000,Z]
have the opposite order after NUL joining; the short A element should sort first,
but its following Z compares after the extra NUL. Both names satisfy the stated
nonblank domain. This is not a claimed executed route result.
Generation0040 can append 4096 references to one 1,048,576-character string;
its mathematical length is 2^32, but int length becomes zero. No oversized
allocation or candidate execution was performed; missing representability policy
is recorded rather than inventing an error API.
Unicode findings use the same already executed U+2003 behavior, distinguished
from tasks explicitly requiring trim/nonempty. Focused positives are not full
seven-criterion passes or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
