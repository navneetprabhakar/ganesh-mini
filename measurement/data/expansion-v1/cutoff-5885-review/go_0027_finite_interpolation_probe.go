package solution

import (
    "math"
    "testing"
)

func TestReviewFiniteMidpoint0027(t *testing.T) {
    got, err := InterpolateObservation([]Observation{{Minute: 0, Value: -1e308}, {Minute: 2, Value: 1e308}}, 1)
    if err != nil || math.IsNaN(got) || math.IsInf(got, 0) || got != 0 {
        t.Fatalf("representable midpoint: got %v, error %v; want 0", got, err)
    }
}
