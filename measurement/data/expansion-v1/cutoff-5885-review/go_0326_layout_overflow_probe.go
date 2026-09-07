package solution

import "testing"

func TestReviewLayoutOverflow0326(t *testing.T) {
	maximum := int(^uint(0) >> 1)
	_, err := EncodeLayout(Layout{Material: "m", Capacity: maximum, Segments: []Segment{{Code: "a", Span: maximum}, {Code: "b", Span: 1}}})
	if err == nil { t.Fatal("accepted total span MaxInt+1 exceeding capacity MaxInt") }
}
