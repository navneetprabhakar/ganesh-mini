# JS/TS final contract adjudication — 2026-09-08

## Scope and evidence

Gate 2 expansion-admission quality review. This isolated report resolves exactly the 18 non-Rust/non-property targeted rows delegated from JS_TS_LEGACY_SCOPE_CLOSURE_20260908.md. The other 25 targeted IDs belong to separate reviewers. No central hold/state edits, cloud access, candidate execution, training, or publication occurred.

All 18 complete prompts, references and all test files were freshly read; repair prompts include the complete known-bad source. Five specifically named out-of-group caveats were also fully reread. This is 23 reread IDs (5 repairs, 18 generations), **zero new unique-row coverage**. All findings below are static adjudications, not executed metrics. No bounded execution is required for these decisions.

Candidate source: datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl. SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

Reconciled against the prior per-ID ARRAY/JS_TS notes joined in JS_TS_LEGACY_SCOPE_CLOSURE_20260908.md and SEVEN_CRITERIA_JAVASCRIPT.md / SEVEN_CRITERIA_TYPESCRIPT.md calibration. In particular, missing interfaces and nonempty-to-nonblank narrowing are substantive clarity issues; independent registration semantics must not be imported into explicitly identity-deduplicating APIs. Positives below close only the indicated question, not other gates or admission.

## Exact targeted decisions

A = reference_accommodates_incorrect_test_or_api; J = javascript_reference_test_accommodation; I = subscription_registration_identity; S = sparse_element_validation.

| Candidate ID | Targeted criterion | Disposition | Contract-level rationale |
|---|---|---|---|
| exp-v1-typescript-generation-0029 | A | HOLD | The prompt names MemberProfile and RegistrationResult but does not supply the profile identifier field or result union schema. The reference invents memberId and ok/profile/reason branches, and tests require them. These are not inferable merely from immutable locker registration. Exact error-message wording is not the basis: tests deliberately accept flexible messages. This is a self-contained API/clarity hold, not a claimed execution failure. |
| exp-v1-typescript-generation-0030 | A | HOLD | The prompt names RouteRecord and says every field is a string, but names only id/slug/title and never specifies the required path field. The reference reads, validates and returns path; tests reject numeric path and expect it round-tripped. Hold the missing required API field. The prior sparse malformed-record question need not decide this hold; no forced out-of-type sparse probe was run. |
| exp-v1-typescript-generation-0057 | A | HOLD | CaseRecord and Action are specified, but the other exported exact interfaces are not. Tests require RootState.import.inProgress, RemovalState.pendingId and DetailState.record while the prompt provides behavior rather than those field schemas. Hold missing public interface fields, not mutability of initialState: runtime freezing is not promised and unaffected branches explicitly retain identity. |
| exp-v1-typescript-generation-0087 | A | HOLD | The explicitly supported active update can be lost: a typed patch {active:false} remains a valid Partial<Pick<Account,...>> after Object.defineProperty(patch,"active",{enumerable:false}). Reference update reads displayName directly but merges active only through {...patch}, so a previously active account remains active. This is a static supported-property conflict, not an exotic extra-field requirement. Per-registration watch entries correctly implement independent duplicates and snapshots. Explicit-undefined optional-property policy is unnecessary to this finding. |
| exp-v1-typescript-generation-0169 | A | HOLD | CustomerSummary is requested without the id field/type or customer-validity rules. Reference requires string-or-finite-number id and tests use id; prose only establishes reference syntax/name trimming and invalid-customer rejection. Hold missing customer schema and validity domain. Do not hold a particular status discriminant spelling: tests accept alternatives. |
| exp-v1-typescript-generation-0242 | A | HOLD | Prompt gives Avatar an id and Vector2 position and assigns members to Arena. A supplied test instead executes a.members.push(a) on an Avatar. Reference adds unrequested Avatar.members to accommodate that access. A minimal implementation of the stated class API fails that test at TypeScript compilation. Static oracle/API accommodation; the codec identity algorithm itself is not declared broken. |
| exp-v1-typescript-generation-0257 | A | HOLD | The generation prompt requests three interfaces without naming or defining them and does not supply signIn parameter signatures. Reference invents CredentialsVerifier/TokenSink/SignInInput plus two overloads; tests require the four-argument object-verifier form. Hold missing API contract. The overload implementation is not itself alleged invalid. |
| exp-v1-javascript-repair-0005 | J | POSITIVE | Stricter plain-object validation implements the prose requirement rather than merely pleasing a Date-rejection test. Object.prototype and null prototypes are accepted. Call-side headers/params correctly override base entries, including undefined, and fresh map spreads preserve own __proto__ data. The specified nested maps are shallow maps; no arbitrary recursive value-cloning guarantee is inferred. |
| exp-v1-javascript-repair-0008 | J | POSITIVE | The prompt expressly requires elements to be exactly valid records shaped {sensor,value,sequence}; the exact-three-key validation has contract authority, including the extra-field rejection test. Inclusive upper bound, sequence order, copies and Map storage agree. This is not an unjustified test accommodation; no new execution or blanket descriptor-domain guarantee is claimed. |
| exp-v1-javascript-generation-0021 | J | HOLD | The reference require-nonempty helper rejects trim-empty strings for host IDs/names and workshop address, while prose requires nonempty strings and only specifies trimming for workshop-name uniqueness. An initial host {id:" ",name:"Host"} is nonempty under the stated ID rule but is statically rejected. This concrete domain narrowing independently holds the row; exact outer record-key closure need not be presumed from examples. |
| exp-v1-javascript-repair-0014 | J | HOLD | The supplied repair source accepts a null-prototype options object and checks its recognized fields; the correction newly requires Object.prototype exactly. Object.assign(Object.create(null),{insecure:true}) therefore changes from a supported source input to TypeError, rather than receiving the prescribed inverted Boolean. Prose says plain object but does not announce this null-prototype exclusion. Hold the repair-domain/clarity change, not the valid rejection of a custom inherited-prototype object in the test. Tests do not themselves demand null-prototype rejection. |
| exp-v1-javascript-generation-0109 | J | HOLD | Required text fields are described as nonempty strings; reference requireText instead rejects every whitespace-only string using trim(). A whitespace-only emblem is nonempty yet rejected. This is the same concrete nonempty-versus-nonblank domain narrowing as the calibrated sample. Do not base the hold on exact nested output-field spelling: the supplied substring assertions intentionally allow representational flexibility. |
| exp-v1-javascript-generation-0346 | J | HOLD | Emptiness is explicitly trim-based, but the entire contact email-pattern match is not specified as operating on trimmed input. Reference tests the trimmed contact, and the supplied test requires a space-padded email to pass even though whitespace prevents the raw entire string matching the stated pattern. Hold the normalization/test-contract ambiguity; do not silently transfer the emptiness normalization rule to the separate pattern rule. |
| exp-v1-javascript-generation-0391 | J | HOLD | Prompt explicitly asks for an async function. Tests require assert.throws(() => runStages(null)) synchronous validation; a true async function instead returns a rejected Promise. Reference accommodates this using an ordinary function with synchronous validation and an async inner function. Hold the incompatible async API/error contract; no runtime was needed to establish the language-level distinction. |
| exp-v1-typescript-generation-0128 | I | POSITIVE | Repeated registration of the same function is expressly idempotent. The Set is therefore the specified listener identity, not a missing per-call registration. Handles guard repeated invocation; removal and additions change only later snapshot notifications. No independent-generation handle ownership across unsubscribe/re-register cycles is promised. Do not import the distinct independent-registration criterion from other samples. |
| exp-v1-typescript-generation-0232 | I | POSITIVE | The contract specifies subscription order, snapshot membership and idempotent unsubscribe, but does not promise duplicate-function multiplicity or generation-isolated handles. Set registration preserves the order of present listeners; Array.from freezes membership; each handle has an idempotence guard. A first use of a still-unused duplicate handle removing the identity is not a stated violation. Optional initial?: DisplayDensity supports the normal omitted/undefined default convention, not an additional density error hold. |
| exp-v1-typescript-repair-0217 | I | POSITIVE | The supplied API already uses a Set; no instruction changes duplicate identity into independent registrations. Repair makes clear call set(null), preserving snapshots, immediate subscription delivery and idempotent handles. The snapshot promises which subscribers are called, not a frozen primitive across unspecified reentrant callbacks. No fresh duplicate/reentrancy requirement is imposed. |
| exp-v1-javascript-generation-0364 | S | POSITIVE | Arrays may contain holes, but no contract rule requires materializing holes as undefined values or rejecting sparse arrays. forEach visits present elements in index order and validates every returned formatter result. Empty input is explicitly handled; nonempty sparse arrays need not synthesize elements. Callback-driven input mutation shielding is also not promised. Close the speculative sparse policy question without asserting all conceivable array behaviors were tested. |

## Separate exact out-of-membership findings

These are not silently absorbed into the 18 targeted decisions. Three additional hold proposals concern previously surviving rows whose original systematic membership did not include the demonstrated criterion. Two additional fresh reads close earlier caveats; two secondary findings concern already-targeted hold IDs.

| Candidate ID | Disposition | Exact finding and reconciliation |
|---|---|---|
| exp-v1-javascript-generation-0112 | NO ADDITIONAL HOLD | Fresh full read resolves the earlier broad-alias caveat using the specific contract: LOAD_OK and selector explicitly require shallow copies, and RESET explicitly returns the initial object. The no-alias instruction is read consistently as a fresh handled root except for its express RESET exception, not an unannounced deep clone of all shared state. Do not silently claim a deep-alias proof; the concrete previously named RESET contradiction is discharged by its explicit rule. |
| exp-v1-javascript-generation-0113 | ADDITIONAL HOLD | Required own-string-key preservation is broader than own-enumerable value validation. A plain registry with non-enumerable own x=0 and enumerable y=1 passes validation; toggling y spreads away x, contrary to the same-own-string-key requirement. This does not depend on allowing an invalid selected value. Source: JS_TS_RESIDUAL_REVIEW_12.md retained this descriptor question; fresh full read now provides the concrete loss. |
| exp-v1-javascript-generation-0270 | ADDITIONAL HOLD | A valid externally supplied normalized state can have a null-prototype byId dictionary with a non-enumerable engine entry and enumerable wing entry, and order ["engine","wing"]. PIN_PART wing copies with Object.assign, dropping engine instead of preserving the unaffected record and normalized contents. No own-enumerable dictionary restriction is stated. Hold that required-entry loss; arbitrary extra part-field preservation is not needed. Source: JS_TS_RESIDUAL_REVIEW_25.md. |
| exp-v1-javascript-generation-0307 | ADDITIONAL HOLD | The prompt distinguishes non-integers (TypeError) from out-of-range integers (RangeError), yet reference and supplied test require TypeError for pageCount=Number.MAX_SAFE_INTEGER+1. That value is an integer outside the permitted safe range. The exception-class contract and oracle conflict statically. Do not additionally claim an actually exercised refresh-counter exhaustion. Source: JS_TS_RESIDUAL_REVIEW_29.md. |
| exp-v1-javascript-repair-0207 | NO ADDITIONAL HOLD | Fresh full prompt/source/reference/tests explicitly say registers once by identity; Set deduplication is correct. Idempotence guards repeated calls to each handle, not an unstated independent registration generation. Snapshot array plus per-call id/oldId also preserves the explicitly allowed reentrant transition arguments. Callback exception recovery is not specified. The old duplicate-lifecycle/error-handling caveat does not justify a new hold. Source: JS_TS_RESIDUAL_REVIEW_29.md. |
| exp-v1-typescript-generation-0029 | SECONDARY ISSUE; ALREADY TARGETED HOLD | Outside its C membership, copying existing lockers with object spread can drop a non-enumerable required code/label/capacity property even though typed field access and input validity remain valid. This is a separate required-property-copy issue alongside the API-schema hold above, not a second row or extra unique hold. |
| exp-v1-typescript-generation-0087 | SECONDARY ISSUE; ALREADY TARGETED HOLD | The active patch loss above is also a required-property-copy/application defect although the initial systematic memberships did not include C. Record that exact missing membership; do not count the same candidate twice. |

## Counts and proposed integration

| Scope | Rows | Scoped positive / no additional hold | Proposed hold | Unresolved requiring execution |
|---|---:|---:|---:|---:|
| A targeted | 7 | 0 | 7 | 0 |
| J targeted | 7 | 2 | 5 | 0 |
| I targeted | 3 | 3 | 0 | 0 |
| S targeted | 1 | 1 | 0 | 0 |
| Targeted total | 18 | 6 | 12 | 0 |
| Separate freshly read IDs | 5 | 2 | 3 | 0 |
| Unique reread total | 23 | 8 | 15 | 0 |

Proposed targeted hold IDs (12):

- `exp-v1-typescript-generation-0029`
- `exp-v1-typescript-generation-0030`
- `exp-v1-typescript-generation-0057`
- `exp-v1-typescript-generation-0087`
- `exp-v1-typescript-generation-0169`
- `exp-v1-typescript-generation-0242`
- `exp-v1-typescript-generation-0257`
- `exp-v1-javascript-generation-0021`
- `exp-v1-javascript-repair-0014`
- `exp-v1-javascript-generation-0109`
- `exp-v1-javascript-generation-0346`
- `exp-v1-javascript-generation-0391`

Separate additional hold IDs (3):

- `exp-v1-javascript-generation-0113`
- `exp-v1-javascript-generation-0270`
- `exp-v1-javascript-generation-0307`

Main owns validation, exact-ID deduplication against current holds, and integration. The 2 secondary property findings do not add unique IDs. No holding total is changed by this report. Existing other criterion outcomes remain intact; no failed candidate is repaired, removed from provenance, or admitted here.

