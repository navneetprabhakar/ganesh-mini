# Array-pattern follow-up, batch 3

2026-09-06. Inspected not-in-frozen-sample array-hit positions 31–45 in v1
inventory order. TypeScript generation0026 was already reviewed in the first
targeted batch and is not counted again: **14 new / 54 total unique outside-
sample targeted inspections**, plus unchanged frozen 300. This is scoped
contract/reference/original-test review, not full seven-criterion approval.

## Reproduced holds

All six diagnostics exited `[1]` with no timeout in the unchanged pinned JS
sandbox. None is a host execution or a reconstructed metric.

| ID suffix (JavaScript) | Finding | Result file | ms |
| --- | --- | --- | ---: |
| repair-0015 | unreachable module's sparse imports bypass whole-graph validation | module-unused-sparse-result.json | 404 |
| generation-0030 | sparse names become Step: undefined instead of rejecting | steps-sparse-result.json | 384 |
| repair-0017 | MAX_VALUE * 2 * 0 returns NaN instead of zero volume | prism-zero-overflow-result.json | 364 |
| repair-0019 | single sparse requested ID passes some plus Set uniqueness validation | replies-sparse-result.json | 461 |
| generation-0025 | own non-enumerable assetId patch bypasses explicit immutable-key rejection | asset-hidden-id-result.json | 340 |
| generation-0034 | both sparse categories and sparse review tokens are accepted | glossary-sparse-result.json | 369 |

The module probe deliberately uses an unreachable, non-side-effect node; if
visited, its malformed imports could cause an incidental TypeError. The prompt
requires validating the whole graph. The prism probe has only accepted finite,
nonnegative inputs and an exactly representable zero result. Intermediate
overflow, not input infinity, causes the failure. The asset probe uses an own
data property with enumerable=false, not a getter/proxy: the prompt forbids
attempts to patch assetId without limiting that rule to enumerable properties.
The glossary probe executes both checks and reports both failures, avoiding
an early assertion that would hide the second case. Original tests omit these
inputs. This batch adds six holds, **75 additive / 78 including historical three**.

## Scoped negative findings and open interpretation

- JavaScript generation0019 ScreenFlow: exact-key helper's every operates on
  a fixed dense key list; outer for-of rejects sparse definitions. Snapshots
  freshly copy nested header state, and navigation records even same-screen
  transitions. No sparse acceptance found.
- JavaScript generation0021 WorkshopRegistry: initial hosts are validated by
  for-of; list maps private push-built storage. Host/newHost shape and atomic
  commit logic are explicit. Closed-key requirements on initial hosts and the
  outer workshop are stronger than clearly stated prose; retain for API clarity
  review, not an automatically inferred sparse defect.
- JavaScript repair0014 connection options: Reflect.ownKeys returns a dense
  array and catches symbols/non-enumerables; own Boolean fields determine
  precedence. The reference restricts plain objects to Object.prototype;
  whether null-prototype objects count as plain needs explicit contract wording.
- JavaScript generation0027 settleTasks: Array.from and Promise.all create dense
  bounded arrays (at most 1000). Output ordering/copying is sound for that path.
  Fake microtask workload and redundant sort are non-triviality/idiom questions.
- TypeScript generation0025 ProgressLedger: for-of validates names into a fresh
  dense array, values are bounded [0,100], frozen snapshots are allocated per
  call. No array callback defect established.
- TypeScript repair0017 packAligned: prompt validates width/fill but does not
  specify malformed frame-array handling; do not invent a sparse-rejection
  requirement. Padding correction handles aligned and empty real frames.
  Huge-output allocation limits remain an unspecified resource envelope.
- TypeScript generation0029 registerLocker: draft validation/messages and
  copying are defined, but malformed preexisting profile validation is not.
  No sparse rejection requirement invented for that profile. Exact supporting
  interfaces/messages are incompletely stated; preserve the API-clarity concern.
- TypeScript generation0030 MemoryRouteRegistry: callback runs over a literal
  dense list of four fields; the constructor iterates records with for-of.
  Sparse record throws incidentally before field validation. The malformed-
  record error-type boundary is not cleared by this review; no acceptance hold.
- TypeScript generation0026 ArchiveService: already held and runtime-confirmed;
  referenced here without duplicate inspection/hold count.

Continue at `exp-v1-javascript-generation-0035`, array-hit position 46. Numeric,
API and non-triviality work remains open. No candidate rewrites, new partition,
training seal, generation restart or new VM.
