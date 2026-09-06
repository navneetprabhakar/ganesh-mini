import unittest
from solution import create_credential

class Probe(unittest.TestCase):
    def test_underscores_count_toward_handle_limit(self):
        with self.assertRaises(ValueError):
            create_credential('_'*21, 'a@b.co', 'x', b's')

if __name__ == '__main__':
    unittest.main()
