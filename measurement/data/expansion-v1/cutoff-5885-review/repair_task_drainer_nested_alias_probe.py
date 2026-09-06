import unittest
from solution import TaskDrainer

class Probe(unittest.TestCase):
    def test_later_nested_caller_mutation(self):
        value = [1]
        drainer = TaskDrainer([value])
        before = drainer.drain()
        value.append(2)
        self.assertEqual(drainer.drain(), before)

if __name__ == '__main__':
    unittest.main()
