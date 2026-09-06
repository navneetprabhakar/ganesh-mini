# Go focused non-triviality review — batch 10

Positions136–150, full prompt/reference read; not a full new test/mutant review.
Nine criterion-positive, six non-triviality holds plus one behavioral hold.
1218 total holds (1215 additive+3),3080 unique outside inspections. Resume151.

| Position | ID | Finding |
| --- | --- | --- |
| 136 | exp-v1-go-repair-0072 | Criterion-positive: recursive quotient must decrease while remainder preserves radix digit order, ensuring bounded recursion over uint64. |
| 137 | exp-v1-go-generation-0116 | Criterion-positive: tagged storage, wrong-type errors and two-way slice ownership with nil/empty distinction. |
| 138 | exp-v1-go-generation-0117 | Non-triviality hold: fully prescribed fixed-byte masks and fixed-position hex formatting around library conversion. |
| 139 | exp-v1-go-generation-0119 | Criterion-positive: collection-local uniqueness, validation before insertion and independent ordered copies. |
| 140 | exp-v1-go-repair-0077 | Non-triviality hold: directly add the disclosed missing third arithmetic pairing. |
| 141 | exp-v1-go-repair-0078 | Non-triviality hold: direct maximum comparison reversal with rune counting already supplied. |
| 142 | exp-v1-go-repair-0079 | Non-triviality hold: direct loop-start correction from one to zero. |
| 143 | exp-v1-go-repair-0080 | Non-triviality hold: direct comma-to-pipe literal in supplied splitter branch. |
| 144 | exp-v1-go-generation-0121 | Criterion-positive catalog; executed behavioral hold for distinct tuple collision and valid pagination overflow panic. |
| 145 | exp-v1-go-generation-0122 | Criterion-positive: recipe validation, zero-value initialization and nested slice ownership on storage and retrieval. No explicit preservation of non-nil-empty ingredient/tag shape. |
| 146 | exp-v1-go-generation-0123 | Criterion-positive: global observation identity, per-sensor aggregation and nil/zero-value semantics. Huge observation-count sum overflow is not a feasible executed probe here. |
| 147 | exp-v1-go-generation-0125 | Criterion-positive: ordered validation precedence, presence distinct from empty occupant and atomic two-key relocation. |
| 148 | exp-v1-go-generation-0126 | Criterion-positive: stable existing assignments, deterministic shard mapping and explicit released-state sentinel distinct from zero epoch. No private worker-removal injection. |
| 149 | exp-v1-go-repair-0082 | Non-triviality hold: explicitly disclosed library encoding selector replacement. |
| 150 | exp-v1-go-repair-0084 | Criterion-positive: matching top-of-stack delimiter type is a substantive nested parser invariant, not depth alone. |

go_0121_catalog_boundaries_probe-result.json: Go1.22.12 exit[1], no timeout,
26621ms. Both subtests ran: distinct non-empty tuples containing NUL collapse to
one entry; List(1,MaxInt) over two entries panics because offset+limit wraps.
The latter panic is caught in the test to retain both findings.
Additive test ran alongside original tests, not a separate known-bad rerun.
Network off,1CPU/512MiB/64PIDs/60s; task, code and output hashes retained.
Candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
