import tracemalloc
import unittest
from solution import locate_loop

class Probe(unittest.TestCase):
    def test_constant_auxiliary_space(self):
        links = [None] * 200000
        tracemalloc.start()
        try:
            self.assertIsNone(locate_loop(links, None))
            current, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        # Input allocated before tracing. A copied 200000-pointer tuple is
        # approximately 1.6MB; allow 128KiB for constant bookkeeping.
        self.assertLess(peak, 128*1024)

if __name__ == '__main__':
    unittest.main()
