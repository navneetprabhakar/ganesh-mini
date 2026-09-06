# Rust generation review, batch 15

Positions 211–225 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections. Six new static interface holds. Total
774 unique outside-sample inspections, 409 additive plus historical three = 412 holds.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 211 | 0243 | Exact API/derives and checked positive material formulas/totals. Signed-positive parsing and simultaneous zero/malformed precedence not explicitly adjudicated. No new hold. |
| 212 | 0244 | Exact API, declared validation order, all win lines before draw and stable row-major moves. No new hold. |
| 213 | 0245 | Exact function, first complete matching record, reset on nested start and last recognized field wins. No new hold. |
| 214 | 0246 | Exact API, validation at zero steps, row-major nine-bit index and correct infinite background transition. Extreme grid/step resource envelope not executed. No new hold. |
| 215 | 0248 | Static hold: Column variant shape and tested Clone/equality omitted. |
| 216 | 0249 | Static hold: constructor and required method signatures omitted. |
| 217 | 0247 | Static hold: unavailable reference API and tested lookup/trait requirements omitted. |
| 218 | 0250 | Static hold: directly constructed rig/part/motion field shapes/types omitted. |
| 219 | 0251 | Static hold: Record shapes and Store constructor/signatures/traits omitted. |
| 220 | 0252 | Static hold: declaration-order contract without a Key declaration; event/control API omitted. |
| 221 | 0253 | Exact API/derives, first lexicon duplicate retained, Unicode buffer, gated edits, lazy visibility and ordered suggestions. Initial enabled state not explicit; tests enable before edits. No new hold. |
| 222 | 0254 | Exact API, checked delta before mutation and borrowed first-on-tie result. Small arithmetic/comparison wrapper nontriviality unresolved. No new hold. |
| 223 | 0255 | Exact API, checked read area, tolerant malformed plane entries, row rendering. Corresponding digit character for pixel >9 and huge manually supplied area remain unspecified/unadjudicated. No new hold. |
| 224 | 0256 | Exact API, validation before in-place replacement and insertion-order borrowed results. The Duplicate clause is interpreted as ID mismatch; no broader precedence oracle imposed. No new hold. |
| 225 | 0257 | Exact API, copied FIFO, protocol-first errors and explicit saturating sequence. External close preserves open state/buffer. No new hold. |

Static evidence details (not runtime failures):

- 0248 names Column/ColumnKind without declaring variants or data shapes. Test
  `compression_splits_runs_at_255_and_does_not_mutate` constructs
  `Column::Text(vec![...])`, calls clone and asserts whole-value equality. Those
  compile-time requirements are not provided by the prompt's encoding prose.
- 0249 tests construct `MemoryPlugin::new()` although no constructor is named in
  the prompt, and require `handle(&str)->Result<String,_>` and
  `get(&str)->Option<&str>`. The prose does not specify these complete signatures.
- 0247 says to use the public API shown by the reference, but the user prompt
  includes no reference. Original tests require get/get_mut/children and
  NavHistory clone/equality; the corresponding names/signatures/traits are absent.
- 0250 tests construct public `Rig { parts: [Part;6] }`, Part with position:Vec3
  and f64 pitch/yaw/roll/scale, and Motion with four f64 fields. Naming six parts
  and formulas does not supply this particular field/type representation.
- 0251 tests construct `Record::Put { key:String,value:String }` and
  `Record::Erase { key:String }`, use `Store::new()`, and clone/compare Store and
  Record values. The prompt supplies the wire tags but not these Rust declarations.
- 0252 requires pressed_keys in declaration order without giving a Key
  declaration. Tests require ShiftLeft/ShiftRight and specific Event variants,
  public boolean Controls fields, is_open/menu_opacity accessors and exact order.

Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
No new sandbox execution. No-hold is not admission approval; scope v6 unchanged.
GCS verified through 405 holds / Rust batch 13 / 744 inspections; batches 14–15
await backup. Continue position 226. No new VM, seal or revised partition.
