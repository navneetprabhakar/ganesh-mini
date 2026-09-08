# R5 terminal correction and admission — 2026-09-08

Main fully read both r5 review reports and checked selected candidate file hashes
against them. All11 corrections preserve r3 spec/reference/mutant bytes. Actual
33 serial diagnostic executions completed: JS5 and TS0022/0140/0261/0270/0281
pass reference/mutant/original directionality. TS0195 fails allthree behaviorally
because its new mapper-identity oracle is unsupported; it also asserts absence of
unspecified extras. Preserve held; no automatic repeated critic or reference edit.

Explicit selected10 preparation compares3073 retained originals and11 previous
hash-bound recoveries: zero overlap. Fresh candidate admission checks546 evaluation
files and reruns references and supplied mutants serially in pinned network-disabled
resource-limited sandboxes. Accepted10/rejected0, candidate status passed,
balance_passed=false. This is not a corpus/training seal.

Output measurement/data/expansion-v1/recovery-admission/r5-ten-v1/admitted.jsonl
bytes79389; SHA4b6510fb3a66f230a93e97c306568240a63d11a2ffdb204a9ffd81c6be768aea.
Admission logical sealdbe60b404f706f3c5b9c290bd595d42128f14e763639e23b3e56336d9a83de86.
Total new recoveries admitted21: Go2,Java2,JS9,TS7,Python1,Rust0; allgeneration.
Original holds2812 unchanged; maximum3073+21=3094; minimum additional906 to4000
before further exclusions/token balancing. No original unique coverage added.

R4 Go initial diagnostics completed27executions:0774/0522 allthree behavioral
failures on unsupported oracles; other7 allthree pass, showing missing defect
coverage. Main integrated its full review; r7 is the one bounded test correction.
R4 Java prompt guard failure remains intact; r8 is a fresh immutable retry.

R6 generation completed11; main fully read Python/Rust reports: scoped positives
Python0269/0314/0319,Rust0757. Six test-only holds go to one bounded r9 correction.
Rust0704 retains a real zero-area copy-loop reference defect; don't weaken its valid
zero-width/huge-height test or include it in test-only correction. Original r6
diagnostics are running and must be preserved separately. No executed r6 outcome
is inferred from these static decisions.
