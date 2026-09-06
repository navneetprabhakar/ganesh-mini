import unittest
from solution import order_entries


class OrderPolicyTests(unittest.TestCase):
    def test_unhashable_policy_has_required_error(self):
        with self.assertRaisesRegex(ValueError, "^invalid policy$"):
            order_entries([], [])


if __name__ == "__main__":
    unittest.main()
