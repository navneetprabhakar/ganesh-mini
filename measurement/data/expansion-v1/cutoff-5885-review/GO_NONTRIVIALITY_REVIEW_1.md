# Go non-triviality follow-up, batch 1

Positions 1–15 of 757: v7 reopened Go records outside the frozen sample, in
inventory order. Full prompts and complete reference source read. This is a
focused non-triviality review, not a fresh test/known-bad review or all-seven
approval. Original tests were not read in this focused pass. The two Go
diagnostics below include the original tests plus an added diagnostic file;
no known-bad implementation was re-executed.
Candidate SHA: 680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

| Position | ID suffix (Go) | Criterion decision and incidental findings |
| --- | --- | --- |
| 1 | generation-0001 | Non-trivial: provider/method validation, exactly-once external interface delegation and error identity. |
| 2 | generation-0002 | Non-trivial: bounded framing, checksum, failed-add atomicity and ownership on both boundaries. |
| 3 | generation-0003 | Non-trivial: composite keys, ordered mutation, nil behavior and independent filtered snapshots. |
| 4 | generation-0004 | Non-trivial: interface dispatch, conditional sink choice, validation and original error propagation. |
| 5 | generation-0005 | Non-trivial despite short source: evaluated defer arguments, named result mutation and LIFO execution are required language mechanisms, not just the displayed output. |
| 6 | generation-0006 | Non-trivial: mask enumeration, integer-width guard, duplicate-position identity and independent inner storage. General feasible-allocation envelope not adjudicated. |
| 7 | repair-0001 | Hold: non-triviality not met; elementary AND-to-OR library predicate correction with non-nil empty normalization. |
| 8 | repair-0002 | Non-trivial: rune-count filtering, separate numeric/bytewise sort keys and preserved duplicates/copies. |
| 9 | repair-0003 | Non-trivial: minimum-int magnitude conversion, digit-key sorting and tie/copy semantics. |
| 10 | generation-0008 | Non-trivial; separate reproduced hold: NUL-delimited composite identity collides across distinct map keys/origins. Mutual causal dominance wording also deserves eventual contract disposition. |
| 11 | generation-0010 | Non-trivial: matrix shape/finite validation, copied model data and closed-resource lifecycle. No output-finiteness guarantee invented beyond the prescribed formula. |
| 12 | generation-0011 | Non-trivial: Unicode filtering/lowercasing and rune-palindrome analysis across ordered records. |
| 13 | generation-0012 | Non-trivial: minimum versus inclusive selected sum and widened accumulation. Unrestricted slice sizes can exceed uint64 aggregate capacity; no huge-allocation execution or final range adjudication claimed. |
| 14 | repair-0005 | Non-trivial: negative parity classification within a cross-slice swap feasibility algorithm. |
| 15 | repair-0008 | Non-trivial: zero representation interacts with bounded multiple enumeration and digit counting. Separate reproduced nontermination hold below. |

14 criterion-positive, one non-triviality hold; two incidental behavioral holds.
Three new holds: 1088 additive plus historical three = 1091. Fifteen new
outside-sample scoped inspections bring unique coverage to 2945.

Both diagnostics used pinned Go 1.22.12, network disabled and resource limited;
go test completed with exit [1], sandbox timed_out=false:

- `go_replica_0008_key_collision_probe-result.json`, 29817 ms: map key `a\0b`
  with origin `c` and key `a` with origin `b\0c`, both counter1, are rejected
  as a conflicting same dot although the key/origin pairs are distinct.
- `go_multiples_0008_overflow_probe-result.json`, 31622 ms: limit2^62+1 and
  divisor2^62 require only multiples 0 and 2^62. The function did not complete
  within the diagnostic's two-second deadline. Static signed arithmetic explains
  the repeating increment sequence 0, 2^62, -2^63, -2^62, 0. This is a completed
  failing diagnostic, not an infrastructure timeout or measured infinite run.

Correction after the first 1092-hold archive: unlike the other language probe
modes, the Go helper preserves original test files and adds review_test.go.
The recorded tasks and probe_mode=additive are authoritative. The earlier
archived prose incorrectly called these isolated replacements. There was no
separate original-suite-only or known-bad run. No original candidate, test,
sample or partition changed. Continue position16. Criterion-positive does not
mean training admission.
