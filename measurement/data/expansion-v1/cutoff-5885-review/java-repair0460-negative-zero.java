public final class SolutionTest {
    public static void main(String[] args) {
        try {
            long[] actual = Solution.decodeLongs("-0");
            throw new AssertionError("Explicitly forbidden -0 accepted as " + java.util.Arrays.toString(actual));
        } catch (IllegalArgumentException expected) {
            // Contract requires rejection.
        }
    }
}
