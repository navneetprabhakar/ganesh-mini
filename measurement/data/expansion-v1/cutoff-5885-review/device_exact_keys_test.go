package solution

import "testing"

func TestReviewDeviceKeysAreExact(t *testing.T) {
	for _, input := range []string{`{"Label":"x","level":1}`, `{"label":"x","Level":1}`} {
		if got, err := DecodeDeviceConfig([]byte(input)); err == nil {
			t.Errorf("non-exact field spelling accepted: input=%s got=%+v", input, got)
		}
	}
}
