# Review continuation after the 100-record checkpoint

Inspected frozen indices 100–164; total 165/300. These are static inspections of
prompt, reference, original tests and known-bad diffs unless execution is stated.
All are standard-library-only. Provenance is traced separately in the sealed
all-300 chain report; no new teacher generation occurred.

- Java repair 0184: long mask fixes both int shift-distance truncation and sign
  extension; tests cover 31/32/63, invalid indices and idempotence. Realistic
  wrong-width literal mutant caught. No new defect identified.
- 0219: index upper bound, array shape and empty checks agree. NaN coordinate
  is explicitly accepted by tests and not forbidden by spec. Boundary mutant
  caught; straightforward bounds repair noted for non-triviality review.
- 0222: detached mutable point, normal wrapping arithmetic and null rejection
  agree. Tests cover bidirectional mutation and wraparound; alias mutant caught.
  Elementary constructor-copy repair, non-triviality concern.
- 0241: nullable value equality, exact name rendering, complete name validation
  and ordered changes agree. Tests catch reference comparison and validate even
  unchanged entries. No new semantic defect identified within trim semantics.
- 0243: constructor and getter clones preserve exact strings and new empty
  arrays; tests exercise both alias directions and invalid tags. Retained-array
  mutant caught. Blank-name Unicode envelope is not clarified beyond source trim.
- 0270: complete task validation, inclusive due boundary and stable sorting
  agree. Tests catch boundary mutant but also require private field names and
  final modifiers via reflection although immutability/API do not prescribe
  private representation. Record as test/API overconstraint.
- 0305: codePointCount handles paired and unpaired surrogates; tests thoroughly
  distinguish reversed/adjacent pairs. Wrong UTF-16 length mutant caught.
  Direct library wrapper remains a non-triviality question.
- 0325: case-sensitive adjacent collapse agrees for ASCII whitespace. Java
  whitespace requirement is not met by default regex \\s plus trim for U+2003;
  focused pinned-runtime probe compiled and failed (exit codes 0,1, no timeout,
  2,624 ms), preserving U+2003 instead of collapsing duplicate tokens. See
  `collapse-java-whitespace-result.json`. Original tests omit Unicode whitespace.
- 0372: ordinary ceiling-factor downsampling and deep copies agree; tests catch
  floor-division mutant and both-axis rounding. int ceiling-sum overflow is a
  large-dimension static concern, not a demonstrated small-input defect.

- 0376: full null validation, FIFO capacity eviction and fresh mutable empty
  results agree. Tests catch newest-event eviction; no new defect identified.
- 0414: clear resets head and size; unsigned FIFO, wrap and full/empty behavior
  agree. Tests catch stale-size clear mutant. head+size overflow at huge
  capacities is a static envelope concern, not an executed defect claim.
- 0418: full available/request grammar validation and ordered membership
  filtering agree. Tests catch inverted membership and verify mutable copies.
  Prose's allowed-character rule omits the colon delimiter but context/source
  clearly separate namespace and local characters; minor wording issue.
- 0428: exhaustive role/action matrix and error classes agree. Tests exercise
  all nine combinations and malformed strings; editor-delete mutant is real.
- 0475: priority queue re-evaluates lexicographically earliest ready node after
  every removal, unlike held Go 0720's scan strategy. Full graph validation and
  cycle detection agree. Tests catch reverse priority; this single related
  inspection is not a corpus-wide scheduling clearance.
- 0499: occurrence counts, descending frequency and ascending ties agree;
  tests use equal nonidentical strings and mutable zero/empty outputs. Reverse
  tie mutant caught. Complete null validation at zero limit is present.
- 0512: copied TreeMap, checked addition and immutable entries agree; tests
  catch input aliasing and verify overflow atomicity. No new defect identified.
- JavaScript generation 0160: static hold. Known-bad only returns a copied
  librarian from assignLibrarian instead of undefined, but prompt specifies no
  return value for this method. Original tests demand undefined. This is not
  a defensible semantic mutant under the given contract. CRUD/copies/order
  otherwise agree. Revision exception classification also needs clearer wording.
- JavaScript 0233: asynchronous notification sequencing, deep record copies,
  update validation and delete agree for tested dense arrays. Sparse ingredient
  arrays bypass some() validation; whitespace-only key/ingredients are rejected
  although only title is expressly trimmed for nonempty validation. Tests also
  require AsyncFunction constructor identity rather than just async behavior.
  Record these API/test concerns; no sparse-array execution claimed yet.

- JavaScript 0241: static hold: explicitly defaulted createSpecimenShelf(initial
  = []) is contradicted by reference arguments.length check and original test
  requiring no-argument TypeError. Ordinary IDs/order/copies otherwise agree;
  unrestricted integer IDs can exceed safe increment range, an additional
  numeric-envelope concern. Shallow list-copy mutant itself is realistic.
- 0292: confirmed strict-command defect. Object key coercion accepts boxed
  String('N') although command must be exactly one of the primitive strings.
  Pinned JavaScript probe fails missing expected TypeError (exit 1, no timeout,
  479 ms), preserved in `robot-command-type-result.json`. Grid validation
  correctly visits sparse rows/cells; original tests omit boxed commands.
- 0006: synchronous callback validation, per-job step IDs, copies and idempotent
  approval agree. Tests catch reversed step lookup and state isolation. Plain
  object is not required, so array-with-title is not automatically malformed.
  Callback-throw behavior under 'failed operations do not mutate' is unspecified;
  no rollback claim for user callback exceptions.

- JavaScript 0124: Map equality/recency, oldest eviction and fresh array with
  intentionally shared values agree. Tests cover NaN, undefined, object identity
  and signed zero. Newest eviction mutant caught; invalid capacity error class
  is prescribed by tests but not expressly by prompt.
- 0173: recursive detached normalization and identity-cycle guard agree for
  dense media arrays. Sparse media bypasses map validation; original tests omit
  holes. Missing author/counts still throw TypeError via property access. Arrays
  with properties are not explicitly excluded by the object-shaped contract.
- 0196: bounded binary search avoids multiplication comparisons and covers
  safe-integer square boundaries. Perfect-square strict comparator mutant caught.
  No new defect identified; bound constant deserves explanatory comment.
- 0206: ordered position-based rows, integer cent formatting and detached values
  agree for dense inputs; MAX_SAFE_INTEGER is tested. Sparse record arrays bypass
  map validation, another instance of the same JavaScript validation gap.
- 0218: async rejection ordering, selection order and fresh options agree for
  tested inputs. Tests reject whitespace-only strings while prompt says nonempty
  without declaring trim for validation; explicit contract clarification needed.
- 0230: canonical decimal grammar, exact field order/case and outer trim agree.
  Tests reject boxed strings and leading-zero mutant. No new defect identified.
- 0254: confirmed identity-conversion defect. MAX_VALUE seconds to seconds
  returns Infinity after intermediate multiplication, violating same-unit value
  preservation. Pinned probe exit 1, no timeout, 341 ms in
  `duration-identity-result.json`. Unit key lookup also coerces boxed values
  despite string requirement; original tests omit both cases.
- 0296: confirmed valid-JSON-key cloning defect. Own __proto__ key changes clone
  prototype, causing later clone to return the stored object directly. Mutating
  get result changes repository state. Pinned probe exit 1, no timeout, 362 ms in
  `profile-json-key-result.json`. Original tests use ordinary nested keys only.
- 0319: title/seat validation, trim and ordering agree for dense arrays. Sparse
  topics bypass map validation; original tests omit holes. Repeated sparse-array
  pattern needs affected-stratum audit, not isolated silent exclusions.

- JavaScript 0335: confirmed safe-integer arithmetic defect: previous from page
  3 with MAX_SAFE_INTEGER pageCount yields 1 instead of 2 because intermediate
  addition rounds. Pinned probe exit 1, no timeout, 676 ms. Original tests cover
  revision overflow but not large pageCount arithmetic. Other transitions agree.
- 0339: confirmed required-handler validation defect. on('topic') accepts an
  omitted handler because shared validator allows undefined for publish. Pinned
  probe fails first assertion (exit 1, no timeout, 494 ms); off(undefined) is
  statically affected but second assertion was not reached. Original tests use
  null, not undefined. Snapshot publication and live-set mutant otherwise agree.
- 0374: dense fee validation, quantities and fee multiplication agree, with
  for-of correctly visiting sparse array holes. Extent decimal grammar rejects
  signs/exponents; arbitrarily large decimal strings can normalize to Infinity
  because finiteness is not checked. Fee overflow/zero-times-infinity behavior
  and extent representable-range policy require adjudication, not an invented
  finite-output guarantee. Handling-fee mutant is realistically caught.

- JavaScript 0394: copies, insertion order and ordinary patch validation agree.
  Object.keys ignores non-enumerable and symbol own patch properties despite
  the explicit own-property restriction; focused validation needed. Description
  trimming is tested but only SKU normalization is explicit in the prompt.
  Internal-record-return mutant is realistic and caught.
- JavaScript repair 0054: explicit own-property definition safely copies
  __proto__, and indexed own checks reject array holes. Ancestor tracking rejects
  cycles while allowing reused acyclic objects. Tests cover these boundaries,
  case-preserving header values and normalization collisions. Symbol-header
  policy is not explicit; no new demonstrated defect. This is one positive
  comparison, not clearance of the related cloning/array strata.
- 0096: ready-state transition, queue detachment, immediate reentrant callbacks
  and exception propagation agree with the explicit contract. Tests exercise
  exception/no-replay, nesting, validation and state isolation. Late-callback
  mutant is realistic and caught; no new defect identified.
- 0111: declared accumulator fixes strict-mode ReferenceError; left-to-right
  reduction, no input mutation and no global agree on dense arrays. some/reduce
  skip holes, another sparse-input validation concern. Original tests omit holes.
  Single-declaration repair is a non-triviality concern.
- 0132: precise four-character whitespace rule, all four formula prefixes and
  CSV escaping agree on dense input. every/map skip holes, another array-type
  validation concern. Tests catch incomplete-prefix mutant but omit sparse input.
- 0144: for-of explicitly visits holes, and original tests reject sparse arrays.
  Named copies, odd-sequence repetition, error classes and isolation agree.
  Odd-length mutant is realistic and caught; no new defect identified.

- JavaScript repair 0147: GET-only storage, response validation even for POST,
  detached outputs and clear counts agree; POST mutant is realistic. Whitespace
  keys rejected by reference/tests despite prose saying non-empty, a wording gap
  also inherited from supplied source.
- 0227: exact doubled length, strict types and fresh byte arrays agree; tests
  include final newline rejection and mixed hex case. Wrong-length mutant caught.
  Single multiplication repair is a non-triviality concern.
- 0229: zero and 130 boundaries, preserved names including whitespace-only
  strings, validation and no mutation agree. Falsy-zero mutant caught; elementary
  guard removal remains a non-triviality concern.
- 0231: exact spread ordering, distinct new arrays and deliberately shallow
  metadata preservation agree. Stale-width alias mutant caught; simple literal
  replacement remains a non-triviality concern.
- 0239: own source validation, same-key copy and nested reference preservation
  agree. Computed property syntax safely handles __proto__. Reversed assignment
  mutant caught; shallow-copy non-enumerable semantics are not expressly defined.
- 0240: exact-before-wildcard priority and snapshotting agree on dense input.
  map skips holes so malformed sparse routes are accepted during construction;
  later find can throw on a hole. Tests omit this repeated sparse validation
  pattern. Uppercase permits uncased characters; alphabet-only is not specified.
- 0249: supported token boundaries and output conversion match ordinary tests;
  identifier-suffix mutant caught. Decimal identifier suffixes can be partially
  matched after a dot (for example r1.5px), despite unit-like-text wording; needs
  adjudication against the explicitly immediate-predecessor rule. No unexecuted
  counterexample is claimed as confirmed.
- Python generation 0152: frozen fields, canonical address, boolean CPU
  rejection and detached metadata agree. Set membership on an unhashable
  platform raises TypeError rather than mandatory ValueError; static defect to
  probe. Tests omit unhashable platform values. Arbitrary Mapping deep-copy
  failures are outside a clearly specified copyability envelope.

- Python 0263: maximal-run sanitization, lowercase-only extensions, chapter
  ordering and deep copies agree. Tests catch missing regex quantifier and
  both input/output aliasing. URL strings accepted solely as nonempty can still
  fail URL parsing later; valid-URL envelope should be clarified. Empty export
  deliberately does not validate prefix, consistent with explicit empty result.
- Python 0271: border geometry, palette, adjacency/non-overlap and offset canvas
  agree. Tests catch wrong palette and exercise dimensions/types. Reference
  accepts general iterables although prose says sequence; tests do not decide
  whether broad iterable acceptance is intended. No new confirmed defect.
- Python 0619: required shared tokenizer/encoder vocabulary and separate decoder
  and scorer state agree, with thorough alias tests. Original test additionally
  requires nested component field locations (including backend on every component)
  that prose does not fully enumerate. Record API schema underspecification;
  the separate-encoder-vocabulary mutant itself is explicitly invalid and caught.

Focused follow-up execution (all pinned, network-disabled sandbox; exit 1 and
no timeout for each): JS 0394 hidden own patch accepted (399 ms); repair 0111
sparse readings accepted (347 ms); repair 0132 sparse cells accepted (358 ms);
repair 0240 sparse routes accepted at construction (478 ms); Python 0152
unhashable platform raises wrong exception class (429 ms). Full original tasks,
diagnostic tasks, runtime identity, hashes and stderr are in their respective
`*-result.json` files referenced by additional-holds.json. These five observations
are now additive holds. Sparse validation is a repeated pattern requiring
affected-stratum review, not a waiver through individual removal.

- Python 0754: normal distance, upward rounding, clamping and fresh point tuples
  agree. Static contract conflict: invalid point sizes require ValueError but
  reference and tests require TypeError. Very large finite products can overflow
  before a finite maximum is applied; this numeric envelope is not tested.
- Python 0759: sorted matrices, deterministic split, copies, fitting, tie-to-zero
  and scoring agree for ordinary finite values. Tests catch reversed distance
  comparison. Finite large inputs can overflow centroid sums and squared
  distances; range/precision envelope is unspecified beyond finite inputs.
  Score's list-only labels requirement is stronger than explicit prose.
- Python 0041: complete validation, matching day sets, sorted fresh dictionaries
  and weighted combined denominator agree, including individual/combined zero
  cases. Wrong denominator mutant is realistic and caught. No new defect found.

- Python 0058: exact shapes, hashability, per-ID coverage and inclusive
  tolerances agree for ordinary values; boundary mutant caught. Float running
  sums can overflow/cancel and very large integers can overflow isfinite
  conversion; numeric range/accumulation semantics need explicit limits.
- Python 0127: exact schema, ordered columns/rows, empty-width tables and deep
  nested copies agree. Shallow-row-copy mutant caught. No new defect identified
  within ordinary deep-copyable input values.
- Python 0200: rectangular dimensions, deep input/output isolation, read-only
  index, cyclic stepping and reset agree. Tests catch shallow constructor copy
  and validate rejected step operations leave state unchanged. No new defect.
- Python 0237: formula, built-in rounding and hex conversion agree on tested
  finite values; truncation mutant caught. Positive infinite rate is not
  explicitly excluded by prose but zero-step computation produces NaN; huge
  integer conversion and rate finiteness need clarified numeric envelope.
- Python 0246: bounded BFS, endpoint validation, iterable obstacles, duplicates
  and adjacent movement agree. Missing-boundary mutant finds an invalid route
  in original blocked-route test. No new defect identified.
- Python 0259: catalog order, duplicates and deep copies agree. Static mismatch:
  prompt accepts mapping labels but reference restricts to dict; UserDict or
  MappingProxyType would be rejected. Tests exercise dictionaries only. Original
  store-by-reference mutant remains valid and caught.

- Python 0268: casefold/split, unknown IDs, distinct special IDs and independent
  source/target padding agree. Tests catch source-width target padding. Arbitrary
  keys retained unchanged can be mutable lists, conflicting with broad no-output-
  list-alias wording; key identity exception needs clarification. Item sequence
  versus general iterable acceptance also underspecified.
- Python 0269: threshold order, stable entry order, equality placement, shape
  validation and new bucket containers agree. Equality mutant caught. Numeric
  is implemented as Real (not arbitrary numeric types); huge-int finiteness and
  mutable hashable ID alias envelope are not covered by ordinary tests.
- Python 0290: sample order, retained entire profiles, corrected labels,
  unrelated data preservation and deep copying agree. Mutating-input mutant
  caught. Dataclass defaults are implementation extras not mandated by tests.
- Python 0313: staged updates preserve atomicity, quantities remain nonnegative,
  snapshots sorted and detached. Alias-return mutant caught. items-based duck
  typing broadens Mapping acceptance; no concrete ordinary-input failure found.
- Python 0368: name grammar, final-dot extension, truncation and callable identity
  agree. migrate_schema accepts Mapping but deepcopies then mutates it; immutable
  mappings such as MappingProxyType cannot follow that path. Same broad mapping
  support issue as 0259, warrants focused reproduction. Other-value aliasing
  inside input also needs preservation-versus-targeted-replacement clarification.
- Python 0369: stride selection, strict zero-crossing, ordered partition output,
  one-hot vectors and detached mutable deserialization agree. Boundary mutant
  caught. Finite inputs can overflow summary features which deserialize then
  rejects; numeric range closure is not addressed in original tests. Some long
  validation lines reduce readability, not by themselves a semantic rejection.

Next frozen index: 165. No training-ready seal or changed original partition.
