import unittest
from solution import sanitize_session_descriptor


class ReviewProbe(unittest.TestCase):
    def test_other_values_preserved_when_preferences_shared(self):
        preferences = {'debug': True, 'automation': True}
        profile = {'preferences': preferences, 'other': preferences}
        result = sanitize_session_descriptor(profile)
        self.assertEqual(result['preferences'], {'automation': False})
        self.assertEqual(result['other'], {'debug': True, 'automation': True})
        self.assertEqual(preferences, {'debug': True, 'automation': True})


if __name__ == '__main__':
    unittest.main()
