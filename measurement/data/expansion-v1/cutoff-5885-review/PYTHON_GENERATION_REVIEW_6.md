# Python generation review, batch 6

Positions 76–90 of 684, v6 outside-sample Python generation queue. Fifteen full
prompt/reference/original-test inspections; four reproduced holds and one
static prompt/test contradiction. 510 additive plus historical three = 513
holds; 1,323 unique outside-sample inspections. No seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 76 | 0084 | Positive-step range excludes horizon, validates interval even for nonpositive horizon and returns fresh list. Output-size envelope pending; no new hold. |
| 77 | 0079 | Full width/type validation before integer addition and new rows agree. No new hold. |
| 78 | 0085 | Identifier validation, deepcopied registrations/retrievals and sorted capabilities agree for instance-owned state. Non-string lookup and custom copy behavior remain pending; no new hold. |
| 79 | 0086 | Ordered path extraction, falsey scalar preservation and typed joins agree. Copying unsupported malformed terminal objects before join validation remains pending; no new hold. |
| 80 | 0087 | Complete rectangular validation and copied retained slices agree. No new hold. |
| 81 | 0088 | Nonempty Kadane recurrence and all-negative handling agree after full validation. No new hold. |
| 82 | 0089 | repr-based literal output, sorted flags and exact boolean validation agree. Custom str repr behavior not imposed; no new hold. |
| 83 | 0090 | Hold: noninteger NaN position raises ValueError before required TypeError check. Ordinary repeated reflections, marker cycling and friction agree; large reflection-count resource envelope pending. |
| 84 | 0092 | Hold: finite integer coordinates 10**400 and 10**400+3 overflow validation although Manhattan distance is 7.0. |
| 85 | 0095 | Hold: already-fitting dimension 2**53+1 changes to 2**53 through float multiplication, contrary to explicit original-dimension identity. |
| 86 | 0096 | Whole-list deepcopy and shared snapshot-derived outputs agree. has_none equality-versus-identity semantics and unrestricted custom copy behavior remain pending; no new hold. |
| 87 | 0091 | Unique key/slot checks and sorted activation tuple agree. No new hold. |
| 88 | 0094 | Static hold: prompt says invalid title raises TypeError, but empty-title reference and original test require ValueError. Nested non-string JSON keys remain a separate contract question. |
| 89 | 0097 | Hold: valid UserDict scoped-suffix mapping rejected by dict-only check. Ordered matching and independently copied removed/remaining lists otherwise agree. |
| 90 | 0098 | Direct overlapping comparison and empty-needle boundaries agree. Exact-int versus integer-subclass acceptance remains pending; no new hold. |

Four probes ran in pinned Python 3.11.15, network disabled and resource limited;
all exited 1 without timeout. Static title contradiction is not presented as an
executed probe. Frozen candidate and original test artifacts are unchanged.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0090 | puck_field_type_probe.py / puck-field-type-result.json | 463 | ValueError for NaN position instead of TypeError. |
| 0092 | taxicab_integer_coordinate_probe.py / taxicab-integer-coordinate-result.json | 438 | OverflowError in math.isfinite on accepted integer coordinates. |
| 0095 | thumbnail_identity_probe.py / thumbnail-identity-result.json | 401 | 9007199254740992 returned instead of unchanged 9007199254740993. |
| 0097 | catalog_mapping_probe.py / catalog-mapping-result.json | 424 | TypeError rejects UserDict mapping. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Continue position 91. No admission seal, new VM or changed frozen sample.
