# Python Mapping and enum scope closure — 2026-09-08

Gate 2 bounded follow-up, not admission. Exact-ID join against the 2,721-hold
checkpoint (2,718 additive plus historical three), after Python668 N/E integration.
Only this note and `python-mapping-enum-closure-20260908.json` are new artifacts.
No candidate execution, central changes, cloud activity, or unique-row credit.

## Exact accounting

| Frozen v14 group | Members | Already held | Surviving | Prior outside-sample evidence | Positive sample evidence |
| --- | ---: | ---: | ---: | ---: | ---: |
| python_mapping_contract | 597 | 275 | 322 | 308 | 14 |
| python_invalid_enum_exception | 720 | 347 | 373 | 358 | 15 |

Mapping survivors are a subset of enum-scope survivors. The surviving union is
373 IDs, not 695. All 373 join to prior per-ID evidence: 358 numbered generation
review findings carried by `python-criteria-reconciliation-v1.json`, plus 15
positive sample records in `sample-criteria-reconciliation-v2.json`. No missing
evidence IDs. The exact-ID report binds these rows, candidate hashes, source
evidence and input-file hashes. Its retained-evidence labels are deliberately not
new full-seven-criterion positives; only the listed group memberships apply.

The systematic scopes are strata, not claims that every member accepts Mapping
or Enum input. Source inspection/search was used to identify actual relevant
contracts and retained questions; keyword absence alone is not admission.
Existing per-ID validation/API findings remain controlling where no concrete
unresolved Mapping or invalid-enum question was found. No original hold is lifted.

## Four unresolved Mapping decisions: proposed static holds

Full original prompt, reference and tests were reread for each row below. These
are contract/reference predictions, **not executed failures**. The simple standard
library Mapping examples avoid hostile custom methods and oversized input.

| Candidate ID | Proposed disposition and exact basis |
| --- | --- |
| exp-v1-python-generation-0220 | Mapping HOLD: `DocumentActivator(documents)` accepts a mapping of names to document dictionaries and promises independent stored data. It calls `deepcopy(documents)` directly. A `types.MappingProxyType({'doc': {'sections': ['x']}})` is an ordinary read-only Mapping with ordinary copyable contents; direct deepcopy is predicted to raise TypeError. No dict-only or deepcopy-compatible-wrapper restriction is specified. Snapshotting the mapping contents is feasible. Original tests use dict only; their successful nested copies do not settle wrapper breadth. |
| exp-v1-python-generation-0355 | Mapping/API HOLD: `compile_catalog(batches, schemes)` constrains the inner record `name` to nonempty string, but does not restrict batch mapping keys to strings. The reference adds `isinstance(batch_name, str)` and rejects `{1: [('x', b'a')]}` with TypeError, even though the mapping and record satisfy the stated rules. Expected shape for scheme `sample2` is `{1: {'sample2': {'x': (97,)}}}`. Tests only use string batch keys. Freeze the batch-key restriction explicitly in recovery or preserve valid mapping keys; do not infer it from the identifier `batch_name`. |
| exp-v1-python-generation-0445 | Mapping HOLD: `find_notices` expressly accepts notice mappings. A matching `MappingProxyType` containing required string fields and `published=True` passes structural validation, then reaches `deepcopy(notice)` and is predicted to fail with TypeError. No noncopyable descendants are needed. Normalize the mapping container before copying, or explicitly restrict the contract in recovery. Existing scalar-validation test cases also have extra list wrappers; that coverage weakness remains separate, not the basis for this Mapping hold. |
| exp-v1-python-generation-0517 | Mapping HOLD: `stage_module` describes `cache` and `available` as mappings, preserves their ownership and returns a detached cache that can receive downloaded content. It calls `deepcopy(cache)` without normalizing the mapping. Even an empty `MappingProxyType({})` on the no-match path is predicted to fail; the download path also assumes the copied mapping is mutable. Tests exercise plain dicts only. The contract does not say mutable-input-cache or deepcopy-compatible concrete wrapper. |

Main owns whether to integrate these four proposals and any later bounded
execution. If accepted, Mapping scope becomes 279 held / 318 surviving; the enum
stratum becomes 351 held / 369 surviving because it contains the same four IDs.
The global total would be 2,725 only if the checkpoint is otherwise unchanged.
No new enum-exception hold is proposed.

The exact unresolved scoped ID set from this pass is therefore:
`exp-v1-python-generation-0220`, `exp-v1-python-generation-0355`,
`exp-v1-python-generation-0445`, `exp-v1-python-generation-0517`.
They need a hold/contract decision, not another unspecified blanket rereview.

## Focused closures and retained boundaries

Sixteen full prompt/reference/test rereads were performed: generation
0179, 0211, 0220, 0315, 0316, 0347, 0355, 0445, 0455, 0517, 0562,
0633, 0697, 0700, 0708 and 0723. All had prior inspection credit.

| ID suffix | Narrow disposition |
| --- | --- |
| 0179 | Mapping support uses `collections.abc.Mapping` and constructs independent ordinary containers. Duplicate entries emitted by a malformed custom Mapping are not a new required-domain test. Whether extra state fields are allowed remains a distinct clarity question, not silently cleared here. |
| 0211 | Enum-like sorting options use tuple membership, hence ordinary nonstring/unhashable invalid values do not cause accidental hash TypeError. The explicit ValueError rule for invalid options is more specific than the broad argument-type sentence; independent tests include None options. Do not invent opposite error precedence. |
| 0315 | Real mappings provide callable `.items()`; values/names are validated and copied into an ordinary dict. An object with an unusable `.items` attribute is not thereby an admitted Mapping. No promised generic fake-object error normalization is added. |
| 0316 | Actual Mapping validation plus Enum conversion catches both TypeError and ValueError and emits ordered issues. Prompt specifies enum member names, not literal backing strings; tests use exported members and do not force arbitrary values. Unspecified message text/value spelling is implementation freedom here, not a missing invalid-enum decision. |
| 0347 | Required mappings provide valid `.items()`; detached channel lists are built explicitly. No hostile duck-object normalization guarantee. Tokens containing the separator may never match a first-separator frame, but the grammar does not promise every token is reachable; do not invent escaping. |
| 0455 | Ordinary invalid roles are compared directly and raise PermissionDeniedError without a hash lookup. Unhashable nonstring booking references and custom equality do not establish a missing enum policy. Falsey nonempty dict subclasses remain outside this narrow scope. |
| 0562 | `from_mapping(data: dict)` expressly requires dictionaries, not general Mapping. Property assignment error conventions are explicit, while malformed mapping shapes are rejected and tests allow TypeError or ValueError; no enum criterion applies. Mutable scalar subclasses remain separate. |
| 0633 | Genuine Mapping `.items()`/`.keys()` behavior is supported, fields/flags validated and fresh tuple projections built. A fake `.keys` attribute with invalid protocol behavior is not required input. No remaining scoped malformed-duck-mapping hold. |
| 0697 | Mapping membership validation and `deepcopy(dict(raw))` for metrics handle ordinary read-only mappings; source-call exception wrapping is explicit. No protection against malicious mapping methods is inferred. The prior nonempty-versus-whitespace-only string interpretation is a separate clarity issue and is not adjudicated by Mapping closure. |
| 0700 | `Mapping` validation followed by `deepcopy(dict(config))` normalizes the wrapper before storage, unlike 0220. Arbitrary nested noncopyable objects are not automatically a Mapping defect. |
| 0708 | Records accept Mapping and normalize with `dict(record)` before copying; rules explicitly require dict. Independent tests include UserDict. The broader arbitrary-copy caveat is not a new Mapping narrowing defect. |
| 0723 | Boolean rounds are explicitly invalid; ValueError for that excluded integer-subtype value is supported by original tests. No enum lookup occurs. Do not turn this into a new universal rule that every bool rejection must be TypeError. |

An additional narrow source check found the surviving actual enum definitions in
0038, 0042, 0316, 0646 and 0752: concrete-instance validation, internal state enums,
catching failed conversion, internally assigned phase, and type-guarded rank
conversion respectively. Their prior per-ID evidence remains intact. This is not
an execution claim and does not imply that a textual Enum search exhausts every
string-option contract. For example, prior0007/0059 specifically record type
checks before lookup; those findings are carried rather than reopened by a
generic “other criteria retained” sentence.

## Integration limitations

The exact report closes the **evidence join**, and the review isolates the four
concrete Mapping decisions above. Retaining 369 prior scoped dispositions does
not newly certify copy-hook immunity, recursion capacity, sequence breadth,
Unicode interpretations, error priority outside the specified API, or all tests.
Existing explicit questions in other criteria remain intact. In particular,
0179 extra state fields, 0445 malformed scalar test coverage, and 0697 whitespace
validation were not erased or counted as fresh bulk queues. Main should retain
their exact existing evidence if separately reconciling clarity/test adequacy.

Zero new unique inspections, zero candidate executions, zero central mutations.
Do not train or seal on the strength of this note alone.
