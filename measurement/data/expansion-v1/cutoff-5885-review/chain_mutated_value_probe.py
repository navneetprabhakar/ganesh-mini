import unittest
from solution import ChainNode, merge_sorted_chains


class ChainValueTests(unittest.TestCase):
    def test_public_node_value_is_revalidated_before_merge(self):
        node = ChainNode(1)
        node.value = True
        with self.assertRaises(ValueError):
            merge_sorted_chains([node])


if __name__ == "__main__":
    unittest.main()
