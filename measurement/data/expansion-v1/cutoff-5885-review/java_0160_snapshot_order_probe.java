import java.util.Arrays;

public class SolutionTest {
    public static void main(String[] args) {
        Solution.clear();
        if (!Solution.write("A", "x") || !Solution.write("A0", "y")) {
            throw new AssertionError("valid writes rejected");
        }
        String[] actual = Solution.snapshot();
        String[] expected = {"A=x", "A0=y"};
        if (!Arrays.equals(expected, actual)) {
            throw new AssertionError("Expected key order " + Arrays.toString(expected)
                    + " but received " + Arrays.toString(actual));
        }
    }
}
