package solution

import "testing"

func TestReviewDeltaOverflow0095(t *testing.T) {
	const minimum int64 = -1 << 63
	const maximum int64 = 1<<63 - 1
	g, err := NewChronoID(0, minimum)
	if err != nil { t.Fatal(err) }
	if id, err := g.Next(maximum); err == nil {
		t.Fatalf("delta greater than 41 bits accepted: id=%d", id)
	}
	if id, err := g.Next(minimum); err != nil || id != 0 {
		t.Fatalf("valid first timestamp after rejection: id=%d err=%v", id, err)
	}
}
