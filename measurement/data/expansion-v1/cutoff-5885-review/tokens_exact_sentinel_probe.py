import unittest
from solution import summarize_tokens


class TokensExactSentinelTests(unittest.TestCase):
    def test_sentinel_is_exact_not_numeric_whitespace_rule(self):
        with self.assertRaises(ValueError):
            summarize_tokens(['1', ' STOP'])


if __name__ == '__main__':
    unittest.main()
