public class SolutionTest {
    public static void main(String[] args) {
        if (!"0".equals(Solution.fold("\u2003"))) {
            throw new AssertionError("whitespace-only input must return zero");
        }
    }
}
