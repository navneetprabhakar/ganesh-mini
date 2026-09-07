public class SolutionTest {
    public static void main(String[] args) {
        Solution.Rectangle a = new Solution.Rectangle(Integer.MIN_VALUE, 0, 0, 1);
        Solution.Rectangle b = new Solution.Rectangle(Integer.MAX_VALUE, 0, 0, 1);
        Solution.Rectangle result = Solution.visibleRegion(a, b);
        if (result.width != 0) throw new AssertionError("disjoint intersection must be empty");
    }
}
