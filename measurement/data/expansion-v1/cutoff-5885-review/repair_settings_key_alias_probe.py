import unittest
from solution import merge_settings


class Key:
    def __init__(self):
        self.metadata = []


class Probe(unittest.TestCase):
    def test_overlay_key_is_detached(self):
        key = Key()
        result = merge_settings({}, {key: 1})
        copied_key = next(iter(result))
        self.assertIsNot(copied_key, key)
        copied_key.metadata.append('changed')
        self.assertEqual(key.metadata, [])


if __name__ == '__main__':
    unittest.main()
