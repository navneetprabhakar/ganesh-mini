import unittest
from solution import make_web_config


class EnvironmentValidationTests(unittest.TestCase):
    def test_unhashable_unknown_environment(self):
        with self.assertRaises(ValueError):
            make_web_config([], {"DATABASE_URL": "x"})


if __name__ == "__main__":
    unittest.main()
