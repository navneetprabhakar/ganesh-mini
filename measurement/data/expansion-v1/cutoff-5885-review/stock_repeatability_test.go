package solution

import (
	"os"
	"os/exec"
	"testing"
)

// Re-run the unmodified original tests in fresh processes to expose dependence
// on Go's unspecified map iteration order. This is a diagnostic, not admission.
func TestReviewStockDirectionalityRepeatability(t *testing.T) {
	passed := 0
	for i := 0; i < 64; i++ {
		cmd := exec.Command(os.Args[0], "-test.run=^TestStockLedger", "-test.count=1")
		output, err := cmd.CombinedOutput()
		t.Logf("trial=%d error=%v output=%q", i, err, output)
		if err == nil {
			passed++
		} else if _, ok := err.(*exec.ExitError); !ok {
			t.Fatalf("child infrastructure error: %v; %s", err, output)
		}
	}
	// Always emit counts, including on a passing reference control.
	t.Errorf("DIAGNOSTIC_ONLY: original-suite passes=%d failures=%d trials=64", passed, 64-passed)
}
