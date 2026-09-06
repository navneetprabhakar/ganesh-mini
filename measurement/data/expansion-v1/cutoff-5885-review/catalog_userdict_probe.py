import unittest
from collections import UserDict
from solution import catalog_snapshot


class CatalogMappingTests(unittest.TestCase):
    def test_mapping_item(self):
        result = catalog_snapshot([UserDict(id="a", title="A", votes=1)], [], 1, 10)
        self.assertEqual(result["item_total"], 1)


if __name__ == "__main__":
    unittest.main()
