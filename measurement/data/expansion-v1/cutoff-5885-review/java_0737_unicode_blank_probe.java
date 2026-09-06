public class SolutionTest {
    public static void main(String[] args) {
        if (!Character.isWhitespace('\u2003')) throw new AssertionError("whitespace control failed");
        String owner = Solution.identify("/", java.util.Map.of("Authorization", "Token k"), java.util.Map.of(), java.util.Set.of(), java.util.Map.of("k", "\u2003"));
        if (!owner.isEmpty()) throw new AssertionError("blank credential owner returned");
    }
}
