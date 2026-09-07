# Prior Java pagination decisions — 2026-09-07

Follow-up to executed repair0318 page-end overflow. Frozen candidates unchanged;
this pass grants no new outside-sample inspection count and no admission seal.
Searched all unheld Java prompts for page/pagination/batch/chunk/ceil,
then inspected reference line hits for those terms plus subList/copyOfRange. Keyword
discovery is not proof of universal absence; dispositions below bind the relevant
previous-positive range operations that were reread in full.

| ID suffix | Arithmetic reconciliation |
| --- | --- |
| generation-0269 | Start clamped to match size; start+limit widened before addition. |
| generation-0287 | Source size widened to long before +63 ceiling division. |
| generation-0378 | index*size widened first; startLong+size fits long for all positive int arguments; endpoints clamp to result size. |
| repair-0265 | pageNumber-1 safe after >=1 guard; multiplication and end addition widened; out-of-range returns before narrowing. |
| generation-0583 | Long product and long end addition; explicit beyond-results branch. |
| generation-0716 | Slice count uses 1+(size-1)/sliceSize; validated sliceIndex bounds product, count bounds end. Arithmetic itself is sound. New hold: eager constructor allocation precedes element validation. |
| generation-0408 | One unsigned byte bounds length to255; length+1/+2 safe. |
| repair-0293 | Subtraction-based remaining-length guard proves position+length within stream.length before copying. |
| repair-0499 | Guarded subList(0,limit), no offset+limit sum; also in sample reconciliation. |
| generation-0395 | Selected palindrome range derives from actual array endpoints; also in sample reconciliation. |

Generation0347 iterates supplied page lists; it has no page-offset calculation.
Its int aggregate count is not an executed arbitrary-size nested-list guarantee.
Generation0531 likewise traverses supplied pages and compares result.size to limit
without adding an offset. UI Page/Batch type names, serializer page-size parameter,
transaction batches and chunk encoders are not evidence of pagination arithmetic.
Repair0372/0414 concrete-array envelope caveats are retained in sample-v2.

## New executed hold

`java-generation0716-invalid-virtual-list-result.json`:
`new SliceBook(Collections.nCopies(Integer.MAX_VALUE,null),1)` should reject
the first null element with IllegalArgumentException. Instead ArrayList(size)
throws `OutOfMemoryError: Requested array size exceeds VM limit` before validation.
Input is a compact standard-library repeated-element list, not a huge allocation
or custom subclass. This matches the previously executed generation0313 finding.
Compilation0/runtime1,2589ms, no timeout. Network-disabled pinned Java21 sandbox,
1CPU/512MiB/64pids/60s. Original task, hashes and raw output preserved in receipt.

This is a candidate-requested oversized array, not evidence that the host or
training VM needs more memory. Repair with prevalidation before snapshot allocation
and fresh independent tests; do not rewrite original5885. Total holds2029
(2026 additive+historical3), sample165/135, outside4799. Original unheld ceiling3856.
Cross-lane newer-scope reconciliation remains open.
