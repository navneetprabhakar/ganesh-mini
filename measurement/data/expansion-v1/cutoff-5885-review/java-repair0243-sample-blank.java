public class SolutionTest {
    public static void main(String[] args) {
        try {
            Solution.createSnapshot("\u2003", new String[0]);
        } catch (IllegalArgumentException expected) { return; }
        throw new AssertionError("blank snapshot name accepted");
    }
}
