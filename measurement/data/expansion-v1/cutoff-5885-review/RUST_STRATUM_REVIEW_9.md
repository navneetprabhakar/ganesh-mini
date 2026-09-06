# Rust generation review, batch 9

Positions 121–135 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections. Four new holds. Total 684 unique
outside-sample inspections, 398 additive plus historical three = 401 holds.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 121 | 0144 | Exact API, scalar-value reversal per run and unchanged Unicode whitespace. No new hold. |
| 122 | 0139 | Explicit API, full required-key validation and decimal port range. Additional equals in values is underspecified; tests require rejection. No new hold. |
| 123 | 0140 | Named public methods but incomplete parameter/return signatures; tests choose owned marker strings and Result returns. API self-containment remains unresolved, not approved. Internal submitted-and-signaled phase versus prose idle wording not forced into a runtime failure. No new hold. |
| 124 | 0141 | Hold: valid transfer restoring exact maximum supply is rejected as overflow; original test endorses that error. Method signatures also partly implicit. |
| 125 | 0142 | Hold: explicit special case for a tested path returns incorrect axial destination. Original test endorses the wrong answer. |
| 126 | 0143 | Named methods with partly implicit argument/return types; self-containment unresolved. Ordinary state consumption and migration logic follows prose. Private counter exhaustion not executed. No new hold. |
| 127 | 0145 | Exact API, checked arithmetic, variable instruction arity and first-halt behavior. No new hold. |
| 128 | 0146 | Exact API, unsigned_abs handles i32::MIN. Small formatting task; nontriviality unresolved. No new hold. |
| 129 | 0147 | Exact API, requested-ID duplicate check and owned unique result. Small lookup task; nontriviality unresolved. No new hold. |
| 130 | 0148 | Exact API, balanced contiguous partitions and ordered joins. Early error detaches remaining owned-input workers; no retained input references. Spawn/resource-limit behavior not separately adjudicated. No new hold. |
| 131 | 0150 | Explicit API, exact segment checks and single suffix removal. Multiple-error precedence in locators is not separately adjudicated. No new hold. |
| 132 | 0151 | Hold: first ASCII letter after leading digits is not capitalized. Zero-count/combination-limit precedence remains an additional unresolved envelope, not counted. |
| 133 | 0152 | Typed ticket API, complete 18-byte groups, exact alphabet/length and output-prefix lifetime. Associated versus free constructors inferred from method grouping; self-containment not fully signed off. No new hold. |
| 134 | 0154 | Hold: EnvelopeDecoder lacks the equality traits required for all public types. |
| 135 | 0155 | Exact API and enum-to-string mapping, owned output and literal empty fields. Small formatting task; nontriviality unresolved. No new hold. |

Executed evidence in the pinned network-disabled/resource-limited Rust sandbox,
all without timeouts:

- 0141 `ledger-maximum-balance-result.json`, [0,101], 1725 ms: supply MAX,
  transfer one out then one back. Required Ok, actual Overflow, even though
  checked addition reaches exactly MAX. Reference includes an extra MAX guard;
  original destination_overflow test requires the same incorrect rejection.
  Post-return balance assertion is not reached.
- 0142 `hex-compound-path-result.json`, [0,101], 1827 ms: declared r/ur/ul/dr/dl
  deltas sum to (1,0); path `ruruldrdl` returns (0,0) via a hard-coded branch.
  Original compound-path test expects (0,0). This is a direct prompt/reference/
  test contradiction, not a claim about the generator's intent. Coordinate
  boundary overflow is an additional static concern, not executed here.
- 0151 `titleize-first-ascii-letter-result.json`, [0,101], 1479 ms:
  `123alpha.txt` becomes `123alpha` instead of `123Alpha`. Original title tests
  start words with ASCII letters and miss this case.
- 0154 `envelope-decoder-equality-result.json`, compile exit [1], 662 ms:
  requiring Eq for EnvelopeDecoder fails E0277. No test executable ran. Decoder
  has Clone/Debug/Default but lacks PartialEq/Eq; original tests compare decoded
  Envelope results, not the decoder itself.

No-hold is not admission approval; unresolved API/nontriviality items still
require adjudication. Frozen artifacts and scope v6 unchanged. GCS verified
through 397 holds / Rust batch 8 / 669 inspections; batch 9 awaits backup.
Continue position 136. No new VM, training seal or revised partition.
