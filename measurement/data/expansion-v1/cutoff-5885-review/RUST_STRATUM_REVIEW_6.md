# Rust generation review, batch 6

Positions 76–90 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections. Three new holds. Total 639 unique
outside-sample inspections, 388 additive plus historical three = 391 holds.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 76 | 0086 | Exact API, fixed eight-byte big-endian frame, append-only and immutable message. Small encoding exercise; nontriviality unresolved. No new hold. |
| 77 | 0087 | Hold: cfg outer attribute disables struct but leaves an unconditional impl referencing the absent type. |
| 78 | 0088 | Exact API, fallible reservation, owned vector and exclusive mutable slice, fixed-length fill. Small allocation wrapper; nontriviality unresolved. No new hold. |
| 79 | 0090 | Exact API and independent masks preserve all other u32 bits. Small bit-field wrapper; nontriviality unresolved. No new hold. |
| 80 | 0089 | Explicit API, namespace validation, Arc replacement, per-index ordered thread results. Original tests exercise actual concurrent handler calls. Unbounded one-thread-per-input resource envelope not separately executed or adjudicated. No new hold. |
| 81 | 0091 | Explicit API, whole-input scan after first hit, exact ID comparison, trimmed owned fields. Multiple simultaneous errors have no explicit precedence. No new hold. |
| 82 | 0092 | Hold: matched hyphenated delimiter rejected by an unstated ASCII-alphanumeric/underscore restriction. |
| 83 | 0093 | Explicit API, first equals split, duplicate unknown-key rejection, complete record validation and owned values. No new hold. |
| 84 | 0094 | Exact methods/traits, manual Default preserves root invariant, layer-local set, reverse lookup, deep clones. No new hold. |
| 85 | 0095 | Explicit callback API, conditional single invocation, ordered normalization and stable exact deduplication of owned strings. No new hold. |
| 86 | 0096 | Explicit API, checked arithmetic and exact arity. Prose trailing-whitespace preservation sits uneasily with initial whole-command trim; original tests choose trim first. No contradictory oracle imposed; no new hold. |
| 87 | 0098 | Explicit method signatures and handle variants; checked single-count changes and uniqueness without summation overflow. Private count exhaustion not injected. No new hold. |
| 88 | 0099 | Hold: sorting nested scope/tag components is not sorting full scope::tag strings. |
| 89 | 0100 | Public data/function contract, clone-before-commit atomicity and first-invalid-patch indexing. Test chooses within-patch error priority not explicitly stated; not separately adjudicated. No new hold. |
| 90 | 0101 | Named fields and typed methods, exact stored strings, lookup-before-replacement validation, atomic revise and owned sorted output. Field types partly inferred from method signatures; no new hold. |

Executed evidence, all in the pinned network-disabled/resource-limited Rust
sandbox, no timeouts:

- 0087 `record-macro-cfg-result.json`: valid `#[cfg(any())]` outer attribute
  disables a record. Compilation fails E0412 because emitted impl still names
  DisabledRecord. Exit [1], 602 ms; test executable was not run. A second enabled
  record supplies the test. Prompt allows zero or more outer attributes; original
  tests cover derives only.
- 0092 `tagged-field-hyphen-result.json`: `[item-name]exact text[/item-name]`
  has matched, nonnested delimiters beginning with an ASCII letter, but returns
  Malformed instead of exact text. Prompt specifies no subsequent name alphabet.
  Compiled then assertion failed [0,101], 1442 ms.
- 0099 `scoped-tag-lexicographic-result.json`: scopes `a` and `a0`, each tag `x`,
  return `[a::x,a0::x]`, whereas complete strings sort `[a0::x,a::x]` because
  `0` precedes `:`. Compiled then assertion failed [0,101], 1626 ms. Original
  tests use scopes whose component and qualified-string orders agree.

No-hold is not admission approval. Frozen artifacts and scope v6 unchanged.
GCS verified through 387 holds / Rust batch 4 / 609 inspections; batches 5–6
await backup. Continue position 91. No new VM, training seal or revised partition.
