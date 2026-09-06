import unittest
from solution import privileged_tasks

class Probe(unittest.TestCase):
    def test_mixed_container_types(self):
        self.assertEqual(privileged_tasks(('a',), ['1|a|x']), [{'pid': 1, 'owner': 'a', 'name': 'x'}])

    def test_valid_large_pid(self):
        self.assertEqual(privileged_tasks(['a'], ['1' + '0'*4999 + '|a|x'])[0]['pid'], 10**4999)

    def test_nondecimal_digit_is_skipped(self):
        self.assertEqual(privileged_tasks(['a'], ['²|a|x']), [])

if __name__ == '__main__':
    unittest.main()
