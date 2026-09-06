# Rust generation review, batch 25

Positions 361–375 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections; five new static contract-completeness
holds. Total 924 unique outside-sample inspections; 441 additive plus historical
three = 444 holds. Inspection is not seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 361 | 0420 | Exact layout types, duplicate-page prevalidation, kind-specific updates and deep snapshots agree. No new hold. |
| 362 | 0422 | Exact binary note layout, owned UTF-8, length/checksum/terminator checks agree. Original tests omit oversized encode despite explicit limit; reference checks u16 conversion. Method signatures/traits only partly stated; no new concrete hold here. |
| 363 | 0426 | Escape-aware separator location, nonempty decoded fields, physical numbering and rendering agree. Error names not frozen by tests; CRLF interpretation remains pending. No new hold. |
| 364 | 0423 | Per-channel quiet calls support non-Clone samples, finite metadata and unending next agree. Concrete constructor numeric types omitted but literals do not distinguish them in tests; no new hold. |
| 365 | 0424 | Static hold: config construction/default and diagnostic/span declarations required by tests are not supplied. |
| 366 | 0425 | Warm-up formula and independent direction alternation, unique settling targets and size-one cases agree for inspected reachable examples. Action field types and large wrapping-step/resource envelope remain pending; no claim of exhaustive usize execution. |
| 367 | 0428 | Exact state reducer validates before mutation and implements stated flag/screen transitions. No new hold. |
| 368 | 0429 | General positive alignment and checked smallest-multiple rounding agree at boundaries. No new hold; elementary scope pending. |
| 369 | 0430 | Trim/uniqueness, checked ID increment, exact permits and documents agree. Public malformed registry state and combined error precedence remain pending; no new hold. |
| 370 | 0431 | Two optional minima handle duplicates/full integer range without allocation or subtraction. No new hold; elementary scope pending. |
| 371 | 0432 | Declared grouping, textual digit key, alphabetic filtering and original tie-break agree with tests. Per-character versus contextual whole-string Unicode lowercasing is not resolved by examples; retained as a contract question, not an executed failure. |
| 372 | 0435 | Static hold: Packet/Endpoint public field declarations used by tests are omitted. |
| 373 | 0437 | Static hold: UploadLog construction/default and uploads field shape required by tests are omitted. |
| 374 | 0433 | Static hold: prompt refers to an absent reference API for Pose/Bearing/Step/Query/Command. |
| 375 | 0434 | Static hold: Entry field declarations and Value variant names/types required by tests are omitted. |

0424 names AuditConfig, Span, DiagnosticKind and Diagnostic but gives neither
their declarations nor a config constructor/default policy. Original tests call
AuditConfig::default(), access diagnostic.kind and diagnostic.span.start/end,
and inspect Debug names. All-enabled defaults are an unprovided requirement.

0435 names Packet and Endpoint without declaring fields/types. Tests directly
access endpoint.address and packet.from/body, requiring specific public owned
string fields. Behavioral agreement of the reference does not complete that API.

0437 specifies the stage_upload signature and matrix field names, but not
UploadLog's representation or initialization. Tests call UploadLog::default()
and directly read uploads as Vec<Vec<f32>>. Neither requirement is given.

0433 explicitly says types are "as shown by the reference API" but supplies no
such API. Tests construct Pose { x, y, bearing }, Step::Absolute { x, y },
Forward/Reverse payloads, and Query::State/Health variants. Saturating reference
behavior does not cure the missing declarations.

0434 names Entry and Value but omits their declarations. Tests require public
Entry { locale, section, key, template } owned strings, plus Value::String and
Value::Integer constructors; the prompt describes string/integer semantics
without specifying those Rust variants or the integer width.

These five holds are static comparisons; no new sandbox executions occurred
in this batch. Original tests and frozen candidates remain unchanged.
Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scope v6 unchanged. Continue 376. No new VM or training seal.
