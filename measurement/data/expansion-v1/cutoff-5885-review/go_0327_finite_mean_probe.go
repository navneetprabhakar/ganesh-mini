package solution

import (
	"math"
	"testing"
)

func TestReviewFiniteMean0327(t *testing.T) {
	l := NewLedger()
	for i := 0; i < 2; i++ { if err := l.Append("a", math.MaxFloat64, int64(i)); err != nil { t.Fatal(err) } }
	got, ok := l.Mean("a")
	if !ok || got != math.MaxFloat64 { t.Fatalf("mean of two identical finite values=%v ok=%v, want MaxFloat64", got, ok) }
}
