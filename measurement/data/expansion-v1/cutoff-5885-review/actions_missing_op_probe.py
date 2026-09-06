import unittest
from solution import apply_actions


class MissingOperationTests(unittest.TestCase):
    def test_missing_key_raises_value_error(self):
        with self.assertRaises(ValueError):
            apply_actions([{"owner": "a"}])


if __name__ == "__main__":
    unittest.main()
