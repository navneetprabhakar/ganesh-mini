package solution

import (
	"errors"
	"testing"
)

func TestReviewNullShape0280(t *testing.T) {
	_, err := ParseBadge([]byte("null"), []string{""})
	if !errors.Is(err, ErrMalformedBadge) { t.Fatalf("non-object null: err=%v, want ErrMalformedBadge", err) }
}
