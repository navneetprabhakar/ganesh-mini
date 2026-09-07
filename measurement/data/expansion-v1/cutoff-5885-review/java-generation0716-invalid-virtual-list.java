import java.util.Collections;

public class SolutionTest {
    public static void main(String[] args) {
        try {
            new Solution.SliceBook<String>(Collections.nCopies(Integer.MAX_VALUE, null), 1);
        } catch (IllegalArgumentException expected) { return; }
        throw new AssertionError("null element must be rejected");
    }
}
