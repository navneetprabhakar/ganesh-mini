package solution

import "testing"

func TestReviewEndpoints0233(t *testing.T) {
	base := int(int64(1) << 53)
	got := ScaleReadings([]int{base, base + 1})
	if len(got) != 2 || got[0] != 0 || got[1] != 1 { t.Fatalf("adjacent-int endpoints=%v, want [0 1]", got) }
}
