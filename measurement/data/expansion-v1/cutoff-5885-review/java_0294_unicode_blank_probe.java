public class SolutionTest {
    public static void main(String[] args) {
        if (!Character.isWhitespace('\u2003')) throw new AssertionError("whitespace control failed");
        try { new Solution.Clip("id", "\u2003", "creator"); }
        catch (IllegalArgumentException expected) { return; }
        throw new AssertionError("blank clip title accepted");
    }
}
