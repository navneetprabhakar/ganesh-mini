# Python repair review, batch 1

Positions 1–15 of 426, v6 outside-sample Python repair queue. Full prompt,
known-bad source, corrected source and original-test inspections. Eight new
additive holds: 738 additive plus historical three = 741; 1,932 unique
outside-sample inspections. These are review items, not final rejections.
The stated repairs agree on ordinary inputs; separate inherited contract
issues do not mean those repairs failed. This is not seven-criterion approval,
known-bad execution certification, a nontriviality seal or training admission.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 1 | 0001 | Corrected middle padding from width minus one to width minus two. Ordinary dimensions, fill and validation agree; no new hold. |
| 2 | 0002 | Corrected line counting to LF count plus one for nonempty input. Empty, words and codepoint counts agree; no new hold. |
| 3 | 0003 | Corrected truthiness to key presence. Present zero/negative levels and validation agree; no new hold. |
| 4 | 0004 | Sorted copy repairs input mutation. Hold: mean of two 1e308 values overflows instead of returning 1e308. |
| 5 | 0006 | Multiplication repairs dot-product operation. Hold: finite cancellation produces NaN. Ordinary ranking, stable ties and validation agree. |
| 6 | 0008 | Escaped next character now copied instead of backslash. Quote transitions, explicit empty arguments, literal quoted backslashes and malformed endings agree; no new hold. |
| 7 | 0009 | Inclusive distance comparison repairs boundary retention. Hold: Fraction coordinate and minimum rejected despite finite-real contract. |
| 8 | 0010 | Subtraction repairs elimination sign. Hold: large finite elimination intermediates produce NaN for solution [-1, 2]. |
| 9 | 0011 | Default-bound factor repairs late closure capture. Hold: finite large integers raise OverflowError at factor/argument validation. Additional optional factor parameter and scalar subclasses remain contract-review questions. |
| 10 | 0012 | Tuple key repairs grouping by both system and table. First-pair order, full validation and fresh mappings agree. Broad duck-typed mapping acceptance pending; no new hold. |
| 11 | 0013 | Active disconnect now records rollback, idle disconnect is a no-op. Transition atomicity and fresh events agree; no new hold. |
| 12 | 0014 | Recursive dictionary merge repairs shallow replacement, with ordinary order/detachment intact. Hold: finite 600-level dictionary cannot be copied. Arbitrary copy and graph domains pending. |
| 13 | 0017 | Scaling before clamp repairs operation order. Hold: finite huge integer rejected despite representable clamped output. |
| 14 | 0018 | Unpaired terminal escape now raises ValueError. Empty fields and escaped separators/backslashes agree; no new hold. |
| 15 | 0019 | KeyError catch repairs ordinary missing-key translation. Hold: missing defaultdict key returns default, not ConfigError. Ordinary detached lookup and component naming agree. |

Eight pinned Python 3.11.15 isolated probes, network disabled and resource
limited; every run exits 1 without timeout. Original verifier tests were read,
not rerun in these isolated probes. Original candidates/tests/frozen sample
and historical partition remain unchanged. Candidate SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0004 | repair_central_mean_overflow / repair-central-mean-overflow | 839 | infinity instead of 1e308 |
| 0006 | repair_suggestions_cancellation / repair-suggestions-cancellation | 935 | NaN instead of zero |
| 0009 | repair_thin_fraction / repair-thin-fraction | 755 | two TypeErrors |
| 0010 | repair_tridiagonal_overflow / repair-tridiagonal-overflow | 793 | two NaN solution entries |
| 0011 | repair_scaler_large_integer / repair-scaler-large-integer | 785 | two OverflowErrors |
| 0014 | repair_node_config_depth / repair-node-config-depth | 777 | bounded RecursionError diagnostic |
| 0017 | repair_clamp_large_integer / repair-clamp-large-integer | 876 | OverflowError |
| 0019 | repair_config_missing_default / repair-config-missing-default | 799 | ConfigError not raised |

Probe filenames append `_probe.py`; result filenames append `-result.json`.
Batch backed up in QUALITY_STRATUM_746_BACKUP.md. Continue position 16.
