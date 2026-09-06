package solution

import "testing"

func TestReviewBoundedGenerator0204(t *testing.T) {
	defer func() { if p := recover(); p != nil { t.Errorf("bounded output panicked: %v", p) } }()
	values := PowersOfThree(int(^uint(0)>>1))
	if len(values) != 41 || values[0] != 1 || values[40] != 12157665459056928801 {
		t.Fatalf("incorrect bounded power sequence: %v", values)
	}
}
