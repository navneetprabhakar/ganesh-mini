import sys
import unittest

from solution import TokenRule


class ComplexityTests(unittest.TestCase):
    def test_adversarial_suffix_does_not_repeat_quadratic_work(self):
        counts = []
        target = TokenRule.accepts.__code__
        for size in (128, 256, 512):
            count = 0

            def trace(frame, event, arg):
                nonlocal count
                if frame.f_code is target and event == "line":
                    count += 1
                return trace

            sys.settrace(trace)
            try:
                result = TokenRule().accepts(["a"] * (2 * size), [Ellipsis] + ["a"] * size + ["b"])
            finally:
                sys.settrace(None)
            self.assertFalse(result)
            counts.append(count)
        print("accepts line events at suffix sizes 128,256,512:", counts)
        # Both input dimensions double. Near-fourfold repeated work contradicts
        # the required linear bound; this is an operation-count probe, not timing.
        self.assertLess(counts[2], 2.5 * counts[1])


if __name__ == "__main__":
    unittest.main()
