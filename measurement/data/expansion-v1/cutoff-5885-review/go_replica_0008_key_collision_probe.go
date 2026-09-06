package solution

import "testing"

func TestDistinctReplicaKeysDoNotShareDots(t *testing.T) {
    reads := []map[string][]Version{{
        "a\x00b": {{Origin: "c", Counter: 1, Value: "first"}},
        "a": {{Origin: "b\x00c", Counter: 1, Value: "second"}},
    }}
    got, err := MergeReplicaReads(reads, "siblings")
    if err != nil { t.Fatalf("distinct keys and dots rejected: %v", err) }
    if len(got) != 2 { t.Fatalf("wanted two keys, got %v", got) }
}
