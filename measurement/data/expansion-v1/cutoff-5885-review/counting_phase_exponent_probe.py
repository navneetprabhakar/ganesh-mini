import unittest
from solution import build_counting_plan


class PhaseExponentTests(unittest.TestCase):
    def test_phase_uses_target_minus_source(self):
        self.assertEqual(build_counting_plan(2)[3], (("mix", 0), ("phase", 1, 0, 1), ("mix", 1)))


if __name__ == "__main__":
    unittest.main()
