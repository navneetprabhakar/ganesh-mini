# Java combined quality follow-up — batch 72

Positions1066–1080 of v14 Java queue1112, full prompt/reference read.
Eight new holds: three non-triviality and five static behavioral/contract findings.
2004 total holds (2001 additive+3),4767 unique outside inspections. Resume1081.
Approved versioned recovery remains pending; original corpus unchanged.

| Position | ID | Finding |
| --- | --- | --- |
| 1066 | exp-v1-java-repair-0508 | Criterion-positive primary-only priority reversal preserves ascending listener tie ordering within each event's topic-matched notification sequence. |
| 1067 | exp-v1-java-generation-0762 | Static hold: extra separators are accepted as part of URL; title|url|extra is admitted despite exactly one separator. Not executed. |
| 1068 | exp-v1-java-generation-0763 | Static hold: U+2003-only ledger text passes required blank rejection. Synchronized state/snapshot operations otherwise preserve concurrency boundaries; not executed. |
| 1069 | exp-v1-java-generation-0764 | Criterion-positive index-ordered backtracking copies each completed combination independently and handles the zero-selection base case. |
| 1070 | exp-v1-java-generation-0765 | Static contract hold: unqualified whitespace-separated clauses use ASCII-default regex whitespace/trim, rejecting team U+2003 EQ U+2003 value. Clarify whitespace domain before recovery; not executed. |
| 1071 | exp-v1-java-generation-0766 | Criterion-positive structural/symmetry validation precedes parent-aware DFS cycle detection across disconnected components. |
| 1072 | exp-v1-java-generation-0768 | Criterion-positive length-framed category preserves embedded delimiters and canonical numeric roundtrips; malformed/overflowed bounds become the required IllegalArgumentException. |
| 1073 | exp-v1-java-repair-0509 | Criterion-positive runtime type filter replaces unsafe String narrowing while retaining checked length accumulation and ignoring unsupported values. |
| 1074 | exp-v1-java-repair-0510 | Criterion-positive copy-before-volatile-publication closes the caller mutation channel; snapshot copies separately protect readers from mutating stored state. |
| 1075 | exp-v1-java-repair-0511 | Non-triviality hold: guarded hashCode-to-floorMod library wrapper, consistent with earlier single-bucket-index holds. |
| 1076 | exp-v1-java-generation-0769 | Criterion-positive bounded repeated digit-square transition counts replacements with correct initial-one and exhausted-budget behavior. |
| 1077 | exp-v1-java-generation-0770 | Non-triviality hold: directly transcribes the fully specified cell formula using prescribed exact-arithmetic wrappers. |
| 1078 | exp-v1-java-generation-0772 | Static contract hold: arbitrary String elements may contain newlines, but formatter emits them raw despite requiring one indented line per string element; continuation lines are unindented. Freeze multiline escaping/indent semantics before recovery. Not executed. |
| 1079 | exp-v1-java-generation-0774 | Non-triviality hold: directly prescribed scalar capacity formulas and overload comparison with independent finite/range guards. |
| 1080 | exp-v1-java-repair-0513 | Static contract hold: prose declares applyRefresh(int[]) while supplied and returned source expose String[]; nonblank tile validation also accepts U+2003-only IDs. Resolve signature mismatch before recovery; not executed. |

No new execution. Static findings are not executed results. Focused positives are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
