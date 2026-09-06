package solution

import "testing"

func TestReviewSpanOverflow0048(t *testing.T) {
    minInt := -int(^uint(0)>>1) - 1
    low, high, ok := ClosestSpan([]int{minInt, 0, 1})
    if !ok || low != 0 || high != 1 { t.Fatalf("got (%d,%d,%v), want (0,1,true)", low, high, ok) }
}
