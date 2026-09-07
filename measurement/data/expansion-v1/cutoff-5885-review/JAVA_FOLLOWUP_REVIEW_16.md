# Java combined quality follow-up — batch 16

Positions226–240 of v14 Java queue1112, full prompt/reference read.
Twelve new holds: seven non-triviality, three static behavioral, two executed.
1565 total holds (1562 additive+3),3927 unique outside inspections. Resume241.

| Position | ID | Finding |
| --- | --- | --- |
| 226 | exp-v1-java-repair-0105 | Non-triviality hold: changes <= to < in the supplied bounded schedule loop; validation and widened increment are already present. |
| 227 | exp-v1-java-repair-0106 | Non-triviality hold: adds previous=current to the supplied two-state literal transition detector. |
| 228 | exp-v1-java-repair-0107 | Non-triviality hold: adds the unsigned-byte mask to the supplied slice-copy expression; all range and overflow checks are already supplied. |
| 229 | exp-v1-java-repair-0108 | Non-triviality hold: adds state=next to the supplied two-state literal callback detector. |
| 230 | exp-v1-java-generation-0159 | Criterion-positive immutable catalog admission, duplicate-bin rejection and ordered detached displays. Explicit trimmed-nonempty labels and add-time validation govern. |
| 231 | exp-v1-java-generation-0160 | Executed behavioral hold: snapshot sorts rendered key=value strings and returns [A0=y,A=x] for keys A and A0, violating key order despite the underlying TreeMap being correctly ordered. |
| 232 | exp-v1-java-generation-0163 | Criterion-positive synchronized dual identity registry and immutable snapshots; static hold: U+2003-only email registers despite blank-email rejection. ID exhaustion is not newly executed or adjudicated. |
| 233 | exp-v1-java-generation-0164 | Criterion-positive schema replacement, normalized duplicate checks and synchronized error/success logs; static hold: U+2003-only source or field passes nonblank validation. |
| 234 | exp-v1-java-generation-0165 | Executed behavioral hold: a non-owning observer sees holdCount zero while another thread owns the pair twice; contract asks total count. Additional static race: clearUnused can remove a retrieved lock before acquire reaches lockInterruptibly, allowing detached ownership and a second lock for the same pair. |
| 235 | exp-v1-java-generation-0166 | Non-triviality hold: literal score-threshold result wrapped in immutable interface/record boilerplate. Static behavior defect: U+2003-only factory target is accepted despite blank rejection. |
| 236 | exp-v1-java-generation-0167 | Non-triviality hold: scalar validated getters/setters, copy and explicitly supplied geometry formulas. Static behavior defect: U+2003-only shade accepted despite blank rejection; specified floating formulas are not independently held for overflow. |
| 237 | exp-v1-java-generation-0168 | Criterion-positive synchronized create/active/removed lifecycle and immutable geometry snapshots across movement. Contract restricts numeric arguments, not an additional finite-result invariant. |
| 238 | exp-v1-java-repair-0109 | Criterion-positive normalized identity repair before staged posting; static hold: U+2003-only account names pass nonblank validation. |
| 239 | exp-v1-java-repair-0110 | Non-triviality hold: changes <= to < in the supplied bounded attempt loop. Static behavior defect: U+2003-only allowed names pass and blank attempts produce UNKNOWN rather than INVALID. |
| 240 | exp-v1-java-repair-0111 | Criterion-positive callback exclusivity repair prevents true status from falling through into MALFORMED; synchronous invocation and listener exception propagation remain intact. |

Executed probes and matching -result.json receipts:
- java_0160_snapshot_order_probe.java: compile/run [0,1],2486ms,no timeout.
- java_0165_cross_thread_count_probe.java: compile/run [0,1],3004ms,no timeout.
Both pinned Java21.0.11, network disabled,1CPU,512MiB,64PIDs,60-second timeout.
Receipts preserve original task/reference, hashes and assertion outputs.
The lock-cleanup race is static analysis, not the executed count probe: acquire
retrieves L under MONITOR then pauses; clearUnused removes unlocked L; another
acquire creates L2; first acquire can own L while second owns L2. No private-field
access or new contract is needed. Probe only confirms total-count failure.
Other findings are static; focused positives are not admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
