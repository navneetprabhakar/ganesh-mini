import unittest
from solution import PermitDesk, AuthenticationError

class PermitHashProbe(unittest.TestCase):
    def test_nonmatching_nonascii_stored_hash_is_authentication_error(self):
        desk = PermitDesk([{'identifier': 'a', 'pin_hash': 'é', 'profile': {}}])
        with self.assertRaises(AuthenticationError):
            desk.login('a', 'pin')

if __name__ == '__main__':
    unittest.main()
