# Review continuation after the 165-record checkpoint

Inspected frozen indices 165–299; total 300/300. Static inspection covers
prompt, reference, original tests and known-bad diff. Standard-library-only
dependencies; test provenance traced separately. No automatic criterion pass.

- Python generation 0430: eight-neighbor counts, exact marking victory, terminal
  state guard, loss rendering and input copying agree. Orthogonal-only mutant
  caught. Tests require reveal returning None although prose leaves return
  unspecified; constructor tuple-length error classification is also vague.
- 0492: exact default types, conversion rules, bool/int distinction and ordered
  fresh output agree. Truthiness mutant caught. Finite restriction explicitly
  applies to string-to-float conversion, so accepting an exact float infinity
  is not automatically a defect. No new semantic defect identified.
- 0502: first equal marker search, order, duplicates and independent deep copies
  agree. Identity-comparison mutant caught. Arbitrary deepcopy-supported objects
  can have recursive or throwing equality, an input behavior envelope not
  discussed by the prompt; ordinary mutable marker tests are appropriate.

- Python 0503: validation-before-mutation, assignment-before-factory and exact
  returned identity agree. Factory-throw test catches ordering mutant. ASCII
  lexical identifier versus reserved keyword eligibility is not clarified.
- 0529: memo-before-recursion preserves cycles, sharing and child order; copied
  nodes/tags are detached. Late-memo mutant caught by cyclic graph test. Names
  validated at clone time, not construction, leaving wording ambiguity on when
  invalid names must raise. Long acyclic graphs can exceed recursion limit;
  supported graph-depth envelope not specified.
- 0588: operation order, sorted output, referential integrity and caller-data
  atomicity agree. Unhashable op value reaches dictionary membership and raises
  TypeError rather than required ValueError; same enum-validation pattern as
  0152. Tests omit this malformed case. Category deletion mutant caught.

- Python 0589: exact entry shape, alias validation, handler identity and deep
  copied configuration agree. Aliased-config mutant caught. Prompt contains an
  awkward 'Ask for a new implementation' residue, but intended API is clear.
- 0618: sync/awaitable sender and callback sequencing, return identity and
  exception replacement agree for Exception subclasses. Cancellation and other
  BaseException behavior are unspecified; deepcopy failure is caught as sender
  failure even though sender never ran. Need copy-failure/cancellation envelope,
  not an unsupported blanket failure-handler claim. Payload-alias mutant caught.
- 0666: generation order, escaping and ordinary validation agree. Validator
  omits nested locator child checks and source text/tail checks, accepting
  structure generator cannot produce. Focused sandbox probe prepared. XML
  character validity and locator normalization idempotence also deserve checks.
  Reverse source-order mutant is caught by original tests.

Focused follow-up: 0588 wrong exception reproduced (446 ms); 0368 read-only
Mapping deepcopy failure reproduced (666 ms); 0666 all three XML invalid-shape
tests returned True (490 ms). Each pinned sandbox execution exited 1 without
timeout, with complete task/output evidence in additional-holds.json. Three
additive holds recorded; no original candidate or VM evidence was changed.

- Python 0672: normalization, duplicate-after-trim detection, key order and
  deep attributes agree. Shallow-copy mutant caught. Annotated string attribute
  keys are not validated; whether annotations fall under all wrong-type errors
  needs explicit adjudication. No executed defect claim yet.
- 0680: increment-before-record, exact count, boolean rejection and fresh empty
  results agree. Wrong right-step mutant caught. Very elementary generation
  task raises non-triviality concern.
- 0689: exhaustive nonnegative triples and lexicographic order agree; max-large
  boundary mutant caught. Inner medium range can be tightened but is correct.
  Original tests check some totals rather than independent exhaustive oracle.
- 0733: immutable cards/draft, dispatch limits, identity retention and full
  directory validation agree. Tests preserve surrounding card whitespace;
  prose 'after trimming' is interpreted as validation, not storage normalization.
  Length mutant caught. Draft recipient malformed-type policy not specified.
- 0765: shared queue identity, earliest selection, successful-removal quota,
  owner reset and listener changes agree. No-item quota mutant caught. Returned
  item text is normalized though prose explicitly says trim for validation and
  comparison; storage normalization needs clarification, as do exact errors
  demanded by tests without explicit prompt classes.
- 0767: OLS and supplied diagnostic formulas agree on moderate data; prediction
  sign mutant caught. Exact floating SSE==0 determines perfect fit, so mathematically
  perfect but roundoff-affected inputs may miss special behavior. Finite-value
  overflow and leverage-one conventions are not fully specified. Original tests
  impose dictionary order although prompt only requires contained fields.
- 0792: inclusive Cartesian bounds, exclusions, lexicographic order and type
  rejection agree. Missing third upper boundary mutant caught; simple nested
  comprehension merits non-triviality review. No new semantic defect found.

- Python 0795: complete prevalidation, subtraction and one-based formatting
  agree for ordinary integers; numbering mutant caught. Explicit arbitrary-size
  integer promise conflicts with pinned Python's decimal conversion digit limit;
  a 5,001-digit value needs focused runtime reproduction.
- Python repair 0132: complete validation before deepcopy, preserved graph
  sharing/cycles and once-per-object shifting agree. Tests directly exercise
  duplicate object references and pre-copy validation. Original shallow-copy
  mutant caught. Output arithmetic overflow is not addressed by finite-input
  wording; full graph alias preservation may necessarily change nested views
  of a shifted record, which is consistent with those identity requirements.
- 0367: explicit missing sentinel rejects None converters; replacement clears
  cache and next conversion uses new callable. Stale-cache mutant caught.
  Tests demand None return for register/replace although prose does not specify
  return values. Redundant resolved cache is avoidable but inherited from repair.
- 0005: correct destination lookup, complete validation, fresh room lists and
  ordered duplicate suppression agree. Tests catch account-as-room lookup both
  when absent and present. No new semantic defect identified.

- Python repair 0015: bool-before-int dispatch, sorted tags and exact function
  alias agree. Wrong type-order mutant caught. 'Exactly' versus isinstance
  subclass acceptance is ambiguous. Unlike 0795, conversion explicitly uses
  str(value), so decimal-limit behavior is less clearly a contract violation.
- 0016: first occurrence retention, all-entry validation and deep copies in
  both modes agree. Last-occurrence mutant caught. Arbitrarily nested input
  depth is practically bounded by deepcopy recursion; no explicit depth policy.
- 0038: explicit membership distinguishes absent from None, stable matching
  and deep isolation agree. Missing-field mutant caught; no new ordinary-input
  semantic defect identified.
- 0050: immediate-neighbor differences, full validation and fresh empty output
  agree. Two-ahead mutant caught; elementary single-index repair has non-triviality
  concern.

0795 follow-up: pinned sandbox rejected a 5,001-digit valid integer with
ValueError at formatting (exit 1, no timeout, 429 ms). Full evidence is
`differences-large-integer-result.json`; additive hold recorded.

- Python repair 0085: modular identity, repeated squaring, exponent-zero/modulus
  one and negative multiplier semantics agree. Original tests use independent
  built-in pow oracle and huge exponent. Zero accumulator mutant caught.
- 0103: ordered mappings, duplicate rejection and copied values agree. Overwrite
  mutant caught; arbitrary values must be copyable for the broad guarantee to
  hold. No demonstrated defect within ordinary supported containers.
- 0138: full validation including rejected events, accepted-first category order
  and totals agree. Inverted acceptance mutant caught. float(amount) can overflow
  for mathematically finite integers; repeated numeric-envelope gap.
- 0152: Unicode casefold, first spelling, duplicate normalization and full late
  validation agree. Lowercase-only mutant caught with Straße. Noniterable outer
  error policy is not specified; no new semantic defect identified.
- 0166: stable sorting of deep copy, holdings/cash updates and sorted positions
  agree for ordinary values. In-place sort mutant caught. NaN passes positive
  price/nonnegative cash checks; unhashable side raises TypeError via membership.
  Numeric validation and malformed-side error policy need adjudication. The
  validation-before-processing test raises same ValueError for either path,
  so alone it does not prove validation order; static code does validate first.

- Python repair 0187: final partial window, exact callback count/order, immediate
  exceptions and returned object identity agree. Partial-window mutant caught.
  Input mutation by a user-supplied callback is not prohibited by implementation;
  no claim of shielding input from callback side effects.
- 0268: immediate memoryview-to-bytes copy enforces actual buffer support,
  sorting, overlap rejection and adjacency coalescing agree. Known-bad combines
  overlap and non-buffer acceptance defects although label mentions only overlap;
  both are real but multi-defect attribution should be recorded. Repeated bytes
  concatenation can be quadratic; no performance contract given.
- 0273: descending search from half excludes input itself and returns correct
  greatest proper factor. Original tests catch self-factor mutant. O(value)
  search and unused isqrt are poor idiomatic/efficiency signals; only small
  values tested and no complexity bound supplied.
- 0290: heap re-evaluates smallest eligible declaration after each step, handles
  duplicates, cycles and complete validation. Reverse-order mutant caught.
  Positive follow-up to Go 0720 scheduling issue, not corpus-wide clearance.
- 0312: exact origin offset, negative origins, deep get/set/snapshot and error
  boundaries agree. Off-by-one mutant caught. Elementary offset repair noted
  for non-triviality adjudication; no new semantic defect identified.

- Python repair 0353: body precedence, ordered duplicates and detached labels
  agree. Overwritten-full-text mutant caught. Output key/headline trim is inherited
  and tested though prose mainly specifies trimmed validation; clarify storage rule.
- 0355: explicit ASCII ranges correctly exclude Unicode letters/digits; original
  tests cover accented and fullwidth/Arabic digits. Unicode predicate mutant
  caught; no new defect identified.
- 0357: full-graph deepcopy preserves shared objects and isolates nested cells.
  Shallow-row mutant caught. Arbitrary depth wording exceeds recursive deepcopy's
  practical depth; routine one-call wrapper is a non-triviality concern.
- 0375: strict interior slice, argument-order independence and unchanged constant
  agree. Included-endpoint mutant caught. Elementary one-index repair noted.
- 0424: ASCII filtering, maximal runs, fallback, digit prefix and keyword suffix
  agree with examples. Decimal digits wording could mean Unicode digits but
  original source/tests consistently mean ASCII. Wrong-prefix mutant caught.
- 0447: registration retains callable without invoking, frozen state and order
  agree. invoke neither strips names nor rejects blanks with ValueError although
  global name rule says stripped/nonempty. Original tests omit whitespace/blank
  invocation; contract scope needs clarification. Registration-call mutant caught.
- 0473: standard finite-range normalization agrees on moderate inputs; wrong
  denominator mutant caught. [-1e308, 1e308] overflows subtraction, yielding a
  NaN output despite explicit [0,1] output promise; focused probe warranted.

- Python repair 0482 (index 206, final Python row): dependency-to-dependent edges,
  heap ordering, duplicate suppression and complete validation agree. Reversed
  edge mutant caught. Related scheduling sample follows the correct invariant.
- Rust generation 0192: STATIC HOLD. Prompt requires exactly one colon per
  locator/attribute entry. Original test demands data:x:y acceptance, and reference
  contains a literal exception `(key == "data" && value == "x:y")` to the colon
  validation. This is test-specific accommodation, not a defensible implementation
  of the given contract. Duplicate-attribute mutant is real but cannot clear this
  contradiction. Audit related targeted-repair/reference-special-case strata.
  LF versus CRLF line-terminator policy is another unresolved wording edge.
- Rust 0566: scalar/vector operand order, checked arithmetic, length validation
  and signed-atom parsing agree. Mismatched-vector mutant caught. Repeated atom
  parsing at operator positions can be quadratic; empty-list division by scalar
  zero policy is not specified clearly beyond generic division-by-zero wording.

0473 follow-up: finite extreme endpoint input returned [0.0, NaN], violating
the [0,1] output requirement (pinned sandbox exit 1, no timeout, 409 ms).
`scaling-finite-range-result.json` preserves the evidence; additive hold recorded.

- Rust generation 0630: exhaustive oriented paths, sorted output, input-order
  validation and checked totals agree when every explored prefix can complete.
  Overflow is raised on incomplete dead-end prefixes too, although contract
  specifies otherwise-valid full tours. A disconnected graph with overflowing
  three-node component should return empty tours, not CostOverflow; probe needed.
- 0702: malformed-field precedence, enum matching, unique-count PickMany and
  exact Ordering/Blanks content agree. Repeated-index mutant caught. Empty
  Blanks name collection is rejected though 'nonempty, unique field names' can
  mean each name rather than collection; tests do not settle empty collection.
- 0777: private nonzero field, const constructor/getter, MIN acceptance and
  checked doubling agree. Saturation mutant caught. Free constructor versus
  associated constructor is not completely explicit in prose; tests choose free.
  Private field inspected statically; tests do not include compile-fail access.

- Rust generation 0028: exact advance calls, saturation, explicit-only observes
  and immediate stop agree. Tests use independent counting Simulation; continue-
  after-stop mutant caught. No new defect identified.
- 0050: BTreeMap ascending overlay yields greatest-ID visibility, errors have
  specified precedence, copies and zero-dimension render agree. Reverse-overlay
  mutant caught. Literal no-trailing-newline rule conflicts with joining multiple
  zero-width rows; tests explicitly expect newline for width zero, height two.
  Record this edge-case wording conflict.
- 0065: shared Rc state, immediately ready operations, detachment and preserved
  nonfinite rect values agree. Wrong flag mutant caught. Public API sketch shows
  unit ElementHandle although required state needs private fields; interpret as
  abstract type sketch, but wording 'exact API' is misleading. Test's no-op raw
  waker uses unsafe, despite a safe Wake implementation being possible.

- Rust 0083: permission precedence, always-allowed Session, exact audit strings,
  sign-in/out resets and observation behavior agree. Wrong sign-in destination
  mutant caught; no new defect identified.
- 0097: little-endian word conversion, wrapping ARX schedule, feed-forward and
  validation priority agree. Independent test-author oracle structurally follows
  the fully specified formula, with zero-round hand-check; endian mutant caught.
  No claim of cryptographic suitability beyond this defined mixer.
- 0115: peer preservation/ASCII-only blank check, bypass precedence, copied
  anchors and bounded big-endian bundle parsing agree. Endian mutant caught;
  no new defect identified.

0630 follow-up: disconnected graph with an overflowing incomplete path returned
CostOverflow instead of no tours. Pinned rustc succeeded, test exited 101,
no timeout, 2,326 ms. Full evidence in `tour-dead-end-overflow-result.json`;
additive hold recorded.

- Rust 0119: constructor validation, title preservation, ordered removal and
  u64 page sum agree. Swap-remove mutant caught. Public Document fields allow
  bypassing constructor validation; Archive::add does not revalidate. Whether
  document invariants must also hold for direct literals is not expressly scoped.
- 0132: half-open wrapping interval, empty equal endpoints and validation priority
  agree without arithmetic overflow. Inclusive-end mutant caught. Straightforward
  predicate implementation merits non-triviality review.
- 0149: required traits, impulse/interval semantics, zero-length continuation and
  preserved error bounds agree. Begin-as-finish mutant caught. No new semantic
  defect identified; small enum accessor task has limited complexity.

- Rust 0160: duplicate attributes, case-sensitive key, exact values and major
  malformed syntax agree. Parser does not require whitespace between adjacent
  attributes; XML-like grammar versus expressly allowed spacing is underspecified.
  Duplicate-attribute mutant caught. No immediate malformed-short-string panic:
  prefix/suffix checks imply sufficient length for slicing.
- 0171: ready/reserved masks, ignored argument bit zero and full reset agree.
  Retained-reserved-reset mutant caught; small bitfield generation task has
  non-triviality concern.
- 0266: shared lock protects both indexes through each mutation; normalized
  lookups, duplicate rejection and reverse-index cleanup agree. Known-bad is
  minified but semantically drops reverse cleanup, caught by removal tests.
  Poison mapping inspected statically; original tests do not exercise poisoning.
- 0279: bit-seven preservation, idempotence and reset agree; overbroad clear
  mutant caught. Prompt says 'matching the reference signatures' but supplies
  no signatures or reference source, an explicit prompt/API completeness gap.
  Reference is heavily compressed and task elementary; criteria remain open.

- Rust 0283: bit ranges, enum rejection, Unicode scalar/control validation and
  exact rendering agree. Inverted priority mutant caught. Simultaneous label/raw
  invalidity priority is not specified, but original tests do not overconstrain it.
- 0291: exact IDs, global leaf uniqueness, exclusive cutoff and mutation-free
  errors agree. Cutoff-boundary mutant caught. Prompt omits Hub/Leaf field types,
  error variants and full accessor signatures while tests assume concrete shape;
  API completeness needs adjudication, not silent inference as a quality pass.
- 0328: checked ranges, validation-atomic writes, input-order overlap, dirty
  behavior and saturating commit agree. End-equality mutant caught. Saturation
  inspected in code, not exercised at MAX by original tests; state private.
- 0345: constructor validation, exact storage, default trunk and borrowed
  accessors agree. Wrong default-revision mutant caught. Method signatures and
  Kind variants are omitted in prose though tested; public enum permits direct
  invalid construction, so invariant scope should be explicit.

- Rust 0363: exact Gauge formatting, insertion order, duplicate rendering and
  unchanged empty captions agree. Reverse-iteration mutant caught. Generic
  Renderable permits custom types but tests only Gauge; elementary wrapper
  non-triviality remains open.
- 0466: validates all channels, including disabled IDs, before commands; checked
  wide frequency arithmetic and command order agree. Prompt omits Command
  variants/fields; original tests check command counts, not values/order.
  Disabled-ID validation mutant caught. API/coverage gap, not provenance failure.
- 0513: bounded count, wide products and range checks avoid overflow; output
  ordering and packed limits agree. Rejecting the allowed count 16 mutant caught.
- 0526: right-first ceiling-half interleave, odd left remainder, zero rounds,
  atomic excessive-round rejection and front drawing agree. Back-draw mutant
  caught; bounded deck length avoids count arithmetic overflow.
- 0558: normalized insertion, sorted zones, insertion-order IDs and cascading
  removals agree; orphan-tools mutant caught. Blank Zone lookup returns NotFound
  while prose says malformed names return Invalid, unlike RemoveZone's explicit
  rejection. Publicly constructible inconsistent maps also lack an invariant
  scope. Blank lookup needs a focused probe/contract adjudication.
- 0568: byte cap, submission ordering, continue-after-rejection, success count
  and exactly-once commit agree. Count-rejections mutant caught. Prompt omits
  Event fields and trait result signatures despite tests requiring exact shapes;
  API completeness remains open. CRLF uses standard Rust lines semantics.
- 0587: source order, safe header/payload bounds, offsets and endian decoding
  agree; little-endian mutant caught. Empty alias is classified InvalidUtf8 by
  reference/tests although prompt does not explicitly map this semantic error.
  Invalid service UTF-8 classification likewise should be made explicit.
- 0600: bounded indexing, both-direction contiguous counting, local-move outcome
  and validation-before-mutation agree. Missing ascending-diagonal mutant caught.
  No global terminal-state restriction is specified, so continued placement is
  not a defect; simultaneous invalidity precedence is not overconstrained.

- Rust 0603: FIFO, atomic paired configuration, watermark boundaries and clearing
  interrupt without removing data agree. Newest-peek mutant caught. No new
  semantic defect identified; allocation is incremental, not capacity-sized.
- 0617: Unicode whitespace/ASCII control checks, repeated command logging and
  saturation agree. Deactivate-inserts mutant caught. Internal lexical ordering
  and saturation cannot be feasibly established through current black-box tests;
  code uses BTreeSet and saturating_add as required.
- 0662: shared borrow before move and saturated adjustment agree; wrapping
  mutant caught. Tests verify arithmetic but not the requested borrow technique;
  tiny generation task raises non-triviality concern.
- 0677: exact mappings, concatenated byte checksum, literal path construction
  and ordered duplicate response fields agree. Secret-first mutant caught.
  Specification-only critic lineage already verified; no test-specific exception
  identified here, unlike 0192.
- 0699: two-pass text validation preserves atomicity; Unicode cells, newline
  reset and final-newline bounds agree. Off-by-one mutant caught. Dimension
  allocation uses saturating multiplication but impossible allocations can panic;
  no capacity/error policy is provided by the infallible constructor.
- 0779: exact module names, owned lookup, equal-height replacement and atomic
  regression rejection agree. Equal-height rejection mutant caught. No new defect.
- Repair 0383: placeholder lexical validation and literal substitution agree;
  missing-value mutant caught. Single braces rejected by reference/tests, though
  whether these count as unmatched delimiters is less explicit than double
  braces. Missing value before later malformed syntax has unspecified priority.
- Repair 0458: inclusive end/zero-length ranges, checked address arithmetic,
  copying and little endian agree. End-equality mutant caught. Prompt's supplied
  source also has a read_u8 type error; tested mutant isolates behavioral boundary
  defect after fixing that compile issue, so these are not identical bad sources.
- Repair 0098: final run, 255 splitting and bounded decompression agree;
  final-run omission mutant caught. Million-byte boundary exercised by originals.
- Repair 0123: canonical validation guards bounded field arithmetic; inverse,
  identity, zero-y doubling and scalar-zero behavior agree. Negation-sign mutant
  caught. Invalid-point negate behavior is not constrained like add/scale.

- Rust repair 0136: positioned nested expansion, absolute reset, above-root
  rejection and exact expansion limit agree. Early-limit mutant caught; unknown
  alias lookup precedes limit validation, unspecified simultaneous-error priority.
- 0158: filter before skip/take, stable insertion, borrowed results and atomic
  field changes agree. Limit-plus-one mutant caught, including zero and MAX offset.
- 0178: accessor coverage, channel/message order and edge trimming agree.
  Reversed IDs mutant caught. Zero-ID rejection comes from supplied source,
  not prose; single-bug repair context supports preserving it.
- 0202: explicit sender count separates observer lifetime, shared drains and
  last-sender close agree. Missing increment mutant caught. Poisoning is mapped
  in fallible methods but silently ignored in Clone/Drop; blanket no-panic and
  poison contract lacks scope for infallible lifecycle methods. No public poison
  path demonstrated; original tests are sequential only.
- 0237: escape state, Unicode ownership, exactly four nonempty fields and
  trailing-escape rejection agree. Trailing-slash acceptance mutant caught.
- 0243: strict comparison preserves self identity on ties, saturation and
  constructor fields agree. Tie mutant caught with pointer identity, not just
  value comparison. Small single-operator repair non-triviality remains open.
- 0245: exact expiry boundary, refresh skip and atomic invalid replacement agree;
  expiry-equality mutant caught. Constructor can accept an empty cached token,
  but prose expressly validates refreshed leases rather than constructor cache.
- 0261: split_once, trim, ordered duplicate selectors and last-wins sorted
  attributes agree. Over-splitting required assignment mutant caught.
- 0295: status-scoped insert versus cross-status update, validation before
  mutation and ascending references agree. Incomplete move mutant caught.
- 0322: all-byte wrapping FNV and exact session formatting agree; last-byte
  omission mutant caught. Toy authentication equates 64-bit digest equality
  with plaintext equality; collision/security scope is not stated. This should
  not be treated as a production password-storage example.

- Rust repair 0350: owned non-destructive reads, empty-value acceptance and sorted
  borrowed keys agree; destructive-read mutant caught with repeat lookup.
- 0385: strict attribute bytes, independent defaults, last recognized key wins
  and malformed unknown-key rejection agree. Inherited-style mutant caught.
- 0389: final block flush, blank suppression, ordered atoms and exact line errors
  agree; final-block loss mutant caught. i64 boundaries covered.
- 0393: correct directional signs and final-direction behavior agree; right-sign
  mutant caught. Nonnegative speed excludes i32::MIN negation overflow. Tiny
  literal/sign repair has a non-triviality concern.
- 0411: globally unique IDs, atomic referential validation, all accepted count
  versus distinct solved sum agree. Duplicate-count mutant caught. Saturating
  accumulation is present, but original tests cannot practically reach u64 MAX.
- 0466: trait default dispatch, unconditional hash prepend and exact announcement
  agree. Wrong-prefix mutant caught. Single-character repair is very elementary;
  custom Renderable behavior is not exercised by original tests.
- 0503: strict dimensional containment and checked multiplication agree;
  equality mutant caught. A zero final dimension after overflowing first product
  returns overflow rather than mathematical zero; prompt says checked u32
  multiplication and supplied source fixes its order, so scope needs clarity
  before treating this as a reference defect.
- 0032: streaming flatten preserves FIFO, bounded groups and no empty tail;
  reverse-queue mutant caught. Reference avoids source's huge eager capacity,
  and original tests explicitly exercise usize::MAX limit successfully.
- 0018: parity, negative/zero/boundary values and order agree; odd-filter mutant
  caught. Three-line one-operator repair is a strong non-triviality concern.
- 0025: checked decimal accumulation, leading zeros and full u64 boundary agree;
  wraparound mutant caught. No new semantic defect.
- 0040: validated topology, wide doubling, blocking-only cap and exact fields
  agree; physical/logical mixup mutant caught. Prompt identifies exact defect,
  reducing repair difficulty substantially.
- 0048: separator only between fields, empty fields and Unicode agree;
  leading-separator mutant caught. Equivalent standard join is elementary.

- TypeScript generation 0273: preview copying, toggles and normal invalid bytes
  agree; retained-array mutant caught. every() skips sparse holes, so a nonempty
  sparse number[] is accepted then spread to undefined bytes. Same repeated
  sparse-validation pattern; focused execution needed. Full public type shape
  is implicit in prose rather than exact signatures.
- 0345: false patches, sorting and defensive snapshots agree; truthiness mutant
  caught. Blank amend/drop return Feature not found rather than global invalid
  code message. Optional undefined versus absent patch field behavior unspecified.
- 0382: ordinary snapshot notification works, but unsubscription removes ALL
  subscriptions created by the same notifying parent, not just its own registration.
  Original test overwrites the older late-listener unsubscribe handle then expects
  both registrations gone. Reference's owner grouping accommodates that test and
  violates independent subscription semantics. Focused proof and hold required.
- 0390: normal sparse slots, frozen snapshots and unweighted mean agree;
  weighted-average mutant caught. Nonnegative integer indexes >= 2^32-1 become
  non-array properties, silently omitted by totals/snapshot. Finite total overflow
  envelope and NaN-accepting approximate test helper are additional concerns.
- 0010: exact eligibility/language comparisons and fresh notices agree;
  language-prefix mutant caught. Very elementary generation task. Malformed
  codes compare safely; undefined applicant is outside declared interface.
- 0070: ordinary successful/failed save baseline and detached notices agree;
  false-clears-dirty mutant caught. Reentrant writer can replace text and make
  saved baseline differ from text passed to writer; callback reentrancy unspecified.
- 0083: once-only loader, shallow fresh primitive-field parcels and error messages
  agree; discarded-Error-message mutant caught. String(reason) can itself throw
  for arbitrary non-Error reasons, contradicting unconditional return-not-reject
  unless input/error conversion envelope is clarified. Sparse parcel array policy
  unspecified, not automatically same as required integer-byte validation.
- 0121: exact-key lookup, copied primitive fields, order and targeted toggle agree;
  inequality mutant caught. Sparse initial map skips validation and later
  findIndex dereferences undefined. Prompt lacks field types and sparse policy;
  named entries imply valid objects but runtime validation envelope unclear.
- 0140: ordinary escapes, empty markers, route separator and text coalescing agree;
  escaped-separator mutant caught. Unknown/incomplete/malformed fallback copies
  raw backslashes despite global unescaping rule. Nested opener is accepted in
  note payload; non-nesting interpretation also needs an explicit decision.

- TypeScript 0156: literal segments, normalized separators, final unlinked node
  and fresh root/nonroot results agree. Clickable-final mutant caught.
- 0164: decision priority, exact normalized grant and defaults agree;
  requireChanges-default mutant caught. Blank grant validation precedes signed-out
  decision; prompt distinguishes validation from failure reasons only implicitly.
- 0251: own profile lookup, age validation and fresh views agree; reversed
  existence mutant caught. Routes retain table via closure but do not expose it;
  prompt forbids exposing aliases, not retaining a live lookup source.
- 0260: exact palettes, preserved text and fresh frozen output agree; wrong-color
  mutant caught. Pure constant lookup generation has non-triviality concern.
- 0269: label-first validation, original text, exact true and once-only writer
  agree; trim-before-write mutant caught. Tests resolve otherwise ambiguous
  simultaneous invalid label/writer precedence in favor of label.
- 0281: ordinary events, snapshots, post-mutation exception and promotion agree;
  wrong-end mutant caught. Duplicate same-function subscriptions unsubscribe by
  first indexOf, not registration identity: A/B/A then remove final A leaves B/A,
  violating retained insertion order. Focused probe needed. Reentrant rename can
  also change indexed return; event copies protect store but are shared between
  listeners, which prompt does not expressly forbid.
- 0319: supplied strings escaped, exact classes, order and blank rejection agree;
  unescaped-main mutant caught. Tests overconstrain equivalent apostrophe entity
  spelling to &#39;. Escaping alone is not URL-scheme sanitization, but prompt
  explicitly asks literal routes; do not imply this is production-safe HTML.
- 0330: normalized unique SKU, quantities, sorted copies and removal agree;
  aliased-item mutant caught. for-of does not silently skip sparse initial holes,
  though resulting type error for absent item is outside explicit field rules.
- 0348: busy precedence, own enumerable sorted keys and fresh primitive-field
  item copies agree; shallow-array mutant caught. Structurally extra nested item
  fields are copied shallowly, so deep-copy promise should scope to declared API.

- TypeScript repair 0208: two-phase insertMany, first offending candidate and
  exact IDs agree; incremental-mutation mutant caught. Reference ADDS a public
  find overload returning DroneRecord without null, contradicting preserved API
  and runtime null. Original test's non-asserting boolean helper does not narrow
  found2 before .model; reference papers over that compiler error with an unsound
  overload. Static API/test accommodation hold required.
- 0060: close-before-callback and cross-action idempotence agree; late-close
  mutant caught. Critic-origin tests cover throwing callback and preserve exact
  error identity. No new semantic defect identified.
- 0078: ordinary selective providers, full row validation and settled-only sum
  agree; reversed-status mutant caught. every/filter/reduce silently skip holes
  across all arrays; finite inputs can overflow revenue. Sparse/finite envelope
  needs related-stratum adjudication rather than automatic approval.
- 0145: normalized inclusive bounds, atomic failed set and fresh snapshots agree;
  unconverted-max mutant caught. Initial zero violates positive minimum but tests
  explicitly preserve it; 'last valid state' wording is misleading. Unbounded
  finite dozen quantity can overflow normalized count, policy unspecified.
- 0149: priority and first nonblank duplicates agree; message-first mutant caught.
  Parser stops after chosen value and never decodes irrelevant values, allowing
  malformed escapes later in query despite unconditional propagation rule.
  Focused probe required. URL trim is confirmed by supplied source/tests.
- 0166: normalized case-insensitive duplicate/filter and fresh results agree;
  case-sensitive mutant caught. Default locale lowercasing is environment-sensitive
  and broader Unicode casefold meaning unspecified; runtime pinned, not portable
  language-independent equivalence. No demonstrated new failure.
- 0174: clone-before-replace, cycle/duplicate rejection and visible preorder agree;
  always-traverse mutant caught. Repeated listener function uses indexOf and has
  same registration-order issue as generation 0281. Sparse trees can enter via
  map then throw during traversal. Original tests additionally demand listener
  exception propagation/stop without explicit prose policy.
- 0176: exact CSS and frozen bundles agree; descendant-selector mutant caught.
  Terminal-line-terminator acceptance was suspected from the regex anchor;
  the focused pinned sandbox probe REJECTED this hypothesis: all four terminal
  newline cases correctly threw TypeError. No hold from this concern.
- 0194: exact entity spelling, runtime tone/text checks and immutable input agree;
  raw-body mutant caught. No new semantic defect found.
- 0258: copied ordered entries and exact matching toggle agree; next-index mutant
  caught. Constructor for-of visits holes rather than silently admitting them.
- 0031: explicit unique registration objects correctly support duplicate listener
  ordering and idempotence; first-function-match mutant caught. Positive control
  for generation 0281 / repair 0174, with stronger explicit duplicate contract.
- 0018: worker count, ordered results, exact rejection and empty validation agree;
  single-worker mutant caught via deterministic gates, not timing thresholds.
  Other workers may continue after rejection; cancellation is not promised.
- 0046: one factory call, exact object identity and ordinary tag checks agree;
  unchecked assertion mutant caught. Callable objects with string tag are rejected
  despite structural NodeLike compatibility; object scope ambiguous. JSX
  compatibility is inspected statically; standard .ts harness does not establish
  a .tsx compile merely by rejecting malformed runtime outputs.

Initial inspection complete: 300/300 (Go 56, Java 60, JavaScript 30, Python 61,
Rust 62, TypeScript 31). This is not seven-criterion approval. Concrete pending
probes, explicit API/test holds and related-stratum audits remain before a
defensible quality decision. No training seal or revised partition exists.

Focused TypeScript follow-up: seven diagnostic tests compiled and failed at
runtime (no timeouts): sparse preview 3771 ms, sibling unsubscribe 3668 ms,
large accepted index 4282 ms, fallback escaping 4153 ms, timeline duplicate
registration 5139 ms, query malformed suffix 4870 ms, outline duplicate
registration 4805 ms. Each complete diagnostic/original task and pinned runtime
result is retained. The CSS terminal-newline control passed (4788 ms); it is
not a defect. With the static DroneDirectory API hold, there are now 38 additive
holds plus the original three, 41 total, not a revised admission count.
Original candidates and reports remain unchanged.
