public class SolutionTest {
    public static void main(String[] args) {
        if (Solution.findPng(java.util.Map.of("\u2003x.png", new byte[]{1}), "\u2003x.png").isPresent()) throw new AssertionError("leading U+2003 accepted");
    }
}
