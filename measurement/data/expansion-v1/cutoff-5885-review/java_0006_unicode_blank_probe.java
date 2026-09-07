public class SolutionTest {
    public static void main(String[] args) {
        boolean rejected=false; try { new Solution.Profile("\u2003", java.util.List.of()); } catch (IllegalArgumentException expected) { rejected=true; } if (!rejected) throw new AssertionError("blank handle accepted");
    }
}
