import java.util.List;

public final class SolutionTest {
    public static void main(String[] args) {
        List<String> input = List.of("sku|title|section", "A|book|B");
        List<String> expected = List.of("sku|title|section", "A|BOOK|B");
        List<String> actual = Solution.transformCatalog(input, Integer.MAX_VALUE);
        if (!actual.equals(expected)) throw new AssertionError("Expected " + expected + ", got " + actual);
    }
}
