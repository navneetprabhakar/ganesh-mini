import java.util.AbstractList;
import java.util.List;

public final class SolutionTest {
    public static void main(String[] args) {
        List<String> virtual = new AbstractList<>() {
            public int size() { return Integer.MAX_VALUE; }
            public String get(int index) {
                if (index < 0 || index >= size()) throw new IndexOutOfBoundsException();
                return "row";
            }
        };
        List<String> page = Solution.slice(virtual, 2_147_484, 1000);
        if (page.size() != 647) throw new AssertionError("Expected 647 rows, got " + page.size());
    }
}
