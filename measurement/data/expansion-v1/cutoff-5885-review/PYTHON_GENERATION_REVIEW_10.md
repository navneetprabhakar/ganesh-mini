# Python generation review, batch 10

Positions 136–150 of 684, v6 outside-sample Python generation queue. Fifteen
full prompt/reference/original-test inspections; seven reproduced holds.
545 additive plus historical three = 548 holds; 1,383 unique outside-sample
inspections. No seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 136 | 0149 | Hold: float division loses exact quantile endpoint. Ordinary batching/deep copies agree; malformed compressed payload handling remains pending. |
| 137 | 0153 | Hold: mixed asset key types are sorted before validation, yielding TypeError instead of ValueError. Normal route ordering/callable identity agree. |
| 138 | 0154 | Base36 divmod encoding and validation agree; no new hold. |
| 139 | 0155 | Exact control tokens, nickname stripping, send spacing, snapshots and closed state agree; no new hold. |
| 140 | 0156 | Hold: valid falsey logger discarded by truthiness fallback. Ordinary lifecycle hook/state ordering agrees. |
| 141 | 0151 | Hold: permitted generator group iterable cannot be deep-copied; Unicode secret also fails hmac string comparison. Ordinary atomic replacements/admin override agree. |
| 142 | 0157 | Current selection ordering and bank fill agree. Payload preservation and cumulative skipped semantics remain ambiguous/pending; no new hold. |
| 143 | 0158 | Hold: decimal one with 5,000 leading zeroes rejected by integer conversion limit. Ordinary task commands and copying agree. |
| 144 | 0159 | Hold: literal-space partition does not recognize tab-delimited command token. |
| 145 | 0161 | Manual constants, normalization and readonly tuple agree; depth criterion pending. |
| 146 | 0162 | EventStore ordinary JSON validation, IDs, deep copies and clear agree. Extreme JSON numbers/duplicate-key semantics remain pending; no new hold. |
| 147 | 0163 | Strict streak logic, empty/equal cases and full validation agree. Integer-subclass domain pending; no new hold. |
| 148 | 0164 | Hold: unrestricted integer coefficient/constant overflow eager complex conversion even with exactly representable solution 1. Ordinary pivoting/copying/residual agree. |
| 149 | 0165 | Tokenization dynamic program, empty text, Unicode and order invariance agree; no new hold. |
| 150 | 0166 | Casefold uniqueness, exact PIN, profile filtering and metadata copy agree for ordinary values; custom object copying semantics pending, no new hold. |

Seven pinned Python 3.11.15 probes, network disabled/resource limited, all exit
1 without timeout. Holds are review items, not final rejection decisions.

| ID | Probe / result stem | ms | Observed finding |
| --- | --- | ---: | --- |
| 0149 | quantile_integer_endpoint_probe.py / quantile-integer-endpoint-result.json | 403 | Last position rounds down from 2**53+1. |
| 0153 | routes_mixed_asset_keys_probe.py / routes-mixed-asset-keys-result.json | 425 | Mixed-key sorting TypeError. |
| 0156 | lifecycle_falsey_logger_probe.py / lifecycle-falsey-logger-result.json | 414 | Supplied logger receives no initialization message. |
| 0151 | policy_iterable_secret_probe.py / policy-iterable-secret-result.json | 430 | Generator deepcopy and Unicode compare_digest TypeErrors. |
| 0158 | task_number_leading_zeros_probe.py / task-number-leading-zeros-result.json | 393 | Valid decimal one rejected. |
| 0159 | dispatch_whitespace_probe.py / dispatch-whitespace-result.json | 417 | Tab-delimited repeat dispatch returns False. |
| 0164 | complex_integer_identity_probe.py / complex-integer-identity-result.json | 418 | OverflowError during constructor conversion. |

Candidate SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Continue position 151. Original candidates/tests/sample/partition unchanged.
