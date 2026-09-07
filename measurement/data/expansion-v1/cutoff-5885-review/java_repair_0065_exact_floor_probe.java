public class SolutionTest {
    public static void main(String[] args) {
        int[] got = Solution.fitSize(100, 100, 29, 29);
        if (got[0] != 29 || got[1] != 29)
            throw new AssertionError("expected [29,29], got " + java.util.Arrays.toString(got));
    }
}
