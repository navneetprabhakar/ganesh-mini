import unittest

from solution import TreeNode, mirror_copy


class DeepTreeTests(unittest.TestCase):
    def test_valid_deep_tree(self):
        root = None
        for value in range(1500):
            root = TreeNode(value, left=root)
        result = mirror_copy(root)
        source = root
        count = 0
        while source is not None:
            self.assertIsNot(result, source)
            self.assertIs(result.value, source.value)
            self.assertIsNone(result.left)
            source, result = source.left, result.right
            count += 1
        self.assertIsNone(result)
        self.assertEqual(count, 1500)


if __name__ == "__main__":
    unittest.main()
