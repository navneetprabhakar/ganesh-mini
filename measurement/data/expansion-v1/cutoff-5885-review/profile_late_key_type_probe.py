import unittest
from solution import profile_is_complete


class ProfileLateKeyTypeTests(unittest.TestCase):
    def test_all_requested_key_types_validated(self):
        with self.assertRaises(TypeError):
            profile_is_complete({}, ['missing', 3])


if __name__ == '__main__':
    unittest.main()
