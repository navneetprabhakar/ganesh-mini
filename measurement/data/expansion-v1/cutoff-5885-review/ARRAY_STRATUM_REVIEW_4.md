# Array-pattern follow-up, batch 4

2026-09-06. Array-hit positions 46–60 outside the frozen sample are inspected
for contract/reference/original-test consistency: **15 new / 69 unique outside-
sample targeted inspections**. The frozen 300 remain unchanged. Nine diagnostic
failures on seven records, all in pinned sandboxes with no timeout. JS results
exit `[1]`; TS results compile then exit `[0,0,1]`.

| ID suffix | Finding | Result file | ms |
| --- | --- | --- | ---: |
| javascript-repair-0024 | sparse keywords bypass required validation | keywords-sparse-result.json | 346 |
| javascript-repair-0024 | lowercasing expands İ and shifts later ASCII match offsets | keywords-unicode-offset-result.json | 355 |
| typescript-generation-0031 | markers 2^32 are accepted as zero bits despite required 0–31 bound | tile-high-bits-result.json | 2168 |
| typescript-generation-0032 | sparse navigation entries bypass field validation | navigation-sparse-result.json | 2565 |
| typescript-generation-0034 | overflowing finite day difference yields NaN and accepts positive advance for zero-rate stay | stay-zero-rate-overflow-result.json | 2749 |
| javascript-generation-0041 | sparse required topics produce successful workshop payload | workshop-request-sparse-result.json | 446 |
| javascript-repair-0026 | sparse 3D point accepted instead of TypeError | beam-sparse-result.json | 445 |
| javascript-repair-0026 | large finite point on cone axis incorrectly excluded after cross-product overflow | beam-finite-collinear-result.json | 338 |
| javascript-generation-0044 | sparse selected station list bypasses string validation | stations-sparse-result.json | 394 |

The Unicode diagnostic only asks to match ASCII `x` after an unmatched `İ`;
it does not depend on a disputed case-folding equivalence for the first letter.
The cone point equals its target, has finite distance below range, and should
lie on the zero-angle axis. Its cross products become Infinity-Infinity/NaN.
The quote probe asserts the zero-rate business constraint, not representability
of a gigantic nights field. Bitwise coercion must not replace an explicit upper
bound. Original tests omit these inputs. Seven new holds bring totals to
**82 additive / 85 including historical three**.

## Scoped negative findings and remaining questions

- JS generation0035 squareFiniteNumbers: filter intentionally ignores malformed
  values, so skipping holes is valid. Its original test explicitly expects
  Infinity when MAX_VALUE is squared; unlike the held zero-volume and bounded
  rounding cases, no representable finite result is lost here. No overflow hold.
- JS generation0036 SelectionTray: for-of validates input, snapshots map private
  dense storage, exact normalized selection IDs and defensive copies agree with
  ordinary tests. No sparse acceptance found.
- JS repair0023 prioritizeJobs: for-of validation precedes stable filter/map.
  Malformed holes throw before filtering. The repair reverses concatenation
  order; non-triviality remains a separate judgment.
- TS repair0024 assignBehaviors: both input collections are for-of validated;
  final map and grouped push-built arrays are dense. Label nonblank validation
  is inherited from the provided source; no new sparse hold inferred.
- JS repair0025 readPath: split produces dense segments. Object wrapping allows
  normal primitive property traversal and inherited properties; final falsy/null
  behavior matches original tests. No sparse issue.
- JS generation0038 buildPaletteModel: indexed validation explicitly catches
  holes, including an original `new Array(1)` test. Duplicate selection is first
  occurrence only, as required. This is a static negative control supported by
  the archived original passing campaign, not a newly executed probe.
- TS generation0042 expandRows: no malformed-values validation is specified;
  NaN/infinities are expressly accepted. Sparse rejection is not invented.
  Safe-integer column counts exceed JavaScript array capacity; retain this
  infeasible output-size envelope for API clarity rather than allocating it.
- TS repair0027 findFreeCalendars: for-of validates all intervals before filter,
  preventing malformed numeric ranges from hiding in excluded calendars. Null/
  hole interval error type remains an unresolved boundary; no acceptance hold.

Continue at array-hit position 61 (resolve its ID from the immutable inventory).
No full seven-criterion approvals or unbiased failure-rate claims. No candidates
rewritten, generation restarted, training seal issued, or VM created.
