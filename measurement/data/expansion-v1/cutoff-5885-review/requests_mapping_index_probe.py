import unittest
from collections import UserDict
from solution import answer_requests


class RequestMappingTests(unittest.TestCase):
    def test_standard_mapping_index(self):
        self.assertEqual(answer_requests(UserDict(A="asset"), ["A"]), ["A: asset"])


if __name__ == "__main__":
    unittest.main()
