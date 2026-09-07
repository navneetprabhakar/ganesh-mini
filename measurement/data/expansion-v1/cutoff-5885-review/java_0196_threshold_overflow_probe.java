public class SolutionTest {
    public static void main(String[] args) {
        Solution.configure(Integer.MAX_VALUE, 1);
        Solution.add(new Solution.Command("first", 1));
        if (!Solution.committed().isEmpty()) {
            throw new AssertionError("Weight 1 committed below mathematical threshold 1073741824");
        }
    }
}
