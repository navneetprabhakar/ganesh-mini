public class SolutionTest {
    public static void main(String[] args) {
        if (!Character.isWhitespace('\u2003')) throw new AssertionError("whitespace control failed");
        Solution.Catalog catalog = new Solution.Catalog(java.util.Map.of(1L, "c"), java.util.Map.of(1L, "t"), new java.util.LinkedHashMap<>());
        try { Solution.create(catalog, new Solution.Article(1L, "\u2003", java.util.List.of(1L), java.util.List.of(1L))); }
        catch (IllegalArgumentException expected) { return; }
        throw new AssertionError("whitespace-only article title accepted");
    }
}
