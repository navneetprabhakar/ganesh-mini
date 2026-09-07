public class SolutionTest {
    public static void main(String[] args) {
        String actual = Solution.parseInfix("-02147483648").toString();
        if (!"-2147483648".equals(actual)) {
            throw new AssertionError("minimum signed integer was not preserved: " + actual);
        }
    }
}
