public class SolutionTest {
    public static void main(String[] args) {
        try {
            Solution.cachedSegments("valid:\u2003");
        } catch (IllegalArgumentException expected) { return; }
        throw new AssertionError("blank segment accepted");
    }
}
