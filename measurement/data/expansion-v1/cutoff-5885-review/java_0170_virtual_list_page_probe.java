import java.util.Collections;
import java.util.List;

public class SolutionTest {
    static final class Item implements Solution.Freezable<Item> {
        int calls;
        public Item freeze() { calls++; return this; }
    }
    public static void main(String[] args) {
        Item item = new Item();
        List<Item> input = Collections.nCopies(Integer.MAX_VALUE, item);
        List<Item> result = Solution.frozenPage(input, Integer.MAX_VALUE - 1, 1);
        if (result.size() != 1 || result.get(0) != item || item.calls != 1) {
            throw new AssertionError("final one-element virtual page incorrect");
        }
    }
}
