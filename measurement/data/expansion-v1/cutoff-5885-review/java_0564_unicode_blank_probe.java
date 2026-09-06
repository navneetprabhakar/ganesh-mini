import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.atomic.AtomicInteger;

public class SolutionTest {
    public static void main(String[] args) {
        if (!Character.isWhitespace('\u2003')) throw new AssertionError("whitespace control failed");
        AtomicInteger calls = new AtomicInteger();
        Solution.loadBadges("\u2003", key -> {
            calls.incrementAndGet();
            return CompletableFuture.completedFuture(List.of());
        }).join();
        if (calls.get() != 0) throw new AssertionError("loader invoked for blank key");
    }
}
