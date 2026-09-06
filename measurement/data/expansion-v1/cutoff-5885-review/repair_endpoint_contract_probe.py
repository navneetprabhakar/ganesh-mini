import unittest
from solution import endpoint_plan


class Probe(unittest.TestCase):
    def test_address_requires_string(self):
        for args in ((1, 80), (True, 80), ('127.0.0.1', 80, 1)):
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    endpoint_plan(*args)

    def test_bind_preserves_supplied_address(self):
        bind = '2001:0db8:0:0:0:0:0:1'
        self.assertEqual(endpoint_plan(bind, 80)['bind'], (bind, 80))


if __name__ == '__main__':
    unittest.main()
