# Go focused non-triviality review — batch 20

Positions286–300, full prompt/reference read; not a full new test/mutant review.
11 criterion-positive, four non-triviality holds; one also has an executed behavioral finding.
1274 total holds (1271 additive+3),3230 unique outside inspections. Resume301.

| Position | ID | Finding |
| --- | --- | --- |
| 286 | exp-v1-go-generation-0245 | Criterion-positive: escaped-comma parser maintains escape and token boundaries. |
| 287 | exp-v1-go-repair-0161 | Criterion-positive: transpose output dimensions must reflect the input matrix shape. |
| 288 | exp-v1-go-repair-0162 | Criterion-positive: mutate the actual run state instead of a copied struct value. |
| 289 | exp-v1-go-repair-0163 | Non-triviality hold: direct weekday AND-versus-OR correction. |
| 290 | exp-v1-go-generation-0248 | Criterion-positive: locked publish/subscribe snapshot and state ownership. |
| 291 | exp-v1-go-generation-0249 | Criterion-positive: block parsing, last-key-wins semantics and detached strip result. |
| 292 | exp-v1-go-generation-0250 | Criterion-positive: concurrent command catalog and in-memory state transitions. |
| 293 | exp-v1-go-repair-0165 | Non-triviality hold: direct alphabet accumulator assignment-to-addition correction. |
| 294 | exp-v1-go-repair-0167 | Non-triviality hold: direct final-token loop-bound correction. |
| 295 | exp-v1-go-repair-0168 | Non-triviality hold: direct annulus formula substitution. Also executed equal-finite-radii violation. |
| 296 | exp-v1-go-generation-0254 | Criterion-positive: dispatcher records audit after every non-nil call; nil dispatcher exception does not require impossible recording. |
| 297 | exp-v1-go-generation-0255 | Criterion-positive: concurrent wait-all execution with errors retained by input index. |
| 298 | exp-v1-go-generation-0256 | Criterion-positive: bounded active publication accounting. |
| 299 | exp-v1-go-generation-0257 | Criterion-positive: color catalog validation and detached state. |
| 300 | exp-v1-go-generation-0258 | Criterion-positive: validate all parcels, including unselected ones, and pointer bounds. |

go_0168_equal_radii_probe-result.json: Go1.22.12 exit[1], no timeout,26802ms. RingArea(1e200,1e200) returns NaN,nil despite the explicit equal-radii zero requirement.
Additive probe ran alongside original tests. Network off,1CPU/512MiB/64PIDs/60s.
Task, code, runtime and output hashes retained in the receipt.
Frozen candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

