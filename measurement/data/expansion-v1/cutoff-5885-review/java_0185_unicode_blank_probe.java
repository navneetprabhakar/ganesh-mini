public class SolutionTest {
    public static void main(String[] args) {
        if (!Character.isWhitespace('\u2003')) throw new AssertionError("whitespace control failed");
        try { Solution.upsert(java.util.List.of(), new Solution.Item(1, "\u2003")); }
        catch (IllegalArgumentException expected) { return; }
        throw new AssertionError("blank item title accepted");
    }
}
