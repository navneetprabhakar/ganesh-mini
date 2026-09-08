# Main r10 bounded correction approval

Main fully read r8Java review and complete provisional r10request/feedback.
Actual previous canonical candidate and review-file hashes validated for allfour.
Approve exactly one test-only correction for0641/0617/0687/0762. Preserve r8
specification/reference/mutant bytes and independent spec/tests/feedback-only
critic context. No reference edit to accommodate an unsupported oracle.

0641 needs exact integer-distance exclusion rather than floating tolerance;
0617 accepts standard Set.of/TreeSet;0687 checks invalid DELETE permissions at
apply-time with construction inside the check;0762 drops the disputed standalone
newline assertion without adding either acceptance or rejection. Preserve every
other explicit contract and whole-target test. No private layout or new domain.
Original r8 diagnoses are already preserved:0641/0617 allcontrols pass;
0687/0762 allcontrols fail behaviorally. No automatic second correction or
admission claim. Current Go verifier remains serial and undisturbed.
