package solution

import (
    "encoding/json"
    "testing"
)

func TestReviewJSONControl0072(t *testing.T) {
    text, err := RenderBindings(map[string]string{"key": "\a"}, FormatJSON)
    if err != nil { t.Fatal(err) }
    if !json.Valid([]byte(text)) { t.Fatalf("not valid JSON: %q", text) }
}
