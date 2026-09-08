# Recovery r2 Go test review — 2026-09-08

## Scoped decision

Both r2 test corrections are **statically acceptable for the targeted original defects**. Go0740 now tests representable maximum-capacity overflow rejection; Go0761 now tests maximum logical capacity with bounded actual storage. The mailbox mixed-operation test has a valid synchronized count-conservation oracle with no cross-call snapshot or scheduling overconstraint. Actual reference/known-bad sandbox results and Go0761 **-race qualification remain outstanding to this static review**.

This completes the requested one-correction review. No further automated critic loop is recommended or invoked. No execution, teacher/cloud calls, candidate edits, central edits or admission claim. Only this report is written.

## Scope and integrity

Full changed test files and correction-author evidence were inspected against the previously full-reviewed r1 specifications/references/known-bad programs and `RECOVERY_R1_GO_REVIEW_20260908.md`. Read-only byte comparisons confirmed both r2 messages arrays (prompt and reference) and complete verification validation objects (reference and known-bad) equal r1. Test/support content hashes were recomputed successfully. Thus prior static correction-completeness, API, non-triviality, idiom and dependency findings carry unchanged; these findings concern new test qualification, not another blanket review.

Candidate paths share `datasets/cache/expansion-v1/versioned-recovery/r2/`; filenames are the complete derived ID plus `.candidate.json`. Canonical hashes use the admission planner's sorted compact UTF-8 JSON encoding.

### exp-v1-recovery-r2-go-generation-0740

- Candidate file SHA256: `3e30522a3d99583f7e2085bc174256e77b12072be9219d669ddfa3b44e5c43a2`
- Candidate canonical SHA256: `e13edcc1dface332a0a3a6f8a3b08c23b147c492f73109122807ba1f99076b4b`
- Immutable r1 file SHA256: `a55a3b02a6d3f2de97704d7961f434656de1c9ddcb835a7052c11956a99da8e8`
- Unchanged prompt SHA256: `220b8c28ab30a397905298e1c72e521ed31f99a62a765c8e7b19c041276bb5a0`
- Unchanged reference SHA256: `42152f66d50893545898b815b5bb05564a8645a2525b033fa132fe2774c6766f`
- Unchanged original-defect known-bad SHA256: `4f77d159544fedfd02a49f7cda6e7ccd7f2632accf37c43e0df1f242436c785b`
- Corrected solution_test.go SHA256: `a1d71cdf533a5736202a6d2f83ea18fb436ec701292e7a9e216816293ce5260c`

### exp-v1-recovery-r2-go-generation-0761

- Candidate file SHA256: `a047b209c95b374ffbee8fc53ac5b7d4588c29918fcb509bf39dcfd10f98482d`
- Candidate canonical SHA256: `12d8492bfa5f5b5e678cbf63a51e92a511abdf2f181abf87acb68a742d36f183`
- Immutable r1 file SHA256: `f3e1ed91cd8418fe8a4fa8bcde1e9db1eaf6d2fdff2ffc28d6e8952b55eb2827`
- Unchanged prompt SHA256: `a7309c9d0b71be26d31364013e48a6e7b396dd1b652f86f89e871b1f7d2e4676`
- Unchanged reference SHA256: `ea2c90390516f68803ca88ba21850a4390a569da08ca9a379613c8f14bf3ae09`
- Unchanged original-defect known-bad SHA256: `a58a70a904ae140f4219b18d66f2cd7c925248042abee7fd64990db78b19d6db`
- Corrected solution_test.go SHA256: `79399e50842890f015098ed531247c8f00d8510e3d8916e4be7e1587776e9ce5`


| Binding/evidence file | File SHA256 |
| --- | --- |
| datasets/cache/expansion-v1/versioned-recovery/r2/plan.json | `5dae7eac34ac462f6173dc6b740364d5c4b68129950359f453f4038111ad1d29` |
| datasets/cache/expansion-v1/versioned-recovery/r2/go-recovery-test-correction-evidence.json | `aae6fbfb05729e04002173f8b36370469130b4b35441f1d858adc7297431853f` |

## Go0740 — valid maximum-boundary regression

`TestMaximumIntCapacityAndOverflowBoundary` computes maxInt as int(^uint(0)>>1), valid on the supported int width without an out-of-range literal. It creates one book, adds maxInt-1 seats, adds one exact-fitting seat, and requires the next one-seat addition to return ErrCapacityExceeded. No huge collection is allocated: capacity is an integer bound and only two active reservations are needed.

The unchanged reference's remaining-capacity guard rejects that last addition. The unchanged original control's used+seats expression wraps after used reaches maxInt and accepts it, so this test statically distinguishes the actual hold. It then checks the unchanged active reservations and verifies that canceling the large reservation permits a replacement with ID3, rather than consuming an ID on the rejected addition. All expectations follow from the existing capacity, monotonic-ID and failure-atomicity contract.

The added U+2003-only guest rejection is within whitespace-only validation; no ASCII-only whitespace promise exists. The new List mutation test checks independent value observations, consistent with the in-memory book and prior parent test contract. Existing ordinary limits, invalid inputs, ID order and cancellation tests remain. No test-only internal field access, private counter injection, arbitrary capacity limit or unpromised failed-result payload assertion was added.

Disposition: prior missing overflow witness is closed statically; actual reference pass plus behavioral known-bad rejection must still be recorded.

## Go0761 — valid logical-capacity regression

`TestMaximumIntLogicalCapacity` uses the same architecture-sized maxInt with MaxPayloadBytes one and only two actual packets. It checks enqueue/count, selective drain, missing-topic non-nil empties, nil-payload normalization and final empty state. The reference lazily stores these bounded packets; the original control tries to allocate a capacity-sized Packet slice at construction. This is exactly the original avoidable eager-allocation defect, not a demand to physically store maxInt packets or guarantee arbitrary memory resources.

The test does not inspect allocation internals, impose a specific slice capacity, or force an implementation strategy beyond successful supported behavior. The original control is statically expected to panic/fail construction under the pinned sandbox, while the corrected reference should use bounded memory. Preserve actual runtime evidence; this review did not execute either.

The payload test now enqueues the same caller slice twice before caller mutation, then mutates one drained result and checks the other. This strengthens cross-packet ownership coverage without imposing unpromised deep structure.

## Mixed Enqueue/Drain/Count test

`TestMailboxConcurrentOperationsConservePackets` starts four enqueue workers ×50, four drain workers ×60 and two count workers ×100 using one start channel. All loops are finite; the test has no sleeps or retry-until-success loop. Logical capacity maxInt ensures 200 valid attempted one-byte packets cannot make the mailbox legitimately full.

The test's own successful/drained counters use atomics; invalid-count flag is atomic; errors flow through a channel sized for all possible enqueue/drain errors (200+240). It waits for all workers before closing that channel, avoiding send-on-closed-channel and error-channel backpressure deadlock. Worker failures are reported after joining; no worker calls Fatal/FailNow.

A packet may be drained before its enqueue worker increments successful; the test correctly avoids comparing those counters during execution. After joining, each successful operation has completed its accounting. Then:
- drained <= successful;
- remaining Count equals successful minus drained;
- final bounded drain length equals remaining;
- successful equals concurrent-drain count plus final-drain count;
- final Count is zero.

Those are valid serializable count-conservation properties. During mutation it checks only that a single total Count is between0 and200; it does not compare separately sampled total/topic counts or demand a particular cross-goroutine order. Draining before any enqueue is valid and produces an empty slice. The common start permits overlapping method execution but does not guarantee any particular interleaving, which is appropriate.

### Limits of what this test proves

It checks **cardinality conservation**, not unique packet-identity conservation: every worker repeats one byte payload, and concurrently drained payloads are only counted. A hypothetical equal-count drop-plus-duplicate or payload corruption could escape this concurrency test. It also does not inspect each concurrently drained result's topic/limit/content; sequential tests cover those behaviors, and the unchanged reference uses one mutex around the full operation. Record this limit honestly; it is not a demonstrated defect in the reference and does not require another critic loop for the targeted eager-allocation correction.

The old phased multi-topic concurrent test is replaced, rather than retained. This is a change in concurrency test shape, not proof that all concurrent schedules or topic combinations are covered.

## Actual -race qualification

Still required before calling Go0761 race-qualified: run the corrected suite including the mixed-operation test under the pinned, race-capable Go toolchain in the resource-limited network-disabled sandbox and preserve exact command, runtime/image identity, hashes, stdout/stderr, exit status and limits. A normal go test pass, atomic counters in the test, or static observation of a mutex does not equal an executed -race pass. If instrumentation cannot run with the pinned environment, report that concrete tooling condition; do not silently downgrade to ordinary execution or label it qualified.

A bounded -race pass is useful evidence, not exhaustive schedule/linearizability proof. Main may report separately the scope of executed coverage and the static mutex argument.

## Correction-origin audit and handoff

The correction prompt supplied only the two unchanged specifications, their proposed r1 tests and specification-derived review requirements. It did not provide reference or known-bad code. Its excerpted review requests maxInt/atomic rejection and bounded mixed-method count conservation, not implementation-specific private state. Archived audit records returncode0, no timeout, no disallowed tool items and no event parse error. Prompt SHA256: `9982e4c4ebd5e7336878e47ac2711f3d2bf47ef0b2fb53bbc0c3b1f5212a0082`; final-output SHA256: `1901338ad82f6276955ca62fcdefdf3b371f2bc49b62c17413de22219bbc4f02`.

The r1 failed/insufficient tests and raw evidence remain historical, not overwritten by this review. Proceed with main's bounded sandbox diagnostics and race qualification; no automatic further correction loop. Other release/admission/overlap gates remain independent.

