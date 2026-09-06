# Rust generation review, batch 17

Positions 241–255 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections. Four new holds. Total 804 unique
outside-sample inspections, 416 additive plus historical three = 419 holds.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 241 | 0282 | Typed API, exact credentials and username-before-password validation, no trimming. Small comparison task nontriviality unresolved. No new hold. |
| 242 | 0285 | Typed fields/function, exact seven lines and uppercase bounded hex. Small formatting task nontriviality unresolved. No new hold. |
| 243 | 0287 | Typed methods, validated registration and owned sorted snapshots. Invalid identifier inside apply has unspecified EmptyId/UnknownId/malformed precedence; not forced into a hold. |
| 244 | 0288 | Typed API, checked adjustment before mutation and owned lexicographic output. No new hold. |
| 245 | 0284 | Typed methods, strict decimal and exact flag aliases. Error String payload meanings selected by tests but not explicitly described; full self-containment unresolved. No new hold. |
| 246 | 0286 | Typed API, stable descending reading/ascending station and malformed counts even at zero limit. Signed-positive numeric syntax unspecified; not forced into a hold. |
| 247 | 0292 | Static hold: tested Order field/API declarations omitted. |
| 248 | 0294 | Static hold: tested Position fields and move-generation API omitted. |
| 249 | 0289 | Typed free functions, command/options parsing and deterministic message counts. Config/RunReport shapes incomplete and log/color value retention not directly tested; full API/oracle approval unresolved. No new hold. |
| 250 | 0290 | Static hold: tested nested Limits field shape omitted. |
| 251 | 0295 | Exact API, maximum historical count, explicit saturating limits, bounded stop and consumed finish behavior. No new hold. |
| 252 | 0296 | Explicit generic predicate/trait API, validation before per-record predicate, stable path deduplication and borrowed optional output. No new hold. |
| 253 | 0297 | Hold: empty first-word output does not alias original whitespace string. |
| 254 | 0299 | Exact API/derives, cancellation precedence, owned unchanged identifiers and ordered duplicate chunks. No new hold. |
| 255 | 0300 | Exact API, checked field slices, tag-offset policy errors, field-start truncation and exact trailing position. No new hold. |

0292: original tests directly read order.id, construct Side::Buy/Sell, and use
specific method arguments/return shapes. Prompt names public Order but gives no
field declaration, leaving its required public id shape unstated.
0294: tests construct `Position { row:usize,col:usize }` and call valid_moves,
whose method name/signature is absent from the prose. The all-leaders-absent
winner case is also underspecified, but not a separate hold.
0290: tests require `parsed.limits.max`, nested public Limits, and public id,
label, hint, kind and required fields. Recognized input keys do not specify this
Rust output representation. These three are static holds, not execution failures.

0297: `first-word-empty-alias-result.json` records pinned network-disabled,
resource-limited execution: [0,101], 1442 ms, no timeout. An owned all-whitespace
String yields an empty result whose pointer is outside the input's inclusive
byte range. Original tests check content on empty cases but aliasing only on a
nonempty word. The prompt requires a slice of the original without an empty-case
exception. No mutation or allocation claim is inferred from this probe.

Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
No-hold is not admission approval; scope v6 unchanged. GCS verified through 415
holds / Rust batch 16 / 789 inspections; batch 17 awaits backup. Continue 256.
No new VM, training seal or revised partition.
