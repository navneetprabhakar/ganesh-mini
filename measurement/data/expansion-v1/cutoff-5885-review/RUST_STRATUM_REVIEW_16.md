# Rust generation review, batch 16

Positions 226–240 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections. Three new holds. Total 789 unique
outside-sample inspections, 412 additive plus historical three = 415 holds.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 226 | 0258 | Exact API and validation precedence, bounded low bytes, segment/block reversal with within-block order. No new hold. |
| 227 | 0259 | Explicit API and hash constants, distinct targets, first match, stable pair order and empty-plan errors. No new hold. |
| 228 | 0263 | Exact API/derives, strict decimal parser, checked coordinates and atomic follow restoration. No new hold. |
| 229 | 0265 | Exact API, validation before normal-state edits and nonmutating sorted rendering. Arbitrarily corrupted public layout fields not specified; underflow risk outside established constructor invariants not executed. No new hold. |
| 230 | 0267 | Exact API, final-address validation, inclusive empty-range endpoint and disjoint atomic exchange. Publicly malformed bank address span not explicitly specified. No new hold. |
| 231 | 0269 | Exact API, section-local uniqueness, first-equals parsing and physical line errors. Bracket-delimited text containing equals could be header or key/value; ambiguity not forced into a hold. |
| 232 | 0268 | Hold: independent machines share incorrect duration state and cloned machine panics after original transition. |
| 233 | 0272 | Typed trait/function API, wide signed/unsigned shift toward zero and idempotent clear. Small exercise nontriviality unresolved. No new hold. |
| 234 | 0273 | Exact consuming trait API, nested box moved without clone and checked subtraction. Small exercise nontriviality unresolved. No new hold. |
| 235 | 0274 | Typed fields/methods, full validation before replacement and length-prefixed injective key. get return type implicit; tests leave exact error variants unconstrained. No new hold. |
| 236 | 0275 | Exact API, scalar-preserving escapes, explicit empty token and duplicate order. Small formatting task nontriviality unresolved. No new hold. |
| 237 | 0276 | Typed simulation fields/function, snapshot turn queue, checked transforms and ordered routing. Error category discriminants checked but station/item payload oracle not exercised. No new hold. |
| 238 | 0271 | Static hold: required operation variant spellings/shapes omitted. |
| 239 | 0278 | Capability-gated trait shape and generic Copy blanket implementation; two low-level calls. Original harness is same-crate and does not certify downstream privacy with a separate-crate compile check. No new hold. |
| 240 | 0281 | Static hold: requested reference signatures absent from prompt. |

0268: `phase-machine-independence-result.json` records pinned network-disabled,
resource-limited Rust execution, exit codes [0,101], 1504 ms, no timeout. Both
independent tests fail: equal-warmup machines return the first machine's 20 ms
duration instead of the second's 30 ms; a clone panics after the original removes
the shared warmup state. The clone's later duration assertion is not reached.
Prompt additionally mandates an exact two-public-field struct while asking for
private stored duration; original tests construct two-field struct literals,
preventing a normal additional private field. One candidate hold, not three.

0271: tests directly construct Op::Push(i64), Load(String), Store(String), Add,
Subtract, Multiply and Divide. Prompt names operation concepts but omits their
Rust variant declarations; Sub versus Subtract and payload choices are not
recoverable from a supplied API. RunOutput fields are also absent, though tests
do not directly inspect them. No runtime failure claimed.

0281: prompt says new/encode/decode have reference signatures, without providing
them. In particular constructor parameter order/types and encoding return shape
are unstated. Original tests exercise method calls but not new, so constructor
conformance is neither specified nor verified. No runtime failure claimed.

Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
No-hold is not admission approval; scope v6 unchanged. GCS verified through 412
holds / Rust batch 15 / 774 inspections; batch 16 awaits backup. Continue 241.
No new VM, training seal or revised partition.
