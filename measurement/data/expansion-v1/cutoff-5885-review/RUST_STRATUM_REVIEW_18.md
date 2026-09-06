# Rust generation review, batch 18 (partial)

Positions 256–258 of the 684-record outside-sample queue. Three full prompt,
reference and original-test inspections. One new static hold. Total 807 unique
outside-sample inspections, 417 additive plus historical three = 420 holds.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 256 | 0298 | Static hold: Position field names/types required by original tests omitted from prompt. |
| 257 | 0302 | Exact API/derives, specified fingerprint, zero-secret precedence, ordered alias replacement and no mutation on errors. Public duplicate slots unspecified. No new hold. |
| 258 | 0304 | Exact API, per-original-character escaping, optional current attribute and stable duplicate order. Small rendering exercise nontriviality unresolved. No new hold. |

0298 static contract/test comparison: prompt declares fields for Range and
Location but only asks for Position with public fields, never specifying which
fields or types. Original location helper directly constructs
`Position { line:u32, character:u32 }`. These required declarations are absent.
Reference also lacks an explicit empty-symbol guard when a caller populates the
public map with an empty key; this secondary case has not been probed and is not
claimed as executed evidence. One hold for the missing Position interface.

Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
No new sandbox execution. No-hold is not admission approval; scope v6 unchanged.
Continue position 259, not the next batch boundary. No new VM, seal or partition.
