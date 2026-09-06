package solution

import (
	"reflect"
	"testing"
)

func TestReviewNewlyReadyEarlierStepWins(t *testing.T) {
	var calls []string
	_, err := RunPlan([]Step{{Name: "a", Requires: []string{"b"}}, {Name: "b"}, {Name: "c"}}, func(n string) error {
		calls = append(calls, n)
		return nil
	})
	if err != nil || !reflect.DeepEqual(calls, []string{"b", "a", "c"}) {
		t.Fatalf("ready steps must use input-order priority: calls=%v err=%v", calls, err)
	}
}
