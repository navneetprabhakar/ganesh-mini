# Provisional recovery tranche recommendations — 2026-09-08

## Status and scope

PROVISIONAL ONLY: 12 held generation parents, exactly two each in Go, Java, JavaScript, TypeScript, Python and Rust. These are recommendations, not approved selections, recovered candidates, admission, or training evidence. Main must first save the cumulative quality closure and explicitly integrate the selection. Gate 2 expansion admission remains the relevant gate.

Fresh full prompt, reference and every original test were read for all 12 recommended parents, together with their exact hold entries and the cited per-ID review findings. One additional inspected parent, Rust generation0697, was not selected: its narrow three-field parser/oracle repair offers weaker nontriviality value than the charged-action state machine. No code execution, teacher request, cloud use, central mutation, new unique-row credit, or candidate generation occurred. Only this note is written.

The original frozen corpus is `datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl`, SHA256 `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`. The read snapshot of `additional-holds.json` contains 2809 additive holds (2812 including the three base holds), SHA256 `9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee`. All 12 exist in that snapshot with focused behavioral/contract holds; none of their recorded holds is elementary/padding, licensing, or evaluation-overlap. This selection screen does not replace renewed evaluation-separation and rights-lineage validation for derived artifacts.

Recommended execution order after approval: Python0220/0517, Go0740/0761, JavaScript0014/0270, TypeScript0064/0087, Rust0359, Java0781/0788, then Rust0396. The last case requires an explicit semantic decision, not merely a reference patch.

## Exact immutable parent bindings

Hashes below are the planner's canonical candidate SHA256: UTF-8 JSON, sorted keys, compact separators, ensure_ascii=false, allow_nan=false, no trailing newline. They are not raw JSONL-line hashes. Source line is one-based.

| Parent ID | Source line | parent_candidate_sha256 |
| --- | --- | --- |
| exp-v1-javascript-generation-0014 | 136 | `e545f4c21fb6f2b5cbbd468b700b96f652be2cc4c7cb3a1a7b0e36678e3931e8` |
| exp-v1-typescript-generation-0064 | 456 | `b282271869c48b1390be6822cad7841c19d1ae211a3f378ea186e65c197d9f39` |
| exp-v1-typescript-generation-0087 | 635 | `ddaa661359f01faf3d8e72ad106469dbdeddc378af9923560d2cbe1a39bc4f27` |
| exp-v1-python-generation-0220 | 1379 | `bca2cf2f83b29f86f9b5cd86f07a8256cccca0fabb12438d232066376f9212ce` |
| exp-v1-javascript-generation-0270 | 1635 | `a7b809fba05e9a23cf9977b895faa05a982b73cf871ff9bcc8e70f99b42820cd` |
| exp-v1-python-generation-0517 | 3171 | `05afcd1e6831356400649b9e287629fdc3016e152134d58ab70a83652eb58c93` |
| exp-v1-rust-generation-0359 | 4291 | `cbd06d15f78b5b9e6a8b072ea30dcf7072ab0160259bda440c9b58bd704a93be` |
| exp-v1-rust-generation-0396 | 4431 | `e41829396ee52614f965b12d66de50255affc3c8b06af066d79d5d8f6e89404e` |
| exp-v1-java-generation-0788 | 4730 | `4959a3daecf43d2ed70ec7221329d70c3ab760974b210815ab4d3c2d74ffa30e` |
| exp-v1-java-generation-0781 | 4733 | `2fe9d28d7cc74ea034ab338a3c535100a5fe47cfd627268ca4544a8ad528ad27` |
| exp-v1-go-generation-0740 | 5708 | `5f9493bb7fd2618a8143a76f133d05671201dc83e37a572f0e637882661dd417` |
| exp-v1-go-generation-0761 | 5737 | `b0a6022abea6f524ed7f48a4f8a39b676bb6946e34a95f54a07e9b4603218360` |

All parents retain the complete existing source/rights object: McEval-Instruct revision `57bd46727e49ac3e2890218a146d35c2454a8496`, per-source record ID and source_record_sha256, CC-BY-SA-4.0 attribution/license URI, transformation history and original independent-teacher test lineage. Preserve those verbatim in the derived manifest; do not replace historical lineage with this review's authorship.

## Focused recommendations and independent-test requirements

### Go generation0740 — reference-fix

Substantive target: capacity-constrained reservation lifecycle, cancellation, monotonic IDs, ordered snapshots and error atomicity. Hold: unchecked `used+seats` wraps and admits more seats than capacity.

Minimal correction: under the existing invariant 0 <= used <= capacity, compare requested seats against `capacity-used` before addition; preserve positive-seat validation, unchanged state on failure, cancellation accounting and ID allocation. Do not narrow valid capacities or add arbitrary small limits.

Independent tests: compute architecture-sized MaxInt; capacity MaxInt, reserve MaxInt, then reserve one must fail without changing total/list/next successful ID. Also MaxInt-1 then one succeeds, another one fails, cancellation restores room, and invalid guest/seat failures remain atomic. Use an independently written bounded accounting model, not the same comparison copied as the sole oracle. Retain ordered/limited non-nil snapshots and ordinary lifecycle tests. No enormous collections or private ID injection are required.

### Go generation0761 — reference-fix

Substantive target: mutex-protected bounded mailbox with global order, topic-limited drain, validation precedence and byte ownership. Hold: constructor allocates full configured capacity before any packet exists, so valid MaxInt capacity panics.

Minimal correction: lazy/empty initial packet storage with growth only for actual enqueues; keep the configured capacity as a logical bound, not a preallocation command. Do not promise unlimited memory or swallow genuine resource exhaustion.

Independent tests: construct MaxInt capacity and payload limit one, enqueue/drain a few packets only; small-capacity fullness, invalid-before-full precedence, mixed-topic drain order and remaining global order, count by topic, detached payloads and non-nil empty results. A bounded race-enabled suite must cover concurrent enqueue/drain/count using the pinned sandbox; this note does not claim it ran.

### JavaScript generation0014 — reference-fix

Substantive target: immutable registry CRUD/search with exact no-op identity and changed-record-only rebuilding. Hold: direct-access validation accepts required string fields, then spread drops non-enumerable required fields.

Minimal correction: explicitly materialize key, code, owner and openedOn when copying a validated entry, including constructor/add and edited-entry rebuilds. Optional extras may retain the existing policy; do not invent a universal deep-copy requirement. Absent-key edits must remain exact no-ops, even when their irrelevant patch would be invalid for an existing key.

Independent tests: make each required field non-enumerable separately while keeping its valid value; constructor/add retain all four fields, hidden duplicate keys are still duplicates, edit preserves untouched required fields, attempted key edits are ignored, unchanged branches preserve identity and search returns the intended original matching record references. Include ordinary enumerable objects and direct-readable inherited required fields under an explicit field-access contract; no getter side effects are needed.

### JavaScript generation0270 — reference-fix

Substantive target: normalized immutable reducer, null-prototype dictionary ownership, ordered IDs, validation and selective structural sharing. Hold: copying byId with Object.assign loses an unaffected non-enumerable own entry in a valid externally supplied normalized state.

Minimal correction: copy every own dictionary key, including non-enumerable names, into a null-prototype result while retaining unaffected record identities; reconstruct affected required record fields explicitly. Preserve order identity on pin/unpin and copied inputs on replace. Do not silently restrict supported states to those produced by this particular implementation or to enumerable keys.

Independent tests: non-enumerable engine plus enumerable wing, pin wing, and assert engine survives by identity and order remains unchanged; then hide required fields of the affected part separately. Exercise "__proto__" as a data ID, non-null input values, null-prototype output, unknown-action/unknown-ID no-ops and invalid replace atomicity. Do not require arbitrary extra part fields to be deeply preserved.

### TypeScript generation0064 — reference-fix

Substantive target: foreign-key-valid reservation storage, generated/explicit ID collision handling, ordered detached queries and atomic updates. Hold: spreading the patch silently ignores a supplied non-enumerable seat.

Minimal correction: apply the three permitted patch fields explicitly, retaining the existing reservation ID. Preserve missing-field behavior and the current rejection of a supplied invalid value; freeze the supplied-versus-absent rule in the derived contract if implementation requires a choice. Presence-aware direct reads can support non-enumerable fields without spreading arbitrary extra properties.

Independent tests: typed hidden seat update, hidden invalid performance combined with another change leaves the entire reservation unchanged, empty valid patch returns fresh detached data, generated IDs skip explicit collisions, query ordering and copy isolation remain stable. Test absent and explicitly undefined optional fields against the finalized contract, not a test-writer guess. An extra id is not the original hold basis; any new requirement to ignore it must be explicitly documented as contract clarification rather than smuggled into tests.

### TypeScript generation0087 — reference-fix

Substantive target: account lifecycle, detached observations and independent/snapshot subscription registrations. Hold: valid typed hidden active=false is ignored because active is copied only by spread.

Minimal correction: explicitly select supported displayName/active values into the new Account; retain identity and notification semantics. Decide any explicit-undefined optional-field policy in the derived contract before test authoring; ordinary hidden false requires no such ambiguity to demonstrate the defect. Do not change independent duplicate-watch registration semantics.

Independent tests: hidden active=false actually deactivates, hidden displayName is normalized, empty patch still notifies, invalid update has no mutation, returned/listener objects cannot mutate stored state, duplicate callbacks unsubscribe independently and dispatch snapshots survive listener additions/removals. Keep arbitrary extra-field behavior outside the oracle unless the new contract explicitly resolves it.

### Python generation0220 — reference-fix

Substantive target: load/initialize/activate composition, first-failure propagation, identity-preserving Outcome and deduplicated success history with data ownership. Hold: directly deepcopy-ing a read-only Mapping wrapper rejects ordinary supported document contents.

Minimal correction: normalize the outer document mapping to a dict, then deepcopy its contents. Retain the specified document-dictionary domain and all existing result/history rules; do not add support promises for arbitrary noncopyable nested objects.

Independent tests: MappingProxyType containing ordinary nested dict/list documents and another simple Mapping implementation; mutate caller data and returned data separately to check independence. Verify missing/broken load stops initialization, failed initialization does not enter recent successes, repeated activation deduplicates, remember=false does not record, and Outcome behavior remains unchanged. Existing dict-only tests remain regression evidence, not wrapper-breadth evidence.

### Python generation0517 — reference-fix

Substantive target: tolerant HTML selection, first matching script semantics, relative URL resolution, filename-keyed cache precedence and immutable caller ownership. Hold: deepcopy(cache) preserves/rejects an unsuitable wrapper instead of returning a detached mutable cache.

Minimal correction: normalize cache mapping contents into a dict before independent copying. available remains a read-only lookup; no real network download is introduced.

Independent tests: MappingProxyType cache for no-match, hit and miss paths, read-only available mapping, first qualifying script wins, exact data-kind value and .mjs path rule, malformed HTML recovery, relative URLs/query/fragment basename behavior and filename collisions according to the contract. Missing content raises KeyError without input mutation; returned cache is a detached dict that receives downloaded content. Avoid inventing an unrestricted URL-parser acceptance guarantee.

### Rust generation0359 — oracle-rebuild (with reference-fix)

Substantive target: charged-action energy accounting, one-shot strike, independently advanced swing/recovery, zero-duration phases and interruption. Hold: u32 saturating multiplication is widened to u64 before division, changing the stated formula.

Minimal correction: evaluate bonus_damage.saturating_mul(charge_ms) in u32, divide by max_charge_ms, then saturating-add base_damage. Keep the original explicit operation order and type, rather than rewriting the prompt to legitimize widening.

Important original-oracle conflict discovered in the full read: the existing `damage_uses_saturating_multiplication_and_addition` test has max_charge_ms=MAX, charge_ms=MAX, bonus=MAX, base=MAX-2 and expects MAX. Under the stated u32 operation order its correct result is MAX-1: saturated product MAX divided by MAX is one. Therefore merely patching the reference cannot pass the old oracle. Archive the old assertion unchanged and replace it only in the derived test version with an independently justified expected value.

Independent tests: max_charge_ms=2, charge=2, bonus=MAX, base=0 gives 2147483647; also the corrected MAX-1 example, no-overflow ordinary proportions and saturating addition cases. Independently model the clamped integer formula and bounded state transitions; retain exact energy cost, insufficient-energy execution, excess-time discard, one strike, later zero-duration transitions and finished energy immutability. The original implementation must fail the new distinguishing tests; no padding is needed.

### Java generation0781 — reference-fix

Substantive target: exact monetary component rounding, original/discounted subtotal ordering, checked final totals and deterministic participant-share distribution. Hold: intermediate percentage multiplication/addition overflows even when the required result fits.

Minimal correction: exact safe quotient/remainder decomposition or BigInteger intermediates for half-up basis-point calculations, with checks on required representable outputs/final totals. If needed, clarify that overflow concerns required monetary results, not an avoidable implementation intermediate. Do not remove checks for genuinely unrepresentable totals.

Independent tests: Long.MAX_VALUE subtotal with 10000 discount basis points produces full discount and zero total, half-cent rounding boundaries for each component, zero/full rates, genuine final overflow, and deterministic share remainders. Use a separately written BigInteger rational oracle. Large participant counts must be tested with a bounded selection of indices/formula checks, not a massive array allocation.

### Java generation0788 — contract-clarification (with reference-fix)

Substantive target: hardened XML parsing, direct-child schema checks, ordered duplicate-preserving messages and immutable detached output. Hold: U+2003-only Category/Message passes trim().isEmpty despite mandatory nonblank validation.

Minimal correction: preserve existing String.trim output normalization but explicitly define blank as String.isBlank/Character.isWhitespace and reject such leaf values. Do not silently substitute a broader Unicode normalization policy.

The prompt's comment wording should also be made precise: comments are ignored and cannot satisfy required structural children; the existing valid-document test includes fake markup in a comment. Distinguish this clarification from allowing comments to substitute for elements. If the intended policy instead rejects every markup-bearing comment, that is a different derived contract/oracle choice and must be recorded.

Independent tests: U+2003-only category and individual message separately, nonblank Unicode text with preserved chosen normalization, nested substitutes, duplicate/missing direct children, number overflow/negative values, comment-only fake children and valid comments, immutable message list. Retain DOCTYPE/external-entity rejection and malformed XML tests under the network-disabled sandbox. No XML security certification is claimed here.

### Rust generation0396 — contract-clarification (with reference-fix; last priority)

Substantive target: owner authorization, per-user charges, pause state, atomic balance updates and single pending withdrawal commit/rollback. Hold: pending withdrawal restoration headroom can be consumed by later record calls, making promised failure rollback impossible.

Recommended explicit derived rule: balance plus pending withdrawal amount is reserved within u64; record rejects Overflow atomically if adding its charge would violate that combined invariant. This preserves unconditional restoration/clearing for a valid failed withdrawal. It changes which intervening record calls succeed, so it MUST be stated in the new prompt; it is not a silent reference-only fix. Do not change the getter's balance meaning or weaken rollback to "may fail" merely to match the old implementation.

Independent tests: record one, withdraw one, then attempt to record MAX: reject without state change; finish failure restores one and clears pending; subsequent withdrawal succeeds. Also exact remaining headroom succeeds, successful finish releases reservation headroom, failed finish restores it, mismatched/unauthorized finish is atomic, overrides and paused recording retain their rules. Use a small u128-backed model to check the u64 invariant across bounded sequences. No private ID exhaustion or huge histories are necessary. If this clarification is not accepted, defer this parent; do not substitute a different ledger task under the same parent.

## Evidence bindings

Paths are repository-relative. The precise per-ID findings above were reconciled with these notes; hashes bind the existing files, not an inferred current approval.

| Parent ID | Reviewed evidence path | Evidence SHA256 |
| --- | --- | --- |
| exp-v1-javascript-generation-0014 | measurement/data/expansion-v1/cutoff-5885-review/FINAL_DELTA_JAVASCRIPT_1_20260908.md | `6a608b2781ab0f84a8ade2e52dd81de4f6bfac8268583d3447be5c3965c0aaba` |
| exp-v1-typescript-generation-0064 | measurement/data/expansion-v1/cutoff-5885-review/TS_PROPERTY_FINAL_ADJUDICATION_20260908.md | `7d43ac37c43e5eef5f4f86dad4a8738e4e52945801008b5bcb8414183b4dab13` |
| exp-v1-typescript-generation-0087 | measurement/data/expansion-v1/cutoff-5885-review/JS_TS_FINAL_CONTRACT_ADJUDICATION_20260908.md | `47a779ab1fca686b69041c94492b08046616c10e20426a1824d8eabee6f81494` |
| exp-v1-python-generation-0220 | measurement/data/expansion-v1/cutoff-5885-review/PYTHON_MAPPING_ENUM_CLOSURE_20260908.md | `6bfe636fd24282b350cfe3b21838400df202de6e9273edf5654d3c9adc2e46b2` |
| exp-v1-javascript-generation-0270 | measurement/data/expansion-v1/cutoff-5885-review/JS_TS_FINAL_CONTRACT_ADJUDICATION_20260908.md | `47a779ab1fca686b69041c94492b08046616c10e20426a1824d8eabee6f81494` |
| exp-v1-python-generation-0517 | measurement/data/expansion-v1/cutoff-5885-review/PYTHON_MAPPING_ENUM_CLOSURE_20260908.md | `6bfe636fd24282b350cfe3b21838400df202de6e9273edf5654d3c9adc2e46b2` |
| exp-v1-rust-generation-0359 | measurement/data/expansion-v1/cutoff-5885-review/RUST_FINAL_CONTRACT_ADJUDICATION_20260908.md | `b7d4190075a713f3fe4bf5aed9574b9a97dfe93b0384cb049173dafaf1ec9fc5` |
| exp-v1-rust-generation-0396 | measurement/data/expansion-v1/cutoff-5885-review/RUST_FINAL_CONTRACT_ADJUDICATION_20260908.md | `b7d4190075a713f3fe4bf5aed9574b9a97dfe93b0384cb049173dafaf1ec9fc5` |
| exp-v1-java-generation-0788 | measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_74.md | `f3f3c73faa182c988a013fce83e23f5308b4ea5cec0f5d44f675994c9eb5056c` |
| exp-v1-java-generation-0781 | measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_74.md | `f3f3c73faa182c988a013fce83e23f5308b4ea5cec0f5d44f675994c9eb5056c` |
| exp-v1-go-generation-0740 | measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_46.md | `9712ed2076e11379f10dc836cda4f37e7d3ad299c26bfbb223a3f8dab216949b` |
| exp-v1-go-generation-0761 | measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_47.md | `46515d53a60b666e2286b52f51e970e782e54aad5a554698ad216e6832dba488` |

## Versioned recovery handoff and hard stops

1. Save cumulative original-quality closure, refresh the ledger hash, and approve an exact subset. This note does not constitute that approval.
2. Use the create-only versioned planner described in `docs/data/VERSIONED_RECOVERY.md`; reserve one globally unique rN. Bind original parent ID/canonical hash, corpus hash, ledger hash, source/rights object, hold/evidence content hashes, change class and explicit semantic rationale. Derived IDs must differ from parents; originals and old failing tests/results stay immutable.
3. Create the finalized derived specification/reference and preserve prompt/rendered-prompt hashes, raw author output, extraction, runtime/model identity and all generated artifact hashes. For contract clarifications, record the exact old/new semantic diff before tests.
4. Independently author tests from only the finalized derived specification, without visibility of parent/reference implementations or this implementation-specific fix recipe. A separate reviewer can subsequently add the known regression witnesses and review oracle correctness. Keep this independence provenance explicit.
5. Run the derived reference plus meaningful known-bad controls in the pinned network-disabled resource-limited sandbox; preserve all execution evidence. Original generation parents have no supplied known-bad repair source; do not pretend one was read or executed. Controls must demonstrate rejection of the actual defect and relevant plausible alternatives, not just syntactic failures.
6. Recheck all seven quality criteria, evaluation separation, duplicate/task-family overlap with retained parents and other derived rows, rights/attribution and new admission seal. Parent historical execution cannot stand in for derived-version execution. Do not admit both parent and near-identical recovery to inflate coverage.
7. No restoration to training, release gate advancement or success claim follows from a proposed fix alone. New defects or ambiguous semantic choices remain blockers to the specific derived candidate. These recommendations authorize no GCloud usage.

Counts: 12 provisional parents; six lanes × two; 13 full candidate reads including one excluded parser; zero generated/recovered/admitted rows; zero new execution.

