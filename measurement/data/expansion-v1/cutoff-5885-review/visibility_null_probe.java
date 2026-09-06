import java.util.Arrays;

class SolutionTest {
    public static void main(String[] args) {
        try {
            boolean actual = Solution.allVisible(Arrays.asList(false, null));
            throw new AssertionError("malformed null suffix accepted: " + actual);
        } catch (IllegalArgumentException expected) {
            System.out.println("null suffix rejected as required");
        }
    }
}
