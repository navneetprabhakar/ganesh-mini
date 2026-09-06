import sys
import unittest

from solution import absent_index


class ComplexityTests(unittest.TestCase):
    def test_whole_function_work_includes_linear_validation(self):
        counts = []
        target = absent_index.__code__
        for size in (256, 512, 1024):
            values = list(range(size))
            count = 0

            def trace(frame, event, arg):
                nonlocal count
                if frame.f_code is target and event == "line":
                    count += 1
                return trace

            sys.settrace(trace)
            try:
                result = absent_index(values, size)
            finally:
                sys.settrace(None)
            self.assertEqual(result, size)
            counts.append(count)
        print("whole-function line events for n=256,512,1024:", counts)
        self.assertLess(counts[2], 1.5 * counts[1])


if __name__ == "__main__":
    unittest.main()
