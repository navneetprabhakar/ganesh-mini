package solution

import (
	"encoding/json"
	"testing"
)

func TestReviewNilDistribution0162(t *testing.T) {
	var d *DurationDistribution
	got, err := json.Marshal(d)
	if err != nil { t.Fatal(err) }
	if string(got) != `{"bounds_ns":[],"counts":[0]}` {
		t.Fatalf("nil distribution JSON=%s", got)
	}
}
