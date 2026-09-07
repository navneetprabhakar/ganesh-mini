package solution

import "testing"

func TestReviewASCIICase0360(t *testing.T) {
	if got, err := ParseSeverity("\u0130NFO"); err == nil { t.Fatalf("accepted non-ASCII dotted-I severity as %v", got) }
}
