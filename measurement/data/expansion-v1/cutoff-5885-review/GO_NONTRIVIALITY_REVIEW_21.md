# Go focused non-triviality review — batch 21

Positions301–315, full prompt/reference read; repair source compared with reference.
Not a full new test/mutant review. Eight criterion-positive, seven non-triviality
holds plus one behavioral hold. 1282 total holds (1279 additive+3),3245 unique
outside inspections. Resume316.

| Position | ID | Finding |
| --- | --- | --- |
| 301 | exp-v1-go-repair-0169 | Criterion-positive: copy the overlay map before applying changes. |
| 302 | exp-v1-go-repair-0170 | Non-triviality hold: direct inclusive-enumeration loop-bound correction. Extreme loop duration was not executed. |
| 303 | exp-v1-go-repair-0171 | Criterion-positive: cancellation check must precede visit, preserving callback/error boundary. |
| 304 | exp-v1-go-repair-0172 | Criterion-positive: distinguish current parser depth from maximum nesting depth. |
| 305 | exp-v1-go-generation-0259 | Non-triviality hold: literal argument-introduction formatter. |
| 306 | exp-v1-go-generation-0261 | Non-triviality hold: three directly specified standard-library formatting wrappers. |
| 307 | exp-v1-go-generation-0262 | Non-triviality hold: fixed sentinel-to-value mapping. |
| 308 | exp-v1-go-generation-0263 | Criterion-positive: stack-machine operand order, underflow and exactly-one-final-value invariant. |
| 309 | exp-v1-go-generation-0264 | Criterion-positive: backwards in-place stuffing preserves unread source values. |
| 310 | exp-v1-go-repair-0173 | Non-triviality hold: direct count increment two-to-one substitution. |
| 311 | exp-v1-go-repair-0174 | Non-triviality hold: direct initial loop index one-to-zero substitution. |
| 312 | exp-v1-go-repair-0175 | Criterion-positive: copy before interval sorting to preserve caller ownership. |
| 313 | exp-v1-go-repair-0176 | Non-triviality hold: remove the extra minus-one from the supplied primality modulo expression. Whole-int trial-division runtime not measured. |
| 314 | exp-v1-go-generation-0266 | Criterion-positive pagination and validation task; executed behavioral hold for signed page-end overflow. |
| 315 | exp-v1-go-generation-0267 | Criterion-positive: link resolution, cycle handling and explicit hop cap. ReturnLinkTarget explicitly skips target validation; that exception is not a defect. Nil/empty byte-copy shape preservation is not specified. |

go_0266_page_overflow_probe-result.json: Go1.22.12 exit[1], no timeout,26665ms.
One valid record, Cursor="1" and PageSize=MaxInt is allowed: offset equals match
count and page size is positive. Signed offset+size overflow yields a negative
slice bound and panic instead of an empty terminal page. Small input; not an
allocation limit. Additive probe ran alongside original tests.
Network off,1CPU/512MiB/64PIDs/60s. Task, code, runtime/output hashes retained.
Frozen candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

