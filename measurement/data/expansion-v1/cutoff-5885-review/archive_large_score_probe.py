import unittest
from solution import MemoryArchive


class ArchiveIntegerTests(unittest.TestCase):
    def test_finite_integer_score(self):
        archive = MemoryArchive(1)
        self.assertEqual(archive.record(1, {}, 10 ** 400), ("step-1", "best-1"))


if __name__ == "__main__":
    unittest.main()
