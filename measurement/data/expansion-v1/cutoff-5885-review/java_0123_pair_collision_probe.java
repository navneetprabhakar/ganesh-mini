public class SolutionTest {
    public static void main(String[] args) {
        Solution.clear();
        if (!Solution.send("a", "b\u0000c")) throw new AssertionError("send");
        if (!Solution.decide("a", "b\u0000c", Solution.Decision.ACCEPTED)) {
            throw new AssertionError("accept");
        }
        if (Solution.connected("a\u0000b", "c")) {
            throw new AssertionError("Unrelated identifiers collide with the accepted pair");
        }
    }
}
