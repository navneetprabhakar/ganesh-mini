# Rust generation review, batch 20

Positions 286–300 of the frozen 684-record outside-sample queue. Fifteen prompt,
reference and original-test inspections; seven additional holds (six static,
one sandbox-confirmed). Total 849 outside-sample inspections, 428 additive plus
historical three = 431 holds. Inspection is not seven-criterion admission.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 286 | 0335 | Exact Panel API, significant whitespace, numeric bounds and required fields. Extra equals in kind is rejected by reference but prompt grammar is ambiguous; no new hold. |
| 287 | 0336 | Heap priority/FIFO, generation-tagged stale entries, atomic errors and checked sequence agree. Exhaustion is private and not practically exercised. No new hold. |
| 288 | 0337 | Exact config API, parser ranges, patch/default/disabled behavior agree. Whitespace trimming and signed-positive decimal grammar are unspecified; malformed public patches not adjudicated. No new hold. |
| 289 | 0338 | Exact generic tracker API and move/activate/leave transitions, owned listener and immutable reads. No new hold. |
| 290 | 0339 | Static hold: public unbounded payload contradicts assumption that all representable packets encode for infallible fingerprint. |
| 291 | 0340 | Exact option bits and conveyor transitions; fault gate, alarm and error atomicity agree. No new hold. |
| 292 | 0341 | Exact metadata API, checked revision before mutation, no-op-at-maximum and byte-length encoding. Public malformed ID/map states not adjudicated. No new hold. |
| 293 | 0342 | Sandbox hold: Unicode trim violates ASCII-only trimming for both value preservation and required-key recognition. |
| 294 | 0344 | Static hold: Item types and Catalog signatures required by tests absent from prompt. |
| 295 | 0346 | Static hold: Appliance field types and free-function signatures omitted; tests require writable u64 start counter. |
| 296 | 0347 | Static hold: Field variants and Selector constructor signatures required by tests omitted. |
| 297 | 0348 | Static hold: geometric function ownership/signatures and required Point traits omitted. Arithmetic and exact angular ordering inspected without a new runtime defect. |
| 298 | 0343 | Static hold: prompt refers to an expected-solution API that is not supplied. |
| 299 | 0350 | Exact generic pull API, one-time move, FIFO mixed signals, pending/end and close-drain behavior agree. No new hold. |
| 300 | 0351 | Wider derived coordinate, level-before-shift, ordered validation and six exact offsets agree. No new hold. |

## Evidence

0339: Prompt declares public `payload: Vec<u8>` and says encode rejects lengths
above 65,535, then justifies infallible fingerprint by saying all representable
packets encode. A 65,536-byte payload is directly representable, but has no
canonical encoding under this contract. Reference calls encode().expect;
original tests omit oversized encode/fingerprint. Static contradiction only;
no new panic execution claimed.

0342: `profile_ascii_trim_probe.rs` and `profile-ascii-trim-result.json` preserve
two isolated diagnostic tests in the pinned network-disabled Rust sandbox.
Compile exit 0, test exit 101, 1,800 ms, no timeout. U+2003 at either edge of a
label is removed instead of preserved. A U+2003-prefixed code key incorrectly
satisfies the required ASCII key. Original tests only exercise ASCII trimming.

0344: Prompt gives Item field names, not types; original helper constructs owned
String fields. put_collection takes owned String/Vec<Item>, first_names yields
an indexable/equatable vector, and summarize_first yields owned String pairs;
the prompt does not give these interface declarations.

0346: Fields are named without types or public declarations and functions lack
signatures. Tests write `appliance.start_count = u64::MAX` and pass owned String
and u64 capacity into new_appliance, requiring hidden concrete API choices.

0347: Prompt names Field/TextMatch but never declares their variants. Tests
require Field::Code/Field::Alias and exact/prefix(field, owned String), and
select results support Vec-style indexing. Borrowing behavior itself matches.

0348: Prompt supplies Point coordinates but not function signatures. Tests pass
Point by value repeatedly and compare arrays/results, relying on Copy/equality;
functions must return Result<usize, String>/Result<Vec<Point>, String> with
owned origin and borrowed slice. Exact arithmetic uses i64 differences and
i128 squared distances/cross products and does not show subtraction overflow.

0343: Prompt explicitly requests structs "shown by the API in the expected
solution" without supplying that API. Tests construct Rules with u64 and usize
fields, inspect Motion fields, and use several ownership-sensitive method
signatures. These are not inferable exact declarations. Blank-versus-empty
owner behavior remains a secondary unresolved wording question.

Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scope v6, frozen sample and historical partition unchanged. Continue 301.
