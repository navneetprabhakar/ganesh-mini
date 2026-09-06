# Go focused non-triviality review — batch 11

Positions151–165, full prompt/reference read; not a full new test/mutant review.
Ten criterion-positive, five non-triviality holds plus two contract/behavior holds.
1225 total holds (1222 additive+3),3095 unique outside inspections. Resume166.

| Position | ID | Finding |
| --- | --- | --- |
| 151 | exp-v1-go-generation-0127 | Criterion-positive: unique-version ordered planning, independent output and full prevalidation before resetting collections. |
| 152 | exp-v1-go-generation-0132 | Criterion-positive report ownership/aggregation; static range-contract hold: two successful MaxInt64 waits are constructor-valid, but their total cannot be represented by required int64 Total; no overflow/error policy is provided. Not an executed result. |
| 153 | exp-v1-go-repair-0085 | Non-triviality hold: direct maximum comparator reversal. |
| 154 | exp-v1-go-repair-0087 | Non-triviality hold: disclosed revision literal correction from nine to ten. |
| 155 | exp-v1-go-generation-0133 | Criterion-positive scoped registry; executed behavioral hold for distinct scope/name NUL tuple collision. |
| 156 | exp-v1-go-generation-0134 | Criterion-positive: independent member/note sequences, referential integrity and detached joined views. No feasible ID-exhaustion execution claimed. |
| 157 | exp-v1-go-generation-0135 | Criterion-positive: registered pair identity, strict trailing/unknown-field checks and message validation. Standard Go JSON matching is not an expressly forbidden case-normalization policy. |
| 158 | exp-v1-go-repair-0089 | Non-triviality hold: direct missing square factor in supplied formula. |
| 159 | exp-v1-go-repair-0090 | Criterion-positive: ownership separation before in-place filtering/sorting/deduplication while preserving nil and non-nil results. |
| 160 | exp-v1-go-repair-0091 | Criterion-positive: endpoint multiplicity validation is distinct from first-match lookup; ordered interior copy remains detached. |
| 161 | exp-v1-go-repair-0092 | Non-triviality hold: direct inclusive logger threshold comparison. |
| 162 | exp-v1-go-generation-0139 | Criterion-positive: identity-preserving replacement, nested tags ownership and sorted owner views. |
| 163 | exp-v1-go-generation-0140 | Criterion-positive: full NUL prevalidation, all-occurrence substitution, no-match fallback and detached ordered argument storage. |
| 164 | exp-v1-go-generation-0141 | Non-triviality hold: fully disclosed literal route/reply table with direct method guard. |
| 165 | exp-v1-go-generation-0143 | Criterion-positive: accumulating framed bytecode, register validation before append, little-endian address layout and independent byte snapshots. |

go_0133_component_tuple_probe-result.json: Go1.22.12 exit[1], no timeout,
26494ms. Create(name=b NUL c,scope=a) then Create(name=c,scope=a NUL b)
rejects the distinct second tuple as a duplicate. All inputs satisfy non-empty rules.
Additive test ran alongside original tests, not a separate known-bad rerun.
Network off,1CPU/512MiB/64PIDs/60s; task, code and output hashes retained.
Candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
