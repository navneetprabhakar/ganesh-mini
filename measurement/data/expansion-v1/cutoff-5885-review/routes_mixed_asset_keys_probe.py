import unittest
from solution import compile_routes


class AssetValidationTests(unittest.TestCase):
    def test_mixed_asset_key_types_raise_value_error(self):
        with self.assertRaises(ValueError):
            compile_routes([], {"/x": lambda: None, 1: lambda: None})


if __name__ == "__main__":
    unittest.main()
