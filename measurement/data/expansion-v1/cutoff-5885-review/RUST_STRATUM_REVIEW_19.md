# Rust generation review, batch 19

Positions 271–285 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections. Four new static holds. Total 834
unique outside-sample inspections; 421 additive plus historical three = 424 holds.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 271 | 0318 | Exact const signal mapping, signed i8 formatting and copy/comparison traits. No new hold; elementary task nontriviality pending. |
| 272 | 0321 | Static hold: tests construct Catalog as a unit value although prompt does not specify its shape or constructor. |
| 273 | 0322 | ASCII digit validation, reverse parity and checksum match for bounded inputs. u32 sum over unrestricted-length input has an unresolved large-input envelope; not runtime-probed or counted as a new hold. |
| 274 | 0323 | Static hold: typed method signatures and initially enabled credentials required by original tests are absent from prompt. |
| 275 | 0324 | Endpoint preservation, status boundaries, both markers and Unicode scalar length agree. ModuleInfo signatures/description content are underspecified, but original tests do not constrain description content or its return type. No new hold. |
| 276 | 0319 | Static hold: Journal method parameter/return types required by original tests are not declared. |
| 277 | 0320 | Static hold: original tests require exact addition and non-binding line formatting omitted from prompt. |
| 278 | 0325 | Exact descriptor API; first equals split, duplicate/unknown/empty-field rejection and nonmutation. Error strings not specified or asserted. No new hold. |
| 279 | 0326 | Exact endpoint API, permitted character sets/dot rules, ordered unique inserts and atomic errors/removal. No new hold. |
| 280 | 0327 | Exact tuple formatting and first-three joining including empties; debug formatting escapes embedded newlines. No new hold; elementary task scope pending. |
| 281 | 0329 | Checked endpoints, alignment, sorted virtual nonoverlap, allowed physical overlap and half-open translation. No new hold. |
| 282 | 0330 | Exact navigator API, atomic invalid selection, stable page IDs and ordered round trip restoration. No new hold. |
| 283 | 0332 | CRUD behavior and original tests agree. Prompt ordering phrase for missing-ID plus invalid-time replace is ambiguous: reference validates time before lookup. Combined case untested; retained for adjudication, no new hold. |
| 284 | 0333 | Duplicate-before-existence precedence, successful-attempt count and unique solved-exercise weights agree. At most 2^32 distinct u32 exercise IDs, each weight at most 2^32-1, so summed weights fit u64. No new hold. |
| 285 | 0334 | Exact builder API, lexical assignment replacement, ordered filters, identifier validation and specified literal/null formatting. No new hold; not a database execution or production SQL-safety certification. |

## Static contract/test evidence

- **0321:** Prompt says to implement ActionCatalog for Catalog, without declaring
  Catalog's representation or any constructor. Original tests directly invoke
  `Catalog.prepare_actions(&plans)`, requiring a publicly constructible unit
  value. A normal struct with private fields and a constructor would not meet
  those hidden test requirements. Exact command URI punctuation is also left
  implicit; the hold does not depend on resolving that separate question.
- **0323:** Prompt lists method names and argument names but not ownership/types
  or return signatures. Tests require `insert` accepting owned String/Vec<u8>,
  `list` yielding indexable Credential values, and export returning Result with
  Vec<u8>/String. The last test asserts a newly inserted untouched credential is
  enabled, although the prompt never specifies the initial enabled state.
  Password-hash collisions are not claimed as a reproduced defect.
- **0319:** Prompt gives names new/new_record/add_record/validate_record without
  their signatures. Tests require new_record(epoch, owned Token, work) returning
  Result<Record, String>, validate_record(&Record) supporting is_err, and
  add_record consuming Record. These are hidden interface obligations, not an
  executed reference failure. Publicly malformed journal histories are not
  adjudicated here.
- **0320:** Prompt specifies subtraction rendering but not Add rendering; the
  original exact-string test requires parenthesized addition. Only bindings are
  expressly required to end in a newline, yet invocation-only tests require
  `run_0()\n`. Step fields are named without types. Hold for incomplete exact
  output/interface contract, not an executed rendering failure.

Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
No new sandbox execution. No-hold is not seven-criterion admission; scope v6,
frozen sample, historical partition and original VM evidence remain unchanged.
Continue position 286. No new VM or training seal.
