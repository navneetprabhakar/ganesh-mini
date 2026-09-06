# Array-pattern follow-up, batch 1

2026-09-06. Fifteen new outside-sample contract/reference/test inspections,
selected as the first 15 not-in-sample array-callback hits in immutable v1
inventory order. This is targeted review, not an unbiased sample or full
seven-criterion approval. Combined with the first targeted batch, 25 unique
outside-sample records have been inspected for specific issues; frozen sample
still 300. No candidates, original tests or partitions were edited.

## Reproduced findings

Nine sparse-validation defects and one read-API validation gap are separate
holds. All probes ran in the pinned sandbox, with no timeout. JavaScript
failures exited `[1]`; TypeScript failures compiled then exited `[0,0,1]`.

| ID suffix | Finding | Result file | ms |
| --- | --- | --- | ---: |
| javascript-generation-0001 | A valid first account plus trailing hole is credited without validating the entire array; early findIndex success masks hole | ledger-sparse-result.json | 354 |
| javascript-generation-0003 | replace accepts sparse schedule instead of TypeError | runsheet-sparse-result.json | 381 |
| javascript-generation-0005 | sparse units resolve successfully instead of rejecting malformed registry input | deployment-sparse-result.json | 527 |
| javascript-repair-0001 | sparse text runs bypass record validation | text-runs-sparse-result.json | 353 |
| javascript-repair-0003 | sparse requested slugs bypass validation | build-pages-sparse-result.json | 354 |
| typescript-repair-0003 | recipients/publish accept empty topic despite global non-empty ID requirement | topic-empty-id-probe-result.json | 2489 |
| typescript-generation-0012 | one sparse star passes map and Set-size uniqueness checks and enters store | constellation-sparse-result.json | 2932 |
| javascript-generation-0011 | sparse article paragraphs bypass every validation | knowledge-sparse-result.json | 466 |
| javascript-generation-0009 | sparse ledger returns status 200 and sparse snapshots instead of malformed-state 400/empty | defect-sparse-result.json | 543 |
| javascript-generation-0012 | sparse catalog returns 200 instead of 400/empty catalog | catalog-sparse-result.json | 442 |

The original dense-input tests cover ordinary values, errors and aliasing but
omit these holes. For ledger 0001, a hole-only input can accidentally throw a
TypeError in findIndex; that does not establish validation of all inputs. The
probe uses a valid matching first entry, avoiding that accidental protection.
Deployment 0005's sparse locations may fail during Map construction, but sparse
units bypass validation and resolve. These distinctions prevent misleading
pattern-wide assertions. TopicRegistry's Map/Set arrays are dense and safe;
its separate hold concerns global ID rules, not array handling.

## Scoped negative findings

- TypeScript generation-0002 ChunkTransferQueue: filter/map consume a spread
  of an internal Map. No externally supplied array holes reach these callbacks.
  Constructor iterates files directly. Ordinary chunk/state transitions and
  copies are covered. Exact numeric progress beyond safe integers remains a
  separate unproved envelope question; no sparse hold inferred.
- TypeScript repair-0001 normalizeRows: shallow-copy contract explicitly excludes
  nested values and symbol properties. No validation requirement supports
  automatically rejecting sparse input here. Keep its non-triviality concern
  separate: repair is replacing identity map with object spread.
- TypeScript generation-0007 pageDirectory: for-of validates entries before
  filter/map. `directory-sparse-control-result.json` **passed `[0,0,0]`**, no
  timeout, 2619 ms. This is a behavioral negative control, not global approval.
- TypeScript generation-0008 BookmarkStore: array is private, populated by
  validated push and compacted with splice; filter/sort/map operate on dense
  storage. Returned records are copied. No array-pattern defect established.
- TypeScript repair-0005 parseRoute: split produces a dense string array;
  some correctly rejects empty and dot segments. Literal percent sequences
  remain strings as specified; URL decoding is not required. No sparse hold.

This batch adds ten holds: total **60 additive / 63 including historical three**.
It postdates the verified 53-hold GCS archive. Review continues at inventory
array-hit `exp-v1-javascript-repair-0008`; do not repeat these 15. Original
quality sample and v1 scope remain unchanged. No training seal or new VM.
