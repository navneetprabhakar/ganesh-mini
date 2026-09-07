# Java combined quality follow-up — batch 60

Positions886–900 of v14 Java queue1112, full prompt/reference read.
Eight new holds: three non-triviality and five static behavioral/contract findings.
1918 total holds (1915 additive+3),4587 unique outside inspections. Resume901.
Approved versioned recovery remains pending; original corpus unchanged.

| Position | ID | Finding |
| --- | --- | --- |
| 886 | exp-v1-java-repair-0422 | Criterion-positive LRU recency and eviction invariant: evict oldest at the tail after moving an accessed key to the front; capacity zero remains valid. |
| 887 | exp-v1-java-repair-0423 | Non-triviality hold: guarded direct Math.floorMod library wrapper for a single bucket index. |
| 888 | exp-v1-java-repair-0424 | Criterion-positive protocol authorization boundary: HTTPS-only restriction composes with exact normalized host, no-userinfo and no-port checks. |
| 889 | exp-v1-java-generation-0637 | Criterion-positive binary chunk framing separates empty chunks from the terminal frame and preserves byte payloads, hexadecimal lengths and CRLF boundaries. |
| 890 | exp-v1-java-generation-0638 | Non-triviality hold: prescribed x-first scalar branch and single-cell Integer.compare step with independent bounds guards. |
| 891 | exp-v1-java-generation-0640 | Criterion-positive whole-map validation before lookup preserves invalid-entry precedence even after a matching key; checked missing exception retains identifier. |
| 892 | exp-v1-java-generation-0641 | Static hold: squared-double distance rounds (2147483647,1) from viewer (0,0) onto radius 2147483647, including a point strictly outside the integer radius. Overflow avoidance does not preserve the exact inclusion boundary. Not executed. |
| 893 | exp-v1-java-generation-0642 | Static hold: TextConversion.supports runs outside the runtime-exception wrapper; a throwing supports callback escapes rather than becoming ParseException with its original cause. Not executed. |
| 894 | exp-v1-java-repair-0425 | Criterion-positive logical right shift preserves the 64-bit rotation invariant when the sign bit is set; floor-mod distance and zero case remain intact. |
| 895 | exp-v1-java-repair-0426 | Criterion-positive ascending bubble-sort invariant repairs the reversed comparison while retaining stable ties, overflow-safe comparison and deep ownership. |
| 896 | exp-v1-java-repair-0427 | Non-triviality hold: two literal legacy-name substitutions change identity comparison to equals without a substantive algorithm or state invariant. |
| 897 | exp-v1-java-generation-0639 | Criterion-positive full validation before first-match lookup and detached row copy preserve invalid-tail rejection and ownership with duplicate names. |
| 898 | exp-v1-java-generation-0643 | Static hold: squaring each hypot result reintroduces overflow; vector [1e200] produces infinite norm although 1e200 is representable. [Double.MAX_VALUE,Double.MAX_VALUE] also overflows the sum before averaging. Not executed. |
| 899 | exp-v1-java-generation-0644 | Static hold: LocalDate canonical roundtrip accepts extended-year +10000-01-01, outside the required strict yyyy-MM-dd spelling. Ledger getter requirements are also underspecified and need clarification before recovery. Not executed. |
| 900 | exp-v1-java-generation-0645 | Static hold: Locale.ROOT uppercasing accepts dotless-i spelling of italian despite ASCII-letter-case-only parsing. Also elementary literal greeting/enum mapping; not executed. |

No new execution. Static findings are not executed results. Focused positives
are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

