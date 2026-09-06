# Continued semantic review — in progress

Inspected frozen sample indices 12–99, bringing unique inspection to 100/300.
The previously reviewed Go repair 0465 is index 37 and is counted only once.
This is not a passed sample. References, original tests, and known-bad diffs
were read, not inferred from execution counts. All use standard-library-only
dependencies. Test provenance is now traced for all 300 in
`test-origin-all300-chains.json`: 297 unchanged original tests and three
specification-only critic chains. This is separate from semantic review.

- Go generation 0270: severity filtering, locked sequence allocation and
  independent snapshots agree; tests cover concurrency and boundary filtering.
  Reverse-threshold mutation is realistic. Open wording concern: reference
  uses a package-level mutable map despite the no-global-mutable-state rule.
- 0302: range checks precede label indexing; stable filtering, exact message
  preservation and non-nil independent results match. Equal-threshold mutant
  is covered. Simple but combines invalid-enum handling and ordering.
- 0330: confirmed reference bug. Missing map-key membership checks make
  distinct empty-valued label keys compare equal. Additive pinned sandbox
  probe returned action none instead of update, exit 1, no timeout, 25,845 ms.
  Original tests cover changed values and lengths, not this key-presence edge.
  Hold separately; source and executed probe are preserved in
  `reconcile_empty_labels_test.go` and `reconcile-empty-labels-result.json`.
  Minified reference also weakens idiomatic-code quality.
- 0351: trims queries only, counts exact scope/locator matches before validating
  the unique matched record, ignores irrelevant malformed records and preserves
  stored values. Scope-omission mutant is realistic and exercised.
- 0354: validates all capacity fields and trimmed IDs before writes, returns
  independent copies of defaults/overrides, handles nil receivers. Aliased
  override mutant is directly caught. No zero-value guarantee is inferred.
- 0361: validates all rows before batching, uses UTC from explicit timestamps,
  byte-plus-newline sizes, strict-exceed rollover and isolated oversized lines.
  Tests exercise Unicode bytes and exact capacity. Open specification envelope:
  unrestricted int64 timestamps can format years beyond four digits; no bound
  or policy is declared. This is not an executed defect finding.
- 0366: both subset checks are correct and highest-bit/zero tests are present.
  Reverse subset mutant is realistic. Tests additionally insist on zero result
  on error although the prompt specifies only success output; API/test
  consistency needs adjudication. Do not silently strengthen the prompt.
- 0388: per-line CSV decoding, trim-after-decode, ASCII SKU grammar, integer
  parsing, duplicate rejection and bytewise sorting align. Tests reject multiline
  quoting and malformed fields. Missing-sort mutant is real. Whitespace before
  an opening quote is not expressly granted by standard CSV semantics.
- 0397: qualified-key construction, duplicate collapse, nil receiver semantics,
  fresh sorted slices and invalid-before-missing precedence match. Missing
  scope mutant is exercised. Do not add unrequested separator restrictions.
- 0405: finite nonnegative decimal validation, copied scalar values and exact
  unit grammar match. Tests cover NaN, infinities, nil, suffixes and zero.
  NaN omission is a realistic numeric-validation mutant.
- 0416: immutable value receiver, disabled identity and byte-preserving marker
  concatenation match. Tests include malformed UTF-8 and interface assignment.
  Non-triviality concern: validation plus a simple concatenation branch.
- 0560: validates lookup indices, searches nearest-to-base with map presence,
  preserves zero values and returns no partial output. Tests cover nil maps,
  precedence and mutation. Forward-search mutant is realistic and killed.
- 0680: exact segment structure, case folding only for labels, value validation
  and canonical String match. Tests cover Unicode whitespace and case
  preservation; lowercasing-values mutant is real.
- 0690: configuration/resource deep copies, exact pair keys, locked CRUD and
  sorted independent list results match; concurrent creation and alias tests
  exercise the map-return mutant. Stable CSRF token is explicitly required by
  this in-memory exercise, not suitable as a real authentication recommendation.
- 0720: confirmed reference defect in ready-step priority:
  a full forward scan can run a later ready step before an earlier step newly
  unblocked by the preceding callback. Probe for a<-b plus independent c
  returned b,c,a instead of b,a,c (exit 1, no timeout, 26,150 ms), preserved in
  `plan-ready-order-result.json` with the exact additive test.
  Original test layout does not expose that interleaving. Transitive-skip mutant
  is otherwise realistic and covered.
- 0767: locking, credential copies, malformed-call precedence, single-use
  challenges and deterministic counters match ordinary cases. Open conflict:
  Enter deletes the challenge before detecting pass-counter exhaustion, despite
  the no-state-change exhaustion clause. Tests do not reach exhaustion; no
  executable overflow result is claimed. Requires contract/edge adjudication.
- 0780: ASCII tokenization, sentence unions, distinct-term scoring, positive
  maximum ties and note/ID ordering match. Rules validate even for empty notes;
  tests cover no partial output and duplicate term normalization. Dropped-tie
  mutant is exercised. No new defect identified.
- 0791: private token exclusion, number-preserving object decode and trailing
  JSON checks align. Confirmed exact-key defect: struct JSON decoding can
  accept differently cased field names despite the declared exact keys.
  Focused probe accepted both Label and Level variants (exit 1, no timeout,
  26,858 ms), preserved in `device-exact-keys-result.json`. Original tests omit
  case variants. Duplicate
  exact keys are otherwise checked and the trailing-object mutant is covered.

- Generation 0827: registry copies, generation updates, disabled refresh,
  length-prefixed keys and observer snapshot/order match the contract. Tests
  cover callback registration changes, panic propagation and Unicode keys.
  Refresh-disabled mutant is caught; no new defect identified.
- 0834: frame parser enforces decimal uint32, channel grammar, hex byte bounds,
  LF/blank-line rules, uniqueness and no partial output. Boundary/alias tests
  agree; oversized-payload mutant is realistic and caught.
- Repair 0545: reference fixes length error identity and validation precedence;
  tests cover ASCII rules, bounds and priority. Prompt says six exported error
  variables but source declares eight: clarity concern remains open.
- 0552: hierarchical routing, bitmask validation, descendant boundaries and
  independent nil-preserving payload copies align. Tests expose the realistic
  shallow-copy mutant. No new defect identified.
- 0360: zero-value catalog, first-duplicate removal, empty-category deletion,
  sorted nested copies and nil-receiver behavior agree. Tests check aliasing
  across repeated snapshots and duplicate removal; no new defect identified.
- 0392: strict single JSON value, wrapped source errors, validation and ordered
  artifact copies agree. Case-exact keys are not required here. Tests expose
  the sorting mutant without imposing an unrequested key-case policy.
- 0456: independent defaults, inclusive bounds, nil-receiver precedence and
  locked table access agree. Tests include concurrent access and maximum bound;
  rejecting the valid maximum is a realistic caught mutant.
- 0465: reread; existing first-batch disposition retained, not counted twice.
- 0500: locked contact CRUD, validation before ID allocation, phone grammar,
  immutable assigned IDs and sorted list behavior agree. Tests check concurrent
  uniqueness and replacement-ID handling; no new defect identified.
- 0504: fleet transitions, default selection, deep copies and ID-sorted list
  agree. Tests cover failed transitions without mutation, nil receivers,
  malformed JSON and opposite name/ID orders; sorting mutant is caught.
- 0523: Gregorian serial-day arithmetic is bounded and timezone-independent;
  tests cover leap centuries, invalid dates, direction and full supported span.
  Missing divisible-by-400 case is a realistic caught repair defect.
- 0190: strict interior slicing, reversed boundaries, duplicate validation and
  copied non-nil empty results agree. Tests cover aliasing and boundary inclusion
  mutant. Wording 'empty names' could include order elements; reference only
  rejects empty query names, so retain this clarity question rather than infer
  an unstated order-wide rejection rule.

- Repair 0025: stride-zero summation and nil/short/negative cases agree;
  wrong-start mutant is caught. Non-triviality concern: prompt directly names
  the literal to change in a single simple loop.
- 0034: progression formula, nonpositive count and independent storage agree;
  shifted-index mutant is caught. Non-triviality concern: literal formula repair.
- 0055: big-integer inclusive count avoids overflow and singleton division by
  zero; signed truncation and binary formatting agree. Tests include both int64
  extremes and full domain. Reference is correct but needlessly computes the
  full sum instead of dividing endpoint sum by two; compact formatting concern.
- 0056: copy before sort, original-endpoint parity and duplicate retention agree;
  tests cover negative parity and empty backing-array independence. Aliasing
  mutant is realistic and caught.
- 0097: XOR truth table, byte validation, preserved zeros and error results
  agree. Multibyte left input fails at its first non-ASCII leading byte before
  range iteration could skip bytes. Inverted truth-table mutant is caught;
  simple-task non-triviality concern remains.
- 0099: squared recurrence is correct within stated tested range through 1000;
  tests cover nonpositive inputs, recurrence and upper bound. Prompt does not
  explicitly cap inputs at 1000, so recursion/resource envelope is unclear.
  One multiplication repair is also a non-triviality concern.
- 0115: sorted added/removed/revision-or-value changes and no input mutation
  agree; tests catch same-revision value changes. Empty-key rejection is present
  in supplied source and tests but omitted from prose; note API clarity gap.
- 0125: rune filtering and palindrome test agree for empty/single/Unicode cases;
  inverted boolean mutant is caught. No new semantic defect identified.
- 0143: literal ASCII-space splitting and exact uppercase singleton agree;
  tests exercise trailing spaces, tabs and Unicode. Case-normalization mutant
  is caught. Non-triviality concern: remove one normalization call.
- 0245: ordered conjunction matching, wildcard semantics, complete validation
  and nil error result agree. Tests distinguish partial matches and catch OR
  mutant. No new semantic defect identified.
- 0259: message-first substring semantics, duplicates, single inclusion and
  fresh slices agree. Tests catch reversed operands and empty fragment behavior;
  low-complexity repair noted for non-triviality adjudication.
- 0269: validated ASCII segments and exact/descendant boundary rule agree;
  tests include repeated sealed segments, invalid paths and sibling prefixes.
  Raw-prefix mutant is realistic and caught.
- 0280: trimmed unique service names, port bounds, duplicate-port rejection
  and atomic nil-on-error result agree. Tests catch silent overwrite mutant.
- 0324: arbitrary-precision rune totals, first-batch ties and copied storage
  agree. Tests cover malformed UTF-8 and repeated strings; overflow correctness
  is statically supported by big.Int, not established by the modest-sized test.
- Java generation 0549: clear API/test conflict. Prompt says missing IDs cause
  IllegalArgumentException; get directly returns map.get and original tests
  explicitly demand null for missing IDs. Static hold: no new execution claimed.
  Otherwise immutable notebook snapshots, sorted mutable list copies and
  duplicate validation agree; title/ID comparator mutant is caught.

- Java 0619: defensive immutable relationship copies, unique positive IDs,
  relationship lookup and insertion order agree. Open contract issue: invalid
  values require IllegalArgumentException but null values produce NPE and tests
  insist on NPE. Unicode-whitespace titles are checked only with trim, so that
  unspecified whitespace envelope also needs adjudication. Missing-relationship
  mutant is realistically caught; no additional execution claimed.
- 0652: defaults, enum spelling, null-entry validation, range and map isolation
  agree. Tests require rejecting +3 although prose only says decimal integer
  syntax; exact accessor signatures also absent from prompt. API clarity hold
  for adjudication rather than assume Java parseInt grammar is intended.
- 0662: code-point Java whitespace normalization, ROOT casing and independent
  enum-order sets agree. Tests use Turkish locale with finally restoration and
  catch default-locale mutant. Tests prescribe NPE where prompt only says reject
  null: exception-type specification should be explicit.
- 0032: immutable products and newly sorted unmodifiable catalog lists agree;
  complete list validation catches null even after an earlier matching element.
  Missing-update insertion mutant is caught. Prose accidentally groups read
  under a List<Product> signature although behavior requires Product. Blank
  Unicode input policy is also unclear with trim-based implementation.
- 0080: static hold for configuration preservation conflict: prompt requires
  original configuration plus task.index, while reference trims every key/value
  and tests demand normalized dataset/prefix. Only schema strings/table names
  are explicitly declared trimmed. Return signatures/version semantics are
  also underspecified. Otherwise snapshots and map independence agree and
  aliasing mutant is caught. No execution added for this textual conflict.
- 0137: numeric boxed-ID comparison, position-preserving update and immutable
  insertion-order snapshots agree; tests expose reference-identity mutant.
  Constructor-versus-operation validation timing is not explicit. Tests use
  Integer.valueOf(1000) to provoke nonidentity, which relies on runtime cache
  configuration; this is not a newly observed intermittent result.

- Java 0170: ordinary paging, full-list null validation, exactly-once freezing
  and immutable result copies agree. Static overflow concern: from+pageSize
  can overflow for a large valid list's final page; original tests use five
  elements only. No huge-list execution claimed. Original-element mutant caught.
- 0185: duplicate validation precedes lookup, positive IDs, sorted immutable
  upsert and input preservation agree. Tests expose title-based matching mutant.
  Unicode nonblank policy remains underspecified relative to trim.
- 0253: ragged-row skip, full cell-null validation and immutable ordered result
  agree. Tests catch <= boundary mutant. Simple but combines full validation
  with selective extraction; no new semantic defect identified.
- 0268: finite lock-state transitions, invalid actions and fresh result lists
  agree. Tests cover renewal while unlocked and retained input independence;
  acquisition-via-renewal mutant caught. Nonempty result mutability tested even
  though only empty-result mutability is explicitly stated.
- 0270: fixed-size channel state, range checks, duplicate indices and copied
  update agree. Tests cover invalid lengths and aliasing mutant. Small task;
  non-triviality should be assessed with the other elementary examples.
- 0271: strict prefix maxima work at int extremes and preserve input; equality
  mutant is caught. Elementary scan, retained as non-triviality concern.
- 0294: copied media catalog, level bounds, persistent activation on missing
  selection and ordered immutable search results agree for tested inputs.
  Tests catch case-sensitive mutant. Unicode case-insensitive semantics are
  not defined beyond lowercasing and whitespace uses trim; no broad Unicode
  correctness claim from these ASCII-centered tests.
- 0305: inclusive relative cadence avoids int overflow using remaining distance;
  tests cover MAX_VALUE near-end ranges and endpoint mutant. Exception conflict:
  prompt says invalid values throw IAE, but null message produces NPE and tests
  demand NPE. Needs explicit contract adjudication.
- 0308: identity-based DFS, parent-first order, replacement without reordering,
  duplicate local rejection and immutable constructor copies agree. Tests catch
  remove/reinsert mutant and diamond handling. Cycle detection is present but
  ordinary immutable copied records cannot construct cycles; no cycle execution
  is evidenced by original tests. Deep recursive input envelope is unspecified.

- Java 0313: retained-prefix validation, cross-list ID uniqueness and immutable
  ordered concatenation agree. Tests catch inclusive-loop bound mutant and
  intentionally ignore incoming suffixes. 'Non-positive IDs' is ambiguous for
  authorId, which neither reference nor tests validate; reserve clarity concern.
- 0379: distinct mirror replacement and sorted snapshot agree; tests catch
  stale-entry mutant and input aliases. Tests additionally require no partial
  mirror mutation on invalid input, not explicit in prose. Mutable mirror is
  an implied operational requirement, not a guarantee for unmodifiable sets.
- 0384: exact field count, trimmed fields, boolean spelling, integer bounds and
  description agree. Invalid-flag mutant is caught. Base-10 grammar is not
  explicitly ASCII-only; do not declare Java parseInt's signed/Unicode input a
  defect without that rule. StringBuilder test does not establish extra alias
  safety beyond immutable String input.
- 0393: floor-modulo slots, per-call computation count and defensive arrays
  agree. Tests cover repeated slots, negative values, empty and getter copies;
  remainder mutant caught. Small simulation, no new semantic defect identified.
- 0394: signed token parse, separate exact sums and canonical rendering agree.
  Tests cover malformed tokens, numeric parse bounds and arithmetic overflow.
  Rendering-one mutant is caught; overflow during parsing is expressly treated
  as invalid integer in tests, unlike sum overflow.
- 0395: odd/even center expansion and strict improvement preserve earliest
  longest window; arrays are copied. Tests cover ties, singleton aliasing and
  even windows; replacing-on-tie mutant caught. Quadratic worst case has no
  specified performance bound, so no unsupported performance rejection.
- 0406: exact command matching, stack underflow, checked addition and bounded
  nondestructive emission agree. Tests catch pop-on-emit and overflow. Numeric
  grammar is base-10 int, not explicitly ASCII-only; whitespace rejected by
  parsing or exact command checks. No new semantic defect identified.
- 0426: doubly linked endpoints, ownership/removal guards, cleared links and
  size accounting agree. Tests cover middle/end/singleton removal and equality
  search; missing size decrement mutant caught. getIndex return type is implicit
  rather than fully declared in prompt, a minor API clarity question.
- 0434: exact simulated-time threshold, checked addition, non-HOME no-op and
  button state changes agree. Tests catch > versus >= boundary. Public records
  permit unusual HOME/finished combinations whose treatment is unspecified;
  ordinary reachable states and explicit overflow case are covered.

- Java 0458: complete null validation, ordered set difference and immutable
  snapshots agree. Tests cover empty names, duplicates, case and input changes;
  inverted membership mutant caught. No new semantic defect identified.
- 0514: confirmed reference bug: allVisible([false, null]) returns false before
  validating the malformed suffix. Isolated pinned Java probe compiled then
  failed normally (exit codes 0,1; no timeout; 2,951 ms). Original tests cover
  [true,null] but not false-before-null. Original/reference/diagnostic tasks are
  preserved in `visibility-null-result.json`. Tests also unnecessarily insist
  immutable card lists have distinct identities on close; sharing immutable
  lists would not alias mutable caller data as prohibited by the prompt.
- 0564: async success snapshots, duplicates, null futures/results and ordinary
  runtime failures agree; aliasing-view mutant caught. 'If invocation throws'
  is broader than RuntimeException-only catch (Error escapes), and blank-key
  semantics use trim. Retain those contract edges for adjudication.
- 0636: factory calls provider once, preserves runtime error identity and
  delegates to the same panel; tests cover shared and separate panels. Wrong
  hide delegate mutant caught. Initial hidden state tested but not explicit in
  prompt; idempotence for arbitrary Panel subclasses is not guaranteed by API.
- 0680: first-ID order with last-value wins, null arrays and newly constructed
  output contacts agree. Tests catch putIfAbsent mutant and object reuse.
  Negative ID rejection timing is implicit at merge rather than constructor.
- 0689: immutable fields, inheritance, trimmed constructor values and ordered
  string snapshots agree. Tests catch wrong workshop getter. Blank Unicode
  envelope uses trim; boilerplate-heavy task noted for non-triviality review.
- 0737: exact header precedence, no fallback after usable unknown credential,
  path-limited query lookup and complete null validation agree. Tests expose
  unscoped-query mutant; Unicode nonblank envelope is trim-based and unclear.
- 0738: alias-first resolution, input order, validation even for all-results
  and defensive immutable list agree for tested inputs. Reference additionally
  trims alias values while prompt only explicitly trims user and constructor
  fields; whitespace-bearing alias values require contract adjudication.
- 0739: sorted kind indexes, stored immutable artifacts and atomic duplicate
  rejection agree. Tests cover untrimmed IDs, snapshot persistence and nulls;
  overwrite mutant caught. No new semantic defect identified.

- Java 0782: normalized value keys, capability-specific revoke, checked missing
  exception and independent tables agree. Tests catch clear-all revoke mutant.
  Internal empty-entry cleanup is statically present but not directly asserted.
- 0794: confirmed final-pass defect. For [1,2], reference records only the swap
  pass, omitting required final no-swap pass. Isolated pinned Java probe compiled
  and failed normally (exit codes 0,1; no timeout; 3,598 ms), preserved in
  `sort-final-pass-result.json`. Original test's trace stops early only on an
  input where no-swap occurs before the fixed loop runs out; reverse/extreme
  case checks only at least one pass. Array defenses otherwise agree.
- Repair 0140: ROOT-folded content comparison plus complete null validation
  agree. Tests explicitly cover a match before a null suffix, unlike held 0514.
  Identity-comparison mutant is caught. This one follow-up does not clear all
  early-return validators in the corpus.
- 0014: conjunction and inclusive bounds agree; tests cover both one-condition
  false cases. Non-triviality concern: single elementary boolean operator repair.
- 0030: exact Long.parseLong grammar, skipped malformed/null tokens and wrapping
  arithmetic agree. Boundary and over-int-range tests catch narrowed parser
  mutant. No new semantic defect identified.
- 0041: parsed text preservation, immutable cached lists and putIfAbsent agree;
  tests catch mutable-cache exposure. Whitespace means trim in supplied source;
  no separate concurrency execution or unbounded-cache claim is made.
- 0058: snapshot key sorting and corrected exclusive bound agree. Tests catch
  size-equal index exception mismatch. 'Mutations ... computation already in
  progress' overpromises for concurrent mutation during Map.copyOf of an
  arbitrary mutable map; clarification needed, not a demonstrated race run.
- 0068: exact-revision hit preserves cached null and avoids writes; stale/null
  entries replaced, unrelated entries preserved and invalid calls atomic.
  Tests use unmodifiable hit map and catch stale-entry reuse mutant.
- 0130: bounded radix and signed lowercase representation agree; tests catch
  shifted radix at boundaries. Non-triviality concern: direct library wrapper
  with a single argument correction.
- 0147: code-point count and offset preserve surrogate pairs and zero/large
  limits; tests catch UTF-16 unit slicing. No new semantic defect identified.

Next frozen index: 100. Keep findings open until probes and criterion-specific
dispositions are recorded; do not replace the original sample or v1 corpus.
