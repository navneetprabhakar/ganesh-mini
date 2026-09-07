# Java combined quality follow-up — batch 67

Positions991–1005 of v14 Java queue1112, full prompt/reference read.
Five new holds: one non-triviality and four static behavioral/contract findings.
1974 total holds (1971 additive+3),4692 unique outside inspections. Resume1006.
Approved versioned recovery remains pending; original corpus unchanged.

| Position | ID | Finding |
| --- | --- | --- |
| 991 | exp-v1-java-generation-0709 | Criterion-positive bounded command interpreter preserves duplicate stored codes, capacity behavior and STOP termination with detached output. |
| 992 | exp-v1-java-generation-0710 | Static hold: batchSize=Integer.MAX_VALUE makes first start+batchSize overflow from start=1 even for a two-line catalog, then start wraps negative. Not executed. |
| 993 | exp-v1-java-generation-0711 | Criterion-positive validated immutable add/update/filter snapshots preserve replacement identity and original order; String.isBlank correctly handles blank kinds. |
| 994 | exp-v1-java-generation-0712 | Static contract hold: exact uuuu-MM-dd wording needs a frozen year-width interpretation; formatter roundtrip accepts extended signed +10000-01-01 rather than only four-digit dates. Clarify before recovery; not executed. |
| 995 | exp-v1-java-repair-0473 | Criterion-positive key-versus-value membership repair makes existence validation consistent with the subsequent map lookup after whole-map validation. |
| 996 | exp-v1-java-repair-0474 | Criterion-positive invalidation removes requested keys rather than incorrectly treating Integer values as keys, preserving detached insertion order. |
| 997 | exp-v1-java-generation-0713 | Criterion-positive inventory key/asset identity validation and immutable borrow/restore transitions preserve no-change cases and map order. |
| 998 | exp-v1-java-generation-0715 | Criterion-positive immutable monotonic renewal and inclusive date activity with exact-one-at-sign validation; contract explicitly rejects strings empty after trim, not general Unicode blanks. |
| 999 | exp-v1-java-generation-0716 | Criterion-positive overflow-safe slice count, bounded start/count arithmetic and copied list structure preserve pagination and shallow item ownership. |
| 1000 | exp-v1-java-generation-0717 | Static hold: secret letter/digit checks iterate UTF-16 chars, rejecting a valid supplementary Unicode letter followed by sufficient ASCII digits; no ASCII-only letter restriction is specified. Not executed. |
| 1001 | exp-v1-java-generation-0718 | Non-triviality hold: independent literal band/command mappings and directly prescribed fixed-index clamp formulas. |
| 1002 | exp-v1-java-generation-0719 | Static contract hold: unqualified surrounding whitespace/whitespace-only line acceptance is implemented with trim; U+2003-only line is rejected instead of skipped. Clarify whitespace domain before recovery; not executed. |
| 1003 | exp-v1-java-generation-0720 | Criterion-positive bundle includes distinct top-two sentinel management, ordered repeated-run detection and Long.MIN_VALUE-safe digit counting; focused arithmetic and ownership checks found no defect. |
| 1004 | exp-v1-java-repair-0477 | Criterion-positive access-order cache mode restores recency updates on both GET and PUT, which determine later eviction order. |
| 1005 | exp-v1-java-repair-0479 | Criterion-positive top-of-stack comparison restores SINGLE_TOP idempotency without confusing the bottom element with current state. |

No new execution. Static findings are not executed results. Focused positives are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
