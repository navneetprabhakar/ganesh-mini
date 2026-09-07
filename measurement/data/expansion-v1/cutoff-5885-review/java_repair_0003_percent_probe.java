public class SolutionTest {
    public static void main(String[] args) {
        java.util.Map<String,Integer> got=Solution.ownershipPercent(java.util.Collections.nCopies(22000000,"A")); if(got.get("A")!=100) throw new AssertionError("expected 100 percent, got "+got.get("A"));
    }
}
