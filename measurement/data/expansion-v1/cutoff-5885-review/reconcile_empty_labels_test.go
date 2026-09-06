package solution

import "testing"

func TestReviewDifferentEmptyValuedLabelKeysRequireUpdate(t *testing.T) {
	bp := Blueprint{Name: "x", Labels: map[string]string{"desired": ""}}
	current := &Workload{Name: "x", Labels: map[string]string{"existing": ""}}
	got, err := Reconcile(bp, current)
	if err != nil || got.Action != "update" {
		t.Fatalf("different label keys require update; got action=%q err=%v", got.Action, err)
	}
}
