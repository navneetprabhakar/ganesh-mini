# Java combined quality follow-up — batch 11

Positions151–165 of v14 Java queue1112, full prompt/reference read.
Twelve holds: two non-triviality and ten static behavioral/contract findings.
1521 total holds (1518 additive+3),3852 unique outside inspections. Resume166.

| Position | ID | Finding |
| --- | --- | --- |
| 151 | exp-v1-java-generation-0104 | Criterion-positive synchronized lifecycle and shard snapshots; static hold: U+2003-only Config key is accepted, making a blank lookup return a registered entry despite required absence. |
| 152 | exp-v1-java-generation-0105 | Criterion-positive: resumable per-tick cursor, next-due-before-callback update and captured eligible count handle callback additions/exceptions. Callback-triggered stop/reentrant advance semantics are not newly adjudicated. |
| 153 | exp-v1-java-generation-0106 | Criterion-positive exact ledger totals and locale-root distribution; static hold: U+2003-only description is accepted despite nonblank requirement. |
| 154 | exp-v1-java-generation-0107 | Criterion-positive: token grammar, exact aggregation and grouped free-unit arithmetic preserve first occurrence order. |
| 155 | exp-v1-java-generation-0108 | Criterion-positive binary/state codec; static contract/label hold: decode(null) uses requireNonNull and throws NullPointerException despite the specific decoding requirement naming IllegalArgumentException; the final generic null-object sentence conflicts with that requirement. |
| 156 | exp-v1-java-generation-0109 | Non-triviality hold: directly transcribes scalar min/max selection and a two-stage floor formula with widened multiplication. |
| 157 | exp-v1-java-generation-0110 | Criterion-positive normalized independent ordered sets; static hold: U+2003-only competencies pass blank validation. |
| 158 | exp-v1-java-generation-0112 | Criterion-positive normalized key/value identity and collision checks; static hold: U+2003-only code/title/creator pass nonblank-after-trimming requirements. |
| 159 | exp-v1-java-generation-0113 | Criterion-positive globally unique normalized venues and deeply frozen snapshots; static hold: U+2003-only group/venue names pass blank validation. |
| 160 | exp-v1-java-generation-0114 | Criterion-positive complete registry validation and dual email/ID conflict handling before mutation; static hold: U+2003-only applicant fields pass nonblank validation. |
| 161 | exp-v1-java-repair-0075 | Criterion-positive nested-list snapshot repair; static hold: source Map.of("x",List.of(1)) throws from contains(null), rejecting valid immutable list input. |
| 162 | exp-v1-java-repair-0076 | Non-triviality hold: deletes the directly prohibited RECEIVE branch from a supplied literal transition table. |
| 163 | exp-v1-java-generation-0115 | Criterion-positive insertion-position-preserving rename and immutable snapshots; static hold: U+2003-only asset/new key accepted despite nonblank requirement. |
| 164 | exp-v1-java-generation-0116 | Criterion-positive ordered aggregate validation; static hold: valid display name A+U+2003+B is treated as one part because default regex whitespace does not match U+2003. |
| 165 | exp-v1-java-generation-0117 | Criterion-positive sparse Dijkstra with stale-entry filtering, full edge validation and long distance arithmetic. |

No new execution. The nested-list null-query failure propagates the executed
List.of counterexample from Java batches1–3; this row itself was not run.
Unicode findings distinguish actual nonblank/whitespace contracts from merely
nonempty text. The codec conflict is held for contract/label review, not resolved
by silently changing an exception contract. No new scheduler reentrancy rule.
Focused positives are not admission or full seven-criterion approval.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

