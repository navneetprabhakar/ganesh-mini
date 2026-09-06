public class SolutionTest {
    public static void main(String[] args) {
        if (!Character.isWhitespace('\u2003')) throw new AssertionError("whitespace control failed");
        try { new Solution.Member("\u2003"); }
        catch (IllegalArgumentException expected) { return; }
        throw new AssertionError("blank member label accepted");
    }
}
