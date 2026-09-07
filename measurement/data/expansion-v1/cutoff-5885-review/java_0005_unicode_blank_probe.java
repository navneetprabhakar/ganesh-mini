public class SolutionTest {
    public static void main(String[] args) {
        boolean rejected=false; try { Solution.addMember(Solution.createRegistry(), 1, "\u2003", "Family"); } catch (IllegalArgumentException expected) { rejected=true; } if (!rejected) throw new AssertionError("blank given name accepted");
    }
}
