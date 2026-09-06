# Array-validation follow-up, batch 27

Positions 391–405: 15 new / 413 unique outside-sample inspections. Six new
holds: **282 additive / 285 including historical three**. Prompts, references
and original tests inspected. No duplicate IDs added.

| Position | Candidate | Scoped finding |
| --- | --- | --- |
| 391 | JS generation0302 | Query fields validated with for-of; fixed catalog and explicit property copies. No new hold. |
| 392 | JS generation0305 | Per-item normalization, for-of tags, Map IDs and explicit copies. No new hold. |
| 393 | JS generation0308 | Missing initial token accepted. permit-missing-token-result.json, 357 ms. |
| 394 | JS generation0309 | Missing collection record accepted. collection-missing-record-result.json, 436 ms. |
| 395 | JS repair0208 | ID-based once removal precedes invocation. Earlier persistent listener can reenter before a later once listener; snapshot-removal rule conflicts with global single-use interpretation. Leave this edge for oracle adjudication, no reproduced defect claimed. |
| 396 | TS repair0169 | Fixed dense opacity validation precedes predicate; fresh primitive styles, no retained IDs. Missing datum policy unspecified. No new hold. |
| 397 | TS generation0253 | Primitive metadata copies, case folding and host suffix boundary inspected. Exact malformed URI grammar and topology fallback precedence need oracle clarification; no new hold from this scoped inspection. |
| 398 | TS generation0255 | setBadge accepts missing byte instead of INVALID_BADGE. profile-missing-badge-byte-result.json, 2113 ms. |
| 399 | JS generation0316 | Missing string entry accepted. reading-workspace-missing-entry-result.json, 350 ms. |
| 400 | JS repair0212 | Missing string field accepted. encode-fields-missing-field-result.json, 406 ms. |
| 401 | JS generation0314 | Valid numeric payload 1 rejected by explicit special case; original malformed test motivates this unsupported restriction. envelope-valid-numeric-payload-result.json, 337 ms. Sparse configuration also static concern, not separately executed. |
| 402 | JS generation0320 | Object.keys creates dense list and matches explicit own-enumerable scope; negative zero preserved. encodeURIComponent is explicitly prescribed, so lone-surrogate URIError is not automatically a defect. No new hold. |
| 403 | JS generation0322 | Explicit required property copies; subsequent for-of encounters holes and throws TypeError. Internal dense copies safe to spread. No new hold. |
| 404 | JS repair0215 | for-of validates all records; filter preserves required retained identities. No new hold. |
| 405 | TS generation0263 | Copied/frozen options, singleton ignore/reset and isolated instances inspected. Overlapping-separator precedence and missing-slot policy unspecified; leave for oracle adjudication, no automatic hold. |

All six probes failed without timeout in pinned network-disabled/resource-limited
sandboxes (JS exit 1; TS compile succeeded then runtime exit 1). Scoped negative
findings are not seven-criterion approvals. Frozen data/sample/partition unchanged.
No training seal or new VM. Scope v6 unchanged. GCS verified through 279 holds;
this batch awaits backup. Continue position 406 of 544 outside-sample array hits.
