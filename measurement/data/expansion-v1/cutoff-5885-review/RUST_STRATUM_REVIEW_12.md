# Rust generation review, batch 12

Positions 166–180 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections. One new static hold. Total 729 unique
outside-sample inspections, 401 additive plus historical three = 404 holds.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 166 | 0197 | Exact API; byte-index delimiter scanning, exact unknown text, literal nonrecursive replacements and no partial error output. No new hold. |
| 167 | 0198 | Exact API; checked shape before slicing/sortedness, backward merge picks incoming on equality to retain left-first stability, constant auxiliary space. No new hold. |
| 168 | 0193 | Exact API, strict unsigned decimal, physical line enumeration, wide coordinate intermediate and checked unsigned absolute sum. No new hold. |
| 169 | 0199 | Exact API; candidate buffer makes oversize feed transactional, partial data retained, retryable finish and permanent closure. No new hold. |
| 170 | 0201 | Exact API, Unicode trim before interior line checks, delimiter restrictions and independently owned repeated output. Small formatting task nontriviality unresolved. No new hold. |
| 171 | 0203 | Exact API, owned union keys, one wide signed delta per key and sorted output. Small mapping task nontriviality unresolved. No new hold. |
| 172 | 0204 | Exact API; declared validation order before replacement, checked revision boundary, trimmed title and owned receipt. No new hold. |
| 173 | 0200 | Static hold: stated exact formula contradicts zero-stock consumption semantics and the original test. |
| 174 | 0205 | Exact API; parse before write lock, owned payloads and sorted IDs, poison mapped. Full maximum-entry resource envelope and poison injection not newly executed. No new hold. |
| 175 | 0206 | Exact API, page bounds, omitted empty cursor, uppercase UTF-8 hex and exact sort tokens. Small formatting task nontriviality unresolved. No new hold. |
| 176 | 0207 | Exact API, private constant 200-byte pair table, range and complete-size checks before writes, no allocation and preserved suffix. No new hold. |
| 177 | 0208 | Exact API and unchanged unsupported category payload. Two-value mapping task nontriviality unresolved. No new hold. |
| 178 | 0209 | Exact API, iterative checked factorial returns before factor can overflow, including MAX input. Small arithmetic task nontriviality unresolved. No new hold. |
| 179 | 0210 | Exact API, press snapshots, insert preserves drag, matching releases, wide deltas and final saturation/clamping. Button 2 does not start or replace a drag. No new hold. |
| 180 | 0211 | Exact API, monotone index stack, equal-height width retained and final flush. Very large slice area/output representability envelope unresolved, not newly executed. No new hold. |

0200 static contract/test comparison: the prompt says possible "exactly when"
`before < (step + 1) * max_per_step && through > step`. Original test
`zero_stock_categories_are_never_consumable` uses stock `[0,2,0]`, category 2,
step 1, max_per_step 5, expecting false. Here before=through=2, so both specified
inequalities hold (2<10 and 2>1). The reference adds a zero-stock exclusion,
consistent with consumption prose but inconsistent with the exact formula.
This is an internally inconsistent training contract, not an allegation that
consuming an empty category should succeed. No new runtime failure claimed.

Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
No new sandbox execution in this batch. Scope v6 and frozen artifacts unchanged.
No-hold is not admission approval. GCS verified through 403 holds / Rust batch 11 /
714 inspections; this batch awaits backup. Continue position 181.
No new VM, training seal or revised partition.
