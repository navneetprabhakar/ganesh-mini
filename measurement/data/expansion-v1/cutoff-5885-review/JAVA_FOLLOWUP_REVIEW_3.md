# Java combined quality follow-up — batch 3

Positions31–45 of frozen v13 Java combined queue1112, full prompt/reference read.
Seven non-triviality holds and six behavioral holds (three executed, three static).
1439 total holds (1436 additive+3);3732 unique outside-sample inspections. Resume46.

| Position | ID | Finding |
| --- | --- | --- |
| 31 | exp-v1-java-generation-0023 | Criterion-positive: exact descriptor membership and canonical bounded numeric version grammar. |
| 32 | exp-v1-java-generation-0024 | Executed hold: attack A1 as a miss, then place a ship at A1; renderShots changes the recorded miss to x without a hit, exposing an unhit ship. No placement-phase restriction exists in the prompt. |
| 33 | exp-v1-java-repair-0013 | Non-triviality hold: swaps two supplied assignability branches to the explicitly required subtype-first order. |
| 34 | exp-v1-java-repair-0015 | Non-triviality hold: direct equality-to-inequality replacement, with the correct counting predicate already supplied. |
| 35 | exp-v1-java-repair-0016 | Non-triviality hold: substitutes the explicitly named Objects.equals primitive for boxed identity comparison. |
| 36 | exp-v1-java-generation-0019 | Static hold: new Profile(1,U+2003,0) passes trim().isEmpty() despite nonblank name requirement. |
| 37 | exp-v1-java-generation-0022 | Static hold: new Reading(1,U+2003,0) accepts a blank sensor name. |
| 38 | exp-v1-java-generation-0025 | Criterion-positive: validates paired relationship presence/IDs and snapshots the related fields without retaining source objects. |
| 39 | exp-v1-java-generation-0027 | Non-triviality hold: direct prescribed authentication status decision table over map/set lookups and literal result projection. |
| 40 | exp-v1-java-generation-0028 | Static hold: the required immutable OperationOutcome retains and exposes its caller-owned mutable links map; final reference fields do not make that object immutable. |
| 41 | exp-v1-java-generation-0029 | Executed hold: valid empty List.of() rooms throws NullPointerException from contains(null), rather than returning an empty page. |
| 42 | exp-v1-java-generation-0030 | Executed hold: valid List.of("a@b") emails throws NullPointerException from contains(null), rather than mapping the profile. |
| 43 | exp-v1-java-repair-0017 | Non-triviality hold: negates a supplied set-membership predicate. Static additional defect: contains(null) also rejects valid List.of inputs. |
| 44 | exp-v1-java-repair-0018 | Non-triviality hold: direct inclusive-to-strict counter boundary replacement; synchronization and independent state are already supplied. |
| 45 | exp-v1-java-repair-0019 | Non-triviality hold: directly substitutes the prescribed committed counter into one subtraction. |

## Executed evidence

- java_0024_late_placement_probe-result.json: 3378 ms, exit codes [0,1], no timeout.
- java_0029_immutable_list_probe-result.json: 2576 ms, exit codes [0,1], no timeout.
- java_0030_immutable_list_probe-result.json: 2399 ms, exit codes [0,1], no timeout.

All probes compiled in pinned Java21.0.11, network-disabled/resource-limited
sandbox. Original tasks and references are preserved in receipts. List.of is
ordinary valid List input, not a hostile custom implementation. Null-query
validation via contains(null) is not portable across valid List implementations.
This defect will be checked across the already reopened Java queue; pattern
presence alone does not automatically hold other records.

The immutable-outcome finding is static: mutate the constructor's HashMap or
the getLinks() result, and getLinks() subsequently exposes the changed contents.
The two Unicode findings propagate the already executed U+2003 nonblank case.
No other new execution or all-seven-criteria approval is claimed.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

