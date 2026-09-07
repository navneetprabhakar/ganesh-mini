package solution

import (
	"math"
	"testing"
)

func TestReviewEqualSpeed0231(t *testing.T) {
	_, found, err := BestGate([]Gate{{Distance: 1, Grace: 0}}, math.SmallestNonzeroFloat64, math.SmallestNonzeroFloat64)
	if err != nil || !found { t.Fatalf("equal speeds have zero arrival gap: found=%v err=%v", found, err) }
}
