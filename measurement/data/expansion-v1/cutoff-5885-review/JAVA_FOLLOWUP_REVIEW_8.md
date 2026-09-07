# Java combined quality follow-up — batch 8

Positions106–120 of v14 Java queue1112, full prompt/reference read.
Eight new holds: five non-triviality and three static Unicode-blank findings.
1489 total holds (1486 additive+3),3807 unique outside inspections. Resume121.

| Position | ID | Finding |
| --- | --- | --- |
| 106 | exp-v1-java-generation-0075 | Non-triviality hold: direct map credential lookup/equality with prescribed null validation. |
| 107 | exp-v1-java-generation-0076 | Criterion-positive: atomic add/update semantics preserve message fields and nonnegative time subtraction avoids overflow. |
| 108 | exp-v1-java-generation-0077 | Criterion-positive: validates map-key/account identity across the entire input before ordered access decisions. |
| 109 | exp-v1-java-generation-0078 | Criterion-positive: synchronized registration/login/profile state preserves original credentials and prior login state on failures. |
| 110 | exp-v1-java-repair-0049 | Criterion-positive: logical prefix length governs both allocation and transform bounds, excluding unused backing-buffer bytes. |
| 111 | exp-v1-java-repair-0050 | Non-triviality hold: removes a literal minus-one from the supplied distinct-item limit check. |
| 112 | exp-v1-java-repair-0051 | Criterion-positive: advances the tree frontier from each current parent rather than repeatedly selecting from the root. |
| 113 | exp-v1-java-repair-0052 | Criterion-positive: visit marking before descent restores cycle termination while retaining zero-edge reachability. |
| 114 | exp-v1-java-generation-0081 | Criterion-positive ordered set snapshots; static hold: U+2003-only add/remove/contains values pass normalization despite explicit blank-value rejection. |
| 115 | exp-v1-java-generation-0083 | Non-triviality hold: direct bounded age parsing and prescribed three-outcome admission/message table. |
| 116 | exp-v1-java-generation-0084 | Criterion-positive: normalized-key replacement retains insertion order and snapshot filtering. Direct record-constructor constraints are not newly adjudicated. |
| 117 | exp-v1-java-repair-0053 | Non-triviality hold: removes a first-result guard so the supplied accumulator retains the last status. |
| 118 | exp-v1-java-repair-0054 | Criterion-positive ordered per-key list merge; static hold: U+2003-only keys still pass nonblank validation. |
| 119 | exp-v1-java-repair-0055 | Non-triviality hold: substitutes the standard prescribed ceiling-division adjustment into an already overflow-safe BigInteger formula. |
| 120 | exp-v1-java-repair-0056 | Criterion-positive attachment constructor copy fixes input ownership; static hold: U+2003-only document title/name remains accepted despite explicit nonblank requirements. |

No new execution. Static blank findings use U+2003, which trim() does not remove.
State/ownership/graph-invariant repairs remain criterion-positive even when the
source edit is small; literal/comparator or direct formula substitutions alone
do not gain non-triviality from surrounding supplied boilerplate.
Focused positives are not admission or full seven-criterion approval.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

