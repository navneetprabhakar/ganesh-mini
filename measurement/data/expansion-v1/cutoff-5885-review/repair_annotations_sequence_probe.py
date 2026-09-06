import unittest
from solution import render_annotations


class Probe(unittest.TestCase):
    def test_mapping_is_not_field_sequence(self):
        with self.assertRaises(ValueError):
            render_annotations([{'name': 1, 'type': 2, 'description': 3}])


if __name__ == '__main__':
    unittest.main()
