public class SolutionTest {
    public static void main(String[] args) {
        if (!Character.isWhitespace('\u2003')) throw new AssertionError("whitespace control failed");
        try { new Solution.Product(1, "\u2003", "category", 1L); }
        catch (IllegalArgumentException expected) { return; }
        throw new AssertionError("blank product name accepted");
    }
}
