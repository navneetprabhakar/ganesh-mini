# Python generation review, batch 15

Positions 211–225 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; eight reproduced holds.
579 additive plus historical three = 582 holds; 1,458 unique outside-sample
inspections. No seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 211 | 0236 | Frozen models, ordinary scalar/group validation, duplicate-code checks and independent render containers agree; no new hold. |
| 212 | 0239 | Hold: NaN elapsed duration accepted despite nonnegative requirement. Maximum NaN shares static defect but second assertion did not execute. Duplicate-aware matching and runtime warning behavior agree ordinarily. |
| 213 | 0240 | Ascending greedy selection maximizes count with zero/exact-capacity support and exact integers; no new hold. |
| 214 | 0238 | Balanced/size chunking, occurrence-level copies and empty cases agree. Sentinel defaults differ from displayed None signature; within-entry alias wording remains pending, no new hold. |
| 215 | 0245 | Hold: shared Article/Other field list remains shared after deepcopy, so apply and rollback alter unrelated model. Ordinary schema validation/order agree; exact-descriptor bool/int equality pending. |
| 216 | 0241 | Exact surplus calculation, divisibility, tuple snapshot and named fields agree. Legacy sequence protocol acceptance pending; no new hold. |
| 217 | 0242 | Hold: whitespace-padded sentinel accepted contrary to exact STOP; original test explicitly requires it. Numeric token underscore/decimal-limit domain remains pending. |
| 218 | 0243 | Exact adjacent/window sums and short inputs agree. Quadratic window construction and legacy sequence acceptance pending; no new hold. |
| 219 | 0244 | Hold: mean difference of one collapses to zero after premature integer division to float. Ordinary schema validation/tie order agree. |
| 220 | 0247 | Authentication priority, complete ID validation, lookup and single upload/copy agree ordinarily. Callback mutation and arbitrary noncopyable nested data remain pending; no new hold. |
| 221 | 0248 | Multi-pointer growth, duplicate suppression and bounded position agree; no new hold. |
| 222 | 0249 | Hold: list deployment raises TypeError rather than required ValueError. Ordinary loader/copy checks agree; function-object mutable attributes remain a copy-contract issue. |
| 223 | 0251 | Hold: superscript numeric path passes isdigit then raises ValueError instead of400. Ordinary catalog validation/responses/copies agree; mapping breadth and escaped identifier paths pending. |
| 224 | 0252 | Hold: list state raises TypeError rather than ValueError in both renderers. Ordinary filtering/order/slug checks and copies agree. |
| 225 | 0250 | Hold: canonical year0001 rejected by pinned strftime roundtrip; NaN minutes accepted as nonnegative. Locale-dependent English weekday names remain a static concern. |

Eight pinned Python 3.11.15 probe runs, network disabled/resource limited, all
exit1 without timeout. Holds remain review items, not final rejection decisions.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0239 | auditor_nan_duration_probe.py / auditor-nan-duration-result.json | 441 | Observation NaN accepted; later maximum assertion not reached. |
| 0245 | revision_shared_models_probe.py / revision-shared-models-result.json | 429 | Both apply/rollback change unrelated Other fields. |
| 0242 | tokens_exact_sentinel_probe.py / tokens-exact-sentinel-result.json | 406 | Padded STOP accepted. |
| 0244 | rank_field_integer_difference_probe.py / rank-field-integer-difference-result.json | 456 | Score0 instead of1. |
| 0249 | environment_deployment_type_probe.py / environment-deployment-type-result.json | 403 | Unhashable list TypeError. |
| 0251 | asset_nondecimal_probe.py / asset-nondecimal-result.json | 401 | Malformed path raises instead of400 response. |
| 0252 | release_state_type_probe.py / release-state-type-result.json | 403 | Both renderers raise unhashable list TypeError. |
| 0250 | visits_year_nan_probe.py / visits-year-nan-result.json | 397 | Early-year ValueError and NaN validation failure. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Continue position226. Original candidates/tests/sample/partition unchanged.
