# Rust generation review, batch 18

Positions 256–270 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections. One new static hold. Total 819 unique
outside-sample inspections, 417 additive plus historical three = 420 holds.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 256 | 0298 | Static hold: Position field names/types required by original tests omitted from prompt. |
| 257 | 0302 | Exact API/derives, specified fingerprint, zero-secret precedence, ordered alias replacement and no mutation on errors. Public duplicate slots unspecified. No new hold. |
| 258 | 0304 | Exact API, per-original-character escaping, optional current attribute and stable duplicate order. Small rendering exercise nontriviality unresolved. No new hold. |
| 259 | 0305 | Scalar-column offsets, trimmed-part ranges, error precedence and checked oversized decimal handling match the specification. Leading zeroes do not themselves overflow numeric parsing. No new hold. |
| 260 | 0303 | Exact postfix API, operand order, Unicode whitespace, checked arithmetic and zero-divisor precedence. No new hold. |
| 261 | 0307 | Empty-only route filtering, bytewise UTF-8 form encoding and validated/clamped same-day arithmetic. No new hold; elementary utility scope remains for nontriviality review. |
| 262 | 0309 | Exact types, trimming and preserved name/ID. Simultaneously invalid fields have no declared priority and original tests do not impose one. No new hold; elementary validation scope pending. |
| 263 | 0310 | Exact shipment fields, template and independent owned replacement. No new hold; elementary data-model scope pending. |
| 264 | 0311 | Ordered set differences satisfy distinctness, sorting, empties and immutability. No new hold; elementary set-operation scope pending. |
| 265 | 0312 | Private version/key context, exact response length, error clearing and XOR payload handling. Invalid-version context is not constructible through the public API; multi-gigabyte message limit not exercised. No new hold. |
| 266 | 0308 | Explicit initial flags, locked-before-disabled precedence, atomic errors, retained stored flags and reset-only unlock. No new hold. |
| 267 | 0313 | Const getters, bit masks, reserved-bit preservation and range rejection agree with prompt/tests. No new hold. |
| 268 | 0314 | Exact bytewise wrapping fingerprint and canonical string equality. Tests mirror the specified algorithm plus fixed vectors. No new hold. |
| 269 | 0315 | Trim/ASCII case handling and permanent close agree. Already-closed batch emits one Closed entry per original tests; wording permits this interpretation but does not explicitly fix cardinality. No new hold; ambiguity retained. |
| 270 | 0317 | Final marker, exact suffixes, ASCII numeric grammar, bounded values, equal endpoints and inclusive range agree. No new hold. |

0298 static contract/test comparison: prompt declares fields for Range and
Location but only asks for Position with public fields, never specifying which
fields or types. Original location helper directly constructs
`Position { line:u32, character:u32 }`. These required declarations are absent.
Reference also lacks an explicit empty-symbol guard when a caller populates the
public map with an empty key; this secondary case has not been probed and is not
claimed as executed evidence. One hold for the missing Position interface.

Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
No new sandbox execution. No-hold is not admission approval; scope v6 unchanged.
Batch complete; next position 271. No new VM, seal or partition.
