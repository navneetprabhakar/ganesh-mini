import java.util.List;
import java.util.Map;

public class SolutionTest {
    public static void main(String[] args) {
        if (!Character.isWhitespace('\u2003')) throw new AssertionError("whitespace control failed");
        List<Solution.Submission> items = List.of(new Solution.Submission("id", "title", "owner"));
        if (Solution.findSubmissions(items, Map.of(), "\u2003").size() != 1) {
            throw new AssertionError("blank user did not return all submissions");
        }
    }
}
