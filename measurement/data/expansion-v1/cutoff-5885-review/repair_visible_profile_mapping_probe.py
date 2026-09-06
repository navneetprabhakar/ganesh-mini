import unittest
from types import MappingProxyType
from solution import select_visible_profiles


class Probe(unittest.TestCase):
    def test_standard_mapping_profile(self):
        profile = MappingProxyType({'x': [1]})
        result = select_visible_profiles([{'id': 'x', 'display_name': '', 'profile': profile}], ['x'])
        self.assertEqual(result[0]['profile'], {'x': [1]})
        self.assertIsNot(result[0]['profile']['x'], profile['x'])


if __name__ == '__main__':
    unittest.main()
