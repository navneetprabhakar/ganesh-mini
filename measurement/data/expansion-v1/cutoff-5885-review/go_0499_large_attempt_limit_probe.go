package solution

import "testing"

func TestReviewLargeAttemptLimitEarlySuccess(t *testing.T) {
	calls := 0
	used, err := RunWeighted(int(^uint(0)>>1), 1, func(weight int) error {
		calls++
		return nil
	})
	if err != nil || calls != 1 || len(used) != 1 || used[0] != 1 {
		t.Fatalf("used=%v calls=%d err=%v", used, calls, err)
	}
}
