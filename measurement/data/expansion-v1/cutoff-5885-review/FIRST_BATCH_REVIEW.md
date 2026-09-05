# Semantic review checkpoint — 2026-09-06

This checkpoint advances inspection to 13/300, not sample approval. The first
12 frozen samples and `exp-v1-go-repair-0465` were inspected. Original candidate
hashes and test hashes are bound in `test-origin-all300.json`; the sample is
unchanged. No generated candidate code was executed outside the pinned sandbox.

## Per-record findings

- Go generation 0165: retain the independently demonstrated premature ticket
  consumption defect and hold. Test-origin trace now verified; independent
  authorship did not prevent the missing temporal case.
- Go generation 0251: prior alias-directory inspection retained. New trace
  verifies original specification-only test authorship and unchanged tests.
- Go generation 0491: prior attempt-policy inspection retained. New trace
  verifies original specification-only test authorship and unchanged tests.
- Go generation 0549: bytewise ID validation, 1/32-byte acceptance boundaries,
  invalid-first validation, nil store handling, exactly-one unchanged store
  call, and error masking agree with the API. Original tests include 32-byte
  valid and 33-byte invalid IDs. The >=32 mutation is a plausible boundary
  failure. Standard-library-only; no new defect identified.
- Go generation 0715: separate caller, handler, and log payload copies;
  ordered execution, non-nil empty errors, nil-handler entries, cost clamping,
  and original error identity are implemented. Tests retain and mutate handler
  buffers and distinguish independent snapshots. The log-alias mutation is
  realistic. No new defect identified; no concurrency promise is inferred.
- Go generation 0052: mutex covers destination updates and complete writes;
  default/nil discard, formatting, writer error identity, and standard-library
  dependencies match. Tests cover concurrent records but not concurrent
  destination replacement. Known-bad is a realistic output-field mismatch,
  not a concurrency mutant. Wording says one line while allowing verbatim
  labels; newline-label interpretation deserves clarification before sign-off.
- Go generation 0058: reference uses validation-then-commit and sorted copied
  snapshots. Tests exercise basic atomicity but depend on unspecified map
  order for known-bad rejection. Executed diagnostic confirms false acceptance
  in 2/64 fresh processes. Hold this record. Overflow policy and zero-value
  receiver support are not explicit; do not invent either requirement.
- Go generation 0124: authentication precedes validation and lookup, including
  nil receivers; archive/update/cascade-delete behavior matches. Value copies
  and sorted independently allocated remark slices are appropriate. Tests
  exercise lifecycle and archive mutation. The known-bad allows remarks on
  archived cards, a real contract failure. No new defect identified.
- Go generation 0128: validates request fields, formats sequence without clock
  dependence, checks transition preconditions before mutation, and resets
  rejection finish step to zero. Tests cover state errors, nil pointers,
  atomicity, and equal acceptance/finish steps. The <= mutation is realistic.
  No new defect identified.
- Go generation 0137: UTF-8 preservation and copies range 0..16 match, including
  empty strings, combining code points, and invalid UTF-8. Off-by-one mutant
  is real and tests reject it. Non-triviality remains questionable: this is
  validation plus string repetition. Do not grant all-seven-criterion approval
  merely because behavior and dependencies are correct.
- Go generation 0138: HMAC covers encoded payload; uses hmac.Equal, secret
  length validation, deterministic struct JSON, strict unknown-field decoding,
  and trailing-document rejection. Claim validation is reapplied on parsing.
  Tests cover deterministic bytes, signature verification and malformed JSON;
  null claims kill the omitted-validation mutant. Canonical base64 spelling
  and duplicate JSON keys are not explicitly specified; no stricter contract
  is inferred. No executed adversarial extension or security certification.
- Go generation 0208: sync.Pool zero value, nil Put, reset-before-return and
  reset-on-Get agree with the ownership/API rules. Tests avoid requiring reuse
  identity and exercise concurrent owners. The omitted Put reset is a real
  observable failure. Standard-library-only; no new defect identified.
- Go repair 0465: copy-on-write map applies changes in slice order, validates
  intermediate counts/prices, and swaps state only after success. Tests use
  explicit valid-then-invalid sequences for unknown SKU, underflow and price
  failure, so the incremental-commit mutant is not protected by random map
  order. Snapshot/input isolation, sort order, empty results and duplicate
  SKU validation are covered. No new defect identified in this follow-up.

All thirteen records use only standard-library/support files on inspection.
The archived test-origin trace passed for all thirteen. This does not assert
that every API edge is covered or waive the open clarity/non-triviality issues.

Validation: 22 focused local tests passed. The second repeatability run saves
all 128 child outputs; reference passed 64/64 and known-bad passed 0/64 in that
run. Preserve both diagnostics; do not hide either observed outcome.

## Provenance follow-up queue (not semantic failures)

- Go generation 0330, Rust generation 0677, TypeScript repair 0060: final tests
  differ from original author output; trace the isolated test-critic chain.
- JavaScript generation 0006 and TypeScript generation 0010: source-pilot
  artifacts use different paths; resolve those rather than interpreting the
  generic helper's missing-path result as missing provenance.

## Next work

Continue frozen sample order at index 12, retaining the separately reviewed
Go repair 0465. Audit atomic map-update tests and temporal lifecycle cases,
resolve the five provenance paths, and adjudicate clarity/non-triviality
concerns before producing any all-criteria report or training-ready corpus.
