# Recovery r3 JavaScript A static quality review — 2026-09-08

## Decisions

Exactly four generation candidates reviewed: **0025 static quality positive;0137/0212/0219 quality-held for missing intended mutant discrimination.** Their reference corrections are statically consistent with the approved scope. No candidate execution, generation, cloud activity, central edits or admission occurred here. Main owns fresh sandbox measurements. Zero new unique original review credit.

Complete derived prompts, references, test files and known-bad sources were read against all four approved r3 plan entries. The three reference-fix prompts are byte-identical to their immutable parents;0025's contract clarification implements the explicitly approved own-key, hidden-key, symbol and inherited-field distinctions. Parent canonical hashes match the plan; exact IDs and all prompt/reference/mutant/test contents match their architect/independent outputs. Stored content hashes recompute. The independent request supplies specifications and IDs, not implementations or architect context. Both archived evidence streams contain only thread/turn/agent-message events, with no tool execution, and their request/output hashes recompute.

## Individual findings

### exp-v1-recovery-r3-javascript-generation-0025 — positive

Reference uses Reflect.ownKeys for exact asset shape and forbidden patch keys, checks required own fields, ignores inherited patch properties, and reads allowed own fields even when non-enumerable. It retains unpatched strings without trimming, trims supplied strings, distinguishes TypeError from empty-trim RangeError and reconstructs the specified ordered result without input aliases.

The suite tests an all-hidden valid asset, a hidden allowed category, hidden unknown patch key, symbol patch key and symbol asset key, plus inherited-patch no-op, invalid fields, normalization and output order. The Object.keys mutant fails these genuinely required own-key distinctions; notably the all-hidden valid asset is incorrectly rejected. The original hidden assetId witness is not explicitly repeated, but the shared all-own-key defect is meaningfully exercised by hidden/symbol unknown keys and valid hidden asset fields. This is not a mutant-survival gap. The mutant has multiple manifestations of the same enumerable-versus-own mechanism; do not report it as an isolated single assetId-only defect.

Non-triviality is retained for the interacting exact shape, own/inherited visibility, immutable-key rejection, patch-only normalization and atomic copy requirements, not mere field count. No unsupported concrete prototype/descriptor-cloning requirement is imposed by the tests. Static seven-criterion positive pending execution.

### exp-v1-recovery-r3-javascript-generation-0137 — hold: no hidden-state witness

Reference reconstructs changed ticket id/title/details/status and changed root nextId/tickets explicitly, retaining unaffected ticket identities. Frozen initial state, trim-based add validation, positive integer IDs, no-op identity and insertion/ID lifecycle agree with the contract. Specific recognized-action payload TypeError rules govern those actions; generic unknown/malformed fallback is not used to erase them.

Every ticket/state in the independent suite is created by the reducer as ordinary enumerable literals. The mutant spreads existing tickets/roots; it behaves identically on all such cases. No supplied external state hides title/details or nextId. Thus the suite does not distinguish the original required-field-loss defect, despite otherwise strong ordinary lifecycle/identity coverage. This is a test-breadth hold, not a reference correctness hold or a new demand to preserve arbitrary extras.

A specification-grounded distinguishing case supplies a valid external ticket with a non-enumerable required title/details and a valid root with non-enumerable nextId; toggle/delete must preserve required fields and unaffected identities. No prototype pollution, counter exhaustion or deep cloning of unchanged tickets is required.

### exp-v1-recovery-r3-javascript-generation-0212 — hold: ordinary sparse tests miss inherited-hole defect

Reference checks own-index existence before reading values and passes that same captured value to fallback. This satisfies explicit sparse-as-undefined behavior while preserving callback result/error identity, per-index ordering and immediate fallback-error propagation. Every-position processing plus mapper/fallback error boundaries makes the complete target substantive.

The suite's sparse array has holes but no inherited numeric entries. Both raw values[index] and the corrected own-index branch produce undefined there. Dense, ordinary sparse, callback identity and error tests therefore do not distinguish this mutant. A one-hole array with a local Array-derived prototype owning index0 with value7 is the bounded accepted-domain witness: mapper and failing mapper's fallback must receive undefined. Do not globally modify Array.prototype or invent callback-driven length-mutation semantics. No contradictory oracle was identified; the narrow discrimination gap still blocks quality approval.

### exp-v1-recovery-r3-javascript-generation-0219 — hold: whitespace-only failure message absent

Reference now rejects only non-string/zero-length failure messages, preserving nonempty whitespace exactly. It correctly retains the separate trim-based save-start name rule. Every successful transition reconstructs values/saved separately, edits retain saved content, and save/load/error state transitions match the stated API. No extra edit-clears-error or phase restriction is inferred.

Independent tests use a normal failure message and reject empty/numeric messages, but never use a whitespace-only nonempty message. The mutant's trim-empty check consequently behaves identically on every supplied failure test. The previous contradictory whitespace-rejection assertion was not repeated, but absence of a wrong test is not coverage of the recovery. A spaces-only message must enter error phase with the exact message and fresh values/saved copies. This is the required narrow witness, not a new universal string-domain audit.

## Seven-criterion accounting

| Criterion | All four / exceptions |
| --- | --- |
| Prompt clarity | Explicit contracts and approved0025 own-field clarification support scoped positives. |
| API consistency | References match required exports, transitions, type/error and copy policies; no fresh reference defect identified. |
| Test independence | Exact archived specification-only origin verified; independence does not establish behavioral coverage. |
| Non-triviality |0025 own-key/normalization constraints;0137 immutable ticket lifecycle;0212 error/fallback/index interactions;0219 saved-versus-live transition ownership. No elementary padding. |
| Idiomatic implementation | Standard own-key/own-index predicates and explicit required-field reconstruction; no suspicious dependency workaround. |
| Dependency isolation | CommonJS with standard runtime APIs; tests use allowed node:assert, no network/filesystem side effects. |
| Realistic known-bad failure |0025 has direct own-key discrimination.0137/0212/0219 realistic mutants lack their distinguishing input classes: hold. |

Do not relabel expected mutant survival as an infrastructure failure. No further critic job is launched or implicitly authorized by this report. Main can apply the existing bounded correction policy while preserving immutable current artifacts and all failed/undiscriminating evidence.

## SHA-256 bindings

Candidate files are under datasets/cache/expansion-v1/versioned-recovery/r3 and named exp-v1-recovery-r3-javascript-generation-SUFFIX.candidate.json.

| Suffix | Candidate file bytes | Independent test content |
| --- | --- | --- |
|0025 | abda4c6898ba8a8334e0910c2e172616f2570be852f8b6856077e805282a50c0 | 1ff0e4508b235e86ce0ca0a4581bc665751d68c26c1cfd84a3c05bd8371d222a |
|0137 | 487f9fbdf91f87b0a2ac7ff152d9ee58b73e3fee196bcc7b6cf4c23f63fffa78 | 35c282235fa9e2035a39956491a8d58713dca434507f4183c2f42a38774563a2 |
|0212 | 21fe576d43012c044c5ae84e3dfe19c0c409c976eff45eb4291632106f193e95 | bca89137d2d018647b322650faa61f4b1c4e921f5b846e90e17e466a5f992cd6 |
|0219 | 540451e0262d47ed8f0e35ed3d2b83ddd7636e986406e9846faaed72bc2d3724 | bf5860f4e690e66645cec56aa14015d7d02506246ac47a80fc905b68a0ea9597 |

Architect evidence file: `4b5665badbbbcb29e6ef27ddf0b4b3e659c02fdbdbdba943a3ba83c054ae165e`.
Independent-test evidence file: `8acfbb37aa9866dcedf238951491154ae1271fadb9484c1b049c57ff952e0719`.

Both files are javascript-recovery-architect-evidence.json and javascript-recovery-independent-tests-evidence.json in the same r3 directory. Candidate-file hashes bind all complete prompt/reference/mutant/test contents; their embedded individual SHA-256 values were additionally recomputed during review.
