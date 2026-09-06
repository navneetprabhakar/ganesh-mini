# Rust generation review, batch 14

Positions 196–210 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections. One new static hold. Total 759 unique
outside-sample inspections, 403 additive plus historical three = 406 holds.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 196 | 0224 | Already a historical VM timeout hold, not counted again. Checked polynomial and bounded trial division mathematically valid; full-range primality test expensive. No rerun. |
| 197 | 0230 | Typed API and error derives, validation before mutation, explicit zero/zero replacement and literal floating formula. Extreme finite addition stability not required separately from stated formula. No new hold. |
| 198 | 0231 | Exact API, pointer identity before reading, zero short circuit and nonzero copy/clear. Small cell operation nontriviality unresolved. No new hold. |
| 199 | 0233 | Explicit API/derives, zero-page precedence, exact preserved text and page count. Valid allocated ReadingItem slice bounds keep page arithmetic representable. No new hold. |
| 200 | 0229 | Exact field/API shapes, first-seen per-member resources, badges retained, saturating points and last credits. Repeated owner assignment has same specified final value. No new hold. |
| 201 | 0232 | Typed API, free and associated constructors, ordered owned records and first conversion failure context. Simultaneous construction-error precedence not fully specified. No new hold. |
| 202 | 0234 | Typed expression API/derives, checked left-to-right evaluation, lazy branches and successful nested Bind persistence. Deep recursion envelope not executed. No new hold. |
| 203 | 0235 | Static hold: check-then-drop strong-count race can omit last-clone close event. |
| 204 | 0236 | Typed API, bit set/clear and pre-clear snapshot correct. Other bits unreachable through public API; original tests cannot independently distinguish preserving them. Nontriviality/oracle sufficiency pending. No new hold. |
| 205 | 0237 | Typed API, route-before-sequence validation and exact bounded binary decoding. Private sequence exhaustion after infeasible retained dispatch count not newly adjudicated. No new hold. |
| 206 | 0238 | Explicit API, checked decimal sum, trimmed comment handling and exact ASCII identifiers. ASCII whitespace vertical-tab policy not independently adjudicated. No new hold. |
| 207 | 0239 | Explicit API, all structure checked before support, direct neighbors only and strict tie rejection. No new hold. |
| 208 | 0240 | Const generic API, safe zero-length loop and byte transformations without heap allocation. Extreme stack/resource envelope not newly executed. No new hold. |
| 209 | 0241 | Exact API, validation before activation, literal role preserved and borrowed accessor. Small state/format wrapper nontriviality unresolved. No new hold. |
| 210 | 0242 | Exact API/derives, normalized lookup/removal, pre-insert validation and owned removal. Empty lookup maps to missing; prompt only requires empty-name rejection for creation. No new hold. |

0235 static concurrency analysis: `Channel::drop` calls close only if
`Arc::strong_count(&self.inner) == 1`. With two final Channel clones on separate
threads, both drop bodies can observe count 2 before either inner Arc field is
dropped. Both skip close; the subsequent field drops release Inner, which has no
Drop implementation to emit Closed. Thus last-clone cleanup is not guaranteed.
Original tests drop clones sequentially and cannot expose this interleaving.
No stress test or runtime failure is claimed; this finding follows from the
reference's check-before-field-drop sequence. Other close/receive ordering
questions are not counted as additional findings.

Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
No new sandbox execution. No-hold is not admission approval; scope v6 unchanged.
GCS verified through 405 holds / Rust batch 13 / 744 inspections; batch 14 awaits
backup. Continue position 211. No new VM, seal or revised partition.
