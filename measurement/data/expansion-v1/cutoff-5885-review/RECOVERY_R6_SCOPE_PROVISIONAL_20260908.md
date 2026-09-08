# Provisional r6 Python/Rust generation scope — 2026-09-08

**Provisional only: 11 generation parents (7 Python,4 Rust).** These are exactly the generation subset of RECOVERY_TRANCHE_PYTHON_RUST_20_20260908.md. No new original review sweep, version reservation, plan materialization, teacher call, execution or cloud action occurred. Main must validate/integrate before any launch; the r6 names are proposed identities, not reserved artifacts. All repairs are excluded.

Three requests are explicit contract-clarifications: Python0314, Python0319 and Rust0704. The remaining eight are reference-fix requests preserving prompt bytes. Corrected independent tests are required for all; this is not permission to reuse conflicting parent tests. Original holds stay intact, and no original unique-coverage increment or admission is claimed.

## Exact proposed requests

### exp-v1-python-generation-0355

Proposed derived ID: exp-v1-recovery-r6-python-generation-0355. Change class: reference-fix.

Keep the specification byte-for-byte unchanged. Remove only the unstated string-only restriction on batch mapping keys; retain hashable keys as supplied, without stringification. Keep record names nonempty strings, buffer one-byte validation, four descriptor semantics, one-shot materialization, first scheme order and duplicate-record position. Independent tests must exercise integer and tuple batch keys, one-shot records under several schemes, partial blocks and payload isolation. Test outputs by required contents/order; do not require unpromised input Mapping concrete types.

### exp-v1-python-generation-0445

Proposed derived ID: exp-v1-recovery-r6-python-generation-0445. Change class: reference-fix.

Keep the specification unchanged. Snapshot selected outer notice Mapping contents before deepcopy so standard MappingProxyType with ordinary nested dict/list values works. Preserve authentication-first, all-row validation, filter/duplicate order and deep independence. Independent tests must use a matching read-only notice/principal, validate actual malformed scalar fields without extra list wrappers, and exercise nested ownership. Do not assert concrete copied mapping type, restrict notices to dict, change filter domains, or import an exception policy for arbitrary noncopyable opaque objects.

### exp-v1-python-generation-0298

Proposed derived ID: exp-v1-recovery-r6-python-generation-0298. Change class: reference-fix.

Keep the specification unchanged. Validate finite ints without conversion to float; reject bool and nonfinite float as before. Preserve rank values, casefold substring/fuzzy matching, category/enabled filtering, ranking tie breaks and pagination. Test rank10**500 and adjacent integer ranks with deterministic title/ID ties, ordinary floats, nonfinite/bool rejection and snapshots. No finite-float output or rank cap is permitted; no global conversion-limit mutation.

### exp-v1-python-generation-0314

Proposed derived ID: exp-v1-recovery-r6-python-generation-0314. Change class: contract-clarification.

Explicit derived numeric policy: supported built-in int/float values exclude bool; all ints are finite without float coercion and floats must be finite. adjusted uses ordinary Python addition on supplied values, retaining arbitrary-precision all-int results. A mixed int/float addition whose integer conversion is outside float range raises OverflowError; finite float additions may produce native infinity, since input finiteness is not an output-finiteness guarantee. Do not cap valid integers or silently cast every value to float. Freeze this policy in the derived problem. Preserve composite-key uniqueness, full validation including unmatched corrections, exact output schema/order and copied tags. Tests: no-correction10**500, cancelling huge integer correction, ordinary float addition, explicit mixed OverflowError, unmatched invalid correction, duplicate keys and tag isolation. On any error caller inputs remain unchanged; no partial result is returned. No unrelated Mapping protocol narrowing.

### exp-v1-python-generation-0319

Proposed derived ID: exp-v1-recovery-r6-python-generation-0319. Change class: contract-clarification.

Explicit derived numeric policy: coordinates and limit accept built-in int/float excluding bool, all ints are finite without coercion, floats must be finite; speed remains positive non-bool int. Validate fire coordinates and advance limit before active/inactive shortcuts as existing behavior. Active advance computes y+speed using native Python numeric semantics; all-int movement remains arbitrary precision. If mixed float/int addition raises OverflowError, propagate it before changing x,y,speed,active. A native floating result of infinity is not a new invalid input: compare it to finite limit normally and deactivate if >=limit. Freeze these distinctions and bool-limit rejection in the derived problem rather than silently narrowing coordinates/speed. Preserve active-fire no-op, reusability and detached snapshot. Tests: huge integer x/y/speed/limit on bounded calls, exact boundary, refire, active invalid fire validation, bool/nonfinite rejection and atomic mixed-overflow advance. Do not mutate public fields into unspecified malformed states for tests.

### exp-v1-python-generation-0269

Proposed derived ID: exp-v1-recovery-r6-python-generation-0269. Change class: reference-fix.

Keep specification unchanged. Avoid float coercion when checking finite exact integral/rational Real values; preserve finite ordinary float behavior and bool rejection. Comparisons, not float output, determine buckets. Test integer threshold/value10**500 and neighbors, standard Fraction controls, threshold iteration and entry order, MappingProxy inputs, duplicate/hashable IDs, malformed metric schemas and fresh nested containers. Do not add a numeric range cap or require concrete Mapping wrappers; standard numeric values suffice, no hostile custom Real implementation.

### exp-v1-python-generation-0672

Proposed derived ID: exp-v1-recovery-r6-python-generation-0672. Change class: reference-fix.

Keep specification unchanged. Enforce the declared attributes dict[str,object] key types before deepcopy; non-string attribute keys raise TypeError. Empty string attribute keys remain valid because no key nonempty rule exists. Preserve frozen dataclass defaults, whitespace normalization of title/curator/tags, normalized duplicate rejection, tag order, exact outer key order and nested copy independence. Test integer attribute key, valid empty/string keys, nested ordinary contents, frozen fields and blank versus type errors. Do not infer blank attribute-key rejection or concrete subclass preservation.

### exp-v1-rust-generation-0558

Proposed derived ID: exp-v1-recovery-r6-rust-generation-0558. Change class: reference-fix.

Keep specification unchanged. Trim Zone lookup names and reject an empty result with Reply::Invalid before lookup, matching global malformed-name rules. Unicode whitespace follows Rust str::trim consistently with other names; nonblank missing names still return NotFound. Preserve linked zone/tool indexes, insertion-ordered zone replies, sorted Summary, cascade removal and command failure atomicity. Tests must distinguish blank Zone from nonblank absent Zone using a valid workshop built through commands, include Unicode blank and normal trimmed lookup, and retain cascade/insertion tests. No policy for manually inconsistent public maps is invented.

### exp-v1-rust-generation-0778

Proposed derived ID: exp-v1-recovery-r6-rust-generation-0778. Change class: reference-fix.

Keep specification unchanged. Trim ASCII whitespace around each bracketed record and the empty interior rather than literal spaces only; retain ASCII-only outer trimming. Replace conflicting parent trailing-tab rejection in independently generated tests. Test tabs/newlines/CR around bracketed records and empty brackets, reject internal key/value whitespace, preserve Lines CR/blank rejection, percent syntax and UTF-8 error distinction, duplicates and uppercase canonical output. No Unicode-whitespace widening or trimming inside encoded values; no copied original oracle that contradicts prose.

### exp-v1-rust-generation-0757

Proposed derived ID: exp-v1-recovery-r6-rust-generation-0757. Change class: reference-fix.

Keep specification unchanged. Validate every kind in input order before checked u128 summation so a later first mismatch takes priority over earlier possible sum overflow. Test MAX and1 matching then a wrong kind returns UnexpectedKind with exact fields; all matching MAX+1 returns Overflow; exact MAX and empty input/kind remain valid. Preserve borrowed input and owned returned kind. Tests match declared variants/fields without requiring unpromised derives. Whole-target validation precedence plus checked arithmetic is the substantive mechanism.

### exp-v1-rust-generation-0704

Proposed derived ID: exp-v1-recovery-r6-rust-generation-0704. Change class: contract-clarification.

Explicit derived allocation/error policy: after required argument/tile validation, compute grid rows by quotient plus nonzero remainder (avoiding an unnecessary ceil-add overflow), checked dimensions and byte length. Return existing AtlasError::Overflow for checked arithmetic overflow, output byte lengths exceeding Vec<u8> representable capacity (isize::MAX), or fallible output buffer reservation failure; never deliberately attempt such impossible allocation and never claim all memory exhaustion succeeds. Freeze allocation failure mapping in the derived prompt. Preserve zero-columns-before-tile validation, lowest invalid tile index, per-tile pixel-length/dimension checks, row-major placement and zero-filled unused cells. Zero-area output remains valid whenever dimensions themselves are representable. Use fallible reserve before zero fill. Tests: one1x1 tile with usize::MAX columns returns Overflow in bounded resources, zero-area and arithmetic-overflow controls, ordinary non-square/partial-row atlas and nonmutation. No huge feasible allocation, allocator exhaustion, or platform-agnostic capacity constant assumption in tests; use pinned runtime limits.

## Policy and integrity boundary

Python0314/0319 explicitly distinguish finite accepted inputs from native mixed-arithmetic representability; valid huge integers are not capped. Their proposed OverflowError/native-infinity choices are new derived wording requiring main acceptance, not retroactive claims about the original contract. Rust0704 explicitly maps fallible allocation failure to the existing Overflow variant; this is not a promise to allocate arbitrary memory. Blank-name policy in Rust0558 follows its existing trim contract; bracketed whitespace in Rust0778 remains ASCII-only.

The companion request JSON uses the existing planner's version/parent_corpus_sha256/hold_ledger_sha256/selections schema, with extra provisional and per-selection hold/source evidence bindings. Its review_evidence points to this note and hashes its bytes. Each parent canonical hash, exact current hold entry hash, hold evidence path/hash and original source/rights data are recorded from the current files. A ledger change invalidates the pinned request hash and requires main revalidation; do not automatically refresh it and launch. The JSON is not itself an admission seal or a generated plan.

Preserve the source commit/revision, source record IDs/hashes, rights and immutable lineage through actual planning. Fresh independent tests must receive only the derived ID/specification, with specification-grounded feedback if the bounded policy permits; do not pass reference or mutant source to the test author. Require a realistic discriminating witness for every held defect and a correct reference pass, not merely any mutant failure. Main retains all later execution/evaluation-separation/sufficiency and final admission responsibilities.

