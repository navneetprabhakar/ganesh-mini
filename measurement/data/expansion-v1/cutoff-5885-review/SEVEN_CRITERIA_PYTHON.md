# Python frozen-sample criterion dispositions — 2026-09-07

All 61 original Python sample records are dispositioned below. Initial complete
prompt/reference/test/known-bad inspections are in THIRD_BATCH_REVIEW.md and
FOURTH_BATCH_REVIEW.md; open contracts were reread and selected boundary cases
executed in pinned sandboxes. Original candidates/sample remain unchanged.
Candidate SHA: 680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
Seven criteria and small-patch distinction follow SEVEN_CRITERIA_GO.md.
All 61 have archived independent test lineage and standard-library dependencies.
Positive review is not admission; holds are reversible, not final rejection.

## Positive decisions (32)

Prefix: exp-v1-python-.

| ID suffix | Basis / resolution |
| --- | --- |
| generation-0263 | URL-path extension selection, maximal-run sanitization, unique chapter order and detached copies. URL inputs are interpreted as URLs; no claim that malformed URL syntax must export successfully. Empty export expressly ignores prefix. |
| generation-0041 | Complete matching-day validation and weighted denominator, including combined zero. |
| generation-0127 | Exact table schema and independently copied nested values within deepcopy-supported inputs. |
| generation-0200 | Rectangular shape, copied cells, cyclic transitions and rejected-step state preservation. |
| generation-0246 | Bounded BFS, obstacles and endpoint validation with realistic boundary mutant. |
| generation-0268 | Independent source/target widths and special-ID checks. Explicit unchanged key retention governs keys; no-output-row-alias rule governs newly allocated batch/row containers, not a new key cloning requirement. |
| generation-0290 | Correct label rewriting, preservation of unrelated profile data and deep isolation. |
| generation-0313 | Atomic staged inventory, nonnegative quantities and sorted independent snapshots. Extra items-based duck typing does not demonstrate failure on required Mapping inputs. |
| generation-0430 | Eight-neighbor game state, exact marking and terminal behavior. None is a permissible unspecified reveal return; meaningful mutant changes neighbors. |
| generation-0492 | Exact default-type conversion and bool/int distinction. Finite restriction is specifically for string-to-float conversion. |
| generation-0502 | First equality match, order and independent copied outputs. No guarantee for deliberately throwing equality implementations. |
| generation-0503 | Complete validation before side effects, assignment before factory, exact identity and exception behavior. Explicit ASCII lexical grammar governs identifiers; no unrequested reserved-keyword exclusion. |
| generation-0589 | Entry shape, normalized unique aliases, callable identity and independent configuration. Residual prose does not obscure the API. |
| generation-0689 | Bounded integer combination search, nonnegative remainder divisibility and ordered exhaustive solutions. Not merely a direct literal/library wrapper. |
| generation-0733 | Immutable records, complete directory validation and dispatch constraints. Trimming is for validation; surrounding card text is preserved. |
| repair-0132 | Prevalidation and whole-graph deepcopy preserve repeated identities while shifting each object once. No separately promised finite output. |
| repair-0367 | Missing sentinel, converter replacement and cache invalidation. None return is permissible and not the semantic mutant. |
| repair-0005 | Destination-based lookup, all-entry validation and ordered duplicate suppression with fresh lists. |
| repair-0015 | bool-before-int dispatch, exact alias and sorted tagged output. Supplied isinstance source establishes subclass-aware repair context; explicit str(value) governs integer conversion. |
| repair-0016 | First occurrence retention, late validation and independent output in both modes; ordinary deepcopy-supported envelope. |
| repair-0038 | Missing versus None distinction and stable deeply copied selection. |
| repair-0085 | Repeated squaring, modular identity and huge exponent with independent built-in pow oracle. |
| repair-0103 | Ordered mapping composition, duplicate rejection and copied supported values. |
| repair-0152 | Unicode casefold deduplication with first spelling retained and late validation. |
| repair-0187 | Final partial window and exact callback count, order, result identity and exception propagation. No shielding from callback-authored side effects. |
| repair-0268 | Actual buffer conversion, immutable input copy, sort and overlap/coalescing. Known-bad has two real defects despite its narrower label; no single-defect attribution claim. |
| repair-0290 | Heap re-evaluates smallest eligible declaration, full graph validation and cycle rejection. |
| repair-0312 | Offset boundary is shared by get/set, with negative origins and deep-copy state boundaries. Small patch in a substantive stateful API. |
| repair-0353 | Source-defined trimming, full schema validation, body precedence and detached labels. |
| repair-0355 | Explicit ASCII predicate excludes non-ASCII letters and digits; substantive Unicode/ASCII distinction. |
| repair-0424 | Source-defined ASCII grammar, maximal runs, fallback and keyword-safe naming. |
| repair-0482 | Dependency direction, dynamic heap ordering, duplicate suppression and validation. |

## Held decisions (29)

| ID suffix | Blocking criterion / evidence |
| --- | --- |
| generation-0152 | Existing executed malformed platform exception mismatch. |
| generation-0754 | Existing invalid-shape error-class contradiction. |
| generation-0259 | Existing required Mapping restricted to dict. |
| generation-0368 | Existing read-only Mapping copy/mutation failure. |
| generation-0588 | Existing executed malformed operation exception mismatch. |
| generation-0666 | Existing executed XML invalid-shape acceptance. |
| generation-0795 | Existing explicit arbitrary-size integer formatting failure. |
| repair-0473 | Existing executed extreme finite normalization outside [0,1]. |
| generation-0759 | New executed prediction OverflowError for two one-feature centroids and a query exactly at centroid zero. |
| generation-0058 | New executed OverflowError validating an exactly conserved finite integer. |
| generation-0237 | New executed OverflowError for valid nonnegative integer steps with a bounded limiting tint. |
| generation-0269 | New executed OverflowError for a finite integer threshold and identical value; comparison needs no float conversion. |
| generation-0369 | New executed constant-signal mean assertion failure; static sum overflows despite representable mean. |
| generation-0529 | New executed RecursionError cloning a 1200-node acyclic graph; small memory footprint and no stated graph-depth restriction. |
| generation-0672 | New executed non-string attribute key acceptance against dict[str, object] and wrong-type rejection contract. |
| generation-0767 | New executed OverflowError fitting three finite scaled x values to a finite line. |
| repair-0138 | New executed OverflowError validating a finite integer amount before otherwise exact integer aggregation. |
| repair-0166 | New executed NaN accepted as a positive price. This is not a claim about unspecified infinity policy. |
| generation-0271 | Static clarity/type hold: sequence requirement and wrong-type rejection versus general iterable materialization; valid-sequence behavior alone does not settle broader acceptance. |
| generation-0619 | Static API hold: nested component field schema and backend locations required by tests are not fully specified. |
| generation-0618 | Clarity hold: copy failures are sent to on_failure even though the sender never ran; payload copyability and failure-domain boundary remain unspecified. No cancellation failure claimed. |
| generation-0765 | Clarity hold: validation/comparison trimming versus stored/returned item normalization not resolved by generation prompt. |
| repair-0447 | Static global name-rule mismatch: invoke does not strip or reject blank names with ValueError. |
| generation-0680 | Non-triviality: direct repeated increment of two counters under an explicit formula. |
| generation-0792 | Non-triviality: literal bounded Cartesian comprehension with a direct sum filter. |
| repair-0050 | Non-triviality: disclosed adjacent-index correction in an elementary difference comprehension. |
| repair-0273 | Idiomatic/complexity concern: downward linear scan despite supplied unused isqrt, with no bounded numeric envelope. No new timing failure claimed. |
| repair-0357 | Non-triviality: direct deepcopy wrapper; explicit arbitrary-depth wording also remains unresolved. |
| repair-0375 | Non-triviality: endpoint slice correction over a fixed seven-stage tuple. |

## New executed evidence

Every result below preserves original task, diagnostic task, hashes, pinned
Python 3.11.15 identity, output and resource contract: network disabled, 1 CPU,
512 MiB, 64 PIDs, 60-second timeout. All exit [1], timed_out=false. These replace
the test entrypoint; original tests/mutants were not rerun by these diagnostics.

| Result file stem (append -result.json) | Milliseconds |
| --- | --- |
| python_0759_large_distance_probe | 328 |
| python_0058_large_integer_probe | 350 |
| python_0237_large_steps_probe | 463 |
| python_0269_large_integer_probe | 335 |
| python_0369_constant_mean_probe | 353 |
| python_0529_deep_graph_bounded_trace_probe | 331 |
| python_0672_attribute_key_probe | 396 |
| python_0767_scaled_line_probe | 332 |
| python_0138_large_integer_probe | 330 |
| python_0166_nan_price_probe | 430 |

Initial python_0529_deep_graph_probe also failed (522 ms) but hit the output
capture limit before the terminal traceback line. Preserved unchanged; the
bounded-trace rerun explicitly catches only RecursionError and records it.
Repeated numeric and elementary patterns require criterion-scoped stratum
follow-up; historical semantic coverage is not automatically that follow-up.
