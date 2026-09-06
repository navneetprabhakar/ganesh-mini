import unittest

from solution import merge_snapshot


class SharedDefaultTests(unittest.TestCase):
    def test_override_does_not_change_other_path(self):
        shared = {"value": 1}
        defaults = {"a": shared, "b": shared}
        result = merge_snapshot(defaults, {"a": {"value": 2}}, [])
        self.assertEqual(result, {"a": {"value": 2}, "b": {"value": 1}})
        self.assertEqual(shared, {"value": 1})


if __name__ == "__main__":
    unittest.main()
