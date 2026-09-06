import unittest
from solution import Unit


class UnitStateTests(unittest.TestCase):
    def test_invalid_list_state_raises_value_error(self):
        with self.assertRaises(ValueError):
            Unit("worker", [])


if __name__ == "__main__":
    unittest.main()
