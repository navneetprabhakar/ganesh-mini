public class SolutionTest {
    public static void main(String[] args) {
        try {
            new Solution.ResourceKey("\u2003");
        } catch (IllegalArgumentException expected) { return; }
        throw new AssertionError("blank resource key accepted");
    }
}
