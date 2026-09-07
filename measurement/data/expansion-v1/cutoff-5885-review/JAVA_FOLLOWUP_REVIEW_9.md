# Java combined quality follow-up — batch 9

Positions121–135 of v14 Java queue1112, full prompt/reference read.
Eight new holds: four non-triviality and four static Unicode-blank findings.
1497 total holds (1494 additive+3),3822 unique outside inspections. Resume136.

| Position | ID | Finding |
| --- | --- | --- |
| 121 | exp-v1-java-generation-0079 | Criterion-positive: validation precedes monotone ID assignment; immutable status replacement and Optional lookup preserve state. |
| 122 | exp-v1-java-generation-0082 | Non-triviality hold: two literal message formatter wrappers and command dispatch. Static additional defect: U+2003-only message passes required non-whitespace validation. |
| 123 | exp-v1-java-generation-0086 | Non-triviality hold: direct credential pair equality with prescribed validation and exception message. |
| 124 | exp-v1-java-repair-0057 | Non-triviality hold: one duplicated wire-code literal 8-to-9 replacement. |
| 125 | exp-v1-java-repair-0059 | Non-triviality hold: direct exact-class-to-instanceof primitive replacement. |
| 126 | exp-v1-java-generation-0085 | Criterion-positive: full batch validation before any generated IDs/state mutations, stable host filtering and immutable snapshots; isBlank handles Unicode. |
| 127 | exp-v1-java-generation-0087 | Criterion-positive: validated append/update distinction and immutable insertion-order equipment snapshots; isBlank handles labels. |
| 128 | exp-v1-java-generation-0089 | Criterion-positive: nested rate snapshots, selected-input fallback and apply-before-state-commit controller transitions. |
| 129 | exp-v1-java-generation-0090 | Criterion-positive: combined operation validates both heights before either state change, preserving failure atomicity. |
| 130 | exp-v1-java-generation-0091 | Criterion-positive bounded savings ledger; static hold: U+2003-only IDs/labels pass explicitly nonblank-after-trimming validation. |
| 131 | exp-v1-java-generation-0092 | Criterion-positive atomic row snapshot and stable generation; static hold: U+2003-only job title passes nonblank validation. |
| 132 | exp-v1-java-generation-0093 | Criterion-positive normalized immutable license copies and selective update; static hold: U+2003-only code/title passes nonblank validation. |
| 133 | exp-v1-java-generation-0095 | Criterion-positive: rebuilds sparse level links with constant live auxiliary state, disregarding stale peer pointers and terminating each level. |
| 134 | exp-v1-java-generation-0096 | Criterion-positive: encoding-dependent separator invariants, immutable replacement and sorted snapshots; no unspecified scalar-Unicode separator rule added. |
| 135 | exp-v1-java-repair-0061 | Criterion-positive: deleting only empty topic buckets preserves other subscriptions; static hold: U+2003-only topic/client remains accepted despite nonblank requirements. |

No new execution. Unicode findings preserve the distinction between explicit
nonblank requirements and APIs requiring only a nonempty String.trim result.
Generated records used as operation inputs are not automatically assumed to
require constructor-time validation when the public operation validates them.
Focused positives are not admission or full seven-criterion approval.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

