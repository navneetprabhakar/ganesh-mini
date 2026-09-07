public class SolutionTest {
    public static void main(String[] args) {
        if (Solution.averageValidIntegers(new String[]{"\u20031\u2003"}).orElse(-1) != 1) throw new AssertionError("U+2003 whitespace was not removed");
    }
}
