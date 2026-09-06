import unittest
from solution import authorize


class Probe(unittest.TestCase):
    def test_sets_are_not_sequences(self):
        with self.assertRaises(ValueError):
            authorize({'subject': 'user', 'scopes': {'read'}}, ['read'])


if __name__ == '__main__':
    unittest.main()
