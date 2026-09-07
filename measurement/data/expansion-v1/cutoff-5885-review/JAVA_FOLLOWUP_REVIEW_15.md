# Java combined quality follow-up — batch 15

Positions211–225 of v14 Java queue1112, full prompt/reference read.
Four new non-triviality holds; eleven focused criterion positives.
1553 total holds (1550 additive+3),3912 unique outside inspections. Resume226.

| Position | ID | Finding |
| --- | --- | --- |
| 211 | exp-v1-java-generation-0149 | Criterion-positive canonical UTF-16 length parsing rejects leading zeros and overflow before slicing, handles arbitrary payload characters and consumes complete records. |
| 212 | exp-v1-java-generation-0150 | Non-triviality hold: directly transcribes the fixed four-level lookup fallback policy with a simple minimum-key scan and null checks. |
| 213 | exp-v1-java-repair-0098 | Non-triviality hold: changes the comma guard from i>1 to i>0 in a fully supplied formatter. |
| 214 | exp-v1-java-repair-0100 | Non-triviality hold: deletes the state assignment in the explicitly no-op SKIP branch of a supplied transition table. |
| 215 | exp-v1-java-generation-0151 | Criterion-positive consecutive-run state, transition flush and final-run flush preserve order with checked counts and independent result. |
| 216 | exp-v1-java-generation-0152 | Criterion-positive stack nesting invariant distinguishes unmatched, mismatched and unclosed bracket types while ignoring other characters. |
| 217 | exp-v1-java-generation-0153 | Criterion-positive exact command grammar and staged sequential updates with final int bounds and ordered detached result. Positive long overflow yields a negative rejected value, not an accepted wrapped int. |
| 218 | exp-v1-java-generation-0154 | Criterion-positive one-pass placeholder grammar preserves absent placeholders and treats replacements literally without rescanning, with full map-null validation. |
| 219 | exp-v1-java-repair-0101 | Non-triviality hold: changes the initial loop index from one to zero in a complete first-match search. |
| 220 | exp-v1-java-repair-0102 | Criterion-positive escaping repair separates source traversal from generated entity text, avoiding double escaping while preserving remaining UTF-16 code units. |
| 221 | exp-v1-java-repair-0103 | Criterion-positive signed-magnitude repair widens before abs, covering MIN_VALUE while retaining the positive-wins tie invariant. |
| 222 | exp-v1-java-generation-0155 | Criterion-positive bounded run grammar and total-size invariant reject malformed counts, empty segments and surrogate payloads before expanding. |
| 223 | exp-v1-java-generation-0158 | Criterion-positive atomic normalized duplicate detection and replacement with copies at both array boundaries. Explicit trimmed-nonempty validity definitions govern; no stronger Unicode-blank rule imposed. |
| 224 | exp-v1-java-generation-0161 | Criterion-positive copied credential storage and full maximum-length comparison with length mismatch folded into the result; no timing-independent machine-code guarantee is claimed. |
| 225 | exp-v1-java-generation-0162 | Criterion-positive deterministic expiry boundary, normalized replacement and sorted fresh snapshots; firstEmptyStep derives the maximum expiry without overflow-prone stepping. |

No new execution. Positives are focused review findings, not seven-criterion
approval or training admission. Explicit normalization definitions are preserved.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
