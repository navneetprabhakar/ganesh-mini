import unittest
from solution import resolve_inventory_request


class UnmatchedMethodTests(unittest.TestCase):
    def test_unsupported_method_does_not_parse_unbounded_id(self):
        self.assertIsNone(resolve_inventory_request("PATCH", "/items/" + "1" * 5000 + "/"))


if __name__ == "__main__":
    unittest.main()
