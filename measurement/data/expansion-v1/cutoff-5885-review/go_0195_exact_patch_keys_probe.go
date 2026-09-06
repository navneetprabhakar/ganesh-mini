package solution

import (
	"errors"
	"testing"
)

func TestReviewExactPatchKeys0195(t *testing.T) {
	s := NewCardService([]Card{{ID:1,Board:"b",Name:"old"}}, map[string][]string{"a":{"b"}}, true, true)
	if card, err := s.UpdateCard("a", "b", 1, []byte(`{"Name":"changed"}`)); !errors.Is(err, ErrBadBody) {
		t.Fatalf("unknown capitalized key accepted: card=%+v err=%v", card, err)
	}
	if s.SearchCopy()[1].Name != "old" || len(s.EventsCopy()) != 0 { t.Fatal("failed patch changed state") }
}
