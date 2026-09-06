package solution

import "testing"

func TestReviewComponentTuple0133(t *testing.T) {
	r := NewRegistry()
	if _, err := r.Create("b\x00c", "a", "v1"); err != nil { t.Fatal(err) }
	if _, err := r.Create("c", "a\x00b", "v2"); err != nil {
		t.Fatalf("distinct scope/name tuple rejected: %v", err)
	}
}
