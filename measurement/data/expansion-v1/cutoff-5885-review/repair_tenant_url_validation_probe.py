import unittest
from solution import tenant_label

class Probe(unittest.TestCase):
    def test_malformed_host_control_character(self):
        with self.assertRaises(ValueError):
            tenant_label('https://a.exa\nmple.com')

    def test_empty_explicit_port(self):
        with self.assertRaises(ValueError):
            tenant_label('https://a.example.com:')

if __name__ == '__main__':
    unittest.main()
