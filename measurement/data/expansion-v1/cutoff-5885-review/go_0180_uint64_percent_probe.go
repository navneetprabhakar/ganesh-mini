package solution

import "testing"

func TestReviewUint64Percent0180(t *testing.T) {
	got, err := CollectionPercent(uint64(1)<<63, ^uint64(0))
	if err != nil || got != 99 { t.Fatalf("percent=%v err=%v, want 99", got, err) }
}
