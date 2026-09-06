package solution

import "testing"

func TestReviewAlteredToken0102(t *testing.T) {
	s, err := NewAccountStore([]byte("review-secret"))
	if err != nil { t.Fatal(err) }
	if _, err = s.Register("A", "a@example.test", "password1"); err != nil { t.Fatal(err) }
	token, err := s.Authenticate("a@example.test", "password1")
	if err != nil { t.Fatal(err) }
	if _, err = s.Verify(token); err != nil { t.Fatal(err) }
	if account, err := s.Verify(token + "\n"); err == nil {
		t.Fatalf("altered token with newline accepted: %+v", account)
	}
}
