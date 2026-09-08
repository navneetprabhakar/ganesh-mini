# Go0386 recovery scope adjudication — 2026-09-08

## Decision

**A narrowly versioned contract-clarification is coherent and recommended for main approval.** Require each required JSON member exactly once, comparing decoded member names case-sensitively. This resolves duplicate-name ambiguity explicitly while fixing the already documented case-folded acceptance. It is not permission to replace the original record, change unrelated semantics or declare admission. No reservation, generation, candidate execution or cloud action was performed; no new original-row review credit.

Full original prompt, reference, tests and known-bad code were read. Existing static evidence establishes the case-matching hold; the old reference uses tagged structs plus DisallowUnknownFields, which does not make field matching case-sensitive. Original tests cover normal ordering, leap dates, empty items, required/unknown/null fields, invalid dates/IDs, trailing JSON and malformed input, but do not settle duplicate member names. The original known-bad reverses item order; it is not a case/duplicate-policy control.

## Proposed precise contract addition

Insert immediately after the existing schema paragraph; preserve the remainder of the original specification and exported API:

> Object member names are compared case-sensitively after JSON string escape decoding. The root object must contain `items` and `next_cursor` exactly once each. Every item object must contain `id`, `name`, and `published` exactly once each. Repeated member names are errors, even if their values are equal; this includes different JSON spellings that decode to the same member name. Member order is unrestricted. JSON-escaped spellings of the required names are valid when their decoded spelling matches exactly and occurs only once.

This means `items` plus `\u0069tems` is a duplicate, a sole `\u0069tems` is valid, and `ITEMS` is unknown rather than an alternative spelling of `items`. Equal-valued duplicates, conflicting duplicates, and null-then-valid duplicates all fail. Duplicate checking is local to each object: `id` in two different items is not a duplicate member, although equal numeric ID values still violate the separate page-wide ID uniqueness rule.

The duplicate rejection is a newly explicit policy of the derived version, **not** a retroactive claim that the original contract already unambiguously selected this policy. Class must therefore be `contract-clarification`, not reference-fix or test-only oracle-rebuild.

## Preserved semantics and limits

- Keep `Release`, `ReleasePage`, `DecodeReleasePage([]byte)`, package solution, standard library and existing Go runtime contract unchanged.
- Root must be an object, items an array of item objects; all required fields retain their existing types. Missing/unknown/null values, malformed JSON and any trailing JSON value fail. Ordinary JSON whitespace before/after the single value remains allowed; object member order remains free.
- ID and cursor retain native Go `int` decoding semantics: JSON integer tokens representable as int, positive IDs, nonnegative cursor. Do not convert via float64, accept integral fraction/exponent spellings that existing int decoding rejects, wrap overflow, narrow to int32 on a 64-bit runtime, or add an arbitrary numeric cap. Native MaxInt should be tested with tiny input; overflow tokens must fail. Negative-zero cursor retains native int decoding behavior rather than acquiring a new spelling prohibition.
- Names remain nonempty strings, not trimmed/nonblank strings. Whitespace-only names are valid; preserve their exact decoded content. Do not introduce normalization or raw-byte/canonical JSON spelling restrictions.
- Dates retain the existing exact YYYY-MM-DD grammar, calendar validity and `time.Parse("2006-01-02", value)` plus exact format-roundtrip semantics; returned time values retain midnight UTC as in the original reference/tests. Do not add timezone suffixes, relax leading zeros, change year handling or impose a new modern-year range. Keep leap-day and impossible-date checks.
- Preserve item array order, unique numeric IDs across the page, explicitly nonnil empty Items, independent decoded values, unmodified caller bytes, and exactly zero ReleasePage on every error. Do not freeze error wording, subtype or which invalidity is reported first.
- This is a strict schema/parser task with interacting token validation, nested required fields, numeric/date rules, identity/order and isolation. The correction must not add padding or unrelated functionality.

## Complete proposed request rationale

Parent `exp-v1-go-generation-0386`; parent canonical SHA-256 `74d38e3539a8ee3765eada0f7313188fb1ff8aa67e84e64c905e526283e065f4`; change class **contract-clarification**.

Create a separate immutable derived version that fixes case-sensitive JSON schema matching and explicitly freezes exactly-once object member handling at the root and each item. Add only the contract paragraph above. Validate decoded member names exactly and reject repetitions before their multiplicity is lost; a map-only parse cannot by itself establish whether repeated members appeared in the raw JSON. The decoder implementation strategy is unrestricted if it enforces these semantics and preserves all original API, native int conversion/range, exact calendar-date parsing, name nonemptiness, null/missing/unknown/trailing rejection, order, zero-error result and storage-isolation rules. Do not accept case variants through struct matching, choose implicit last-value-wins, or silently narrow the valid integer/date/string domain.

Generate independent specification-only tests after freezing the clarified prompt. The independent author must not see reference, known-bad implementation or original source tests. Include canonical and JSON-escaped required-name positives, arbitrary member order, exact-case rejection, equal/conflicting duplicate members at both levels and escaped-name duplicates. Require zero ReleasePage for each error. Retain all substantive original behavior tests and native integer boundary/date cases. A plausible semantic control may accept duplicated required members while otherwise following the clarified contract; its rejection must use a valid duplicate-input oracle, not a compiler error. Independently test exact-case negatives whether or not the chosen control targets that defect. Do not fold multiple intentional bugs into a claimed single-defect control. Bind original ID/hash/source rights and all derived prompt/reference/test/control/output hashes; execute only through the established bounded network-disabled admission sandbox after main approval. No admission until quality and execution both pass.

## Required independent test matrix

| Requirement | Tiny specification-grounded witness |
| --- | --- |
| Exact names | Reject uppercase/mixed-case ITEMS/NEXT_CURSOR and ID/Name/Published individually, with all other fields canonical and valid. Also reject canonical plus case-variant unknown key. |
| Root exactly once | Reject two `items` members and two `next_cursor` members, separately, with equal and differing values. Include null then valid and valid then null. |
| Item exactly once | Reject repeated `id`, `name` and `published` separately with otherwise valid object; include equal and unequal values. Do not confuse repeated member names with page-wide repeated IDs. |
| Decoded-name identity | Reject `items` with `\u0069tems` in the same root, and `id` with `\u0069d` in the same item. Accept sole escaped spelling and reordered members. |
| Scalar domain | MaxInt ID/cursor pass; int overflow, quoted numbers, booleans and fractional/exponent numeric tokens fail under existing int rules. Positive ID/nonnegative cursor unchanged; whitespace-only nonempty name passes unchanged. |
| Dates | Valid leap day and ordered records pass; nonleap February 29, impossible month/day, non-padded dates and timestamp suffixes fail. Preserve original year policy, not a new year>=1 rule. |
| Completion/isolation | Empty array yields nonnil Items; missing/unknown/null/wrong-shape/malformed/trailing values fail with zero page; trailing whitespace allowed; input and decoded strings/slices remain independent. |

No execution is claimed by this proposed matrix. Duplicate-member tests must use literal JSON strings rather than maps that cannot represent duplicate names.

## Exact provenance bindings

- Original corpus: `datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl`; frozen corpus SHA-256 `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
- Candidate ID: `exp-v1-go-generation-0386`, canonical SHA-256 `74d38e3539a8ee3765eada0f7313188fb1ff8aa67e84e64c905e526283e065f4`. Exact JSONL record bytes including newline SHA-256 `92b437eb7ecca8ff904aac5d5b803b2a859f1f370e2eb1a2dd819bef93774f53`.
- Prompt/rendered prompt SHA-256: `7089466188ba5b5e70f5fa5e8b9cedc34057396e91e0ec8b6629aa2bf8dfee92`.
- Reference SHA-256: `b9b8042f07547c4070d6104c93a6825dcadd2011da1942155746b1e995cc8bc6`.
- Original independent test SHA-256: `3b76e611558cff9c92eec5823238c7dd45159ba24721ec5925e933791b0bea3f`.
- Original order-reversal control SHA-256: `c709175ee052c6ea7bb21337789a6e9b99e1509f9c6bc79593279c0b7e0360fa`.
- Hold evidence: `measurement/data/expansion-v1/cutoff-5885-review/GO_NONTRIVIALITY_REVIEW_31.md`, SHA-256 `03179b4ce3250f9973eca3222985da27492f510d6331e5cfe9b6f755dc955f4f`. Its finding is static case-insensitive struct matching, not a new executed duplicate-name probe.
- Prior selection evidence: `measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_TRANCHE_GO_JAVA_20_20260908.md`, SHA-256 `4bf3108660d2e69a2c210b8c9d9e53fbf89431f93c2541b745b70b71dd067a7d`. Its unresolved duplicate-policy decision is resolved provisionally here, pending main approval.
- Source dataset: `Multilingual-Multimodal-NLP/McEval-Instruct`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-16048`, source-record SHA-256 `10182ee6cc22a20f9461469aa57e2c9eeca38f6715ad863e66aa7a7734b2a74b`.
- Source license CC-BY-SA-4.0; source URI `https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct`; license URI `https://creativecommons.org/licenses/by-sa/4.0/`. Candidate rights answer/model_training/prompt/redistribution/tests are all true. Preserve original transformation lineage and attribution; this note does not reopen ownership approval or certify final release packaging.

Canonical record hashing uses sorted compact UTF-8 JSON with ensure_ascii=False and allow_nan=False. Only this isolated scope note was written; main must approve the versioned clarification before creating any new candidate.
