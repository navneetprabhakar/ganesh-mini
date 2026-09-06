import unittest
from collections import defaultdict
from solution import read_required, ConfigError


class ReviewProbe(unittest.TestCase):
    def test_missing_key_in_standard_mapping(self):
        config = defaultdict(list)
        with self.assertRaises(ConfigError):
            read_required(config, ['missing'])


if __name__ == '__main__':
    unittest.main()
