# R3 JavaScript B independent static recovery review — 2026-09-08

Scope: exactly generation 0221, 0296, 0339, 0394. Complete derived prompts, references, independent test files and supplied mutants were read against their approved r3 plan entries. No generated code was executed; main owns sandbox diagnostics and admission. This adds zero original unique-row review credit and changes no original hold, candidate or central ledger.

## Dispositions

| Derived candidate suffix | Static recovery disposition | Basis |
| --- | --- | --- |
| 0221 | HOLD: missing defect qualification | Reference fixes length-based text validation, but tests never create/update whitespace-only text. Supplied trim-based mutant is not distinguished. |
| 0296 | HOLD: invalid oracle, absent intended witness, required-data loss | Tests impose out-of-domain JSON validation, omit own `__proto__` regression, and clone still drops a non-enumerable required `id`. |
| 0339 | HOLD: missing defect qualification | Required-handler validation is corrected, but tests omit missing/undefined handler cases; supplied shared-validation mutant is not distinguished. |
| 0394 | STATIC POSITIVE, execution-qualified admission still separate | `Reflect.ownKeys` validates hidden/symbol patch keys before absence; tests directly exercise both defect classes and allowed hidden quantity. |

Totals: four fully read derived rows, one static positive, three holds. These are recovery dispositions, not new original-parent holds or executed pass/fail claims.

## Seven-criterion assessment

1. **Prompt clarity:** 0221 defines routing, ID accounting and snapshot semantics; 0339 defines Set-style registration identity and snapshot publication; 0394 explicitly limits own patch properties and orders validation before absence. These are sufficient for their corrections. 0296 is expressly bounded to acyclic JSON-compatible remaining data; it does not promise arbitrary-value/cycle rejection, and must not acquire that guarantee through an oracle. Required string `id` has no enumerable-only restriction.
2. **API consistency:** 0221 and 0339 references implement their documented corrections without changing API. 0394 correctly checks all own patch keys, handles allowed non-enumerable fields through own-property checks, and copies named record fields. 0296 fixes dangerous-key assignment through data-property definitions but still loses a valid required hidden `id`, detailed below.
3. **Independent tests and valid oracles:** request separation is preserved: independent test author sees IDs/specifications only, not references, mutants, source tests or architect context. This establishes provenance, not adequacy. 0221/0339 miss the precise intended regression. 0296 adds unsupported exception requirements and misses the intended regression. 0394 contains relevant valid defect oracles; no unsupported descriptor/prototype or arbitrary Unicode requirement is imposed.
4. **Entire-target nontriviality:** all four remain substantive interacting stateful APIs, not padding or fixed-template elementary tasks: dispatcher routing/error precedence/ownership, recursive repository isolation and stable replacement, subscription mutation snapshots/identity/error propagation, and catalog validation/normalization/ordering/copying. A small corrective patch does not negate whole-target complexity.
5. **Idiomatic implementation:** closure state, Map/Set, explicit record copies and standard property APIs are suitable here. 0296's recursive data-property construction is appropriate for dangerous JSON keys but its required-field omission prevents unqualified correctness. Do not demand private-field syntax solely because 0394 uses conventionally internal `_records`; public methods return copies as specified.
6. **Dependency isolation:** CommonJS implementations and `node:assert` tests need no external package, framework, network, filesystem service or nondeterministic external fixture.
7. **Realistic known-bad failure:** all supplied bugs are plausible semantic defects. Only 0394 currently has a direct valid test distinguishing its supplied mutant. The other three must not gain this credit from missing tests or unsupported oracles. Actual sandbox qualification remains main's responsibility.

## Individual analysis

### 0221 — task dispatcher

Approved reference-fix removes trimming from POST/PUT validation while retaining exact routing, missing-item handling before PUT body validation, per-instance counters, no failed-create ID consumption and detached responses. The reference uses `body.text.length === 0`, copies returned item fields, and never retains caller request/body objects. This is a scoped-positive correction.

The complete test file uses ordinary texts such as `first`, `second`, `updated` and `own`, plus empty/non-string invalid bodies. It never submits a whitespace-only nonempty POST or PUT text. Its supplied mutant rejects exactly those texts using `.trim() === ''`; other relevant behavior remains observationally equivalent on these fixtures. Therefore the expected static result is no legitimate mutant rejection, not an executed result.

Required bounded correction: independently authored POST and PUT cases with nonempty whitespace, asserting exact preserved text, snapshots and ID accounting. Do not trim the expected text or reject it. Reference correction is otherwise positive; test qualification is not.

### 0296 — profile repository

Approved scope is safe own-key recursive cloning of acyclic JSON-compatible data, including literal JSON `__proto__`, `constructor` and `prototype`. `Object.defineProperty` now creates ordinary copied data properties instead of triggering the legacy prototype setter. This addresses that defect in the reference.

However, independent tests demand `TypeError` for a cyclic profile, `undefined`/function remaining values, and a replacement containing a Symbol value. These are outside the promised JSON-compatible domain and approved plan explicitly forbids expanding cycle/arbitrary-serializer semantics. The reference would recurse on a cycle and otherwise return these unsupported scalar values; those observations do not establish an in-domain defect. Remove these invalid oracles in a separately versioned correction, rather than enlarging the reference to satisfy them. The complete test file contains no own `__proto__` preservation/isolation regression, so its failures cannot qualify the intended mutant.

Separate concrete in-domain required-data problem: create a plain object with `Object.defineProperty(profile, 'id', {value: 'p', enumerable: false})` and otherwise ordinary JSON-compatible fields. Validation accepts its required nonempty string ID and the Map indexes by `p`; `clone` uses only `Object.keys`, so stored and returned copies lack `id`. `get('p')`/`list()` therefore cannot return the specified profile. This is not a demand to preserve descriptors, prototypes or arbitrary non-JSON objects. The required ID value itself must survive, independently of descriptor form. It remains a reference/API hold, not silently waived by the prototype-key fix.

Bounded correction needs an approved semantic decision preserving required ID data (or an explicitly approved enumerable-only input clarification, not silently inferred), plus independent root/nested JSON dangerous-key tests across initialization/get/list/replace with post-return mutation proving isolation. Keep duplicate-ID, matching replacement ID and stable-position behavior. Do not require cycle handling outside the domain.

### 0339 — signal hub

Splitting topic validation from required-handler validation correctly makes omitted/undefined handlers invalid for both `on` and `off`, while allowing arbitrary or omitted publication payload. Set insertion preserves same-function idempotence and registration order; copying the Set before invocation preserves the current publication under add/remove, and immediate exceptions propagate naturally.

Tests cover invalid topics, handlers `[null, {}, 'fn', 1]`, idempotence, payload identity, off Boolean/unsubscribe behavior, mutation snapshots, immediate exception propagation and independent hubs. They never call `on(topic)`/`off(topic)` or explicitly undefined handlers. The supplied mutant's permissive undefined branch therefore has no distinguishing test. Scope-positive reference, qualification hold.

Required bounded correction: omitted and explicit undefined handler cases for both methods, verifying no invalid registration remains and ordinary publication still works; include omitted payload publication to avoid incorrectly treating that as a handler requirement. No change to Set identity semantics is warranted.

### 0394 — parts catalog

Reference iterates `Reflect.ownKeys(patch)`, rejecting symbols and unknown hidden strings before lookup; validates allowed own values before lookup; inherited extras are not consulted. Allowed hidden quantity/description participate through `hasOwnProperty`, not enumerability. Updates allocate explicit field copies without reordering Map entries.

Independent tests construct a hidden allowed quantity, an unknown symbol, and an unknown non-enumerable `extra`. The latter two must throw for an existing SKU. The supplied `Object.keys` mutant would accept both and thus fails a legitimate assertion. Existing tests also cover invalid quantity on absent SKU, normalized duplicate SKUs, case sensitivity, insertion order, empty patch and detached snapshots. Full reference inspection establishes the same unknown-own-key rejection for absent SKUs; missing additional cross-product tests do not erase a valid direct witness or require rejecting this row. Hidden description, malformed hidden-field atomicity, and unknown hidden/symbol keys on absent SKU are useful bounded additions, not a newly invented oracle gate. Static positive, subject to actual sandbox results.

## Immutable bindings

All paths below are relative to repository root. Candidate directory is `datasets/cache/expansion-v1/versioned-recovery/r3/`; each filename is `exp-v1-recovery-r3-javascript-generation-NNNN.candidate.json`. Canonical hashes use sorted compact JSON, UTF-8, `ensure_ascii=False`, `allow_nan=False`; file hashes are exact bytes.

| Suffix | Parent canonical SHA-256 | Derived canonical SHA-256 | Derived file SHA-256 |
| --- | --- | --- | --- |
| 0221 | 94f0a2708bfdae7d8c51403d29d8db63d40262c2364e30da8f5956ac3ecd5e15 | 5492f1d76e7d14022cd32affcf84fa96ff4ef5947ebce30e7d5d932f27ee9f81 | 51407d618c94715d7f8778489215e1cc1720680bc231affb8edffe93c644a4f4 |
| 0296 | 2b3d0af804fe14c3bc0948b50fd0d3b6c86303a9ce922204e4eb4804a7e454b2 | 99f6276aaa35ae0f0531bc840f61ab6c4776b4fed58154a5e191f940bcf53614 | 24e76760edb2950b89644ebeb7b638d51fd43157b1d9257747c3abdf9d53a7c1 |
| 0339 | f5a8f4c167fb310ec01e944aad20045f9ddabc074d77d318ba0bff5d161c8a3c | adcb74a5117dd285ea01c16e1050ec88e600d3bd1ff5acd3ac5f8deb6fc74e2b | 41ae9a432d206c0ff4707b934780bc1281340f4b4e000002436fc30e380b85ea |
| 0394 | 79a01f3d92235f6fb81a627bc8b3d19d2010f653919dc55d05c814ef4ab44a91 | c2d69c52c91f9a44cfa54b7ae71f6b6a1c24392c60474345b5d5034a0edaebc5 | 9ef36e37d4ff462649bc0957cbe8f01f5657242c7e03377a7cffc6f52faaa387 |

Plan file SHA-256: `cbad9d14a504531e749b5eb3433f0bf4670e21f2a8e8d5f310d2e843e53c6231`.

Architect evidence file `javascript-recovery-architect-evidence.json`: `4b5665badbbbcb29e6ef27ddf0b4b3e659c02fdbdbdba943a3ba83c054ae165e`.

Independent evidence file `javascript-recovery-independent-tests-evidence.json`: `8acfbb37aa9866dcedf238951491154ae1271fadb9484c1b049c57ff952e0719`.

Both recorded evidence requests have matching prompt hashes, return code zero, no timeout, no event parse error and no recorded disallowed tool item types. These are authoring evidence checks, not candidate execution.

Approved selection note: `measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_TRANCHE_JS_TS_20_20260908.md`, SHA-256 `029d28f88e1b4923dcc5ca64e84bafb9c08c0031ff631750bba9c672445261f9`. Parent hold bindings in the approved plan respectively name `FINAL_DELTA_JAVASCRIPT_2_20260908.md`, `profile-json-key-result.json`, `hub-missing-handler-result.json`, and `parts-hidden-patch-result.json` within the same review directory.

All four retain the authorized McEval-Instruct source/revision `57bd46727e49ac3e2890218a146d35c2454a8496`, CC-BY-SA-4.0 attribution and rights flags, with transformation lineage naming the immutable parent and canonical hash. This review does not reopen rights approval or certify downstream license packaging.
