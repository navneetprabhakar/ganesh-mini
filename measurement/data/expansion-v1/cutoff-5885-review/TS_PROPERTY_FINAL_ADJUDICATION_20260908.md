# TypeScript required-property final adjudication — 2026-09-08

Gate 2. Nine disjoint generation IDs from
`JS_TS_LEGACY_SCOPE_CLOSURE_20260908.md`. Full original prompts, references and
tests read for all nine. Only this isolated note changed; no central holds/state,
candidate execution, cloud operations, or new unique inspection credit.
Static predictions are not executed failures. Scoped positives close the named
property question, not all seven admission criteria.

Source: `datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl`, SHA256
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

## Exact dispositions

| Candidate ID | Property disposition | Prompt/reference/test basis |
| --- | --- | --- |
| exp-v1-typescript-generation-0007 | HOLD | `pageDirectory` reconstructs required id/label explicitly and is sound for this scope. However `omitDirectoryEntry` validates the same public records through ordinary property access, then spreads retained records. A valid retained record with non-enumerable id/label is returned without those required fields. The public DirectoryEntry contract does not restrict required fields to enumerable own properties. Original tests only omit plain literal entries and therefore miss the loss. |
| exp-v1-typescript-generation-0008 | Scoped positive | `add` accepts primitive owner/title/priority arguments, validates them and creates the complete internal Bookmark literal. All later spreads operate on that internally created object, not a caller-supplied record with hidden/inherited required fields. Returned records are detached. Original tests exercise mutations of add/list results and confirm isolation; no requirement to support mutation of private storage is added. |
| exp-v1-typescript-generation-0049 | Scoped positive | All three Feature fields are read directly, trimmed and assigned explicitly into a new literal. Non-enumerable or inherited required values are preserved as sanitized own fields. Tests check every trimmed field, duplicate normalized keys, order and two-way mutation isolation. The earlier sparse-array question is separate and is not a property-copy failure. |
| exp-v1-typescript-generation-0059 | Scoped positive | Constructor input is strings, not public StoredMessage objects. `send` creates an internal literal containing sequence/text; reads spread those literals. Snapshot constructs path/messages explicitly. Original tests check independent arrays/messages and altered sequence/text results. No caller-controlled property descriptor can enter stored message fields through the specified API. |
| exp-v1-typescript-generation-0064 | HOLD | Performance constructor and draft addition reconstruct required fields explicitly, but update uses `{...current, ...patch}`. A valid non-enumerable supplied seat is silently ignored instead of changing that supplied field. Neither the patch type nor prose restricts supplied fields to enumerable-own properties. Original tests only supply literal patches. This witness uses an allowed patch field, not an extra id or ambiguous unknown-property policy. |
| exp-v1-typescript-generation-0066 | Scoped positive | Constructor explicitly reads id, label and optional disabled and constructs a fresh record. Its later spreads copy this internal literal. Hidden/inherited required values survive through ordinary reads; disabled is normalized to a boolean by the specified behavior. Original tests check field copies, ordering, enabled/disabled behavior and returned mutation isolation. No general descriptor/prototype preservation is required. |
| exp-v1-typescript-generation-0078 | HOLD, required enumerable-own presence | The contract defines a valid draft by the three enumerable own keys, with all three present. Reference only uses Object.keys to reject unknown keys, then reads required values without verifying their enumerable-own presence. A plain object with non-enumerable priority is accepted. This is not a demand to preserve arbitrary hidden extras: their exclusion is expressly permitted and the hidden-extra test is correct. It is failure to enforce the explicitly required key set. |
| exp-v1-typescript-generation-0091 | Scoped positive | `add` accepts primitive strings and creates a complete internal key/label literal; get/list spread only internal literals. menuConfig constructs its fixed keys explicitly. Tests verify detached results and exact menu keys. No public input record supplies descriptors or inherited fields. |
| exp-v1-typescript-generation-0094 | Scoped positive | Constructor reads every specified field directly and assigns primitives individually; toObject and parent construct fresh literals. Conditional parent spreads spread newly constructed literals, not the input. Required hidden/inherited values are not dropped, and unknown extras are expressly ignored. Tests verify returned-object isolation and optional parent presence. Direct runtime mutation of TypeScript-readonly instance properties is outside this property-copy adjudication; no new runtime-freezing claim is made. |

## Minimal static witnesses — not executed

These use standard descriptors, ordinary scalar values and small arrays. They do
not require prototype pollution, hostile accessors, custom equality, or casts that
remove the required public fields. `Object.defineProperty` changes only a field's
enumerability, not its existence, type or readable value.

### 0007: removal drops required fields of the retained entry

```ts
const keep = { id: "keep", label: "Keep" };
Object.defineProperty(keep, "id", { enumerable: false });
Object.defineProperty(keep, "label", { enumerable: false });
const result = omitDirectoryEntry(
  [keep, { id: "remove", label: "Remove" }], "remove"
);
// Required: result[0].id === "keep", result[0].label === "Keep".
// Predicted reference: result[0] is {}, both fields undefined.
```

Both fields remain writable primitive string properties. Validation reads them
successfully. Detachment does not permit deleting required return-interface fields.

### 0064: update silently omits a supplied permitted field

```ts
const store = new ReservationStore([{ id: "show", venueId: "venue" }]);
const r = store.add({ customerId: "customer", performanceId: "show", seat: "A1" });
const patch = { seat: "B2" };
Object.defineProperty(patch, "seat", { enumerable: false });
const updated = store.update(r.id, patch);
// Required: updated!.seat === "B2" and store.get(r.id)!.seat === "B2".
// Predicted reference: both remain "A1".
```

The patch structurally satisfies `Partial<Omit<ReservationDraft, "id">>` without
extra keys. This resolves the narrower required-field question independently of
the older extra-id patch caveat.

### 0078: required key is not enumerable-own, but accepted

```ts
const draft = { recipientCode: "AB-1234", crateCount: 1, priority: "standard" };
Object.defineProperty(draft, "priority", { enumerable: false });
const result = validateShipmentDraft(draft);
// Object.keys(draft) contains only recipientCode and crateCount.
// Required: invalid result with a priority issue.
// Predicted reference: error:null and a sanitized valid value.
```

The predicate “only enumerable own keys are [three names], with all three
present” specifies the required enumerable-own key set, not merely a whitelist
for optional keys. The supplied test explicitly ignoring an unknown hidden extra
does not waive required key presence. No Object.prototype mutation is needed to
establish the contradiction. Required values are copied into the output correctly;
the defect is admission of an invalid input shape.

## Reference hashes

| Generation suffix | Reference SHA256 |
| --- | --- |
| 0007 | d1e06e496c9fbf949ccb7525abf11231484f34e5e504ff19f6f8e3ea6b64e12f |
| 0008 | 93fc392141556bbed3de995b009fa5c59749021d7eeb3b3c241e7033604b7a50 |
| 0049 | 0fabcb6b054c2fb3ad03985f55929554a840b074a5e4727ccd2f9c19fe8da453 |
| 0059 | 3e25983c4b747864d5cfed6f4babbd259e328d32eeef0dbaec5977a38c468f03 |
| 0064 | 83e7eff45487902c5362d460030cf83a656f30cb9aed4c33031f4bdc1a4c2b4c |
| 0066 | ab136384a121b8d8de508e61a5531fbc00dcdd2a259ee042d90781c07ad47f0e |
| 0078 | a1fb1ac7325854469d6f4350af649949e5874edf5bff8b97b7792dd2f122deb8 |
| 0091 | 647d80eb45cb2eef7134a03450d839e20a4f4c53123f8f03f15af7e5b49e8b27 |
| 0094 | 150bed197186257ff9880bb434399f2946be2cfe1c15a182b69144d8e49e302f |

## Integration

Nine records: **3 proposed holds, 6 scoped positives, 0 undecided property
questions**. Proposed IDs: `exp-v1-typescript-generation-0007`,
`exp-v1-typescript-generation-0064`, `exp-v1-typescript-generation-0078`.
For 0078 this also resolves the linked required-versus-inherited key question
adversely under its enumerable-own contract; arbitrary hidden extras remain valid.

No original tests rerun, no generated witness executed, no central disposition
changed. Existing unrelated criteria remain as recorded; this note adds neither
a universal correctness claim nor a generic pending-property loop.
