import unittest
from solution import select_links


class LinkSequenceTests(unittest.TestCase):
    def test_range_endpoint_pair(self):
        self.assertEqual(select_links([(0, 0), (1, 0)], [range(2)], 1),
                         {"edges": [(0, 1)], "cost": 1.0, "degrees": [1, 1]})


if __name__ == "__main__":
    unittest.main()
