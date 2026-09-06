# Array-pattern follow-up, batch 2

2026-09-06. Fifteen further outside-sample contract/reference/test inspections:
not-in-sample array-hit positions 16–30 in immutable v1 inventory order.
Forty outside-sample targeted inspections now accompany the unchanged frozen
300. No full seven-criterion approval or unbiased failure-rate claim.

## Reproduced holds

All failures below were executed in the unchanged pinned sandbox with no
timeout. JS failures exited `[1]`; TS failures compiled then exited `[0,0,1]`.

| ID suffix | Finding | Result file | ms |
| --- | --- | --- | ---: |
| typescript-generation-0015 | sparse identifier array passes validation and enters allow-list | allowlist-sparse-probe-result.json | 4849 |
| javascript-generation-0015 | sparse showcase cards bypass constructor validation | showcase-sparse-result.json | 476 |
| javascript-generation-0016 | sparse lookup tags are accepted and frozen instead of rejected | lookup-tags-sparse-result.json | 813 |
| javascript-repair-0011 | sparse segments silently join to empty string | segments-sparse-result.json | 774 |
| javascript-generation-0017 | finite 1e308 rounds via Infinity to MAX_VALUE instead of remaining 1e308 | dial-finite-rounding-result.json | 765 |
| typescript-generation-0022 | valid parameter named __proto__ is lost by assignment into ordinary object | path-parameter-key-result.json | 6513 |
| typescript-generation-0023 | sparse TagValue array serializes null instead of rejecting | encoded-tags-sparse-result.json | 6681 |
| typescript-repair-0014 | finite dimensions overflow their sum: endExclusive 10 instead of 2 | window-finite-sum-result.json | 6513 |
| javascript-generation-0022 | sparse ready sessions silently render empty string | sessions-sparse-result.json | 1221 |

The two numeric probes use accepted finite values without loops or private
state manipulation. DecimalDial's input is already an integer and lies inside
the bounds; multiplying by the decimal factor overflows. visibleWindow's
rowHeight, scrollTop and viewportHeight are the same finite integer MAX_VALUE;
the viewport covers exactly row 1, but intermediate addition overflows before
division. Their original tests cover small ordinary values only. The path
probe uses the contract's unrestricted nonempty parameter name and checks an
own property explicitly; it does not execute injected code or pollute the host.

AllowListPolicy's `active: any` getter also weakens type information unnecessarily.
Its original assert function narrows getter comparisons across calls; further
provenance review is needed before describing this as test accommodation. The
hold here is based on the executed sparse-validation defect, not that inference.

## Scoped negative findings and cautions

- JavaScript repair-0008 MetricIndex: every skips holes, but subsequent for-of
  copy dereferences each element and throws TypeError on a hole. Successful
  construction builds dense groups; query map is safe. Extra own enumerable
  key validation matches the original test. No sparse acceptance inferred.
- TypeScript repair-0009 applyPulse: explicit for-of validation catches holes
  before mapping. Retaining order by removing sort matches the stated repair.
- TypeScript generation-0018 MentorDirectory: for-of validates and copies into
  fresh dense storage. Safe-integer greatest-ID overflow is guarded, and patch
  validation precedes missing-ID handling. Query-ID validation scope remains
  ambiguous; no array-pattern hold inferred.
- JavaScript generation-0013 selectParcelsByZone: the contract requires ignoring
  malformed records and retaining original matching identities. A sparse array
  with one matching parcel correctly returns that same parcel. Executed
  `parcels-sparse-control-result.json` passed `[0]`, no timeout, 990 ms.
- JavaScript generation-0014 membership registry: constructor's for-of over
  mapped copies rejects holes; normal constructor/command paths stay dense.
  Missing-key edit versus malformed change validation precedence is ambiguous,
  and extra-field shallow copies are expressly allowed. No new hold here.
- TypeScript generation-0019 renderIndicator: filter uses a literal dense
  four-element array, and Unicode Array.from produces dense code points.
  Null optional-value defaulting versus runtime unsupported-tone wording is a
  separate scope question; no sparse defect inferred.

Nine new holds bring the total to **69 additive / 72 with historical three**.
These records are not regenerated or silently patched. Next array hit is
`exp-v1-javascript-repair-0015`. Numeric and parameter-object findings also
require systematic-scope follow-up; v1's 11-stratum scope is only a minimum.
