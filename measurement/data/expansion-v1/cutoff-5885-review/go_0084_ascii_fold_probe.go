package solution

import "testing"

func TestReviewASCIIOnlyFold0084(t *testing.T) {
    result, err := InspectFieldMatches("package p; type D struct { AK int }", "D", "package p; type S struct { AK int }", "S")
    if err != nil { t.Fatal(err) }
    if len(result) != 0 { t.Fatalf("ASCII-only lowercase must not fold Kelvin sign: %+v", result) }
}
