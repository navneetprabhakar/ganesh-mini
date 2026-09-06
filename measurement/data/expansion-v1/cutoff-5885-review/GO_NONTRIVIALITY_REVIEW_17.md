# Go focused non-triviality review — batch 17

Positions241–255, full prompt/reference read; not a full new test/mutant review.
Ten criterion-positive, five non-triviality holds plus one static determinism hold.
1256 total holds (1253 additive+3),3185 unique outside inspections. Resume256.

| Position | ID | Finding |
| --- | --- | --- |
| 241 | exp-v1-go-repair-0134 | Non-triviality hold: direct uppercase base literal correction. |
| 242 | exp-v1-go-generation-0205 | Criterion-positive: bounded worker pool, disjoint indexed output and nested nil/empty ownership with completion wait. |
| 243 | exp-v1-go-generation-0206 | Criterion-positive: width64 special case, operand representability and masked fixed-width bit reports. |
| 244 | exp-v1-go-generation-0207 | Criterion-positive: nil channel, closure and stop signal are distinct termination states; later signals remain unread. |
| 245 | exp-v1-go-generation-0209 | Non-triviality hold: fully specified action table with direct authentication and equality guards. |
| 246 | exp-v1-go-repair-0137 | Criterion-positive: JSON stream must reach EOF after the first value, distinguishing valid trailing whitespace from extra or malformed data. |
| 247 | exp-v1-go-repair-0138 | Non-triviality hold: remove special-case branch in favor of direct math.Round; supplied parse/range guards unchanged. Decimal-text versus parsed-float precision is not adjudicated here. |
| 248 | exp-v1-go-repair-0139 | Non-triviality hold: explicitly disclosed shadowed accumulator becomes an assignment. |
| 249 | exp-v1-go-repair-0140 | Criterion-positive: prime predicate must exclude zero/one while preserving UTF-8-valid rune-length selection and output shape. Huge string/divisor limits not executed. |
| 250 | exp-v1-go-generation-0212 | Criterion-positive: rectangular shape validation and inclusive overlapping two-dimensional window traversal without mutation. |
| 251 | exp-v1-go-generation-0213 | Criterion-positive normalized composition; static determinism hold because distinct input map keys may normalize to the same key with different values. |
| 252 | exp-v1-go-generation-0214 | Criterion-positive: required rights subset, no-op before revision overflow and failure-preserving value/invalidation result. |
| 253 | exp-v1-go-generation-0215 | Non-triviality hold: directly specified field getters plus a name-and-sum loop. |
| 254 | exp-v1-go-generation-0216 | Criterion-positive: tagged varint framing, canonical length verification, bounded consumption and malformed-input distinctions. |
| 255 | exp-v1-go-repair-0141 | Criterion-positive: transactional result rolls back all earlier transfers on any later validation failure, preserving independent returned storage. |

No new candidate execution. Static generation0213 example: base map containing
A:first and a:second, with no overrides/removals. Both keys normalize to a;
unordered map iteration decides the surviving value, violating deterministic
composition. No tie policy is specified. This follows the already documented
case-colliding-map pattern; it is not a claimed new runtime observation.
Candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
