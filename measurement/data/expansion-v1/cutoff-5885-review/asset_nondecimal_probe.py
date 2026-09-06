import unittest
from solution import resolve_asset


class AssetNondecimalTests(unittest.TestCase):
    def test_malformed_numeric_path_returns_bad_request(self):
        response = resolve_asset({}, '/v1/bundles/x/symbols/f/²-3')
        self.assertEqual(response['status'], 400)


if __name__ == '__main__':
    unittest.main()
