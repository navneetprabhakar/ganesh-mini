import java.util.concurrent.atomic.AtomicInteger;

public class SolutionTest {
    public static void main(String[] args) throws Exception {
        Solution.acquire("group", "key");
        Solution.acquire("group", "key");
        AtomicInteger observed = new AtomicInteger(-1);
        try {
            Thread observer = new Thread(() -> observed.set(Solution.holdCount("group", "key")));
            observer.start();
            observer.join(2000);
            if (observer.isAlive()) throw new AssertionError("Observer did not finish");
            if (observed.get() != 2) {
                throw new AssertionError("Total reentrant hold count expected 2, got " + observed.get());
            }
        } finally {
            Solution.release("group", "key");
            Solution.release("group", "key");
        }
    }
}
