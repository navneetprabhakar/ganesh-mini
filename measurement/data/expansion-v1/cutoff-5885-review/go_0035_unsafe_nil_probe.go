package solution

import (
    "testing"
    "unsafe"
)

func TestReviewNilUnsafePointer0035(t *testing.T) {
    var value unsafe.Pointer
    matched, _ := IsNil()(value)
    if !matched { t.Fatal("typed nil unsafe.Pointer was not recognized") }
}
