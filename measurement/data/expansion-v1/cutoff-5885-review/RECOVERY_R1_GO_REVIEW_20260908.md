# Recovery r1 Go independent quality review — 2026-09-08

## Decision

Two complete derived Go candidates reviewed; both remain **not ready for admission**. Their reference corrections are statically complete for the original held defect, but neither independent test suite distinguishes its supplied known-bad/original reference from the corrected reference. This is a concrete recovery-verification gap, not an allegation of test-author contamination or a new defect in the fix.

Go0761 additionally still requires race-enabled concurrency qualification, including overlapping Enqueue, Drain and Count. No candidate, test, known-bad or race run was executed in this review. Main owns sandbox verification and integration.

Scope: ONLY r1 Go0740 and Go0761, their immutable original records, request/plan bindings, relevant generation evidence and frozen `SEVEN_CRITERIA_GO.md`. Full derived prompts/references/all tests/known-bad programs and both parent prompts/references/tests were read. No candidate, plan, ledger or other central file changed; only this report is written.

## Content bindings

Candidate paths share prefix `datasets/cache/expansion-v1/versioned-recovery/r1/`; suffix is the full derived ID plus `.candidate.json`. Canonical SHA uses the admission planner's sorted compact UTF-8 JSON representation, not the pretty-printed file bytes.

### exp-v1-recovery-r1-go-generation-0740

- Parent: `exp-v1-go-generation-0740`
- Parent canonical SHA256: `5f9493bb7fd2618a8143a76f133d05671201dc83e37a572f0e637882661dd417`
- Derived file SHA256: `a55a3b02a6d3f2de97704d7961f434656de1c9ddcb835a7052c11956a99da8e8`
- Derived canonical SHA256: `9cb089922fd394b23d7d60a7b4f059c1c5aa7d3d0c3c3ebee433d42b5fd62a08`
- Prompt/rendered-prompt SHA256: `220b8c28ab30a397905298e1c72e521ed31f99a62a765c8e7b19c041276bb5a0`
- Reference SHA256: `42152f66d50893545898b815b5bb05564a8645a2525b033fa132fe2774c6766f`
- Independent solution_test.go SHA256: `a56ed46553b1edf4e82f6d6e1435535b4ebb5d0b310192a1d0a50f7cb800f6a6`
- Known-bad SHA256: `4f77d159544fedfd02a49f7cda6e7ccd7f2632accf37c43e0df1f242436c785b`

### exp-v1-recovery-r1-go-generation-0761

- Parent: `exp-v1-go-generation-0761`
- Parent canonical SHA256: `b0a6022abea6f524ed7f48a4f8a39b676bb6946e34a95f54a07e9b4603218360`
- Derived file SHA256: `f3e1ed91cd8418fe8a4fa8bcde1e9db1eaf6d2fdff2ffc28d6e8952b55eb2827`
- Derived canonical SHA256: `552ffcaa815f0d9e1750a396ae7aeaba726a16d5bbf3744fc8fe6c5b340bdb1a`
- Prompt/rendered-prompt SHA256: `a7309c9d0b71be26d31364013e48a6e7b396dd1b652f86f89e871b1f7d2e4676`
- Reference SHA256: `ea2c90390516f68803ca88ba21850a4390a569da08ca9a379613c8f14bf3ae09`
- Independent solution_test.go SHA256: `d852a75d96a46ffd7dc6b4ee7987fa0db744047de73bcd39a0fbdee128ecd074`
- Known-bad SHA256: `a58a70a904ae140f4219b18d66f2cd7c925248042abee7fd64990db78b19d6db`


Read-only integrity checks confirmed: parent canonical hashes match both request selections and plan records; derived prompt bytes equal their original parent prompts; known-bad code bytes equal the respective original parent reference; messages[1] equals verification reference; derived task IDs agree; every support/test, prompt/rendered prompt and reference/known-bad declared content hash matches actual content. The parent source/rights and historical hold are retained in the plan. Both changes are classified reference-fix in the approved request. Frozen parent corpus SHA256 is `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| Binding file | File SHA256 |
| --- | --- |
| measurement/data/expansion-v1/cutoff-5885-review/recovery-requests-r1.json | `c7fed0810f7fa42b2b0e5c56ccf9e0afe2c0b239db8aa529c5c0744f58e6b37d` |
| datasets/cache/expansion-v1/versioned-recovery/r1/plan.json | `a955b22d518994f9b2470cd6aaf89134a709bd7ba33dbe7d06797dc5b06ef9f1` |
| datasets/cache/expansion-v1/versioned-recovery/r1/run-contract.json | `359ed51b2db8f6e4e169b352435a822670d35376fb5d1d705999a2ba310839ce` |
| datasets/cache/expansion-v1/versioned-recovery/r1/go-recovery-architect-evidence.json | `7145d55e2e8f5b48a9298b10722f88cdad49aa37d0d12cf1ce9d33f6a2887729` |
| datasets/cache/expansion-v1/versioned-recovery/r1/go-recovery-independent-tests-evidence.json | `2e9ba2e46f3a858d630703c77a2b553bd13ee36e12cd7cbbac153024cb88ed85` |

The run contract records cumulative original-quality closure as generation permission, not admission. Immutable plan records still say planned-not-generated-not-admitted; they are planning lineage, not the authoritative execution/admission result.

## Go0740: capacity arithmetic

Reference diff is exactly the capacity guard: `b.used+seats > b.capacity` becomes `seats > b.capacity-b.used`. Valid constructor capacity is positive, accepted seats are positive, and every successful addition preserves used <= capacity. Cancellation subtracts a previously active positive reservation. Thus capacity-used is representable and the checked addition cannot overflow under the reachable accounting invariant. Input validation remains before mutation; failed capacity requests consume neither IDs nor seats. Ordered List, value-copy observations, sentinel errors and cancellation semantics remain intact.

This is a substantive reservation lifecycle, not padding around a trivial patch. No concurrency guarantee is present for Book and none is added. Unbounded private ID-counter exhaustion is not newly asserted as an executed or required fresh failure under the frozen calibration; the targeted reachable capacity bug is fixed.

**Tests do not reject the original defect.** All created valid capacities are small (1, 3, 4, 5, 10); requested valid seats are likewise small. The only difference between the supplied known-bad and reference cannot manifest in any listed test. The ordinary capacity-boundary test distinguishes overbooking without overflow, not overflow. Static expectation: both programs pass or fail together on these assertions; this is not a newly executed acceptance claim.

Required distinguishing regression in a new immutable test/candidate revision: use `maxInt := int(^uint(0) >> 1)`, construct that capacity, Add a valid guest with maxInt seats, then Add another valid guest with one seat. Require ErrCapacityExceeded, unchanged Get/List, and unchanged next successful ID after cancellation and re-add. A second near-boundary case maxInt-1 then one establishes that the correction does not reject valid exact fits. This uses only a few reservations and no large memory allocation. Require the original known-bad to fail the new regression in the sandbox and the reference to pass.

Other nonblocking coverage observations: derived tests no longer explicitly mutate a returned List element and check storage independence, although static value-copy code preserves it. Adding that regression is useful but not a separate demonstrated reference failure.

## Go0761: lazy storage and concurrency

Reference diff replaces the constructor's capacity-sized packet allocation with `&Mailbox{config: config}`. Logical capacity and positive validation are unchanged. Actual storage grows only when actual packets are enqueued; all operations correctly handle nil initial packets. No arbitrary capacity cap is added. This removes the avoidable upfront allocation at valid MaxInt configuration without promising unlimited resources for physically huge packet populations.

Static concurrency/ownership check: packets reads and mutations in Enqueue, positive-limit Drain and Count share one mutex. Config is copied at construction and never mutated; reading MaxPayloadBytes before locking is not a race on this implementation. Invalid/zero-limit Drain paths access no packet state. Each accepted payload and each returned payload is copied; non-nil zero-length payloads are constructed with make. Stable iteration retains matching and nonmatching order. No caller concurrently mutating its own input buffer is promised safe.

**Tests do not reject the original defect.** Valid configured capacities range only up to 40. The known-bad differs solely by eagerly reserving that small capacity; the tests inspect no allocation behavior and never supply a valid huge logical capacity. The exact supplied known-bad retains the same mutex and payload-copy logic, so the existing concurrency test cannot distinguish it either.

Required distinguishing regression in a new immutable version: construct capacity maxInt, MaxPayloadBytes one, assert successful non-nil construction and zero Count, enqueue a few one-byte/nil packets, check counts and selective drain ordering/non-nil empty semantics. The original allocation should be rejected by the sandbox run (panic/nonzero), while the lazy reference should succeed with bounded memory. Preserve that actual result rather than treating this static prediction as evidence.

**Race qualification remains required.** `TestMailboxSupportsConcurrentCalls` has 40 concurrent enqueues, a Wait barrier, then 40 concurrent drains, another Wait, with Count calls only after barriers. This usefully exercises same-method contention but does not overlap Count with writers or Enqueue with Drain. Running it without -race cannot certify race behavior. The candidate task names runtime go-1.22.12 but contains no race execution result or race qualification.

Main should run the existing suite with the pinned race-enabled toolchain and add a bounded overlapping workload: finite uniquely identified successful enqueues, concurrent bounded drains, concurrent Count reads, final joined drain, and exact conservation/no-duplicate checks against recorded successful enqueues. During overlap, assert only valid per-call bounds, not equality of counts sampled at different times. Do not demand a deterministic cross-goroutine enqueue ordering. Synchronize the test's own accounting, avoid sleeps as correctness conditions, and impose external sandbox time/resource limits. Record actual -race command/runtime compatibility and race output; do not silently fall back to an ordinary run if race instrumentation is unavailable.

## Seven-criterion dispositions

| Criterion | Go0740 | Go0761 |
| --- | --- | --- |
| Prompt clarity | Scoped positive: unchanged concrete API, validation, capacity/lifecycle and ordering rules; no new unstated numeric cap. | Scoped positive: unchanged capacity, precedence, ordering, ownership and concurrency contract. |
| API consistency | Scoped positive: one arithmetic guard correction preserves exported shape and sentinel behavior. | Scoped positive: constructor allocation strategy changes only; exported shape/behavior retained. |
| Independent test origin | Supported by fresh specification-only author prompt and archived isolated/no-tool event audit; test weakness is not evidence of contamination. | Same origin chain, separate from architect output; not behavioral certification. |
| Non-triviality | Positive under frozen lifecycle/accounting/atomicity calibration. | Positive under frozen synchronization/ordered drain/ownership calibration. |
| Idiomatic code | Positive statically: ordinary map/value storage, sorted snapshots, sentinel errors, safe remaining-capacity comparison. | Positive statically: immutable config, mutex-protected packet state, explicit payload copies and lazy allocation. |
| Dependency isolation | Standard-library-only candidate/tests and local go.mod; actual network-disabled execution pending main. | Standard-library-only candidate/tests and local go.mod; race-toolchain execution pending main. |
| Realistic known-bad failure | NOT CLOSED: realistic exact original overflow defect supplied, but tests omit every overflow witness. | NOT CLOSED: realistic exact original eager-allocation defect supplied, but tests omit large logical-capacity witness; race qualification also outstanding. |

Independent-author evidence prompt contains only the two IDs/specifications plus generic test-author instructions, not references, known-bad programs, source tests or architect context. Its audit records returncode 0, no timeout, no disallowed tool items and no event parse error. Prompt SHA is `20674b8007bc110c8c853014b897d5a339396f1610fd8d06270a61c760849672`; final output SHA is `3e69929c35a2a2c7c229924fd9075a298a76c17c825ef42dfb6f2d1604fdfc29`. These establish the inspected lineage facts, not test sufficiency or executed correctness.

## Handoff

Retain both r1 artifacts and all initial test-author evidence unchanged. Record failed/insufficient mutant qualification honestly, then strengthen independent specification-derived boundary coverage in a separately versioned, hash-bound artifact; no same-path overwrite or silent replacement of tests. Re-evaluate the updated tests against both reference and original known-bad, preserve any original failure/acceptance results, and complete Go0761 race qualification. This report does not add central holds or approve either candidate for admission.

