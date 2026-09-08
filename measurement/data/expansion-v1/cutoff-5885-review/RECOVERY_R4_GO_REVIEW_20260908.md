# R4 Go recovery static review — 2026-09-08

Scope: complete prompts, references, test files and supplied mutants for all nine completed Go candidates in `datasets/cache/expansion-v1/versioned-recovery/r4`, against their approved plan entries. No candidate execution, generation, cloud operation, central edit or admission was performed. Zero new original-row review credit. The Java prompt-guard failure does not invalidate intact, independently bound Go lane artifacts.

## Outcome

All nine derived rows remain **HOLD for test qualification**, despite scoped-positive intended reference corrections. None contains a valid direct distinguishing witness for its supplied original-defect mutant. 0522 and 0774 additionally have unsupported oracles; 0720's exact skipped/executable interleaving expectations exceed the approved scope. These are static findings, not executed pass/fail results. No recommendation to alter correct references merely to satisfy unsupported tests.

| Suffix (all `exp-v1-recovery-r4-go-generation-`) | Reference correction / whole-target assessment | Test disposition and minimal bounded correction |
| --- | --- | --- |
| 0330 | Positive: map equality checks key presence and value; copies caller labels and conditions; preserves reconciliation priorities. Stateful create/delete/update/no-op plus ownership is substantive. | HOLD: no equal-sized maps with distinct nonempty keys and empty values. Add desired `{"desired":""}` versus current `{"existing":""}` with same name, require update; matching empty-valued keys require none. Existing different nonempty values do not distinguish the mutant. |
| 0439 | Positive: two-string structural key prevents NUL delimiter collisions; Apply locks state and Snapshot copies under read lock then sorts. Watch/leader/validation/order/ownership remain substantive. | HOLD: tests contain no embedded NUL identifiers. Insert `(a\x00b,c)` and `(a,b\x00c)`, verify both records and independent replacement/deletion. Concurrency assessment below. |
| 0499 | Positive: incremental `used` allocation permits early success for huge logical attempt limits; saturation, final-error identity, panic propagation and validation retained. This is callback lifecycle/ordering, not merely doubling arithmetic. | HOLD: largest attempts in tests is five; MaxInt is used only as starting weight. Add `RunWeighted(MaxInt,1,first-call-success)` requiring exactly one callback and `[1],nil`. Do not run MaxInt callbacks. |
| 0514 | Positive: all nonpositive IDs checked before any existence lookup, then all existence checked before mutation. Atomic batch deletion, CRUD and ordered filtering retain substantive interactions. | HOLD: separate `[existing,0]` and `[existing,999]` cases cannot expose priority defect. Add `[existing,999,0]` and reorderings; require ErrInvalidNote and unchanged existing records. |
| 0522 | Positive intended fix: reflection validates pointer/non-nil before absent return without unmarshalling dummy data. Copied bytes, JSON encode-before-lock commit and copied Keys retain storage isolation. | HOLD: only nil-interface destination is tested absent; original mutant already rejects that. Add absent scalar and typed-nil pointer requiring an error without an extra boolean constraint. Remove unsupported present-invalid-destination found=true and empty Keys nonnil oracles. Concurrency assessment below. |
| 0567 | Positive: declared final variadic slice goes through CallSlice, ordinary methods through Call; UnsafePointer added to nil-capable kinds. Exported bound signatures, exact assignability, result ordering and panic/mutation semantics substantive. | HOLD: test fixtures define no variadic method or unsafe.Pointer parameter. Add final-slice variadic success including nil slice, expanded-argument rejection, and nil unsafe.Pointer acceptance without dereference. Supplied mutant retains both omissions although label names only variadic defect; report both, not a claimed single isolated mutation. |
| 0692 | Positive: full-slice expression caps shared allocation capacity at its endpoint; remaining-capacity subtraction, zero-size, independent fallbacks and reset/reuse retained. Allocation lifecycle and ownership substantive. | HOLD: tests mutate within lengths only. Their `append(append([]byte{}, a...), b...)` copies into a new slice, not appending through arena allocation `a`. Add Take(1), append nonzero through returned slice, then Take(1), require new byte zero; also verify earlier append cannot corrupt a later live region. No huge capacity or post-reset independence demand. |
| 0720 | Positive intended fix: restart input-order search after each resolution; validate whole graph before callbacks and preserve failures/skips. Graph validation/readiness/callback outcomes substantive. | HOLD: existing successful fixture produces independent,first,second,third under both algorithms; there is no later ready competitor when an earlier step becomes newly ready. Add `[a requires b,b,c]`, require callback order b,a,c. Remove unsupported exact relative placement of skipped versus executable outcomes; preserve statuses, error text and ready callback order. |
| 0774 | Positive: cap count by remaining articles before adding to start, so large valid logical limit cannot overflow. Deterministic sort/cursor/budget/trace/copy interactions substantive. | HOLD: no MaxInt page limit; tests also reject nil empty Items although prompt and plan permit them. Add one/two-article MaxInt-limit cursor cases with tiny physical input and exact trace; assert empty length, not nonnil representation. |

## Oracle and concurrency details

### 0522 registry

The invalid-destination loop includes `nil`, scalar `1`, nil map, and typed nil pointer against an existing key and insists on `found == true`. The specification requires an error for invalid destinations but does not freeze the accompanying boolean. The approved plan explicitly forbids imposing that boolean. Reference validates first and returns false/error; even the supplied mutant returns false/error for nil interface, so that assertion cannot be credited as a meaningful mutant distinction. A valid nonnil pointer to an incompatible destination type against existing stored JSON is the appropriate `(true,error)` decoding-failure test. `Keys` promises sorted contents, not a nonnil empty slice; remove that representation constraint.

The concurrency test launches 40 goroutines with unique keys, each doing Put/Get/Has/Keys. Shared registry access overlaps and test errors use goroutine-safe `t.Errorf`; WaitGroup synchronization makes final length/order check deterministic. It does not assert decoded `value == i`, ignores Has results, never invokes Delete concurrently, and does not exercise competing replacement/deletion on shared keys. It is useful smoke, not full all-method concurrency qualification. Add bounded mixed Delete/Put/Get/Has/Keys with specification-safe assertions (avoid assuming an exact interleaving), local destinations, and final deterministic reconciliation. Actual network-disabled sandbox `-race` is still required; this report claims none.

### 0439 reconciler

50 goroutines insert distinct names then Snapshot. This is a valid Apply/Snapshot overlap smoke and final count is deterministic; `t.Errorf` is used safely. Snapshots' contents/order are ignored during overlap, and concurrent replacement/deletion is absent. Add bounded insert/replace/delete plus snapshot readers, check each snapshot's ordering/unique structural keys without assuming concurrent population size, and a final deterministic state. The reference consistently guards records with RWMutex; immutable watch/leader configuration is safe. Actual `-race` qualification remains outstanding here, regardless of ordinary test results.

### 0720 ordering

`TestRunPlanWaitsForAllDependenciesBeforeSkipping` uses bad,good,join input order, so its result follows that order whether skipping is immediate or delayed; its name establishes no additional guarantee. The failure/transitive test freezes root,direct,transitive,free outcomes even though approved scope does not settle relative ordering of skipped versus executable outcomes. Compare outcomes by name/status/error for that aspect and independently assert ready executable ordering. Do not expand the reference contract just to justify a convenient test oracle.

Other test assertions sometimes inspect zero/nil secondary return values where only an error is explicitly promised (for example 0330 malformed-result Workload and 0514 invalid returned Note). References happen to satisfy these, but independent-test revision should avoid using such unspecified representation details as mutant evidence. No current hold requires broad API redesign.

## Seven criteria, explicitly

1. **Clarity:** intended defect witnesses derive from actual declared domains, including nonempty Go strings with NUL, all positive logical int limits with tiny physical workloads, declared variadic slice types, and nil-capable pointer kinds. Do not add global resource guarantees, forbid valid identifiers, or infer extra error/empty-slice representations. The 0720 skip interleaving is deliberately not expanded.
2. **API consistency:** all nine intended reference corrections are scoped positive as detailed above; no observed new substantive reference defect is asserted. Public API declarations and generation task identity remain intact. No current/private-field manipulation is needed for a witness.
3. **Independent-test provenance and validity:** authoring inputs/results are separately bound below. Independence is preserved but does not establish adequacy. Missing precise witnesses and the specified invalid oracles prevent quality closure.
4. **Nontriviality:** entire targets retain the multi-branch, state, ownership, callback or graph interactions listed per row. The small size of a correction is not a reason to reject these parents as elementary.
5. **Idiomatic implementation:** standard errors, explicit structural map keys, mutex-protected state, full slices, reflection assignability/CallSlice, bounded arithmetic and fresh copies fit these tasks. No extra dependency or padding is needed. Tautological `errors.Is(err,err)` in 0330 is redundant, not a meaningful error assertion.
6. **Isolation:** package solution, Go 1.22 module, standard-library tests and references only; no network, filesystem service, external package or environment-dependent data required. All future candidate execution belongs in the resource-limited network-disabled sandbox.
7. **Realistic known-bad failure:** supplied defects are plausible semantic failures, but all nine presently lack a valid discriminating test. Unsupported-oracle failure is not qualification. Only fresh independent bounded test correction plus actual sandbox verification can close that gap.

## Exact artifact/evidence bindings

Directory: `datasets/cache/expansion-v1/versioned-recovery/r4/`. File names below use `exp-v1-recovery-r4-go-generation-NNNN.candidate.json`. SHA-256 canonical form is sorted compact UTF-8 JSON with ensure_ascii=False and allow_nan=False; file form hashes exact bytes.

| Suffix | Candidate canonical SHA-256 | Candidate file SHA-256 |
| --- | --- | --- |
| 0330 | cb2f0c59d9aa8a6f0d89cc421446c62e131158a105c2a47f8d9353cbf6fb8f60 | 7b849f1ba0fe64c41be2fe3618db9b0243239fbf68f4d740bd1ff3b6b09813b4 |
| 0439 | 2545b02494023dd2f2c58404a33d972b9a3664ee61564612ff872104f5b01612 | f1a51ef8e196e3cb7d0e490b652ba5ace602dbb2a25a5e432af1d8d330d0b058 |
| 0499 | 2f2c70521ba6817a224c6f1e8d73505e43384480b2fa3ed5ae5bc44eb7d5d2e7 | 28615cbc18bd0b5e7dea78bb860eef4a450edb623ec24fedb482f0358392cdb7 |
| 0514 | d52beea470abba8412da83129aaa00f7254222d26f2936292e00ae2f7db9aa6e | 1b3795c425cc300719bf71f3fc16c7438db587d50f8a60e9142ab3e548e05311 |
| 0522 | 737d4aea9fa7785d0e14cc7943b93c38af5b209745b7eb71ca11f74257a6f392 | 40ae4d3eaa491d03ff9cb5cd3aad2c1110d5c483edfaf66c99926cb3193ba005 |
| 0567 | 83f039a62a08d7b6cc37de50c22140f2798209249fa9724e16e4df3447aae1af | 2a32238dfef3a093bb54c909b870028fd9881fe6cda263cc8dc21b973162f9be |
| 0692 | d2414cb601ff5d3bd04ded6df7dabb3c05dc398e3f451e763e1ceaffcddce425 | 461fd0050d125da8125c9554ae61fed492fdf8ec894b96f9397ebf5984dea22b |
| 0720 | e990f25b24b3d27b87904bff846960e588ae26522be3ab4717b2e45ce91d5b42 | 1a49d15b75b282da6c53a5433b4ccc8885458ac652670af09b0ad122172d119b |
| 0774 | 8c6c7c211b5d1948013d75ad11b5ffc3c0460ce3b00cf93b5103592b9bef1ab0 | 6003473bfdd12f1aa43c49bf43ebc4557b08e08a19dae165ef4a1ce4fe7dc45d |

Parent canonical hashes (same suffix, `exp-v1-go-generation-` prefix):

- 0330: `e5db26603288b8f8b3233f61100859d76916748a2a3b42df7b35918c69239e06`
- 0439: `c98f733a049b368652aff85a793bed83bf2796a5f98f4dd6fccabf333fb23ab6`
- 0499: `9b190e492fd3f7c21c17423635bda2b301fe9e435f0d9ef658187c2d06a407c2`
- 0514: `9e389d7133dd006fb3ed971fb237c5ff0e31b5db870aa9732b3bbbe7a09d50b0`
- 0522: `ce7690df2df169a97c0b73bce989ce42a742bb3ed8912b8bb6bc63f1fae90645`
- 0567: `4853e6847f4cd0226bb6f87ae406b5f5460ec83791ce0426d046ac63ece981d4`
- 0692: `a14c1b71685a247a7d47525cafdf1157bdd21c252bea64424d752d4087931944`
- 0720: `45d36ad4cc375b01c404dabea0c4555c4ae9b39d1665bc54eea32a1341bd499e`
- 0774: `58aa8b8386f2d7ba10e86d4d479df6518ca44d733b957b5dcb44d54adee26813`

Evidence exact file hashes:

- `plan.json`: `8a6137773e65e1a55e5eaceed9a8c2e40153b5759a46a5189ba6a488d530d58c`
- `lane-results.json`: `21d5a21f818f02c813c51d625a0692e050c68e5a01a69523d70815b2d42b8a92`
- `go-recovery-architect-evidence.json`: `a48d375fb6f1271008701844e557550689ca7defb53424f4caa89c42c06d2efc`
- `go-recovery-independent-tests-evidence.json`: `d1fb6c501e9c3439a70fa17789574ce475e5ddb2d86e4f7ff47d05d7469169c4`

For every nine-row ID, exact equality checked: derived prompt = architect returned problem = independent request specification = architect request original problem; derived reference/mutant = architect returned code; derived test = independent returned test code. Thus all nine reference-fix prompts are unchanged and test origin is not reconstructed from candidate code. Both Go authoring evidence records have matching request prompt hashes, returncode zero, no timeout, no parse error, and empty disallowed-tool lists. These are authoring provenance facts, not executed candidate metrics.

Approved selection/source binding is preserved through the plan's parent source, rights and review evidence records, originating from `RECOVERY_TRANCHE_GO_JAVA_20_20260908.md`. The frozen parent corpus SHA-256 is `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`; held-parent ledger binding is `9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee`. This report does not reopen authorized source rights or assert release-license packaging completion.
