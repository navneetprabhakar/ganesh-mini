package solution

import "testing"

func TestReviewTokenEncoding0160(t *testing.T) {
	s, err := NewPassService("review-key")
	if err != nil { t.Fatal(err) }
	token, err := s.Issue(PassClaims{Subject:"s",DisplayName:"n",ExpiresAt:10})
	if err != nil { t.Fatal(err) }
	if _, err = s.Verify(token, 0); err != nil { t.Fatal(err) }
	if claims, err := s.Verify(token+"\n", 0); err == nil {
		t.Fatalf("non-base64url newline accepted: %+v", claims)
	}
}
