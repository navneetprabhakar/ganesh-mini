package solution

import (
	"math"
	"testing"
)

func TestReviewFiniteAngles(t *testing.T) {
	frame := Frame{East: 1, North: 2, Up: 3, Azimuth: math.MaxFloat64}
	got, err := Advance(frame, 0)
	if err != nil || got.East != frame.East || got.North != frame.North || got.Up != frame.Up || math.IsNaN(got.Azimuth) || got.Azimuth < 0 || got.Azimuth >= 360 {
		t.Errorf("zero distance with finite azimuth: got %+v, err %v", got, err)
	}
	got, err = Reorient(frame, math.MaxFloat64, 0)
	if err != nil || math.IsNaN(got.Azimuth) || math.IsInf(got.Azimuth, 0) || got.Azimuth < 0 || got.Azimuth >= 360 {
		t.Errorf("finite angle sum must normalize: got %+v, err %v", got, err)
	}
}
