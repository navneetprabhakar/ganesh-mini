# Final systematic delta: TypeScript C — 2026-09-08

Gate 2. Frozen `final-systematic-delta-queue-v1.json`, selecting only
`prior_held == false` and `stratum.lane == "typescript"`, preserving record order.
Exactly 36 records; criterion C is `required_property_copy_loss` only.
All 36 already have inspection credit. No central edits, candidate execution,
cloud operations, new unique coverage or admission seal.

Result: **36 scoped positives, 0 proposed holds, 0 undecided C questions**.
“Positive” includes contracts that return primitives or require no record copying;
it does not certify unrelated prompt/API, numeric, test or other criteria.
The three earlier TypeScript property holds are not silently reconsidered by this
disjoint frozen queue.

## Method

Reconciled numbered residual/array findings per ID. Fresh full prompt/reference/
test rereads were needed for 0003, 0018, 0054, 0157, 0289, 0312, 0321, 0335,
0369 and 0378. Additional prompt/reference checks clarified 0013, 0019, 0020,
0039, 0043, 0085, 0113, 0125, 0141, 0147, 0198, 0246, 0258, 0355 and 0364;
their existing test-review evidence is retained, not misreported as fresh full
test reads. Remaining records carry substantive existing explicit-field/internal
record evidence listed below.

Frozen source: `datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl`,
SHA256 `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
No code was run. Source reasoning distinguishes public record spreads from direct
field construction, internal literals, shallow arrays and arbitrary-key merges.
There is no requirement to preserve descriptors or prototypes themselves.

## Exact frozen-order dispositions

Evidence abbreviations: Rn = `JS_TS_RESIDUAL_REVIEW_n.md`;
An = `ARRAY_STRATUM_REVIEW_n.md`. All paths are relative to this note.

| Position | Candidate ID | C disposition and substantive basis |
| --- | --- | --- |
| 1 | exp-v1-typescript-generation-0003 | Positive. Full reread: captions, data, threshold and callback are accessed directly; output fields are explicit, byte arrays copied before/after callback. Hidden required input fields are not lost. R1. |
| 2 | exp-v1-typescript-generation-0013 | Positive. All four required arrays are read and validated by key; entries/dependencies are explicitly constructed shallow arrays. The contract preserves opaque element identity and does not require cloning their fields. R2 plus prompt/reference check. |
| 3 | exp-v1-typescript-generation-0018 | Positive. Full reread: constructor/create/copy enumerate required field names explicitly. Update uses hasOwnProperty, including non-enumerable own name/email/yearsActive, then directly assigns values; no spread loss. Explicit-undefined own patches are rejected. Inherited patch values are not promoted to supplied own changes. A2. |
| 4 | exp-v1-typescript-generation-0019 | Positive. Renderer reads label/tone/side/limit directly and returns a primitive string. No record copy can discard required properties. Optional defaulting questions are not C. A2 plus prompt/reference check. |
| 5 | exp-v1-typescript-generation-0020 | Positive. Explicit state and view literals retain directly read bulletin values; readIds and badges are copied arrays. Spread is over those arrays, not caller record fields. R3 plus prompt/reference check. |
| 6 | exp-v1-typescript-generation-0039 | Positive. Encoder accesses channel/leg/plan fields directly and returns encoded text; exact leg identity is expressly required. No detached channel-copy promise is added. R5 plus prompt/reference check. |
| 7 | exp-v1-typescript-generation-0043 | Positive. Fresh nested results spread module-defined constant literals with known enumerable scalar fields. No user input record is copied; externally redefining readonly exported constants is not required. R6 plus prompt/reference check. |
| 8 | exp-v1-typescript-generation-0054 | Positive. Full reread: validator returns error strings, not a copied WarehouseQuery. Required page/pageSize are read directly; own optional validation includes hidden own fields. Inherited optional presence interpretation is not a required-copy loss. R7. |
| 9 | exp-v1-typescript-generation-0055 | Positive. AdaptiveMenu copies snapshots of fixed internal definitions; no caller-controlled required record descriptors enter the copied definitions. A5. |
| 10 | exp-v1-typescript-generation-0056 | Positive. Explicit primitive-field copying retains required values; no field-bearing public input is shallow-spread away. R8. |
| 11 | exp-v1-typescript-generation-0085 | Positive. Contract explicitly requires shallow preference merges over an arbitrary-key scalar bag, not preservation of named required record fields or arbitrary hidden descriptors. State and listener snapshots are fresh spreads; no new hidden-key mandate inferred. A9 plus prompt/reference check. |
| 12 | exp-v1-typescript-generation-0104 | Positive. Headings are parsed from text into ordered new entries; required values originate in parsing, not public record spreads. R13. |
| 13 | exp-v1-typescript-generation-0113 | Positive. SVG renderer reads options directly and returns text; no required input-property copy path. R14 plus prompt/reference check. |
| 14 | exp-v1-typescript-generation-0125 | Positive. ActionChip constructs its node explicitly, copies the child array and intentionally preserves child identities. handleAction directly reads target fields and mutates the designated children; deep cloning child records would contradict identity requirements. R15 plus prompt/reference check. |
| 15 | exp-v1-typescript-generation-0126 | Positive. openCatalog validates public tables/columns and copies them field-by-field. Required values are not selected through enumeration/spread. A13. |
| 16 | exp-v1-typescript-generation-0141 | Positive. theme/options fields are read directly and fresh class-string fields constructed explicitly. R16 plus prompt/reference check. |
| 17 | exp-v1-typescript-generation-0147 | Positive. Notice command is an internally constructed literal per instance; registry handler/unregister identities follow the explicit API. No public command record is copied. R17 plus prompt/reference check. |
| 18 | exp-v1-typescript-generation-0157 | Positive. Full reread: mode/location/temperature/unit/query are read directly and each PanelRow is an explicit new literal; shortcuts become fresh text rows. No required property is omitted through enumeration. A16. |
| 19 | exp-v1-typescript-generation-0170 | Positive. Prior source review identifies copies of internally created dense records; no public field-bearing object is spread into storage. A18. |
| 20 | exp-v1-typescript-generation-0178 | Positive. Prior per-ID review explicitly establishes seed/update field copies and fresh reads; required values are retained rather than spread selectively. R20. |
| 21 | exp-v1-typescript-generation-0179 | Positive. Complete validation precedes explicit field copies, preserving path/group values and duplicate order. R20. |
| 22 | exp-v1-typescript-generation-0198 | Positive. Named RuleOptions values are read directly; RuleSpec and caption are explicit literals. style is an arbitrary-key default/override bag copied by ordinary spread, with no named required input style fields or descriptor-preservation requirement. Do not extend C into a universal hidden-style-key contract. A21 plus prompt/reference check. |
| 23 | exp-v1-typescript-generation-0246 | Positive. Destructuring reads current/total/radius directly; output is a newly built primitive token array. No record property copy. A26 plus prompt/reference check. |
| 24 | exp-v1-typescript-generation-0247 | Positive. Required trims and navigation projection use explicit detached fields; inherited/hidden required readable values are not lost through a public-record spread. R28. |
| 25 | exp-v1-typescript-generation-0249 | Positive. Bookmark/member records are copied through explicit fields; ranking and tie logic do not change that property retention. A26. |
| 26 | exp-v1-typescript-generation-0253 | Positive. Primitive metadata fields are copied explicitly; URI/topology interpretations do not establish required property loss. A27. |
| 27 | exp-v1-typescript-generation-0256 | Positive. Required fields are normalized directly, defaults retain false and fresh schema descriptors are constructed. Runtime freezing is not a property-copy requirement. R29. |
| 28 | exp-v1-typescript-generation-0258 | Positive. Primitive state/delay input produces twelve complete internally constructed spoke literals and explicit output fields. R29 plus prompt/reference check. |
| 29 | exp-v1-typescript-generation-0289 | Positive. Full reread: required member fields are validated/read directly and rendered to a primitive string, with no intermediate public-record spread. R34. |
| 30 | exp-v1-typescript-generation-0312 | Positive. Full reread: initial required fields copied explicitly. Patch contract expressly ignores inherited values; hasOwnProperty covers hidden own relevant fields and direct assignment preserves them. Internal current spread is safe. Unknown-extra validation remains a separate API interpretation, not missing required copied fields. R36. |
| 31 | exp-v1-typescript-generation-0321 | Positive. Full reread: store loads and save snapshots use explicit field copies; edit directly reads output/volume/muted and constructs candidate fields, including valid hidden own values. No supplied valid field is omitted merely for enumerability. Undefined/unknown policy is not C. R36. |
| 32 | exp-v1-typescript-generation-0335 | Positive. Full reread: sorting copies only the input array; each timeline record is explicitly reconstructed from sequence/type/optional actor then frozen. Hidden/inherited readable required fields survive. R37. |
| 33 | exp-v1-typescript-generation-0355 | Positive. Primitive channel/payload API returns strings/counts; private queues are not exposed. No record-copy operation. R38 plus prompt/reference check. |
| 34 | exp-v1-typescript-generation-0364 | Positive. Numeric/unit inputs read directly and explicit CapacityAssessment fields constructed. No validated public field is lost through spread. R38 plus prompt/reference check. |
| 35 | exp-v1-typescript-generation-0369 | Positive. Full reread: variant fields are accessed directly; function returns an error-string array, not a copied BoardCommand. Blank optional-code interpretation is separate and does not reopen C. R39. |
| 36 | exp-v1-typescript-generation-0378 | Positive. Full reread: assignment sku/group are read directly into scalar maps; open builds the complete private Lot literal, then close/list spread only internally created lots. Required caller record fields cannot be dropped by those copies. A36. |

## Closure boundary

The C question is resolved for every listed ID. These are not statements that all
old prose caveats are defects, nor that every other criterion is now positive.
Own-field update handling, explicit field construction, primitive outputs and
intentional shallow/identity contracts are substantive reasons for closure.
No fresh hostile-object, descriptor-preservation or universal deep-copy guarantee
has been imposed. This note proposes no additional hold IDs.
