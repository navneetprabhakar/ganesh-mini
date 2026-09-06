package solution

import "testing"

func TestReviewSignatureNewline0276(t *testing.T) {
	secret := []byte("review-secret")
	token, err := GenerateSessionCredential("subject", "contact", secret, 0)
	if err != nil { t.Fatal(err) }
	if _, err = VerifySessionCredential(token+"\n", secret, 1); err == nil { t.Fatal("accepted newline outside unpadded URL-safe base64 alphabet") }
}
