# JavaScript retained semantic adjudication — 2026-09-08

Two full prompt/reference/original-test rereads. **One scoped-positive, one static hold; zero pending, zero new unique coverage, zero candidate executions.** No central/cloud changes. Prior C/J positives remain criterion-specific and are not overwritten by this independent semantic finding.

Source: `datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl`, SHA256 `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`. Prior evidence: `ARRAY_STRATUM_REVIEW_5.md`, `_9.md`, `FINAL_DELTA_JAVASCRIPT_1_20260908.md` positions15/42.

| Candidate ID | Disposition | Precise basis |
| --- | --- | --- |
| exp-v1-javascript-generation-0047 | Static semantic hold | Unrestricted nonempty string title words must capitalize their first character. Reference splits a supplementary cased character into UTF-16 halves before uppercasing, so it cannot capitalize that character. The prompt does not prescribe charAt or limit its input to BMP/ASCII. |
| exp-v1-javascript-generation-0103 | Scoped-positive | The href expression explicitly requires encodeURIComponent(code). Its native lone-surrogate error behavior is not overridden by a promise to repair malformed UTF-16, suppress URIError or skip otherwise string-valued records. No custom total URI encoder is implied. |

## generation0047: valid supplementary character, not malformed-string speculation

Use a plain profile with imageUrl='i', biographyUrl='b', archiveUrl='a', topic='topic', and displayName consisting of the one character U+10428 DESERET SMALL LETTER LONG I (`\u{10428}`, UTF-16 `\uD801\uDC28`). This is a valid, nonempty Unicode string with no surrounding whitespace. Its uppercase/titlecase counterpart is U+10400 (`\uD801\uDC00`), as explicitly recorded in [UnicodeData](https://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt).

Reference `word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()` operates first on high surrogate D801 alone, then low surrogate DC28 alone. Neither half has a case mapping, so concatenation retains U+10428 instead of producing U+10400. [ECMAScript charAt](https://tc39.es/ecma262/multipage/text-processing.html#sec-string.prototype.charat) returns a code-unit substring, explaining the split. This is a static source/specification deduction, not an executed witness.

The original tests use ASCII names/topics and do not expose this defect. They do not explicitly demand the incorrect Unicode output, so classify the finding as an algorithmic Unicode capitalization defect, **not** reference accommodation to an incorrect test. It also does not involve dropped property descriptors: required fields are explicitly read and reconstructed. No grapheme segmentation, locale-sensitive casing or normalization requirement is needed for this single scalar witness.

## generation0103: exact named native function controls the exceptional domain

Reference trims required code/label/summary/section fields, uses Map/Set for section grouping and first-valid-code retention, explicitly constructs entry fields, and forms href using precisely the named encodeURIComponent call. The prompt's ignore rule covers nonobjects, nonstring properties and strings empty after trimming. It does not add malformed-Unicode recovery. A lone surrogate would reach the explicitly required native encoder, whose Encode operation throws URIError for an unpaired surrogate; that is not evidence of a custom guarantee violation. See [ECMAScript encodeURIComponent and Encode](https://tc39.es/ecma262/multipage/global-object.html#sec-encodeuricomponent-uricomponent).

Neither UTF-16 sort order nor the instruction to return menu sections silently replaces the explicit encoder with a total replacement-character encoder. The original URI example and snapshot tests agree with the specified operation. Close this retained semantic caveat; do not add a surrogate-input hold or a new URI review lane.

## Criterion-to-stratum accounting recommendation

The0047 defect is distinct from every existing v14 named group: Java Unicode blank validation is a different language/operation; C is required-property copying; J is incorrect-test accommodation. If integrating this adverse semantic mechanism into the systematic scope ledger, use a narrowly named mechanism such as `javascript_supplementary_character_capitalization` and attach the **observed** stratum only:

- lane:javascript
- source:Multilingual-Multimodal-NLP/McEval-Instruct
- task_type:generation
- rejection_history:first_pass

That stratum contains273 original inventory records; this is membership accounting, **not273 demonstrated failures or273 newly required full reads**. No evidence here justifies adding corrected generations, repairs, another language, all Unicode operations, or all URI users. Main should first reconcile existing per-ID casing evidence and any actual implementation/contract matches before assigning narrowly unresolved work. This report does not create a queue or initiate an automatic population re-review.

Proposed additive hold: `exp-v1-javascript-generation-0047`, semantic supplementary-character capitalization. Generation0103 needs no new criterion-to-stratum expansion. Main owns ledger integration and all remaining admission gates.
