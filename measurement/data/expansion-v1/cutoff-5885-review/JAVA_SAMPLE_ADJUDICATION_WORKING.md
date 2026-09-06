# Java sample criterion adjudication — working, 2026-09-07

The original 60 Java sample records remain unchanged. SECOND_BATCH_REVIEW.md
and THIRD_BATCH_REVIEW.md preserve full initial prompt/reference/test/known-bad
inspection notes. The all-300 origin trace remains evidence for independent
test authorship, not correctness. No Java all-seven approval is issued here.

## Reproduced Unicode-blank contract gaps

Five generation records use trim().isEmpty() for a nonblank/non-whitespace
requirement. Each probe first verifies Character.isWhitespace(U+2003) in the
pinned runtime, then exercises the stated API. All compile and fail normally
with exit codes [0,1], timed_out=false, using pinned Java21.0.11, network disabled
and resource limits. These Java probes replace SolutionTest.java; original tests
are preserved in receipts but are not rerun by these diagnostics.

| Generation ID | Observed outcome | Duration ms | Probe/result stem |
| --- | --- | ---: | --- |
| 0619 | Whitespace-only article title accepted despite requiring a non-whitespace character. | 3745 | java_0619_unicode_blank_probe |
| 0032 | Whitespace-only product name accepted despite nonblank constructor requirement. | 3349 | java_0032_unicode_blank_probe |
| 0185 | Whitespace-only item title accepted on upsert despite invalid-item rejection. | 3525 | java_0185_unicode_blank_probe |
| 0689 | Whitespace-only Member label accepted despite blank-argument rejection. | 2984 | java_0689_unicode_blank_probe |
| 0737 | Whitespace-only credential owner returned despite nonblank owner requirement. | 2925 | java_0737_unicode_blank_probe |

Each stem has .java source and -result.json full evidence. These add five holds:
1094 additive plus historical three = 1097. Existing Java holds remain 0549,
0080, 0514, 0794 and repair0325. The five new probes exercise the original sample,
so outside-sample inspection count stays 2960. They do not claim NPE/IAE
counterexamples, generalized Unicode normalization failures or unchanged tests.

The repeated generation pattern requires a new scope version reopening both
Java generation histories, population720 including 36 frozen sample records;
684 outside-sample records need focused disposition. Scope v7 remains historical.

## Further cases already reread, pending criterion decisions

Full prompt/reference rereads: generation0619/0305 (null exception wording),
0652 (getter API and decimal grammar), 0032 (abbreviated read signature),
0270/0271 (elementary generation), 0689 (inheritance/boilerplate), 0185 and0737
(blank validation above); repair0014/0130/0219/0222/0305 (non-triviality),
repair0270 (private-field reflection in original tests), repair0058 (concurrent
mutation/snapshot scope), generation0738 (alias-value normalization).

Do not mechanically equate patch size with task difficulty. The inherited full
source may resolve a repair's terse prose, while exact prescribed helper calls
can make a whole target elementary. Conversely, field layouts private to a valid
alternative implementation should not become mandatory merely through tests.
No new hold or positive decision beyond the five reproduced cases is implied
by this working note. Complete remaining Java criterion decisions next.

Candidate SHA:
680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
