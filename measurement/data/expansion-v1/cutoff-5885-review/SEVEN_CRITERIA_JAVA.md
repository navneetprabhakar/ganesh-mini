# Java frozen-sample criterion dispositions — 2026-09-07

All 60 original Java sample records are dispositioned below: 29 positive
seven-criterion reviews and 31 holds. This does not approve a stratum or seal
training data. Original sample/candidate bytes remain unchanged. Initial full
prompt/reference/test/known-bad reviews are in SECOND_BATCH_REVIEW.md and
THIRD_BATCH_REVIEW.md; open cases were reread during this adjudication.
Candidate SHA: 680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

The seven criteria and patch-size distinction are those stated in
SEVEN_CRITERIA_GO.md. Archived independent test lineage and standard-library
dependency isolation are established for all 60. Neither establishes reference
correctness. Holds remain reversible review exclusions, not final rejections.

Five previous positives are superseded by JAVA_SAMPLE_SCOPE_RECONCILIATION_V2.md.
Historical reconciliation-v1 preserves the earlier judgments and their hashes.

## Positive sample decisions (29)

Prefix for IDs: exp-v1-java-. Full original notes retain mutation/test evidence.
Acceptance is a bounded review judgment, not a proof over all Java objects,
arbitrary subclass behavior or allocations beyond the pinned sandbox envelope.

| ID suffix | Basis / resolution of prior concerns |
| --- | --- |
| generation-0662 | Explicit Java-whitespace normalization, ROOT casing and independent enum set. NPE is an allowed rejection of unspecified-class null input; the meaningful mutant concerns locale dependence, not exception selection. |
| generation-0137 | Numeric boxed-ID matching, stable update position and immutable snapshots. Identity-cache sensitivity is a portability caveat, not an observed failure under the pinned runtime. |
| generation-0253 | Full null validation across ragged rows, selective extraction and immutable order. |
| generation-0268 | Stateful acquisition/renewal/release validity and ordered result. Mutable nonempty output is allowed, though not separately promised; reference is consistent and the mutant changes state semantics. |
| generation-0308 | Identity-based traversal, shadow replacement without reorder and copied hierarchy. No fabricated cycle execution or unlimited-depth claim. |
| generation-0379 | Distinct synchronized mirror, sorted detached output and null validation. Prevalidation before mutation is a valid stronger implementation; not presented as a separately explicit rollback promise. |
| generation-0384 | Structured field parsing, exact flags, integer bounds and preserved description. No unrequested ASCII-only numeric grammar. |
| generation-0393 | Floor-modulo indexing, per-call accounting and independent arrays. |
| generation-0395 | Odd/even center expansion, earliest maximal tie and copying. No unstated linear-time requirement. |
| generation-0406 | Stateful stack machine, checked arithmetic, underflow and nondestructive emission. |
| generation-0434 | Simulated-time state transitions, inclusive threshold and checked addition. No invented invalid-state combinations. |
| generation-0458 | Complete null validation, ordered distinct difference and immutable snapshots. |
| generation-0636 | Exactly-once provider construction, same-panel delegation and error identity. Contract governs supplied Panel semantics, not deliberately misbehaving subclasses. Initial hidden state is permissible, not claimed uniquely mandated. |
| generation-0680 | First-ID position with last-value replacement, explicit null arrays and fresh output contacts. |
| generation-0739 | Atomic uniqueness, sorted kind indexes and immutable snapshots. |
| repair-0140 | Value-based ROOT comparison with complete null validation, including a malformed suffix after a match. |
| repair-0030 | Long rather than int parse domain, malformed-token handling and prescribed wrapping sum. |
| repair-0068 | Revision-based hit preserving cached null, no writes on hit and atomic replacement. |
| repair-0147 | Code-point prefix boundaries translated to UTF-16 offsets without splitting surrogate pairs. |
| repair-0184 | Long-width shifts repair both distance masking and sign-extension errors. Small patch, substantive language-width boundary. |
| repair-0219 | Coordinate shape derives the vertex bound used across all indexes; correction preserves divisibility/empty/domain checks. |
| repair-0372 | Common sampling factor, ceiling dimensions and deep copies within feasible primitive-array sizes. Integer-overflow concern requires multi-gigabyte primitive arrays outside the 512-MiB execution envelope; not claimed universally overflow-safe. |
| repair-0376 | Full null validation, FIFO bounded eviction and fresh mutable outputs. |
| repair-0414 | FIFO wraparound, unsigned byte read, clear/reset and full/empty errors. The unexecuted >1-GiB capacity index-overflow concern is outside the pinned 512-MiB envelope; no private-field manipulation used. |
| repair-0418 | Source context separates namespace/local grammar from their colon delimiter; full validation and stable membership filtering. |
| repair-0428 | Complete role/action policy matrix and malformed-input classes. |
| repair-0475 | Re-evaluated lexicographic readiness, complete graph validation and cycle detection. |
| repair-0499 | Frequency counts, ascending tie breaks, zero limit and copied mutable results. |
| repair-0512 | Copied ordered maps, checked accumulation and overflow atomicity. |

## Held sample decisions (31)

| ID suffix | Blocking criterion / evidence |
| --- | --- |
| generation-0394 | Executed U+2003-only input throws instead of zero; see JAVA_SAMPLE_SCOPE_RECONCILIATION_V2.md. |
| generation-0782 | Executed U+2003-only resource key accepted under nonblank contract; see v2 reconciliation. |
| repair-0041 | Executed U+2003-only segment accepted. Known-bad source trim does not unambiguously narrow prose nonblank contract; v2 supersedes earlier rationale. |
| repair-0241 | Executed U+2003-only property name accepted. Known-bad source trim does not unambiguously narrow prose nonblank contract; v2 supersedes earlier rationale. |
| repair-0243 | Executed U+2003-only snapshot name accepted. Known-bad source trim does not unambiguously narrow prose blank contract; v2 supersedes earlier rationale. |
| generation-0549 | Existing prompt/test contradiction: missing ID exception versus required null. |
| generation-0080 | Existing configuration-preservation versus normalization conflict. |
| generation-0514 | Existing full-validation failure after an early false result. |
| generation-0794 | Existing missing final no-swap trace pass. |
| repair-0325 | Existing explicit Java-whitespace token collapse failure. |
| generation-0619 | Reproduced nonblank title failure; null exception-class wording remains an additional concern, not a new executed claim. |
| generation-0032 | Reproduced nonblank product field failure. Abbreviated read signature does not rescue this defect. |
| generation-0185 | Reproduced nonblank item-title failure. |
| generation-0689 | Reproduced nonblank constructor failure; inheritance/boilerplate alone is not the hold. |
| generation-0737 | Reproduced blank owner returned from credential lookup. |
| generation-0564 | Reproduced loader invocation for blank key. Broader Error-versus-RuntimeException recovery is not separately executed. |
| generation-0738 | Reproduced blank-user all-results branch failure. Alias-value trimming remains an additional scope concern. |
| generation-0294 | Reproduced blank clip title accepted. No blanket Unicode casefolding claim. |
| generation-0170 | Reproduced index arithmetic requests VM-limit array for a valid one-element page of a compact virtual list. |
| generation-0313 | Reproduced eager allocation reaches VM array-size limit before rejecting a compact virtual list of null messages. |
| generation-0652 | Prompt clarity/API unresolved: exposed policy accessor names are unspecified; decimal syntax is silently narrowed by tests/reference. |
| generation-0305 | Prompt/API error-class conflict: invalid values require IAE but null message produces NPE, which original tests demand. Static comparison, no new null probe. |
| generation-0426 | Prompt/API incomplete: getIndex return type/returned object not stated while tests require Node rather than element. |
| repair-0058 | Prompt clarity unresolved: later concurrent mutations cannot be excluded throughout snapshot construction from an arbitrary mutable Map. No new race experiment claimed. |
| repair-0270 | Test/API overconstraint: private field names and representation modifiers demanded by reflection although public API preservation does not freeze private representation. |
| generation-0270 | Non-triviality not met: fixed-three-slot copy and direct Boolean assignments with independent guards. |
| generation-0271 | Non-triviality not met: elementary running-maximum counter with null/empty guards. |
| repair-0014 | Non-triviality not met: disclosed elementary OR-to-AND predicate correction. |
| repair-0130 | Non-triviality not met: exact required library call exposes the one argument correction. |
| repair-0222 | Non-triviality not met: direct two-field constructor copy/shift replaces mutation; no substantive algorithm or state interaction beyond that literal expression. |
| repair-0305 | Non-triviality not met: one direct codePointCount wrapper replaces length. |

## Executed evidence additions

JAVA_SAMPLE_ADJUDICATION_WORKING.md describes the first five Unicode probes.
Additional completed isolated Java probes, all exit [0,1], timed_out=false:

- java_0564_unicode_blank_probe-result.json: 4204 ms, loader invoked for U+2003 key.
- java_0738_unicode_blank_probe-result.json: 3892 ms, U+2003 user returns no records rather than all.
- java_0294_unicode_blank_probe-result.json: 3263 ms, U+2003 clip title accepted.
- java_0170_virtual_list_page_probe-result.json: 5556 ms, candidate-derived array-size request fails at ArrayList construction. Collections.nCopies stores a compact repeated-element list; correct final page has one element. No multi-gigabyte input was allocated.
- java_0313_invalid_virtual_list_probe-result.json: 3213 ms, null repeated-element list should fail at its first invalid element; candidate preallocates at Integer.MAX_VALUE before validation and receives Requested array size exceeds VM limit.

The latter two are candidate-requested illegal/oversized arrays, not host OOM
kills or evidence that a larger training VM is needed. Java diagnostics replace
the original test entry point; original tasks remain unchanged in the receipts.

21 new Java quality holds join five historical Java sample holds. Combined
Go/Java sample dispositions: 116 records, 73 positives and 43 holds; 184 sample
records still need criterion-specific disposition. Total register becomes
1110 additive plus historical three = 1113. Outside-sample coverage stays2960.
Repeated elementary Java targets require a new scope version; the generation
scope is already reopened, while the affected repair source/history must also
be reopened. No candidate rewrites, training seal or new VM.
