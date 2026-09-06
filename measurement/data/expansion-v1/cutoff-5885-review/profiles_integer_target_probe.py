import unittest
from solution import advance_profiles


class ProfileIntegerTargetTests(unittest.TestCase):
    def test_empty_profiles_accept_finite_integer_target(self):
        self.assertEqual(advance_profiles([], 10**400), [])


if __name__ == "__main__":
    unittest.main()
