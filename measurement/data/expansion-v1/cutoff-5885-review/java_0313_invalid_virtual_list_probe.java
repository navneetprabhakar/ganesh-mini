import java.util.Collections;
import java.util.List;

public class SolutionTest {
    public static void main(String[] args) {
        List<Solution.Message> invalid = Collections.nCopies(Integer.MAX_VALUE, null);
        try { Solution.append(invalid, List.of(), 0); }
        catch (IllegalArgumentException expected) { return; }
        throw new AssertionError("null messages not rejected");
    }
}
