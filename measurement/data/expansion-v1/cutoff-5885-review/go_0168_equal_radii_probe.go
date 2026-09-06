package solution

import "testing"

func TestReviewEqualRadii0168(t *testing.T) {
	area, err := RingArea(1e200, 1e200)
	if err != nil || area != 0 { t.Fatalf("equal finite radii: area=%v err=%v, want zero", area, err) }
}
