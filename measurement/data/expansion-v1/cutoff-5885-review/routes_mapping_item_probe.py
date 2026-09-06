import unittest
from solution import compile_routes


class RouteItemTests(unittest.TestCase):
    def test_mapping_is_not_two_element_sequence(self):
        with self.assertRaises(TypeError):
            compile_routes([{"path": "a", "handler": "h"}])


if __name__ == "__main__":
    unittest.main()
