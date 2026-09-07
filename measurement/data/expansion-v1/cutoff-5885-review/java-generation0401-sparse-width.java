public class SolutionTest {
    private static Solution.Node leaf(Solution.Node root, int index, int depth) {
        Solution.Node node = root;
        for (int bit = depth - 1; bit >= 0; bit--) {
            if (((index >>> bit) & 1) == 0) {
                if (node.left == null) node.left = new Solution.Node(0);
                node = node.left;
            } else {
                if (node.right == null) node.right = new Solution.Node(0);
                node = node.right;
            }
        }
        return node;
    }
    public static void main(String[] args) {
        Solution.Node root = new Solution.Node(0);
        leaf(root, 0, 31);
        leaf(root, 536870912, 31).left = new Solution.Node(0);
        leaf(root, 1610612736, 31).left = new Solution.Node(0);
        int actual = Solution.widestSpan(root);
        if (actual != Integer.MAX_VALUE) {
            throw new AssertionError("expected saturated width, got " + actual);
        }
    }
}
