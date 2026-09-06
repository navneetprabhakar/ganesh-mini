package solution

import "testing"

func TestReviewPageOverflow0266(t *testing.T) {
	defer func() { if p := recover(); p != nil { t.Fatalf("valid end cursor panicked: %v", p) } }()
	records := []AssetRecord{{ID: "a", Created: "2026-01-01T00:00:00Z", Modified: "2026-01-01T00:00:00Z"}}
	rows, next, err := ListAssets(records, AssetQuery{PageSize: int(^uint(0) >> 1), Cursor: "1"})
	if err != nil || len(rows) != 0 || next != "" { t.Fatalf("end page: rows=%v next=%q err=%v", rows, next, err) }
}
