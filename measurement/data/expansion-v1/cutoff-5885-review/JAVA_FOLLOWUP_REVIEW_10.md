# Java combined quality follow-up — batch 10

Positions136–150 of v14 Java queue1112, full prompt/reference read.
Twelve holds: seven non-triviality, four other static findings and one executed
rounding defect.1509 total holds (1506 additive+3),3837 unique outside
inspections. Resume151.

| Position | ID | Finding |
| --- | --- | --- |
| 136 | exp-v1-java-repair-0062 | Non-triviality hold: single loop-start literal 1-to-0 replacement with all parsing/counters supplied. |
| 137 | exp-v1-java-repair-0063 | Non-triviality hold: directly substitutes the prescribed final issuer field for subject. Static additional defect: U+2003-only certificate/anchor names pass nonblank validation. |
| 138 | exp-v1-java-repair-0064 | Non-triviality hold: substitutes the explicitly required OR for AND; U+2003 handler/approval names also remain accepted despite nonblank requirements. |
| 139 | exp-v1-java-generation-0094 | Criterion-positive same-state user identity and paired locker/credit-box creation; static hold: U+2003-only normalized email passes nonblank validation. |
| 140 | exp-v1-java-generation-0098 | Criterion-positive: password array ownership is protected at constructor/getter boundaries and authentication observes exact role/content. |
| 141 | exp-v1-java-generation-0099 | Non-triviality hold: direct canonical decimal/range guards followed by a two-field array projection. |
| 142 | exp-v1-java-generation-0100 | Criterion-positive: nested ordered pair search preserves lexicographic indices with widened subtraction avoiding false matches. |
| 143 | exp-v1-java-generation-0101 | Non-triviality hold: direct three-field projection with one suffix concatenation and null guards. |
| 144 | exp-v1-java-generation-0102 | Criterion-positive: ordered null-preserving record transformation changes only secret fields, dispatching the correct codec with unchanged error propagation. |
| 145 | exp-v1-java-repair-0065 | Executed hold: fitSize(100,100,29,29) returns [28,28], not the exact-floor [29,29]; binary floating rounding changes the required integer result. |
| 146 | exp-v1-java-repair-0067 | Criterion-positive transactional copy/commit repair; static contract/label hold: self-transfer bypasses the stated sufficient-funds condition, so balance0 with transfer{0,0,1} returns true. |
| 147 | exp-v1-java-generation-0103 | Criterion-positive explicit mentor-reference identity and validated mutable fields; static hold: U+2003-only contact name passes nonblank setter/constructor checks. |
| 148 | exp-v1-java-repair-0069 | Non-triviality hold: degree-conversion literal 360-to-180 replacement. Static additional defects: finite maximum radians overflow before normalization and tiny negative degrees can round to forbidden 360. |
| 149 | exp-v1-java-repair-0070 | Criterion-positive snapshot-and-clear repairs skipped FIFO entries; static hold: U+2003-only submitted message remains accepted despite nonblank requirement. |
| 150 | exp-v1-java-repair-0071 | Non-triviality hold: direct comparator direction replacement; complete Unicode totals, tie policy and copying are already supplied. |

Executed java_repair_0065_exact_floor_probe-result.json: Java21.0.11,
2362 ms, exit codes [0,1], no timeout. The assertion reports [28,28];
compilation succeeded. Network-disabled/resource-limited sandbox, original
reference/task and hashes retained. No other new execution in this batch.
The self-transfer finding is a conflict with the prompt's sufficient-funds
conjunction; it does not introduce a new debit/credit requirement for valid
self-transfers. Static whitespace findings use established U+2003 behavior.
Focused positives are not admission or full seven-criterion approval.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

