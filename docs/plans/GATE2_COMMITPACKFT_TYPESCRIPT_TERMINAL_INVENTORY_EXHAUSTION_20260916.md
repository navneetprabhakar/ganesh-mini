# Gate 2 CommitPackFT TypeScript terminal inventory exhaustion — 2026-09-16

Status: frozen terminal source-construction contract; no tail queue generated
and no classification launched by this document.

Parent candidate contract: `capability-stratified-v3-repair-delta/v1`

Parent plan SHA-256:
`4023a896300112f9f93f2a16698d549f203e3e75b4e71ae054f3a98463e2f0f0`

## Bound predecessor evidence

- first CommitPackFT contingency addendum file SHA-256:
  `5d1301d7e277f6ea977e6ccc6740a33f877ed0d20cc4a535098b8947c2788049`
- first CommitPackFT policy file SHA-256:
  `7ab381b7a2be66b175a5833450b77489d8b7e91a9feeab54a170fa23e1e4dbb7`
- first CommitPackFT canonical policy seal:
  `d17aa531b9ad1d95b186e544ecf6f68cf2626c79a56fb0ce587a0d2f5d686028`
- v9 terminal aggregate file SHA-256:
  `a3f27f9666c1f07f617c812fe816d811323adc26eccad3b0b7a55a26779cb295`
- v9 terminal aggregate canonical seal:
  `6f1251d3e7db2c09f315b74784f550620fb6fb31f47a35b0ce8570cecf7b7614`
- v9 formal queue-failure file SHA-256:
  `0b1aee312b2ebffbb04e2724e9b70d52748987db9fedf952ade4ebafa345e354`
- v9 formal queue-failure canonical seal:
  `0505bbdf7893e5458fe6c0ca65aca8be992262212a5089c120966dab84d6d47b`

V9 is terminal at the source-construction boundary: 59 of 60 cells have at
least two qualified sources, while `binary_and_bitwise/typescript/repair` has
exactly one. No repair-delta teacher candidate has been generated and no
120-assignment source queue has been sealed.

## Terminal source decision

Consume the complete unclassified tail of the already pinned, licensed, and
content-blindly ordered native TypeScript CommitPackFT inventory. The eligible
inventory contains exactly 4,990 records and is committed by ordered-identity
SHA-256:

`509dfff5178682ca84ed7673eced106e935a7ea4c79ac9bae3097e6a1cce62a1`

The first contract consumed one-based ranks 1–1000. This contract consumes
every remaining one-based rank 1001–4990, exactly 3,990 records. It does not
select for binary/bitwise keywords, classifier outcomes, or any evaluation
property. The same revision, file hash, license allowlist, prohibited-marker
filter, stimulus bounds, ordering seed, lineage fields, and `new_contents`
quarantine remain unchanged.

The builder must reconstruct all 4,990 eligible identities, reproduce the
ordered-inventory hash above, take the exact zero-based half-open slice
`[1000, 4990)`, and fail if any selected identity collides with prior corpus,
v2, the first CommitPack pool, or other cited evidence. Output IDs retain their
global one-based ranks, so the tail is structurally disjoint from ranks 1–1000.

## Immutable concurrent classification waves

For execution speed, the one tail queue is prepartitioned into four disjoint
classifier-selection shards. `run_repair_source_ontology.py` deterministically
re-sorts the provided tail queue by `SHA256("3505" || NUL || lane || NUL ||
queue_id)`, so these offsets are relative to that 3,990-record classifier
ordering, not to the original CommitPack inventory ranks. They are runtime
slices over the same sealed queue, not independently selectable experiments:

1. classifier offset `0`, count `998`;
2. classifier offset `998`, count `998`;
3. classifier offset `1996`, count `998`;
4. classifier offset `2994`, count `996`.

Together these half-open classifier ranges cover `[0, 3990)` exactly once.
The tail queue itself still contains original inventory ranks 1001–4990 in
the content-blind CommitPack ordering.

All four shards must complete terminally. Finding a second source for the
observed missing cell does not permit early stopping. Every record is
classified once against the complete ten-capability ontology. There are no
content retries. The 60 V9 records whose batches produced internally
inconsistent ontology output remain terminal V9 failures and are not replayed
under this contract. Infrastructure-only replay remains limited by the parent
contract and cannot alter source, prompt, model, schema, or runtime bytes.

## Separation, aggregation, and terminality

Before classification, the complete 3,990-record tail must receive its own
content-free exact, normalized, and fuzzy evaluation comparison and sealed
attestation. After all four waves finish, aggregate them with all previously
sealed ontology evidence and run the unchanged global 120-slot matcher over
all 60 repair cells. No new record is forced into the observed missing cell;
global uniqueness, dataset caps, source affinity, and all downstream candidate
gates remain unchanged.

Previously classified lanes and cells are not rerun. Their evidence may be
carried forward only after hashes, prompt bindings, runtime bindings, source
lineage, and separation attestations validate under an explicit carry-forward
report.

This is the final v3 source expansion. No fifth shard, partial tail, new source
dataset, capability-targeted retrieval, early stop, or additional v3 source
extension is allowed. If the completed tail still cannot produce a valid
global 120-source queue, v3 source construction stops and any further attempt
requires a separately frozen v4 contract.

This contract authorizes no teacher generation, model training, GCloud use,
or publication. It records the deterministic local source-construction work;
execution remains separately evidenced and must not be reported until run.
