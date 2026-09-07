public class SolutionTest {
    public static void main(String[] args) {
        try {
            Solution.describeChanges(new String[]{"\u2003"}, new String[]{"old"}, new String[]{"new"});
        } catch (IllegalArgumentException expected) { return; }
        throw new AssertionError("blank property name accepted");
    }
}
