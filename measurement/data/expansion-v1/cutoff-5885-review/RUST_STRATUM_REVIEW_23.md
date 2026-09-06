# Rust generation review, batch 23

Positions 331–345 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections; one new sandbox-confirmed hold.
Total 894 unique outside-sample inspections; 433 additive plus historical three
= 436 holds. Inspection is not seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 331 | 0388 | Both vector/map backends implement exact trait, atomic errors, owned get/all and ascending IDs. No new hold. |
| 332 | 0389 | Exact prefix borrow including empty pointer, length precedence and selected-byte-only validation. No new hold; elementary scope pending. |
| 333 | 0390 | Ordered single/batch transitions and cloned returned states agree with tests. Initial state/counter and combined rename-error priority not explicitly stated; retained for completeness adjudication, no new hold. |
| 334 | 0392 | First-equals split, trim/filter and ordered duplicate selectors agree. No new hold; elementary scope pending. |
| 335 | 0394 | Full ragged check before mutation; original first-row/column flags and marker algorithm use constant auxiliary space. No new hold. |
| 336 | 0391 | Exact diagnostic syntax, locale fallback and message mapping agree. No new hold; elementary scope pending. |
| 337 | 0393 | Sandbox hold: inverse uses forward rotation signs, original inverse test also expects wrong values. |
| 338 | 0396 | Checked ledger operations and original tests agree. record return-value meaning and withdrawal restoration after intervening balance growth are incompletely specified; no new concrete hold here. |
| 339 | 0397 | Exact eight-byte lowercase hex gate, replace return, kind rendering and owned descriptions agree. No new hold. |
| 340 | 0400 | Exact twenty composed pairs, adjacent consumption and unsupported-mark retention agree. No new hold. |
| 341 | 0401 | Plan add/parse/merge and atomic prevalidation agree with tests. CRLF interpretation and public-versus-private stages declaration remain completeness questions. No new hold. |
| 342 | 0398 | Checked integer kinds and float promotion agree with original tests. Unary plus preservation versus nonfinite rejection, and mixed-kind zero-divisor precedence remain ambiguous. No new hold. |
| 343 | 0402 | Exact limited combining-unit rule, leading marks, tab replacement and owned ranges agree. No new hold. |
| 344 | 0403 | Checked event ledger and successful-ID tracking agree. Exact two-field API versus internal operation set and duplicate malformed-event priority remain unresolved; no new hold. |
| 345 | 0404 | Atomic clone-before-step and ordered following agree. Private reachable neighbor deltas stay bounded, so unchecked abs on i32::MIN is not a demonstrated reachable bug. No new hold. |

0393: `camera_inverse_rotation_probe.rs` and `camera-inverse-rotation-result.json`
preserve a pinned network-disabled round-trip execution: compile 0, test 101,
1,529 ms, no timeout. For center (10,-2), rotation pi/2, zoom 2, width 8,
height 6, inverse of NDC (2,-3), followed by the returned view and projection,
produces approximately (-2,3), not (2,-3). View rotates by -rotation; inverse
must use +rotation. Reference uses +s in inverse x and -s in inverse y, the
same signs as forward rotation. Original test explicitly expects world (5.5,-6)
rather than (14.5,2), so its assertion reinforces the error instead of detecting
it. No changes to original tests or candidates were made.

Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scope v6 and historical evidence unchanged. Continue 346. No new VM or seal.
