package solution

import (
    "strconv"
    "strings"
    "testing"
    "time"
)

func TestLargeDivisorTerminatesAfterTwoMultiples(t *testing.T) {
    if strconv.IntSize != 64 { t.Fatal("diagnostic requires the pinned 64-bit runtime") }
    divisor := int(1) << 62
    type result struct { count int; err error }
    done := make(chan result, 1)
    go func() {
        count, err := CountDigitInMultiples(divisor + 1, divisor, 0)
        done <- result{count, err}
    }()
    select {
    case got := <-done:
        want := 1 + strings.Count(strconv.Itoa(divisor), "0")
        if got.err != nil || got.count != want { t.Fatalf("got %v, want count %d", got, want) }
    case <-time.After(2 * time.Second):
        t.Fatal("two-multiple calculation did not terminate; signed increment wraps into a four-value cycle")
    }
}
